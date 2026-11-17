import os
import time
from deep_translator import GoogleTranslator

BATCH_SIZE = 10  # 每次打包 10 句一起翻譯，大幅降低請求次數

def translate_with_retry(translator, texts, max_retries=3):
    """帶有自動重試與退避等待的批次翻譯函式"""
    for attempt in range(max_retries):
        try:
            return translator.translate_batch(texts)
        except Exception as e:
            wait_time = (attempt + 1) * 5
            print(f"翻譯遇到頻率限制，等待 {wait_time} 秒後進行第 {attempt + 1} 次重試... ({e})")
            time.sleep(wait_time)
    
    print("警告：多次重試仍失敗，該批次將保留原文。")
    return texts

def main():
    if not os.path.exists("original.srt"):
        print("錯誤：找不到 original.srt，請先執行 step2_transcribe.py")
        return

    print("正在使用批次模式將字幕翻譯為繁體中文...")
    translator = GoogleTranslator(source='auto', target='zh-TW')

    with open("original.srt", "r", encoding="utf-8") as f:
        blocks = f.read().strip().split("\n\n")

    parsed_items = []
    for block in blocks:
        lines = block.split("\n")
        if len(lines) >= 3:
            index_num = lines[0]
            time_code = lines[1]
            original_text = " ".join(lines[2:])
            parsed_items.append((index_num, time_code, original_text))

    total_items = len(parsed_items)
    translated_blocks = []

    # 依照 BATCH_SIZE 分批送出翻譯
    for start_idx in range(0, total_items, BATCH_SIZE):
        batch = parsed_items[start_idx : start_idx + BATCH_SIZE]
        texts_to_translate = [item[2] for item in batch]

        zh_texts = translate_with_retry(translator, texts_to_translate)

        for (index_num, time_code, original_text), zh_text in zip(batch, zh_texts):
            # 確保翻譯結果不為 None
            final_zh = zh_text if zh_text else original_text
            
            # 若想改為「中英雙語字幕」，請將下一行改為：
            # translated_blocks.append(f"{index_num}\n{time_code}\n{final_zh}\n{original_text}")
            translated_blocks.append(f"{index_num}\n{time_code}\n{final_zh}")

        current_done = min(start_idx + BATCH_SIZE, total_items)
        print(f"翻譯進度：{current_done}/{total_items}")
        
        # 每批之間休息 2 秒，確保穩定不被封鎖
        if current_done < total_items:
            time.sleep(2)

    with open("chinese.srt", "w", encoding="utf-8") as f:
        f.write("\n\n".join(translated_blocks) + "\n")

    print("\n✅ 步驟 3 完成！已儲存繁體中文字幕檔：chinese.srt")

if __name__ == "__main__":
    main()
