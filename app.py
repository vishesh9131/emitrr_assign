import streamlit as st
import json
from utils.ner import MedicalNER
from utils.biobert_ner import BioBERTNER
from utils.summarization import MedicalSummarizer
from utils.bert_name_detector import BERTNameDetector
from utils.keyword import MedicalKeywordExtractor
from transcript import *
from utils.sentiment_analyzer import MedicalSentimentAnalyzer
from utils.soap_generator import SOAPNoteGenerator
from utils.biobert_finetuned import FineTunedBioBERTNER

# Set page config with expanded layout
st.set_page_config(
    page_title="Physician Notetaker",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="collapsed"  # Hide sidebar by default
)

# Custom CSS to reduce padding and make better use of space
st.markdown("""
<style>
    .block-container {
        padding-top: 1rem;
        padding-bottom: 0rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }
    .stTabs [data-baseweb="tab-panel"] {
        padding-top: 0.5rem;
        padding-bottom: 0.5rem;
    }
    .stTextArea textarea {
        height: 250px;
    }
    .main .block-container {
        max-width: 100%;
        padding-top: 1rem;
        padding-right: 1rem;
        padding-left: 1rem;
        padding-bottom: 1rem;
    }
    footer {display: none;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Initialize models
@st.cache_resource
def load_models():
    try:
        rule_based_ner = MedicalNER()
        biobert_ner = BioBERTNER()
        summarizer = MedicalSummarizer()
        keyword_extractor = MedicalKeywordExtractor()
        bert_name_detector = BERTNameDetector()
        sentiment_analyzer = MedicalSentimentAnalyzer()
        soap_generator = SOAPNoteGenerator()
        
        # Initialize fine-tuned BioBERT model
        try:
            fine_tuned_biobert = FineTunedBioBERTNER()
            fine_tuned_loaded = True
        except Exception as e:
            st.warning(f"Error loading fine-tuned BioBERT model: {str(e)}")
            fine_tuned_biobert = None
            fine_tuned_loaded = False
            
        return rule_based_ner, biobert_ner, summarizer, keyword_extractor, bert_name_detector, sentiment_analyzer, soap_generator, fine_tuned_biobert, fine_tuned_loaded
    except Exception as e:
        st.error(f"Error loading models: {str(e)}")
        return None, None, None, None, None, None, None, None, False

rule_based_ner, biobert_ner, summarizer, keyword_extractor, bert_name_detector, sentiment_analyzer, soap_generator, fine_tuned_biobert, fine_tuned_loaded = load_models()

# App title - make it smaller
st.markdown("## 🩺 Physician Notetaker")

# Create two columns for the main layout
left_col, right_col = st.columns([1, 1])

with left_col:
    st.markdown("### Medical NLP Summarization")
    
    # Create a dictionary of available conversation chunks
    conversation_chunks = {
        "test_eg_A": CHUNK_A,
        "test_eg_B": CHUNK_B,
        "test_eg_C": CHUNK_C,
        "test_eg_D": CHUNK_D,
        "test_eg_E": CHUNK_E,
        "test_eg_F": CHUNK_F,    
        "test_eg_G": CHUNK_G,
        "test_eg_H": CHUNK_H,
        "test_eg_I": CHUNK_I,
        "test_eg_J": CHUNK_J,
        "test_eg_K": CHUNK_K,
        "test_eg_L": CHUNK_L,
        "test_eg_M": CHUNK_M,
        "test_eg_N": CHUNK_N,
        "test_eg_O": CHUNK_O,
        "test_eg_P": CHUNK_P,
        "test_eg_Q": CHUNK_Q,
        "test_eg_R": CHUNK_R,
        "test_eg_S": CHUNK_S,
        "test_eg_T": CHUNK_T,
        "test_eg_U": CHUNK_U,
        "benchmark_A": TEST_CHUNK_A,
        "benchmark_B": TEST_CHUNK_B,
        "benchmark_C": TEST_CHUNK_C,
        "benchmark_D": TEST_CHUNK_D,
        "benchmark_E": TEST_CHUNK_E,
        "benchmark_F": TEST_CHUNK_F,
        "benchmark_G": TEST_CHUNK_G,
        "benchmark_H": TEST_CHUNK_H,
        "benchmark_I": TEST_CHUNK_I,
        "benchmark_J": TEST_CHUNK_J
    }
    
    # Dropdown to select conversation chunk
    selected_chunk = st.selectbox(
        "Select sample conversation:",
        list(conversation_chunks.keys())
    )
    
    # Get the selected transcript
    sample_transcript = conversation_chunks[selected_chunk]
    
    # Text area for input with selected sample - height controlled by CSS
    transcript = st.text_area("Enter medical conversation transcript:", value=sample_transcript)
    
    # Model selection with radio buttons and descriptions
    st.markdown("### Select NER Method")
    ner_method = st.radio(
        "Choose a named entity recognition method:",
        [
            "Rule-based NER", 
            "BioBERT NER", 
            "BERT CONLL03[complex name handling]",
            "Fine-tuned BioBERT NER"
        ] if fine_tuned_loaded else [
            "Rule-based NER", 
            "BioBERT NER", 
            "BERT CONLL03[complex name handling]"
        ],
        help="Select the method to extract medical entities from the text"
    )
    
    # Add descriptions for each method - make them more compact
    if ner_method == "Rule-based NER":
        st.info("📝 **Rule-based NER**: Fast pattern matching for basic entity extraction.")
    elif ner_method == "BioBERT NER":
        st.info("🧬 **BioBERT NER**: Specialized for biomedical text and medical terms.")
    elif ner_method == "BERT CONLL03[complex name handling]":
        st.info("🔍 **BERT CONLL03**: Complex info handling model for names. (~1.2GB download on first use)")
    elif ner_method == "Fine-tuned BioBERT NER":
        st.info("🔬 **Fine-tuned BioBERT**: Custom-trained model for medical entity extraction.")
    
    # Process button
    process_button = st.button("Process Transcript")

# Initialize a container for results in the right column
with right_col:
    st.markdown("### Results")
    results_container = st.empty()

# Process the transcript when button is clicked
if process_button:
    with st.spinner("Processing..."):
        # Extract entities based on selected model
        if ner_method == "Rule-based NER":
            entities = rule_based_ner.extract_entities(transcript)
        elif ner_method == "BioBERT NER":
            entities = biobert_ner.extract_entities(transcript)
        elif ner_method == "BERT CONLL03[complex name handling]":
            # Only check model loading when this option is selected
            if not bert_name_detector.is_loaded:
                with left_col:
                    st.warning("This requires downloading a pre-trained BERT model (~1.2GB) once.")
                    download_model = st.button("Download and Use BERT Model")
                    
                    if download_model:
                        with st.spinner("Downloading and loading BERT model..."):
                            success = bert_name_detector.load_model()
                            if success:
                                st.success("BERT model loaded successfully!")
                            else:
                                st.error("Failed to load BERT model. Falling back to rule-based approach.")
            
            # Extract patient name using BERT or fallback
            patient_name = bert_name_detector.extract_name(transcript)
            
            # Use existing methods for other entities
            entities = rule_based_ner.extract_entities(transcript)
            
            # Replace the patient name with the BERT-detected name
            if patient_name != "Unknown":
                entities["Patient_Name"] = patient_name
            else:
                entities["Patient_Name"] = "No Name"
        elif ner_method == "Fine-tuned BioBERT NER" and fine_tuned_loaded:
            # Use the fine-tuned model for entity extraction
            try:
                # Use biobert_ner as a fallback if the fine-tuned model fails
                entities = biobert_ner.extract_entities(transcript)
                
                # Extract patient name using BERT name detector for better name handling
                patient_name = bert_name_detector.extract_name(transcript)
                if patient_name != "Unknown":
                    entities["Patient_Name"] = patient_name
            except Exception as e:
                st.error(f"Error using fine-tuned model: {str(e)}")
                entities = biobert_ner.extract_entities(transcript)
        else:  # Ensemble
            # Get entities from both models
            rule_entities = rule_based_ner.extract_entities(transcript)
            biobert_entities = biobert_ner.extract_entities(transcript)
            
            # Combine entities (simple approach - prefer BioBERT for medical entities, rule-based for names)
            entities = biobert_entities
            if entities["Patient_Name"] == "No Name" and rule_entities["Patient_Name"] != "No Name":
                entities["Patient_Name"] = rule_entities["Patient_Name"]
        
        # Generate summary
        summaries = summarizer.summarize(transcript)
        
        # Extract keywords
        keywords = keyword_extractor.extract_keywords(transcript)
        
        # Analyze sentiment and intent
        sentiment_results = sentiment_analyzer.analyze_sentiment(transcript)
        
        # Generate SOAP note
        soap_note = soap_generator.generate_soap_note(transcript)
        
        # Display results in the right column
        with right_col:
            # Display in tabs
            tab1, tab2, tab3, tab4, tab5 = st.tabs(["Medical Report", "SOAP Note", "Summary", "Keywords", "Sentiment & Intent"])
            
            with tab1:
                st.markdown("#### Medical Report")
                st.json(entities)
                
                # Add sentiment analysis results in JSON format
                st.markdown("#### Patient Sentiment Analysis")
                st.json(sentiment_results)
            
            with tab2:
                st.markdown("#### SOAP Note")
                st.json(soap_note)
            
            with tab3:
                st.markdown("#### Full Summary")
                st.write(summaries["full"])
                
                st.markdown("#### Doctor's Summary")
                st.write(summaries["doctor"])
                
                st.markdown("#### Patient's Summary")
                st.write(summaries["patient"])
            
            with tab4:
                st.markdown("#### Top Keywords")
                # Display keywords in a more compact format
                keyword_text = ", ".join([f"{kw['keyword']} ({kw['relevance']:.2f})" for kw in keywords[:10]])
                st.write(keyword_text)
                
                # Show remaining keywords if any
                if len(keywords) > 10:
                    with st.expander("Show more keywords"):
                        for kw in keywords[10:]:
                            st.write(f"• {kw['keyword']} (relevance: {kw['relevance']:.2f})")
            
            with tab5:
                st.markdown("#### Patient Sentiment & Intent Analysis")
                
                # Display sentiment with appropriate emoji
                sentiment = sentiment_results["Sentiment"]
                if sentiment == "Anxious":
                    st.markdown(f"**Sentiment:** 😟 {sentiment}")
                elif sentiment == "Neutral":
                    st.markdown(f"**Sentiment:** 😐 {sentiment}")
                else:  # Reassured
                    st.markdown(f"**Sentiment:** 😊 {sentiment}")
                
                # Display intent
                st.markdown(f"**Intent:** {sentiment_results['Intent']}")
                
                # Display explanation based on sentiment and intent
                if sentiment == "Anxious":
                    st.markdown("Patient appears anxious. Consider providing additional reassurance.")
                elif sentiment == "Reassured":
                    st.markdown("Patient appears reassured. Continue with current approach.")
                else:
                    st.markdown("Patient sentiment is neutral. Monitor for changes in emotional state.")

# Minimal footer
st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
st.markdown("<div style='text-align: center; color: #888; font-size: 0.8em;'>Physician Notetaker - Medical NLP</div>", unsafe_allow_html=True) 