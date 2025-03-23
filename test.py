import json
from collections import defaultdict
import re


from utils.ner import MedicalNER
from utils.biobert_ner import BioBERTNER
from utils.bert_name_detector import BERTNameDetector

from transcript import *
def calculate_accuracy(predicted, ground_truth):
    """
    Calculate accuracy metrics for NER predictions
    Returns precision, recall, and F1 score
    """
    # For Patient_Name (exact match)
    name_correct = predicted["Patient_Name"] == ground_truth["Patient_Name"]
    
    # For list fields (Symptoms, Treatment)
    symptoms_precision = len(set(predicted["Symptoms"]) & set(ground_truth["Symptoms"])) / len(predicted["Symptoms"]) if predicted["Symptoms"] else 0
    symptoms_recall = len(set(predicted["Symptoms"]) & set(ground_truth["Symptoms"])) / len(ground_truth["Symptoms"]) if ground_truth["Symptoms"] else 0
    symptoms_f1 = 2 * (symptoms_precision * symptoms_recall) / (symptoms_precision + symptoms_recall) if (symptoms_precision + symptoms_recall) > 0 else 0
    
    treatment_precision = len(set(predicted["Treatment"]) & set(ground_truth["Treatment"])) / len(predicted["Treatment"]) if predicted["Treatment"] else 0
    treatment_recall = len(set(predicted["Treatment"]) & set(ground_truth["Treatment"])) / len(ground_truth["Treatment"]) if ground_truth["Treatment"] else 0
    treatment_f1 = 2 * (treatment_precision * treatment_recall) / (treatment_precision + treatment_recall) if (treatment_precision + treatment_recall) > 0 else 0
    
    # For string fields (Diagnosis, Current_Status, Prognosis) - use partial matching
    # Handle None values for these fields
    diagnosis_match = 0.0
    if ground_truth["Diagnosis"] is not None and predicted["Diagnosis"] is not None:
        diagnosis_match = 1.0 if ground_truth["Diagnosis"] in predicted["Diagnosis"] or predicted["Diagnosis"] in ground_truth["Diagnosis"] else 0.0
    elif ground_truth["Diagnosis"] is None and predicted["Diagnosis"] is None:
        diagnosis_match = 1.0  # Both are None, consider it a match
    
    status_match = 0.0
    if ground_truth["Current_Status"] is not None and predicted["Current_Status"] is not None:
        status_match = 1.0 if ground_truth["Current_Status"] in predicted["Current_Status"] or predicted["Current_Status"] in ground_truth["Current_Status"] else 0.0
    elif ground_truth["Current_Status"] is None and predicted["Current_Status"] is None:
        status_match = 1.0  # Both are None, consider it a match
    
    prognosis_match = 0.0
    if ground_truth["Prognosis"] is not None and predicted["Prognosis"] is not None:
        prognosis_match = 1.0 if ground_truth["Prognosis"] in predicted["Prognosis"] or predicted["Prognosis"] in ground_truth["Prognosis"] else 0.0
    elif ground_truth["Prognosis"] is None and predicted["Prognosis"] is None:
        prognosis_match = 1.0  # Both are None, consider it a match
    
    # Overall accuracy
    field_scores = [
        1.0 if name_correct else 0.0,
        symptoms_f1,
        diagnosis_match,
        treatment_f1,
        status_match,
        prognosis_match
    ]
    
    overall_accuracy = sum(field_scores) / len(field_scores)
    
    return {
        "Patient_Name_Accuracy": 1.0 if name_correct else 0.0,
        "Symptoms_Precision": symptoms_precision,
        "Symptoms_Recall": symptoms_recall,
        "Symptoms_F1": symptoms_f1,
        "Diagnosis_Match": diagnosis_match,
        "Treatment_Precision": treatment_precision,
        "Treatment_Recall": treatment_recall,
        "Treatment_F1": treatment_f1,
        "Status_Match": status_match,
        "Prognosis_Match": prognosis_match,
        "Overall_Accuracy": overall_accuracy
    }

