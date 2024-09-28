"sorts a file of words"

with open("output.txt", "r", encoding="utf8") as file:
    sorted_words = sorted(file.read().split("\n"))
sorted_words.sort(key=lambda s: (len(s), s))
with open("output.txt", "a", encoding="utf8") as file:
    file.truncate(0)
    for sorted_word in sorted_words:
        file.write(sorted_word+"\n")
