import os
import shutil
import requests


BASE_URL = "http://127.0.0.1:5000"
UPLOAD_FOLDER = "test_data/uploads"
OUTPUT_FOLDER = "test_data/output"

def setup_test_environment():
    """
    Подготавливает тестовую среду: создает тестовые папки и файлы.
    """
    if os.path.exists("test_data"):
        shutil.rmtree("test_data")

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)


    sample_image_path = os.path.join(UPLOAD_FOLDER, "sample_image.jpg")
    with open(sample_image_path, "wb") as f:
        f.write(requests.get("https://via.placeholder.com/300").content)
    print("✅ Тестовая среда подготовлена.")
    return sample_image_path

def test_classify(sample_image_path):

    url = f"{BASE_URL}/classify"
    payload = {"file_path": sample_image_path}

    response = requests.post(url, json=payload)
    assert response.status_code == 200, f"Ошибка классификации: {response.json()}"
    print(f"✅ Классификация успешна: {response.json()}")

def test_ocr(sample_image_path):

    url = f"{BASE_URL}/ocr"
    payload = {"file_path": sample_image_path}

    response = requests.post(url, json=payload)
    assert response.status_code == 200, f"Ошибка OCR: {response.json()}"
    print(f"✅ OCR успешен: {response.json()}")
    return response.json()["output_path"]  # Возвращаем путь к OCR результатам

def test_spellcheck(results_dir):

    url = f"{BASE_URL}/spellcheck"
    payload = {"ocr_results_dir": results_dir}

    response = requests.post(url, json=payload)
    assert response.status_code == 200, f"Ошибка проверки орфографии: {response.json()}"
    print(f"✅ Проверка орфографии успешна: {response.json()}")

def test_extract(results_dir):

    url = f"{BASE_URL}/extract"
    payload = {"ocr_results_dir": results_dir}

    response = requests.post(url, json=payload)
    assert response.status_code == 200, f"Ошибка извлечения данных: {response.json()}"
    print(f"✅ Извлечение данных успешно: {response.json()}")

def cleanup_test_environment():

    if os.path.exists("test_data"):
        shutil.rmtree("test_data")
    print("🧹 Тестовая среда очищена.")

if __name__ == "__main__":
    try:
        print("🚀 Запуск интеграционных тестов...")
        sample_image = setup_test_environment()


        test_classify(sample_image)


        ocr_results_dir = test_ocr(sample_image)


        test_spellcheck(ocr_results_dir)


        test_extract(ocr_results_dir)

        print("🎉 Все интеграционные тесты выполнены успешно!")
    except Exception as e:
        print(f"❌ Тесты завершились с ошибкой: {str(e)}")
    finally:
        cleanup_test_environment()
