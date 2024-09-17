sorted_words = sorted(open("english_common_words.txt", "r").read().split("\n"))
sorted_words.sort(key=len)
open("english_sorted_common_words.txt", "w")
for sorted_word in sorted_words:
    open("english_sorted_common_words.txt", "a").write(sorted_word+"\n")