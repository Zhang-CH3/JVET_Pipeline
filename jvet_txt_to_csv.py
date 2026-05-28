# type: ignore
import re
import csv
from pathlib import Path

def parse_jvet_txt_to_csv(input_txt: str, output_csv: str = "jvet_documents.csv"):
    """
    读取 JVET 格式的 txt 文件，生成 CSV。
    
    txt 格式示例：
        JVET-42
        SantaEularia
        JVET-AP0168	EE2-1.3: ...	...	2026-04-17
        JVET-42
        SantaEularia
        JVET-AP0199	Crosscheck ...	...	2026-04-17
    
    CSV 输出列：meeting_id, document_id
    """
    # 读取 txt 文件
    with open(input_txt, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    
    records = []
    i = 0
    total_lines = len(lines)
    
    while i < total_lines:
        line1 = lines[i]
        
        # 匹配会议编号：JVET-42 或 JVET42 或 42
        match_num = re.search(r"JVET[-_]?(\d+)", line1, re.IGNORECASE)
        if not match_num:
            i += 1
            continue
        
        meeting_num = match_num.group(1)
        
        # 下一行必须是地点（纯字母）
        if i + 1 >= total_lines:
            break
        location = lines[i + 1].strip()
        if not re.match(r"^[A-Za-z]+", location):
            i += 1
            continue
        
        meeting_id = f"{meeting_num}_{location}"
        i += 2  # 移到文档行
        
        # 收集归属当前会议的所有文档
        while i < total_lines:
            current_line = lines[i]
            # 遇到新的会议标识则停止
            if re.search(r"^JVET[-_]?\d+", current_line, re.IGNORECASE):
                break
            
            # 匹配文档编号 JVET-XXXXX
            doc_match = re.search(r"(JVET-[A-Z0-9]+)", current_line, re.IGNORECASE)
            if doc_match:
                doc_id = doc_match.group(1).upper()
                records.append([meeting_id, doc_id])
            i += 1
    
    # 写入 CSV
    with open(output_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["meeting_id", "document_id"])
        writer.writerows(records)
    
    print(f"读取文件: {input_txt}")
    print(f"生成 CSV: {output_csv}")
    print(f"共 {len(records)} 条记录")
    return records


if __name__ == "__main__":
    # ===== 修改这里的文件路径 =====
    input_file = "jvet_cccm.txt"      # 你的输入 txt 文件名
    output_file = "jvet_documents_cccm.csv"
    
    # 检查文件是否存在
    if not Path(input_file).exists():
        print(f"错误：找不到文件 {input_file}")
        print("请将 txt 文件放在脚本同目录下，或修改 input_file 变量为完整路径")
    else:
        parse_jvet_txt_to_csv(input_file, output_file)