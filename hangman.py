import copy
import time
import random


class Guesser:
    letters = list("etarionshdluwmfcgypbkvjxqz")  # letters in order of frequency

    defaults = list("eaaaaeeeeeeiiiiiiiiioooee")  # first guess for different length words (hardcoded for efficency)

    @classmethod
    def ask_length(cls):  # take input and check validity of word length
        while True:
            word_len = input("What is the length of your word? ")
            try:
                return int(word_len)  # if integer (5)
            except:
                if set(word_len) <= set(LETTER_CHARACTERS[0]):  # if string of blanks (------)
                    return len(word_len)
                elif set(word_len) <= set(cls.letters):  # if word (triggers autoplay)
                    return word_len
                print("That isn't a valid word length...")

    def __init__(self, length):  # creates a guesser-type with a given word length
        self.letters = copy.copy(self.letters)  # class attribute is mutable by default

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
        words = open(WORDS_FILE, "r").read().split("\n \n")
        if words[length - 1]:
            self.words = words[length - 1].split("\n")
        else:
            self.words = list()

    def ask_letter(self):  # take input and check validity of letter answer
        accurate = False
        while not accurate:  # repeat request until success

            example = list()  # create example string
            for _ in range(self.word_len):
                example.append(LETTER_CHARACTERS[random.randint(0, 1)])
            example = "".join(example)

            response = input("\nIs '{}' in the word? eg({}): ".format(self.guess, example))

            if len(response) <= self.word_len:  # fill remaining blanks after response
                response += LETTER_CHARACTERS[0] * (self.word_len - len(response))
                if set(response) <= set(LETTER_CHARACTERS):  # test response only contains true/false characters
                    accurate = True
                    for index, character in enumerate(response):  # test for no overlaps with current string
                        is_letter = character == LETTER_CHARACTERS[1]
                        is_free = self.cipher[index] == "-"
                        accurate = accurate and is_letter <= is_free  # a implies b
                    if not accurate:  # if any errors are found, accurate becomes false
                        print("Character space already taken...")
                else:
                    print("Please only include {}s and {}s...".format(*LETTER_CHARACTERS))
            else:
                print("Please enter a valid length string...")

        self.indices = response
        self.letters.remove(self.guess)  # remove asked letter from set of letters

    def build_letter(self):  # for autoplay
        print("\nGuess: {}".format(self.guess))
        self.indices = str()
        for character in word:
            self.indices += LETTER_CHARACTERS[character == self.guess]

    def update_cipher(self):
        cipher = list(self.cipher)
        for index, truth in enumerate(self.indices):
            if truth == LETTER_CHARACTERS[1]:
                cipher[index] = self.guess
        self.cipher = "".join(cipher)

    def get_words(self, letter, indices):  # gets new set of words given index restrictions
        words = list()
        for word in self.words:
            if indices == LETTER_CHARACTERS[0] * self.word_len:
                if letter not in word:  # efficient check for specific case
                    words.append(word)
            else:
                append = True
                for index, truth in enumerate(indices):  # check for other cases
                    if (word[index] == letter) != (truth == LETTER_CHARACTERS[1]):
                        append = False
                        break
                if append:
                    words.append(word)

        return words

    def check_words(self):
        if len(self.words) in (0, 1):
            if len(self.words) == 1:  # if word list reduced to single word
                print("Your word is '{}'!".format(self.words[0]))
            elif len(self.words) == 0:  # if word list reduced to empty
                print("I don't know your word...")
            return True  # found
        else:
            return False  # not found

    def decide_letter(self):  # decide optimal letter to ask
        min_length = len(self.words)
        self.guess = self.letters[0]

        string = "Thinking"
        for letter in self.letters:  # pick letter which reduces possible words the most if not in word
            print(string, end="\r")
            string += "."

            start = time.time()

            current_length = len(self.get_words(letter, LETTER_CHARACTERS[0] * self.word_len))

            if current_length < min_length and current_length != 0:  # dont pick a letter which would remove all words
                min_length = current_length
                self.guess = letter

            end = time.time()
            time.sleep(0.05 - end + start)

        print(" " * 100, end="\r")

    def update(self, word):
        if word is None:  # gets self.indices
            self.ask_letter()
        else:
            self.build_letter()

        self.update_cipher()
        if LETTER_CHARACTERS[1] not in self.indices:
            self.errors += 1

        print("\nCurrent word: {}\nErrors: {}".format(self.cipher, self.errors))
        new_words = self.get_words(self.guess, self.indices)  # get new words given indices

        if MAX_PRINTED_WORDS:  # printing current/previous words
            if len(new_words) not in (0, 1) and len(new_words) <= MAX_PRINTED_WORDS:
                print("Your word might be {}".format(", ".join(new_words)))
            elif len(new_words) > 1:
                print("There are now {} possible words".format(len(new_words)))

            if len(new_words) in (0, 1) and len(self.words) > MAX_PRINTED_WORDS:
                print("Previous possible words: {}".format(", ".join(self.words)))

        elif len(new_words) in (0, 1):
            print("Previous possible words: {}".format(", ".join(self.words)))

        self.words = new_words
        found = self.check_words()
        if found:  # break from loop
            return True
        self.decide_letter()  # gets self.guess

    @staticmethod
    def prune_database():  # cleans a list of words
        allowed_letters = list("abcdefghijklmnopqrstuvwxyz")

        words = open(WORDS_FILE, "r").read().split("\n")

        valid_words = list()
        for word in words:
            if word and (set(word) <= set(allowed_letters)):  # ignore blanks and words with other characters
                valid_words.append(word)

        valid_words = list(set(valid_words))  # remove duplicate words
        valid_words.sort()  # sort by alphabet
        valid_words.sort(key=len)  # sort by length

        current_len = 1
        wordset = list()
        for word in valid_words:
            if current_len != len(word):
                wordset.append(" ")  # leave a linebreak if word length changes
                current_len = len(word)
            wordset.append(word)

        open(WORDS_FILE, "w").write("\n".join(wordset))


#Guesser.prune_database()

LETTER_CHARACTERS = ("-", "=")
MAX_PRINTED_WORDS = 8
WORDS_FILE = "english_words.txt"

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
