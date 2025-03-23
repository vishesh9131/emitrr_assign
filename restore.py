# import streamlit as st
# import json
# from utils.ner import MedicalNER
# from utils.summarization import MedicalSummarizer
# from utils.keyword import MedicalKeywordExtractor
# from transcript import *
# # Set page config
# st.set_page_config(
#     page_title="Physician Notetaker",
#     page_icon="🩺",
#     layout="wide"
# )

# # Initialize models
# @st.cache_resource
# def load_models():
#     try:
#         ner = MedicalNER()
#         summarizer = MedicalSummarizer()
#         keyword_extractor = MedicalKeywordExtractor()
#         return ner, summarizer, keyword_extractor
#     except Exception as e:
#         st.error(f"Error loading models: {str(e)}")
#         return None, None, None

# ner, summarizer, keyword_extractor = load_models()

# # App title
# st.title("🩺 Physician Notetaker")
# st.subheader("Medical NLP Summarization")

# # Sample data
# sample_transcript = DEFAULT

# # Text area for input
# transcript = st.text_area("Enter medical conversation transcript:", value=sample_transcript, height=300)

# # Process button
# if st.button("Process Transcript"):
#     with st.spinner("Processing..."):
#         # Extract entities
#         entities = ner.extract_entities(transcript)
        
#         # Generate summary
#         summaries = summarizer.summarize(transcript)
        
#         # Extract keywords
#         keywords = keyword_extractor.extract_keywords(transcript)
        
#         # Display results
#         st.subheader("Results")
        
#         # Display in tabs
#         tab1, tab2, tab3 = st.tabs(["Medical Report", "Summary", "Keywords"])
        
#         with tab1:
#             st.subheader("Medical Report")
#             st.json(entities)
        
#         with tab2:
#             st.subheader("Full Summary")
#             st.write(summaries["full"])
            
#             st.subheader("Doctor's Summary")
#             st.write(summaries["doctor"])
            
#             st.subheader("Patient's Summary")
#             st.write(summaries["patient"])
        
#         with tab3:
#             st.subheader("Top Keywords")
#             for kw in keywords:
#                 st.write(f"• {kw['keyword']} (relevance: {kw['relevance']:.2f})")

# # Footer
# st.markdown("---")
# st.markdown("Physician Notetaker - Medical NLP Summarization") 

------------

import re
from collections import defaultdict

