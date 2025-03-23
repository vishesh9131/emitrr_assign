import re
import nltk
import ssl
import os
from nltk.tokenize import sent_tokenize

class MedicalSummarizer:
    def __init__(self):
        """Initialize the summarization model using a simple approach"""
        # Fix SSL certificate issue for NLTK downloads
        try:
            _create_unverified_https_context = ssl._create_unverified_context
        except AttributeError:
            pass
        else:
            ssl._create_default_https_context = _create_unverified_https_context
        
        # Try to download NLTK resources
        try:
            nltk.download('punkt')
            nltk.download('stopwords')
            from nltk.corpus import stopwords
            self.stopwords = set(stopwords.words('english'))
        except Exception as e:
            print(f"Error downloading NLTK resources: {str(e)}")
            # Fallback stopwords if download fails
            self.stopwords = set([
                'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 
                'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 
                'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 
                'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 
                'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 
                'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 
                'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 
                'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 
                'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 
                'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 
                'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 
                'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 
                'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 
                's', 't', 'can', 'will', 'just', 'don', 'should', 'now'
            ])
        
        # Add medical stopwords
        self.stopwords.update([
            "doctor", "patient", "said", "told", "asked", "mentioned",
            "explained", "discussed", "noted", "recommended", "suggested"
        ])
    
    def clean_text(self, text):
        """Clean and preprocess the text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        # Remove special characters
        text = re.sub(r'[^\w\s.,?!:;-]', '', text)
        return text
    
    def split_by_speaker(self, transcript):
        """Split transcript by speaker (doctor/patient)"""
        doctor_text = []
        patient_text = []
        
        lines = transcript.split('\n')
        for line in lines:
            if line.startswith("Doctor:"):
                doctor_text.append(line.replace("Doctor:", "").strip())
            elif line.startswith("Patient:"):
                patient_text.append(line.replace("Patient:", "").strip())
        
        return {
            "doctor": " ".join(doctor_text),
            "patient": " ".join(patient_text),
            "full": transcript
        }
    
    def sentence_importance(self, sentence, important_words):
        """Calculate sentence importance based on important words"""
        words = [word.lower() for word in sentence.split() 
                if word.isalnum() and word.lower() not in self.stopwords]
        
        return sum(1 for word in words if word in important_words) / max(len(words), 1)
    
    def extractive_summarize(self, text, ratio=0.3):
        """Generate an extractive summary using a simple approach"""
        # Simple sentence splitting by punctuation
        sentences = [s.strip() for s in re.split(r'[.!?]+', text) if s.strip()]
        
        if len(sentences) <= 3:
            return text
        
        # Get all words that are not stopwords
        words = [word.lower() for word in re.findall(r'\b\w+\b', text.lower())
                if word.lower() not in self.stopwords]
        
        # Calculate word frequency
        word_freq = {}
        for word in words:
            word_freq[word] = word_freq.get(word, 0) + 1
        
        # Get most important words (top 20%)
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        top_n = max(int(len(sorted_words) * 0.2), 5)
        important_words = {word for word, _ in sorted_words[:top_n]}
        
        # Score sentences
        sentence_scores = [(sentence, self.sentence_importance(sentence, important_words)) 
                          for sentence in sentences]
        
        # Sort sentences by score
        sorted_sentences = sorted(sentence_scores, key=lambda x: x[1], reverse=True)
        
        # Select top sentences (based on ratio)
        selected_sentences = sorted_sentences[:max(int(len(sentences) * ratio), 3)]
        
        # Sort selected sentences by original order
        selected_sentences = [(i, sentence, score) 
                             for i, (sentence, score) in enumerate(sentence_scores) 
                             if (sentence, score) in selected_sentences]
        selected_sentences.sort(key=lambda x: x[0])
        
        # Join sentences
        summary = '. '.join(sentence for _, sentence, _ in selected_sentences)
        if not summary.endswith('.'):
            summary += '.'
        return summary
    
    def summarize(self, transcript, ratio=0.3):
        """Generate a summary of the medical transcript"""
        # Split text by speaker
        texts = self.split_by_speaker(transcript)
        
        # Clean texts
        for key in texts:
            texts[key] = self.clean_text(texts[key])
        
        # Generate summaries
        summaries = {}
        
        # Summarize full transcript
        summaries["full"] = self.extractive_summarize(texts["full"], ratio)
        
        # Summarize doctor's part
        summaries["doctor"] = self.extractive_summarize(texts["doctor"], ratio)
            
        # Summarize patient's part
        summaries["patient"] = self.extractive_summarize(texts["patient"], ratio)
        
        return summaries 