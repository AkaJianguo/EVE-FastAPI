#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将 SDE SQLite 数据迁移到 PostgreSQL raw schema。

默认：
- SQLite: sde-processor/output_sde/db/item_db_zh.sqlite
- PG: postgresql://postgres:root@localhost:15432/ruoyi-fastapi
"""

from __future__ import annotations

import argparse
import sqlite3
from pathlib import Path
from typing import Iterable, Sequence

import psycopg2
from psycopg2 import sql
from psycopg2.extras import execute_values

DEFAULT_SQLITE_PATH = Path("sde-processor/output_sde/db/item_db_zh.sqlite")
DEFAULT_PG_DSN = "postgresql://postgres:root@localhost:15432/ruoyi-fastapi"
DEFAULT_SCHEMA = "raw"
DEFAULT_BATCH_SIZE = 1000


def map_sqlite_type(sqlite_type: str | None) -> str:
    if not sqlite_type:
        return "TEXT"
    t = sqlite_type.lower()
    if "int" in t:
        return "BIGINT"
    if "bool" in t:
        return "BOOLEAN"
    if "char" in t or "text" in t or "clob" in t:
        return "TEXT"
    if "real" in t or "floa" in t or "doub" in t:
        return "DOUBLE PRECISION"
    if "blob" in t:
        return "BYTEA"
    if "date" in t or "time" in t:
        return "TIMESTAMP"
    if "numeric" in t or "dec" in t:
        return "NUMERIC"
    return "TEXT"


def get_sqlite_tables(conn: sqlite3.Connection) -> Sequence[str]:
    cursor = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name"
    )
    return [row[0] for row in cursor.fetchall()]


def get_table_columns(conn: sqlite3.Connection, table: str) -> Sequence[dict]:
    cursor = conn.execute(f'PRAGMA table_info("{table}")')
    columns = []
    for cid, name, col_type, notnull, default_value, pk in cursor.fetchall():
        columns.append(
            {
                "cid": cid,
                "name": name,
                "type": col_type,
                "notnull": bool(notnull),
                "default": default_value,
                "pk": pk,
            }
        )
    return columns


def create_schema(pg_cursor, schema: str) -> None:
    pg_cursor.execute(sql.SQL("CREATE SCHEMA IF NOT EXISTS {};").format(sql.Identifier(schema)))


def create_table(pg_cursor, schema: str, table: str, columns: Sequence[dict]) -> None:
    column_defs: list[sql.Composed] = []
    pk_columns = sorted([c for c in columns if c["pk"]], key=lambda c: c["pk"])

    for col in columns:
        col_parts: list[sql.SQL | sql.Identifier] = [
            sql.Identifier(col["name"]),
            sql.SQL(map_sqlite_type(col["type"])),
        ]
        if col["notnull"]:
            col_parts.append(sql.SQL("NOT NULL"))
        column_defs.append(sql.SQL(" ").join(col_parts))

    if pk_columns:
        pk_clause = sql.SQL("PRIMARY KEY ({})").format(
            sql.SQL(", ").join(sql.Identifier(c["name"]) for c in pk_columns)
        )
        column_defs.append(pk_clause)

    create_stmt = sql.SQL("CREATE TABLE IF NOT EXISTS {}.{} ({})").format(
        sql.Identifier(schema),
        sql.Identifier(table),
        sql.SQL(", ").join(column_defs),
    )
    pg_cursor.execute(create_stmt)


def truncate_table(pg_cursor, schema: str, table: str) -> None:
    pg_cursor.execute(
        sql.SQL("TRUNCATE TABLE {}.{};").format(sql.Identifier(schema), sql.Identifier(table))
    )


def fetch_sqlite_rows(
    conn: sqlite3.Connection, table: str, batch_size: int
) -> Iterable[list[tuple]]:
    cursor = conn.execute(f'SELECT * FROM "{table}"')
    while True:
        rows = cursor.fetchmany(batch_size)
        if not rows:
            break
        yield rows


def insert_rows(
    pg_cursor,
    schema: str,
    table: str,
    columns: Sequence[str],
    rows: Sequence[tuple],
) -> None:
    insert_stmt = sql.SQL("INSERT INTO {}.{} ({}) VALUES %s").format(
        sql.Identifier(schema),
        sql.Identifier(table),
        sql.SQL(", ").join(sql.Identifier(c) for c in columns),
    )
    execute_values(pg_cursor, insert_stmt, rows, page_size=len(rows))


def migrate(sqlite_path: Path, pg_dsn: str, schema: str, batch_size: int, truncate: bool) -> None:
    if not sqlite_path.exists():
        raise FileNotFoundError(f"SQLite 文件不存在: {sqlite_path}")

    sqlite_conn = sqlite3.connect(sqlite_path)
    sqlite_conn.row_factory = sqlite3.Row

    with psycopg2.connect(pg_dsn) as pg_conn:
        with pg_conn.cursor() as pg_cursor:
            create_schema(pg_cursor, schema)
            pg_conn.commit()

            tables = get_sqlite_tables(sqlite_conn)
            for table in tables:
                columns = get_table_columns(sqlite_conn, table)
                if not columns:
                    continue

                create_table(pg_cursor, schema, table, columns)
                if truncate:
                    truncate_table(pg_cursor, schema, table)
                pg_conn.commit()

                column_names = [col["name"] for col in columns]
                total_rows = 0
                for rows in fetch_sqlite_rows(sqlite_conn, table, batch_size):
                    insert_rows(pg_cursor, schema, table, column_names, rows)
                    total_rows += len(rows)
                    pg_conn.commit()

                print(f"[OK] {table}: {total_rows} rows migrated")

    sqlite_conn.close()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Sync SDE SQLite -> PostgreSQL raw schema")
    parser.add_argument(
        "--sqlite",
        default=str(DEFAULT_SQLITE_PATH),
        help="SQLite 文件路径",
    )
    parser.add_argument(
        "--pg",
        default=DEFAULT_PG_DSN,
        help="PostgreSQL DSN",
    )
    parser.add_argument(
        "--schema",
        default=DEFAULT_SCHEMA,
        help="目标 schema（默认 raw）",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=DEFAULT_BATCH_SIZE,
        help="每批插入行数",
    )
    parser.add_argument(
        "--truncate",
        action="store_true",
        help="迁移前清空目标表",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    migrate(Path(args.sqlite), args.pg, args.schema, args.batch_size, args.truncate)


if __name__ == "__main__":
    main()
