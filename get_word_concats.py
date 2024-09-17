def decompose_string(list):
    string = list[-1]
    for i, _ in enumerate(string):
        if i > 0 and string[:i+1] in words:
            if i == len(string)-1:
                return list, "done"
            else:
                list = list[:-1]
                list.append(string[:i+1])
                list.append(string[i+1:])
                list, task = decompose_string(list)
                if task == "done":
                    return list, "done"
                
    if len(list) == 1:
        return list, "done"
    
    list = list[:-1]
    list[-1] = list[-1]+string
    return list, "fail"


WORDS_FILE = "english_sorted_common_words.txt"
OUTPUT_FILE = "output.txt"
LIST_FILE = "contractions_list.txt"
GENERATE_WORDS = True

if GENERATE_WORDS:
    word_sets = open(WORDS_FILE, "r").read().split("\n\n")
    sorted_words = [word for word_set in word_sets for word in word_set.split("\n")]
    words = set(sorted_words)

    open(OUTPUT_FILE, "w")
    for check_word in sorted_words:
        result, _ = decompose_string([check_word])
        if len(result) > 1:
            #print(" ".join(result))
            open(OUTPUT_FILE, "a").write(" ".join(result)+"\n")

else:
    contraction_words = list()
    word_sets = open(OUTPUT_FILE, "r").read().split("\n\n")
    words = [word for word_set in word_sets for word in word_set.split("\n")]
    for check_word in words:
        keep = input(check_word)
        if keep != "":
            print("stored!")
            open(LIST_FILE, "a").write(check_word+"\n")