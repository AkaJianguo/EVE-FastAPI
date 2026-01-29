#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成 whats_new 报告
独立脚本：下载新旧版本的 JSONL 文件，进行比对，生成报告
"""

import json
import os
import sys
import zipfile
import shutil
from pathlib import Path
from typing import Dict, Any, Optional

# 添加项目根目录到 Python 路径，以便导入 utils 和 scripts 模块
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from utils.http_client import get
import scripts.item_changes_analyzer as item_changes_analyzer


def load_config() -> Optional[Dict[str, Any]]:
    """加载配置文件"""
    # 使用全局的 project_root
    config_path = project_root / "config.json"
    
    if not config_path.exists():
        print(f"[x] 配置文件不存在: {config_path}")
        return None
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"[x] 加载配置文件失败: {e}")
        return None


def get_latest_release_info(github_repo: str) -> Optional[Dict[str, Any]]:
    """获取最新 Release 信息"""
    try:
        headers = {
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'EVE-SDE-Processor'
        }
        
        repo_url = f"https://api.github.com/repos/{github_repo}/releases/latest"
        response = get(repo_url, headers=headers, timeout=30)
        
        release_info = response.json()
        if release_info and not release_info.get('draft', False) and not release_info.get('prerelease', False):
            return release_info
        
        return None
    except Exception as e:
        print(f"[!] 获取最新 Release 信息失败: {e}")
        return None


def extract_build_number_from_tag(tag_name: str) -> Optional[str]:
    """从 tag_name 中提取 build_number"""
    if tag_name.startswith('sde-build-'):
        return tag_name.replace('sde-build-', '')
    return None


def download_and_extract_jsonl(config: Dict[str, Any], build_number: str, output_dir: Path) -> Optional[Path]:
    """下载并解压指定版本的 JSONL 压缩包"""
    try:
        download_url = config["urls"]["sde_download_template"].format(build_number=build_number)
        zip_filename = f"eve-online-static-data-{build_number}-jsonl.zip"
        zip_path = output_dir / zip_filename
        extract_to = output_dir / f"jsonl_{build_number}"
        
        print(f"[+] 开始下载 build {build_number} 的 JSONL 文件...")
        print(f"    下载地址: {download_url}")
        
        # 如果已解压，直接返回
        if extract_to.exists() and (extract_to / "types.jsonl").exists():
            print(f"[+] 使用已存在的 JSONL 文件: {extract_to}")
            return extract_to
        
        # 下载
        response = get(download_url, stream=True, timeout=300, verify=False)
        
        with open(zip_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        
        print(f"[+] 下载完成: {zip_path}")
        
        # 解压
        print(f"[+] 开始解压到: {extract_to}")
        extract_to.mkdir(parents=True, exist_ok=True)
        
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        
        print(f"[+] 解压完成")
        
        # 清理压缩包
        zip_path.unlink()
        
        return extract_to
        
    except Exception as e:
        print(f"[x] 下载或解压失败: {e}")
        if zip_path.exists():
            zip_path.unlink()
        return None


def get_current_build_number(config: Dict[str, Any]) -> Optional[str]:
    """获取当前版本的 build_number"""
    # 优先从环境变量获取（GitHub Actions 会设置）
    build_number = os.environ.get('FINAL_BUILD_NUMBER') or os.environ.get('BUILD_NUMBER')
    if build_number:
        return str(build_number)
    
    # 从 build_info.json 读取
    # 使用全局的 project_root
    sde_jsonl_path = project_root / config["paths"]["sde_jsonl"]
    build_info_path = sde_jsonl_path / "build_info.json"
    
    if build_info_path.exists():
        try:
            with open(build_info_path, 'r', encoding='utf-8') as f:
                build_info = json.load(f)
                build_number = build_info.get('build_number') or build_info.get('buildNumber')
                if build_number:
                    return str(build_number)
        except Exception as e:
            print(f"[!] 读取 build_info.json 失败: {e}")
    
    # 从 _sde.jsonl 读取
    sde_info_file = sde_jsonl_path / "_sde.jsonl"
    if sde_info_file.exists():
        try:
            with open(sde_info_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        data = json.loads(line)
                        build_number = data.get('buildNumber') or data.get('build_number')
                        if build_number:
                            return str(build_number)
        except Exception as e:
            print(f"[!] 读取 _sde.jsonl 失败: {e}")
    
    return None


def verify_jsonl_files(jsonl_path: Path) -> bool:
    """验证 JSONL 文件是否完整"""
    required_files = [
        "types.jsonl",
        "groups.jsonl",
        "categories.jsonl",
        "blueprints.jsonl",
        "typeDogma.jsonl",
        "dogmaAttributes.jsonl"
    ]
    
    for file_name in required_files:
        if not (jsonl_path / file_name).exists():
            print(f"[x] 缺少必需文件: {file_name}")
            return False
    
    return True


def main():
    """主函数"""
    print("=" * 60)
    print("生成 whats_new 报告")
    print("=" * 60)
    print()
    
    # 加载配置
    config = load_config()
    if not config:
        print("[x] 无法加载配置文件，退出")
        sys.exit(1)
    
    github_repo = config.get('github_repo', '')
    if not github_repo:
        print("[x] 配置文件中缺少 github_repo，退出")
        sys.exit(1)
    
    # 获取当前版本的 build_number
    current_build_number = get_current_build_number(config)
    if not current_build_number:
        print("[x] 无法获取当前版本的 build_number，退出")
        sys.exit(1)
    
    print(f"[+] 当前版本 build_number: {current_build_number}")
    
    # 获取上一版本的 build_number
    release_info = get_latest_release_info(github_repo)
    if not release_info:
        print("[!] 无法获取最新 Release 信息，可能是首次构建")
        print("[!] 跳过 whats_new 报告生成")
        sys.exit(0)  # 首次构建不算错误，正常退出
    
    prev_tag = release_info.get('tag_name', '')
    old_build_number = extract_build_number_from_tag(prev_tag)
    
    if not old_build_number:
        print(f"[!] 无法从 tag_name ({prev_tag}) 中提取 build_number")
        print("[!] 跳过 whats_new 报告生成")
        sys.exit(0)
    
    print(f"[+] 上一版本 build_number: {old_build_number}")
    print()
    
    # 创建临时目录
    temp_dir = project_root / "temp_whats_new"
    temp_dir.mkdir(exist_ok=True)
    
    try:
        # 下载并解压当前版本的 JSONL（如果本地不存在）
        current_jsonl_path = project_root / config["paths"]["sde_jsonl"]
        if not verify_jsonl_files(current_jsonl_path):
            print("[+] 当前版本 JSONL 文件不完整，开始下载...")
            current_jsonl_path = download_and_extract_jsonl(config, current_build_number, temp_dir)
            if not current_jsonl_path:
                print("[x] 下载当前版本 JSONL 失败")
                sys.exit(1)
        else:
            print("[+] 使用本地当前版本 JSONL 文件")
        
        # 验证当前版本 JSONL 文件
        if not verify_jsonl_files(current_jsonl_path):
            print("[x] 当前版本 JSONL 文件不完整")
            sys.exit(1)
        
        # 下载并解压上一版本的 JSONL
        print()
        print(f"[+] 开始下载上一版本 (build {old_build_number}) 的 JSONL 文件...")
        old_jsonl_path = download_and_extract_jsonl(config, old_build_number, temp_dir)
        if not old_jsonl_path:
            print("[x] 下载上一版本 JSONL 失败")
            sys.exit(1)
        
        # 验证上一版本 JSONL 文件
        if not verify_jsonl_files(old_jsonl_path):
            print("[x] 上一版本 JSONL 文件不完整")
            sys.exit(1)
        
        # 生成文件名格式：whats_new_{old_build_number}_{new_build_number}.md
        whats_new_filename = f"whats_new_{old_build_number}_{current_build_number}.md"
        whats_new_dir = project_root / "whats_new"
        whats_new_dir.mkdir(parents=True, exist_ok=True)
        whats_new_path = whats_new_dir / whats_new_filename
        
        print()
        print(f"[+] 开始生成 whats_new 报告...")
        print(f"    输出文件: {whats_new_path}")
        
        # 调用 item_changes_analyzer 生成报告
        success = item_changes_analyzer.main(
            config,
            old_jsonl_path,
            current_jsonl_path,
            whats_new_path
        )
        
        if not success:
            print("[x] 生成 whats_new 报告失败")
            sys.exit(1)
        
        if not whats_new_path.exists():
            print("[x] whats_new 报告文件未生成")
            sys.exit(1)
        
        print()
        print(f"[+] whats_new 报告生成成功!")
        print(f"    文件路径: {whats_new_path}")
        print(f"    文件名: {whats_new_filename}")
        
        # 清理临时目录
        if temp_dir.exists():
            print()
            print("[+] 清理临时文件...")
            shutil.rmtree(temp_dir)
        
        print()
        print("[+] 完成")
        return True
        
    except Exception as e:
        print(f"[x] 生成 whats_new 报告时出错: {e}")
        import traceback
        traceback.print_exc()
        
        # 清理临时目录
        if temp_dir.exists():
            shutil.rmtree(temp_dir)
        
        sys.exit(1)


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

