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


def reduce(key, values):
    word_count = 0
    stemmed_words_count_dict = {}
    lemmatized_words_count_dict = {}

    for line_counts in values:
        word_count += line_counts["word_count"]
        for stemm in line_counts["stemmed_words"]:
            stemmed_word, count = stemm
            if stemmed_word not in stemmed_words_count_dict:
                stemmed_words_count_dict[stemmed_word] = 0
            stemmed_words_count_dict[stemmed_word] += count
        for lemma in line_counts["lemmatized_words"]:
            lemmatized_word, count = lemma
            if lemmatized_word not in lemmatized_words_count_dict:
                lemmatized_words_count_dict[lemmatized_word] = 0
            lemmatized_words_count_dict[lemmatized_word] += count
    out = f"{key}, {word_count}, {json.dumps(stemmed_words_count_dict, separators=(',', ':'))}, " + \
        f"{json.dumps(lemmatized_words_count_dict, separators=(',', ':'))}"
    return key, out


def generate_output(lines):
    global_stemmed_word_dict = {}
    global_lemm_word_dict = {}
    rows = []

    for line in lines:
        print(line)

        stemmed_words_count_dict = json.loads(
            "{"+line.split("{")[1].strip()[:-1])
        lemmatized_words_count_dict = json.loads(
            "{"+line.split("{")[2].strip())

        for w in stemmed_words_count_dict:
            if w not in global_stemmed_word_dict:
                global_stemmed_word_dict[w] = 0
            global_stemmed_word_dict[w] += stemmed_words_count_dict[w]

        for w in lemmatized_words_count_dict:
            if w not in global_lemm_word_dict:
                global_lemm_word_dict[w] = 0
            global_lemm_word_dict[w] += lemmatized_words_count_dict[w]

    for w in sorted(global_stemmed_word_dict.keys()):
        row = ["S", w, global_stemmed_word_dict[w]]
        rows.append(row)

    for w in sorted(global_lemm_word_dict.keys()):
        row = ["L", w, global_lemm_word_dict[w]]
        rows.append(row)

    with open('output.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerows(rows)


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
