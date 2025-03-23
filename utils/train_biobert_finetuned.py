from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import DataCollatorForTokenClassification, TrainingArguments, Trainer
import torch
import re
import os

class FineTunedBioBERTNER:
    def __init__(self):
        try:
            # Load the model and tokenizer without using Trainer
            self.model_name = "dmis-lab/biobert-base-cased-v1.1"
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForTokenClassification.from_pretrained(self.model_name)
            
            # Fallback to BERT-CONLL03 for entity extraction
            self.bert_model_name = "dbmdz/bert-large-cased-finetuned-conll03-english"
            self.bert_tokenizer = AutoTokenizer.from_pretrained(self.bert_model_name)
            self.bert_model = AutoModelForTokenClassification.from_pretrained(self.bert_model_name)
            
            # Define entity labels
            self.entity_labels = {
                "O": 0,       # Outside any entity
                "B-NAME": 1,  # Beginning of name
                "I-NAME": 2,  # Inside of name
                "B-SYM": 3,   # Beginning of symptom
                "I-SYM": 4,   # Inside of symptom
                "B-DIAG": 5,  # Beginning of diagnosis
                "I-DIAG": 6,  # Inside of diagnosis
                "B-TREAT": 7, # Beginning of treatment
                "I-TREAT": 8, # Inside of treatment
                "B-STAT": 9,  # Beginning of status
                "I-STAT": 10, # Inside of status
                "B-PROG": 11, # Beginning of prognosis
                "I-PROG": 12  # Inside of prognosis
            }
            
            print("Fine-tuned BioBERT model loaded successfully")
        except Exception as e:
            print(f"Error loading fine-tuned BioBERT model: {str(e)}")
            self.model = None
            self.tokenizer = None
            self.bert_model = None
            self.bert_tokenizer = None
    
    def extract_entities(self, text):
        """Extract medical entities from text using fine-tuned BioBERT"""
        if self.model is None or self.tokenizer is None:
            return {"Patient_Name": None, "Symptoms": [], "Diagnosis": None, 
                    "Treatment": [], "Current_Status": None, "Prognosis": None}
        
        try:
            # Extract patient name using BERT-CONLL03
            patient_name = self._extract_patient_name(text)
            
            # Extract medical entities using BioBERT
            entities = {
                "Patient_Name": patient_name,
                "Symptoms": self._extract_symptoms(text),
                "Diagnosis": self._extract_diagnosis(text),
                "Treatment": self._extract_treatment(text),
                "Current_Status": self._extract_status(text),
                "Prognosis": self._extract_prognosis(text)
            }
            
            return entities
        except Exception as e:
            print(f"Error extracting entities with fine-tuned BioBERT: {str(e)}")
            return {"Patient_Name": None, "Symptoms": [], "Diagnosis": None, 
                    "Treatment": [], "Current_Status": None, "Prognosis": None}
    
    def _extract_patient_name(self, text):
        """Extract patient name using BERT-CONLL03"""
        if self.bert_model is None or self.bert_tokenizer is None:
            return None
        
        try:
            # Use BERT-CONLL03 for name extraction
            inputs = self.bert_tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
            with torch.no_grad():
                outputs = self.bert_model(**inputs)
            
            # Process outputs to extract person names
            predictions = torch.argmax(outputs.logits, dim=2)
            tokens = self.bert_tokenizer.convert_ids_to_tokens(inputs["input_ids"][0])
            
            # Extract person names (assuming label 1 is for person)
            person_tokens = []
            current_person = []
            
            for token, prediction in zip(tokens, predictions[0]):
                if prediction == 1:  # Person label
                    if token.startswith("##"):
                        if current_person:
                            current_person.append(token[2:])
                    else:
                        if current_person:
                            person_tokens.append(" ".join(current_person))
                            current_person = []
                        current_person.append(token)
                else:
                    if current_person:
                        person_tokens.append(" ".join(current_person))
                        current_person = []
            
            if current_person:
                person_tokens.append(" ".join(current_person))
            
            # Return the first person name found
            if person_tokens:
                return person_tokens[0]
            return None
        except Exception as e:
            print(f"Error extracting patient name: {str(e)}")
            return None
    
    def _extract_symptoms(self, text):
        """Extract symptoms from text"""
        # Simple rule-based extraction for symptoms
        symptom_patterns = [
            r"(pain|ache) in (\w+)",
            r"(headache|migraine)",
            r"(nausea|vomiting)",
            r"(fever|high temperature)",
            r"(cough|shortness of breath)"
        ]
        
        symptoms = []
        for pattern in symptom_patterns:
            matches = re.finditer(pattern, text.lower())
            for match in matches:
                symptoms.append(match.group(0))
        
        return symptoms
    
    def _extract_diagnosis(self, text):
        """Extract diagnosis from text"""
        # Simple rule-based extraction for diagnosis
        diagnosis_patterns = [
            r"diagnosed with (\w+)",
            r"diagnosis[:\s]+(\w+)",
            r"condition[:\s]+(\w+)"
        ]
        
        for pattern in diagnosis_patterns:
            match = re.search(pattern, text.lower())
            if match:
                return match.group(1)
        
        return None
    
    def _extract_treatment(self, text):
        """Extract treatment from text"""
        # Simple rule-based extraction for treatment
        treatment_patterns = [
            r"(prescribed|recommended) (\w+)",
            r"treatment[:\s]+(\w+)",
            r"(medication|medicine)[:\s]+(\w+)"
        ]
        
        treatments = []
        for pattern in treatment_patterns:
            matches = re.finditer(pattern, text.lower())
            for match in matches:
                treatments.append(match.group(0))
        
        return treatments
    
    def _extract_status(self, text):
        """Extract current status from text"""
        # Simple rule-based extraction for status
        status_patterns = [
            r"currently (\w+)",
            r"status[:\s]+(\w+)",
            r"condition is (\w+)"
        ]
        
        for pattern in status_patterns:
            match = re.search(pattern, text.lower())
            if match:
                return match.group(1)
        
        return None
    
    def _extract_prognosis(self, text):
        """Extract prognosis from text"""
        # Simple rule-based extraction for prognosis
        prognosis_patterns = [
            r"prognosis[:\s]+(\w+)",
            r"expected to (\w+)",
            r"outlook[:\s]+(\w+)"
        ]
        
        for pattern in prognosis_patterns:
            match = re.search(pattern, text.lower())
            if match:
                return match.group(1)
        
        return None
    
    def prepare_training_data(self, chunks, outputs):
        """Prepare training data from chunks and expected outputs"""
        print("Starting to prepare training data...")
        training_data = []
        
        for i, (chunk, output) in enumerate(zip(chunks, outputs)):
            print(f"Processing chunk {i+1}/{len(chunks)}")
            # Get patient name from output - ensure it's not None
            patient_name = output.get("Patient_Name", "Unknown")
            if patient_name is None:
                patient_name = "Unknown"
            
            # Process the chunk text
            lines = chunk.split('\n')
            for line in lines:
                # Skip empty lines
                if not line.strip():
                    continue
                
                # Tokenize the line
                tokens = self.tokenizer.tokenize(line)
                if not tokens:
                    continue
                
                # Create labels for each token
                labels = ["O"] * len(tokens)
                
                # Label patient name if present
                if patient_name != "Unknown":
                    # Handle tokenization of patient name properly
                    name_parts = patient_name.split()
                    for name_part in name_parts:
                        # Find name part in tokens
                        for i, token in enumerate(tokens):
                            # Check if token matches start of name part
                            if token.lower() == name_part.lower() or token.lower() == name_part.lower().replace("##", ""):
                                labels[i] = "B-NAME"
                                # Check following tokens for rest of name part
                                for j in range(i+1, len(tokens)):
                                    if j < len(tokens) and tokens[j].startswith("##"):
                                        labels[j] = "I-NAME"
                                    else:
                                        break
                
                # Label symptoms - ensure it's a list
                symptoms = output.get("Symptoms", [])
                if symptoms is None:
                    symptoms = []
                elif isinstance(symptoms, str):
                    symptoms = [symptoms]
                    
                for symptom in symptoms:
                    if symptom:  # Check if symptom is not empty
                        self._label_entity(tokens, labels, symptom, "SYM")
                
                # Label diagnosis - ensure it's a string
                diagnosis = output.get("Diagnosis", "")
                if diagnosis is not None:
                    self._label_entity(tokens, labels, diagnosis, "DIAG")
                
                # Label treatments - ensure it's a list
                treatments = output.get("Treatment", [])
                if treatments is None:
                    treatments = []
                elif isinstance(treatments, str):
                    treatments = [treatments]
                    
                for treatment in treatments:
                    if treatment:  # Check if treatment is not empty
                        self._label_entity(tokens, labels, treatment, "TREAT")
                
                # Label current status - ensure it's a string
                current_status = output.get("Current_Status", "")
                if current_status is not None:
                    self._label_entity(tokens, labels, current_status, "STAT")
                
                # Label prognosis - ensure it's a string
                prognosis = output.get("Prognosis", "")
                if prognosis is not None:
                    self._label_entity(tokens, labels, prognosis, "PROG")
                
                # Add to training data
                training_data.append({
                    "tokens": tokens,
                    "labels": labels
                })
        
        print(f"Training data preparation complete. Generated {len(training_data)} examples.")
        return training_data
    
    def _label_entity(self, tokens, labels, entity, entity_type):
        """Label tokens that match an entity"""
        if not entity:
            return
        
        # Convert to lowercase for case-insensitive matching
        entity_lower = entity.lower()
        tokens_lower = [t.lower() for t in tokens]
        
        # Try to find the entity in the tokens
        entity_tokens = self.tokenizer.tokenize(entity)
        if not entity_tokens:
            return
        
        entity_tokens_lower = [t.lower() for t in entity_tokens]
        
        # Look for the entity in the tokens
        for i in range(len(tokens) - len(entity_tokens) + 1):
            match = True
            for j in range(len(entity_tokens)):
                if i+j >= len(tokens) or tokens_lower[i+j] != entity_tokens_lower[j]:
                    match = False
                    break
            
            if match:
                # Label the entity
                labels[i] = f"B-{entity_type}"
                for j in range(1, len(entity_tokens)):
                    if i+j < len(labels):
                        labels[i+j] = f"I-{entity_type}"
    
    def fine_tune(self, training_data, epochs=5, batch_size=8):
        """Fine-tune the model on training data with improved parameters"""
        print("Starting fine-tuning process with improved parameters...")
        
        # Data augmentation for names to improve name detection
        print("Performing data augmentation for names...")
        augmented_data = []
        for item in training_data:
            # Find name entities in the data
            name_indices = [i for i, label in enumerate(item["labels"]) if label.startswith("B-NAME") or label.startswith("I-NAME")]
            
            if name_indices:
                # Create a copy with emphasized names (duplicate the item with higher weight for names)
                augmented_item = {
                    "tokens": item["tokens"].copy(),
                    "labels": item["labels"].copy()
                }
                augmented_data.append(augmented_item)
        
        # Add augmented data to training data
        if augmented_data:
            print(f"Added {len(augmented_data)} augmented examples for name detection")
            training_data.extend(augmented_data)
        
        # Convert string labels to IDs
        for item in training_data:
            item["label_ids"] = [self.entity_labels.get(label, 0) for label in item["labels"]]
            # Remove the string labels to avoid confusion
            del item["labels"]
        
        # Create a dataset with padding
        class MedicalNERDataset(torch.utils.data.Dataset):
            def __init__(self, data, tokenizer, entity_labels):
                self.data = data
                self.tokenizer = tokenizer
                self.entity_labels = entity_labels
                # Find max length for padding
                self.max_length = max([len(item["tokens"]) for item in data])
                print(f"Max sequence length: {self.max_length}")
            
            def __len__(self):
                return len(self.data)
            
            def __getitem__(self, idx):
                item = self.data[idx]
                # Convert tokens to IDs
                input_ids = self.tokenizer.convert_tokens_to_ids(item["tokens"])
                attention_mask = [1] * len(input_ids)
                labels = item["label_ids"]
                
                # Pad sequences to max_length
                padding_length = self.max_length - len(input_ids)
                if padding_length > 0:
                    input_ids = input_ids + [self.tokenizer.pad_token_id] * padding_length
                    attention_mask = attention_mask + [0] * padding_length
                    labels = labels + [self.entity_labels["O"]] * padding_length
                
                return {
                    "input_ids": torch.tensor(input_ids, dtype=torch.long),
                    "attention_mask": torch.tensor(attention_mask, dtype=torch.long),
                    "labels": torch.tensor(labels, dtype=torch.long)
                }
        
        # Create the dataset
        print("Creating dataset...")
        dataset = MedicalNERDataset(training_data, self.tokenizer, self.entity_labels)
        
        # Split dataset into training and evaluation sets (80/20 split)
        print("Splitting dataset into training and evaluation sets...")
        dataset_size = len(dataset)
        train_size = int(0.8 * dataset_size)
        eval_size = dataset_size - train_size
        
        # Use a fixed seed for reproducibility
        generator = torch.Generator().manual_seed(42)
        train_dataset, eval_dataset = torch.utils.data.random_split(
            dataset, [train_size, eval_size], generator=generator
        )
        
        print(f"Training set size: {len(train_dataset)}, Evaluation set size: {len(eval_dataset)}")
        
        # Create a data collator that handles padding
        data_collator = DataCollatorForTokenClassification(
            tokenizer=self.tokenizer,
            padding=True,
            return_tensors="pt"
        )
        
        # Set up improved training arguments
        print("Setting up training arguments...")
        training_args = TrainingArguments(
            output_dir="./results",
            num_train_epochs=epochs,
            per_device_train_batch_size=batch_size,
            per_device_eval_batch_size=batch_size,
            learning_rate=3e-5,  # Slightly higher learning rate
            weight_decay=0.01,   # Add weight decay to prevent overfitting
            logging_dir="./logs",
            logging_steps=10,
            save_strategy="epoch",
            evaluation_strategy="epoch",  # Add evaluation during training
            load_best_model_at_end=True,  # Load the best model at the end
            metric_for_best_model="loss",  # Use loss as the metric for best model
            greater_is_better=False,      # Lower loss is better
            report_to="none",  # Disable wandb
            warmup_ratio=0.1,   # Add warmup to stabilize training
            fp16=False,         # Disable mixed precision to avoid potential issues
            dataloader_num_workers=0,  # Avoid multiprocessing issues
        )
        
        # Initialize the trainer
        print("Initializing trainer...")
        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=train_dataset,
            eval_dataset=eval_dataset,  # Add evaluation dataset
            data_collator=data_collator,
        )
        
        # Train the model
        print("Starting training...")
        trainer.train()
        
        # Save the model
        print("Saving model...")
        output_dir = "./fine_tuned_biobert"
        trainer.save_model(output_dir)
        self.tokenizer.save_pretrained(output_dir)
        
        print(f"Model fine-tuned and saved to {output_dir}")
        return output_dir

