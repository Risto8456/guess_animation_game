# 聽歌猜動畫遊戲
## 使用工具
1. python
    + 注意 moviepy 不要用最新版，目前有 bug
    + `pip install moviepy==1.0.3`
2. youtube(API)
3. google 試算表、Apps Script
4. [Hitomi-Downloader](https://github.com/KurtBestor/Hitomi-Downloader)

## 一、歌曲清單建置
###### 嫌麻煩也可以直接用 Hitomi 抓到的檔名資料，只是字串處理要設計一下
1. 將歌曲加到 youtube 播放清單
2. 創建 Youtube API 金鑰 - [教學](https://gg90052.github.io/blog/yt_api_key/)
3. 創建 google 試算表，名稱隨便
4. 在該試算表創建工作表，名稱：YT Playlist Export
5. 在擴充功能那邊打開 Apps Script，把程式碼(在 Apps_Script_code.txt 裡)貼上去
6. '服務' 開啟 'YouTube Data API v3'
7. 將程式碼中 `playlistId` 改成你的 youtube 播放清單 ID
    + 若連結網址為：`https://www.youtube.com/playlist?list=PL13RIfcroB45ZrTZryP44qPEbFLyle11E`
    + ID 就是 `list=` 之後的：`PL13RIfcroB45ZrTZryP44qPEbFLyle11E`
8. 第一次執行需要審核
9. 程式會自動新增 `# | Title | VideoID | URL` 欄位，其他須自己輸入
    + `Animation | SeasonOPED | Song | CHtranslation | Point | Time`
    + `動畫 | 出處 | 歌曲名 | 歌曲中文譯名 | 分數 | 開始時間`
    + `Time` 欄位建議格式轉為 `MM:SS`
    + 其他格式 -> 自訂數字格式 -> 輸入 `00:00`
10. 好了就載 .csv 檔下來

## 二、圖片處裡
1. 自己找圖片放到  `picture\original_picture` 裡面(須注意有一些圖片格式不支援)，檔名取相對應的歌曲 ID (# 欄位)
2. 依序執行 3 步
  1. `picture\convert_to_jpg.py`：將各種格式圖片轉換為 jpg 格式
  2. `picture\resize_picture.py`：縮放圖片至指定大小，並保持比例
  3. `picture\pixelate_picture.py`：產生多階段馬賽克圖片

## 三、音檔處理
1. 安裝好 Hitomi-Downloader，盡量放在空間足夠的磁碟，如：D 槽
2. 直接丟 youtube 播放清單的連結網址，它就會將全部歌曲下載 .mp4
3. 下載好後執行 `mp3_audio\take_audio.py`：從影片.mp4 取 30 秒音檔.mp3
    + 用 `VideoID` 對齊
    + 從 `Time` 開始算 30 秒
4. 取完音檔執行 `mp3_audio\normalize.py`：正規化 mp3 音量，避免不同首歌聲音忽大忽小

## 遊戲程式
1. 按第一下空白鍵：顯示原圖以及答案(動畫 | 出處 | 歌曲名 | 歌曲中文譯名)
2. 按第二下空白鍵：換下一首歌
