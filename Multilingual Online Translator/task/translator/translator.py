from enum import Enum

import requests
from argparse import ArgumentParser
from bs4 import BeautifulSoup


class DateFetcher:
    session = requests.Session()

    def __init__(self, link):
        try:
            self.soup_content = None
            response = self.session.get(link, headers={'User-Agent': 'Mozilla/5.0'})
            if response.status_code == 200:
                # print(f"{response.status_code} OK")
                self.soup_content = BeautifulSoup(response.content, "html.parser")
        except ConnectionError:
            print("Something wrong with your internet connection")

    def get_words(self):
        try:
            words_dom = self.soup_content.find('div', attrs={'id': 'translations-content'})
            words = []
            for word in words_dom.find_all('a'):
                words.append(word.text.strip())
            return words
        except AttributeError:
            return []

    def get_sentences(self):
        try:
            sentences_dom = self.soup_content.find('section', attrs={'id': "examples-content"})
            sentences = []
            for sentence_dom in sentences_dom.find_all('div', attrs={'class': 'example'}):
                source = sentence_dom.find('div', attrs={'class': 'src'}).text.strip()
                target = sentence_dom.find('div', attrs={'class': 'trg'}).text.strip()
                sentences.append((source, target))
            return sentences
        except AttributeError:
            return []


class Language(Enum):
    ARABIC = 1
    GERMAN = 2
    ENGLISH = 3
    SPANISH = 4
    FRENCH = 5
    HEBREW = 6
    JAPANESE = 7
    DUTCH = 8
    POLISH = 9
    PORTUGUESE = 10
    ROMANIAN = 11
    RUSSIAN = 12
    TURKISH = 13

    @classmethod
    def get_language(cls, text):
        for lang in cls:
            if lang.name == text.upper():
                return lang
        return None


class Translator:
    translate_url_prefix = "https://context.reverso.net/translation/"

    def __init__(self, src: Language, dst: Language):
        self.src = src
        self.dst = dst
        self.translate_url = f"{self.translate_url_prefix}{self.src.name.lower()}-{self.dst.name.lower()}/"

    def translate(self, text, word_count=5, sentence_pair_count=5, save_to_file=False):
        lines = []
        data_fetcher = DateFetcher(f"{self.translate_url}{text}")
        lines.append(f"{self.dst.name.capitalize()} Translations:")
        words = data_fetcher.get_words()
        if not words:
            print(f"Sorry, unable to find {text}")
            exit()
        for index, word in enumerate(words):
            if index == word_count:
                break
            lines.append(word)
        lines.append(f"{self.dst.name.capitalize()} Examples:")
        sentences = data_fetcher.get_sentences()
        for index, sentence in enumerate(sentences):
            if index == sentence_pair_count:
                break
            lines.append(sentence[0])
            lines.append(sentence[1])
        self.print(lines)
        if save_to_file:
            self.write_to_file(f"{text}.txt", lines)

    @staticmethod
    def print(lines):
        for line in lines:
            print(line)

    @staticmethod
    def write_to_file(filename, lines):
        with open(filename, 'a') as f:
            for line in lines:
                f.write(line + '\n')


def main():
    parser = ArgumentParser(description="""Hello, you're welcome to the translator. Translator supports:
1. Arabic
2. German
3. English
4. Spanish
5. French
6. Hebrew
7. Japanese
8. Dutch
9. Polish
10. Portuguese
11. Romanian
12. Russian
13. Turkish
""")
    # choices = ["arabic",
    #            "german",
    #            "english",
    #            "spanish",
    #            "french",
    #            "hebrew",
    #            "japanese",
    #            "dutch",
    #            "polish",
    #            "portuguese",
    #            "romanian",
    #            "russian",
    #            "turkish"]
    # parser.add_argument("source_lang", choices=choices)
    # parser.add_argument("dest_lang", choices=choices + ["all"])
    parser.add_argument("source_lang")
    parser.add_argument("dest_lang")
    parser.add_argument("word_to_translate")
    args = parser.parse_args()
    source_lang = Language.get_language(args.source_lang)
    dest_lang = Language.get_language(args.dest_lang)
    word_to_translate = args.word_to_translate
    if args.dest_lang == "all":
        for lang in Language:
            if lang == source_lang:
                continue
            dest_lang = lang
            translator = Translator(source_lang, dest_lang)
            translator.translate(args.word_to_translate, word_count=1, sentence_pair_count=1, save_to_file=True)
    elif source_lang is None or dest_lang is None:
        print(f"Sorry, the program doesn't support {args.source_lang if source_lang is None else args.dest_lang}")
        exit()
    else:
        translator = Translator(source_lang, dest_lang)
        translator.translate(word_to_translate, save_to_file=True)


if __name__ == '__main__':
    main()
