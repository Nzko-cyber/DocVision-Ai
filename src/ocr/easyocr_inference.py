
import easyocr
import os
import json
import logging
from concurrent.futures import ThreadPoolExecutor

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("ocr_processing.log", mode='w', encoding='utf-8')
    ]
)

# Файл для отслеживания обработанных изображений
PROGRESS_FILE = "ocr_progress.json"

def load_progress(progress_file):
    """Загрузка состояния обработки."""
    if os.path.exists(progress_file):
        with open(progress_file, 'r', encoding='utf-8') as f:
            return set(json.load(f))
    return set()

def save_progress(progress_file, processed_files):

    with open(progress_file, 'w', encoding='utf-8') as f:
        json.dump(list(processed_files), f, ensure_ascii=False, indent=4)

def process_image(reader, image_path, output_dir, processed_files, contrast_ths=0.7, adjust_contrast=0.5):
    file_name = os.path.basename(image_path)
    try:

        if file_name in processed_files:
            logging.info(f"Файл уже обработан: {file_name}")
            return

        logging.info(f"Начало обработки файла: {file_name}")
        results = reader.readtext(image_path, detail=0, contrast_ths=contrast_ths, adjust_contrast=adjust_contrast)

        output_path = os.path.join(output_dir, f"{os.path.splitext(file_name)[0]}.json")
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump({"file": file_name, "text": results}, f, ensure_ascii=False, indent=4)


        processed_files.add(file_name)
        save_progress(PROGRESS_FILE, processed_files)

        logging.info(f"Успешная обработка файла: {file_name}, результат сохранен в {output_path}")
    except Exception as e:
        logging.error(f"Ошибка обработки файла {file_name}: {e}")

def ocr_with_easyocr(input_dir, output_dir, num_threads=3, contrast_ths=0.7, adjust_contrast=0.5):
    reader = easyocr.Reader(['en', 'ru'])
    os.makedirs(output_dir, exist_ok=True)

    # Загрузка прогресса обработки
    processed_files = load_progress(PROGRESS_FILE)


    image_files = []
    for root, _, files in os.walk(input_dir):
        for file_name in files:
            if file_name.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.tiff')):
                image_files.append(os.path.join(root, file_name))

    print(f"Найдено изображений: {len(image_files)}")
    print(f"Пропущено ранее обработанных: {len(processed_files)}")

    # Обработка изображений с использованием потоков
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [
            executor.submit(process_image, reader, image_path, output_dir, processed_files, contrast_ths, adjust_contrast)
            for image_path in image_files
        ]
        for future in futures:
            try:
                future.result()
            except Exception as e:
                logging.error(f"Ошибка при выполнении потока: {e}")

if __name__ == "__main__":
    input_folder = r"C:\Users\quvon\Desktop\OCR\Ocr2\data\train"
    output_folder = "output/ocr_results2"

    ocr_with_easyocr(
        input_dir=input_folder,
        output_dir=output_folder,
        num_threads=4,
        contrast_ths=0.6,
        adjust_contrast=0.7
    )
