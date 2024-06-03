import os
from nltk.tokenize import word_tokenize, sent_tokenize
import string
import pandas as pd

def stopword_getter(dir_path):
    stop_words = []
    for i in os.listdir(dir_path):
        if i.startswith('StopWords'):
            with open(dir_path + '/' + i, encoding="latin-1") as f:
                text = f.read()
            words = text.split()
            for word in words:
                stop_words.append(word.lower())
    return stop_words

def pos_neg_dict(dir_path,exclusion_list):
    sentiment_dict = {}
    words_excluded = []
    for i in os.listdir(dir_path):
        if i.startswith('1positive'):
            with open(dir_path + '/' + i, encoding="latin-1") as f:
                text = f.read()
            words = text.split()
            for word in words:
                if word not in exclusion_list:
                    sentiment_dict[word.lower()] = 'positive'
                else:
                    words_excluded.append(word)
        elif i.startswith('negative'):
            with open(dir_path + '/' + i, encoding="latin-1") as f:
                text = f.read()
            words = text.split()
            for word in words:
                if word not in exclusion_list:
                    sentiment_dict[word.lower()] = 'negative'
                else:
                    words_excluded.append(word)
    return sentiment_dict

def count_syllables(word):
    word = word.lower()
    vowels = "aeiou"
    current_count = 0
    prev_char_was_vowel = False

    for char in word:
        if char in vowels:
            if not prev_char_was_vowel:
                current_count += 1
            prev_char_was_vowel = True
        else:
            prev_char_was_vowel = False

    if word.endswith("e"):
        current_count -= 1
    if word.endswith("le") and len(word) > 2 and word[-3] not in vowels:
        current_count += 1
    if current_count == 0:
        current_count = 1

    return current_count

def get_complex_percentage(txt_file):
    complex_percentage = 0
    complex_count = 0
    with open (txt_file, encoding="latin-1") as f:
        text = f.read()
    word_tokens = word_tokenize(text)
    for i in word_tokens:
        if count_syllables(i) > 2:
            complex_count += 1
    complex_percentage = complex_count/len(word_tokens)

    resulting = [complex_count,complex_percentage]
    return resulting

def count_personal_pronouns(text):
    with open (text, encoding="latin-1") as f:
        text = f.read()
    pronoun_count = 0
    personal_pronouns = [
    'I', 'we', 'We', 'you', 'You', 'he', 'He', 'she', 'She', 'it', 'It', 'they', 'They'
    'me', 'Me', 'us', 'Him', 'Her', 'him', 'her', 'them', 'Them'
    'my', 'My', 'our', 'Our', 'your', 'Your', 'his', 'His', 'their', 'Their','its', 'Its'
    'mine', 'Mine','yours', 'Yours','hers', 'Hers','ours','Ours', 'theirs','Theirs']

    words = list(word_tokenize(text))

    for word in words:
        if word in personal_pronouns:
            pronoun_count += 1
    return pronoun_count

def avg_word_length(txt_file):
    sum_of_lengths = 0
    with open(txt_file, encoding="latin-1") as f:
        text = f.read()
    word_tokens = word_tokenize(text)
    word_tokens = [token for token in word_tokens if token not in string.punctuation]
    for i in word_tokens:
        sum_of_lengths += len(i)
    return sum_of_lengths/len(word_tokens)

def syllable_count(txt_file):
    with open(txt_file, encoding="latin-1") as f:
        text = f.read()
    word_tokens = word_tokenize(text)
    word_tokens = [token for token in word_tokens if token not in string.punctuation]
    syllable_count = 0
    for i in word_tokens:
        if i.endswith("es") or i.endswith("ed"):
                syllable_count -= 1
        syllable_count += count_syllables(i)
    return syllable_count

def txt_process(txt_file,stopwords,posneg_dict):
    frame = pd.read_excel('problem_statement/Input.xlsx')
    txt_report = {}
    pos_neg_count = {}
    clean_words = 0
    pos_neg_count['URL_ID'] = txt_file[10:-4]
    # print(txt_file[10:-4])
    # print(frame.loc[frame['URL_ID'] == txt_file[10:-4], 'URL'].values[0])
    pos_neg_count['URL'] = frame.loc[frame['URL_ID'] == txt_file[10:-4], 'URL'].values[0]
    with open(txt_file,encoding="latin-1") as f:
        text = f.read()
    word_tokens = list(set(word_tokenize(text)))
    sent_tokens = list(set(sent_tokenize(text)))
    word_tokens = [token for token in word_tokens if token not in string.punctuation]
    sent_tokens = [token for token in sent_tokens if token not in string.punctuation]
    for i in word_tokens:
        if i.lower() not in stopwords:
            clean_words += 1
            if i.lower() in posneg_dict:
                txt_report[i.lower()] = str(posneg_dict[i.lower()]+" score").upper()
    for j in txt_report.values():
        if j in pos_neg_count:
            pos_neg_count[j] += 1
        else:
            pos_neg_count[j] = 1

    if 'POSITIVE SCORE' not in pos_neg_count:
        pos_neg_count['POSITIVE SCORE'] = 0
    if 'NEGATIVE SCORE' not in pos_neg_count:
        pos_neg_count['NEGATIVE SCORE'] = 0

    average_sentence_length = len(word_tokens)/len(sent_tokens)
    complex_percentage = get_complex_percentage(txt_file)
    personal_pronouns = count_personal_pronouns(txt_file)

    pos_neg_count['POLARITY SCORE'] = ((pos_neg_count['POSITIVE SCORE'] - pos_neg_count['NEGATIVE SCORE'])/((pos_neg_count['POSITIVE SCORE'] + pos_neg_count['NEGATIVE SCORE'])+0.000001))
    pos_neg_count['SUBJECTIVITY SCORE'] = ((pos_neg_count['POSITIVE SCORE'] + pos_neg_count['NEGATIVE SCORE'])/(clean_words+0.000001))
    pos_neg_count['AVG SENTENCE LENGTH'] = average_sentence_length
    pos_neg_count['PERCENTAGE OF COMPLEX WORDS'] = complex_percentage[1]
    pos_neg_count['FOG INDEX'] = 0.4*(average_sentence_length + complex_percentage[1])
    pos_neg_count['AVG NUMBER OF WORDS PER SENTENCE'] = len(word_tokenize(text))/len(sent_tokenize(text))
    pos_neg_count['COMPLEX WORD COUNT'] = complex_percentage[0]
    pos_neg_count['WORD COUNT'] = clean_words
    pos_neg_count['SYLLABLE PER WORD'] = syllable_count(txt_file)
    pos_neg_count['PERSONAL PRONOUNS'] = personal_pronouns
    pos_neg_count['AVG WORD LENGTH'] = avg_word_length(txt_file)

    return pos_neg_count

all_rows = []

stopword_list = stopword_getter('problem_statement/StopWords')
psng_dict = pos_neg_dict('problem_statement/MasterDictionary',stopword_getter('problem_statement/StopWords'))

for i in os.listdir('txt_files'):
    all_rows.append(txt_process('txt_files/'+i, stopword_list, psng_dict))
    print('Row Added')

df = pd.DataFrame(all_rows)
df.to_csv('Output Data Structure.csv', index=False)
print('Done!')