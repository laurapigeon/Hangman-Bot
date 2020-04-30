import copy
import time
import random


class Guesser:
    letters = list("etarionshdluwmfcgypbkvjxqz")  # letters in order of frequency

    defaults = list("aoaaaeeeeeeiiiiiiiiioooee")  # first guess for different length words (hardcoded for efficency)

    @classmethod
    def ask_length(cls):  # take input and check validity of word length
        while True:
            word_len = input("What is the length of your word? (enter word for auto): ")
            try:
                return int(word_len)  # if integer (5)
            except:
                if set(word_len) <= set(LETTER_CHARACTERS[0]):  # if string of blanks (------)
                    return len(word_len)
                elif set(word_len) <= set(cls.letters):  # if word (triggers autoplay)
                    return word_len
                print("That isn't a valid word length...")

    @staticmethod
    def get_random_word():
        global word_index
        word_sets = open(WORDS_FILE, "r").read().split("\n \n")
        words = list()
        for word_set in word_sets:
            for word in word_set.split("\n"):
                words.append(word)
        word = words[word_index - 1]
        if PRINT_RESULTS:
            print(word)
        word_index += 1
        return word

    def __init__(self, length):  # creates a guesser-type with a given word length
        self.letters = copy.copy(self.letters)  # class attribute is mutable by default

        self.word_len = length
        self.words = self.create_word_list(self.word_len)
        self.letter_sequence = str()

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
            return words[length - 1].split("\n")
        else:
            return list()

    def ask_indices(self):  # take input and check validity of letter answer
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

    def build_indices(self):  # for autoplay
        if PRINT_RESULTS:
            print("\nGuess: {}".format(self.guess))
        self.indices = str()
        for character in word:
            self.indices += LETTER_CHARACTERS[character == self.guess]
        self.letters.remove(self.guess)

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
            if PRINT_RESULTS:
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

        if PRINT_RESULTS:
            string = "Thinking"
        for letter in self.letters:  # pick letter which reduces possible words the most if not in word
            if PRINT_RESULTS:
                print(string, end="\r")
                string += "."

                start = time.time()

            current_length = len(self.get_words(letter, LETTER_CHARACTERS[0] * self.word_len))

            if current_length < min_length and current_length != 0:  # dont pick a letter which would remove all words
                min_length = current_length
                self.guess = letter

            if PRINT_RESULTS:
                end = time.time()
                time.sleep(WAIT_TIME - end + start)

        if PRINT_RESULTS:
            print(" " * 100, end="\r")

    def update(self, word):
        if RECORD_RESULTS:
            self.letter_sequence += self.guess  # for output file

        if word is None:  # gets self.indices
            self.ask_indices()
        else:
            self.build_indices()

        self.update_cipher()
        if LETTER_CHARACTERS[1] not in self.indices:
            self.errors += 1

        if PRINT_RESULTS:
            print("\nCurrent word: {}\nErrors: {}".format(self.cipher, self.errors))
        new_words = self.get_words(self.guess, self.indices)  # get new words given indices

        if PRINT_RESULTS:
            if MAX_PRINTED_WORDS:  # printing current/previous words
                if len(new_words) not in (0, 1) and len(new_words) <= MAX_PRINTED_WORDS:
                    print("Your word might be {}".format(", ".join(new_words)))
                elif PERCENTAGE:
                    if len(self.words):
                        print("I am {}% more sure of your word".format(round(100 * ((1 - len(new_words) / len(self.words)) % 1), 2)))
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

    def record_results(self):
        #previous_results = open(OUTPUT_FILE, "r").read().split("\n")
        string = "|".join([self.words[0], str(self.errors), self.letter_sequence])
        #if string not in previous_results:
        open(OUTPUT_FILE, "a").write(string + "\n")

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

    @staticmethod
    def get_average(word_len):
        results = open(OUTPUT_FILE, "r").read().split("\n")
        num_of_words = 0
        total_errors = 0
        total_guesses = 0
        for result in results:
            if len(result.split("|")[0]) == word_len:
                num_of_words += 1
                total_errors += int(result.split("|")[1])
                total_guesses += len(result.split("|")[2])
        if num_of_words:
            average_errors = round(total_errors / num_of_words, 4)
            average_guesses = round(total_guesses / num_of_words, 4)
            print("Of {} {}-letter words, average error is {} with {} guesses".format(num_of_words, word_len, average_errors, average_guesses))
        else:
            print("No {}-letter words in the database".format(word_len))

    @staticmethod
    def get_max(word_len):
        results = open(OUTPUT_FILE, "r").read().split("\n")
        max_value = 0
        max_word = list()
        for result in results:
            if len(result.split("|")[0]) == word_len:
                if int(result.split("|")[1]) > max_value:
                    max_value = int(result.split("|")[1])
                    max_word = [result.split("|")[0]]
                elif int(result.split("|")[1]) == max_value:
                    max_word.append(result.split("|")[0])
        if max_word:
            print("The maximum error {} letter word ({} errors) is {}".format(word_len, max_value, ", ".join(max_word)))
        else:
            print("No {}-letter words in the database".format(word_len))

    @staticmethod
    def get_min(word_len):
        results = open(OUTPUT_FILE, "r").read().split("\n")
        min_value = 100000000
        min_word = list()
        for result in results:
            if len(result.split("|")[0]) == word_len:
                if len(result.split("|")[2]) < min_value:
                    min_value = len(result.split("|")[2])
                    min_word = [result.split("|")[0]]
                elif len(result.split("|")[2]) == min_value:
                    min_word.append(result.split("|")[0])
        if min_word:
            print("The minimum guess {} letter word ({} guesses) is {}".format(word_len, min_value, ", ".join(min_word)))
        else:
            print("No {}-letter words in the database".format(word_len))


USE_RANDOM_WORD = True
word_index = 0
LETTER_CHARACTERS = ("-", "=")
MAX_PRINTED_WORDS = 8
PRINT_RESULTS = False
WAIT_TIME = 0.05  # seconds between "thinking" dots
WORDS_FILE = "english_words.txt"
OUTPUT_FILE = "results.txt"
RECORD_RESULTS = True
PERCENTAGE = True

#Guesser.prune_database()  # sort words file into readable form
#quit()

#for i in range(45):
#    Guesser.get_min(i + 1)
#quit()

while True:  # multiple games loop
    if USE_RANDOM_WORD:
        length = Guesser.get_random_word()
    else:
        length = Guesser.ask_length()

    if type(length) != int:  # if auto
        word, length = length, len(length)
    else:
        PRINT_RESULTS = True
        word = None

    guesser = Guesser(length)  # creates guesser instance

    done = False

    while not done:  # guessing loop
        done = guesser.update(word)

    if RECORD_RESULTS and word in [None, *guesser.words]:
        guesser.record_results()  # output word, errors, letter sequence to text file

    if PRINT_RESULTS:
        print("\nNEW GAME!\n")
