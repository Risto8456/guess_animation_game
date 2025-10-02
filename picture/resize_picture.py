# -*- coding: utf-8 -*-
# 第二步 : 縮放圖片至指定大小，並保持比例
from PIL import Image
import os

# 圖片資料夾
folder = r"picture/jpg_picture"
# 輸出資料夾
output_folder = r"picture/resized_pictures"
os.makedirs(output_folder, exist_ok=True)

# 最大尺寸
max_width = 1280
max_height = 720

# 處理每張圖片
for filename in os.listdir(folder):
    if filename.lower().endswith(".jpg"):
        path = os.path.join(folder, filename)
        img = Image.open(path)

        # 計算等比例縮放尺寸
        w_ratio = max_width / img.width
        h_ratio = max_height / img.height
        ratio = min(w_ratio, h_ratio)  # 可放大圖片
        # ratio = min(w_ratio, h_ratio, 1.0)  # 不放大圖片

        new_width = int(img.width * ratio)
        new_height = int(img.height * ratio)

        # 縮放
        img_resized = img.resize((new_width, new_height), Image.LANCZOS)

        # 儲存
        save_path = os.path.join(output_folder, filename)
        img_resized.save(save_path)

        print(f"{filename} → {new_width}x{new_height}")

print("所有圖片已處理完成！")
