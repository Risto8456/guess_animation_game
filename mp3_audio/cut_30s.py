# -*- coding: utf-8 -*-
# 使用 moviepy 套件來處理影片剪輯 (取音檔)

# pip install moviepy==1.0.3
from moviepy.editor import VideoFileClip
import pandas as pd
import os

# 環境路徑
# C:\Users\User\youtube_video_env\Scripts\python.exe
# 環境啟動指令
# C:\Users\User\youtube_video_env\Scripts\Activate.ps1

# 讀取 CSV 檔案
csv_file_path = r"youtube - YT Playlist Export.csv"
df = pd.read_csv(csv_file_path)

# 影片檔案夾路徑，放在專案外
video_folder = r"D:\hitomi_downloader_GUI\hitomi_downloaded_youtube\[Playlist] 系員大會_題庫"
# 儲存剪輯音檔的資料夾
cut_folder = r"mp3_audio/original_audio"
os.makedirs(cut_folder, exist_ok=True)

# 讀取 CSV 中的 VideoID 和 Time 欄位
for _, row in df.iterrows():
    id = row['#']
    video_id = row['VideoID']
    time_str = row['Time']

    # 如果 id 小於 1，跳過這一行(從 1 開始)
    if id < 1:
        continue

    # 輸出 mp3 檔案名稱
    output_filename = f"{id}.mp3"
    output_path = os.path.join(cut_folder, output_filename)
    # 如果檔案已存在則跳過
    if os.path.exists(output_path):
        print(f"{output_filename} 已存在，跳過轉換。")
        continue

    # 如果 Time 欄位是空的，從頭(00:00)開始
    if pd.isna(time_str):
        start_time = 0
    else:
        # 解析時間格式（假設時間格式為 "MM:SS"）
        minutes, seconds = map(int, time_str.split(':'))
        start_time = minutes * 60 + seconds
    end_time = start_time + 30  # 取 30 秒片段

    # 根據 VideoID 在資料夾中尋找對應的影片檔案
    video_filename = None
    for filename in os.listdir(video_folder):
        if filename.endswith(f"({video_id}).mp4"):  # 檢查檔名是否以 VideoID 結尾
            video_filename = filename
            break
    
    if not video_filename:
        print(f"未找到檔案對應於 VideoID: {video_id}")
        continue
    
    video_path = os.path.join(video_folder, video_filename)

    # 讀取影片並擷取音訊
    try:
        video = VideoFileClip(video_path)
        audio_clip = video.audio.subclip(start_time, end_time)
        # 儲存音訊片段到 cut_folder
        audio_clip.write_audiofile(output_path)
        print(f"已保存音檔：{output_filename}")
    except Exception as e:
        print(f"處理 {video_filename} 時出錯：{e}")
