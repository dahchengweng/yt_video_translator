import os
import argostranslate.package
import argostranslate.translate
from opencc import OpenCC

def setup_offline_model():
    """檢查並自動下載離線英翻中語言包（僅初次執行需下載約 100MB）"""
    from_code = "en"
    to_code = "zt"  # zt 代表繁體中文 (Traditional Chinese)

    installed_languages = argostranslate.translate.get_installed_languages()
    from_lang = next((lang for lang in installed_languages if lang.code == from_code), None)
    to_lang = next((lang for lang in installed_languages if lang.code == to_code), None)

    if from_lang and to_lang and from_lang.get_translation(to_lang):
        return

    print("初次執行，正在下載離線英翻中語言包（約 100MB）...")
    argostranslate.package.update_package_index()
    available_packages = argostranslate.package.get_available_packages()
    package_to_install = next(
        filter(lambda x: x.from_code == from_code and x.to_code == to_code, available_packages)
    )
    argostranslate.package.install_from_path(package_to_install.download())
    print("離線語言包安裝完成！")

def main():
    if not os.path.exists("original.srt"):
        print("錯誤：找不到 original.srt，請先執行 step2_transcribe.py")
        return

    cc = OpenCC('s2twp')
    setup_offline_model()
    print("正在使用本機離線模型翻譯為繁體中文...")

    with open("original.srt", "r", encoding="utf-8") as f:
        blocks = f.read().strip().split("\n\n")

    translated_blocks = []
    total_blocks = len(blocks)

    for idx, block in enumerate(blocks, start=1):
        lines = block.split("\n")
        if len(lines) >= 3:
            index_num = lines[0]
            time_code = lines[1]
            original_text = " ".join(lines[2:])

            zh_text = argostranslate.translate.translate(original_text, "en", "zt")
            tw_zh = cc.convert(zh_text)
            translated_blocks.append(f"{index_num}\n{time_code}\n{tw_zh}")
            print(f"[{idx}/{total_blocks}] {tw_zh}")

    with open("chinese.srt", "w", encoding="utf-8") as f:
        f.write("\n\n".join(translated_blocks) + "\n")

    print("\n✅ 步驟 3 完成！已使用離線模型生成繁體中文字幕：chinese.srt")

if __name__ == "__main__":
    main()
