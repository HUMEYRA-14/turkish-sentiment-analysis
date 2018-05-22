import time, sys
import Util

def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn

from sklearn.neighbors import KNeighborsClassifier
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import Pipeline
from sklearn import metrics

from pathlib import Path
import numpy as np
from spell_correction import correction

src_folder = Path("./")
#stopwords = Util.read_file(Path(src_folder / "stopwords")).split("\n")
stopwords = []

def preprocess(text):
	delete_list = [",", "’"]
	tweet = Util.delete_characters_space(text, delete_list)
	word_list = tweet.split()
	word_list = [ Util.stem_word(correction.correction(Util.remove_punct(Util.remove_repeating_char(Util.remove_with_regex(word))))) for word in word_list ]
	word_list = [word for word in word_list if len(word) > 1]
	word_list = Util.remove_words(word_list, stopwords)

	sentence = ""
	for word in word_list:
		sentence = sentence + " " + word
	return(sentence)

start = time.time()

data = Util.open_pickle("data")
labels = Util.open_pickle("labels")

categories = ['-1', '0', '1']

text_clf = ""

if len(sys.argv) == 3:
	if sys.argv[2] == "bigram":
		neighbor_count = int(sys.argv[1])
		text_clf = Pipeline([('vect', CountVectorizer(ngram_range=(1, 2),
                      token_pattern=r'\b\w+\b', min_df=1)),
                     ('tfidf', TfidfTransformer()),
                     ('clf', KNeighborsClassifier(n_neighbors=neighbor_count)),
		])
	else:
		print("Usage: python3 Test_data_KNN.py <neighbor_count>")
		print("Usage (bigram): python3 Test_data_KNN.py <neighbor_count> bigram")
		sys.exit()
elif len(sys.argv) == 2:
	neighbor_count = int(sys.argv[1])
	text_clf = Pipeline([('vect', CountVectorizer()),
                     ('tfidf', TfidfTransformer()),
                     ('clf', KNeighborsClassifier(n_neighbors=neighbor_count)),
	])
else:
	print("Usage: python3 Test_data_KNN.py <neighbor_count>")
	print("Usage (bigram): python3 Test_data_KNN.py <neighbor_count> bigram")
	sys.exit()

text_clf.fit(data, labels)

docs_test = Util.read_file("tests").split("\n")
docs_test_processed = [preprocess(sen.lower()) for sen in docs_test ]
predicted = text_clf.predict(docs_test_processed)

#actual = Util.read_file("tests_values").split("\n")
#right = 0

#count = 0
for p in predicted:
	#print("Sentence: " + docs_test[count])
	#print("Processed sentence: " + docs_test_processed[count])
	#print("Predicted: " + categories[p] + "\n")
	print(categories[p])
	#if int(actual[count]) == int(categories[p]):
	#	right += 1
	#count += 1

#print(np.mean(predicted == actual))
#print(metrics.classification_report(actual, predicted, target_names=categories))
#print(metrics.confusion_matrix(actual, predicted))

#print("Accuracy: " + str((float(right)/len(actual)) * 100))

end = time.time()
#print("Elapsed time: " + str(end - start) + " seconds")