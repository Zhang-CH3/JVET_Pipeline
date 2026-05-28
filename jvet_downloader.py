#!/usr/bin/env python3
"""
JVET 文档批量下载脚本
功能：读取 CSV 文件中的 meeting_id 和 document_id，自动尝试下载文档的 ZIP 包
"""

import csv
import requests
import time
import os
from pathlib import Path
from typing import List, Tuple, Optional

# ==================== 配置区域（用户可修改）====================
# 请求间隔时间（单位：秒）
# 建议：1.0 ~ 3.0 秒。太短可能被服务器封 IP，太长下载慢
REQUEST_INTERVAL_SECONDS = 1.5

# 最大尝试版本号（v1, v2, v3, v4 ...）
MAX_VERSION = 4

# 下载超时时间（单位：秒）
DOWNLOAD_TIMEOUT = 30

# 输出目录
OUTPUT_DIR = "./downloaded_docs"

# CSV 文件路径（请修改为你的文件）
CSV_FILE_PATH = "jvet_documents_cccm.csv"
# ================================================================


def build_download_url(meeting_id: str, document_id: str, version: int) -> str:
    """
    构造下载链接
    
    格式：https://jvet-experts.org/doc_end_user/documents/{meeting_id}/wg11/{document_id}-v{version}.zip
    
    参数：
        meeting_id: 例如 "42_SantaEularia"
        document_id: 例如 "JVET-AP0105"
        version: 版本号 1, 2, 3, 4
    
    返回：
        完整的下载 URL
    """
    return f"https://jvet-experts.org/doc_end_user/documents/{meeting_id}/wg11/{document_id}-v{version}.zip"


def download_file(url: str, output_path: Path) -> bool:
    """
    下载文件到指定路径
    
    参数：
        url: 下载链接
        output_path: 本地保存路径
    
    返回：
        True 表示下载成功，False 表示失败
    """
    try:
        # headers: 模拟浏览器访问，避免被拒绝
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, stream=True, headers=headers, timeout=DOWNLOAD_TIMEOUT)
        
        if response.status_code == 200:
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            return True
        else:
            return False
            
    except Exception as e:
        print(f"    异常: {e}")
        return False


def read_csv_documents(csv_path: str) -> List[Tuple[str, str]]:
    """
    读取 CSV 文件，返回文档列表
    
    参数：
        csv_path: CSV 文件路径
    
    返回：
        [(meeting_id, document_id), ...] 列表
    """
    documents = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            meeting_id = row['meeting_id'].strip()
            document_id = row['document_id'].strip()
            documents.append((meeting_id, document_id))
    return documents


def main():
    """主函数"""
    print("=" * 60)
    print("JVET 文档批量下载脚本")
    print(f"配置文件: {CSV_FILE_PATH}")
    print(f"请求间隔: {REQUEST_INTERVAL_SECONDS} 秒")
    print(f"最大版本号: v{MAX_VERSION}")
    print(f"输出目录: {OUTPUT_DIR}")
    print("=" * 60)
    
    # 创建输出目录
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
    
    # 读取 CSV
    if not Path(CSV_FILE_PATH).exists():
        print(f"\n错误：找不到文件 {CSV_FILE_PATH}")
        print("请修改脚本中的 CSV_FILE_PATH 变量")
        return
    
    documents = read_csv_documents(CSV_FILE_PATH)
    print(f"\n共读取 {len(documents)} 个文档")
    
    # 统计
    success_count = 0
    fail_count = 0
    skip_count = 0
    
    # 逐个下载
    for idx, (meeting_id, document_id) in enumerate(documents, 1):
        print(f"\n[{idx}/{len(documents)}] 处理: {document_id} ({meeting_id})")
        
        downloaded = False
        for version in range(1, MAX_VERSION + 1):
            # 构造 URL 和本地文件名
            url = build_download_url(meeting_id, document_id, version)
            filename = f"{document_id}_v{version}.zip"
            output_path = Path(OUTPUT_DIR) / filename
            
            # 如果文件已存在，跳过
            if output_path.exists():
                file_size = output_path.stat().st_size
                print(f"    文件已存在，跳过: {filename} ({file_size} bytes)")
                skip_count += 1
                downloaded = True
                break
            
            # 尝试下载
            print(f"    尝试版本 v{version}...")
            if download_file(url, output_path):
                file_size = output_path.stat().st_size
                print(f"    ✅ 下载成功: {filename} ({file_size} bytes)")
                success_count += 1
                downloaded = True
                break
            else:
                print(f"    ❌ 版本 v{version} 不存在")
            
            # 请求间隔（避免被封）
            if version < MAX_VERSION:
                time.sleep(REQUEST_INTERVAL_SECONDS)
        
        if not downloaded:
            print(f"    ⚠️ 未找到该文档的任何版本 (v1-v{MAX_VERSION})")
            fail_count += 1
        
        # 每个文档之间的间隔
        if idx < len(documents):
            time.sleep(REQUEST_INTERVAL_SECONDS)
    
    # 输出统计
    print("\n" + "=" * 60)
    print("下载完成！")
    print(f"✅ 成功: {success_count}")
    print(f"⏭️ 跳过（已存在）: {skip_count}")
    print(f"❌ 失败: {fail_count}")
    print(f"📁 文件保存在: {Path(OUTPUT_DIR).absolute()}")
    print("=" * 60)


if __name__ == "__main__":
    main()