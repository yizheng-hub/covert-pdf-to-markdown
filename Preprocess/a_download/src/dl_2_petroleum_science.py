import requests
from bs4 import BeautifulSoup
import os

# 生成 ScienceDirect 链接列表
def generate_sciencedirect_links(start_volume, end_volume, issue_range):
    links = []
    for volume in range(start_volume, end_volume + 1):  # 遍历 volume
        for issue in range(1, issue_range + 1):  # 遍历 issue
            link = f"https://www.sciencedirect.com/journal/petroleum-science/vol/{volume}/issue/{issue}"
            links.append(link)
    return links

# 提取 PDF 链接
def extract_pdf_links(issue_url):
    try:
        # 发送 GET 请求获取网页内容
        response = requests.get(issue_url)
        if response.status_code == 403:
            print(f"403 Forbidden: 无法访问 {issue_url}")
            return None
        if response.status_code == 404:
            print(f"Issue 不存在，跳过: {issue_url}")
            return []  # 返回空列表
        # response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 从 </style><div class="app sd-flex-container"> 后查找所有的 href 链接
        pdf_links = []
        container = soup.find('div', class_='app sd-flex-container')
        
        if container:
            for a_tag in container.find_all('a', href=True):
                href = a_tag['href']
                if href.endswith('main.pdf'):  # 检查是否以 main.pdf 结尾
                    pdf_links.append(f"{href}")

        if not pdf_links:
            print(f"未找到 PDF 链接: {issue_url}")
        return pdf_links

    except requests.exceptions.RequestException as e:
        print(f"请求过程中发生错误: {e}")
        return []

# 下载 PDF 文件
def download_pdf(pdf_url, save_dir):
    try:
        # 下载 PDF 文件
        response = requests.get(pdf_url, stream=True)
        response.raise_for_status()

        # 生成保存文件名
        file_name = pdf_url.split("/")[-1]
        save_path = os.path.join(save_dir, file_name)

        # 保存 PDF 文件
        with open(save_path, 'wb') as pdf_file:
            for chunk in response.iter_content(chunk_size=1024):
                pdf_file.write(chunk)

        print(f"PDF 文件已成功下载并保存到: {save_path}")

    except requests.exceptions.RequestException as e:
        print(f"请求过程中发生错误: {e}")
    except Exception as e:
        print(f"发生错误: {e}")

# 主函数：运行流程
def main():
    # 配置参数
    start_volume = 18
    end_volume = 21
    issue_range = 6
    save_dir = "../downloads/Petroleum_Science_until2024"  # 下载目录

    # 创建保存目录
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # 生成 Issue 链接列表
    issue_links = generate_sciencedirect_links(start_volume, end_volume, issue_range)
    # print(issue_links)
    for issue_url in issue_links:
        print(f"正在处理 Issue: {issue_url}")

        # 提取 PDF 链接
        pdf_links = extract_pdf_links(issue_url)
        if not pdf_links:
            continue
        print(pdf_links)
        # 下载每个 PDF 文件
        # for pdf_url in pdf_links:
        #     print(f"正在下载 PDF: {pdf_url}")
        #     download_pdf(pdf_url, save_dir)

if __name__ == "__main__":
    main()