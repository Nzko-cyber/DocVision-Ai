from flask import Flask, request, jsonify
from flask_cors import CORS  # Enable CORS
import os
import torch
import easyocr
from Ocr2.src.document_structure.extract_tables import extract_table_data
from Ocr2.src.document_structure.heading_paragraph_analysis import process_document

from Ocr2.src.classification.predict_category import load_model, predict_category
from Ocr2.src.extraction.extract_key_data import process_ocr_results
from Ocr2.src.extraction.spelling_punctuation_check import check_spelling_and_punctuation

# Global Configurations
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "output"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Load Model
MODEL_PATH = "../../models/classifier.pth"
LABEL_CLASSES = [
    'advertisement', 'budget', 'email', 'file folder', 'form',
    'handwritten', 'invoice', 'letter', 'memo', 'news article',
    'questionnaire', 'resume', 'scientific publication', 'scientific report', 'specification'
]
EXECUTION_DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
CLASSIFICATION_MODEL = load_model(MODEL_PATH, num_classes=len(LABEL_CLASSES), execution_device=EXECUTION_DEVICE)

# Initialize Flask App
app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return jsonify({"message": "OCR, Classification, and Extraction API is running!"})

@app.route("/classify", methods=["POST"])
def classify():
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No file provided"}), 400

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    try:
        category = predict_category(file_path, CLASSIFICATION_MODEL, EXECUTION_DEVICE, LABEL_CLASSES)
        return jsonify({"message": "Classification complete", "category": category})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/ocr", methods=["POST"])
def ocr():
    if 'file' not in request.files:
        print("DEBUG: No file key in request.files")
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    if not file.filename:
        print("DEBUG: Empty file provided")
        return jsonify({"error": "No file selected"}), 400

    print(f"DEBUG: Received file: {file.filename}")

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    try:
        file.save(file_path)
        print(f"DEBUG: File saved to: {file_path}")

        reader = easyocr.Reader(['en', 'ru'])
        results = reader.readtext(file_path, detail=0)
        print(f"DEBUG: OCR results: {results}")

        return jsonify({"message": "OCR completed", "results": results}), 200
    except Exception as e:
        print(f"DEBUG: OCR Error: {str(e)}")
        return jsonify({"error": str(e)}), 500



@app.route("/spellcheck", methods=["POST"])
def spellcheck():
    ocr_results_dir = request.form.get("ocr_results_dir")
    output_dir = os.path.join(OUTPUT_FOLDER, "corrected_text")
    os.makedirs(output_dir, exist_ok=True)

    if not ocr_results_dir or not os.path.exists(ocr_results_dir):
        return jsonify({"error": "OCR results directory not found"}), 400

    try:
        check_spelling_and_punctuation(ocr_results_dir, output_dir)
        return jsonify({"message": "Spellcheck completed", "output_path": output_dir}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/extract_tables", methods=["POST"])
def extract_tables():
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No file provided"}), 400

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    output_dir = os.path.join(OUTPUT_FOLDER, "tables")
    os.makedirs(output_dir, exist_ok=True)

    try:
        extract_table_data(file_path, os.path.join(output_dir, f"{file.filename}.csv"))
        return jsonify({"message": "Tables extracted successfully", "output_path": output_dir}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/analyze_headings", methods=["POST"])
def analyze_headings():
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No file provided"}), 400

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    output_dir = os.path.join(OUTPUT_FOLDER, "headings_paragraphs")
    os.makedirs(output_dir, exist_ok=True)

    try:
        process_document(file_path, output_dir)
        return jsonify({"message": "Heading analysis completed", "output_path": output_dir}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/extract", methods=["POST"])
def extract():
    ocr_dir = request.form.get("ocr_results_dir")
    output_path = os.path.join(OUTPUT_FOLDER, "extracted_data")

    if not ocr_dir or not os.path.exists(ocr_dir):
        return jsonify({"error": "OCR results directory not found"}), 400
    try:
        process_ocr_results(ocr_dir, output_path)
        return jsonify({"message": "Data extraction completed", "output_path": output_path}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