def evaluate_name_extraction(chunk_text, expected_name, model_name, extractor):
    """Evaluate name extraction for a specific model"""
    try:
        if model_name == "Rule_Based":
            extracted_name = extractor.extract_name(chunk_text)
        elif model_name == "BioBERT":
            extracted_name = extractor.extract_name(chunk_text)
        elif model_name == "BERT_CONLL03":
            # For BERT_CONLL03, we need to ensure the model is loaded
            if not extractor.is_loaded:
                extractor.load_model()
            # Use the extract_name method which handles special cases
            extracted_name = extractor.extract_name(chunk_text)
        
        # Normalize names for comparison
        expected_normalized = normalize_name(expected_name)
        extracted_normalized = normalize_name(extracted_name)
        
        # Check for exact match first
        if extracted_name == expected_name:
            return 1.0, extracted_name
        
        # Check for normalized match
        if extracted_normalized == expected_normalized:
            return 1.0, extracted_name
        
        # Check for partial match (first name or last name)
        expected_parts = expected_normalized.split()
        extracted_parts = extracted_normalized.split()
        
        # If either name has parts and there's an overlap
        if expected_parts and extracted_parts:
            # Check if any part matches
            for part in expected_parts:
                if part in extracted_parts:
                    return 0.5, extracted_name
        
        # No match
        return 0.0, extracted_name
    except Exception as e:
        print(f"Error in {model_name} name extraction: {str(e)}")
        return 0.0, "ERROR"

def normalize_name(name):
    """Normalize name for comparison by removing punctuation and lowercasing"""
    if not name:
        return ""
    # Remove spaces around hyphens and apostrophes
    name = re.sub(r'\s*-\s*', '-', name)
    name = re.sub(r'\s*\'\s*', "'", name)
    # Remove other punctuation and extra spaces
    name = re.sub(r'[^\w\s\'-]', '', name)
    # Convert to lowercase and normalize whitespace
    return ' '.join(name.lower().split())

