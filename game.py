import pygame
import os
import cv2
import csv
import random

# 取得該檔案所在資料夾
dir_path = os.path.dirname(__file__)

# 設定資料夾
image_dir = dir_path + r"/picture/pixelated_picture"
audio_dir = dir_path + r"/mp3_audio/normalized_audio"
csv_path = dir_path + r"/youtube - YT Playlist Export.csv"

# 1 ~ 103
ids = list(range(1, 104))
random.shuffle(ids)  # 隨機播放順序
stages = [6,5,4,3,2,1]
stage_interval = 5
song_length = 30
WINDOW_W, WINDOW_H = 1280, 720

pygame.init()
screen = pygame.display.set_mode((WINDOW_W, WINDOW_H))
pygame.display.set_caption("聽歌猜動畫遊戲")

# 讀取 CSV
csv_data = {}
with open(csv_path, newline='', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
        csv_data[int(row['#'])] = {
            'Animation': row['Animation'],
            'SeasonOPED': row['SeasonOPED'],
            'Song': row['Song'],
            'CHtranslation': row['CHtranslation'],
            'Point': row['Point']
        }

# 字體 (使用支援中日文字體，如 msyh.ttc)
font_path = dir_path + r"/msyh.ttc"
font1_size = 60
font2_size = 40
font1 = pygame.font.Font(font_path, font1_size)
font2 = pygame.font.Font(font_path, font2_size)
font_color = (255, 255, 255)
bg_color = (0, 0, 0)

# 文字換行函式
def wrap_text(text, font, max_width):
    """將文字依據 max_width 分行"""
    words = list(text)  # 一個字一個字（適合中日文字）
    lines = []
    current_line = ""

    for ch in words:
        test_line = current_line + ch
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = ch
    if current_line:
        lines.append(current_line)
    return lines

# 主迴圈
for song_index, song_id in enumerate(ids):
    # 載入圖片
    frame_files = [os.path.join(image_dir, f"{song_id}_{stage}.jpg") for stage in stages]
    frames = []
    for f in frame_files:
        img = cv2.imread(f)
        if img is None:
            raise ValueError(f"讀取失敗: {f}")
        H, W = img.shape[:2]
        surf = pygame.image.frombuffer(img.tobytes(), (W, H), "BGR")
        frames.append(surf)

    # 播放音訊
    pygame.mixer.init()
    audio_path = os.path.join(audio_dir, f"{song_id}.mp3")
    pygame.mixer.music.load(audio_path)
    pygame.mixer.music.play()

    running = True
    start_time = pygame.time.get_ticks()
    manual_override = False  # 第一次空白鍵切最清晰
    skip_to_next_song = False  # 第二次空白鍵跳下一首歌
    song_finished = False  # 音檔是否播完

    # 初始文字：只顯示 Point, id
    info = csv_data.get(song_id, {})
    text_lines_default = [
        f"分數: +{info.get('Point','')}",
        f"ID: {song_id}"
    ]
    text_lines_full = [
        f"動畫名稱: {info.get('Animation','')}",
        f"出自 Season/OP/ED/IN: {info.get('SeasonOPED','')}",
        f"歌曲名稱: {info.get('Song','')}"
    ]
    ch_translation = info.get('CHtranslation','').strip()
    if ch_translation:
        text_lines_full.append(f"歌曲台灣譯名: {ch_translation}")

    while running:
        t_ms = pygame.time.get_ticks() - start_time
        t_sec = t_ms / 1000.0

        if skip_to_next_song:
            break

        if t_sec >= song_length:
            song_finished = True  # 音檔播完
            stage_idx = len(frames) - 1  # 保持最後一幀
        else:
            # 計算階段
            if manual_override:
                stage_idx = len(frames) - 1  # 最清晰
                text_lines = text_lines_full
            else:
                stage_idx = int(t_sec // stage_interval)
                if stage_idx >= len(frames):
                    stage_idx = len(frames) - 1
                text_lines = text_lines_default

        # 背景
        screen.fill((0,0,0))

        # 置中圖片
        img_surf = frames[stage_idx]
        img_W, img_H = img_surf.get_size()
        x = (WINDOW_W - img_W) // 2
        y = (WINDOW_H - img_H) // 2
        screen.blit(img_surf, (x, y))

        # 顯示文字浮水印
        padding = 5
        # 左上角文字 (text_lines_default)
        for i, line in enumerate(text_lines_default):
            text_surf = font1.render(line, True, font_color, bg_color)
            line_height = font1.get_linesize()  # 正確行高
            screen.blit(text_surf, (10, 10 + i*(line_height + padding)))
        if manual_override:
            # 左下角文字 (text_lines_full)
            line_height = font2.get_linesize()  # 正確行高
            wrapped_lines = []
            for line in text_lines_full:
                wrapped_lines.extend(wrap_text(line, font2, WINDOW_W - 20))

            total_height = line_height * len(text_lines_full) + padding * (len(text_lines_full)-1)
            y_offset = WINDOW_H - total_height - 60
            for wline in wrapped_lines:
                text_surf = font2.render(wline, True, font_color, bg_color)
                screen.blit(text_surf, (10, y_offset))
                y_offset += line_height + padding

            
        pygame.display.flip()

        # 事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.mixer.music.stop()
                    pygame.quit()
                    exit()
                elif event.key == pygame.K_SPACE:
                    if not manual_override:
                        manual_override = True  # 第一次切最清晰 + 顯示完整文字
                    else:
                        skip_to_next_song = True  # 第二次空白鍵 -> 下一首歌

    pygame.mixer.music.stop()

pygame.quit()