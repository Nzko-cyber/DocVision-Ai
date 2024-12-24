<<<<<<< HEAD
import os
from docx import Document
from PIL import Image, ImageDraw, ImageFont

def extract_text_from_docx_file(docx_path):
    """
    Извлекает текст из одного DOCX-файла.
    :param docx_path: Путь к DOCX-файлу.
    :return: Извлеченный текст в виде строки.
    """
    document = Document(docx_path)
    return "\n".join([para.text for para in document.paragraphs])


def save_text_to_file(text, output_path):
    """
    Сохраняет текст в текстовый файл.
    :param text: Текст для сохранения.
    :param output_path: Путь к выходному файлу.
    """
    with open(output_path, "w", encoding="utf-8") as txt_file:
        txt_file.write(text)
    print(f"Текст сохранен: {output_path}")


def convert_text_to_image(text, output_image_path, image_size=(1000, 800)):
    """
    Конвертирует текст в изображение для дальнейшего OCR (опционально).
    :param text: Текст для конвертации.
    :param output_image_path: Путь для сохранения изображения.
    :param image_size: Размер изображения.
    """
    img = Image.new("RGB", image_size, color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()

    # Разбиение текста на строки
    lines = text.split("\n")
    y = 10
    for line in lines:
        draw.text((10, y), line, fill=(0, 0, 0), font=font)
        y += 20  # Смещение вниз для следующей строки

    img.save(output_image_path)
    print(f"Изображение с текстом сохранено: {output_image_path}")


def process_docx(input_dir, text_output_dir, image_output_dir=None):
    """
    Основная функция: обрабатывает DOCX-файлы, извлекает текст и сохраняет как TXT или изображения.
    :param input_dir: Путь к папке с DOCX-файлами.
    :param text_output_dir: Путь для сохранения текстовых файлов.
    :param image_output_dir: Путь для сохранения изображений (опционально).
    """
    os.makedirs(text_output_dir, exist_ok=True)
    if image_output_dir:
        os.makedirs(image_output_dir, exist_ok=True)

    for file_name in os.listdir(input_dir):
        if file_name.endswith(".docx"):
            docx_path = os.path.join(input_dir, file_name)
            print(f"Обработка: {docx_path}")

            # Извлечение текста с использованием вспомогательной функции
            text_content = extract_text_from_docx_file(docx_path)

            # Сохранение текста в файл
            text_output_path = os.path.join(text_output_dir, file_name.replace(".docx", ".txt"))
            save_text_to_file(text_content, text_output_path)

            # Дополнительно: сохранение текста как изображения
            if image_output_dir:
                image_output_path = os.path.join(image_output_dir, file_name.replace(".docx", ".jpg"))
                convert_text_to_image(text_content, image_output_path)


if __name__ == "__main__":
    input_folder = "data/docx_files"           # Папка с DOCX-файлами
    text_output_folder = "data/processed_docx/txt"  # Папка для текстовых файлов
    image_output_folder = "data/processed_docx/img" # Папка для изображений (опционально)

    process_docx(input_folder, text_output_folder, image_output_folder)
=======
import os
from docx import Document
from PIL import Image, ImageDraw, ImageFont

def extract_text_from_docx_file(docx_path):
    """
    Извлекает текст из одного DOCX-файла.
    :param docx_path: Путь к DOCX-файлу.
    :return: Извлеченный текст в виде строки.
    """
    document = Document(docx_path)
    return "\n".join([para.text for para in document.paragraphs])


def save_text_to_file(text, output_path):
    """
    Сохраняет текст в текстовый файл.
    :param text: Текст для сохранения.
    :param output_path: Путь к выходному файлу.
    """
    with open(output_path, "w", encoding="utf-8") as txt_file:
        txt_file.write(text)
    print(f"Текст сохранен: {output_path}")


def convert_text_to_image(text, output_image_path, image_size=(1000, 800)):
    """
    Конвертирует текст в изображение для дальнейшего OCR (опционально).
    :param text: Текст для конвертации.
    :param output_image_path: Путь для сохранения изображения.
    :param image_size: Размер изображения.
    """
    img = Image.new("RGB", image_size, color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()

    # Разбиение текста на строки
    lines = text.split("\n")
    y = 10
    for line in lines:
        draw.text((10, y), line, fill=(0, 0, 0), font=font)
        y += 20  # Смещение вниз для следующей строки

    img.save(output_image_path)
    print(f"Изображение с текстом сохранено: {output_image_path}")


def process_docx(input_dir, text_output_dir, image_output_dir=None):
    """
    Основная функция: обрабатывает DOCX-файлы, извлекает текст и сохраняет как TXT или изображения.
    :param input_dir: Путь к папке с DOCX-файлами.
    :param text_output_dir: Путь для сохранения текстовых файлов.
    :param image_output_dir: Путь для сохранения изображений (опционально).
    """
    os.makedirs(text_output_dir, exist_ok=True)
    if image_output_dir:
        os.makedirs(image_output_dir, exist_ok=True)

    for file_name in os.listdir(input_dir):
        if file_name.endswith(".docx"):
            docx_path = os.path.join(input_dir, file_name)
            print(f"Обработка: {docx_path}")

            # Извлечение текста с использованием вспомогательной функции
            text_content = extract_text_from_docx_file(docx_path)

            # Сохранение текста в файл
            text_output_path = os.path.join(text_output_dir, file_name.replace(".docx", ".txt"))
            save_text_to_file(text_content, text_output_path)

            # Дополнительно: сохранение текста как изображения
            if image_output_dir:
                image_output_path = os.path.join(image_output_dir, file_name.replace(".docx", ".jpg"))
                convert_text_to_image(text_content, image_output_path)


if __name__ == "__main__":
    input_folder = "data/docx_files"           # Папка с DOCX-файлами
    text_output_folder = "data/processed_docx/txt"  # Папка для текстовых файлов
    image_output_folder = "data/processed_docx/img" # Папка для изображений (опционально)

    process_docx(input_folder, text_output_folder, image_output_folder)
>>>>>>> 75bc998f7ed79a04da2b9a8d7988df558d3f8125
