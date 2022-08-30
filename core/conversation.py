""" 1
"""

from pickle import load

from keras.models import load_model
from keras.preprocessing.text import Tokenizer
from keras_preprocessing.sequence import pad_sequences
from numpy import argmax


# load a clean dataset
def load_clean_sentences(filename):
	return load(open(filename, 'rb'))


# fit a tokenizer
def create_tokenizer(lines):
	tokenizer = Tokenizer(char_level=False)
	tokenizer.fit_on_texts(lines)
	return tokenizer


# max sentence length
def max_length(lines):
	return max(len(line.split()) for line in lines)


# map an integer to a word
def word_for_id(integer, tokenizer):
	for word, index in tokenizer.word_index.items():
		if index == integer:
			return word
	return None


# generate target given source sequence
def predict_sequence(model, tokenizer, source):
	prediction = model.predict(source, verbose=0)[0]
	integers = [argmax(vector) for vector in prediction]
	target = list()
	for i in integers:
		word = word_for_id(i, tokenizer)
		if word is None:
			break
		target.append(word)
	return ' '.join(target)


# translate
def translate(model, sources):
	predicted = list()
	for i, source in enumerate(sources):
		# translate encoded source text
		source = source.reshape((1, source.shape[0]))
		translation = predict_sequence(model, all_tokenizer, source)
		print(translation)
		predicted.append(translation.split())


# load datasets
dataset = load_clean_sentences('../model/both.pkl')
reshaped_dataset = dataset.reshape(-1, 1)

# prepare tokenizer
all_tokenizer = create_tokenizer(reshaped_dataset[:, 0])
all_vocab_size = len(all_tokenizer.word_index) + 1
all_length = max_length(reshaped_dataset[:, 0])

# load model
model = load_model('../model/model.h5')

# Setting up the chat
while True:
	query = (input(str("> ")))

	if query == '/exit':
		break

	query = query.strip().split('\n')

	# we tokenize
	X = all_tokenizer.texts_to_sequences(query)
	X = pad_sequences(X, maxlen=all_length, padding='post')

	# find reply and print it out
	translate(model, X)