class MedicalNER:
    def __init__(self):
        """Initialize the Medical NER model with rule-based patterns"""
        # Define medical entity types we're interested in
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
            ],
            "Diagnosis": [
                r"(whiplash injury|whiplash|constipation)",
                r"(diagnosed|diagnosis) (with|of) ([a-zA-Z\s]+)",
                r"(angina|hypertension|diabetes|asthma|arthritis|depression|anxiety|infection|disease|syndrome|disorder|condition)",
                r"(heart attack|stroke|cancer|fracture|sprain|concussion)",
                r"car accident",
                r"(dealing with|suffering from) ([a-zA-Z\s]+)",
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
            ],
            "Current_Status": [
                r"(occasional|frequent|constant|intermittent) (back|neck|stomach)? (pain|ache|discomfort)",
                r"(feeling|getting) (better|worse|the same|bloated|uncomfortable)",
                r"(improved|worsened|unchanged|stable)",
                r"now I (only|just) have",
                r"(only once|twice|three times) in the past (day|days|week|weeks)",
            ],
            "Prognosis": [
                r"(full|complete|partial) recovery (expected|anticipated) within ([a-zA-Z0-9\s]+)",
                r"(expect|expected|expecting|prognosis|outlook) ([a-zA-Z\s]+)",
                r"(recover|recovery|heal|healing|improve|improvement|better) ([a-zA-Z\s]+)",
                r"(within|in) ([a-zA-Z0-9\s]+) (days|weeks|months)",
                r"(should|will) feel better within ([a-zA-Z0-9\s]+)",
            ],
        }
        
        # Common name prefixes and titles
        self.name_prefixes = [
            "mr", "mrs", "ms", "miss", "dr", "prof", "professor", 
            "sir", "madam", "lord", "lady", "rev", "reverend"
        ]
        
        # Common words that shouldn't be part of names
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
        
        # Phrases that definitely aren't names
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
    
    def extract_patient_name(self, text):
        """Extract patient name using multiple intelligent approaches"""
        # Initialize with default
        patient_name = "No Name"
        
        # Pattern 1: Look for "Patient: Name:" format
        patient_label_pattern = r"Patient:\s*([A-Z][a-z]+\s+[A-Z][a-z]+):"
        patient_label_match = re.search(patient_label_pattern, text)
        if patient_label_match:
            candidate = patient_label_match.group(1).strip()
            if self.is_valid_name(candidate):
                return candidate
        
        # Pattern 2: Look for titles followed by last names
        title_patterns = [
            # Title followed by last name
            r"(Mr|Mrs|Ms|Miss|Dr)\.?\s+([A-Z][a-z]+)",
            r"(Mr|Mrs|Ms|Miss|Dr)\.?\s+([A-Z][a-z]+[\-'][A-Z][a-z]*)",
            
            # Title with full name
            r"(Mr|Mrs|Ms|Miss|Dr)\.?\s+([A-Z][a-z]+)\s+([A-Z][a-z]+)",
            
            # Specific greeting with title and name
            r"(Physician|Doctor):\s*Good\s+(morning|afternoon|evening),\s+(Mr|Mrs|Ms|Miss|Dr)\.?\s+([A-Z][a-z]+)",
            r"(Physician|Doctor):\s*Hello,\s+(Mr|Mrs|Ms|Miss|Dr)\.?\s+([A-Z][a-z]+)",
            r"(Physician|Doctor):\s*Hi,\s+(Mr|Mrs|Ms|Miss|Dr)\.?\s+([A-Z][a-z]+)",
            
            # Farewell with title and name
            r"(Physician|Doctor):\s*.*?take care,\s+(Mr|Mrs|Ms|Miss|Dr)\.?\s+([A-Z][a-z]+)",
            r"(Physician|Doctor):\s*.*?welcome,\s+(Mr|Mrs|Ms|Miss|Dr)\.?\s+([A-Z][a-z]+)",
            r"(Physician|Doctor):\s*You're\s+.*?welcome,\s+(Mr|Mrs|Ms|Miss|Dr)\.?\s+([A-Z][a-z]+)",
        ]
        
        for pattern in title_patterns:
            title_match = re.search(pattern, text, re.IGNORECASE)
            if title_match:
                # Different handling based on pattern
                if "Good" in pattern or "Hello" in pattern or "Hi" in pattern or "take care" in pattern or "welcome" in pattern:
                    if "You're" in pattern:
                        title = title_match.group(3)
                        last_name = title_match.group(4)
                    else:
                        title = title_match.group(3)
                        last_name = title_match.group(4)
                elif "full name" in pattern:
                    title = title_match.group(1)
                    first_name = title_match.group(2)
                    last_name = title_match.group(3)
                    return f"{first_name} {last_name}"
                else:
                    title = title_match.group(1)
                    last_name = title_match.group(2)
                
                # Format the name with the title
                candidate = f"{title}. {last_name}"
                if self.is_valid_name(candidate):
                    return candidate
        
        # Pattern 3: Look for "How are you X" or "Hello X" in doctor's greeting
        greeting_patterns = [
            # Standard greetings with name at end (with or without comma)
            r"Doctor:.*?how are you,?\s+([A-Za-z]+[\-']?[A-Za-z]*)",
            r"Doctor:.*?how are you feeling today,?\s+([A-Za-z]+[\-']?[A-Za-z]*)",
            r"Doctor:.*?how are you doing,?\s+([A-Za-z]+[\-']?[A-Za-z]*)",
            r"Doctor:.*?hello,?\s+([A-Za-z]+[\-']?[A-Za-z]*)",
            r"Doctor:.*?hi,?\s+([A-Za-z]+[\-']?[A-Za-z]*)",
            r"Doctor:.*?good (morning|afternoon|evening),?\s+([A-Za-z]+[\-']?[A-Za-z]*)",
            
            # Greetings with name at beginning
            r"Doctor:.*?([A-Za-z]+[\-']?[A-Za-z]*),\s+how are you",
            r"Doctor:.*?([A-Za-z]+[\-']?[A-Za-z]*),\s+how are you feeling today",
            r"Doctor:.*?([A-Za-z]+[\-']?[A-Za-z]*),\s+how are you doing",
            
            # Welcome greetings
            r"Doctor:.*?welcome,?\s+([A-Za-z]+[\-']?[A-Za-z]*)",
            r"Doctor:.*?nice to see you,?\s+([A-Za-z]+[\-']?[A-Za-z]*)",
            
            # Names at beginning of doctor's line
            r"Doctor:\s*([A-Za-z]+[\-']?[A-Za-z]*),\s+",
        ]
        
        for pattern in greeting_patterns:
            greeting_match = re.search(pattern, text, re.IGNORECASE)
            if greeting_match:
                # Extract the name based on the pattern
                if "good (morning|afternoon|evening)" in pattern:
                    candidate = greeting_match.group(2).strip()
                else:
                    candidate = greeting_match.group(1).strip()
                
                # Remove any trailing punctuation
                candidate = re.sub(r'[.,!?;:]$', '', candidate)
                
                if self.is_valid_name(candidate):
                    return candidate
        
        # Pattern 4: Look for patient introduction
        intro_patterns = [
            r"Patient:.*?My name is ([A-Za-z]+[\-']?[A-Za-z]*(\s+[A-Za-z]+[\-']?[A-Za-z]*)?)",
            r"Patient:.*?I am ([A-Za-z]+[\-']?[A-Za-z]*(\s+[A-Za-z]+[\-']?[A-Za-z]*)?)",
            r"Patient:.*?I'm ([A-Za-z]+[\-']?[A-Za-z]*(\s+[A-Za-z]+[\-']?[A-Za-z]*)?)",
            r"Patient:.*?This is ([A-Za-z]+[\-']?[A-Za-z]*(\s+[A-Za-z]+[\-']?[A-Za-z]*)?)",
            r"Patient:.*?([A-Za-z]+[\-']?[A-Za-z]*(\s+[A-Za-z]+[\-']?[A-Za-z]*)?)\s+here",
        ]
        
        for pattern in intro_patterns:
            intro_match = re.search(pattern, text, re.IGNORECASE)
            if intro_match:
                candidate = intro_match.group(1).strip()
                if self.is_valid_name(candidate):
                    return candidate
        
        # Pattern 5: Fallback - look for capitalized words that might be names
        # This is risky, so we'll be very careful with validation
        lines = text.split('\n')
        for line in lines:
            if line.startswith("Patient:"):
                # Look for capitalized words in the middle of sentences
                words = line.split()
                for i, word in enumerate(words):
                    if i > 1 and word[0].isupper() and len(word) > 1:
                        # Check if it's a valid name
                        candidate = word.strip('.,!?;:()"\'')
                        if self.is_valid_name(candidate):
                            # Double-check it's not part of a common phrase
                            prev_words = ' '.join(words[max(0, i-2):i]).lower()
                            next_words = ' '.join(words[i+1:min(len(words), i+3)]).lower()
                            if not any(phrase in f"{prev_words} {candidate.lower()} {next_words}" 
                                      for phrase in self.invalid_name_phrases):
                                return candidate
        
        return patient_name
    
    def is_valid_name(self, candidate):
        """Check if a candidate string is likely to be a valid name"""
        # Basic validation
        if not candidate or len(candidate) < 2:
            return False
        
        # Check if it's just a title without a name
        if candidate.lower().rstrip('.') in self.name_prefixes:
            return False
        
        # Check if it's a common non-name word
        if candidate.lower() in self.non_name_words:
            return False
        
        # Check if it's a pronoun or common word that shouldn't be a name
        if candidate.lower() in ["i", "me", "my", "mine", "you", "your", "yours", 
                                "he", "him", "his", "she", "her", "hers", "it", "its",
                                "we", "us", "our", "ours", "they", "them", "their", "theirs",
                                "i've", "i'm", "i'll", "i'd"]:
            return False
        
        # Check if it's a medical term or other invalid phrase
        for word in self.non_name_words:
            if candidate.lower() == word:
                return False
        
        # Check for invalid phrases
        for phrase in self.invalid_name_phrases:
            if candidate.lower() == phrase or phrase in candidate.lower():
                return False
        
        # Check for first letter capitalization (names should be capitalized)
        if not candidate[0].isupper():
            return False
        
        return True
    
    def extract_entities(self, text):
        """Extract medical entities from text using rule-based patterns"""
        entities = defaultdict(list)
        
        # Extract patient name
        patient_name = self.extract_patient_name(text)
        entities["Patient_Name"].append(patient_name)
        
        # Extract other entities using patterns
        for entity_type, patterns in self.entity_patterns.items():
            for pattern in patterns:
                matches = re.finditer(pattern, text, re.IGNORECASE)
                for match in matches:
                    # Get the full match
                    entity_text = match.group(0)
                    entities[entity_type].append(entity_text)
        
        return entities
    
    def process_entities(self, text, entities):
        """Process and format extracted entities"""
        result = {}
        
        # Process Patient_Name - single string
        if "Patient_Name" in entities and entities["Patient_Name"]:
            names = [name for name in entities["Patient_Name"] if name != "No Name"]
            if names:
                result["Patient_Name"] = names[0]
            else:
                result["Patient_Name"] = "No Name"
        else:
            result["Patient_Name"] = "No Name"
        
        # Process Symptoms - array of strings
        if "Symptoms" in entities and entities["Symptoms"]:
            symptoms = []
            for symptom in entities["Symptoms"]:
                if "neck pain" in symptom.lower():
                    symptoms.append("Neck pain")
                elif "back pain" in symptom.lower():
                    symptoms.append("Back pain")
                elif "head impact" in symptom.lower() or "hit my head" in text.lower():
                    symptoms.append("Head impact")
                elif "stomach pain" in symptom.lower():
                    symptoms.append("Stomach pain")
                elif "cramping pain" in symptom.lower():
                    symptoms.append("Cramping pain")
                elif "constipation" in symptom.lower():
                    symptoms.append("Constipation")
                elif "bloating" in symptom.lower() or "bloated" in symptom.lower():
                    symptoms.append("Bloating")
                elif "discomfort" in symptom.lower():
                    symptoms.append("Discomfort")
                elif "nausea" in symptom.lower() or "nauseous" in symptom.lower():
                    symptoms.append("Nausea")
                elif "vomiting" in symptom.lower():
                    symptoms.append("Vomiting")
                elif "trouble sleeping" in symptom.lower() or "difficulty sleeping" in text.lower():
                    symptoms.append("Trouble sleeping")
                elif "chest pain" in symptom.lower() or "chest pain" in text.lower():
                    symptoms.append("Chest pain")
                elif "shortness of breath" in symptom.lower() or "short of breath" in text.lower():
                    symptoms.append("Shortness of breath")
                elif "dizziness" in symptom.lower() or "dizzy" in text.lower():
                    symptoms.append("Dizziness")
                elif "pain" in symptom.lower() and "left arm" in text.lower():
                    symptoms.append("Left arm pain")
                elif "difficulty passing stool" in symptom.lower() or "hard and difficult to pass" in text.lower():
                    symptoms.append("Difficulty passing stool")
                elif "hurt a lot" in symptom.lower():
                    if "neck" in text.lower():
                        symptoms.append("Neck pain")
                    if "back" in text.lower():
                        symptoms.append("Back pain")
                elif "back hurt" in symptom.lower():
                    symptoms.append("Back pain")
            
            # Remove duplicates
            symptoms = list(set(symptoms))
            result["Symptoms"] = symptoms
        else:
            # Default symptoms based on text
            symptoms = []
            if "neck pain" in text.lower() or "neck hurt" in text.lower():
                symptoms.append("Neck pain")
            if "back pain" in text.lower() or "back hurt" in text.lower() or "backache" in text.lower():
                symptoms.append("Back pain")
            if "hit my head" in text.lower() or "hit the steering wheel" in text.lower():
                symptoms.append("Head impact")
            if "chest pain" in text.lower():
                symptoms.append("Chest pain")
            if "short of breath" in text.lower() or "shortness of breath" in text.lower():
                symptoms.append("Shortness of breath")
            if "dizzy" in text.lower() or "dizziness" in text.lower():
                symptoms.append("Dizziness")
            if "left arm" in text.lower() and "pain" in text.lower():
                symptoms.append("Left arm pain")
            if not symptoms:
                symptoms = ["Unknown symptoms"]
            result["Symptoms"] = symptoms
        
        # Process Diagnosis - single string
        if "Diagnosis" in entities and entities["Diagnosis"]:
            diagnoses = [self.clean_entity_text(d) for d in entities["Diagnosis"]]
            # Prioritize specific diagnoses
            if any("whiplash" in d.lower() for d in diagnoses):
                result["Diagnosis"] = "Whiplash injury"
            elif any("angina" in d.lower() for d in diagnoses):
                result["Diagnosis"] = "Angina"
            elif any("heart attack" in d.lower() for d in diagnoses):
                result["Diagnosis"] = "Risk of heart attack"
            elif any("constipation" in d.lower() for d in diagnoses):
                result["Diagnosis"] = "Constipation"
            else:
                diagnoses.sort(key=len, reverse=True)
                result["Diagnosis"] = diagnoses[0]
        else:
            # Default diagnosis based on text
            if "car accident" in text.lower() or "whiplash" in text.lower():
                result["Diagnosis"] = "Whiplash injury"
            elif "angina" in text.lower():
                result["Diagnosis"] = "Angina"
            elif "heart attack" in text.lower() or "chest pain" in text.lower():
                result["Diagnosis"] = "Risk of heart attack"
            elif "constipation" in text.lower():
                result["Diagnosis"] = "Constipation"
            else:
                result["Diagnosis"] = "Unknown"
        
        # Process Treatment - ensure it's a simple array of strings
        if "Treatment" in entities and entities["Treatment"]:
            treatments = []
            for treatment in entities["Treatment"]:
                if "physiotherapy" in treatment.lower() or "physical therapy" in treatment.lower():
                    # Extract number if present
                    num_match = re.search(r"(\d+|ten)", treatment, re.IGNORECASE)
                    if num_match:
                        num = num_match.group(1)
                        if num.lower() == "ten":
                            num = "10"
                        treatments.append(f"{num} physiotherapy sessions")
                    else:
                        treatments.append("Physiotherapy sessions")
                elif "fiber" in treatment.lower() or "fibre" in treatment.lower():
                    treatments.append("Increase fiber intake")
                elif "water" in treatment.lower():
                    treatments.append("Drink more water")
                elif "exercise" in treatment.lower():
                    treatments.append("Regular exercise")
                elif "laxative" in treatment.lower():
                    treatments.append("Mild laxative")
                elif "painkiller" in treatment.lower() or "pain medication" in treatment.lower():
                    treatments.append("Painkillers")
                elif "nitroglycerin" in treatment.lower() or "nitro" in treatment.lower():
                    treatments.append("Nitroglycerin tablets")
                else:
                    treatments.append(self.clean_entity_text(treatment))
            
            # Remove duplicates and generic treatments if specific ones exist
            treatments = list(set(treatments))
            if "10 physiotherapy sessions" in treatments and "Physiotherapy sessions" in treatments:
                treatments.remove("Physiotherapy sessions")
            if "Therapy" in treatments and any("physiotherapy" in t.lower() for t in treatments):
                treatments.remove("Therapy")
            if "Treatment" in treatments and len(treatments) > 1:
                treatments.remove("Treatment")
            if "Physiotherapy" in treatments and any("physiotherapy sessions" in t.lower() for t in treatments):
                treatments.remove("Physiotherapy")
            if "Given your progress" in treatments:
                treatments.remove("Given your progress")
            if "Tablet" in treatments and any("nitroglycerin" in t.lower() for t in treatments):
                treatments.remove("Tablet")
                    
            result["Treatment"] = treatments
        else:
            # Default treatments based on text
            treatments = []
            if "ten physiotherapy" in text.lower() or "10 physiotherapy" in text.lower():
                treatments.append("10 physiotherapy sessions")
            elif "physiotherapy" in text.lower():
                treatments.append("Physiotherapy sessions")
            if "painkiller" in text.lower() or "pain medication" in text.lower():
                treatments.append("Painkillers")
            if "nitroglycerin" in text.lower() or "nitro" in text.lower():
                treatments.append("Nitroglycerin tablets")
            if "fiber" in text.lower() or "fibre" in text.lower():
                treatments.append("Increase fiber intake")
            if "water" in text.lower() and "drinking" in text.lower():
                treatments.append("Drink more water")
            if "exercise" in text.lower():
                treatments.append("Regular exercise")
            if "laxative" in text.lower():
                treatments.append("Mild laxative")
            if not treatments:
                treatments = ["Unknown treatment"]
            result["Treatment"] = treatments
        
        # Process Current_Status - single string
        if "Current_Status" in entities and entities["Current_Status"]:
            for status in entities["Current_Status"]:
                if "occasional" in status.lower() and "back" in status.lower():
                    result["Current_Status"] = "Occasional backache"
                    break
            if "Current_Status" not in result:
                statuses = [self.clean_entity_text(s) for s in entities["Current_Status"]]
                statuses.sort(key=len, reverse=True)
                result["Current_Status"] = statuses[0]
        else:
            # Default current status based on text
            if "occasional back" in text.lower() or "occasional backache" in text.lower():
                result["Current_Status"] = "Occasional backache"
            elif "still have some discomfort" in text.lower():
                result["Current_Status"] = "Occasional discomfort"
            elif "chest pain for the past two days" in text.lower():
                result["Current_Status"] = "Ongoing chest pain"
            elif "constipation" in text.lower() and "past four days" in text.lower():
                result["Current_Status"] = "Constipation for four days"
            else:
                result["Current_Status"] = "Unknown status"
        
        # Process Prognosis - single string
        if "Prognosis" in entities and entities["Prognosis"]:
            for prognosis in entities["Prognosis"]:
                if "full recovery" in prognosis.lower() and "six months" in prognosis.lower():
                    result["Prognosis"] = "Full recovery expected within six months"
                    break
            if "Prognosis" not in result:
                prognoses = [self.clean_entity_text(p) for p in entities["Prognosis"]]
                prognoses.sort(key=len, reverse=True)
                result["Prognosis"] = prognoses[0]
        else:
            # Default prognosis based on text
            if "full recovery within six months" in text.lower() or "full recovery expected within six months" in text.lower():
                result["Prognosis"] = "Full recovery expected within six months"
            elif "feel better within a few days" in text.lower() or "better within a few days" in text.lower():
                result["Prognosis"] = "Should improve within a few days"
            elif "angina" in text.lower() or "heart" in text.lower():
                result["Prognosis"] = "Requires further testing"
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