from collections import Counter
import operator
from scipy import spatial
import gensim.models as gsm
import numpy as np
from imdb import IMDb
import pandas as pd

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
		print("It doesn't exist")
		return {}
	for emoji in e2v.vocab.keys():
		em2vec = e2v[emoji]
		similar[emoji] = 1 - spatial.distance.cosine(vector, em2vec)
	# emojis = dict(sorted(similar.items(), key=operator.itemgetter(1), reverse=True)[:10])
	# print(emojis)
	return similar

def preprocess(word):
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
	word = word.replace(":", "")
	word = word.replace("'s", "")
	word = word.replace(",", "")
	word = word.replace(".", "")
	word = word.replace("!", "")
	word = word.replace("-", "")
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
		movie = el["title"]
	# vocab += movie.split()
	# movie = movie.lower()
	# vocab += movie.split()
		sp = movie.split()
		sp = [preprocess(x) for x in sp]
		movie = " ".join(sp)
		print(movie)
		similar = get_emojis(movie)
		emojis += Counter(similar)
		print()
		movie = movie.lower()
		sp = movie.split()
		sp = [preprocess(x) for x in sp]
		movie = " ".join(sp)
		print(movie)
		similar_small = get_emojis(movie)
		print()
		emojis += Counter(similar_small)
	emojis = dict(emojis)
	emojis = dict(sorted(emojis.items(), key=operator.itemgetter(1), reverse=True)[:10])
	return emojis

# df = pd.read_csv("imdb_ids.csv")
# for i in range(1, 11):
# 	col = "Emoji " + str(i)
# 	df[col] = ""
df = pd.read_csv("Emojis.csv")

for i, row in df.iterrows():
	if i < 68:
		continue
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