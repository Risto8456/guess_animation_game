# -*- coding: utf-8 -*-
# 第三步 : 產生多階段馬賽克圖片
import os
import cv2

input_dir = r"picture/resized_pictures"     # 原始圖片資料夾
output_dir = r"picture/pixelated_picture"   # 輸出馬賽克圖片資料夾
os.makedirs(output_dir, exist_ok=True)

# 馬賽克每個階段的方塊大小 (pixel block)
pixel_map = {
    1: None,   # 原版，不動
    2: 64,
    3: 48,
    4: 32,
    5: 24,
    6: 16
}

files = sorted(os.listdir(input_dir))
for idx, fname in enumerate(files, start=1):
    path = os.path.join(input_dir, fname)
    img = cv2.imread(path)
    if img is None:
        print(f"讀取失敗: {path}")
        continue

    H, W = img.shape[:2]
    basename, ext = os.path.splitext(fname)  # 取得檔名不含副檔名
    
    for stage in range(1, 7):
        out_name = f"{basename}_{stage}.jpg"
        out_path = os.path.join(output_dir, out_name)

        if stage == 1:
            # 原版
            cv2.imwrite(out_path, img)
        else:
            block_size = pixel_map[stage]

            # 計算縮小尺寸，使「最大邊 = block_size」
            scale = block_size / max(W, H)
            down_w = max(1, int(W * scale))
            down_h = max(1, int(H * scale))

            # 先縮小再放大
            small = cv2.resize(img, (down_w, down_h), interpolation=cv2.INTER_AREA)
            pixelated = cv2.resize(small, (W, H), interpolation=cv2.INTER_NEAREST)
            cv2.imwrite(out_path, pixelated)

    print(f"已生成 6 個階段: {fname}")

print("全部圖片馬賽克處理完成")
