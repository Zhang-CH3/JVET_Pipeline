---

# JVET_Pipeline / JVET 文档批量处理工具集

> **English** | [**中文**](#中文版)

---

## English Version

# JVET_Pipeline: JVET Document Batch Processing Toolkit

A set of Python scripts for batch downloading JVET proposals and converting them into plain text format for AI-assisted analysis.

## Scripts

| Script | Function | Dependencies |
| :--- | :--- | :--- |
| `jvet_txt_to_csv.py` | Convert JVET search results to CSV list | None (standard library only) |
| `jvet_downloader.py` | Batch download ZIP files from CSV list | `requests` |
| `check_missing.py` | Check download status, generate missing list | None (standard library only) |
| `convert_docs_to_txt.py` | Convert Word/PPT to plain text | `python-docx`, `python-pptx` |
| `merge_txt.py` | Merge all TXT files into one | None (standard library only) |

## Installation

```bash
# Core dependency (required for downloader)
pip install requests

# Optional: for document conversion
pip install python-docx python-pptx

# Optional: for legacy .doc/.ppt files
# pip install textract
```

## Usage

### Step 1: Search Results → CSV

**Input**: Copied text from JVET search results

**Operation**:
1. Search JVET website with keywords (e.g., `CCCM`)
2. Copy the result table, save as `.txt` (e.g., `jvet_cccm.txt`)
3. Run the script

```bash
python jvet_txt_to_csv.py
```

**Output**: CSV file with `meeting_id` and `document_id` columns

**CSV Example**:
```csv
meeting_id,document_id
42_SantaEularia,JVET-AP0105
42_SantaEularia,JVET-AP0168
41_Teleconference,JVET-AO0070
```

### Step 2: Batch Download ZIP Files

**Input**: CSV file from Step 1

**Configuration** (edit at top of script):

```python
CSV_FILE_PATH = "jvet_documents.csv"        # Path to CSV file
OUTPUT_DIR = "./downloaded_docs"            # Download directory
REQUEST_INTERVAL_SECONDS = 1.5              # Request interval (seconds)
MAX_VERSION = 4                             # Maximum version to try
```

**Run**:

```bash
python jvet_downloader.py
```

**Notes**:
- Tries versions v1 to v4, downloads the first existing version
- Skips already downloaded files
- Increase `REQUEST_INTERVAL_SECONDS` if network is slow

### Step 3: Check Download Status

**Input**: CSV file + `downloaded_docs/` directory

**Run**:

```bash
python check_missing.py
```

**Output**:
- Statistics of completed/missing documents
- Missing document list (saved to `missing_docs.txt`)
- Version information for downloaded documents

### Step 4: Extract and Convert to TXT

**Pre-step**: Manually extract all ZIP files to `docs_decomp/` (or change `INPUT_DIR`)

**Configuration**:

```python
INPUT_DIR = "./docs_decomp"      # Original files directory
OUTPUT_DIR = "./docs_txt"        # TXT output directory
```

**Run**:

```bash
python convert_docs_to_txt.py
```

**Supported formats**: `.docx`, `.pptx`, `.doc`, `.ppt` (legacy requires `textract`)

### Step 5: Merge All TXT Files

**Input**: All `.txt` files in `docs_txt/` directory

**Configuration**:

```python
INPUT_DIR = "./docs_txt"          # TXT files directory
OUTPUT_FILE = "./merged.txt"      # Output merged file
SEPARATOR = True                  # Add separator between files
SHOW_FILENAME = True              # Show filename before content
```

**Run**:

```bash
python merge_txt.py
```

**Output**: `merged.txt` - ready to feed into AI for analysis

## Workflow Diagram

```
Web Text → CSV → ZIP Download → Extract → Word/PPT → TXT Convert → TXT Merge → AI Analysis
   ↓         ↓         ↓            ↓           ↓            ↓           ↓
 Copy     csv_     downloader   manual      convert_      merge_     prompt
 Save    to_csv              (or script)  docs_to_txt    txt       template
```

## FAQ

### Q1: Slow download or timeout?

- Increase `REQUEST_INTERVAL_SECONDS` to 3-5 seconds
- Use `check_missing.py` to find missing documents, manually download during off-peak hours
- Or change the meeting_id in CSV to a wrong value (e.g., `39_Daejeon` → `39_Caejeon`) to skip, then download manually

### Q2: `requests` library not found?

```bash
pip install requests
```

### Q3: Error converting Word/PPT?

Make sure dependencies are installed:
```bash
pip install python-docx python-pptx
```

### Q4: No `meeting_id` in CSV?

Check if the input text format is correct. It should look like:

```text
JVET-42
SantaEularia
JVET-AP0105	Title...
```

## File Summary

| File | Description |
| :--- | :--- |
| `jvet_txt_to_csv.py` | Text → CSV converter |
| `jvet_downloader.py` | Batch downloader |
| `check_missing.py` | Download checker |
| `convert_docs_to_txt.py` | Document → TXT converter |
| `merge_txt.py` | TXT merger |
| `README.md` | This file |

---

## 中文版

# JVET_Pipeline：JVET 文档批量处理工具集

本工具集用于从 JVET 网站批量下载提案文档，并转换为适合 AI 分析的纯文本格式。

## 工具列表

| 脚本 | 功能 | 依赖 |
| :--- | :--- | :--- |
| `jvet_txt_to_csv.py` | 将 JVET 搜索结果文本转换为 CSV 清单 | 无（仅标准库） |
| `jvet_downloader.py` | 根据 CSV 清单批量下载 ZIP 文件 | `requests` |
| `check_missing.py` | 检查下载完成情况，生成缺失列表 | 无（仅标准库） |
| `convert_docs_to_txt.py` | 将 Word/PPT 转换为纯文本 | `python-docx`, `python-pptx` |
| `merge_txt.py` | 合并所有 TXT 文件为一个文件 | 无（仅标准库） |

## 安装依赖

```bash
# 基础依赖（下载器需要）
pip install requests

# 文档转换需要（可选，不转换可跳过）
pip install python-docx python-pptx

# 如需处理旧版 .doc/.ppt，额外安装
# pip install textract
```

## 使用流程

### 步骤1：获取搜索结果文本 → CSV

**输入**：从 JVET 网站复制的搜索结果文本

**操作**：
1. 在 JVET 网站搜索关键词（如 `CCCM`）
2. 复制结果文本，保存为 `.txt` 文件（如 `jvet_cccm.txt`）
3. 运行脚本

```bash
python jvet_txt_to_csv.py
```

**输出**：CSV 文件，包含 `meeting_id` 和 `document_id` 两列

**CSV 格式示例**：
```csv
meeting_id,document_id
42_SantaEularia,JVET-AP0105
42_SantaEularia,JVET-AP0168
41_Teleconference,JVET-AO0070
```

### 步骤2：批量下载 ZIP 文件

**输入**：上一步生成的 CSV 文件

**配置**（修改脚本顶部）：

```python
CSV_FILE_PATH = "jvet_documents.csv"        # CSV 文件路径
OUTPUT_DIR = "./downloaded_docs"            # 下载目录
REQUEST_INTERVAL_SECONDS = 1.5              # 请求间隔（秒）
MAX_VERSION = 4                             # 最大尝试版本号
```

**运行**：

```bash
python jvet_downloader.py
```

**说明**：
- 脚本会从 v1 到 v4 依次尝试，下载第一个存在的版本
- 已存在的文件会自动跳过
- 网络慢时可适当增加 `REQUEST_INTERVAL_SECONDS`

### 步骤3：检查下载完成情况

**输入**：CSV 文件 + `downloaded_docs/` 目录

**运行**：

```bash
python check_missing.py
```

**输出**：
- 已完成/缺失文档统计
- 缺失文档列表（保存至 `missing_docs.txt`）
- 已下载文档的版本号

### 步骤4：解压并转换为 TXT

**前置**：手动解压所有 ZIP 文件到 `docs_decomp/` 目录（或修改 `INPUT_DIR`）

**配置**：

```python
INPUT_DIR = "./docs_decomp"      # 原始文件目录
OUTPUT_DIR = "./docs_txt"        # 输出 TXT 目录
```

**运行**：

```bash
python convert_docs_to_txt.py
```

**支持格式**：`.docx`, `.pptx`, `.doc`, `.ppt`（旧版需要 `textract`）

### 步骤5：合并所有 TXT 文件

**输入**：`docs_txt/` 目录下的所有 `.txt` 文件

**配置**：

```python
INPUT_DIR = "./docs_txt"          # TXT 文件目录
OUTPUT_FILE = "./merged.txt"      # 合并后的输出文件
SEPARATOR = True                  # 是否添加分隔符
SHOW_FILENAME = True              # 是否显示文件名
```

**运行**：

```bash
python merge_txt.py
```

**输出**：`merged.txt`，可直接喂给 AI 进行分析

## 完整工作流示意图

```text
网页文本 → CSV → ZIP下载 → 解压 → Word/PPT → TXT转换 → TXT合并 → AI分析
    ↓        ↓         ↓         ↓           ↓          ↓         ↓
 复制     csv_     downloader  手动解压   convert_      merge_   提示词
 保存    to_csv               (或用脚本)  docs_to_txt    txt      模板
```

## 常见问题

### Q1：下载速度慢或超时怎么办？

- 增加 `REQUEST_INTERVAL_SECONDS` 到 3-5 秒
- 使用 `check_missing.py` 找出缺失文档，凌晨时段手动下载
- 或将 CSV 中卡住的文档对应的**会议名**改成错误的（如 `39_Daejeon` → `39_Caejeon`），跳过然后手动下载

### Q2：提示找不到 `requests` 库？

```bash
pip install requests
```

### Q3：转换 Word/PPT 时报错？

确认已安装依赖：
```bash
pip install python-docx python-pptx
```

### Q4：CSV 中没有 `meeting_id`？

检查输入文本格式是否正确。需要包含类似：

```text
JVET-42
SantaEularia
JVET-AP0105	标题...
```

## 文件清单

| 文件 | 说明 |
| :--- | :--- |
| `jvet_txt_to_csv.py` | 文本 → CSV 转换 |
| `jvet_downloader.py` | 批量下载 |
| `check_missing.py` | 下载检查 |
| `convert_docs_to_txt.py` | 文档 → TXT 转换 |
| `merge_txt.py` | TXT 合并 |
| `README.md` | 本文件 |

---


## Contact

Issues and pull requests are welcome.
