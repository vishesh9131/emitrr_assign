from transformers import AutoTokenizer, AutoModelForTokenClassification
# from transformers import DataCollatorForTokenClassification, TrainingArguments, Trainer
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
    
    def extract_name(self, text):
        """Extract patient name from text using the fine-tuned model"""
        if self.model is None or self.tokenizer is None:
            return None

        try:
            # Tokenize the input text
            inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
            with torch.no_grad():
                outputs = self.model(**inputs)

            # Get the predicted labels
            predictions = torch.argmax(outputs.logits, dim=2)
            tokens = self.tokenizer.convert_ids_to_tokens(inputs["input_ids"][0])

            # Extract name entities based on the predicted labels
            name_tokens = []
            current_name = []

            for token, pred in zip(tokens, predictions[0]):
                if pred in [self.entity_labels["B-NAME"], self.entity_labels["I-NAME"]]:
                    if token.startswith("##"):
                        if current_name:
                            current_name.append(token[2:])  # Remove '##' from subword tokens
                    else:
                        if current_name:
                            name_tokens.append(" ".join(current_name))
                            current_name = []
                        current_name.append(token)
                else:
                    if current_name:
                        name_tokens.append(" ".join(current_name))
                        current_name = []

            if current_name:
                name_tokens.append(" ".join(current_name))

            # Clean up the extracted names
            cleaned_names = [" ".join(name.split()) for name in name_tokens if name]

            # Return the first valid name found
            return cleaned_names[0] if cleaned_names else None

        except Exception as e:
            print(f"Error in fine-tuned name extraction: {str(e)}")
            return None
    
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
            
            # Clean up person tokens
            cleaned_persons = []
            for person in person_tokens:
                if person not in ["[CLS]", "[SEP]"] and not person.startswith("##"):
                    # Handle special characters in names
                    person = re.sub(r'\s+([\'"\-])\s+', r'\1', person)
                    cleaned_persons.append(person)
            
            # Return the first person found or None
            return cleaned_persons[0] if cleaned_persons else None
        
        except Exception as e:
            print(f"Error in BioBERT name extraction: {str(e)}")
            return None
    
    def _extract_symptoms(self, text):
        """Extract symptoms from text"""
        # Simple rule-based extraction for symptoms
        symptom_patterns = [
            r"(pain|ache|discomfort) in (\w+)",
            r"(headache|migraine|fever|cough|nausea|vomiting|dizziness|fatigue)",
            r"(shortness of breath|chest pain|back pain|stomach pain)",
            r"feeling (tired|dizzy|nauseous|weak)",
            r"(sore|swollen|stiff) (throat|joints|muscles)"
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
    
    def fine_tune(self, training_data, epochs=3, batch_size=8):
        """Fine-tune the model on training data"""
        print("Starting fine-tuning process...")
        
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
        
      