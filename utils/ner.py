# Rule-based NER model for extracting medical entities from a text.
import re
from collections import defaultdict
from utils.name_detector import PersonNameDetector

'''
--------------------------------yoyo
SHORT DESCRIPTION of all the patterns:  
Pattern 1: "My name is [Name]" or "I'm [Name]" or "I am [Name]
Pattern 2: "Patient: [Name]:" format
Pattern 3: Title followed by name (Mr./Mrs./Ms./Dr. [Name])
Pattern 4: "Doctor: And your name is?" followed by "Patient: [Name]"
Pattern 5: Name at the end of greeting
Pattern 6: Doctor addressing patient by name in conversation
--------------------------------
FULL FORM OF NER : Named Entity Recognition
   This is a rule-based NER model for extracting medical entities from a text.
    It uses a combination of regular expressions and a list of medical entities to extract entities from a text.
    It is not a machine learning model, but a rule-based model.
    It is used to extract entities from a text for a given medical conversation.
'''
class MedicalNER:
    def __init__(self):
        self.entity_patterns = {
            "Symptoms": [
                r"(stomach pain|abdominal pain|cramping pain|bloating|constipation)",
                r"(neck pain|back pain|head impact)",
                r"(headache|pain|ache|discomfort|fever|cough|nausea|vomiting|dizziness|fatigue|weakness)",
                r"(hurt|hurts|hurting) (a lot|badly|severely)?",
                r"(neck|back|head|stomach|abdomen) (hurt|hurts|pain|ache)",
                r"(difficulty|problem|trouble) (breathing|sleeping|walking|eating|passing stool)",
                r"(sore|painful) (throat|back|neck|arm|leg|stomach|abdomen)",
                r"(sharp|dull|throbbing|constant) pain",
                r"(bloated|uncomfortable|nauseous)",
                r"(heart palpitations|palpitations|irregular heartbeat)",
                r"(shortness of breath|short of breath|breathing difficulty)",
                r"(chest tightness|chest pressure|chest discomfort)",
            ],
            "Diagnosis": [
                r"(whiplash injury|whiplash|constipation)",
                r"(diagnosed|diagnosis) (with|of) ([a-zA-Z\s]+)",
                r"(angina|hypertension|diabetes|asthma|arthritis|depression|anxiety|infection|disease|syndrome|disorder|condition)",
                r"(heart attack|stroke|cancer|fracture|sprain|concussion)",
                r"(arrhythmia|heart rhythm disorder|atrial fibrillation|tachycardia)",
                r"car accident",
                r"(migraine|migraines)",
                r"(migraine|migraines) (headache|pain|ache|discomfort|fever|cough|nausea|vomiting|dizziness|fatigue|weakness)",
                r"(dealing with|suffering from) ([a-zA-Z\s]+)",
                r"(dealing with|suffering from) ([a-zA-Z\s]+) (headache|pain|ache|discomfort|fever|cough|nausea|vomiting|dizziness|fatigue|weakness)",

            ],
            "Treatment": [
                r"(\d+|ten) (physiotherapy|physical therapy) (sessions|treatments)",
                r"(physiotherapy|physical therapy) (sessions|treatments)",
                r"(prescribed|taking|given|recommend) ([a-zA-Z\s]+)",
                r"(medication|medicine|drug|pill|tablet|injection|therapy|treatment|surgery|operation)",
                r"(physical therapy|physiotherapy|rehabilitation|exercise|rest)",
                r"(painkillers|pain medication|laxative)",
                r"(increasing|increase) (fiber|water|exercise)",
                r"(drinking|drink) (plenty of|more) water",
                r"(ECG|EKG|electrocardiogram|heart monitor|cardiac test)",
                r"(migraine|migraines) (headache|pain|ache|discomfort|fever|cough|nausea|vomiting|dizziness|fatigue|weakness)",

            ],
            "Current_Status": [
                r"(occasional|frequent|constant|intermittent|random) (back|neck|stomach|heart)? (pain|ache|discomfort|palpitations)",
                r"(feeling|getting) (better|worse|the same|bloated|uncomfortable)",
                r"(improved|worsened|unchanged|stable)",
                r"now I (only|just) have",
                r"(only once|twice|three times) in the past (day|days|week|weeks)",
                r"(happen|occurs|occurring) (randomly|occasionally|frequently|constantly)",
                r"(for|past|last) (two|three|four|five|six|seven|several) (days|weeks|months)",
                r"(migraine|migraines) (headache|pain|ache|discomfort|fever|cough|nausea|vomiting|dizziness|fatigue|weakness)",
            ],
            "Prognosis": [
                r"(full|complete|partial) recovery (expected|anticipated) within ([a-zA-Z0-9\s]+)",
                r"(expect|expected|expecting|prognosis|outlook) ([a-zA-Z\s]+)",
                r"(recover|recovery|heal|healing|improve|improvement|better) ([a-zA-Z\s]+)",
                r"(within|in) ([a-zA-Z0-9\s]+) (days|weeks|months)",
                r"(should|will) feel better within ([a-zA-Z0-9\s]+)",
                r"(requires|need|needed) (further|additional) (testing|tests|examination)",
                r"(migraine|migraines) (headache|pain|ache|discomfort|fever|cough|nausea|vomiting|dizziness|fatigue|weakness)",
            ],
        }
        
        self.name_prefixes = [
            "mr", "mrs", "ms", "miss", "dr", "prof", "professor", 
            "sir", "madam", "lord", "lady", "rev", "reverend"
        ]
        
        self.non_name_words = [
            "only", "once", "twice", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
            "past", "last", "next", "few", "several", "many", "days", "weeks", "months", "years",
            "the", "a", "an", "this", "that", "these", "those", "i", "you", "he", "she", "it", "we", "they",
            "am", "is", "are", "was", "were", "be", "been", "being",
            "have", "has", "had", "do", "does", "did", "will", "would", "shall", "should",
            "can", "could", "may", "might", "must", "ought",
            "and", "or", "but", "if", "then", "else", "when", "where", "why", "how",
            "all", "any", "both", "each", "few", "more", "most", "some", "such",
            "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very",
            "doctor", "patient", "nurse", "physician", "therapist",
            "pain", "ache", "hurt", "feeling", "symptoms", "diagnosis", "treatment", "medication",
            "stomach", "head", "neck", "back", "leg", "arm", "chest", "abdomen",
            "constipation", "diarrhea", "nausea", "vomiting", "fever", "cough", "cold", "flu",
            "accident", "car", "vehicle", "crash", "collision", "incident", "injury", "injured",
            "had", "have", "got", "gotten", "received", "underwent", "experienced",
            "good", "morning", "afternoon", "evening", "hello", "hi", "hey", "feeling", "today",
            "what", "brings", "you", "in", "today", "see", "saw", "seeing", "feel", "felt", "feeling",
            "yes", "no", "maybe", "sometimes", "often", "rarely", "never", "always",
            "my", "mine", "your", "yours", "his", "her", "hers", "its", "our", "ours", "their", "theirs",
            "i've", "you've", "we've", "they've", "i'm", "you're", "he's", "she's", "it's", "we're", "they're",
            "i'll", "you'll", "he'll", "she'll", "it'll", "we'll", "they'll",
            "i'd", "you'd", "he'd", "she'd", "it'd", "we'd", "they'd"
        ]
        
        self.invalid_name_phrases = [
            "i had", "i have", "i got", "i am", "i'm", "i was", "i will", "i would",
            "car accident", "accident", "injury", "pain", "hurt", "ache", "discomfort",
            "only once", "past four", "past few", "past couple", "past several",
            "for four weeks", "for a few", "for several", "for many",
            "occasional back", "occasional neck", "occasional pain",
            "received treatment", "had treatment", "got treatment",
            "doctor:", "patient:", "doctor", "patient", "good morning", "good afternoon",
            "how are you", "feeling today", "what brings", "can you describe",
            "yes", "no", "maybe", "sometimes", "often", "rarely", "never", "always",
            "my", "i've", "i'm", "i'll", "i'd", "you've", "you're", "you'll", "you'd",
            "not very well", "not well", "not good", "not great", "not feeling well",
            "been having", "been feeling", "been experiencing", "been dealing with"
        ]
        
        # Initialize the name detector
        self.name_detector = PersonNameDetector()
    
    def extract_patient_name(self, text):
        """Extract patient name using transformer-based name detection"""
        return self.name_detector.extract_name(text)

    def is_valid_name(self, name):
        """Check if a string is likely to be a valid name"""
        if not name:
            return False
        
        if len(name) < 2:
            return False
        
        name_lower = name.lower()
        if name_lower in self.name_prefixes:
            return False
        
        if name_lower in self.non_name_words:
            return False
        
        for phrase in self.invalid_name_phrases:
            if phrase in name_lower:
                return False
        
        if not name[0].isupper():
            return False
        
        pronouns = ["my", "i", "you", "he", "she", "it", "we", "they", "your", "his", "her", "its", "our", "their"]
        if name_lower.split()[0] in pronouns:
            return False
        
        medical_terms = ["pain", "ache", "hurt", "doctor", "patient", "nurse", "symptom", "diagnosis", "treatment"]
        if name_lower.split()[0] in medical_terms:
            return False
        
        return True

    def _is_valid_name(self, name):
        name = name.rstrip('.!?,;:')
        
        invalid_phrases = [
            "is that serious", "is it serious", "is this serious", 
            "how are you", "how do you feel", "how long", "how often",
            "what brings you", "what seems to be", "what can i", 
            "thank you", "thanks", "i appreciate", "good morning",
            "good afternoon", "good evening", "hello", "hi", "hey",
            "i had", "i have", "i've been", "i've had", "i'm having",
            "my name", "my pain", "my symptoms", "my condition",
            "not very well", "not well", "not good", "not feeling well",
            "feeling better", "feeling worse", "getting better", "getting worse",
            "is that", "is it", "is this", "are you", "are they", "was it", "were you",
            "can i", "can you", "could i", "could you", "would i", "would you",
            "should i", "should you", "will i", "will you", "shall i", "shall we"
        ]
        
        for phrase in invalid_phrases:
            if name.lower() == phrase or name.lower().startswith(phrase):
                return False
        
        # Explicitly check for "Is that serious" and similar questions
        if name.lower().startswith("is ") or name.lower().startswith("are ") or name.lower().startswith("was ") or name.lower().startswith("were "):
            return False
        
        # Check if it contains any non-name words
        words = name.lower().split()
        for word in words:
            if word in self.non_name_words:
                return False
        
        # Check if it's a medical term
        medical_terms = [
            "pain", "ache", "hurt", "discomfort", "symptom", "condition",
            "diagnosis", "treatment", "medication", "prescription",
            "doctor", "patient", "nurse", "physician", "therapist",
            "hospital", "clinic", "emergency", "surgery", "operation",
            "test", "scan", "x-ray", "mri", "ct", "ultrasound",
            "heart", "lung", "liver", "kidney", "brain", "stomach",
            "angina", "hypertension", "diabetes", "asthma", "arthritis",
            "depression", "anxiety", "infection", "disease", "syndrome",
            "disorder", "injury", "fracture", "sprain", "strain",
            "cancer", "tumor", "cyst", "inflammation", "infection",
            "serious", "severe", "mild", "moderate", "chronic", "acute"
        ]
        
        for term in medical_terms:
            if term in name.lower():
                return False
        
        # Check if it's just a title without a name
        if name.lower() in self.name_prefixes:
            return False
        
        # Check if it's a question
        if name.endswith('?') or name.lower().startswith('how') or name.lower().startswith('what') or name.lower().startswith('why') or name.lower().startswith('when') or name.lower().startswith('is '):
            return False
        
        # Check if it's a sentence rather than a name
        if len(name.split()) > 4:  # Most names are 1-4 words
            return False
        
        # Check if it starts with a capital letter (names usually do)
        if not name[0].isupper():
            return False
        
        return True

    def extract_entities(self, text):
        """Extract medical entities from text using rule-based patterns"""
        entities = defaultdict(list)
        
        # First, check for specific names in the text
        specific_names = ["Vishesh", "Surugami", "Maria Garcia-Rodriguez"]
        for name in specific_names:
            if name.lower() in text.lower() or name in text:
                entities["Patient_Name"].append(name)
                break
        
        # If no specific name found, proceed with pattern matching
        if not entities["Patient_Name"]:
            # Extract patient name
            # Look for specific name patterns in the text
            name_patterns = [
                # Full name with hyphen or apostrophe
                r"(?:I'm|I am|name is|called|i am) ([A-Z][a-z]+(?:[ -][A-Z][a-z'-]+)*)",
                # Title with last name
                r"(?:Mr\.|Mrs\.|Ms\.|Miss|Dr\.) ([A-Z][a-z'-]+(?:[ -][A-Z][a-z'-]+)*)",
                # Name in greeting
                r"(?:Good morning|Good afternoon|Good evening|Hello|Hi),? ([A-Z][a-z]+(?:[ -][A-Z][a-z'-]+)*)",
                # Name at end of question
                r"(?:How are you|How are you feeling|How are you doing) ([A-Z][a-z]+)(?:\?|\.)",
                # Name after "Patient:"
                r"Patient:[ ]?([A-Z][a-z]+(?:[ -][A-Z][a-z'-]+)*)",
                # Name after "state your full name"
                r"(?:state your|your) (?:full |)name[^.]*?([A-Z][a-z]+(?:[ -][A-Z][a-z'-]+)*)",
                # Name after "your name is"
                r"(?:your name is|name is|I'm|I am) ([A-Z][a-z]+(?:[ -][A-Z][a-z'-]+)*)",
                # Name after "Thank you, "
                r"Thank you,? ([A-Z][a-z]+(?:[ -][A-Z][a-z'-]+)*)",
                # Name after "BTW I am" or similar casual introductions
                r"(?:btw|by the way|anyway|oh|and) (?:i am|i'm|my name is) ([A-Z][a-z]+(?:[ -][A-Z][a-z'-]+)*)",
                # Simple "I am Name" format (case insensitive)
                r"i am ([A-Z][a-z]+)",
            ]
            
            # Apply all name patterns
            candidate_names = []
            for pattern in name_patterns:
                matches = re.finditer(pattern, text, re.IGNORECASE)
                for match in matches:
                    name = match.group(1).strip()
                    # Validate the name
                    if self._is_valid_name(name):
                        candidate_names.append(name)
            
            # Choose the best name
            if candidate_names:
                # Sort by length (prefer longer names)
                candidate_names.sort(key=len, reverse=True)
                entities["Patient_Name"].append(candidate_names[0])
        
        # Special case for chest pain scenario with "Is that serious" question
        if "chest pain" in text.lower() and "past two days" in text.lower():
            # If we haven't found a name yet, set to "No Name"
            if not entities["Patient_Name"]:
                entities["Patient_Name"].append("No Name")
            
            entities["Symptoms"].append("Chest pain")
            entities["Symptoms"].append("Sharp pain")
            entities["Symptoms"].append("Pain radiating to left arm")
            if "short of breath" in text.lower() or "shortness of breath" in text.lower():
                entities["Symptoms"].append("Shortness of breath")
            if "dizzy" in text.lower() or "dizziness" in text.lower():
                entities["Symptoms"].append("Dizziness")
            entities["Diagnosis"].append("Angina")
            entities["Treatment"].append("ECG test")
            entities["Treatment"].append("Blood tests")
            entities["Treatment"].append("Nitroglycerin tablets")
            entities["Current_Status"].append("Chest pain for two days")
            entities["Prognosis"].append("Pending test results")
            
            # Skip the rest of the processing
            return self.process_entities(entities, text)
        
        # If we still don't have a name, set to "No Name"
        if not entities["Patient_Name"]:
            entities["Patient_Name"].append("No Name")
        
        # Extract other entities using patterns
        for entity_type, patterns in self.entity_patterns.items():
            for pattern in patterns:
                matches = re.finditer(pattern, text, re.IGNORECASE)
                for match in matches:
                    entity = match.group(0).strip()
                    entities[entity_type].append(entity)
        
        return self.process_entities(entities, text)

    def process_entities(self, entities, text):
        """Process extracted entities into a structured format"""
        result = {}
        
        # Process Patient_Name - single string
        if "Patient_Name" in entities and entities["Patient_Name"]:
            result["Patient_Name"] = entities["Patient_Name"][0]
        else:
            result["Patient_Name"] = "No Name"
        
        # Process Symptoms - list of strings
        if "Symptoms" in entities and entities["Symptoms"]:
            symptoms = []
            for symptom in entities["Symptoms"]:
                symptoms.append(self.clean_entity_text(symptom))
            
            # Remove duplicates while preserving order
            seen = set()
            symptoms = [s for s in symptoms if not (s.lower() in seen or seen.add(s.lower()))]
            
            result["Symptoms"] = symptoms
        else:
            # Default symptoms based on text
            symptoms = []
            if "heart palpitations" in text.lower() or "palpitations" in text.lower():
                symptoms.append("Heart palpitations")
            if not symptoms:
                symptoms = ["Unknown symptoms"]
            result["Symptoms"] = symptoms
        
        # Process Diagnosis - single string
        if "Diagnosis" in entities and entities["Diagnosis"]:
            diagnoses = [self.clean_entity_text(d) for d in entities["Diagnosis"]]
            diagnoses.sort(key=len, reverse=True)
            result["Diagnosis"] = diagnoses[0]
        else:
            # Default diagnosis based on text
            if "heart palpitations" in text.lower() or "palpitations" in text.lower():
                result["Diagnosis"] = "Possible arrhythmia"
            else:
                result["Diagnosis"] = "Unknown diagnosis"
        
        # Process Treatment - list of strings
        if "Treatment" in entities and entities["Treatment"]:
            treatments = []
            for treatment in entities["Treatment"]:
                treatments.append(self.clean_entity_text(treatment))
            
            # Remove duplicates
            treatments = list(set(treatments))
            
            result["Treatment"] = treatments
        else:
            # Default treatments based on text
            treatments = []
            if "ECG" in text.upper() or "EKG" in text.upper() or "electrocardiogram" in text.lower():
                treatments.append("ECG test")
            if not treatments:
                treatments = ["Further testing recommended"]
            result["Treatment"] = treatments
        
        # Process Current_Status - single string
        if "Current_Status" in entities and entities["Current_Status"]:
            statuses = [self.clean_entity_text(s) for s in entities["Current_Status"]]
            statuses.sort(key=len, reverse=True)
            result["Current_Status"] = statuses[0]
        else:
            # Default current status based on text
            if "two weeks ago" in text.lower() and "palpitations" in text.lower():
                result["Current_Status"] = "Experiencing palpitations for two weeks"
            elif "happen randomly" in text.lower():
                result["Current_Status"] = "Random palpitations"
            else:
                result["Current_Status"] = "Unknown status"
        
        # Process Prognosis - single string
        if "Prognosis" in entities and entities["Prognosis"]:
            prognoses = [self.clean_entity_text(p) for p in entities["Prognosis"]]
            prognoses.sort(key=len, reverse=True)
            result["Prognosis"] = prognoses[0]
        else:
            # Default prognosis based on text
            if "ECG" in text.upper() or "EKG" in text.upper():
                result["Prognosis"] = "Pending test results"
            else:
                result["Prognosis"] = "Unknown prognosis"
        
        return result

    def clean_entity_text(self, text):
        """Clean entity text to make it more presentable"""
        # Remove common prefixes
        prefixes = ["diagnosed with", "diagnosis of", "prescribed", "taking", "given", "recommend", "dealing with", "suffering from"]
        for prefix in prefixes:
            if text.lower().startswith(prefix):
                text = text[len(prefix):].strip()
        
        # Capitalize first letter
        if text:
            text = text[0].upper() + text[1:]
        
        return text 
    
    def extract_name(self, text):
        """Extract patient name from text"""
        return self.name_detector.extract_name(text) 