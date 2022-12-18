import sys
import json
import csv

from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer
from nltk.stem.snowball import SnowballStemmer

tokenizer = RegexpTokenizer(r'\w+')
snow_stemmer = SnowballStemmer(language='english')
lemmatizer = WordNetLemmatizer()

accumulator = {}


def emit(key, value):
    global accumulator
    if key not in accumulator:
        accumulator[key] = []
    accumulator[key].append(value)


def read_input():
    files = []
    if len(sys.argv) > 1:
        for file in sys.argv[1:]:
            with open(file, 'r') as f:
                files.append({"name": file, "lines": f.readlines()})
    else:
        files.append({"name": "stdin", "lines": sys.stdin.readlines()})
    return files


def map(key, value):
    line = value
    words = tokenizer.tokenize(line)
    line_stem_words = [snow_stemmer.stem(w) for w in words]
    line_lemmatized_words = [lemmatizer.lemmatize(w) for w in words]
    line_word_count = len(words)
    line_stemmed_list = [
        (w, line_stem_words.count(w)) for w in set(line_stem_words)]
    line_lemmatized_list = [
        (w, line_lemmatized_words.count(w)) for w in set(line_lemmatized_words)]
    emit(key, {"word_count": line_word_count, "stemmed_words": line_stemmed_list,
         "lemmatized_words": line_lemmatized_list})


def driver():
    global accumulator
    files = read_input()
    for file in files:
        key = file["name"]
        for line in file["lines"]:
            map(key, line)
    for key in accumulator:
        sorted_values = accumulator[key]
        print(key, json.dumps(sorted_values, separators=(',', ':')))


if __name__ == "__main__":
    driver()
