import os

def rename_zip_to_mp4(root_folder):
    """
    递归遍历 root_folder 及其所有子文件夹，
    将所有 .zip 文件重命名为 .mp4
    """
    for dirpath, dirnames, filenames in os.walk(root_folder):
        for filename in filenames:
            if filename.lower().endswith('.zip'):
                old_path = os.path.join(dirpath, filename)
                # 替换后缀为 .mp4
                new_filename = filename[:-4] + '.mp4'  # 去掉最后4个字符（.zip），加上.mp4
                new_path = os.path.join(dirpath, new_filename)
                
                try:
                    os.rename(old_path, new_path)
                    print(f"已重命名: {old_path} -> {new_path}")
                except OSError as e:
                    print(f"重命名失败: {old_path} -> {new_path}, 错误: {e}")

if __name__ == "__main__":
    # 设置要处理的根文件夹路径
    folder_path = input("请输入要处理的文件夹路径（直接回车则处理当前目录）: ").strip()
    if not folder_path:
        folder_path = os.getcwd()  # 当前工作目录
    
    if not os.path.isdir(folder_path):
        print("错误：指定的路径不是一个有效文件夹。")
    else:
        print(f"开始处理文件夹: {folder_path}")
        rename_zip_to_mp4(folder_path)
        print("处理完成！")