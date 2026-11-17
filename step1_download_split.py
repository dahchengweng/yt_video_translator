import os
import subprocess

def main():
    youtube_url = input("請貼上 YouTube 影片網址: ").strip()
    if not youtube_url:
        print("錯誤：未輸入網址。")
        return

    # 清理舊檔案避免混淆
    for f in ["source_video.mp4", "video_only.mp4", "audio_only.wav"]:
        if os.path.exists(f):
            os.remove(f)

    print("\n1. 正在下載 YouTube 影片...")
    subprocess.run([
        "yt-dlp",
        "-f", "bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]/b",
        "--merge-output-format", "mp4",
        "-o", "source_video.mp4",
        youtube_url
    ], check=True)

    print("\n2. 正在分離「純影像」與「純音訊」...")
    # 分離純影像（直接複製影像流，速度極快）
    subprocess.run([
        "ffmpeg", "-y", "-i", "source_video.mp4",
        "-an", "-c:v", "copy", "video_only.mp4"
    ], check=True)

    # 分離純音訊（轉為 16kHz 單聲道 WAV，供 Whisper 辨識使用）
    subprocess.run([
        "ffmpeg", "-y", "-i", "source_video.mp4",
        "-vn", "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1", "audio_only.wav"
    ], check=True)

    print("\n✅ 步驟 1 完成！已產生 video_only.mp4 與 audio_only.wav")

if __name__ == "__main__":
    main()
