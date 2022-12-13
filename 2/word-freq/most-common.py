import json


def sort_word_frequency(file_name):
    with open(filename) as data_file:
        chapters_dict = json.load(data_file)
    df = {}
    for chapter in chapters_dict:
        for word in chapters_dict[chapter]:
            if word not in df:
                df[word] = 0
            df[word] = df[word] + chapters_dict[chapter][word]
    return {k: v for k, v in sorted(df.items(), key=lambda item: item[1])}


if __name__ == "__main__":
    filename = "chapter_word_occurences.json"
    df = sort_word_frequency(filename)
    sorted_words_by_freq = list(df.keys())
    sorted_words_by_freq.reverse()
    print(sorted_words_by_freq[:11])