def evaluate_models():
    # Initialize models
    rule_based_ner = MedicalNER()
    biobert_ner = BioBERTNER()
    bert_name_detector = BERTNameDetector() 
    
    # Get all chunks from transcript.py
    chunks = {
        "CHUNK_A": CHUNK_A,
        "CHUNK_B": CHUNK_B,
        "CHUNK_C": CHUNK_C,
        "CHUNK_D": CHUNK_D,
        "CHUNK_E": CHUNK_E,
        "CHUNK_F": CHUNK_F,
        "CHUNK_G": CHUNK_G,
        "CHUNK_H": CHUNK_H,
        "CHUNK_I": CHUNK_I,
        "CHUNK_J": CHUNK_J,
        "CHUNK_K": CHUNK_K,
        "CHUNK_L": CHUNK_L,
        "CHUNK_M": CHUNK_M,
        "CHUNK_N": CHUNK_N,
        "CHUNK_O": CHUNK_O,
        "CHUNK_P": CHUNK_P,
        "CHUNK_Q": CHUNK_Q,
        "CHUNK_R": CHUNK_R,
        "CHUNK_S": CHUNK_S,
        "CHUNK_T": CHUNK_T,
        "CHUNK_U": CHUNK_U,
        # Add new test chunks
        "TEST_CHUNK_A": TEST_CHUNK_A,
        "TEST_CHUNK_B": TEST_CHUNK_B,
        "TEST_CHUNK_C": TEST_CHUNK_C,
        "TEST_CHUNK_D": TEST_CHUNK_D,
        "TEST_CHUNK_E": TEST_CHUNK_E,
        "TEST_CHUNK_F": TEST_CHUNK_F,
        "TEST_CHUNK_G": TEST_CHUNK_G,
        "TEST_CHUNK_H": TEST_CHUNK_H,
        "TEST_CHUNK_I": TEST_CHUNK_I,
        "TEST_CHUNK_J": TEST_CHUNK_J
    }
    
    # Get ground truth data
    ground_truth = {
        "CHUNK_A": OUT_CHUNK_A,
        "CHUNK_B": OUT_CHUNK_B,
        "CHUNK_C": OUT_CHUNK_C,
        "CHUNK_D": OUT_CHUNK_D,
        "CHUNK_E": OUT_CHUNK_E,
        "CHUNK_F": OUT_CHUNK_F,
        "CHUNK_G": OUT_CHUNK_G,
        "CHUNK_H": OUT_CHUNK_H,
        "CHUNK_I": OUT_CHUNK_I,
        "CHUNK_J": OUT_CHUNK_J,
        "CHUNK_K": OUT_CHUNK_K,
        "CHUNK_L": OUT_CHUNK_L,
        "CHUNK_M": OUT_CHUNK_M,
        "CHUNK_N": OUT_CHUNK_N,
        "CHUNK_O": OUT_CHUNK_O,
        "CHUNK_P": OUT_CHUNK_P,
        "CHUNK_Q": OUT_CHUNK_Q,
        "CHUNK_R": OUT_CHUNK_R,
        "CHUNK_S": OUT_CHUNK_S,
        "CHUNK_T": OUT_CHUNK_T,
        "CHUNK_U": OUT_CHUNK_U,
        # Add new test ground truth
        "TEST_CHUNK_A": TEST_OUT_CHUNK_A,
        "TEST_CHUNK_B": TEST_OUT_CHUNK_B,
        "TEST_CHUNK_C": TEST_OUT_CHUNK_C,
        "TEST_CHUNK_D": TEST_OUT_CHUNK_D,
        "TEST_CHUNK_E": TEST_OUT_CHUNK_E,
        "TEST_CHUNK_F": TEST_OUT_CHUNK_F,
        "TEST_CHUNK_G": TEST_OUT_CHUNK_G,
        "TEST_CHUNK_H": TEST_OUT_CHUNK_H,
        "TEST_CHUNK_I": TEST_OUT_CHUNK_I,
        "TEST_CHUNK_J": TEST_OUT_CHUNK_J
    }
    
    # Results storage
    results = {
        "Rule_Based": defaultdict(list),
        "BioBERT": defaultdict(list),
        "BERT_CONLL03": defaultdict(list)
    }
    
    # Table data for comparison
    table_data = []
    
    # Process each chunk with each model
    for i, (chunk_name, chunk_text) in enumerate(chunks.items()):
        expected_output = ground_truth[chunk_name]
        
        # Get ground truth name
        expected_name = expected_output.get("Patient_Name", "Unknown")
        
        # Process with each model
        for model_name, extractor in {
            "Rule_Based": rule_based_ner,
            "BioBERT": biobert_ner,
            "BERT_CONLL03": bert_name_detector
        }.items():
            # Extract name
            name_accuracy, extracted_name = evaluate_name_extraction(
                chunk_text, expected_name, model_name, extractor
            )
            
            # Store name accuracy
            results[model_name]["Patient_Name_Accuracy"].append(name_accuracy)
            
            # Rule-based NER
            rule_based_prediction = rule_based_ner.extract_entities(chunk_text)
            rule_based_accuracy = calculate_accuracy(rule_based_prediction, expected_output)
            
            # BioBERT NER
            biobert_prediction = biobert_ner.extract_entities(chunk_text)
            biobert_accuracy = calculate_accuracy(biobert_prediction, expected_output)
            
            # BERT Name Detector
            # First check if model is loaded
            if model_name == "BERT_CONLL03":
                if not bert_name_detector.is_loaded:
                    try:
                        bert_name_detector.load_model()
                    except:
                        print("Could not load BERT model, skipping BERT evaluation")
            
            # Only proceed with BERT if model is loaded
            bert_accuracy = None
            if model_name == "BERT_CONLL03" and bert_name_detector.is_loaded:
                # Create a compatible format for the BERT detector output
                # Use extract_name instead of detect_names
                patient_name = bert_name_detector.extract_name(chunk_text)
                bert_prediction = {
                    "Patient_Name": patient_name if patient_name != "Unknown" else None,
                    "Symptoms": biobert_prediction["Symptoms"],  # Use BioBERT for other fields
                    "Diagnosis": biobert_prediction["Diagnosis"],
                    "Treatment": biobert_prediction["Treatment"],
                    "Current_Status": biobert_prediction["Current_Status"],
                    "Prognosis": biobert_prediction["Prognosis"]
                }
                bert_accuracy = calculate_accuracy(bert_prediction, expected_output)
            
            # Store results for other models
            for metric, value in rule_based_accuracy.items():
                results["Rule_Based"][metric].append(value)
            
            for metric, value in biobert_accuracy.items():
                results["BioBERT"][metric].append(value)
            
            if model_name == "BERT_CONLL03" and bert_accuracy:
                for metric, value in bert_accuracy.items():
                    results["BERT_CONLL03"][metric].append(value)
            
            # Add to table data
            row_data = {
                "Chunk": chunk_name,
                "Rule_Based_Accuracy": rule_based_accuracy["Overall_Accuracy"],
                "BioBERT_Accuracy": biobert_accuracy["Overall_Accuracy"],
                "BERT_CONLL03_Accuracy": bert_accuracy["Overall_Accuracy"] if bert_accuracy else "N/A"
            }
            
            if bert_accuracy:
                row_data["BERT_CONLL03_Accuracy"] = bert_accuracy["Overall_Accuracy"]
            else:
                row_data["BERT_CONLL03_Accuracy"] = "N/A"
            
            table_data.append(row_data)
            
            # Print individual chunk results
            print(f"\n--- {chunk_name} Results ---")
            print(f"Ground Truth: {json.dumps(expected_output, indent=2)}")
            print(f"{model_name}: {json.dumps(extracted_name, indent=2)}")
            print(f"Rule-Based: {json.dumps(rule_based_prediction, indent=2)}")
            print(f"BioBERT: {json.dumps(biobert_prediction, indent=2)}")
            if bert_accuracy:
                print(f"BERT_CONLL03: {json.dumps(bert_prediction, indent=2)}")
            print(f"{model_name} Accuracy: {rule_based_accuracy['Overall_Accuracy']:.2f}")
        
        # Add to table data
        table_data[-1]["Name_Accuracy"] = name_accuracy
    
    # Calculate average metrics
    avg_results = {}
    for model, metrics in results.items():
        if metrics:  # Only process if we have results for this model
            avg_results[model] = {}
            for metric, values in metrics.items():
                if values:  # Check if we have values
                    avg_results[model][metric] = sum(values) / len(values)
    
    # Print overall results
    print("\n=== OVERALL MODEL ACCURACY ===")
    for model, metrics in avg_results.items():
        print(f"\n{model} Model:")
        print(f"  Overall Accuracy: {metrics.get('Overall_Accuracy', 'N/A'):.4f}")
        print(f"  Patient Name Accuracy: {metrics.get('Patient_Name_Accuracy', 'N/A'):.4f}")
        print(f"  Symptoms F1: {metrics.get('Symptoms_F1', 'N/A'):.4f}")
        print(f"  Diagnosis Match: {metrics.get('Diagnosis_Match', 'N/A'):.4f}")
        print(f"  Treatment F1: {metrics.get('Treatment_F1', 'N/A'):.4f}")
        print(f"  Status Match: {metrics.get('Status_Match', 'N/A'):.4f}")
        print(f"  Prognosis Match: {metrics.get('Prognosis_Match', 'N/A'):.4f}")
    
    # Determine which model is most accurate overall
    best_model = None
    best_accuracy = -1
    
    for model, metrics in avg_results.items():
        if metrics.get('Overall_Accuracy', 0) > best_accuracy:
            best_model = model
            best_accuracy = metrics.get('Overall_Accuracy', 0)
    
    print(f"\n{best_model} is more accurate overall with accuracy {best_accuracy:.4f}.")
    
    # Detailed comparison by field
    print("\n=== FIELD-BY-FIELD COMPARISON ===")
    fields = ["Patient_Name_Accuracy", "Symptoms_F1", "Diagnosis_Match", "Treatment_F1", "Status_Match", "Prognosis_Match"]
    for field in fields:
        print(f"\n{field}:")
        
        # Get scores for each model
        scores = {}
        for model, metrics in avg_results.items():
            if field in metrics:
                scores[model] = metrics[field]
                print(f"  {model}: {metrics[field]:.4f}")
        
        # Determine best model for this field
        if scores:
            best_model_field = max(scores.items(), key=lambda x: x[1])[0]
            print(f"  {best_model_field} is better at {field}")
    
    # Print comparison table
    print("\n=== MODEL COMPARISON TABLE ===")
    header = f"{'Chunk':<15} | {'Rule-Based':^12} | {'BioBERT':^12}"
    if "BERT_CONLL03" in avg_results:
        header += f" | {'BERT_CONLL03':^12}"
    header += f" | {'Best Model':^15}"
    
    print(header)
    print("-" * (60 + (25 if "BERT_CONLL03" in avg_results else 0)))
    
    for row in table_data:
        line = f"{row['Chunk']:<15} | {row['Rule_Based_Accuracy']:^12.4f} | {row['BioBERT_Accuracy']:^12.4f}"
        if "BERT_CONLL03" in avg_results:
            if row['BERT_CONLL03_Accuracy'] != "N/A":
                line += f" | {row['BERT_CONLL03_Accuracy']:^12.4f}"
            else:
                line += f" | {'N/A':^12}"
        
        # Determine best model(s) for this chunk
        best_accuracy = max(
            row['Rule_Based_Accuracy'],
            row['BioBERT_Accuracy'],
            row['BERT_CONLL03_Accuracy'] if row['BERT_CONLL03_Accuracy'] != "N/A" else 0
        )
        
        best_models = []
        if row['Rule_Based_Accuracy'] == best_accuracy:
            best_models.append("Rule-Based")
        if row['BioBERT_Accuracy'] == best_accuracy:
            best_models.append("BioBERT")
        if row['BERT_CONLL03_Accuracy'] != "N/A" and row['BERT_CONLL03_Accuracy'] == best_accuracy:
            best_models.append("BERT_CONLL03")
        
        best_model = best_models[0] if len(best_models) == 1 else "Tie"
        
        line += f" | {best_model:^15}"
        print(line)
    
    # Count which model performs better on more chunks
    model_counts = defaultdict(int)
    for row in table_data:
        best_accuracy = max(
            row['Rule_Based_Accuracy'],
            row['BioBERT_Accuracy'],
            row['BERT_CONLL03_Accuracy'] if row['BERT_CONLL03_Accuracy'] != "N/A" else 0
        )
        
        if row['Rule_Based_Accuracy'] == best_accuracy:
            model_counts["Rule-Based"] += 1
        if row['BioBERT_Accuracy'] == best_accuracy:
            model_counts["BioBERT"] += 1
        if row['BERT_CONLL03_Accuracy'] != "N/A" and row['BERT_CONLL03_Accuracy'] == best_accuracy:
            model_counts["BERT_CONLL03"] += 1
    
    print("\n=== MODEL PERFORMANCE SUMMARY ===")
    for model, count in model_counts.items():
        print(f"{model} best on {count} chunks")
    
    # Add separate analysis for test chunks
    print("\n=== TEST CHUNKS PERFORMANCE ===")
    test_chunks = [row for row in table_data if row["Chunk"].startswith("TEST_")]
    
    # Calculate average accuracy for test chunks
    test_avg = {
        "Rule_Based": sum(row["Rule_Based_Accuracy"] for row in test_chunks) / len(test_chunks),
        "BioBERT": sum(row["BioBERT_Accuracy"] for row in test_chunks) / len(test_chunks)
    }
    
    if "BERT_CONLL03" in avg_results:
        bert_test_chunks = [row for row in test_chunks if row["BERT_CONLL03_Accuracy"] != "N/A"]
        if bert_test_chunks:
            test_avg["BERT_CONLL03"] = sum(row["BERT_CONLL03_Accuracy"] for row in bert_test_chunks) / len(bert_test_chunks)
    
    print("Average accuracy on test chunks:")
    for model, avg in test_avg.items():
        print(f"  {model}: {avg:.4f}")
    
    # Count model performance on test chunks (separate counts)
    test_model_counts = {
        "Rule-Based": 0,
        "BioBERT": 0,
        "BERT_CONLL03": 0
    }
    
    for row in test_chunks:
        best_accuracy = max(
            row['Rule_Based_Accuracy'],
            row['BioBERT_Accuracy'],
            row['BERT_CONLL03_Accuracy'] if row['BERT_CONLL03_Accuracy'] != "N/A" else 0
        )
        
        if row['Rule_Based_Accuracy'] == best_accuracy:
            test_model_counts["Rule-Based"] += 1
        if row['BioBERT_Accuracy'] == best_accuracy:
            test_model_counts["BioBERT"] += 1
        if row['BERT_CONLL03_Accuracy'] != "N/A" and row['BERT_CONLL03_Accuracy'] == best_accuracy:
            test_model_counts["BERT_CONLL03"] += 1
    
    print("\nModel performance on test chunks (separate counts):")
    for model, count in test_model_counts.items():
        print(f"  {model} best on {count} test chunks ({count/len(test_chunks)*100:.1f}%)")
    
    # Analyze name detection specifically
    print("\n=== NAME DETECTION ANALYSIS ===")
    name_accuracy = {
        "Rule_Based": [results["Rule_Based"]["Patient_Name_Accuracy"][i] for i, row in enumerate(table_data) if row["Chunk"].startswith("TEST_")],
        "BioBERT": [results["BioBERT"]["Patient_Name_Accuracy"][i] for i, row in enumerate(table_data) if row["Chunk"].startswith("TEST_")]
    }
    
    if "BERT_CONLL03" in avg_results:
        name_accuracy["BERT_CONLL03"] = [results["BERT_CONLL03"]["Patient_Name_Accuracy"][i] for i, row in enumerate(table_data) if row["Chunk"].startswith("TEST_")]
    
    print("Name detection accuracy on test chunks:")
    for model, accuracies in name_accuracy.items():
        avg_name_accuracy = sum(accuracies) / len(accuracies) if accuracies else 0
        print(f"  {model}: {avg_name_accuracy:.4f}")

if __name__ == "__main__":
    evaluate_models()
