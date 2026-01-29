# EVE SDE Build 3096543.01 - 版本比较报告

**构建时间**: 2025-11-15 10:50:18

## 图标文件比较

**文件统计**:
- 当前版本: 10097 个文件
- 旧版本: 10097 个文件
- 新增: 0 个文件
- 删除: 0 个文件
- 共同: 10097 个文件

## 数据库比较

### EN 数据库

**数据库差异**:
```sql
CREATE TABLE ore_colors (
                type_id INTEGER PRIMARY KEY,
                hex_color TEXT NOT NULL,
                FOREIGN KEY (type_id) REFERENCES types(type_id)
            );
INSERT INTO ore_colors(type_id,hex_color) VALUES(18,'#cf8e52');
INSERT INTO ore_colors(type_id,hex_color) VALUES(19,'#d30c04');
INSERT INTO ore_colors(type_id,hex_color) VALUES(20,'#854c0c');
INSERT INTO ore_colors(type_id,hex_color) VALUES(21,'#07f0df');
INSERT INTO ore_colors(type_id,hex_color) VALUES(22,'#ee3001');
INSERT INTO ore_colors(type_id,hex_color) VALUES(1223,'#68e55b');
INSERT INTO ore_colors(type_id,hex_color) VALUES(1224,'#a7794f');
INSERT INTO ore_colors(type_id,hex_color) VALUES(1225,'#e69e18');
INSERT INTO ore_colors(type_id,hex_color) VALUES(1226,'#a1d5ec');
INSERT INTO ore_colors(type_id,hex_color) VALUES(1227,'#cbb552');
INSERT INTO ore_colors(type_id,hex_color) VALUES(1228,'#846436');
INSERT INTO ore_colors(type_id,hex_color) VALUES(1229,'#12df4a');
INSERT INTO ore_colors(type_id,hex_color) VALUES(1230,'#d08967');
INSERT INTO ore_colors(type_id,hex_color) VALUES(1231,'#77acd5');
INSERT INTO ore_colors(type_id,hex_color) VALUES(1232,'#a79c70');
INSERT INTO ore_colors(type_id,hex_color) VALUES(11396,'#cd2810');
INSERT INTO ore_colors(type_id,hex_color) VALUES(16262,'#426274');
INSERT INTO ore_colors(type_id,hex_color) VALUES(16263,'#5bbfce');
INSERT INTO ore_colors(type_id,hex_color) VALUES(16264,'#3985ad');
INSERT INTO ore_colors(type_id,hex_color) VALUES(16265,'#4a6a84');
INSERT INTO ore_colors(type_id,hex_color) VALUES(16266,'#4a86a5');
INSERT INTO ore_colors(type_id,hex_color) VALUES(16267,'#527a9d');
INSERT INTO ore_colors(type_id,hex_color) VALUES(16268,'#4db8bb');
INSERT INTO ore_colors(type_id,hex_color) VALUES(16269,'#186194');
INSERT INTO ore_colors(type_id,hex_color) VALUES(17425,'#ee3001');
INSERT INTO ore_colors(type_id,hex_color) VALUES(17426,'#ee3001');
INSERT INTO ore_colors(type_id,hex_color) VALUES(17428,'#68e55b');
INSERT INTO ore_colors(type_id,hex_color) VALUES(17429,'#68e55b');
INSERT INTO ore_colors(type_id,hex_color) VALUES(17432,'#e69e18');
INSERT INTO ore_colors(type_id,hex_color) VALUES(17433,'#e69e18');
INSERT INTO ore_colors(type_id,hex_color) VALUES(17436,'#a79c70');
INSERT INTO ore_colors(type_id,hex_color) VALUES(17437,'#a79c70');
INSERT INTO ore_colors(type_id,hex_color) VALUES(17440,'#07f0df');
INSERT INTO ore_colors(type_id,hex_color) VALUES(17441,'#07f0df');
INSERT INTO ore_colors(type_id,hex_color) VALUES(17444,'#77acd5');
INSERT INTO ore_colors(type_id,hex_color) VALUES(17445,'#77acd5');
INSERT INTO ore_colors(type_id,hex_color) VALUES(17448,'#a1d5ec');
INSERT INTO ore_colors(type_id,hex_color) VALUES(17449,'#a1d5ec');
INSERT INTO ore_colors(type_id,hex_color) VALUES(17452,'#854c0c');
INSERT INTO ore_colors(type_id,hex_color) VALUES(17453,'#854c0c');
INSERT INTO ore_colors(type_id,hex_color) VALUES(17455,'#cf8e52');
INSERT INTO ore_colors(type_id,hex_color) VALUES(17456,'#cf8e52');
INSERT INTO ore_colors(type_id,hex_color) VALUES(17459,'#a7794f');
INSERT INTO ore_colors(type_id,hex_color) VALUES(17460,'#a7794f');
INSERT INTO ore_colors(type_id,hex_color) VALUES(17463,'#846436');
INSERT INTO ore_colors(type_id,hex_color) VALUES(17464,'#846436');
INSERT INTO ore_colors(type_id,hex_color) VALUES(17466,'#d30c04');
INSERT INTO ore_colors(type_id,hex_color) VALUES(17467,'#d30c04');
INSERT INTO ore_colors(type_id,hex_color) VALUES(17470,'#d08967');
INSERT INTO ore_colors(type_id,hex_color) VALUES(17471,'#d08967');
INSERT INTO ore_colors(type_id,hex_color) VALUES(17865,'#12df4a');
INSERT INTO ore_colors(type_id,hex_color) VALUES(17866,'#12df4a');
INSERT INTO ore_colors(type_id,hex_color) VALUES(17867,'#cbb552');
INSERT INTO ore_colors(type_id,hex_color) VALUES(17868,'#cbb552');
INSERT INTO ore_colors(type_id,hex_color) VALUES(17869,'#cd2810');
INSERT INTO ore_colors(type_id,hex_color) VALUES(17870,'#cd2810');
INSERT INTO ore_colors(type_id,hex_color) VALUES(17975,'#3985ad');
INSERT INTO ore_colors(type_id,hex_color) VALUES(17976,'#4a6a84');
INSERT INTO ore_colors(type_id,hex_color) VALUES(17977,'#5bbfce');
INSERT INTO ore_colors(type_id,hex_color) VALUES(17978,'#426274');
INSERT INTO ore_colors(type_id,hex_color) VALUES(28617,'#d08967');
INSERT INTO ore_colors(type_id,hex_color) VALUES(28618,'#a7794f');
INSERT INTO ore_colors(type_id,hex_color) VALUES(28619,'#cbb552');
INSERT INTO ore_colors(type_id,hex_color) VALUES(28620,'#854c0c');
INSERT INTO ore_colors(type_id,hex_color) VALUES(28621,'#a1d5ec');
INSERT INTO ore_colors(type_id,hex_color) VALUES(28622,'#12df4a');
INSERT INTO ore_colors(type_id,hex_color) VALUES(28623,'#a79c70');
INSERT INTO ore_colors(type_id,hex_color) VALUES(28624,'#e69e18');
INSERT INTO ore_colors(type_id,hex_color) VALUES(28625,'#ee3001');
INSERT INTO ore_colors(type_id,hex_color) VALUES(28626,'#cd2810');
INSERT INTO ore_colors(type_id,hex_color) VALUES(28627,'#3985ad');
INSERT INTO ore_colors(type_id,hex_color) VALUES(28628,'#426274');
INSERT INTO ore_colors(type_id,hex_color) VALUES(45490,'#cdaf80');
INSERT INTO ore_colors(type_id,hex_color) VALUES(45491,'#cdaf80');
INSERT INTO ore_colors(type_id,hex_color) VALUES(45492,'#cdaf80');
INSERT INTO ore_colors(type_id,hex_color) VALUES(45493,'#cdaf80');
INSERT INTO ore_colors(type_id,hex_color) VALUES(45494,'#78d1d8');
INSERT INTO ore_colors(type_id,hex_color) VALUES(45495,'#78d1d8');
INSERT INTO ore_colors(type_id,hex_color) VALUES(45496,'#78d1d8');
INSERT INTO ore_colors(type_id,hex_color) VALUES(45497,'#78d1d8');
INSERT INTO ore_colors(type_id,hex_color) VALUES(45498,'#893d1a');
INSERT INTO ore_colors(type_id,hex_color) VALUES(45499,'#893d1a');
INSERT INTO ore_colors(type_id,hex_color) VALUES(45500,'#893d1a');
INSERT INTO ore_colors(type_id,hex_color) VALUES(45501,'#893d1a');
INSERT INTO ore_colors(type_id,hex_color) VALUES(45502,'#3f6aaf');
INSERT INTO ore_colors(type_id,hex_color) VALUES(45503,'#3f6aaf');
INSERT INTO ore_colors(type_id,hex_color) VALUES(45504,'#3f6aaf');
INSERT INTO ore_colors(type_id,hex_color) VALUES(45506,'#3f6aaf');
INSERT INTO ore_colors(type_id,hex_color) VALUES(45510,'#d17474');
INSERT INTO ore_colors(type_id,hex_color) VALUES(45511,'#d17474');
INSERT INTO ore_colors(type_id,hex_color) VALUES(45512,'#d17474');
INSERT INTO ore_colors(type_id,hex_color) VALUES(45513,'#d17474');
INSERT INTO ore_colors(type_id,hex_color) VALUES(46280,'#cdaf80');
INSERT INTO ore_colors(type_id,hex_color) VALUES(46281,'#e47b35');
INSERT INTO ore_colors(type_id,hex_color) VALUES(46282,'#cdaf80');
INSERT INTO ore_colors(type_id,hex_color) VALUES(46283,'#e47b35');
INSERT INTO ore_colors(type_id,hex_color) VALUES(46284,'#cdaf80');
INSERT INTO ore_colors(type_id,hex_color) VALUES(46285,'#e47b35');
INSERT INTO ore_colors(type_id,hex_color) VALUES(46286,'#cdaf80');
INSERT INTO ore_colors(type_id,hex_color) VALUES(46287,'#e47b35');
INSERT INTO ore_colors(type_id,hex_color) VALUES(46288,'#78d1d8');
INSERT INTO ore_colors(type_id,hex_color) VALUES(46289,'#72c3cf');
INSERT INTO ore_colors(type_id,hex_color) VALUES(46290,'#78d1d8');
INSERT INTO ore_colors(type_id,hex_color) VALUES(46291,'#72c3cf');
INSERT INTO ore_colors(type_id,hex_color) VALUES(46292,'#78d1d8');
INSERT INTO ore_colors(type_id,hex_color) VALUES(46293,'#72c3cf');
INSERT INTO ore_colors(type_id,hex_color) VALUES(46294,'#78d1d8');
INSERT INTO ore_colors(type_id,hex_color) VALUES(46295,'#72c3cf');
INSERT INTO ore_colors(type_id,hex_color) VALUES(46296,'#893d1a');
INSERT INTO ore_colors(type_id,hex_color) VALUES(46297,'#ed6623');
INSERT INTO ore_colors(type_id,hex_color) VALUES(46298,'#893d1a');
INSERT INTO ore_colors(type_id,hex_color) VALUES(46299,'#ed6623');
INSERT INTO ore_colors(type_id,hex_color) VALUES(46300,'#893d1a');
INSERT INTO ore_colors(type_id,hex_color) VALUES(46301,'#ed6623');
INSERT INTO ore_colors(type_id,hex_color) VALUES(46302,'#893d1a');
INSERT INTO ore_colors(type_id,hex_color) VALUES(46303,'#ed6623');
INSERT INTO ore_colors(type_id,hex_color) VALUES(46304,'#3f6aaf');
INSERT INTO ore_colors(type_id,hex_color) VALUES(46305,'#5c95d3');
INSERT INTO ore_colors(type_id,hex_color) VALUES(46306,'#3f6aaf');
INSERT INTO ore_colors(type_id,hex_color) VALUES(46307,'#5c95d3');
INSERT INTO ore_colors(type_id,hex_color) VALUES(46308,'#3f6aaf');
INSERT INTO ore_colors(type_id,hex_color) VALUES(46309,'#5c95d3');
INSERT INTO ore_colors(type_id,hex_color) VALUES(46310,'#3f6aaf');
INSERT INTO ore_colors(type_id,hex_color) VALUES(46311,'#5c95d3');
INSERT INTO ore_colors(type_id,hex_color) VALUES(46312,'#d17474');
INSERT INTO ore_colors(type_id,hex_color) VALUES(46313,'#9d3f31');
INSERT INTO ore_colors(type_id,hex_color) VALUES(46314,'#d17474');
INSERT INTO ore_colors(type_id,hex_color) VALUES(46315,'#9d3f31');
INSERT INTO ore_colors(type_id,hex_color) VALUES(46316,'#d17474');
INSERT INTO ore_colors(type_id,hex_color) VALUES(46317,'#9d3f31');
INSERT INTO ore_colors(type_id,hex_color) VALUES(46318,'#d17474');
INSERT INTO ore_colors(type_id,hex_color) VALUES(46319,'#9d3f31');
INSERT INTO ore_colors(type_id,hex_color) VALUES(46675,'#a79c70');
INSERT INTO ore_colors(type_id,hex_color) VALUES(46676,'#68e55b');
INSERT INTO ore_colors(type_id,hex_color) VALUES(46677,'#e69e18');
INSERT INTO ore_colors(type_id,hex_color) VALUES(46678,'#ee3001');
INSERT INTO ore_colors(type_id,hex_color) VALUES(46679,'#12df4a');
INSERT INTO ore_colors(type_id,hex_color) VALUES(46680,'#07f0df');
INSERT INTO ore_colors(type_id,hex_color) VALUES(46681,'#77acd5');
INSERT INTO ore_colors(type_id,hex_color) VALUES(46682,'#a1d5ec');
INSERT INTO ore_colors(type_id,hex_color) VALUES(46683,'#854c0c');
INSERT INTO ore_colors(type_id,hex_color) VALUES(46684,'#cbb552');
INSERT INTO ore_colors(type_id,hex_color) VALUES(46685,'#cf8e52');
INSERT INTO ore_colors(type_id,hex_color) VALUES(46686,'#a7794f');
INSERT INTO ore_colors(type_id,hex_color) VALUES(46687,'#846436');
INSERT INTO ore_colors(type_id,hex_color) VALUES(46688,'#d30c04');
INSERT INTO ore_colors(type_id,hex_color) VALUES(46689,'#d08967');
INSERT INTO ore_colors(type_id,hex_color) VALUES(49789,'#2eb4df');
INSERT INTO ore_colors(type_id,hex_color) VALUES(50015,'#2eb4df');
INSERT INTO ore_colors(type_id,hex_color) VALUES(52306,'#af5f1b');
INSERT INTO ore_colors(type_id,hex_color) VALUES(52315,'#8cd2d5');
INSERT INTO ore_colors(type_id,hex_color) VALUES(52316,'#d6a946');
INSERT INTO ore_colors(type_id,hex_color) VALUES(56625,'#af5f1b');
INSERT INTO ore_colors(type_id,hex_color) VALUES(56626,'#af5f1b');
INSERT INTO ore_colors(type_id,hex_color) VALUES(56627,'#d6a946');
INSERT INTO ore_colors(type_id,hex_color) VALUES(56628,'#d6a946');
INSERT INTO ore_colors(type_id,hex_color) VALUES(56629,'#8cd2d5');
INSERT INTO ore_colors(type_id,hex_color) VALUES(56630,'#8cd2d5');
INSERT INTO ore_colors(type_id,hex_color) VALUES(60771,'#b43c20');
INSERT INTO ore_colors(type_id,hex_color) VALUES(72935,'#d08967');
INSERT INTO ore_colors(type_id,hex_color) VALUES(74521,'#d08967');
INSERT INTO ore_colors(type_id,hex_color) VALUES(74522,'#d08967');
INSERT INTO ore_colors(type_id,hex_color) VALUES(74523,'#d08967');
INSERT INTO ore_colors(type_id,hex_color) VALUES(74524,'#d08967');
INSERT INTO ore_colors(type_id,hex_color) VALUES(74525,'#cbb552');
INSERT INTO ore_colors(type_id,hex_color) VALUES(74526,'#cbb552');
INSERT INTO ore_colors(type_id,hex_color) VALUES(74527,'#cbb552');
INSERT INTO ore_colors(type_id,hex_color) VALUES(74528,'#cbb552');
INSERT INTO ore_colors(type_id,hex_color) VALUES(74529,'#ee3001');
INSERT INTO ore_colors(type_id,hex_color) VALUES(74530,'#ee3001');
INSERT INTO ore_colors(type_id,hex_color) VALUES(74531,'#ee3001');
INSERT INTO ore_colors(type_id,hex_color) VALUES(74532,'#ee3001');
INSERT INTO ore_colors(type_id,hex_color) VALUES(74533,'#d30c04');
INSERT INTO ore_colors(type_id,hex_color) VALUES(74534,'#d30c04');
INSERT INTO ore_colors(type_id,hex_color) VALUES(74535,'#d30c04');
INSERT INTO ore_colors(type_id,hex_color) VALUES(74536,'#d30c04');
INSERT INTO ore_colors(type_id,hex_color) VALUES(76373,'#8cd2d5');
INSERT INTO ore_colors(type_id,hex_color) VALUES(77118,'#11516b');
INSERT INTO ore_colors(type_id,hex_color) VALUES(77418,'#d65900');
INSERT INTO ore_colors(type_id,hex_color) VALUES(77419,'#ce2810');
INSERT INTO ore_colors(type_id,hex_color) VALUES(77420,'#deae62');
INSERT INTO ore_colors(type_id,hex_color) VALUES(77421,'#cd2810');
INSERT INTO ore_colors(type_id,hex_color) VALUES(77524,'#ba511d');
INSERT INTO ore_colors(type_id,hex_color) VALUES(81900,'#12df4a');
INSERT INTO ore_colors(type_id,hex_color) VALUES(81901,'#12df4a');
INSERT INTO ore_colors(type_id,hex_color) VALUES(81902,'#12df4a');
INSERT INTO ore_colors(type_id,hex_color) VALUES(81903,'#12df4a');
INSERT INTO ore_colors(type_id,hex_color) VALUES(81975,'#cbb552');
INSERT INTO ore_colors(type_id,hex_color) VALUES(81976,'#cbb552');
INSERT INTO ore_colors(type_id,hex_color) VALUES(81977,'#cbb552');
INSERT INTO ore_colors(type_id,hex_color) VALUES(81978,'#cbb552');
INSERT INTO ore_colors(type_id,hex_color) VALUES(82016,'#07f0df');
INSERT INTO ore_colors(type_id,hex_color) VALUES(82017,'#07f0df');
INSERT INTO ore_colors(type_id,hex_color) VALUES(82018,'#07f0df');
INSERT INTO ore_colors(type_id,hex_color) VALUES(82019,'#07f0df');
INSERT INTO ore_colors(type_id,hex_color) VALUES(82163,'#d30c04');
INSERT INTO ore_colors(type_id,hex_color) VALUES(82164,'#d30c04');
INSERT INTO ore_colors(type_id,hex_color) VALUES(82165,'#d30c04');
INSERT INTO ore_colors(type_id,hex_color) VALUES(82166,'#d30c04');
INSERT INTO ore_colors(type_id,hex_color) VALUES(82205,'#ee3001');
INSERT INTO ore_colors(type_id,hex_color) VALUES(82206,'#ee3001');
INSERT INTO ore_colors(type_id,hex_color) VALUES(82207,'#ee3001');
INSERT INTO ore_colors(type_id,hex_color) VALUES(82208,'#ee3001');
INSERT INTO ore_colors(type_id,hex_color) VALUES(88105,'#0bedd5');
UPDATE sqlite_stat1 SET tbl='compressible_types', idx=NULL, stat='205' WHERE rowid=1;
UPDATE sqlite_stat1 SET tbl='celestialNames', stat='410131' WHERE rowid=2;
UPDATE sqlite_stat1 SET tbl='blueprint_process_time', stat='5031' WHERE rowid=3;
UPDATE sqlite_stat1 SET tbl='blueprint_invention_skills', idx='sqlite_autoindex_blueprint_invention_skills_1', stat='3398 4 1' WHERE rowid=4;
UPDATE sqlite_stat1 SET tbl='blueprint_invention_products', idx='sqlite_autoindex_blueprint_invention_products_1', stat='1349 2 1' WHERE rowid=5;
UPDATE sqlite_stat1 SET tbl='blueprint_invention_materials', idx='sqlite_autoindex_blueprint_invention_materials_1', stat='2208 2 1' WHERE rowid=6;
UPDATE sqlite_stat1 SET tbl='traits', idx='sqlite_autoindex_traits_1', stat='3702 6 1 1' WHERE rowid=23;
UPDATE sqlite_stat1 SET tbl='ore_colors', idx=NULL, stat='204' WHERE rowid=24;
UPDATE sqlite_stat1 SET tbl='facility_rig_effects', idx='sqlite_autoindex_facility_rig_effects_1', stat='484 5 3 1' WHERE rowid=25;
UPDATE sqlite_stat1 SET tbl='stations', idx='idx_stations_solarSystemID', stat='5154 4' WHERE rowid=26;
UPDATE sqlite_stat1 SET tbl='solarsystems', idx=NULL, stat='8437' WHERE rowid=27;
UPDATE sqlite_stat1 SET tbl='dynamic_item_attributes', idx='sqlite_autoindex_dynamic_item_attributes_1', stat='1800 5 1' WHERE rowid=28;
UPDATE sqlite_stat1 SET tbl='typeAttributes', idx='sqlite_autoindex_typeAttributes_1', stat='614971 24 1' WHERE rowid=29;
UPDATE sqlite_stat1 SET tbl='blueprint_manufacturing_skills', idx='sqlite_autoindex_blueprint_manufacturing_skills_1', stat='9221 2 1' WHERE rowid=30;
UPDATE sqlite_stat1 SET tbl='regions', stat='113' WHERE rowid=31;
UPDATE sqlite_stat1 SET tbl='metaGroups', stat='13' WHERE rowid=32;
UPDATE sqlite_stat1 SET tbl='factions', idx=NULL, stat='27' WHERE rowid=33;
UPDATE sqlite_stat1 SET tbl='dogmaAttributes', idx=NULL, stat='2775' WHERE rowid=34;
UPDATE sqlite_stat1 SET tbl='loyalty_offer_outputs', idx='idx_loyalty_offer_outputs_lp_cost', stat='3123 17' WHERE rowid=35;
UPDATE sqlite_stat1 SET tbl='loyalty_offer_outputs', idx='idx_loyalty_offer_outputs_type_id', stat='3123 1' WHERE rowid=36;
UPDATE sqlite_stat1 SET tbl='dogmaAttributeCategories', idx=NULL, stat='37' WHERE rowid=37;
UPDATE sqlite_stat1 SET idx='idx_loyalty_offer_requirements_type_id', stat='2566 5' WHERE rowid=38;
UPDATE sqlite_stat1 SET tbl='loyalty_offer_requirements', idx='idx_loyalty_offer_requirements_offer_id', stat='2566 2' WHERE rowid=39;
UPDATE sqlite_stat1 SET tbl='loyalty_offer_requirements', idx='sqlite_autoindex_loyalty_offer_requirements_1', stat='2566 2 1' WHERE rowid=40;
UPDATE sqlite_stat1 SET tbl='typeEffects', idx='sqlite_autoindex_typeEffects_1', stat='51969 4 1' WHERE rowid=41;
UPDATE sqlite_stat1 SET tbl='divisions', idx=NULL, stat='10' WHERE rowid=42;
UPDATE sqlite_stat1 SET tbl='marketGroups', stat='2039' WHERE rowid=43;
UPDATE sqlite_stat1 SET tbl='blueprint_research_material_skills', idx='sqlite_autoindex_blueprint_research_material_skills_1', stat='3806 3 1' WHERE rowid=44;
UPDATE sqlite_stat1 SET tbl='groups', idx=NULL, stat='1557' WHERE rowid=45;
UPDATE sqlite_stat1 SET tbl='blueprint_research_time_skills', idx='sqlite_autoindex_blueprint_research_time_skills_1', stat='3693 3 1' WHERE rowid=46;
UPDATE sqlite_stat1 SET tbl='dbuffCollection', idx='sqlite_autoindex_dbuffCollection_1', stat='85 2 1' WHERE rowid=47;
UPDATE sqlite_stat1 SET tbl='typeMaterials', idx='sqlite_autoindex_typeMaterials_1', stat='46392 5 1' WHERE rowid=48;
UPDATE sqlite_stat1 SET tbl='blueprint_manufacturing_output', idx='sqlite_autoindex_blueprint_manufacturing_output_1', stat='4917 1 1' WHERE rowid=49;
UPDATE sqlite_stat1 SET tbl='blueprint_research_material_materials', idx='sqlite_autoindex_blueprint_research_material_materials_1', stat='2576 4 1' WHERE rowid=50;
UPDATE sqlite_stat1 SET tbl='wormholes', idx=NULL, stat='127' WHERE rowid=51;
UPDATE sqlite_stat1 SET tbl='blueprint_research_time_materials', idx='sqlite_autoindex_blueprint_research_time_materials_1', stat='2401 3 1' WHERE rowid=52;
UPDATE sqlite_stat1 SET tbl='blueprint_copying_skills', idx='sqlite_autoindex_blueprint_copying_skills_1', stat='2134 3 1' WHERE rowid=53;
INSERT INTO sqlite_stat1(rowid,tbl,idx,stat) VALUES(54,'blueprint_copying_materials','sqlite_autoindex_blueprint_copying_materials_1','1818 2 1');
UPDATE version_info SET patch_number=1 WHERE id=1;
```

