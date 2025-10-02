# -*- coding: utf-8 -*-
# 正規化 mp3 音量 (使用 ffmpeg)
import os
import subprocess

# 資料夾設定
input_dir = r"mp3_audio/original_audio"
output_dir = r"mp3_audio/normalized_audio"
os.makedirs(output_dir, exist_ok=True)

print("=" * 40)
print("正在正規化 MP3 音量...")
print(f"輸入資料夾: {input_dir}")
print(f"輸出資料夾: {output_dir}")
print("=" * 40)

# 批次處理所有 mp3
for file in os.listdir(input_dir):
    if file.lower().endswith(".mp3"):
        input_path = os.path.join(input_dir, file)
        output_path = os.path.join(output_dir, os.path.splitext(file)[0] + ".mp3")

        print(f"處理中: {file}")
        cmd = [
            "ffmpeg", "-y", "-i", input_path,
            "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
            output_path
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

print("=" * 40)
print("全部完成！檔案已輸出到:", output_dir)
print("=" * 40)
