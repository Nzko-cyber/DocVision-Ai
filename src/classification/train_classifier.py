
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader
from torchvision.models import ResNet18_Weights

torch.cuda.is_available()

def train_classifier(train_dir, val_dir, output_model_path, num_classes=15, num_epochs=10, batch_size=32):
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
    ])


    train_dataset = datasets.ImageFolder(train_dir, transform=transform)
    val_dataset = datasets.ImageFolder(val_dir, transform=transform)
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=batch_size)

    print(f"Обучающих изображений: {len(train_dataset)}, Валидационных изображений: {len(val_dataset)}")
    print(f"Классы: {train_dataset.classes}")

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = models.resnet18(weights=ResNet18_Weights.IMAGENET1K_V1)
    model.fc = nn.Linear(model.fc.in_features, num_classes)
    model = model.to(device)

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    for epoch in range(num_epochs):
        model.train()
        running_loss = 0.0
        for inputs, labels in train_loader:
            inputs, labels = inputs.to(device), labels.to(device)
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            running_loss += loss.item()

        print(f"Эпоха [{epoch+1}/{num_epochs}], Потери: {running_loss / len(train_loader):.4f}")


        model.eval()
        correct, total = 0, 0
        with torch.no_grad():
            for inputs, labels in val_loader:
                inputs, labels = inputs.to(device), labels.to(device)
                outputs = model(inputs)
                _, predicted = torch.max(outputs, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()

        accuracy = 100 * correct / total
        print(f"Точность на валидации: {accuracy:.2f}%")

    torch.save(model.state_dict(), output_model_path)
    print(f"Модель сохранена в: {output_model_path}")

if __name__ == "__main__":
    train_directory = r"C:\Users\quvon\Desktop\OCR\Ocr2\data\processed_train\train"
    val_directory = r"C:\Users\quvon\Desktop\OCR\Ocr2\data\processed_train\val"
    model_output_path = r"../../models/classifier.pth"

    train_classifier(train_directory, val_directory, model_output_path)
