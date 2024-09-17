"""
creates a list of words which are made of component words,
and lets a user vet them into a second list
"""

def decompose_string(pieces):
    "recursively divides up a word into component words"
    piece = pieces[-1] # take final piece of word
    for i, _ in enumerate(piece): # go through its first letters
        if i > 0 and piece[:i+1] in words: # if letters form a word
            if i == len(piece)-1: # if letters are the word
                return pieces, "done" # gg exit recursion

            pieces = pieces[:-1] # remove final piece
            pieces.append(piece[:i+1]) # add word part of piece
            pieces.append(piece[i+1:]) # add new final piece
            pieces, task = decompose_string(pieces) # recursively continue
            if task == "done": # if recursive node wants to leave
                return pieces, "done" # gg exit recursion

    if len(pieces) == 1: # nothing was found
        return pieces, "done"

    pieces = pieces[:-1] # remove final piece
    pieces[-1] = pieces[-1]+piece # re-attach end
    return pieces, "fail" # nothing was found


INPUT_WORDS_FILE = "test_input.txt"
PIECE_WORDS_FILE = "test_input.txt"
OUTPUT_FILE = "test_output.txt"
VETTED_OUTPUT_FILE = "vetted_contractions.txt"
GENERATE_WORDS = True

if GENERATE_WORDS:
    with open(INPUT_WORDS_FILE, "r", encoding="utf8") as file:
        word_sets = file.read().split("\n\n")
    sorted_words = [word for word_set in word_sets for word in word_set.split("\n")]
    words = set(sorted_words)

    with open(OUTPUT_FILE, "w", encoding="utf8"):
        pass

    for check_word in sorted_words:
        result, _ = decompose_string([check_word])
        if len(result) > 1:
            #print(" ".join(result))
            with open(OUTPUT_FILE, "a", encoding="utf8") as file:
                file.write(" ".join(result)+"\n")

else:
    contraction_words = []
    with open(OUTPUT_FILE, "r", encoding="utf8") as file:
        word_sets = file.read().split("\n\n")
    words = [word for word_set in word_sets for word in word_set.split("\n")]
    for check_word in words:
        keep = input(check_word)
        if keep != "":
            print("stored!")
            with open(VETTED_OUTPUT_FILE, "a", encoding="utf8") as file:
                file.write(check_word+"\n")
