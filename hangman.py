import copy
import random


class Guesser:
    letters = list("etarionshdluwmfcgypbkvjxqz")  # letters in order of frequency

    defaults = list("eaaaaeeeeeeiiiiiiiiioooee")  # first guess for different length words (hardcoded for efficency)

    @classmethod
    def ask_length(cls):  # take input of and check validity of word length
        while True:
            word_len = input("What is the length of your word? ")
            try:
                return int(word_len)  # if integer (5)
            except:
                if set(word_len) <= set("-"):  # if string of blanks (------)
                    return len(word_len)
                elif set(word_len) <= set(cls.letters):  # if word (triggers autoplay)
                    return word_len
                print("That isn't a valid word length...")

    def __init__(self, length):  # creates a guesser-type with a given word length
        self.letters = copy.copy(self.letters)

        self.word_len = length
        self.create_word_list(self.word_len)

        self.cipher = "-" * self.word_len
        self.errors = 0

        self.check_words()  # check for immediate success

        if self.word_len <= len(self.defaults):  # use hardcoded first guess if possible
            self.guess = self.defaults[self.word_len - 1]
        else:
            self.decide_letter()

    def create_word_list(self, length):  # gets the list of words with the given length (hardcoded for efficency)
        words = open("english_words.txt", "r").read().split("\n \n")
        if words[length - 1]:
            self.words = words[length - 1].split("\n")
        else:
            self.words = list()

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

    def update(self, word):
        if word is None:
            self.ask_letter()
        else:
            self.build_letter()

        self.update_cipher()
        if "=" not in self.indices:
            self.errors += 1

        print("\nCurrent word: {}\nErrors: {}".format(self.cipher, self.errors))
        words = self.get_words(self.guess, self.indices)

        if MAX_PRINTED_WORDS:
            if len(words) <= MAX_PRINTED_WORDS:
                print("Current possible words: {}".format(", ".join(words)))
        elif len(words) in (0, 1):
            print("Previous possible words: {}".format(", ".join(self.words)))

        self.words = words
        if self.check_words():
            return True
        self.decide_letter()

    @staticmethod
    def prune_database():
        allowed_letters = list("abcdefghijklmnopqrstuvwxyz")

        words = open("english_words.txt", "r").read().split("\n")

        valid_words = list()
        for word in words:
            if set(word) <= set(allowed_letters):
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

MAX_PRINTED_WORDS = 5

while True:
    length = Guesser.ask_length()
    if type(length) != int:
        word, length = length, len(length)
    else:
        word = None

    guesser = Guesser(length)

    done = False

    while not done:
        done = guesser.update(word)

    print("\nNEW GAME!\n")