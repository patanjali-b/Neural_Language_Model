import argparse
import torch
import numpy as np
from torch import nn, optim
from torch.utils.data import DataLoader
import torchvision.models as models
from model import Model                 # from the class
from dataset import Dataset             # from the class


device = "cuda" if torch.cuda.is_available() else "cpu"
print(device)
import re
def Tokenizer(text):
    text = text.lower()
    # Split the text into tokens using regular expressions
    tokens = re.findall(r'\b\w+\b', text)
    return tokens
    

def get_probability(dataset, model, text):
    model.eval()

    text = " ".join(Tokenizer(text))
    words = text.split(' ')
    for i in range(len(words)):
      if words[i] not in dataset.getUniqWords():
        words[i] = "<unk>"
    prob = 1
    for i in range(1, len(words)):
        x = torch.tensor([[dataset.word2int[w] for w in words[:i]]]).to(device)

        state_h, state_c = model.init_state(i)
        y_pred, (state_h, state_c) = model(x, (state_h, state_c))

        last_word_logits = y_pred[0][-1]
        print(last_word_logits)
        p = torch.nn.functional.softmax(last_word_logits, dim=0).cpu().detach().numpy()
        word_index = dataset.word2int[words[i]]
        # print(dataset.index_to_word[word_index], p[word_index])  REMOVE THIS !!!!!
        prob *= p[word_index]

    return prob


def train(dataset, model, args):
    model.train()

    dataloader = DataLoader(dataset, batch_size=args.batch_size)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    for epoch in range(5):
        state_h, state_c = model.init_state(args.sequence_length)

        for batch, (x, y) in enumerate(dataloader):
            optimizer.zero_grad()

            y_pred, (state_h, state_c) = model(x, (state_h, state_c))
            loss = criterion(y_pred.transpose(1, 2), y)

            state_h = state_h.detach()
            state_c = state_c.detach()

            loss.backward()
            optimizer.step()

            print({ 'epoch': epoch, 'batch': batch, 'loss': loss.item() })


parser = argparse.ArgumentParser()
parser.add_argument('--path', type = str, default = "Ulysses.txt")
parser.add_argument('--max-epochs', type=int, default=25)
parser.add_argument('--batch-size', type=int, default=256)
parser.add_argument('--sequence-length', type=int, default=4)
args = parser.parse_args()
print(args)
dataset = Dataset(args)
model = Model(dataset)
train(dataset, model, args)
sentence = input("Input Sentence: ")
print(get_probability(dataset, model, sentence))

torch.save(model, 'model_weights.pth')

print(get_probability(dataset, model, sentence))

model = torch.load('model_weights.pth')
model.eval()
while(1):
    string = input()
    print(get_probability(dataset, model, string))

