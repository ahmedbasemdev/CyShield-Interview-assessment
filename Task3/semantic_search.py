import pandas as pd
import numpy as np
import re
import string
import nltk
nltk.download('punkt_tab')

from sentence_transformers import SentenceTransformer, util
from rake_nltk import Rake
from helper import *

class SemanticSearchManager:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.rake = Rake()
    
    def insert_date(self, texts:list[str]):
        self.data = pd.DataFrame({"article": texts})
        self.data['article'] = self.data['article'].apply(self.text_preprocessing)
        self.data['key_words'] = self.data['article'].apply(self.extract_keywords)
        self.embeddings = self.model.encode(self.data['article'].to_list(), convert_to_tensor=True)
        

    def text_preprocessing(self, text):
        text = remove_punctuations(text)
        text = remove_digits(text)
        text = remove_links(text)
        text = remove_hashtags_mentions(text)
        return text
    
    def similarity_search(self, query:str, top_k:int = 3):
        query_embedding = self.model.encode(query, convert_to_tensor=True)
        similarities = util.pytorch_cos_sim(query_embedding, self.embeddings)
        top_results = similarities.topk(k=top_k)
        results = []
        for idx in top_results[1].tolist()[0]:
            results.append({"article":self.data.iloc[idx].article, "key_words":self.data.iloc[idx].key_words})
        return results
    
    
    def extract_keywords(self, text):
        self.rake.extract_keywords_from_text(text)
        return self.rake.get_ranked_phrases()
