# Activity 6
#set up sentence
sentence = "dude, I just biked down that mountain \
and at first I was like Whoa and then I was like Whoa"
print(sentence)
sentence = sentence.capitalize()

# split words on the spaces
words = sentence.split(" ")

first_whoa = True # set up a variable to track how many times we've seen whoa
i = 0
for word in words:
    if words[i] == "whoa" and first_whoa:
        words[i] = words[i].lower()
        first_whoa = False # set tracker to false
    elif words[i] == "whoa" and not first_whoa:
        words[i] = words[i].upper()
    else:
        pass
    i += 1

# output new sentence
new_sentence = ""
for word in words:
    new_sentence += " " + word

print(new_sentence)