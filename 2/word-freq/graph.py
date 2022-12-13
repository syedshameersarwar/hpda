import re
from cleantext import clean
import sys
import matplotlib.pyplot as plt

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



def calculate_freq(word, chapters):
    freq_list = []
    for chap in chapters:
        words = chap.strip().split()
        chap_word_count = words.count(word)
        freq_list.append(chap_word_count)
    return freq_list


def plot_freq(freq_list):
    plt.bar(range(1, len(freq_list)+1), freq_list, 0.35)
    plt.ylabel("selected word")
    plt.xlabel("occurrence over all chapters")
    plt.show()


if __name__ == "__main__":
    word = sys.argv[1]
    chapters, _ = read_chapters()
    freq_list = calculate_freq(word, chapters)
    plot_freq(freq_list)
