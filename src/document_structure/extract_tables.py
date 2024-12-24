
import cv2
import pytesseract
import os
import numpy as np
import pandas as pd

# Укажите путь к Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def preprocess_image(image_path):
    """
    Подготовка изображения: бинаризация и морфологическая обработка.
    """
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    _, binary = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY_INV)

    kernel = np.ones((2, 2), np.uint8)
    binary = cv2.erode(binary, kernel, iterations=1)
    binary = cv2.dilate(binary, kernel, iterations=2)

    return binary

def detect_table(image):
    """
    Обнаружение структуры таблицы с помощью морфологических операций.
    """
    kernel_h = cv2.getStructuringElement(cv2.MORPH_RECT, (50, 1))
    kernel_v = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 50))

    horizontal = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel_h)
    vertical = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel_v)

    table_structure = cv2.add(horizontal, vertical)
    contours, _ = cv2.findContours(table_structure, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    return contours

def extract_table_data(image_path, output_csv_path):
    """
    Извлечение данных из таблицы с использованием Tesseract.
    """
    binary_image = preprocess_image(image_path)
    contours = detect_table(binary_image)

    image = cv2.imread(image_path)
    rows = []

    for contour in contours:
        x_coord, y_coord, w, h = cv2.boundingRect(contour)
        if w > 50 and h > 20:
            table_cell = image[y_coord:y_coord + h, x_coord:x_coord + w]
            try:
                # OCR для ячейки таблицы
                text = pytesseract.image_to_string(table_cell, config='--psm 6').strip()
                if text:  # Добавляем только если текст не пустой
                    rows.append((x_coord, y_coord, text))
            except Exception as e:
                print(f"Ошибка OCR на контуре {x_coord}, {y_coord}, {w}, {h}: {e}")
                # Сохраняем изображение ячейки для отладки
                debug_path = f"debug_cell_{x_coord}_{y_coord}.png"
                cv2.imwrite(debug_path, table_cell)
                print(f"Ячейка сохранена для отладки: {debug_path}")

    if rows:
        rows = sorted(rows, key=lambda x: (x[1], x[0]))  # Сортировка по координатам
        data = [row[2] for row in rows]

        # Сохранение данных в CSV
        df = pd.DataFrame(data, columns=["Content"])
        df.to_csv(output_csv_path, index=False)
        print(f"Таблица сохранена в: {output_csv_path}")
    else:
        print(f"Нет данных для сохранения из изображения {image_path}")

def process_table_images(input_dir, output_dir):
    """
    Обработка всех изображений в указанной папке.
    """
    os.makedirs(output_dir, exist_ok=True)

    for file_name in os.listdir(input_dir):
        if file_name.endswith(('.jpg', '.png', '.jpeg')):
            image_path = os.path.join(input_dir, file_name)
            output_csv_path = os.path.join(output_dir, file_name.replace(".jpg", ".csv").replace(".png", ".csv"))
            print(f"Обработка таблицы: {image_path}")
            extract_table_data(image_path, output_csv_path)

if __name__ == "__main__":
    input_folder = r"C:\Users\quvon\Desktop\OCR\Ocr2\data\ss"  # Путь к папке с изображениями
    output_folder = "output/tables"

    process_table_images(input_folder, output_folder)
