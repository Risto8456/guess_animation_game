# -*- coding: utf-8 -*-
# 第一步 : 將各種格式圖片轉換為 jpg 格式
import os
import cv2

# 取得該檔案所在資料夾
dir_path = os.path.dirname(__file__)

input_dir = dir_path + r"/original_picture" # 原始圖片資料夾
output_dir = dir_path + r"/jpg_picture"     # 輸出的 jpg 資料夾

# 建立輸出資料夾
os.makedirs(output_dir, exist_ok=True)

# 支援的副檔名
exts = [".png", ".bmp", ".tif", ".tiff", ".jpeg", ".jpg", ".webp"]

for fname in sorted(os.listdir(input_dir)):
    fpath = os.path.join(input_dir, fname)
    name, ext = os.path.splitext(fname)
    if ext.lower() in exts:
        img = cv2.imread(fpath)
        if img is None:
            print(f"讀取失敗: {fpath}")
            continue
        out_path = os.path.join(output_dir, f"{name}.jpg")
        cv2.imwrite(out_path, img, [int(cv2.IMWRITE_JPEG_QUALITY), 95])
        print(f"轉換完成: {name}.jpg")

print("全部圖片已轉換完成")