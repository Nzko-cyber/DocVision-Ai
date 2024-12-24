<<<<<<< HEAD
import cv2
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed
from sklearn.model_selection import train_test_split
import os

def preprocess_image_cpu(img_path, source_dir, output_base_dir):
    """
    Предобработка изображения на CPU и сохранение результата.
    """
    img_path = Path(img_path)
    img = cv2.imread(str(img_path), cv2.IMREAD_GRAYSCALE)

    if img is None:
        print(f"Ошибка загрузки: {img_path}")
        return

    try:

        denoised = cv2.fastNlMeansDenoising(img, h=30)

        # Бинаризация
        _, binary = cv2.threshold(denoised, 128, 255, cv2.THRESH_BINARY)


        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        sharpened = cv2.morphologyEx(binary, cv2.MORPH_GRADIENT, kernel)

        relative_path = img_path.relative_to(source_dir)
        output_file_path = Path(output_base_dir) / relative_path
        output_file_path.parent.mkdir(parents=True, exist_ok=True)

        cv2.imwrite(str(output_file_path), sharpened)
        print(f"Обработано и сохранено: {output_file_path}")
    except Exception as e:
        print(f"Ошибка при обработке {img_path}: {e}")

def preprocess_and_save_images_parallel(image_list, source_dir, output_base_dir, num_workers=None):
    """
    Параллельная обработка изображений на CPU с контролем количества процессов.
    """
    if num_workers is None:
        num_workers = os.cpu_count() - 1

    print(f"Запуск параллельной обработки с {num_workers} процессами...")
    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        futures = [executor.submit(preprocess_image_cpu, img_path, source_dir, output_base_dir)
                   for img_path in image_list]

        for future in as_completed(futures):
            future.result()

if __name__ == "__main__":
    input_dir = Path(r"C:\Users\quvon\Desktop\OCR\Ocr2\data\train").resolve()
    output_dir = Path(r"C:\Users\quvon\Desktop\OCR\Ocr2\data\processed_train").resolve()

    images = [str(img_path) for img_path in Path(input_dir).rglob("*")
              if img_path.suffix.lower() in ('.jpg', '.jpeg', '.png')]
    print(f"Найдено {len(images)} изображений")

    if not images:
        raise ValueError(f"Нет изображений в папке {input_dir}")


    train_images, test_images = train_test_split(images, test_size=0.2, random_state=42)
    print(f"Train: {len(train_images)}, Test: {len(test_images)}")


    preprocess_and_save_images_parallel(train_images, input_dir, output_dir / 'train')
    preprocess_and_save_images_parallel(test_images, input_dir, output_dir / 'test')
=======
import cv2
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed
from sklearn.model_selection import train_test_split
import os

def preprocess_image_cpu(img_path, source_dir, output_base_dir):
    """
    Предобработка изображения на CPU и сохранение результата.
    """
    img_path = Path(img_path)
    img = cv2.imread(str(img_path), cv2.IMREAD_GRAYSCALE)

    if img is None:
        print(f"Ошибка загрузки: {img_path}")
        return

    try:

        denoised = cv2.fastNlMeansDenoising(img, h=30)

        # Бинаризация
        _, binary = cv2.threshold(denoised, 128, 255, cv2.THRESH_BINARY)


        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        sharpened = cv2.morphologyEx(binary, cv2.MORPH_GRADIENT, kernel)

        relative_path = img_path.relative_to(source_dir)
        output_file_path = Path(output_base_dir) / relative_path
        output_file_path.parent.mkdir(parents=True, exist_ok=True)

        cv2.imwrite(str(output_file_path), sharpened)
        print(f"Обработано и сохранено: {output_file_path}")
    except Exception as e:
        print(f"Ошибка при обработке {img_path}: {e}")

def preprocess_and_save_images_parallel(image_list, source_dir, output_base_dir, num_workers=None):
    """
    Параллельная обработка изображений на CPU с контролем количества процессов.
    """
    if num_workers is None:
        num_workers = os.cpu_count() - 1

    print(f"Запуск параллельной обработки с {num_workers} процессами...")
    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        futures = [executor.submit(preprocess_image_cpu, img_path, source_dir, output_base_dir)
                   for img_path in image_list]

        for future in as_completed(futures):
            future.result()

if __name__ == "__main__":
    input_dir = Path(r"C:\Users\quvon\Desktop\OCR\Ocr2\data\train").resolve()
    output_dir = Path(r"C:\Users\quvon\Desktop\OCR\Ocr2\data\processed_train").resolve()

    images = [str(img_path) for img_path in Path(input_dir).rglob("*")
              if img_path.suffix.lower() in ('.jpg', '.jpeg', '.png')]
    print(f"Найдено {len(images)} изображений")

    if not images:
        raise ValueError(f"Нет изображений в папке {input_dir}")


    train_images, test_images = train_test_split(images, test_size=0.2, random_state=42)
    print(f"Train: {len(train_images)}, Test: {len(test_images)}")


    preprocess_and_save_images_parallel(train_images, input_dir, output_dir / 'train')
    preprocess_and_save_images_parallel(test_images, input_dir, output_dir / 'test')
>>>>>>> 75bc998f7ed79a04da2b9a8d7988df558d3f8125