### ZH 数据库

**数据库差异**:
```sql
CREATE TABLE ore_colors (
                type_id INTEGER PRIMARY KEY,
                hex_color TEXT NOT NULL,
                FOREIGN KEY (type_id) REFERENCES types(type_id)
            );
INSERT INTO ore_colors(type_id,hex_color) VALUES(18,'#cf8e52');
INSERT INTO ore_colors(type_id,hex_color) VALUES(19,'#d30c04');
INSERT INTO ore_colors(type_id,hex_color) VALUES(20,'#854c0c');
INSERT INTO ore_colors(type_id,hex_color) VALUES(21,'#07f0df');
INSERT INTO ore_colors(type_id,hex_color) VALUES(22,'#ee3001');
INSERT INTO ore_colors(type_id,hex_color) VALUES(1223,'#68e55b');
INSERT INTO ore_colors(type_id,hex_color) VALUES(1224,'#a7794f');
INSERT INTO ore_colors(type_id,hex_color) VALUES(1225,'#e69e18');
INSERT INTO ore_colors(type_id,hex_color) VALUES(1226,'#a1d5ec');
INSERT INTO ore_colors(type_id,hex_color) VALUES(1227,'#cbb552');
INSERT INTO ore_colors(type_id,hex_color) VALUES(1228,'#846436');
INSERT INTO ore_colors(type_id,hex_color) VALUES(1229,'#12df4a');
INSERT INTO ore_colors(type_id,hex_color) VALUES(1230,'#d08967');
INSERT INTO ore_colors(type_id,hex_color) VALUES(1231,'#77acd5');
INSERT INTO ore_colors(type_id,hex_color) VALUES(1232,'#a79c70');
INSERT INTO ore_colors(type_id,hex_color) VALUES(11396,'#cd2810');
INSERT INTO ore_colors(type_id,hex_color) VALUES(16262,'#426274');
INSERT INTO ore_colors(type_id,hex_color) VALUES(16263,'#5bbfce');
INSERT INTO ore_colors(type_id,hex_color) VALUES(16264,'#3985ad');
INSERT INTO ore_colors(type_id,hex_color) VALUES(16265,'#4a6a84');
INSERT INTO ore_colors(type_id,hex_color) VALUES(16266,'#4a86a5');
INSERT INTO ore_colors(type_id,hex_color) VALUES(16267,'#527a9d');
INSERT INTO ore_colors(type_id,hex_color) VALUES(16268,'#4db8bb');
INSERT INTO ore_colors(type_id,hex_color) VALUES(16269,'#186194');
INSERT INTO ore_colors(type_id,hex_color) VALUES(17425,'#ee3001');
INSERT INTO ore_colors(type_id,hex_color) VALUES(17426,'#ee3001');
INSERT INTO ore_colors(type_id,hex_color) VALUES(17428,'#68e55b');
INSERT INTO ore_colors(type_id,hex_color) VALUES(17429,'#68e55b');
INSERT INTO ore_colors(type_id,hex_color) VALUES(17432,'#e69e18');
INSERT INTO ore_colors(type_id,hex_color) VALUES(17433,'#e69e18');
INSERT INTO ore_colors(type_id,hex_color) VALUES(17436,'#a79c70');
INSERT INTO ore_colors(type_id,hex_color) VALUES(17437,'#a79c70');
INSERT INTO ore_colors(type_id,hex_color) VALUES(17440,'#07f0df');
INSERT INTO ore_colors(type_id,hex_color) VALUES(17441,'#07f0df');
INSERT INTO ore_colors(type_id,hex_color) VALUES(17444,'#77acd5');
INSERT INTO ore_colors(type_id,hex_color) VALUES(17445,'#77acd5');
INSERT INTO ore_colors(type_id,hex_color) VALUES(17448,'#a1d5ec');
INSERT INTO ore_colors(type_id,hex_color) VALUES(17449,'#a1d5ec');
INSERT INTO ore_colors(type_id,hex_color) VALUES(17452,'#854c0c');
INSERT INTO ore_colors(type_id,hex_color) VALUES(17453,'#854c0c');
INSERT INTO ore_colors(type_id,hex_color) VALUES(17455,'#cf8e52');
INSERT INTO ore_colors(type_id,hex_color) VALUES(17456,'#cf8e52');
INSERT INTO ore_colors(type_id,hex_color) VALUES(17459,'#a7794f');
INSERT INTO ore_colors(type_id,hex_color) VALUES(17460,'#a7794f');
INSERT INTO ore_colors(type_id,hex_color) VALUES(17463,'#846436');
INSERT INTO ore_colors(type_id,hex_color) VALUES(17464,'#846436');
INSERT INTO ore_colors(type_id,hex_color) VALUES(17466,'#d30c04');
INSERT INTO ore_colors(type_id,hex_color) VALUES(17467,'#d30c04');
INSERT INTO ore_colors(type_id,hex_color) VALUES(17470,'#d08967');
INSERT INTO ore_colors(type_id,hex_color) VALUES(17471,'#d08967');
INSERT INTO ore_colors(type_id,hex_color) VALUES(17865,'#12df4a');
INSERT INTO ore_colors(type_id,hex_color) VALUES(17866,'#12df4a');
INSERT INTO ore_colors(type_id,hex_color) VALUES(17867,'#cbb552');
INSERT INTO ore_colors(type_id,hex_color) VALUES(17868,'#cbb552');
INSERT INTO ore_colors(type_id,hex_color) VALUES(17869,'#cd2810');
INSERT INTO ore_colors(type_id,hex_color) VALUES(17870,'#cd2810');
INSERT INTO ore_colors(type_id,hex_color) VALUES(17975,'#3985ad');
INSERT INTO ore_colors(type_id,hex_color) VALUES(17976,'#4a6a84');
INSERT INTO ore_colors(type_id,hex_color) VALUES(17977,'#5bbfce');
INSERT INTO ore_colors(type_id,hex_color) VALUES(17978,'#426274');
INSERT INTO ore_colors(type_id,hex_color) VALUES(28617,'#d08967');
INSERT INTO ore_colors(type_id,hex_color) VALUES(28618,'#a7794f');
INSERT INTO ore_colors(type_id,hex_color) VALUES(28619,'#cbb552');
INSERT INTO ore_colors(type_id,hex_color) VALUES(28620,'#854c0c');
INSERT INTO ore_colors(type_id,hex_color) VALUES(28621,'#a1d5ec');
INSERT INTO ore_colors(type_id,hex_color) VALUES(28622,'#12df4a');
INSERT INTO ore_colors(type_id,hex_color) VALUES(28623,'#a79c70');
INSERT INTO ore_colors(type_id,hex_color) VALUES(28624,'#e69e18');
INSERT INTO ore_colors(type_id,hex_color) VALUES(28625,'#ee3001');
INSERT INTO ore_colors(type_id,hex_color) VALUES(28626,'#cd2810');
INSERT INTO ore_colors(type_id,hex_color) VALUES(28627,'#3985ad');
INSERT INTO ore_colors(type_id,hex_color) VALUES(28628,'#426274');
INSERT INTO ore_colors(type_id,hex_color) VALUES(45490,'#cdaf80');
INSERT INTO ore_colors(type_id,hex_color) VALUES(45491,'#cdaf80');
INSERT INTO ore_colors(type_id,hex_color) VALUES(45492,'#cdaf80');
INSERT INTO ore_colors(type_id,hex_color) VALUES(45493,'#cdaf80');
INSERT INTO ore_colors(type_id,hex_color) VALUES(45494,'#78d1d8');
INSERT INTO ore_colors(type_id,hex_color) VALUES(45495,'#78d1d8');
INSERT INTO ore_colors(type_id,hex_color) VALUES(45496,'#78d1d8');
INSERT INTO ore_colors(type_id,hex_color) VALUES(45497,'#78d1d8');
INSERT INTO ore_colors(type_id,hex_color) VALUES(45498,'#893d1a');
INSERT INTO ore_colors(type_id,hex_color) VALUES(45499,'#893d1a');
INSERT INTO ore_colors(type_id,hex_color) VALUES(45500,'#893d1a');
INSERT INTO ore_colors(type_id,hex_color) VALUES(45501,'#893d1a');
INSERT INTO ore_colors(type_id,hex_color) VALUES(45502,'#3f6aaf');
INSERT INTO ore_colors(type_id,hex_color) VALUES(45503,'#3f6aaf');
INSERT INTO ore_colors(type_id,hex_color) VALUES(45504,'#3f6aaf');
INSERT INTO ore_colors(type_id,hex_color) VALUES(45506,'#3f6aaf');
INSERT INTO ore_colors(type_id,hex_color) VALUES(45510,'#d17474');
INSERT INTO ore_colors(type_id,hex_color) VALUES(45511,'#d17474');
INSERT INTO ore_colors(type_id,hex_color) VALUES(45512,'#d17474');
INSERT INTO ore_colors(type_id,hex_color) VALUES(45513,'#d17474');
INSERT INTO ore_colors(type_id,hex_color) VALUES(46280,'#cdaf80');
INSERT INTO ore_colors(type_id,hex_color) VALUES(46281,'#e47b35');
INSERT INTO ore_colors(type_id,hex_color) VALUES(46282,'#cdaf80');
INSERT INTO ore_colors(type_id,hex_color) VALUES(46283,'#e47b35');
INSERT INTO ore_colors(type_id,hex_color) VALUES(46284,'#cdaf80');
INSERT INTO ore_colors(type_id,hex_color) VALUES(46285,'#e47b35');
INSERT INTO ore_colors(type_id,hex_color) VALUES(46286,'#cdaf80');
INSERT INTO ore_colors(type_id,hex_color) VALUES(46287,'#e47b35');
INSERT INTO ore_colors(type_id,hex_color) VALUES(46288,'#78d1d8');
INSERT INTO ore_colors(type_id,hex_color) VALUES(46289,'#72c3cf');
INSERT INTO ore_colors(type_id,hex_color) VALUES(46290,'#78d1d8');
INSERT INTO ore_colors(type_id,hex_color) VALUES(46291,'#72c3cf');
INSERT INTO ore_colors(type_id,hex_color) VALUES(46292,'#78d1d8');
INSERT INTO ore_colors(type_id,hex_color) VALUES(46293,'#72c3cf');
INSERT INTO ore_colors(type_id,hex_color) VALUES(46294,'#78d1d8');
INSERT INTO ore_colors(type_id,hex_color) VALUES(46295,'#72c3cf');
INSERT INTO ore_colors(type_id,hex_color) VALUES(46296,'#893d1a');
INSERT INTO ore_colors(type_id,hex_color) VALUES(46297,'#ed6623');
INSERT INTO ore_colors(type_id,hex_color) VALUES(46298,'#893d1a');
INSERT INTO ore_colors(type_id,hex_color) VALUES(46299,'#ed6623');
INSERT INTO ore_colors(type_id,hex_color) VALUES(46300,'#893d1a');
INSERT INTO ore_colors(type_id,hex_color) VALUES(46301,'#ed6623');
INSERT INTO ore_colors(type_id,hex_color) VALUES(46302,'#893d1a');
INSERT INTO ore_colors(type_id,hex_color) VALUES(46303,'#ed6623');
INSERT INTO ore_colors(type_id,hex_color) VALUES(46304,'#3f6aaf');
INSERT INTO ore_colors(type_id,hex_color) VALUES(46305,'#5c95d3');
INSERT INTO ore_colors(type_id,hex_color) VALUES(46306,'#3f6aaf');
INSERT INTO ore_colors(type_id,hex_color) VALUES(46307,'#5c95d3');
INSERT INTO ore_colors(type_id,hex_color) VALUES(46308,'#3f6aaf');
INSERT INTO ore_colors(type_id,hex_color) VALUES(46309,'#5c95d3');
INSERT INTO ore_colors(type_id,hex_color) VALUES(46310,'#3f6aaf');
INSERT INTO ore_colors(type_id,hex_color) VALUES(46311,'#5c95d3');
INSERT INTO ore_colors(type_id,hex_color) VALUES(46312,'#d17474');
INSERT INTO ore_colors(type_id,hex_color) VALUES(46313,'#9d3f31');
INSERT INTO ore_colors(type_id,hex_color) VALUES(46314,'#d17474');
INSERT INTO ore_colors(type_id,hex_color) VALUES(46315,'#9d3f31');
INSERT INTO ore_colors(type_id,hex_color) VALUES(46316,'#d17474');
INSERT INTO ore_colors(type_id,hex_color) VALUES(46317,'#9d3f31');
INSERT INTO ore_colors(type_id,hex_color) VALUES(46318,'#d17474');
INSERT INTO ore_colors(type_id,hex_color) VALUES(46319,'#9d3f31');
INSERT INTO ore_colors(type_id,hex_color) VALUES(46675,'#a79c70');
INSERT INTO ore_colors(type_id,hex_color) VALUES(46676,'#68e55b');
INSERT INTO ore_colors(type_id,hex_color) VALUES(46677,'#e69e18');
INSERT INTO ore_colors(type_id,hex_color) VALUES(46678,'#ee3001');
INSERT INTO ore_colors(type_id,hex_color) VALUES(46679,'#12df4a');
INSERT INTO ore_colors(type_id,hex_color) VALUES(46680,'#07f0df');
INSERT INTO ore_colors(type_id,hex_color) VALUES(46681,'#77acd5');
INSERT INTO ore_colors(type_id,hex_color) VALUES(46682,'#a1d5ec');
INSERT INTO ore_colors(type_id,hex_color) VALUES(46683,'#854c0c');
INSERT INTO ore_colors(type_id,hex_color) VALUES(46684,'#cbb552');
INSERT INTO ore_colors(type_id,hex_color) VALUES(46685,'#cf8e52');
INSERT INTO ore_colors(type_id,hex_color) VALUES(46686,'#a7794f');
INSERT INTO ore_colors(type_id,hex_color) VALUES(46687,'#846436');
INSERT INTO ore_colors(type_id,hex_color) VALUES(46688,'#d30c04');
INSERT INTO ore_colors(type_id,hex_color) VALUES(46689,'#d08967');
INSERT INTO ore_colors(type_id,hex_color) VALUES(49789,'#2eb4df');
INSERT INTO ore_colors(type_id,hex_color) VALUES(50015,'#2eb4df');
INSERT INTO ore_colors(type_id,hex_color) VALUES(52306,'#af5f1b');
INSERT INTO ore_colors(type_id,hex_color) VALUES(52315,'#8cd2d5');
INSERT INTO ore_colors(type_id,hex_color) VALUES(52316,'#d6a946');
INSERT INTO ore_colors(type_id,hex_color) VALUES(56625,'#af5f1b');
INSERT INTO ore_colors(type_id,hex_color) VALUES(56626,'#af5f1b');
INSERT INTO ore_colors(type_id,hex_color) VALUES(56627,'#d6a946');
INSERT INTO ore_colors(type_id,hex_color) VALUES(56628,'#d6a946');
INSERT INTO ore_colors(type_id,hex_color) VALUES(56629,'#8cd2d5');
INSERT INTO ore_colors(type_id,hex_color) VALUES(56630,'#8cd2d5');
INSERT INTO ore_colors(type_id,hex_color) VALUES(60771,'#b43c20');
INSERT INTO ore_colors(type_id,hex_color) VALUES(72935,'#d08967');
INSERT INTO ore_colors(type_id,hex_color) VALUES(74521,'#d08967');
INSERT INTO ore_colors(type_id,hex_color) VALUES(74522,'#d08967');
INSERT INTO ore_colors(type_id,hex_color) VALUES(74523,'#d08967');
INSERT INTO ore_colors(type_id,hex_color) VALUES(74524,'#d08967');
INSERT INTO ore_colors(type_id,hex_color) VALUES(74525,'#cbb552');
INSERT INTO ore_colors(type_id,hex_color) VALUES(74526,'#cbb552');
INSERT INTO ore_colors(type_id,hex_color) VALUES(74527,'#cbb552');
INSERT INTO ore_colors(type_id,hex_color) VALUES(74528,'#cbb552');
INSERT INTO ore_colors(type_id,hex_color) VALUES(74529,'#ee3001');
INSERT INTO ore_colors(type_id,hex_color) VALUES(74530,'#ee3001');
INSERT INTO ore_colors(type_id,hex_color) VALUES(74531,'#ee3001');
INSERT INTO ore_colors(type_id,hex_color) VALUES(74532,'#ee3001');
INSERT INTO ore_colors(type_id,hex_color) VALUES(74533,'#d30c04');
INSERT INTO ore_colors(type_id,hex_color) VALUES(74534,'#d30c04');
INSERT INTO ore_colors(type_id,hex_color) VALUES(74535,'#d30c04');
INSERT INTO ore_colors(type_id,hex_color) VALUES(74536,'#d30c04');
INSERT INTO ore_colors(type_id,hex_color) VALUES(76373,'#8cd2d5');
INSERT INTO ore_colors(type_id,hex_color) VALUES(77118,'#11516b');
INSERT INTO ore_colors(type_id,hex_color) VALUES(77418,'#d65900');
INSERT INTO ore_colors(type_id,hex_color) VALUES(77419,'#ce2810');
INSERT INTO ore_colors(type_id,hex_color) VALUES(77420,'#deae62');
INSERT INTO ore_colors(type_id,hex_color) VALUES(77421,'#cd2810');
INSERT INTO ore_colors(type_id,hex_color) VALUES(77524,'#ba511d');
INSERT INTO ore_colors(type_id,hex_color) VALUES(81900,'#12df4a');
INSERT INTO ore_colors(type_id,hex_color) VALUES(81901,'#12df4a');
INSERT INTO ore_colors(type_id,hex_color) VALUES(81902,'#12df4a');
INSERT INTO ore_colors(type_id,hex_color) VALUES(81903,'#12df4a');
INSERT INTO ore_colors(type_id,hex_color) VALUES(81975,'#cbb552');
INSERT INTO ore_colors(type_id,hex_color) VALUES(81976,'#cbb552');
INSERT INTO ore_colors(type_id,hex_color) VALUES(81977,'#cbb552');
INSERT INTO ore_colors(type_id,hex_color) VALUES(81978,'#cbb552');
INSERT INTO ore_colors(type_id,hex_color) VALUES(82016,'#07f0df');
INSERT INTO ore_colors(type_id,hex_color) VALUES(82017,'#07f0df');
INSERT INTO ore_colors(type_id,hex_color) VALUES(82018,'#07f0df');
INSERT INTO ore_colors(type_id,hex_color) VALUES(82019,'#07f0df');
INSERT INTO ore_colors(type_id,hex_color) VALUES(82163,'#d30c04');
INSERT INTO ore_colors(type_id,hex_color) VALUES(82164,'#d30c04');
INSERT INTO ore_colors(type_id,hex_color) VALUES(82165,'#d30c04');
INSERT INTO ore_colors(type_id,hex_color) VALUES(82166,'#d30c04');
INSERT INTO ore_colors(type_id,hex_color) VALUES(82205,'#ee3001');
INSERT INTO ore_colors(type_id,hex_color) VALUES(82206,'#ee3001');
INSERT INTO ore_colors(type_id,hex_color) VALUES(82207,'#ee3001');
INSERT INTO ore_colors(type_id,hex_color) VALUES(82208,'#ee3001');
INSERT INTO ore_colors(type_id,hex_color) VALUES(88105,'#0bedd5');
UPDATE sqlite_stat1 SET tbl='compressible_types', idx=NULL, stat='205' WHERE rowid=1;
UPDATE sqlite_stat1 SET tbl='celestialNames', stat='410131' WHERE rowid=2;
UPDATE sqlite_stat1 SET tbl='blueprint_process_time', stat='5031' WHERE rowid=3;
UPDATE sqlite_stat1 SET tbl='blueprint_invention_skills', idx='sqlite_autoindex_blueprint_invention_skills_1', stat='3398 4 1' WHERE rowid=4;
UPDATE sqlite_stat1 SET tbl='blueprint_invention_products', idx='sqlite_autoindex_blueprint_invention_products_1', stat='1349 2 1' WHERE rowid=5;
UPDATE sqlite_stat1 SET tbl='blueprint_invention_materials', idx='sqlite_autoindex_blueprint_invention_materials_1', stat='2208 2 1' WHERE rowid=6;
UPDATE sqlite_stat1 SET tbl='traits', idx='sqlite_autoindex_traits_1', stat='3702 6 1 1' WHERE rowid=23;
UPDATE sqlite_stat1 SET tbl='ore_colors', idx=NULL, stat='204' WHERE rowid=24;
UPDATE sqlite_stat1 SET tbl='facility_rig_effects', idx='sqlite_autoindex_facility_rig_effects_1', stat='484 5 3 1' WHERE rowid=25;
UPDATE sqlite_stat1 SET tbl='stations', idx='idx_stations_solarSystemID', stat='5154 4' WHERE rowid=26;
UPDATE sqlite_stat1 SET tbl='solarsystems', idx=NULL, stat='8437' WHERE rowid=27;
UPDATE sqlite_stat1 SET tbl='dynamic_item_attributes', idx='sqlite_autoindex_dynamic_item_attributes_1', stat='1800 5 1' WHERE rowid=28;
UPDATE sqlite_stat1 SET tbl='typeAttributes', idx='sqlite_autoindex_typeAttributes_1', stat='614971 24 1' WHERE rowid=29;
UPDATE sqlite_stat1 SET tbl='blueprint_manufacturing_skills', idx='sqlite_autoindex_blueprint_manufacturing_skills_1', stat='9221 2 1' WHERE rowid=30;
UPDATE sqlite_stat1 SET tbl='regions', stat='113' WHERE rowid=31;
UPDATE sqlite_stat1 SET tbl='metaGroups', stat='13' WHERE rowid=32;
UPDATE sqlite_stat1 SET tbl='factions', idx=NULL, stat='27' WHERE rowid=33;
UPDATE sqlite_stat1 SET tbl='dogmaAttributes', idx=NULL, stat='2775' WHERE rowid=34;
UPDATE sqlite_stat1 SET tbl='loyalty_offer_outputs', idx='idx_loyalty_offer_outputs_lp_cost', stat='3123 17' WHERE rowid=35;
UPDATE sqlite_stat1 SET tbl='loyalty_offer_outputs', idx='idx_loyalty_offer_outputs_type_id', stat='3123 1' WHERE rowid=36;
UPDATE sqlite_stat1 SET tbl='dogmaAttributeCategories', idx=NULL, stat='37' WHERE rowid=37;
UPDATE sqlite_stat1 SET idx='idx_loyalty_offer_requirements_type_id', stat='2566 5' WHERE rowid=38;
UPDATE sqlite_stat1 SET tbl='loyalty_offer_requirements', idx='idx_loyalty_offer_requirements_offer_id', stat='2566 2' WHERE rowid=39;
UPDATE sqlite_stat1 SET tbl='loyalty_offer_requirements', idx='sqlite_autoindex_loyalty_offer_requirements_1', stat='2566 2 1' WHERE rowid=40;
UPDATE sqlite_stat1 SET tbl='typeEffects', idx='sqlite_autoindex_typeEffects_1', stat='51969 4 1' WHERE rowid=41;
UPDATE sqlite_stat1 SET tbl='divisions', idx=NULL, stat='10' WHERE rowid=42;
UPDATE sqlite_stat1 SET tbl='marketGroups', stat='2039' WHERE rowid=43;
UPDATE sqlite_stat1 SET tbl='blueprint_research_material_skills', idx='sqlite_autoindex_blueprint_research_material_skills_1', stat='3806 3 1' WHERE rowid=44;
UPDATE sqlite_stat1 SET tbl='groups', idx=NULL, stat='1557' WHERE rowid=45;
UPDATE sqlite_stat1 SET tbl='blueprint_research_time_skills', idx='sqlite_autoindex_blueprint_research_time_skills_1', stat='3693 3 1' WHERE rowid=46;
UPDATE sqlite_stat1 SET tbl='dbuffCollection', idx='sqlite_autoindex_dbuffCollection_1', stat='85 2 1' WHERE rowid=47;
UPDATE sqlite_stat1 SET tbl='typeMaterials', idx='sqlite_autoindex_typeMaterials_1', stat='46392 5 1' WHERE rowid=48;
UPDATE sqlite_stat1 SET tbl='blueprint_manufacturing_output', idx='sqlite_autoindex_blueprint_manufacturing_output_1', stat='4917 1 1' WHERE rowid=49;
UPDATE sqlite_stat1 SET tbl='blueprint_research_material_materials', idx='sqlite_autoindex_blueprint_research_material_materials_1', stat='2576 4 1' WHERE rowid=50;
UPDATE sqlite_stat1 SET tbl='wormholes', idx=NULL, stat='127' WHERE rowid=51;
UPDATE sqlite_stat1 SET tbl='blueprint_research_time_materials', idx='sqlite_autoindex_blueprint_research_time_materials_1', stat='2401 3 1' WHERE rowid=52;
UPDATE sqlite_stat1 SET tbl='blueprint_copying_skills', idx='sqlite_autoindex_blueprint_copying_skills_1', stat='2134 3 1' WHERE rowid=53;
INSERT INTO sqlite_stat1(rowid,tbl,idx,stat) VALUES(54,'blueprint_copying_materials','sqlite_autoindex_blueprint_copying_materials_1','1818 2 1');
UPDATE version_info SET patch_number=1 WHERE id=1;
```

## 地图和本地化文件比较

### regions_data.json

文件无差异

### systems_data.json

文件无差异

### neighbors_data.json

文件无差异

## 本地化文件比较

### accountingentrytypes_localized.json

文件无差异


## 下载文件

- **icons.zip**: 图标压缩包
- **sde.zip**: SDE数据压缩包
- **release_compare_3096543.01.md**: 详细比较报告
