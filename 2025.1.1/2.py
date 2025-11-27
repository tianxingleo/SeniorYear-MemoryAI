import os
import argparse

def rename_zip_to_mp4(directory):
    """
    将指定目录下所有 .zip 文件重命名为 .mp4
    """
    # 遍历目录中的所有文件
    for filename in os.listdir(directory):
        # 检查是否是以 .zip 结尾（不区分大小写）
        if filename.lower().endswith('.zip'):
            old_path = os.path.join(directory, filename)
            # 构造新文件名：去掉.zip，加上.mp4
            new_filename = filename[:-4] + '.mp4'
            new_path = os.path.join(directory, new_filename)
            
            # 重命名文件
            try:
                os.rename(old_path, new_path)
                print(f"已重命名: {filename} → {new_filename}")
            except OSError as e:
                print(f"重命名失败: {filename} - {e}")

def main():
    parser = argparse.ArgumentParser(description="批量将 .zip 文件后缀改为 .mp4")
    parser.add_argument(
        "directory",
        nargs="?",
        default=".",
        help="要处理的目录路径（默认为当前目录）"
    )
    args = parser.parse_args()
    
    rename_zip_to_mp4(args.directory)

if __name__ == "__main__":
    main()