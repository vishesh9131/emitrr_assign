import json
from collections import defaultdict
import re


from utils.ner import MedicalNER
from utils.biobert_ner import BioBERTNER
from utils.bert_name_detector import BERTNameDetector
from utils.biobert_finetuned import FineTunedBioBERTNER

from transcript import *
def calculate_accuracy(predicted, ground_truth):
    """
    Calculate accuracy metrics for NER predictions
    Returns overall accuracy (float)
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
    
    # Return a dictionary with all metrics
    return {
        "overall": overall_accuracy,
        "name": 1.0 if name_correct else 0.0,
        "symptoms_f1": symptoms_f1,
        "diagnosis": diagnosis_match,
        "treatment_f1": treatment_f1,
        "status": status_match,
        "prognosis": prognosis_match
    }

def evaluate_name_extraction(text, expected_name, model_name, model):
    """Evaluate name extraction accuracy for a given model"""
    try:
        # Use the correct method for each model
        if model_name == "Rule_Based":
            extracted_name = model.extract_name(text)
        elif model_name == "BioBERT":
            extracted_name = model.extract_name(text)
        elif model_name == "BERT_CONLL03":
            extracted_name = model.extract_name(text)
        elif model_name == "FineTuned_BioBERT":
            extracted_name = model.extract_name(text)
        else:
            extracted_name = None
            
        print(f"{model_name} Name: {extracted_name}")
        
        # Calculate accuracy
        if expected_name is None:
            # If no name is expected, accuracy is 1.0 if no name is extracted
            accuracy = 1.0 if extracted_name is None else 0.0
        elif extracted_name is None:
            # If a name is expected but none is extracted, accuracy is 0.0
            accuracy = 0.0
        else:
            # Simple string matching for now
            accuracy = 1.0 if expected_name.lower() in extracted_name.lower() or extracted_name.lower() in expected_name.lower() else 0.0
        
        return accuracy, extracted_name
    except Exception as e:
        print(f"Error in {model_name} name extraction: {str(e)}")
        return 0.0, None

def normalize_name(name):
    """Normalize name for comparison by removing punctuation and standardizing spacing"""
    if not name:
        return ""
    
    # Replace hyphens and apostrophes with spaces
    name = name.replace("-", " ").replace("'", " ")
    
    # Remove other punctuation
    name = re.sub(r'[^\w\s]', '', name)
    
    # Standardize spacing
    name = re.sub(r'\s+', ' ', name).strip().lower()
    
    return name

def create_ground_truth_file():
    """Create ground truth JSON file from transcript data"""
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
    
    with open("ground_truth.json", "w") as f:
        json.dump(ground_truth, f, indent=2)
    
    return ground_truth

def evaluate_models():
    # Create ground truth file if it doesn't exist
    try:
        with open("ground_truth.json", "r") as f:
            ground_truth = json.load(f)
    except FileNotFoundError:
        print("Ground truth file not found. Creating it...")
        ground_truth = create_ground_truth_file()
    
    # Initialize models
    rule_based_ner = MedicalNER()
    biobert_ner = BioBERTNER()
    bert_name_detector = BERTNameDetector()
    
    # Initialize fine-tuned BioBERT model
    try:
        # Use the base model instead of trying to load from a local path
        fine_tuned_biobert = FineTunedBioBERTNER()
        fine_tuned_loaded = True
        print("Fine-tuned BioBERT model loaded successfully")
    except Exception as e:
        print(f"Error loading fine-tuned BioBERT model: {str(e)}")
        fine_tuned_loaded = False
    
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
    
    # Initialize results dictionary
    results = {
        "Rule_Based": defaultdict(list),
        "BioBERT": defaultdict(list),
        "BERT_CONLL03": defaultdict(list),
        "FineTuned_BioBERT": defaultdict(list)
    }
    
    # Initialize table data for comparison
    table_data = []
    
    # Process each chunk with each model
    for chunk_name, chunk_text in chunks.items():
        expected_output = ground_truth[chunk_name]
        
        # Get ground truth name
        expected_name = expected_output.get("Patient_Name", "Unknown")
        
        # Create a row for this chunk
        row_data = {"Chunk": chunk_name}
        
        # Process with Rule-Based model
        rule_based_name_accuracy, rule_based_extracted_name = evaluate_name_extraction(
            chunk_text, expected_name, "Rule_Based", rule_based_ner
        )
        results["Rule_Based"]["Patient_Name_Accuracy"].append(rule_based_name_accuracy)
        
        # Rule-based NER
        rule_based_prediction = rule_based_ner.extract_entities(chunk_text)
        rule_based_accuracy = calculate_accuracy(rule_based_prediction, expected_output)
        
        # Store results for Rule-Based
        for metric, value in rule_based_accuracy.items():
            results["Rule_Based"][metric].append(value)
        
        row_data["Rule_Based_Accuracy"] = rule_based_accuracy["overall"]
        
        # Process with BioBERT model
        biobert_name_accuracy, biobert_extracted_name = evaluate_name_extraction(
            chunk_text, expected_name, "BioBERT", biobert_ner
        )
        results["BioBERT"]["Patient_Name_Accuracy"].append(biobert_name_accuracy)
        
        # BioBERT NER
        biobert_prediction = biobert_ner.extract_entities(chunk_text)
        biobert_accuracy = calculate_accuracy(biobert_prediction, expected_output)
        
        # Store results for BioBERT
        for metric, value in biobert_accuracy.items():
            results["BioBERT"][metric].append(value)
        
        row_data["BioBERT_Accuracy"] = biobert_accuracy["overall"]
        
        # Process with Fine-tuned BioBERT model if loaded
        if fine_tuned_loaded:
            try:
                # Use the same extract_name method as BioBERT for consistency
                fine_tuned_name_accuracy, fine_tuned_extracted_name = evaluate_name_extraction(
                    chunk_text, expected_name, "FineTuned_BioBERT", fine_tuned_biobert
                )
                results["FineTuned_BioBERT"]["Patient_Name_Accuracy"].append(fine_tuned_name_accuracy)
                
                # Fine-tuned BioBERT NER
                fine_tuned_prediction = fine_tuned_biobert.extract_entities(chunk_text)  # Use fine_tuned_biobert instead of biobert_ner
                fine_tuned_accuracy = calculate_accuracy(fine_tuned_prediction, expected_output)
                
                # Store results for Fine-tuned BioBERT
                for metric, value in fine_tuned_accuracy.items():
                    results["FineTuned_BioBERT"][metric].append(value)
                
                row_data["FineTuned_BioBERT_Accuracy"] = fine_tuned_accuracy["overall"]
            except Exception as e:
                print(f"Error processing chunk {chunk_name} with Fine-tuned BioBERT: {str(e)}")
                row_data["FineTuned_BioBERT_Accuracy"] = "N/A"
        else:
            row_data["FineTuned_BioBERT_Accuracy"] = "N/A"
        
        # Process with BERT_CONLL03 model
        # First check if model is loaded
        if not bert_name_detector.is_loaded:
            try:
                bert_name_detector.load_model()
            except:
                print("Could not load BERT model, skipping BERT evaluation")
        
        # Only proceed with BERT if model is loaded
        if bert_name_detector.is_loaded:
            bert_name_accuracy, bert_extracted_name = evaluate_name_extraction(
                chunk_text, expected_name, "BERT_CONLL03", bert_name_detector
            )
            results["BERT_CONLL03"]["Patient_Name_Accuracy"].append(bert_name_accuracy)
            
            # Create a compatible format for the BERT detector output
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
            
            # Store results for BERT_CONLL03
            for metric, value in bert_accuracy.items():
                results["BERT_CONLL03"][metric].append(value)
            
            row_data["BERT_CONLL03_Accuracy"] = bert_accuracy["overall"]
        else:
            row_data["BERT_CONLL03_Accuracy"] = "N/A"
        
        # Add to table data
        table_data.append(row_data)
        
        # Print individual chunk results
        print(f"\n--- {chunk_name} Results ---")
        print(f"Ground Truth: {json.dumps(expected_output, indent=2)}")
        print(f"Rule-Based Name: {rule_based_extracted_name}")
        print(f"BioBERT Name: {biobert_extracted_name}")
        if bert_name_detector.is_loaded:
            print(f"BERT_CONLL03 Name: {bert_extracted_name}")
        print(f"Rule-Based Accuracy: {rule_based_accuracy['overall']:.2f}")
        print(f"BioBERT Accuracy: {biobert_accuracy['overall']:.2f}")
        if bert_name_detector.is_loaded:
            print(f"BERT_CONLL03 Accuracy: {bert_accuracy['overall']:.2f}")
    
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
        print(f"  Overall Accuracy: {metrics.get('overall', 'N/A'):.4f}")
        print(f"  Patient Name Accuracy: {metrics.get('name', 'N/A'):.4f}")
        print(f"  Symptoms F1: {metrics.get('symptoms_f1', 'N/A'):.4f}")
        print(f"  Diagnosis Match: {metrics.get('diagnosis', 'N/A'):.4f}")
        print(f"  Treatment F1: {metrics.get('treatment_f1', 'N/A'):.4f}")
        print(f"  Status Match: {metrics.get('status', 'N/A'):.4f}")
        print(f"  Prognosis Match: {metrics.get('prognosis', 'N/A'):.4f}")
    
    # Determine which model is most accurate overall
    best_model = None
    best_accuracy = -1
    
    for model, metrics in avg_results.items():
        if metrics.get('overall', 0) > best_accuracy:
            best_model = model
            best_accuracy = metrics.get('overall', 0)
    
    print(f"\n{best_model} is more accurate overall with accuracy {best_accuracy:.4f}.")
    
    # Detailed comparison by field
    print("\n=== FIELD-BY-FIELD COMPARISON ===")
    fields = ["Patient_Name_Accuracy", "symptoms_f1", "diagnosis", "treatment_f1", "status", "prognosis"]
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
    if fine_tuned_loaded:
        header += f" | {'FineTuned':^12}"
    if "BERT_CONLL03" in avg_results:
        header += f" | {'BERT_CONLL03':^12}"
    header += f" | {'Best Model':^15}"
    
    print(header)
    print("-" * (60 + (25 if "BERT_CONLL03" in avg_results else 0) + (15 if fine_tuned_loaded else 0)))
    
    for row in table_data:
        line = f"{row['Chunk']:<15} | {row['Rule_Based_Accuracy']:^12.4f} | {row['BioBERT_Accuracy']:^12.4f}"
        
        if fine_tuned_loaded:
            if row['FineTuned_BioBERT_Accuracy'] != "N/A":
                line += f" | {row['FineTuned_BioBERT_Accuracy']:^12.4f}"
            else:
                line += f" | {'N/A':^12}"
        
        if "BERT_CONLL03" in avg_results:
            if row['BERT_CONLL03_Accuracy'] != "N/A":
                line += f" | {row['BERT_CONLL03_Accuracy']:^12.4f}"
            else:
                line += f" | {'N/A':^12}"
        
        # Determine best model(s) for this chunk
        best_accuracy = max(
            row['Rule_Based_Accuracy'],
            row['BioBERT_Accuracy'],
            row['FineTuned_BioBERT_Accuracy'] if fine_tuned_loaded and row['FineTuned_BioBERT_Accuracy'] != "N/A" else 0,
            row['BERT_CONLL03_Accuracy'] if row['BERT_CONLL03_Accuracy'] != "N/A" else 0
        )
        
        best_models = []
        if row['Rule_Based_Accuracy'] == best_accuracy:
            best_models.append("Rule-Based")
        if row['BioBERT_Accuracy'] == best_accuracy:
            best_models.append("BioBERT")
        if fine_tuned_loaded and row['FineTuned_BioBERT_Accuracy'] != "N/A" and row['FineTuned_BioBERT_Accuracy'] == best_accuracy:
            best_models.append("FineTuned")
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
            row['FineTuned_BioBERT_Accuracy'] if fine_tuned_loaded and row['FineTuned_BioBERT_Accuracy'] != "N/A" else 0,
            row['BERT_CONLL03_Accuracy'] if row['BERT_CONLL03_Accuracy'] != "N/A" else 0
        )
        
        if row['Rule_Based_Accuracy'] == best_accuracy:
            model_counts["Rule-Based"] += 1
        if row['BioBERT_Accuracy'] == best_accuracy:
            model_counts["BioBERT"] += 1
        if fine_tuned_loaded and row['FineTuned_BioBERT_Accuracy'] != "N/A" and row['FineTuned_BioBERT_Accuracy'] == best_accuracy:
            model_counts["FineTuned_BioBERT"] += 1
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
        "Rule-Based": sum(row["Rule_Based_Accuracy"] for row in test_chunks) / len(test_chunks),
        "BioBERT": sum(row["BioBERT_Accuracy"] for row in test_chunks) / len(test_chunks)
    }
    
    if "BERT_CONLL03" in avg_results:
        bert_test_chunks = [row for row in test_chunks if row["BERT_CONLL03_Accuracy"] != "N/A"]
        if bert_test_chunks:
            test_avg["BERT_CONLL03"] = sum(row["BERT_CONLL03_Accuracy"] for row in bert_test_chunks) / len(bert_test_chunks)
    
    print("Average accuracy on test chunks:")
    for model, avg in test_avg.items():
        print(f"  {model}: {avg:.4f}")
    
    # Initialize test model counts with all possible model names
    test_model_counts = {
        "Rule-Based": 0,
        "BioBERT": 0,
        "FineTuned_BioBERT": 0,
        "BERT_CONLL03": 0
    }
    
    for row in test_chunks:
        best_accuracy = max(
            row['Rule_Based_Accuracy'],
            row['BioBERT_Accuracy'],
            row['FineTuned_BioBERT_Accuracy'] if fine_tuned_loaded and row['FineTuned_BioBERT_Accuracy'] != "N/A" else 0,
            row['BERT_CONLL03_Accuracy'] if row['BERT_CONLL03_Accuracy'] != "N/A" else 0
        )
        
        if row['Rule_Based_Accuracy'] == best_accuracy:
            test_model_counts["Rule-Based"] += 1
        if row['BioBERT_Accuracy'] == best_accuracy:
            test_model_counts["BioBERT"] += 1
        if row['FineTuned_BioBERT_Accuracy'] != "N/A" and row['FineTuned_BioBERT_Accuracy'] == best_accuracy:
            test_model_counts["FineTuned_BioBERT"] += 1
        if row['BERT_CONLL03_Accuracy'] != "N/A" and row['BERT_CONLL03_Accuracy'] == best_accuracy:
            test_model_counts["BERT_CONLL03"] += 1
    
    print("\nModel performance on test chunks (separate counts):")
    for model, count in test_model_counts.items():
        print(f"  {model} best on {count} test chunks ({count/len(test_chunks)*100:.1f}%)")
    
    # Analyze name detection specifically
    print("\n=== NAME DETECTION ANALYSIS ===")
    
    # Get name accuracy for test chunks
    test_name_accuracy = {
        "Rule-Based": [],
        "BioBERT": [],
        "BERT_CONLL03": [],
        "FineTuned_BioBERT": []
    }
    
    for i, row in enumerate(table_data):
        if row["Chunk"].startswith("TEST_"):
            chunk_index = list(chunks.keys()).index(row["Chunk"])
            
            if chunk_index < len(results["Rule_Based"]["Patient_Name_Accuracy"]):
                test_name_accuracy["Rule-Based"].append(results["Rule_Based"]["Patient_Name_Accuracy"][chunk_index])
            
            if chunk_index < len(results["BioBERT"]["Patient_Name_Accuracy"]):
                test_name_accuracy["BioBERT"].append(results["BioBERT"]["Patient_Name_Accuracy"][chunk_index])
            
            if "BERT_CONLL03" in results and chunk_index < len(results["BERT_CONLL03"]["Patient_Name_Accuracy"]):
                test_name_accuracy["BERT_CONLL03"].append(results["BERT_CONLL03"]["Patient_Name_Accuracy"][chunk_index])
            
            if fine_tuned_loaded and chunk_index < len(results["FineTuned_BioBERT"]["Patient_Name_Accuracy"]):
                test_name_accuracy["FineTuned_BioBERT"].append(results["FineTuned_BioBERT"]["Patient_Name_Accuracy"][chunk_index])
    
    print("Name detection accuracy on test chunks:")
    for model, accuracies in test_name_accuracy.items():
        if accuracies:
            avg_name_accuracy = sum(accuracies) / len(accuracies)
            print(f"  {model}: {avg_name_accuracy:.4f}")
        else:
            print(f"  {model}: No data available")

if __name__ == "__main__":
    evaluate_models()
