import requests
from bs4 import BeautifulSoup

# 下载 PDF 的函数
def download_pdf(url, save_path):
    try:
        # 获取网页内容
        response = requests.get(url)
        if response.status_code != 200:
            print(f"无法访问页面，状态码: {response.status_code}")
            return
        
        # 解析页面内容
        soup = BeautifulSoup(response.text, 'html.parser')
        # 查找PDF下载链接
        pdf_button = soup.find('a', {'data-track-action': 'Download PDF'})
        if not pdf_button:
            print("未找到PDF下载链接")
            return
        
        pdf_url = pdf_button['href']
        # 如果链接是相对路径，补全为绝对路径
        if pdf_url.startswith('/'):
            pdf_url = "https://link.springer.com" + pdf_url
        
        # 下载PDF
        print(f"正在下载PDF: {pdf_url}")
        pdf_response = requests.get(pdf_url)
        if pdf_response.status_code == 200:
            with open(save_path, 'wb') as pdf_file:
                pdf_file.write(pdf_response.content)
            print(f"PDF已成功保存到: {save_path}")
        else:
            print(f"无法下载PDF，状态码: {pdf_response.status_code}")
    except Exception as e:
        print(f"发生错误: {e}")

# 目标链接
url = "https://link.springer.com/article/10.1007/s12182-021-00567-w"
# 指定保存路径
save_path = "../downloaded"

# 执行下载
download_pdf(url, save_path)