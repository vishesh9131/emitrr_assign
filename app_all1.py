import streamlit as st
import json
from utils.ner import MedicalNER
from utils.summarization import MedicalSummarizer
from utils.keyword import MedicalKeywordExtractor
from transcript import *

# Set page config
st.set_page_config(
    page_title="Physician Notetaker",
    page_icon="🩺",
    layout="wide"
)

# Initialize models
@st.cache_resource
def load_models():
    try:
        ner = MedicalNER()
        summarizer = MedicalSummarizer()
        keyword_extractor = MedicalKeywordExtractor()
        return ner, summarizer, keyword_extractor
    except Exception as e:
        st.error(f"Error loading models: {str(e)}")
        return None, None, None

ner, summarizer, keyword_extractor = load_models()

# App title
st.title("🩺 Physician Notetaker")
st.subheader("Medical NLP Summarization")

# Define all transcript chunks
CHUNKS = {
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
    
    
    # Add all remaining chunks up to CHUNK_P
}

# Button to process all chunks
if st.button("Process All Chunks"):
    with st.spinner("Processing all transcript chunks..."):
        results = {}

        for chunk_name, chunk_text in CHUNKS.items():
            # Extract entities
            entities = ner.extract_entities(chunk_text)
            
            # Generate summary
            summaries = summarizer.summarize(chunk_text)
            
            # Extract keywords
            keywords = keyword_extractor.extract_keywords(chunk_text)
            
            # Store results
            results[chunk_name] = {
                "entities": entities,
                "summary": summaries,
                "keywords": keywords
            }
        
        # Display results
        st.subheader("Results for All Chunks")
        
        for chunk_name, data in results.items():
            with st.expander(f"Results for {chunk_name}"):
                tab1, tab2, tab3 = st.tabs(["Medical Report", "Summary", "Keywords"])
                
                with tab1:
                    st.subheader("Medical Report")
                    st.json(data["entities"])
                
                with tab2:
                    st.subheader("Full Summary")
                    st.write(data["summary"]["full"])
                    
                    st.subheader("Doctor's Summary")
                    st.write(data["summary"]["doctor"])
                    
                    st.subheader("Patient's Summary")
                    st.write(data["summary"]["patient"])
                
                with tab3:
                    st.subheader("Top Keywords")
                    for kw in data["keywords"]:
                        st.write(f"• {kw['keyword']} (relevance: {kw['relevance']:.2f})")

# Footer
st.markdown("---")
st.markdown("Physician Notetaker - Medical NLP Summarization")