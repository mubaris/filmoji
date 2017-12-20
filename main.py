from collections import Counter
import operator
from scipy import spatial
import gensim.models as gsm
import numpy as np
from imdb import IMDb
import pandas as pd
from num2words import num2words

contra = {
  "ain't": "am not",
  "aren't": "are not",
  "can't": "cannot",
  "can't've": "cannot have",
  "'cause": "because",
  "could've": "could have",
  "couldn't": "could not",
  "couldn't've": "could not have",
  "didn't": "did not",
  "doesn't": "does not",
  "don't": "do not",
  "hadn't": "had not",
  "hadn't've": "had not have",
  "hasn't": "has not",
  "haven't": "have not",
  "he'd": "he would",
  "he'd've": "he would have",
  "he'll": "he will",
  "he'll've": "he will have",
  "he's": "he is",
  "how'd": "how did",
  "how'd'y": "how do you",
  "how'll": "how will",
  "how's": "how is",
  "I'd": "I would",
  "I'd've": "I would have",
  "I'll": "I will",
  "I'll've": "I will have",
  "I'm": "I am",
  "I've": "I have",
  "isn't": "is not",
  "it'd": "it had",
  "it'd've": "it would have",
  "it'll": "it will",
  "it'll've": "it will have",
  "it's": "it is",
  "let's": "let us",
  "ma'am": "madam",
  "mayn't": "may not",
  "might've": "might have",
  "mightn't": "might not",
  "mightn't've": "might not have",
  "must've": "must have",
  "mustn't": "must not",
  "mustn't've": "must not have",
  "needn't": "need not",
  "needn't've": "need not have",
  "o'clock": "of the clock",
  "oughtn't": "ought not",
  "oughtn't've": "ought not have",
  "shan't": "shall not",
  "sha'n't": "shall not",
  "shan't've": "shall not have",
  "she'd": "she would",
  "she'd've": "she would have",
  "she'll": "she will",
  "she'll've": "she will have",
  "she's": "she is",
  "should've": "should have",
  "shouldn't": "should not",
  "shouldn't've": "should not have",
  "so've": "so have",
  "so's": "so is",
  "that'd": "that would",
  "that'd've": "that would have",
  "that's": "that is",
  "there'd": "there had",
  "there'd've": "there would have",
  "there's": "there is",
  "they'd": "they would",
  "they'd've": "they would have",
  "they'll": "they will",
  "they'll've": "they will have",
  "they're": "they are",
  "they've": "they have",
  "to've": "to have",
  "wasn't": "was not",
  "we'd": "we had",
  "we'd've": "we would have",
  "we'll": "we will",
  "we'll've": "we will have",
  "we're": "we are",
  "we've": "we have",
  "weren't": "were not",
  "what'll": "what will",
  "what'll've": "what will have",
  "what're": "what are",
  "what's": "what is",
  "what've": "what have",
  "when's": "when is",
  "when've": "when have",
  "where'd": "where did",
  "where's": "where is",
  "where've": "where have",
  "who'll": "who will",
  "who'll've": "who will have",
  "who's": "who is",
  "who've": "who have",
  "why's": "why is",
  "why've": "why have",
  "will've": "will have",
  "won't": "will not",
  "won't've": "will not have",
  "would've": "would have",
  "wouldn't": "would not",
  "wouldn't've": "would not have",
  "y'all": "you all",
  "y'alls": "you alls",
  "y'all'd": "you all would",
  "y'all'd've": "you all would have",
  "y'all're": "you all are",
  "y'all've": "you all have",
  "you'd": "you had",
  "you'd've": "you would have",
  "you'll": "you you will",
  "you'll've": "you you will have",
  "you're": "you are",
  "you've": "you have"
}

print("Loading Emoji2Vec")
e2v = gsm.KeyedVectors.load_word2vec_format("models/emoji2vec.bin", binary=True)
print("Loading Word2Vec")
w2v = gsm.KeyedVectors.load_word2vec_format("models/w2v.bin", binary=True)

def get_emojis(movie):
	similar = {}
	try:
		movie = movie.split()
		if len(movie) == 1:
			movie = movie[0]
			vector = w2v[movie]
		else:
			vector = w2v[movie]
			vector = np.sum(vector, axis=0)
		#vector = w2v[movie]
	except:
		print(movie)
		print("It doesn't exist")
		print()
		return {}
	for emoji in e2v.vocab.keys():
		em2vec = e2v[emoji]
		similar[emoji] = 1 - spatial.distance.cosine(vector, em2vec)
	# emojis = dict(sorted(similar.items(), key=operator.itemgetter(1), reverse=True)[:10])
	# print(emojis)
	return similar

def preprocess(word, signal=True):
	if word in contra:
		word = contra[word]
	if word.startswith("(") and word.endswith(")"):
		word = ""
	if len(word) == 1 and word == "a":
		word = "A"
	if len(word) == 2 and word == "to":
		word = "To"
	if len(word) == 2 and word == "of":
		word = "Of"
	if word == "and":
		word = "And"
	if word == "i'm":
		word = "I'm"
	if word == "i":
		word = "I"
	word = word.replace("()", "")
	word = word.replace(":", "")
	word = word.replace("'s", "")
	word = word.replace(",", "")
	word = word.replace(".", "")
	word = word.replace("!", "")
	if signal:
		word = word.replace("-", "")
	else:
		word = word.replace("-", " ")
	word = word.replace("?", "")
	word = word.replace("&", "And")
	word = word.replace("in'", "ing")
	word = word.replace("+", "plus")
	return word

def emoji_actor(id):
	ia = IMDb()
	actor = ia.get_person(id, info="filmography")
	emojis = Counter()
	try:
		films = actor["actor"]
	except:
		films = actor["actress"]
	for el in films:
		if el.data["kind"] != "movie":
			continue
		movie = el["title"]
		movie_small = movie.lower()
	# vocab += movie.split()
	# movie = movie.lower()
	# vocab += movie.split()
		sp = movie.split()
		sp = [preprocess(x) for x in sp]
		for i, el in enumerate(sp):
			try:
				sp[i] = int(el)
				sp[i] = num2words(sp[i])
			except:
				continue
		movie = " ".join(sp)
		sp = movie.split()
		sp = [preprocess(x, False) for x in sp]
		movie = " ".join(sp)
		#print(movie)
		similar = get_emojis(movie)
		emojis += Counter(similar)
		#print()
		movie = movie_small
		sp = movie.split()
		sp = [preprocess(x) for x in sp]
		for i, el in enumerate(sp):
			try:
				sp[i] = int(el)
				sp[i] = num2words(sp[i])
			except:
				continue
		movie = " ".join(sp)
		sp = movie.split()
		sp = [preprocess(x, False) for x in sp]
		movie = " ".join(sp)
		#print(movie)
		similar_small = get_emojis(movie)
		#print()
		emojis += Counter(similar_small)
	emojis = dict(emojis)
	emojis = dict(sorted(emojis.items(), key=operator.itemgetter(1), reverse=True)[:10])
	return emojis

df = pd.read_csv("imdb_ids.csv")
for i in range(1, 11):
	col = "Emoji " + str(i)
	df[col] = ""
# df = pd.read_csv("Emojis.csv")

for i, row in df.iterrows():
	print(row["Name"])
	actor = row["ID"][2:]
	emojis = dict(emoji_actor(actor))
	print(emojis)
	emojis = list(emojis.keys())
	for j in range(10):
		col = "Emoji " + str(j+1)
		df.set_value(i, col, emojis[j])
	df.to_csv("Emojis.csv")

df.to_csv("Emojis.csv")