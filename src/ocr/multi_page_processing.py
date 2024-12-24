
import os
from pdf2image import convert_from_path
from docx import Document
import easyocr
import json


reader = easyocr.Reader(['en', 'ru'])


def process_pdf(pdf_path, output_dir, dpi=300):
    """
    Обрабатывает многостраничный PDF: конвертирует страницы в изображения и выполняет OCR.
    :param pdf_path: Путь к PDF-файлу.
    :param output_dir: Путь для сохранения результатов.
    :param dpi: Разрешение изображения.
    """
    os.makedirs(output_dir, exist_ok=True)
    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]


    pages = convert_from_path(pdf_path, dpi=dpi)
    for idx, page in enumerate(pages):
        image_path = os.path.join(output_dir, f"{pdf_name}_page_{idx + 1}.jpg")
        page.save(image_path, "JPEG")
        print(f"Страница сохранена: {image_path}")


        ocr_result = reader.readtext(image_path, detail=0)
        result_path = os.path.join(output_dir, f"{pdf_name}_page_{idx + 1}.json")

        with open(result_path, "w", encoding="utf-8") as f:
            json.dump({"page": idx + 1, "text": ocr_result}, f, ensure_ascii=False, indent=4)  # type: ignore

        print(f"OCR результат сохранен: {result_path}")


def process_docx(docx_path, output_dir):
    """
    Обрабатывает многостраничный DOCX: извлекает текст и сохраняет результаты.
    :param docx_path: Путь к DOCX-файлу.
    :param output_dir: Путь для сохранения результатов.
    """
    os.makedirs(output_dir, exist_ok=True)
    docx_name = os.path.splitext(os.path.basename(docx_path))[0]

    # Извлечение текста из DOCX
    document = Document(docx_path)
    for idx, paragraph in enumerate(document.paragraphs):
        if paragraph.text.strip():  # Пропускаем пустые абзацы
            text_path = os.path.join(output_dir, f"{docx_name}_paragraph_{idx+1}.txt")
            with open(text_path, "w", encoding="utf-8") as f:
                f.write(paragraph.text)
            print(f"Абзац сохранен: {text_path}")


def process_multi_page_documents(input_dir, output_dir, file_type="pdf"):
    """
    Основная функция для обработки многостраничных PDF или DOCX.
    :param input_dir: Папка с документами.
    :param output_dir: Папка для сохранения результатов.
    :param file_type: Тип файла для обработки ("pdf" или "docx").
    """
    os.makedirs(output_dir, exist_ok=True)

    for file_name in os.listdir(input_dir):
        if file_name.endswith(f".{file_type}"):
            file_path = os.path.join(input_dir, file_name)
            print(f"Обработка: {file_path}")
            file_output_dir = os.path.join(output_dir, os.path.splitext(file_name)[0])

            if file_type == "pdf":
                process_pdf(file_path, file_output_dir)
            elif file_type == "docx":
                process_docx(file_path, file_output_dir)
            else:
                print(f"Неподдерживаемый формат: {file_type}")


if __name__ == "__main__":
    input_folder = "data/multi_page_documents"
    output_folder = "output/multi_page_results"


    print("Обработка PDF-документов...")
    process_multi_page_documents(input_folder, output_folder, file_type="pdf")


    print("Обработка DOCX-документов...")
    process_multi_page_documents(input_folder, output_folder, file_type="docx")
