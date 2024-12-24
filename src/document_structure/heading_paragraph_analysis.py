
import cv2
import pytesseract
import os


def extract_text_blocks(image_path):
    """
    Извлекает текстовые блоки из изображения с использованием Tesseract.
    :param image_path: Путь к изображению.
    :return: Список блоков текста с их координатами.
    """
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


    _, binary = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)


    data = pytesseract.image_to_data(binary, output_type=pytesseract.Output.DICT)
    text_blocks = []

    for i in range(len(data['text'])):
        if int(data['conf'][i]) > 50:
            x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
            text = data['text'][i].strip()
            if text:
                text_blocks.append({'text': text, 'x': x, 'y': y, 'w': w, 'h': h})

    return text_blocks


def analyze_headings_and_paragraphs(text_blocks):

    headings = []
    paragraphs = []

    average_height = sum([block['h'] for block in text_blocks]) / len(text_blocks)

    for block in text_blocks:
        if block['h'] > average_height * 1.5:  # Если высота блока значительно больше средней — это заголовок
            headings.append(block)
        else:
            paragraphs.append(block)

    return headings, paragraphs


def process_document(image_path, output_dir):

    os.makedirs(output_dir, exist_ok=True)


    print(f"Обработка изображения: {image_path}")
    text_blocks = extract_text_blocks(image_path)


    headings, paragraphs = analyze_headings_and_paragraphs(text_blocks)


    output_path = os.path.join(output_dir, "headings_and_paragraphs.txt")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("=== Заголовки ===\n")
        for heading in headings:
            f.write(f"{heading['text']} (Координаты: {heading['x']}, {heading['y']})\n")

        f.write("\n=== Абзацы ===\n")
        for paragraph in paragraphs:
            f.write(f"{paragraph['text']} (Координаты: {paragraph['x']}, {paragraph['y']})\n")

    print(f"Результаты анализа сохранены в: {output_path}")


if __name__ == "__main__":
    input_image = "data/test/sample.jpg"
    output_folder = "output/headings_paragraphs"

    process_document(input_image, output_folder)
