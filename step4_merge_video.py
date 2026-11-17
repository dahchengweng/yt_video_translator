import os
import subprocess

OUTPUT_VIDEO = "final_chinese_video.mp4"

def main():
    required_files = ["video_only.mp4", "audio_only.wav", "chinese.srt"]
    for f in required_files:
        if not os.path.exists(f):
            print(f"錯誤：找不到 {f}，請確認前三個步驟皆已順利完成。")
            return

    print("正在將純影像、音訊與繁體中文字幕合併燒錄，請稍候...")

    # 使用 Windows 內建「微軟正黑體」，白字黑邊，底部留白 25
    subtitle_style = (
        "FontName=Microsoft JhengHei,"
        "FontSize=22,"
        "PrimaryColour=&H00FFFFFF,"
        "OutlineColour=&H00000000,"
        "BorderStyle=1,"
        "Outline=2,"
        "MarginV=25"
    )

    cmd = [
        "ffmpeg", "-y",
        "-i", "video_only.mp4",
        "-i", "audio_only.wav",
        "-vf", f"subtitles=chinese.srt:force_style='{subtitle_style}'",
        "-c:v", "libx264",
        "-crf", "23",
        "-preset", "fast",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        OUTPUT_VIDEO
    ]

    subprocess.run(cmd, check=True)
    print(f"\n✅ 全部完成！最終中文影片已生成：{OUTPUT_VIDEO}")

if __name__ == "__main__":
    main()
