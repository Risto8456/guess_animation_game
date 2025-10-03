# 聽歌猜動畫遊戲
## 使用工具
1. python
2. youtube(API)
3. google 試算表、Apps Script
4. [Hitomi-Downloader](https://github.com/KurtBestor/Hitomi-Downloader)

## 一、歌曲清單建置
###### 嫌麻煩也可以直接用 Hitomi 抓到的檔名資料，只是字串處理要設計一下
1. 將歌曲加到 youtube 播放清單
2. 創建 Youtube API 金鑰 - [教學](https://gg90052.github.io/blog/yt_api_key/)
3. 創建 google 試算表，名稱隨便
4. 在該試算表創建工作表，名稱：YT Playlist Export
5. 在擴充功能那邊打開 Apps Script，把程式碼貼上去
6. '服務' 開啟 'YouTube Data API v3'
7. 將程式碼中 `playlistId` 改成你的 youtube 播放清單 ID
  + 若連結為：`https://www.youtube.com/playlist?list=PL13RIfcroB45ZrTZryP44qPEbFLyle11E`
  + ID 就是 `list=` 之後的：`PL13RIfcroB45ZrTZryP44qPEbFLyle11E`
8. 第一次執行需要審核
9. 
