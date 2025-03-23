import re
import ssl
import nltk
from collections import Counter

class MedicalKeywordExtractor:
    def __init__(self):
        """Initialize the keyword extractor"""
        # Fix SSL certificate issue for NLTK downloads
        try:
            _create_unverified_https_context = ssl._create_unverified_context
        except AttributeError:
            pass
        else:
            ssl._create_default_https_context = _create_unverified_https_context
        
        # Download NLTK resources if not already downloaded
        try:
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
    
    def extract_keywords(self, text, top_n=10):
        """Extract keywords from text using a simple approach"""
        # Convert to lowercase
        text = text.lower()
        
        # Simple tokenization using regex
        words = re.findall(r'\b[a-z]{3,}\b', text)
        
        # Remove stopwords
        filtered_words = [word for word in words if word not in self.stopwords]
        
        # Count word frequencies
        word_counts = Counter(filtered_words)
        
        # Get single word keywords
        single_keywords = [{"keyword": word, "relevance": count/len(filtered_words)} 
                          for word, count in word_counts.most_common(top_n)]
        
        # Extract bigrams (pairs of adjacent words)
        bigrams = []
        for i in range(len(filtered_words) - 1):
            bigrams.append(filtered_words[i] + " " + filtered_words[i+1])
        
        # Count bigram frequencies
        bigram_counts = Counter(bigrams)
        
        # Get bigram keywords
        bigram_keywords = [{"keyword": bigram, "relevance": count/len(bigrams) if bigrams else 0} 
                          for bigram, count in bigram_counts.most_common(top_n//2)]
        
        # Combine and sort by relevance
        all_keywords = single_keywords + bigram_keywords
        all_keywords.sort(key=lambda x: x["relevance"], reverse=True)
        
        return all_keywords[:top_n] 