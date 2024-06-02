import string
import nltk
from nltk.corpus import stopwords
import re

# Uncomment if required
# nltk.download('punkt')
# nltk.download('stopwords')

def preprocess_text(filename):

  with open(filename, 'r') as f:
    text = f.read()

  text = text.lower()

  punc_free = "".join([char for char in text if char not in string.punctuation])

  stop_words = stopwords.words('english')
  filtered_words = [word for word in punc_free.split() if word not in stop_words]

  processed_text = re.sub(r"[^a-zA-Z0-9\s]", "", " ".join(filtered_words))

  tokens = processed_text.split()

  return list(set(tokens))

# Example usage
text_file = "txt_files/output_file1.txt"
preprocessed_tokens = preprocess_text(text_file)

print(preprocessed_tokens)