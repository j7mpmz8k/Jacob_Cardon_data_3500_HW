def isAnagram(word1=None, word2=None):

    #checks if both word size is the same
    if len(word1) != len(word2):
        return False
    
    else:
        #convert to list, when a letter match is found, letter is removed from list
        list1 = []#list of word1
        list2 = []#list of word2
        for letter in word1:
            list1.append(letter)
        for letter in word2:
            list2.append(letter)

        #checks if each letter from from word1 is remaining in available letters from the word2 list
        for word1_letter in word1:
            if word1_letter in list2:
                list2.remove(word1_letter)

        #checks if each letter from from word2 is remaining in available letters from the word1 list
        for word2_letter in word2:
            if word2_letter in list1:
                list1.remove(word2_letter)

    #checks if both word lists are reduced to zero implying an anagram is True
    return int(len(list1)) == 0 and int(len(list2)) == 0


print(isAnagram("aekale","aleaek"))
