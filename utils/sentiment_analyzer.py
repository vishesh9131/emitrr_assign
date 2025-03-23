import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import re
import numpy as np
from huggingface_hub import try_to_load_from_cache

class MedicalSentimentAnalyzer:
    def __init__(self):
        """Initialize sentiment and intent analyzer for medical conversations with lazy loading"""
        # Set model name but don't load it yet
        self.sentiment_model_name = "distilbert-base-uncased-finetuned-sst-2-english"
        self.tokenizer = None
        self.model = None
        
        # Check if model files are already in cache
        try:
            # Check if model files exist in cache
            model_file = try_to_load_from_cache(self.sentiment_model_name, "model.safetensors")
            config_file = try_to_load_from_cache(self.sentiment_model_name, "config.json")
            
            # If both files exist, mark as pre-downloaded
            self.is_loaded = model_file is not None and config_file is not None
        except:
            self.is_loaded = False
        
        # Define intent patterns
        self.intent_patterns = {
            "Seeking reassurance": [
                r"(?:worried|concerned|anxious|scared|afraid|fear|nervous|stress|distress)",
                r"(?:will I be okay|will I get better|is it serious|is it dangerous|is it normal)",
                r"(?:hope|hopefully|wish|pray|fingers crossed)",
                r"(?:reassure|reassurance|comfort|comforting|relief)",
                r"(?:right\?|correct\?|isn't it\?|is that normal\?|is that common\?)"
            ],
            "Reporting symptoms": [
                r"(?:pain|ache|hurt|hurts|hurting|sore|tender|burning|throbbing)",
                r"(?:feeling|felt|experiencing|having|had|noticed|been having)",
                r"(?:symptom|symptoms|problem|problems|issue|issues|condition)",
                r"(?:started|began|developed|appeared|noticed|observed)",
                r"(?:yesterday|last week|last month|few days|few weeks|recently|lately)"
            ],
            "Expressing concern": [
                r"(?:worried|concerned|anxious|scared|afraid|fear|nervous|stress|distress)",
                r"(?:serious|severe|dangerous|life-threatening|chronic|permanent)",
                r"(?:cancer|tumor|heart attack|stroke|death|fatal)",
                r"(?:family history|runs in the family|genetic|inherited)",
                r"(?:what if|could it be|is it possible)"
            ],
            "Seeking information": [
                r"(?:what|how|why|when|where|who|which)",
                r"(?:cause|causes|reason|reasons|explanation|explain)",
                r"(?:treatment|medication|medicine|drug|therapy|option|options)",
                r"(?:recommend|suggestion|advise|advice)",
                r"(?:mean|means|meaning|definition|define)"
            ],
            "Discussing treatment": [
                r"(?:treatment|medication|medicine|drug|therapy|option|options)",
                r"(?:surgery|operation|procedure|intervention)",
                r"(?:side effect|side effects|adverse effect|adverse effects|reaction|reactions)",
                r"(?:take|taking|took|prescribed|prescription|dose|dosage)",
                r"(?:work|works|working|effective|effectiveness|efficacy)"
            ]
        }
        
        # Define sentiment keywords
        self.sentiment_keywords = {
            "Anxious": [
                "worried", "concerned", "anxious", "scared", "afraid", "fear", "nervous", 
                "stress", "distress", "panic", "terrified", "frightened", "uneasy", 
                "apprehensive", "dread", "alarmed", "troubled", "disturbed", "tense",
                "what if", "could it be", "is it serious", "is it dangerous", "is it bad"
            ],
            "Neutral": [
                "okay", "fine", "alright", "understand", "understood", "see", "know", 
                "think", "thought", "believe", "feel", "felt", "experiencing", "having", 
                "had", "noticed", "been having", "started", "began", "developed"
            ],
            "Reassured": [
                "better", "improving", "improved", "relief", "relieved", "comfortable", 
                "comforted", "reassured", "confident", "hopeful", "optimistic", "positive", 
                "encouraged", "relaxed", "calm", "calmer", "at ease", "good", "great", 
                "excellent", "wonderful", "fantastic", "thank you", "thanks", "appreciate"
            ]
        }

    def load_model(self):
        """Load the model only when needed"""
        if not self.is_loaded:
            try:
                print("Loading sentiment analysis model... This may take a moment.")
                self.tokenizer = AutoTokenizer.from_pretrained(self.sentiment_model_name)
                self.model = AutoModelForSequenceClassification.from_pretrained(self.sentiment_model_name)
                self.is_loaded = True
                print("Sentiment analysis model loaded successfully.")
                return True
            except Exception as e:
                print(f"Error loading sentiment analysis model: {str(e)}")
                return False
        return True

    def extract_patient_text(self, conversation):
        """Extract only the patient's dialogue from the conversation"""
        patient_lines = []
        lines = conversation.split('\n')
        
        for line in lines:
            if line.strip().startswith("Patient:"):
                # Remove the "Patient:" prefix and add to patient lines
                patient_text = line.strip()[8:].strip()
                if patient_text:
                    patient_lines.append(patient_text)
        
        return " ".join(patient_lines)

    def analyze_sentiment(self, text):
        """Analyze sentiment using transformer model and rule-based approach"""
        # Extract only patient's dialogue
        patient_text = self.extract_patient_text(text)
        if not patient_text:
            patient_text = text  # Use full text if patient dialogue can't be extracted
        
        # Try transformer-based approach if model is loaded or can be loaded
        transformer_sentiment = None
        if self.load_model():
            try:
                transformer_sentiment = self._analyze_sentiment_with_transformer(patient_text)
            except Exception as e:
                print(f"Error in transformer sentiment analysis: {str(e)}")
        
        # Rule-based sentiment analysis
        rule_based_sentiment = self._analyze_sentiment_with_rules(patient_text)
        
        # Combine results, preferring transformer if available
        final_sentiment = transformer_sentiment if transformer_sentiment else rule_based_sentiment
        
        # Analyze intent
        intent = self._analyze_intent(patient_text)
        
        return {
            "Sentiment": final_sentiment,
            "Intent": intent
        }
    
    def _analyze_sentiment_with_transformer(self, text):
        """Analyze sentiment using transformer model"""
        # Tokenize text
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
        
        # Get model predictions
        with torch.no_grad():
            outputs = self.model(**inputs)
            predictions = outputs.logits
        
        # Convert raw logits to probabilities
        probs = torch.nn.functional.softmax(predictions, dim=1)
        
        # SST-2 is binary (positive/negative), map to our categories
        negative_prob = probs[0][0].item()
        positive_prob = probs[0][1].item()
        
        # Map to our three categories
        if negative_prob > 0.7:
            return "Anxious"
        elif positive_prob > 0.7:
            return "Reassured"
        else:
            return "Neutral"
    
    def _analyze_sentiment_with_rules(self, text):
        """Analyze sentiment using rule-based approach"""
        text_lower = text.lower()
        
        # Count occurrences of sentiment keywords
        sentiment_scores = {sentiment: 0 for sentiment in self.sentiment_keywords}
        
        for sentiment, keywords in self.sentiment_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    # Count occurrences and weight them
                    count = text_lower.count(keyword)
                    sentiment_scores[sentiment] += count
        
        # Apply some domain-specific rules
        if "thank you" in text_lower or "thanks" in text_lower:
            sentiment_scores["Reassured"] += 2
        
        if "worried" in text_lower or "concerned" in text_lower:
            sentiment_scores["Anxious"] += 2
        
        if "?" in text:
            sentiment_scores["Anxious"] += 1
        
        # Determine the dominant sentiment
        max_sentiment = max(sentiment_scores.items(), key=lambda x: x[1])
        
        # If no clear sentiment or all scores are 0, return Neutral
        if max_sentiment[1] == 0:
            return "Neutral"
        
        return max_sentiment[0]
    
    def _analyze_intent(self, text):
        """Analyze patient intent using rule-based approach"""
        text_lower = text.lower()
        
        # Count matches for each intent
        intent_scores = {intent: 0 for intent in self.intent_patterns}
        
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                matches = re.findall(pattern, text_lower, re.IGNORECASE)
                intent_scores[intent] += len(matches)
        
        # Apply some domain-specific rules
        if "?" in text:
            intent_scores["Seeking information"] += 1
            
        if "pain" in text_lower or "hurt" in text_lower:
            intent_scores["Reporting symptoms"] += 1
            
        if "worried" in text_lower or "concerned" in text_lower:
            intent_scores["Expressing concern"] += 1
            
        if "will I be okay" in text_lower or "is it serious" in text_lower:
            intent_scores["Seeking reassurance"] += 2
        
        # Determine the dominant intent
        max_intent = max(intent_scores.items(), key=lambda x: x[1])
        
        # If no clear intent or all scores are 0, return a default
        if max_intent[1] == 0:
            return "General discussion"
        
        return max_intent[0] 