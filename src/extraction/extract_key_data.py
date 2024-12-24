
import spacy
import json
import os
from typing import TextIO

def load_ner_model():

    try:
        nlp = spacy.load("en_core_web_sm")
    except OSError:
        os.system("python -m spacy download en_core_web_sm")
        nlp = spacy.load("en_core_web_sm")
    return nlp

def extract_entities(text, nlp):
    """
    Извлекает ключевые данные из текста с использованием NER.
    :param text: Входной текст для анализа.
    :param nlp: Загруженная NER модель.
    :return: Словарь с извлеченными сущностями.
    """
    doc = nlp(text)
    entities = {"DATES": [], "MONEY": [], "ORG": [], "PERSON": []}
    for ent in doc.ents:
        if ent.label_ in entities:
            entities[ent.label_].append(ent.text)
    return entities

def process_ocr_results(ocr_dir, output_dir):
    """
    Обрабатывает JSON-файлы с результатами OCR и извлекает ключевые данные.
    :param ocr_dir: Путь к папке с JSON-файлами OCR.
    :param output_dir: Путь для сохранения извлеченных данных.
    """
    os.makedirs(output_dir, exist_ok=True)
    nlp = load_ner_model()

    for file_name in os.listdir(ocr_dir):
        if file_name.endswith(".json"):
            with open(os.path.join(ocr_dir, file_name), "r", encoding="utf-8") as f:
                ocr_data = json.load(f)
                text = " ".join(ocr_data.get("text", []))


            entities = extract_entities(text, nlp)


            output_path = os.path.join(output_dir, file_name.replace(".json", "_ner.json"))
            with open(output_path, "w", encoding="utf-8") as out_file:  # type: TextIO
                json.dump(entities, out_file, ensure_ascii=False, indent=4)  # type: ignore
            print(f"Ключевые данные сохранены: {output_path}")

if __name__ == "__main__":
    ocr_results_dir = "output/ocr_results"
    extracted_data_dir = "output/extracted_data"

    process_ocr_results(ocr_results_dir, extracted_data_dir)
