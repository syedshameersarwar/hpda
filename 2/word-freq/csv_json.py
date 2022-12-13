import re
from cleantext import clean
import csv
import json


def checkIfRomanNumeral(numeral):
    numeral = numeral.upper()
    validRomanNumerals = ["M", "D", "C", "L", "X", "V", "I", "(", ")"]
    valid = True
    for letters in numeral:
        if letters not in validRomanNumerals:
            valid = False
            break
    return valid


def read_chapters():
    with open('mobydick.txt') as book:
        content = str(book.read())
        chapters = re.split("CHAPTER ", content, flags=re.IGNORECASE)
        chapters.pop(0)
        chapters.pop(0)
        filtered_chapters = []
        filtered_names = []
        for i in range(len(chapters)):
            if not checkIfRomanNumeral(chapters[i].split('\n')[0].strip()):
                filtered_chapters[len(
                    filtered_chapters)-1] = filtered_chapters[len(filtered_chapters)-1] + ' ' + chapters[i]
            else:
                possible_name = chapters[i].split('\n')[2].strip()
                if not len(possible_name) > 0:
                    possible_name = chapters[i].split('\n')[4].strip()
                filtered_chapters.append(chapters[i])
                filtered_names.append(possible_name)

        filtered_chapters = [clean(c, no_line_breaks=True, no_punct=True)
                             for c in filtered_chapters]
        return filtered_chapters, filtered_names


def generate_csv_and_json(chapters_content, chapter_names):
    rows = []
    fields = ['chapter_name', 'chapter_length', 'unique_words']
    rows.append(fields)
    df = {}
    for i in range(len(chapter_names)):
        words = chapters_content[i].split()
        row = [chapter_names[i], len(words)]
        unique_words = set(words)
        for word in unique_words:
            if df.get(chapter_names[i], None) is None:
                df[chapter_names[i]] = {}
            df[chapter_names[i]][word] = words.count(word)

        row.append(len(unique_words))
        rows.append(row)

    filename = "chapter_unique_words.csv"
    with open(filename, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(rows)

    with open('chapter_word_occurences.json', 'w', encoding='utf-8') as f:
        json.dump(df, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    chapters_content, chapters_name = read_chapters()
    generate_csv_and_json(chapters_content, chapters_name)
