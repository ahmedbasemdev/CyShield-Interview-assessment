import re 
import string
def remove_punctuations(text):
  punctuation = string.punctuation
  text = text.translate(str.maketrans("","",punctuation))
  return text

def remove_digits(text):
  digits = string.digits
  text = text.translate(str.maketrans("","",digits))
  return text

def remove_links(text):
  text = re.sub(r"(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w\.-]*)","",text)
  return text

def remove_hashtags_mentions(text):
  text = re.sub(r"@[\w]+","",text)
  text = re.sub(r"#\S+","",text)
  return text