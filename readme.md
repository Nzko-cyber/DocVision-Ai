# 📄 OCR, Document Classification, and Data Extraction System

![Project Banner](https://via.placeholder.com/1200x300?text=OCR+Document+System)  

## 🚀 Project Overview  
This project is a **comprehensive solution** for:
- 📝 **Optical Character Recognition (OCR):** Extract text from various formats like PDFs, DOCX, JPGs, and more.
- 🗂️ **Document Classification:** Categorize documents (e.g., invoices, memos, letters) using a ResNet18-based model.
- 🔍 **Key Data Extraction:** Identify critical information such as dates, amounts, and names.
- ✅ **Spellcheck & Punctuation Correction:** Enhance OCR text accuracy with LanguageTool.
- 📊 **Document Structure Analysis:** Retain tables, headings, and paragraphs for readability.  

✨ **Optimized for seamless API integration** into workflows and high-performance document processing.

---

## 🛠️ Key Features  
### 🎯 High-Quality OCR  
- Supports **PDF, DOCX, and image formats**.  
- Enhances text extraction with preprocessing techniques like **noise removal** and **sharpening**.

### 🗂️ Document Classification  
- Classifies documents into categories such as **invoices**, **letters**, **memos**, and more.  
- Powered by a **ResNet18-based classifier**.

### 🔍 Key Data Extraction  
- Extracts structured information, including:
  - 📅 Dates
  - 💵 Amounts
  - 🏢 Entity Names

### ✅ Spellcheck & Correction  
- Fixes spelling and punctuation using **LanguageTool** for post-OCR accuracy.

### 🌐 Scalable API Integration  
- RESTful API endpoints for:
  - Document preprocessing  
  - OCR  
  - Classification  
  - Data extraction  

---

## 📂 Project Structure  
```bash
project_root/
├── data/                             # Input and processed data
│   ├── train/                        # Training dataset
│   ├── val/                          # Validation dataset
│   ├── test/                         # Testing dataset
│   └── processed_train/              # Preprocessed training data
├── models/                           # Trained models
│   ├── classifier_model.pth          # Classification model
│   ├── ner_model.pth                 # NER model (optional)
├── src/                              # Source code
│   ├── api/                          # API endpoints
│   ├── classification/               # Document classification
│   ├── document_structure/           # Document structure analysis
│   ├── extraction/                   # Data extraction modules
│   ├── ocr/                          # OCR modules
│   ├── preprocessing/                # Preprocessing scripts
│   └── utils/                        # Utility functions
├── tests/                            # Integration and unit tests
├── requirements.txt                  # Python dependencies
└── README.md                         # Project documentation
