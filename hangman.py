import copy
import random


class Guesser:
    letters = list("etarionshdluwmfcgypbkvjxqz")

    defaults = list("eaaaaeeeeeeiiiiiiiiioooee")

    @classmethod
    def ask_length(cls):
        while True:
            word_len = input("What is the length of your word? ")
            try:
                return int(word_len)
            except:
                if set(word_len) <= set("-"):
                    return len(word_len)
                elif set(word_len) <= set(cls.letters):
                    return word_len
                print("That isn't a valid word length...")

    @classmethod
    def get_all_words(cls, length):
        cls.words = list()
        words = open("english_words.txt", "r").read().split("\n \n")
        if words[length - 1]:
            return words[length - 1].split("\n")
        else:
            return list()

    def __init__(self, length, words):
        self.word_len = length
        self.cipher = "-" * length
        self.errors = 0
        self.words = words
        if length <= len(self.defaults):
            self.guess = self.defaults[length - 1]
        else:
            self.decide_letter()
        self.check_words()

    def decide_letter(self):
        min_length = len(self.words)
        self.guess = self.letters[0]
        string = "Thinking"
        for letter in self.letters:
            print(string, end="\r")
            current_length = len(self.get_words(letter, "-" * self.word_len))
            if current_length < min_length and current_length != 0:
                min_length = current_length
                self.guess = letter
            string += "."
        print(" " * 100, end="\r")

    def ask_letter(self):
        accurate = False
        while not accurate:

            example = list()
            for _ in range(self.word_len):
                example.append(("-", "=")[random.randint(0, 1)])
            example = "".join(example)

            response = input("\nIs '{}' in the word? eg({}): ".format(self.guess, example))

            if len(response) <= self.word_len:
                response += "-" * (self.word_len - len(response))
                if set(response) <= set(["-", "="]):
                    accurate = True
                    for index, character in enumerate(response):
                        currently_accurate = (character == "=") and (self.cipher[index] == "-") or (character != "=")
                        accurate = accurate and currently_accurate
                    if not accurate:
                        print("Character space already taken...")
                else:
                    print("Please only include =s and -s...")
            else:
                print("Please enter a valid length string...")

        self.indices = list(response)
        self.letters.remove(self.guess)

    def build_letter(self):
        print("\nGuess: {}".format(self.guess))
        self.indices = str()
        for character in word:
            self.indices += ("-", "=")[character == self.guess]

    def update_cipher(self):
        cipher = list(self.cipher)
        for index, truth in enumerate(self.indices):
            if truth == "=":
                cipher[index] = self.guess
        self.cipher = "".join(cipher)

    def get_words(self, letter, indices):
        words = copy.copy(self.words)
        removed_words = list()
        for word in words:
            if indices == "-" * self.word_len:
                if letter in word:
                    removed_words.append(word)
            else:
                for index, truth in enumerate(indices):
                    if (word[index] == letter) != (truth == "="):
                        removed_words.append(word)
                        break

        for word in removed_words:
            words.remove(word)

        return words

    def check_words(self):
        if len(self.words) == 1:
            print("Your word is '{}'!".format(self.words[0]))
            return True
        elif len(self.words) == 0:
            print("I don't know your word...")
            return True

    def update(self, word):
        if word is None:
            self.ask_letter()
        else:
            self.build_letter()
        if "=" not in self.indices:
            self.errors += 1
        self.update_cipher()
        print("\nCurrent word: {}\nErrors: {}".format(self.cipher, self.errors))
        words = self.get_words(self.guess, self.indices)
        if len(words) in (0, 1):
            print("Previous possible words: {}".format(", ".join(self.words)))
        self.words = words
        if self.check_words():
            return True
        self.decide_letter()

    @staticmethod
    def prune_database():
        letters = list("abcdefghijklmnopqrstuvwxyz")

        words = open("english_words.txt", "r").read().split("\n")

        valid_words = list()
        for word in words:
            if set(word) <= set(letters):
                valid_words.append(word.lower())

        valid_words = list(set(valid_words))
        valid_words.sort()
        valid_words.sort(key = len)

        current_len = 1
        wordset = list()
        for word in valid_words:
            if current_len != len(word):
                wordset.append(" ")
                current_len = len(word)
            wordset.append(word)

        open("english_words.txt", "w").write("\n".join(wordset))


#Guesser.prune_database()

while True:
    length = Guesser.ask_length()
    if type(length) != int:
        word, length = length, len(length)
    else:
        word = None

    words = Guesser.get_all_words(length)
    guesser = Guesser(length, words)

    done = False

    while not done:
        done = guesser.update(word)

    print("\nNEW GAME!\n")