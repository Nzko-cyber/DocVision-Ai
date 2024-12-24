
import torch
from torchvision import transforms, models
from PIL import Image
import os
def load_model(model_file_path, num_classes=15, execution_device="cuda"):
    """
    Загружает обученную модель ResNet18 для классификации.
    """
    device = torch.device(execution_device)
    model_instance = models.resnet18(weights=None)  # Указываем отсутствие предобученных весов
    model_instance.fc = torch.nn.Linear(model_instance.fc.in_features, num_classes)

    # Явно указываем weights_only=True
    model_instance.load_state_dict(torch.load(model_file_path, map_location=execution_device, weights_only=True))
    model_instance.eval()
    model_instance.to(device)
    return model_instance


def predict_category(image_file_path, loaded_model, execution_device, class_labels):
    """
    Предсказывает категорию изображения.
    :param image_file_path: Путь к изображению.
    :param loaded_model: Загруженная модель.
    :param execution_device: Устройство для выполнения ("cpu" или "cuda").
    :param class_labels: Список категорий (классов).
    :return: Предсказанная категория.
    """
    device = torch.device(execution_device)
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
    ])


    image = Image.open(image_file_path).convert("RGB")
    input_tensor = transform(image).unsqueeze(0).to(device)

    # Предсказание
    with torch.no_grad():
        outputs = loaded_model(input_tensor)
        _, predicted = torch.max(outputs, 1)
    return class_labels[predicted.item()]

if __name__ == "__main__":
    model_file = "../../models/classifier.pth"
    test_image_path = r"C:\Users\quvon\Desktop\OCR\Ocr2\data\processed_train\test\budget.jpeg"
    label_classes = ['advertisement', 'budget', 'email', 'file folder', 'form',
                     'handwritten', 'invoice', 'letter', 'memo', 'news article',
                     'questionnaire', 'resume', 'scientific publication', 'scientific report', 'specification']

    execution_device = "cuda" if torch.cuda.is_available() else "cpu"


    classifier_model = load_model(model_file, num_classes=len(label_classes), execution_device=execution_device)


    if os.path.exists(test_image_path):
        category = predict_category(test_image_path, classifier_model, execution_device, label_classes)
        print(f"Изображение: {test_image_path}")
        print(f"Предсказанная категория: {category}")
    else:
        print(f"Ошибка: Файл {test_image_path} не найден.")
