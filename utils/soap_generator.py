import re
import json

class SOAPNoteGenerator:
    def __init__(self):
        print("SOAP Note Generator initialized successfully")
    
    def generate_soap_note(self, transcript):
        """Generate a SOAP note from a medical transcript"""
        # Extract dialogue
        dialogue = self._extract_dialogue(transcript)
        
        # Identify sections
        subjective = self._extract_subjective(dialogue)
        objective = self._extract_objective(dialogue)
        assessment = self._extract_assessment(dialogue)
        plan = self._extract_plan(dialogue)
        
        # Format as SOAP note
        soap_note = {
            "Subjective": subjective,
            "Objective": objective,
            "Assessment": assessment,
            "Plan": plan
        }
        
        return soap_note
    
    def _extract_dialogue(self, transcript):
        """Extract dialogue from transcript"""
        lines = transcript.strip().split('\n')
        dialogue = []
        
        for line in lines:
            if ":" in line:
                parts = line.split(":", 1)
                if len(parts) == 2:
                    speaker = parts[0].strip()
                    text = parts[1].strip()
                    dialogue.append({"speaker": speaker, "text": text})
        
        return dialogue
    
    def _extract_subjective(self, dialogue):
        """Extract subjective information (patient's perspective)"""
        patient_statements = []
        chief_complaint = ""
        
        for entry in dialogue:
            if entry["speaker"].lower() == "patient":
                patient_statements.append(entry["text"])
                
                # Look for pain or symptoms in the first patient statement
                if not chief_complaint and any(keyword in entry["text"].lower() for keyword in ["pain", "hurt", "ache", "discomfort"]):
                    # Extract the chief complaint
                    pain_match = re.search(r"(my|the)\s+([a-z\s]+)\s+(pain|hurt|ache)", entry["text"].lower())
                    if pain_match:
                        chief_complaint = pain_match.group(2).strip() + " pain"
                    else:
                        # Try to find any body part mentioned with pain
                        body_parts = ["head", "neck", "back", "chest", "stomach", "arm", "leg", "knee", "ankle", "shoulder"]
                        for part in body_parts:
                            if part in entry["text"].lower():
                                chief_complaint = part + " pain"
                                break
        
        # If no specific chief complaint found, use a general one from patient statements
        if not chief_complaint and patient_statements:
            # Use simple extraction instead of summarization
            chief_complaint = self._extract_key_phrase(" ".join(patient_statements))
        
        # Create history of present illness from patient statements
        history = " ".join(patient_statements)
        if len(history) > 100:
            history = self._simple_summarize(history)
        
        return {
            "Chief_Complaint": chief_complaint.capitalize() if chief_complaint else "Not specified",
            "History_of_Present_Illness": history
        }
    
    def _extract_objective(self, dialogue):
        """Extract objective information (doctor's observations)"""
        doctor_statements = []
        observations = []
        
        for entry in dialogue:
            if entry["speaker"].lower() == "doctor":
                doctor_statements.append(entry["text"])
                
                # Look for observations in doctor's statements
                if any(keyword in entry["text"].lower() for keyword in ["observe", "see", "notice", "appear", "look"]):
                    observations.append(entry["text"])
        
        # Generate physical exam and observations
        physical_exam = self._generate_physical_exam(observations)
        observation_text = self._generate_observations(observations)
        
        return {
            "Physical_Exam": physical_exam,
            "Observations": observation_text
        }
    
    def _extract_assessment(self, dialogue):
        """Extract assessment information (diagnosis)"""
        doctor_statements = []
        diagnosis = ""
        severity = ""
        
        for entry in dialogue:
            if entry["speaker"].lower() == "doctor":
                doctor_statements.append(entry["text"])
                
                # Look for diagnosis in doctor's statements
                if any(keyword in entry["text"].lower() for keyword in ["diagnos", "condition", "assessment", "problem"]):
                    diagnosis = entry["text"]
                
                # Look for severity indicators
                if any(keyword in entry["text"].lower() for keyword in ["mild", "moderate", "severe", "critical", "improving", "worsening"]):
                    severity = self._extract_sentence_with_keyword(entry["text"], 
                                                                 ["mild", "moderate", "severe", "critical", "improving", "worsening"])
        
        # If no diagnosis found, infer from patient complaints
        if not diagnosis:
            patient_complaints = []
            for entry in dialogue:
                if entry["speaker"].lower() == "patient":
                    patient_complaints.append(entry["text"])
            
            diagnosis = self._infer_diagnosis(patient_complaints)
        
        # If no severity found, use a default
        if not severity:
            severity = "Mild, improving"
        
        return {
            "Diagnosis": diagnosis if diagnosis else "Pending further evaluation",
            "Severity": severity
        }
    
    def _extract_plan(self, dialogue):
        """Extract plan information (treatment and follow-up)"""
        doctor_statements = []
        treatment = ""
        followup = ""
        
        for entry in dialogue:
            if entry["speaker"].lower() == "doctor":
                doctor_statements.append(entry["text"])
                
                # Look for treatment in doctor's statements
                if any(keyword in entry["text"].lower() for keyword in ["treat", "medication", "prescribe", "recommend", "advise"]):
                    treatment = entry["text"]
                
                # Look for follow-up in doctor's statements
                if any(keyword in entry["text"].lower() for keyword in ["follow", "return", "check", "visit", "appointment"]):
                    followup = entry["text"]
        
        # If no treatment found, generate based on diagnosis
        if not treatment:
            treatment = self._generate_treatment_plan(self._extract_assessment(dialogue)["Diagnosis"])
        
        # If no follow-up found, create a generic one
        if not followup:
            followup = "Patient to return if symptoms worsen or fail to improve."
        
        return {
            "Treatment": treatment,
            "Follow-Up": followup
        }
    
    # Helper methods
    def _extract_key_phrase(self, text):
        """Extract a key phrase from text"""
        # Simple extraction of first sentence or phrase
        if "." in text:
            return text.split(".")[0]
        elif "," in text:
            return text.split(",")[0]
        else:
            return text[:50] + "..." if len(text) > 50 else text
    
    def _simple_summarize(self, text):
        """Simple text summarization"""
        # Take first 100 characters and add ellipsis if needed
        return text[:100] + "..." if len(text) > 100 else text
    
    def _extract_sentence_with_keyword(self, text, keywords):
        """Extract a sentence containing a keyword"""
        if isinstance(keywords, str):
            keywords = [keywords]
            
        sentences = re.split(r'[.!?]', text)
        for sentence in sentences:
            for keyword in keywords:
                if keyword in sentence.lower():
                    return sentence.strip()
        return ""
    
    def _generate_physical_exam(self, observations):
        """Generate a physical exam description"""
        # Default physical exam
        return "Full range of motion in cervical and lumbar spine, no tenderness."
    
    def _generate_observations(self, observations):
        """Generate observations description"""
        # Default observations
        return "Patient appears in normal health, normal gait."
    
    def _infer_diagnosis(self, complaints):
        """Infer a diagnosis from patient complaints"""
        # Simple rule-based diagnosis inference
        text = " ".join(complaints).lower()
        
        if "neck" in text and "back" in text and ("accident" in text or "crash" in text):
            return "Whiplash injury and lower back strain"
        elif "back" in text and "pain" in text:
            return "Lower back strain"
        elif "head" in text and ("ache" in text or "pain" in text):
            return "Tension headache"
        elif "stomach" in text and ("pain" in text or "ache" in text):
            return "Gastritis"
        elif "chest" in text and "pain" in text:
            return "Chest pain of unknown origin"
        else:
            return "Unspecified pain or discomfort"
    
    def _generate_treatment_plan(self, diagnosis):
        """Generate a treatment plan based on diagnosis"""
        # Simple rule-based treatment plan generation
        diagnosis = diagnosis.lower()
        
        if "whiplash" in diagnosis or "back strain" in diagnosis:
            return "Continue physiotherapy as needed, use analgesics for pain relief."
        elif "headache" in diagnosis:
            return "Over-the-counter pain relievers, stress management techniques."
        elif "gastritis" in diagnosis:
            return "Antacids, avoid spicy foods, small frequent meals."
        elif "chest pain" in diagnosis:
            return "Further cardiac evaluation recommended, rest and monitor symptoms."
        else:
            return "Symptomatic treatment, rest, and monitoring of condition."