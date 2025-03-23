# Project's mind 

```
Physician Notetaker
├── 1. Medical NLP Summarization
│   ├── Named Entity Recognition (NER)
│   │   └── Extract: Symptoms, Treatment ,Diagnosis, Prognosis
│   ├── Text Summarization
│   │   └── Convert transcript to structured medical report
│   └── Keyword Extraction
│       └── Identify important medical phrases
│
├── 2. Sentiment & Intent Analysis
│   ├── Sentiment Classification
│   │   └── Classify patient sentiment (Anxious, Neutral, Reassured)
│   └── Intent Detection
│       └── Identify patient intent (seeking reassurance, reporting symptoms, etc.)
│
├── 3. SOAP Note Generation (Bonus)
│   ├── Automated SOAP Note Generation
│   ├── Logical Mapping of SOAP sections
│   └── Text Structuring & Formatting
│
└── Submission Requirements
    ├── GitHub Repository
    ├── Live Application
    └── README with setup instructions, screenshots, and methodology
```

```
prasn_1
~1/
├── app.py                # Main Streamlit application
├── requirements.txt      # Dependencies
├── models/               # For storing models
├── utils/
│   ├── __init__.py
│   ├── ner.py            # Named Entity Recognition
│   ├── summarization.py  # Text Summarization
│   └── keyword.py        # Keyword Extraction
└── README.md
```

# 📊 Model Performance Report

## 🔍 Overview
This document provides an interactive comparison of three models:
- **Rule-Based Model**
- **BioBERT Model**
- **BERT_CONLL03 Model**

### **🏆 Best Performing Model:**
- The **Rule-Based Model** achieved the highest overall accuracy of **0.1470**.

## 📈 Overall Model Accuracy
| Model          | Overall Accuracy | Patient Name Accuracy | Symptoms F1 | Diagnosis Match | Treatment F1 | Status Match | Prognosis Match |
|---------------|-----------------|-----------------------|------------|----------------|-------------|--------------|---------------|
| Rule-Based    | **0.1470**       | **0.7527**           | **0.1387** | **0.0645**     | **0.0339**  | **0.0000**   | **0.0000**    |
| BioBERT      | 0.1014           | 0.6849                | 0.0660     | 0.0323         | 0.0264      | 0.0000       | 0.0000        |
| BERT_CONLL03 | 0.1175           | 0.6774                | 0.0660     | 0.0323         | 0.0264      | 0.0000       | 0.0000        |

## 📊 Field-by-Field Comparison
| Field                | Rule-Based | BioBERT | BERT_CONLL03 | Best Model |
|----------------------|------------|---------|-------------|------------|
| **Patient Name Accuracy** | **0.7527** | 0.6849  | 0.6774      | **Rule-Based** |
| **Symptoms F1**           | **0.1387** | 0.0660  | 0.0660      | **Rule-Based** |
| **Diagnosis Match**       | **0.0645** | 0.0323  | 0.0323      | **Rule-Based** |
| **Treatment F1**         | **0.0339** | 0.0264  | 0.0264      | **Rule-Based** |
| **Status Match**         | 0.0000    | 0.0000  | 0.0000      | **Tie**       |
| **Prognosis Match**      | 0.0000    | 0.0000  | 0.0000      | **Tie**       |

## 📌 Model Comparison by Chunks
This section compares model performance across multiple chunks.

| Chunk     | Rule-Based | BioBERT | BERT_CONLL03 | Best Model |
|-----------|------------|---------|-------------|------------|
| CHUNK_A   | **0.1111** | 0.0370  | 0.0370      | **Rule-Based** |
| CHUNK_B   | **0.4103** | 0.3846  | 0.3846      | **Rule-Based** |
| CHUNK_C   | 0.1667    | 0.1667  | 0.1667      | **Tie** |
| CHUNK_D   | **0.2083** | 0.2000  | 0.2000      | **Rule-Based** |
| CHUNK_E   | 0.2778    | 0.2778  | 0.2778      | **Tie** |
| CHUNK_F   | 0.1667    | 0.0000  | 0.1667      | **Tie** |
| ...       | ...        | ...     | ...         | ... |

### **📌 Summary of Chunk-Wise Best Model Performance:**
- **Rule-Based Model** is best on **26** chunks.
- **BioBERT Model** is best on **16** chunks.
- **BERT_CONLL03 Model** is best on **17** chunks.

## 🎯 Model Performance on Test Chunks
| Model         | Avg. Accuracy on Test Chunks |
|--------------|------------------------------|
| **Rule-Based** | **0.1467** |
| BioBERT      | 0.0300   |
| BERT_CONLL03 | 0.0800   |

### **🏆 Best Model on Test Chunks:**
| Model         | Best on # Test Chunks |
|--------------|----------------------|
| **Rule-Based** | **10** (100.0%) |
| BioBERT      | 3 (30.0%)  |
| BERT_CONLL03 | 5 (50.0%)  |

## 🔬 Name Detection Analysis
| Model         | Name Detection Accuracy |
|--------------|-------------------------|
| Rule-Based    | 0.7667                  |
| **BioBERT**  | **0.8667**               |
| BERT_CONLL03 | 0.7333                   |

## 📌 Conclusion
- **Rule-Based Model** performs best overall with the highest accuracy across multiple chunks and test cases.
- **BioBERT Model** excels in **name detection** accuracy.
- **Further improvements** needed in **Status Match & Prognosis Match** as all models score **0.0000** in these fields.

---
🚀 **Explore more insights by running evaluations on new datasets!**

