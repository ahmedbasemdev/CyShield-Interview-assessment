import torch
from transformers import BertTokenizer, BertForSequenceClassification
from torch.nn.functional import softmax

class SentimentAnalyzerManager:
    
    def __init__(self):
        model_name = "nlptown/bert-base-multilingual-uncased-sentiment"
        self.tokenizer = BertTokenizer.from_pretrained(model_name)
        self.model = BertForSequenceClassification.from_pretrained(model_name)

    def predict_sentiment(self, sentence):
        inputs = self.tokenizer(sentence, return_tensors="pt", truncation=True, padding=True, max_length=512)
        with torch.no_grad():
            outputs = self.model(**inputs)
        logits = outputs.logits
        probs = softmax(logits, dim=-1)
        prediction = torch.argmax(probs, dim=-1).item()
        sentiment = "negative" if prediction < 2 else "positive"
        return sentiment  
