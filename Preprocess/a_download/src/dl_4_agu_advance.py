import os
import requests
import time

class PDFExtractor:
    def __init__(self):
        self.session = requests.Session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        }
        self.session.headers.update(self.headers)
        self.base_url = "https://agupubs.onlinelibrary.wiley.com"

    def extract_dois_from_html(self, html_file_path):
        """从HTML文件中提取DOI"""
        try:
            with open(html_file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            dois = []
            # 找到所有包含issue-item__title visitable的行
            for line in content.split('\n'):
                if 'issue-item__title visitable' in line:
                    # 查找/doi/后面的内容
                    doi_start = line.find('/doi/')
                    if doi_start != -1:
                        # 找到引号结束的位置
                        doi_end = line.find('"', doi_start)
                        if doi_end != -1:
                            doi = line[doi_start:doi_end]
                            dois.append(doi)
            
            return dois
            
        except Exception as e:
            print(f"处理文件 {html_file_path} 时发生错误: {e}")
            return []

    def download_pdf(self, doi, save_dir):
        """下载PDF文件"""
        try:
            pdf_url = f"{self.base_url}{doi.replace('/doi/', '/doi/pdfdirect/')}"
            print(f"正在下载: {pdf_url}")
            
            # 使用DOI作为文件名
            file_name = f"{doi.split('/')[-1]}.pdf"
            save_path = os.path.join(save_dir, file_name)

            # 检查文件是否已存在
            if os.path.exists(save_path):
                print(f"文件已存在，跳过: {file_name}")
                return

            # 下载PDF
            pdf_response = self.session.get(pdf_url, stream=True)
            pdf_response.raise_for_status()

            # 保存文件
            with open(save_path, 'wb') as pdf_file:
                for chunk in pdf_response.iter_content(chunk_size=1024):
                    pdf_file.write(chunk)

            print(f"PDF文件已保存: {save_path}")
            time.sleep(2)  # 下载间隔

        except requests.exceptions.RequestException as e:
            print(f"下载过程中发生错误: {e}")
        except Exception as e:
            print(f"发生错误: {e}")

def main():
    # 设置路径
    html_dir = "../agu"  # HTML源文件目录
    save_dir = "../downloads/AGU_Articles"  # PDF保存目录
    
    # 创建保存目录
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # 创建提取器实例
    extractor = PDFExtractor()

    # 处理所有HTML文件
    for filename in os.listdir(html_dir):
        if filename.endswith('.html'):
            html_path = os.path.join(html_dir, filename)
            print(f"\n处理文件: {filename}")
            
            # 提取DOI
            dois = extractor.extract_dois_from_html(html_path)
            
            if not dois:
                print(f"在文件 {filename} 中未找到DOI")
                continue

            print(f"找到 {len(dois)} 个DOI")
            
            # 下载PDF
            for doi in dois:
                extractor.download_pdf(doi, save_dir)

if __name__ == "__main__":
    main()