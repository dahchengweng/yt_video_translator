# YouTube Video Auto Translator (YT 影片全自動本機中文字幕生成器)

這是一個完全在本機端（Local）運行的 YouTube 影片下載、語音辨識、離線翻譯與繁體中文字幕燒錄自動化工具。透過結合 **yt-dlp**、**Faster-Whisper**、**Helsinki-NLP Opus-MT** 與 **OpenCC**，無需依賴付費翻譯 API，即可將外語影片轉換為道地的台灣繁體中文字幕影片。

## ✨ 核心特色

* **分段模組化設計：** 將「下載分離」、「語音辨識」、「字幕翻譯」、「影音合併」拆分為 4 支獨立腳本，方便單獨除錯與手動微調字幕。
* **高速離線語音辨識：** 採用 `faster-whisper` 並支援讀取本機模型權重，支援 NVIDIA GPU (CUDA) 加速。
* **零 API 限制離線翻譯：** 採用開源神經翻譯模型 `Opus-MT` 搭配 `OpenCC (s2twp)`，自動將簡體譯文在地化為台灣正體中文與慣用詞彙，無請求頻率上限。
* **硬字幕自動燒錄：** 透過 `FFmpeg` 呼叫系統內建微軟正黑體，將字幕直接壓製進高畫質 MP4 影片中。

---

## 🛠️ 環境需求與安裝

### 1. 系統前置需求
* **Python 3.10 ~ 3.12**（建議使用虛擬環境 `.venv`）
* **FFmpeg：** 需安裝並加入系統環境變數 `PATH`（Windows 可透過 `winget install Gyan.FFmpeg` 安裝）。
* **NVIDIA GPU（選用）：** 具備 CUDA 環境可大幅提升語音辨識與翻譯速度。

### 2. 安裝 Python 套件
```bash
# 建立並啟動虛擬環境
python -m venv .venv
.\.venv\Scripts\activate

# 安裝相依套件
pip install -r requirements.txt
pip install faster-whisper transformers sentencepiece sacremoses opencc-python-reimplemented
```

---

## 🚀 使用步驟

依照順序在終端機執行以下 4 支程式：

### Step 1：下載 YouTube 影片並分離影音
```bash
python step1_download_split.py
```
* 依提示貼上 YouTube 網址，程式會自動下載最佳畫質並分離出 `video_only.mp4`（純影像）與 `audio_only.wav`（16kHz 單聲道音訊）。

### Step 2：本機語音辨識（產出原文字幕）
```bash
python step2_transcribe.py
```
* 讀取 `audio_only.wav` 並載入本機 `faster-whisper` 模型，生成帶有時間軸的 `original.srt`。
* *注意：執行前請確認腳本內的 `LOCAL_MODEL_DIR` 指向正確的本機模型資料夾路徑。*

### Step 3：離線翻譯與台灣繁體轉換
```bash
python step3_translate.py
```
* 讀取 `original.srt`，透過 `Opus-MT` 翻譯並經由 `OpenCC (s2twp)` 轉換為道地台灣繁體中文，輸出 `chinese.srt`。
* *小技巧：在此步驟完成後，可使用文字編輯器打開 `chinese.srt` 手動微調專有名詞翻譯。*

### Step 4：合併影像、音訊與中文字幕
```bash
python step4_merge_video.py
```
* 使用 FFmpeg 與微軟正黑體將 `chinese.srt` 燒錄進畫面，並重新合併原始音軌，輸出最終成品 `final_chinese_video.mp4`。

---

## 📂 專案結構

```text
yt_translator/
├── step1_download_split.py   # 步驟1：下載影片與分離影音流
├── step2_transcribe.py       # 步驟2：Faster-Whisper 語音辨識
├── step3_translate.py        # 步驟3：Opus-MT 離線翻譯 + OpenCC 繁中轉換
├── step4_merge_video.py      # 步驟4：FFmpeg 燒錄硬字幕與影音合併
├── requirements.txt          # Python 套件清單
├── .gitignore                # Git 忽略清單（排除影片、音訊與虛擬環境）
├── README.md                 # 專案說明文件
└── LICENSE                   # 開源授權條款
```

## 📄 授權條款

本專案採用 [MIT License](LICENSE) 授權。
