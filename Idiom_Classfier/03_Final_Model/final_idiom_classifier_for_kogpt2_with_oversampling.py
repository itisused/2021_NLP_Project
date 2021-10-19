# -*- coding: utf-8 -*-
"""final Idiom Classifier for KoGPT2 with oversampling.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1EkmJtMTWznpjREpWWuzch3kCv99mQqfD
"""

'''
pip install --upgrade mxnet>=1.6.0
pip install gluonnlp
pip install transformers
pip install sentencepiece
'''

import gluonnlp as nlp
from gluonnlp.data import SentencepieceTokenizer, SentencepieceDetokenizer
from transformers import TFGPT2LMHeadModel
import tensorflow as tf

import pandas as pd
import numpy as np
from tensorflow.keras.layers import Dense, Input
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.sequence import pad_sequences
import re
from tqdm import tqdm
import matplotlib.pyplot as plt

import pickle

# oversampling
# pip install imblearn
from imblearn.over_sampling import RandomOverSampler

with open('./3/train_34614.pkl','rb') as f:
  corpus = pickle.load(f)
with open('./3/no_idiom_30000.pkl','rb') as f:
  no_idiom = pickle.load(f)

corpus = corpus[corpus['Label']==1]

new_df = pd.concat([corpus, no_idiom])
new_df = new_df.sample(frac=1)
new_df.reset_index(drop=True, inplace=True)

train, test = train_test_split(new_df, test_size=0.2, random_state=42)
train, val = train_test_split(train, test_size=0.1, random_state=42)

oversample = RandomOverSampler()
ko_t = train.ko.to_numpy().reshape(-1, 1)
label_t = train.Label.to_numpy().reshape(-1, 1)

x_over, y_over = oversample.fit_resample(ko_t, label_t)

data = pd.DataFrame({'ko':x_over.reshape(-1)})
target = pd.DataFrame({'Label':y_over.reshape(-1)})

data = data['ko']
target = target['Label']

dx_train,dx_test, dy_train, dy_test = train_test_split(data, target, test_size=0.2, stratify=target, random_state=42)

MY_PATH = '/content/drive/MyDrive/Colab Notebooks/multicampus/Idiom Classifier/4.KoGPT2/'
MODEL_PATH = MY_PATH + 'gpt_ckpt'
TOKENIZER_PATH = MY_PATH + 'gpt_ckpt/gpt2_kor_tokenizer.spiece'

tokenizer = SentencepieceTokenizer(TOKENIZER_PATH, num_best=0, alpha=0)
detokenizer = SentencepieceDetokenizer(TOKENIZER_PATH)
vocab = nlp.vocab.BERTVocab.from_sentencepiece(TOKENIZER_PATH,
                                               mask_token = None,
                                               sep_token = None,
                                               cls_token = None,
                                               unknown_token = '<unk>',
                                               padding_token = '<pad>',
                                               bos_token = '<s>',
                                               eos_token = '</s>')

MAX_LEN = 60
def build_data(x_data, y_label):
    data_sents = []
    data_labels = []

    for sent, label in zip(x_data, y_label):
        tokenized_text = vocab[tokenizer(sent)]

        tokens = [vocab[vocab.bos_token]]
        tokens += pad_sequences([tokenized_text], 
                                MAX_LEN, 
                                value=vocab[vocab.padding_token], 
                                padding='post').tolist()[0] 
        tokens += [vocab[vocab.eos_token]]

        data_sents.append(tokens)
        data_labels.append(label)

    return np.array(data_sents, dtype=np.int64), np.array(data_labels, dtype=np.int64).reshape(-1, 1)

x_train, y_train = build_data(dx_train, dy_train)
x_test, y_test = build_data(dx_test, dy_test)

x_train.shape, y_train.shape, x_test.shape, y_test.shape

word2idx = {k:v for k, v in vocab.token_to_idx.items()}
idx2word = {v:k for k, v in word2idx.items()}

gpt_model = TFGPT2LMHeadModel.from_pretrained(MODEL_PATH)
gpt_model.summary()

gpt_model = TFGPT2LMHeadModel.from_pretrained(MODEL_PATH)
gpt_model.summary()

gpt_model.trainable = True
gpt_model.summary()

x_input = Input(batch_shape = (None, MAX_LEN + 2), dtype = tf.int32)

output_gpt = gpt_model(x_input)[0][:, -1]

y_output = Dense(1, activation = 'sigmoid')(output_gpt)
model = Model(x_input, y_output)
model.compile(loss = 'binary_crossentropy', optimizer = Adam(learning_rate = 2e-5))
model.summary()

hist = model.fit(x_train, y_train, validation_data = (x_test, y_test), epochs=3, batch_size=32)

gpt_model.trainable = False
gpt_model.summary()

model = Model(x_input, y_output)
model.compile(loss = 'binary_crossentropy', optimizer = Adam(learning_rate = 1e-6))
model.summary()

hist = model.fit(x_train, y_train, validation_data = (x_test, y_test), epochs=3, batch_size=32)

f = open('test_3000.pkl', 'rb')
test = pickle.load(f)
len(test)

text, _ = build_data(test['ko'], np.zeros(len(test)))

pred = model.predict(text)
y_pred = np.where(pred > 0.5, 1, 0)

from sklearn.metrics import accuracy_score, recall_score, precision_score, f1_score, confusion_matrix

print("accuracy:", accuracy_score(label, y_pred))
print("precision:", precision_score(label, y_pred))
print("recall:", recall_score(label, y_pred))
print("F1-Score:", f1_score(label, y_pred))