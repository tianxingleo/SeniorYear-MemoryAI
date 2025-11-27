import os
import re
from datetime import datetime, date, timedelta

def generate_video_notes(root_dir="."):
    """
    扫描指定目录及其子目录下的所有 .mp4 文件，并生成同名的 Markdown 笔记文件。
    笔记文件包含视频的拍摄时间（从文件名提取）和距离特定日期的天数。
    
    Args:
        root_dir (str): 扫描的起始目录。默认为当前目录。
    """
    
    # 目标高考日期：2025年6月7日
    target_date = date(2025, 6, 7)
    
    # 匹配视频文件名的正则表达式
    # 示例文件名: DJI_20241025225132_0172_D.mp4
    # 匹配 group 1: 20241025225132 (年月日时分秒)
    # 匹配 group 2: _0172_D (或其他后缀)
    # 注意：这个正则假定日期时间部分是连续的14位数字
    pattern = re.compile(r"DJI_(\d{14})(_.*)?\.mp4$", re.IGNORECASE)

    print(f"--- 开始扫描目录: {os.path.abspath(root_dir)} ---")

    # 遍历根目录及其所有子目录
    for foldername, subfolders, filenames in os.walk(root_dir):
        for filename in filenames:
            # 确保文件是 .mp4 格式
            if filename.lower().endswith(".mp4"):
                match = pattern.match(filename)
                
                if match:
                    # 1. 提取时间字符串
                    time_str = match.group(1)
                    try:
                        # 将字符串解析为 datetime 对象
                        video_datetime = datetime.strptime(time_str, "%Y%m%d%H%M%S")
                        
                        # 2. 计算天数差
                        current_date = video_datetime.date()
                        
                        # 计算天数差，取绝对值，然后确定方向
                        delta: timedelta = target_date - current_date
                        days_difference = delta.days
                        
                        if days_difference > 0:
                            countdown_message = f"距离 2025年6月7日高考还有 {days_difference} 天"
                        elif days_difference < 0:
                            countdown_message = f"2025年6月7日高考已过去 {abs(days_difference)} 天"
                        else:
                            countdown_message = "今天是 2025年6月7日高考日！"
                        
                        # 3. 格式化视频拍摄时间
                        formatted_time = video_datetime.strftime("%Y年%m月%d日 %H时%M分%S秒")
                        
                        # 4. 准备 Markdown 内容
                        markdown_content = f"""# 视频信息 - {filename}

## 拍摄时间
- **日期时间:** {formatted_time}

## 时间计算
- **特定日期:** {target_date.strftime("%Y年%m月%d日")}
- **倒计时/已过天数:** {countdown_message}

---

## 视频备注
"""
                        
                        # 5. 生成 Markdown 文件路径和文件名
                        base_name = os.path.splitext(filename)[0]
                        md_filename = base_name + ".md"
                        md_path = os.path.join(foldername, md_filename)
                        
                        # 6. 写入文件
                        try:
                            with open(md_path, 'w', encoding='utf-8') as f:
                                f.write(markdown_content)
                            print(f"[成功] 生成笔记: {md_path}")
                        except IOError as e:
                            print(f"[错误] 无法写入文件 {md_path}: {e}")

                    except ValueError:
                        print(f"[跳过] 文件名 {filename} 的时间格式不符合 'YYYYMMDDhhmmss'")
                
                else:
                    print(f"[跳过] 文件 {filename} 不符合 DJI_YYYYMMDDhhmmss_XXXX_D.mp4 的命名规则")

    print("--- 扫描完成 ---")

# --- 主程序入口 ---
if __name__ == "__main__":
    # 将此脚本放在您的视频文件夹中，或更改参数指向目标目录
    generate_video_notes()