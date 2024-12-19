import os
import PyPDF2
from pathlib import Path

def check_pdf(file_path):
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            num_pages = len(pdf_reader.pages)
            # 尝试读取每一页以确保完整性
            for page_num in range(num_pages):
                pdf_reader.pages[page_num]
            return True, num_pages
    except FileNotFoundError:
        return False, "文件不存在"
    except PyPDF2.errors.PdfReadError:
        return False, "PDF文件已损坏"
    except Exception as e:
        return False, f"检查错误: {str(e)}"

def process_pdf_folder(folder_path):
    # 统计数据
    valid_count = 0
    deleted_count = 0
    error_files = []
    
    # 确保文件夹路径存在
    folder_path = Path(folder_path)
    if not folder_path.exists():
        print(f"文件夹 {folder_path} 不存在")
        return

    # 遍历文件夹中的所有PDF文件
    for pdf_file in folder_path.glob("**/*.pdf"):
        print(f"\n检查文件: {pdf_file}")
        is_valid, result = check_pdf(pdf_file)
        
        if is_valid:
            valid_count += 1
            print(f"√ 正常 - 页数: {result}")
        else:
            deleted_count += 1
            error_files.append((str(pdf_file), result))
            print(f"× 损坏 - 原因: {result}")
            try:
                # 删除损坏的文件
                pdf_file.unlink()
                print(f"已删除: {pdf_file}")
            except Exception as e:
                print(f"删除失败: {str(e)}")

    # 打印统计结果
    print("\n====== 检查完成 ======")
    print(f"正常文件数: {valid_count}")
    print(f"删除文件数: {deleted_count}")
    
    if error_files:
        print("\n已删除的损坏文件列表:")
        for file_path, error in error_files:
            print(f"- {file_path}: {error}")

# 使用示例
folder_path = "../downloads/Petroleum_Science_until2024"
# folder_path = "../downloads/Petroleum_Science"
# folder_path = "../downloads/Nature_Geoscience"

process_pdf_folder(folder_path)