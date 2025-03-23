import os
from huggingface_hub import snapshot_download

def download_models():
    """Pre-download models to cache"""
    models = [
        "dmis-lab/biobert-base-cased-v1.1",
        "dbmdz/bert-large-cased-finetuned-conll03-english",
        "distilbert-base-uncased-finetuned-sst-2-english"
    ]
    
    for model in models:
        try:
            snapshot_download(model, local_files_only=False)
            print(f"Downloaded {model}")
        except Exception as e:
            print(f"Error downloading {model}: {e}") 