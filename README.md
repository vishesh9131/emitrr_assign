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


Here’s an interactive README.md file that includes collapsible sections, tables, and formatted summaries for easy navigation.

⸻

📊 Physician Notetaker - Model Performance Report

🔍 Overview

This document provides a detailed comparison of multiple models for Named Entity Recognition (NER) and Medical NLP Tasks, including:
	•	Rule-Based Model
	•	BioBERT Model
	•	BERT_CONLL03 Model
	•	FineTuned_BioBERT Model

Rule-Based Model achieved the highest overall accuracy of 0.1470.

⸻

🏆 Best Performing Model:

Rule-Based Model with an overall accuracy of 0.1470.

<details>
<summary>📈 Overall Model Accuracy</summary>


Model	Overall Accuracy	Patient Name Accuracy	Symptoms F1	Diagnosis Match	Treatment F1	Status Match	Prognosis Match
Rule-Based	0.1470	0.7527	0.1387	0.0645	0.0339	0.0000	0.0000
BioBERT	0.1014	0.6849	0.0660	0.0323	0.0264	0.0000	0.0000
BERT_CONLL03	0.1175	0.6747	0.0660	0.0323	0.0264	0.0000	0.0000
FineTuned_BioBERT	0.1014	0.5565	0.0660	0.0323	0.0264	0.0000	0.0000

</details>




⸻

🏅 Field-by-Field Comparison

<details>
<summary>🔬 Patient Name Accuracy</summary>


Model	Patient Name Accuracy
Rule-Based	0.7527
BioBERT	0.6849
BERT_CONLL03	0.6747
FineTuned_BioBERT	0.5565

Rule-Based model performed best in patient name detection.

</details>


<details>
<summary>💉 Symptoms F1 Score</summary>


Model	Symptoms F1
Rule-Based	0.1387
BioBERT	0.0660
BERT_CONLL03	0.0660
FineTuned_BioBERT	0.0660

Rule-Based model performed best in symptoms extraction.

</details>


<details>
<summary>🧾 Diagnosis & Treatment</summary>


Model	Diagnosis Match	Treatment F1
Rule-Based	0.0645	0.0339
BioBERT	0.0323	0.0264
BERT_CONLL03	0.0323	0.0264
FineTuned_BioBERT	0.0323	0.0264

Rule-Based model performed best in extracting Diagnosis and Treatment.

</details>




⸻

📌 Chunk-Wise Model Comparison

<details>
<summary>📊 Click to Expand Model Comparison Table</summary>


Chunk	Rule-Based	BioBERT	FineTuned_BioBERT	BERT_CONLL03	Best Model
CHUNK_A	0.1111	0.0370	0.0370	0.0370	Rule-Based
CHUNK_B	0.4103	0.3846	0.3846	0.3846	Rule-Based
CHUNK_C	0.1667	0.1667	0.1667	0.1667	Tie
CHUNK_D	0.2083	0.2000	0.2000	0.2000	Rule-Based
…	…	…	…	…	…

</details>


🏆 Model Performance Summary:
	•	Rule-Based model is best on 26 chunks
	•	BioBERT model is best on 16 chunks
	•	FineTuned_BioBERT model is best on 16 chunks
	•	BERT_CONLL03 model is best on 17 chunks

⸻

🎯 Performance on Test Chunks

<details>
<summary>📌 Average Accuracy on Test Chunks</summary>


Model	Avg. Accuracy on Test Chunks
Rule-Based	0.1467
BioBERT	0.0300
BERT_CONLL03	0.0800

Rule-Based model performed best on test data.

</details>


📌 Best Model on Test Chunks

Model	Best on # Test Chunks
Rule-Based	10 (100.0%)
BioBERT	3 (30.0%)
FineTuned_BioBERT	3 (30.0%)
BERT_CONLL03	5 (50.0%)



⸻

🔬 Name Detection Accuracy

<details>
<summary>🧑‍⚕️ Name Detection Analysis</summary>


Model	Name Detection Accuracy
Rule-Based	0.7667
BioBERT	0.8667
BERT_CONLL03	0.7333
FineTuned_BioBERT	0.8000

BioBERT performs best in name detection.

</details>




⸻

🚀 Conclusion
	•	🏆 Rule-Based Model performs best overall with the highest accuracy across multiple chunks and test cases.
	•	🩺 BioBERT Model excels in name detection accuracy.
	•	📈 Further improvements needed in Status Match & Prognosis Match (all models scored 0.0000).

✅ Next Steps:
🔹 Improve Diagnosis & Prognosis matching using fine-tuned models.
🔹 Implement hybrid approaches combining rule-based and transformer models for better accuracy.
🔹 Enhance test chunk performance with more diverse training data.

⸻

💡 Want to Explore More?

Run additional evaluations on new datasets to further analyze model performance!

📌 Developed for Physician Notetaker NLP Task | 🚀 Optimized for Medical Conversations

⸻

This README is structured for easy navigation, with interactive collapsible sections to make data analysis smoother. 🚀