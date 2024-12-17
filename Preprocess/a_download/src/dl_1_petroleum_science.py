import requests
from bs4 import BeautifulSoup
import os

# 生成 Springer 链接列表
def generate_springer_links(start_volume, end_volume, issue_range):
    links = []
    for volume in range(start_volume, end_volume + 1):  # 遍历 volume
        for issue in range(1, issue_range + 1):  # 遍历 issue
            link = f"https://link.springer.com/journal/12182/volumes-and-issues/{volume}-{issue}"
            links.append(link)
    return links

# 提取 Issue 中的文章链接
def extract_article_links(issue_url):
    try:
        # 发送 GET 请求获取网页内容
        response = requests.get(issue_url)
        if response.status_code == 404:
            print(f"Issue 不存在，跳过: {issue_url}")
            return []  # 返回空列表

        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # 查找所有包含文章链接的 h3.app-card-open__heading 元素
        article_links = []
        headings = soup.find_all('h3', class_='app-card-open__heading')
        for heading in headings:
            link = heading.find('a')
            if link and 'href' in link.attrs:
                article_links.append(f"{link['href']}")

        if not article_links:
            print(f"未找到文章链接: {issue_url}")
        return article_links

    except requests.exceptions.RequestException as e:
        print(f"请求过程中发生错误: {e}")
        return []

# 下载 PDF 文件
def download_pdf(article_url, save_dir):
    try:
        # 发送 GET 请求获取文章页面内容
        response = requests.get(article_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # 查找 PDF 下载链接
        pdf_url = soup.find('meta', {'name': 'citation_pdf_url'})
        if not pdf_url:
            print(f"未找到 PDF 下载链接: {article_url}")
            return

        pdf_url = pdf_url['content']
        print(f"发现 PDF 下载链接: {pdf_url}")

        # 下载 PDF 文件
        pdf_response = requests.get(pdf_url, stream=True)
        pdf_response.raise_for_status()

        # 生成保存文件名
        article_title = soup.find('h1', class_='c-article-title')
        if article_title:
            file_name = article_title.text.strip().replace(" ", "_") + ".pdf"
        else:
            file_name = article_url.split("/")[-1] + ".pdf"

        save_path = os.path.join(save_dir, file_name)

        # 保存 PDF 文件
        with open(save_path, 'wb') as pdf_file:
            for chunk in pdf_response.iter_content(chunk_size=1024):
                pdf_file.write(chunk)

        print(f"PDF 文件已成功下载并保存到: {save_path}")

    except requests.exceptions.RequestException as e:
        print(f"请求过程中发生错误: {e}")
    except Exception as e:
        print(f"发生错误: {e}")


def main():
    # 配置参数
    start_volume = 4
    end_volume = 18
    issue_range = 6
    save_dir = "../downloads/Petroleum_Science "  # 下载目录

    # 创建保存目录
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # 生成 Issue 链接列表
    issue_links = generate_springer_links(start_volume, end_volume, issue_range)
    # print(issue_links)
    for issue_url in issue_links:
        print(f"正在处理 Issue: {issue_url}")

        # 提取文章链接
        article_links = extract_article_links(issue_url)
        print(article_links)
        if not article_links:
            continue

        # 下载每篇文章的 PDF
        for article_url in article_links:
            print(f"正在下载文章: {article_url}")
            download_pdf(article_url, save_dir)

if __name__ == "__main__":
    main()