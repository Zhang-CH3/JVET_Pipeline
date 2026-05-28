#!/usr/bin/env python3
"""
检查 JVET 文档下载情况
读取 CSV 清单，扫描 downloaded_docs 目录，输出缺失文件列表
"""

import csv
import os
from pathlib import Path
from collections import defaultdict

# ==================== 配置区域 ====================
CSV_FILE = "jvet_documents_cccm.csv"      # CSV 清单文件路径
DOC_DIR = "./downloaded_docs"              # 下载文件存放目录
MAX_VERSION = 4                            # 最大版本号
# =================================================

def scan_downloaded_files(doc_dir: Path):
    """扫描目录，返回 {提案号: [存在的版本号]} 的字典"""
    result = defaultdict(list)
    if not doc_dir.exists():
        return result
    
    for file_path in doc_dir.glob("*.zip"):
        # 文件名格式: JVET-XXXXXX_v1.zip
        name = file_path.stem  # 去掉 .zip
        if "_v" in name:
            parts = name.rsplit("_v", 1)
            if len(parts) == 2:
                doc_id = parts[0]
                try:
                    version = int(parts[1])
                    result[doc_id].append(version)
                except ValueError:
                    pass
    return result

def check_download_status(csv_path: str, doc_dir: Path):
    """检查下载状态并生成报告"""
    # 读取 CSV 清单
    required_docs = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            required_docs.append(row['document_id'].strip())
    
    # 扫描已下载文件
    downloaded_map = scan_downloaded_files(doc_dir)
    
    # 统计
    completed = []
    missing = []
    version_issue = []
    
    for doc_id in required_docs:
        if doc_id not in downloaded_map:
            missing.append(doc_id)
        else:
            versions = downloaded_map[doc_id]
            # 取最高版本作为代表（v2 优于 v1）
            best_version = max(versions)
            completed.append((doc_id, best_version))
    
    # 输出报告
    print("=" * 60)
    print("JVET 文档下载检查报告")
    print("=" * 60)
    print(f"清单文件: {csv_path}")
    print(f"文档目录: {doc_dir}")
    print(f"应下载总数: {len(required_docs)}")
    print(f"已完成: {len(completed)}")
    print(f"缺失: {len(missing)}")
    print("=" * 60)
    
    # 缺失列表（重点）
    if missing:
        print("\n❌ 缺失文档列表（需手动下载）：")
        print("-" * 40)
        for doc_id in missing:
            print(f"  {doc_id}")
        
        # 生成缺失列表文件
        missing_file = Path("missing_docs.txt")
        with open(missing_file, 'w', encoding='utf-8') as f:
            for doc_id in missing:
                f.write(f"{doc_id}\n")
        print(f"\n缺失列表已保存至: {missing_file}")
    
    # 已下载列表（含版本号）
    if completed:
        print("\n✅ 已下载文档（含版本号）：")
        print("-" * 40)
        for doc_id, version in completed:
            print(f"  {doc_id} (v{version})")
    
    return missing, completed

def generate_manual_download_commands(missing_docs, meeting_map=None):
    """生成手动下载链接（如果提供了 meeting_id 映射）"""
    if not meeting_map or not missing_docs:
        return
    
    print("\n" + "=" * 60)
    print("手动下载链接（需根据会议自行确认版本号）：")
    print("=" * 60)
    print("提示：你需要从 CSV 中查找缺失文档对应的 meeting_id")
    print("链接格式：https://jvet-experts.org/doc_end_user/documents/{meeting_id}/wg11/{doc_id}-v{version}.zip")
    print()
    
    for doc_id in missing_docs[:10]:  # 只显示前10个示例
        if doc_id in meeting_map:
            meeting_id = meeting_map[doc_id]
            print(f"  {doc_id}: https://jvet-experts.org/doc_end_user/documents/{meeting_id}/wg11/{doc_id}-v1.zip")
        else:
            print(f"  {doc_id}: (需查找 meeting_id)")

def load_meeting_map(csv_path: str):
    """从 CSV 加载 meeting_id 映射"""
    meeting_map = {}
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            doc_id = row['document_id'].strip()
            meeting_id = row['meeting_id'].strip()
            if doc_id not in meeting_map:
                meeting_map[doc_id] = meeting_id
    return meeting_map

if __name__ == "__main__":
    csv_file = Path(CSV_FILE)
    doc_dir = Path(DOC_DIR)
    
    if not csv_file.exists():
        print(f"错误：找不到 CSV 文件 {CSV_FILE}")
        exit(1)
    
    # 检查下载状态
    missing, completed = check_download_status(CSV_FILE, doc_dir)
    
    # 可选：生成手动下载链接（需要从 CSV 读取 meeting_id）
    if missing:
        meeting_map = load_meeting_map(CSV_FILE)
        generate_manual_download_commands(missing, meeting_map)