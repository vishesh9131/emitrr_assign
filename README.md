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

## Comparison BioBERT vs Rule-Based NER vs BERT CONLL03
```
=== MODEL COMPARISON TABLE ===
Chunk      |  Rule-Based  |   BioBERT    | BERT_CONLL03 |   Best Model   
--------------------------------------------------------------------------------
CHUNK_A    |    0.1111    |    0.0370    |    0.2037    |  BERT_CONLL03  
CHUNK_B    |    0.4103    |    0.2179    |    0.2179    | BioBERT & BERT_CONLL03
CHUNK_C    |    0.1667    |    0.1667    |    0.1667    |    All Equal   
CHUNK_D    |    0.2083    |    0.2000    |    0.2000    | BioBERT & BERT_CONLL03
CHUNK_E    |    0.2778    |    0.2778    |    0.2778    |    All Equal   
CHUNK_F    |    0.1667    |    0.0000    |    0.0000    | BioBERT & BERT_CONLL03
CHUNK_G    |    0.1667    |    0.1667    |    0.1667    |    All Equal   
CHUNK_H    |    0.0556    |    0.0000    |    0.1667    |  BERT_CONLL03  
CHUNK_I    |    0.2222    |    0.1667    |    0.1667    | BioBERT & BERT_CONLL03
CHUNK_J    |    0.1667    |    0.0000    |    0.1667    | Rule-Based & BERT_CONLL03
CHUNK_K    |    0.1667    |    0.1667    |    0.1667    |    All Equal   
CHUNK_L    |    0.1667    |    0.1667    |    0.1667    |    All Equal   
CHUNK_M    |    0.1667    |    0.1667    |    0.1667    |    All Equal   
CHUNK_N    |    0.0000    |    0.0000    |    0.0000    |    All Equal   
CHUNK_O    |    0.0000    |    0.1667    |    0.0000    | Rule-Based & BERT_CONLL03
CHUNK_P    |    0.2778    |    0.0000    |    0.1667    |   Rule-Based   
CHUNK_Q    |    0.0000    |    0.1667    |    0.1667    | BioBERT & BERT_CONLL03
CHUNK_R    |    0.0606    |    0.2111    |    0.2111    | BioBERT & BERT_CONLL03
CHUNK_S    |    0.0741    |    0.1667    |    0.1667    | BioBERT & BERT_CONLL03
CHUNK_T    |    0.2273    |    0.2333    |    0.2333    | BioBERT & BERT_CONLL03
CHUNK_U    |    0.0000    |    0.0000    |    0.0000    |    All Equal   
TEST_CHUNK_A |    0.2333    |    0.2143    |    0.2143    | BioBERT & BERT_CONLL03
TEST_CHUNK_B |    0.3333    |    0.0303    |    0.1970    |   Rule-Based   
TEST_CHUNK_C |    0.0000    |    0.0000    |    0.0000    |    All Equal   
TEST_CHUNK_D |    0.1667    |    0.0000    |    0.1667    | Rule-Based & BERT_CONLL03
TEST_CHUNK_E |    0.0000    |    0.0000    |    0.0000    |    All Equal   
TEST_CHUNK_F |    0.2333    |    0.0556    |    0.2222    |   Rule-Based   
TEST_CHUNK_G |    0.1667    |    0.0000    |    0.1667    | Rule-Based & BERT_CONLL03
TEST_CHUNK_H |    0.1667    |    0.0000    |    0.0000    | BioBERT & BERT_CONLL03
TEST_CHUNK_I |    0.0000    |    0.0000    |    0.0000    |    All Equal   
TEST_CHUNK_J |    0.1667    |    0.0000    |    0.0000    | BioBERT & BERT_CONLL03
```
```
=== MODEL PERFORMANCE SUMMARY ===
BERT_CONLL03 better on 2 chunks
BioBERT & BERT_CONLL03 better on 7 chunks
All Equal better on 8 chunks
Rule-Based better on 2 chunks
Rule-Based & BERT_CONLL03 better on 2 chunks
```
### note : BERT_CONLL03 is the most accurate model overall based on the comparison table.
