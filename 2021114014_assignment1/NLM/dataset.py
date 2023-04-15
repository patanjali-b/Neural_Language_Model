import torch
import pandas as pd
from torch.utils.data import Dataset
from torchvision import datasets
from torchvision.transforms import ToTensor
import matplotlib.pyplot as plt
from collections import Counter

device = "cuda" if torch.cuda.is_available() else "cpu"

import re
def Tokenizer(text):
    text = text.lower()
    
    # Split the text into tokens using regular expressions
    tokens = re.findall(r'\b\w+\b', text)
    return tokens   
   

class Dataset(torch.utils.data.Dataset):
    def __init__(self,args):
        self.args = args
        self.path = args.path
        self.unique_words = self.getUniqWords() # List of uniq words with their frequence
        self.vocabulary = self.getVocab() # List of Tokens starting wit <sos> and ending wiht <eos>
        self.int2word = {index: word for index, word in enumerate(self.unique_words)}
        self.word2int = {word: index for index, word in enumerate(self.unique_words)}

        self.words_indexes = [self.word2int[w] for w in self.vocabulary]

    def getVocab(self):
        def handle_unknowns(words):
          word_counts = Counter(words)
          for i in range(len(words)):
            if word_counts[words[i]] <= 3:
              words[i] = "<unk>"
          return words
        File_object = open(self.path,"r")
        data = File_object.readlines()
        text = ""
        # adding end of sequence to make the model learn seperation between sentences
        for line in data:
          text += "<sos> " + " ".join(Tokenizer(line)) + " <eos> "
        return handle_unknowns(text.split(' '))
    def getUniqWords(self):
        word_counts = Counter(self.getVocab())
        return sorted(word_counts, key=word_counts.get, reverse=True)
    def __len__(self):
        return len(self.words_indexes) - self.args.sequence_length

    def __getitem__(self, index):
        return (
            torch.tensor(self.words_indexes[index:index+self.args.sequence_length]).to(device),
            torch.tensor(self.words_indexes[index+1:index+self.args.sequence_length+1]).to(device),
        )


         # lines = []
    # for line in file_name:
    #         if not line.isspace():
    #             lines.append(line)
                
    
    # tokens = []
    # str2 = ""
   
    # for line in lines:
    #     line = re.sub(r'(((http|https):\/\/)|www\.)([a-zA-Z0-9]+\.){0,2}[a-zA-Z0-9]+([a-zA-Z0-9\/#%&=\?_\.\-\+]+)', "URLHERE", line)
    #     line = re.sub(r'(@[a-zA-Z0-9_]+)', "MENTIONHERE", line)
    #     line = re.sub(r'(#[a-zA-Z0-9_]+\b)', "HASHTAG", line)
    #     line = re.sub("_","",line)
    #     line = re.sub(r'\d+', "",line)
    #     line = re.sub(r'--',"",line)
    #     line = line.replace("Mr.", "Mr")
    #     line = line.replace("Mrs.", "Mr")
    #     line = line.replace("Dr.", "Dr")
    #     line = line.replace("\x00","")
    #     line = line.lower()
    #     line = re.sub(r'[^a-zA-Z !?.]', '', line)
    #     pattern = r"([a-zA-Z])'([a-zA-Z])"
    #     line = re.sub(pattern, r"\1\2", line)
    #     tokens_in_line = re.findall(r'\b\w+\b|_|[^\w\s]+|"|\'', line)
    #     filtered_tokens = [re.sub(r'([^\w\s])\1+', r'\1', token) for token in tokens_in_line]
    #     tokens['tokens'] = (filtered_tokens)

    #     for k in filtered_tokens:
    #         if k!="." and k!="!" and k!="?":
    #             str2 = str2+ k +" "
    #         else:
    #             str2= str2[0:-1]
    #             str2 = str2+ k +" "
        
    #     final_tokens = []
    #     for token_list in tokens:
    #         final_tokens.extend(token_list)
    #     return final_tokens