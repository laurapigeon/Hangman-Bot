"""
creates a list of words which are made of component words,
and lets a user vet them into a second list
"""
from copy import copy

def decompose_string(pieces: list, spud: list) -> None:
    """
    recursively divides up a word into component words:
    takes a list of pieces of the word
    observes the final piece of the word
    splits it into a word and a new final piece wherever possible
    and calls a new version of itself on that new list
    when the final piece is a full word, adds the pieces to a spud
    spud is a hot potato which is passed around and given every output
    """
    # look at final piece of word
    piece = pieces[-1]
    for i in range(len(piece)):
        # look at its first part (i+1 letters)
        part = piece[:i+1]

        # if the part isn't a word of enough length, skip
        if part not in piece_words or i+1 < MIN_PIECE_LEN:
            continue

        # if the part is the whole piece, we're done
        if i+1 == len(piece):
            # if theres enough pieces, add the word to the spud
            if len(pieces) >= MIN_PIECES:
                spud.append(" ".join(pieces))
            break

        # otherwise, the part is a word but not the whole piece
        # so create new instance to work on the rest of the piece
        pieces_copy = copy(pieces)[:-1] # the current piece
        pieces_copy.append(part) # the new word
        pieces_copy.append(piece[i+1:]) # the new piece
        decompose_string(pieces_copy, spud)


INPUT_WORDS_FILE = "200k_words.txt"
PIECE_WORDS_FILE = "10k_words.txt"
OUTPUT_FILE = "output.txt"
VETTED_OUTPUT_FILE = "vetted_compounds.txt"
GENERATE_WORDS = True
MIN_PIECE_LEN = 4
MIN_PIECES = 3

if GENERATE_WORDS:
    with open(INPUT_WORDS_FILE, "r", encoding="utf8") as file:
        word_sets = file.read().split("\n\n")
        input_words = {word for word_set in word_sets for word in word_set.split("\n")}
    with open(PIECE_WORDS_FILE, "r", encoding="utf8") as file:
        piece_words = set(file.read().split("\n"))

    results = []
    for j, check_word in enumerate(input_words):
        if j % 1000 == 0:
            print(j)
        decompose_string([check_word], results)
    with open(OUTPUT_FILE, "w", encoding="utf8") as file:
        file.write("\n".join(results))

else:
    compound_words = []
    with open(OUTPUT_FILE, "r", encoding="utf8") as file:
        word_sets = file.read().split("\n\n")
    input_words = [word for word_set in word_sets for word in word_set.split("\n")]

    with open(VETTED_OUTPUT_FILE, "a", encoding="utf8") as file:
        for check_word in input_words:
            keep = input(check_word)
            if keep != "":
                print("stored!")
                file.write(check_word+"\n")
