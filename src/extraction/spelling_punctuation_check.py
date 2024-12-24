
import os
import json
import language_tool_python

def check_spelling_and_punctuation(input_dir, output_dir, lang="en-US"):
    """
    Проверяет текст на орфографические и пунктуационные ошибки с использованием LanguageTool.
    :param input_dir: Путь к папке с JSON-файлами OCR.
    :param output_dir: Путь для сохранения исправленного текста.
    :param lang: Язык для проверки (по умолчанию 'en-US').
    """
    os.makedirs(output_dir, exist_ok=True)
    tool = language_tool_python.LanguageTool(lang)

    for file_name in os.listdir(input_dir):
        if file_name.endswith(".json"):
            file_path = os.path.join(input_dir, file_name)
            with open(file_path, "r", encoding="utf-8") as f:
                ocr_data = json.load(f)
                text = " ".join(ocr_data.get("text", []))


            matches = tool.check(text)
            corrected_text = language_tool_python.utils.correct(text, matches)


            output_file_path = os.path.join(output_dir, file_name.replace(".json", "_corrected.txt"))
            with open(output_file_path, "w", encoding="utf-8") as out_file:
                out_file.write(corrected_text)

            print(f"Исправленный текст сохранен: {output_file_path}")
            print(f"Найдено ошибок: {len(matches)}")


if __name__ == "__main__":
    input_folder = "output/ocr_results"
    output_folder = "output/corrected_text"

    check_spelling_and_punctuation(input_folder, output_folder, lang="en-US")
