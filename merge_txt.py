#!/usr/bin/env python3
"""
合并指定文件夹及其子文件夹中的所有 TXT 文件
支持按文件名排序、添加文件分隔符
"""

import os
from pathlib import Path

# ==================== 配置区域 ====================
INPUT_DIR = "./docs_txt"          # 存放 TXT 文件的目录（会递归搜索）
OUTPUT_FILE = "./merged.txt"      # 合并后的输出文件
SEPARATOR = True                  # 是否在文件之间添加分隔符
SEPARATOR_LINE = "=" * 80         # 分隔符内容（当 SEPARATOR=True 时生效）
SHOW_FILENAME = True              # 是否在每个文件内容前显示文件名
SORT_BY_NAME = True               # 是否按文件名排序
# =================================================


def merge_txt_files(input_dir: Path, output_file: Path):
    """合并所有 TXT 文件"""
    
    # 收集所有 TXT 文件
    if SORT_BY_NAME:
        txt_files = sorted(input_dir.rglob("*.txt"))
    else:
        txt_files = list(input_dir.rglob("*.txt"))
    
    if not txt_files:
        print(f"错误：在 {input_dir} 中未找到任何 .txt 文件")
        return
    
    print(f"找到 {len(txt_files)} 个 TXT 文件")
    print(f"输出文件: {output_file}")
    print("-" * 50)
    
    # 合并写入
    with open(output_file, 'w', encoding='utf-8') as out_f:
        for idx, file_path in enumerate(txt_files, 1):
            # 计算相对路径（相对于输入目录）
            rel_path = file_path.relative_to(input_dir)
            
            print(f"  [{idx}/{len(txt_files)}] {rel_path}")
            
            # 添加文件头分隔符
            if SEPARATOR and idx > 1:
                out_f.write(f"\n{SEPARATOR_LINE}\n\n")
            
            if SHOW_FILENAME:
                out_f.write(f"【文件】: {rel_path}\n")
                out_f.write(f"{'-' * 40}\n")
            
            # 读取并写入文件内容
            try:
                with open(file_path, 'r', encoding='utf-8') as in_f:
                    content = in_f.read()
                    out_f.write(content)
                    # 确保文件末尾有换行
                    if content and not content.endswith('\n'):
                        out_f.write('\n')
            except Exception as e:
                out_f.write(f"[读取失败: {e}]\n")
                print(f"    警告: 读取失败 - {e}")
    
    print("-" * 50)
    print(f"✅ 合并完成！输出文件: {output_file.absolute()}")
    print(f"文件大小: {output_file.stat().st_size / 1024:.2f} KB")


def main():
    input_dir = Path(INPUT_DIR)
    output_file = Path(OUTPUT_FILE)
    
    if not input_dir.exists():
        print(f"错误：输入目录不存在 - {INPUT_DIR}")
        return
    
    # 确保输出目录存在
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    merge_txt_files(input_dir, output_file)


if __name__ == "__main__":
    main()