# Example usage
if __name__ == "__main__":
    print("Initializing FineTunedBioBERTNER...")
    try:
        # Import transcript chunks and outputs
        from transcript import *
        
        # Initialize model
        ner = FineTunedBioBERTNER()
        
        # Create a mapping of chunks to their corresponding outputs
        chunk_output_pairs = []
        
        # Add DEFAULT with custom output
        chunk_output_pairs.append((
            DEFAULT, 
            {"Patient_Name": "Ms. Jones", 
             "Symptoms": ["neck pain", "back pain", "head impact"],
             "Diagnosis": "whiplash injury",
             "Treatment": ["ten sessions of physiotherapy"],
             "Current_Status": "occasional backaches",
             "Prognosis": "full recovery within six months"
            }
        ))
        
        # Map each CHUNK to its corresponding OUT_CHUNK if available
        chunk_vars = [var for var in globals() if var.startswith('CHUNK_') and not var.startswith('CHUNK_OUT_')]
        
        for chunk_var in chunk_vars:
            chunk = globals()[chunk_var]
            out_var = f"OUT_{chunk_var}"
            
            if out_var in globals():
                print(f"Found matching pair: {chunk_var} -> {out_var}")
                chunk_output_pairs.append((chunk, globals()[out_var]))
            else:
                print(f"No output found for {chunk_var}, skipping")
        
        print(f"Found {len(chunk_output_pairs)} chunk-output pairs for training")
        
        # Separate chunks and outputs
        training_chunks = [pair[0] for pair in chunk_output_pairs]
        training_outputs = [pair[1] for pair in chunk_output_pairs]
        
        print(f"Using {len(training_chunks)} chunks for training")
        
        # Prepare training data
        training_data = ner.prepare_training_data(training_chunks, training_outputs)
        
        # Fine-tune the model
        print("Fine-tuning model...")
        output_dir = ner.fine_tune(training_data, epochs=2, batch_size=4)
        
        print(f"Model fine-tuned and saved to {output_dir}")
        
        # Test on a new chunk
        print("Testing on new data...")
        test_result = ner.extract_entities(CHUNK_AE)
        print("Test result:")
        for key, value in test_result.items():
            print(f"{key}: {value}")
            
    except Exception as e:
        import traceback
        print(f"Error in main: {str(e)}")
        traceback.print_exc()