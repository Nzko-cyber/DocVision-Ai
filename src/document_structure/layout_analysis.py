
import cv2
import pytesseract
import os
import json

def analyze_layout(image_path, output_dir):
    """
    Анализирует структуру документа, определяя текстовые блоки и сохраняет их координаты.
    :param image_path: Путь к изображению документа.
    :param output_dir: Папка для сохранения результатов анализа.
    """
    os.makedirs(output_dir, exist_ok=True)

    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


    _, binary = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY_INV)


    hocr_output = pytesseract.image_to_pdf_or_hocr(binary, extension='hocr', config='--psm 6')

    # Сохранение hOCR в файл
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    hocr_path = os.path.join(output_dir, f"{base_name}_layout.hocr")
    with open(hocr_path, 'wb') as f:
        f.write(hocr_output)
    print(f"hOCR файл сохранен: {hocr_path}")


    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    blocks = []


    for idx, contour in enumerate(contours):
        x, y, w, h = cv2.boundingRect(contour)
        if w > 50 and h > 20:  # Фильтрация мелких блоков
            blocks.append({"block": idx + 1, "x": x, "y": y, "width": w, "height": h})
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)


    output_image_path = os.path.join(output_dir, f"{base_name}_blocks.jpg")
    cv2.imwrite(output_image_path, image)
    print(f"Изображение с блоками сохранено: {output_image_path}")


    blocks_json_path = os.path.join(output_dir, f"{base_name}_blocks.json")
    with open(blocks_json_path, 'w', encoding='utf-8') as f:
        json.dump(blocks, f, ensure_ascii=False, indent=4)  # type: ignore
    print(f"Координаты блоков сохранены: {blocks_json_path}")

def process_layouts(input_dir, output_dir):

    os.makedirs(output_dir, exist_ok=True)

    for file_name in os.listdir(input_dir):
        if file_name.endswith(('.jpg', '.jpeg', '.png')):
            image_path = os.path.join(input_dir, file_name)
            print(f"Обработка макета: {image_path}")
            analyze_layout(image_path, output_dir)


if __name__ == "__main__":
    input_folder = "data/test.pdf"
    output_folder = "output/layout_analysis"

    process_layouts(input_folder, output_folder)
