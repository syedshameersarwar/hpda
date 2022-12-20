#!/usr/bin/python3
import json
import csv
import sys
import logging


def read_input():
    inn = sys.stdin.read().split()
    file, list_of_dicts = inn[0], inn[1:]
    keys = []
    for l in list_of_dicts:
        if l != file:
            for el in json.loads(l):
                keys.append(el)
    return file, keys


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
    key, values = read_input()
    file, out = reduce(key, values)
    generate_output([out])


if __name__ == "__main__":
    driver()
