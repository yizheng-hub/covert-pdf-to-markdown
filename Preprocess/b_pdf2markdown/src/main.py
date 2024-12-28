import os
import subprocess

def convert_pdfs_to_markdown(input_folder, output_folder):
    # 确保输出文件夹存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 遍历输入文件夹中的所有文件
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if file.lower().endswith('.pdf'):
                pdf_path = os.path.join(root, file)
                output_name = os.path.splitext(file)[0]  # 获取文件名（不带扩展名）
                output_dir = os.path.join(output_folder, output_name)

                # 构建 nougat 命令
                command = [
                    'nougat', '--markdown', pdf_path,
                    '-o', output_dir,
                    '--recompute'  # 如果需要重新处理已经存在的文件，请保留此参数
                ]

                print(f"Processing {pdf_path}...")
                try:
                    result = subprocess.run(command, check=True, capture_output=True, text=True)
                    print("转换成功:", result.stdout)
                except subprocess.CalledProcessError as e:
                    print(f"转换失败: {e.stderr}")

if __name__ == "__main__":
    input_folder = "../../a_download/downloaded"  # 替换为你的PDF文件夹路径
    output_folder = "output_directory"  # 替换为你想要保存Markdown文件的路径
    
    convert_pdfs_to_markdown(input_folder, output_folder)