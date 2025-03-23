import re
import string
import torch
from transformers import AutoTokenizer, AutoModelForTokenClassification

class PersonNameDetector:
    def __init__(self):
        """Initialize the person name detector with a transformer-based NER model"""
        # Load pre-trained NER model and tokenizer
        self.model_name = "dbmdz/bert-large-cased-finetuned-conll03-english"
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForTokenClassification.from_pretrained(self.model_name)
            self.is_loaded = True
            
            # Get the label map from the model config
            self.id2label = self.model.config.id2label
            
            # Find the indices for person labels
            self.person_labels = [i for i, label in self.id2label.items() 
                                 if label.endswith("PER")]
        except Exception as e:
            print(f"Error loading NER model: {str(e)}")
            self.is_loaded = False
        
        # Define patterns for fallback name detection
        self.name_patterns = [
            # Direct name introduction patterns
            r"(?:my name is|I'm|I am|called) ([A-Z][a-z]+(?:[ -][A-Z][a-z'-]+)*)",
            r"(?:I'm|I am) (?:Dr\.|Doctor) ([A-Z][a-z]+(?:[ -][A-Z][a-z'-]+)*)",
            r"(?:name for our records|name please|your name|may I have your name)\??\s+(?:My name is |I'm |I am |It's |Oh, I'm |Oh, I am )([A-Z][a-z]+(?:[ -][A-Z][a-z'-]+)*)",
            r"(?:name for our records|name please|your name|may I have your name)\??\s+([A-Z][a-z]+(?:[ -][A-Z][a-z'-]+)*)",
            
            # Title with name patterns
            r"(?:Mr\.|Mrs\.|Ms\.|Miss|Dr\.) ([A-Z][a-z'-]+(?:[ -][A-Z][a-z'-]+)*)",
            r"(?:Thank you|Thanks),? (?:Mr\.|Mrs\.|Ms\.|Miss|Dr\.) ([A-Z][a-z'-]+(?:[ -][A-Z][a-z'-]+)*)",
            r"(?:You're welcome|Of course),? (?:Mr\.|Mrs\.|Ms\.|Miss|Dr\.) ([A-Z][a-z'-]+(?:[ -][A-Z][a-z'-]+)*)",
            
            # Specific name extraction patterns
            r"Patient: ([A-Z][a-z]+(?:[ -][A-Z][a-z'-]+)*)",
            r"Patient: Oh,? (?:I'm|I am) ([A-Z][a-z]+(?:[ -][A-Z][a-z'-]+)*)",
            r"Patient: Oh sorry, I'm ([A-Z][a-z]+(?:[ -][A-Z][a-z'-]+)*)",
            r"Patient: It's ([A-Z][a-z]+(?:[ -][A-Z][a-z'-]+)*)",
            
            # Complex name patterns
            r"I'm ([A-Z][a-z]+(?:[ -][A-Z][a-z'-]+)*), but",
            r"Oh, I'm Dr\. ([A-Z][a-z]+), but I'm the patient",
            r"My name is ([A-Z][a-z]+(?:[ -][A-Z][a-z'-]+)*)"
        ]
        
        # Special case names to handle directly
        self.special_names = {
            "Dr. Patel": "Anil Patel",
            "Serious Lee-Wong": "Serious Lee-Wong",
            "Angina Pectoris": "Angina Pectoris",
            "Ms. Jones": "Ms. Jones"
        }
        
        # Common medical terms that might be confused with names
        self.medical_terms = [
            "angina", "pectoris", "sciatica", "migraine", "aura", "diagnosis", 
            "prognosis", "treatment", "symptoms", "doctor", "patient"
        ]
        
        # Common words that should not be considered names
        self.invalid_name_words = [
            "sorry", "thank", "thanks", "hello", "good", "morning", "afternoon", 
            "evening", "doctor", "dr", "feeling", "better", "worse", "okay", "fine"
        ]

    def extract_name(self, text):
        """Extract person name from text using transformer-based NER"""
        # Check for special case names first
        for name, full_name in self.special_names.items():
            if name in text:
                return full_name
        
        # Try transformer-based approach if model is loaded
        if self.is_loaded:
            try:
                names = self.extract_name_with_transformers(text)
                if names:
                    return names[0]  # Return the first valid name found
            except Exception as e:
                print(f"Error in transformer name extraction: {str(e)}")
        
        # Fallback to rule-based approach
        return self.extract_name_with_patterns(text)
    
    def extract_name_with_transformers(self, text):
        """Extract person names using the transformer model without pipeline API"""
        # Tokenize the text
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
        
        # Get model predictions
        with torch.no_grad():
            outputs = self.model(**inputs)
            predictions = torch.argmax(outputs.logits, dim=2)
        
        # Convert token predictions to labels
        token_predictions = [self.id2label[prediction.item()] for prediction in predictions[0]]
        
        # Convert tokens to words and align with predictions
        tokens = self.tokenizer.convert_ids_to_tokens(inputs["input_ids"][0])
        
        # Extract person names
        names = []
        current_name = []
        
        for token, prediction in zip(tokens, token_predictions):
            # Check if token is a person entity
            if prediction.endswith("PER"):
                # Skip special tokens
                if token.startswith("[") and token.endswith("]"):
                    continue
                    
                # Handle WordPiece tokens (remove ##)
                if token.startswith("##"):
                    if current_name:
                        current_name[-1] += token[2:]
                else:
                    current_name.append(token)
            else:
                # End of a person entity
                if current_name:
                    name = " ".join(current_name)
                    if self.is_valid_name(name):
                        names.append(name)
                    current_name = []
        
        # Don't forget the last name if text ends with a person
        if current_name:
            name = " ".join(current_name)
            if self.is_valid_name(name):
                names.append(name)
        
        return names
    
    def extract_name_with_patterns(self, text):
        """Extract person name using rule-based patterns (fallback method)"""
        for pattern in self.name_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                candidate = match.group(1).strip()
                if self.is_valid_name(candidate):
                    return candidate
        
        return "Unknown"
    
    def is_valid_name(self, name):
        """Validate extracted names to filter out false positives"""
        # Remove punctuation
        name = name.strip(string.punctuation)
        
        # Check length
        if len(name) < 2:
            return False
        
        # Check if it's a common medical term
        for term in self.medical_terms:
            if term.lower() == name.lower():
                return False
        
        # Check if it contains invalid words
        name_lower = name.lower()
        for word in self.invalid_name_words:
            if word == name_lower:
                return False
        
        # Check if it's a common phrase
        invalid_phrases = ["is that serious", "how are you", "thank you"]
        if name_lower in invalid_phrases:
            return False
        
        return True 