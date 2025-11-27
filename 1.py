import os
import re
from datetime import datetime, date, timedelta

def generate_video_notes(root_dir="."):
    """
    扫描指定目录及其子目录下的所有 .mp4 文件，并生成同名的 Markdown 笔记文件。
    如果同名的 .md 文件已存在，则跳过该视频。
    
    笔记文件包含视频的拍摄时间（从文件名提取）和距离特定日期的天数。
    
    Args:
        root_dir (str): 扫描的起始目录。默认为当前目录。
    """
    
    # 目标高考日期：2025年6月7日
    target_date = date(2025, 6, 7)
    
    # 匹配视频文件名的正则表达式
    pattern = re.compile(r"DJI_(\d{14})(_.*)?\.mp4$", re.IGNORECASE)

    print(f"--- 开始扫描目录: {os.path.abspath(root_dir)} ---")

    for foldername, subfolders, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.lower().endswith(".mp4"):
                # 构造对应的 .md 文件路径
                base_name = os.path.splitext(filename)[0]
                md_filename = base_name + ".md"
                md_path = os.path.join(foldername, md_filename)
                
                # ✅ 跳过：如果 .md 文件已存在
                if os.path.exists(md_path):
                    print(f"[跳过] 已存在笔记: {md_path}")
                    continue

                match = pattern.match(filename)
                if match:
                    time_str = match.group(1)
                    try:
                        video_datetime = datetime.strptime(time_str, "%Y%m%d%H%M%S")
                        current_date = video_datetime.date()
                        delta: timedelta = target_date - current_date
                        days_difference = delta.days
                        
                        if days_difference > 0:
                            countdown_message = f"距离 2025年6月7日高考还有 {days_difference} 天"
                        elif days_difference < 0:
                            countdown_message = f"2025年6月7日高考已过去 {abs(days_difference)} 天"
                        else:
                            countdown_message = "今天是 2025年6月7日高考日！"
                        
                        formatted_time = video_datetime.strftime("%Y年%m月%d日 %H时%M分%S秒")
                        
                        markdown_content = f"""# 视频信息 - {filename}

## 拍摄时间
- **日期时间:** {formatted_time}

## 时间计算
- **特定日期:** {target_date.strftime("%Y年%m月%d日")}
- **倒计时/已过天数:** {countdown_message}

---

## 视频备注
"""
                        # 写入文件（此时确定不存在）
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
    generate_video_notes()