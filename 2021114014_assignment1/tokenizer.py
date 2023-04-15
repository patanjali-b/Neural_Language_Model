# to make a tokenizer using regex

import re

text_str = ""
# Open the file in read mode
with open('Pride and Prejudice - Jane Austen.txt', 'r') as file:
    # Loop through the lines of the file
    for line in file:
        text_str = text_str + line + " "
# replace all spaces with a single space
text_str = re.sub(r'\s+', ' ', text_str)
# replace all urls with <URL>
url_pattern = re.compile(r'^https?:\/\/.*[\r\n]*')
text_str = url_pattern.sub('<URL>', text_str)
text_str = text_str[1713:-18524]
# replace all mentions with <MENTION>
mention_pattern = re.compile(r'@\w+')
text_str = mention_pattern.sub('<MENTION>', text_str)
# replace all hashtags with <HASHTAG>
hashtag_pattern = re.compile(r'#\w+')
text_str = hashtag_pattern.sub('<HASHTAG>', text_str)
# remove all punctuation marks except period, question mark, exclamation mark
text_str = re.sub(r'[^\w\s.?!]', '', text_str)
# replace dr. mr. mrs. ms. with dr mr mrs ms
text_str = re.sub(r'\bdr\.', 'dr', text_str)
text_str = re.sub(r'\bmr\.', 'mr', text_str)
text_str = re.sub(r'\bmrs\.', 'mrs', text_str)
text_str = re.sub(r'\bms\.', 'ms', text_str)
# remove all numeric characters
text_str = re.sub(r'\d+', '', text_str)
# lowercase all letters
text_str = text_str.lower()
# remove all underscores
text_str = re.sub(r'_', '', text_str)

# split text string into a list of sentences
sentences = re.split(r'[.?!]', text_str)
# split sentences into a list of words
words = []
list_of_sentences = []
for sentence in sentences:
    local_list = []
    local_list.append(sentence.split())
    list_of_sentences.append(local_list)
print(list_of_sentences)







