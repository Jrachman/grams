#note to self: 
# - need to add a restricting rule for entering words that do not change the meaning of current words (i.e., "bean" to "beans")
# - create frontend
# - write what happens when all tiles are flipped
# - create start and end game
# - work on condition where you combine words that are already part of the list
# - b, a, s, t good for testing reordering (bast, stab, tabs, batsbasts)

import string, itertools, random, enchant
from collections import Counter as mset

d = enchant.Dict("en_US")

def parse_check(word_attempt, words):
    for word in words:
        if set(x in word_attempt for x in word) == set([True]):
            return word
    return False

alphabet = list(string.ascii_lowercase)
repeats = [13, 3, 3, 6, 18, 3, 4, 3, 12, 2, 2, 5, 3, 8, 11, 3, 2, 9, 6, 9, 6, 3, 3, 2, 3, 2]
grams = [list(itertools.repeat(a, n)) for a, n in zip(alphabet, repeats)]
grams = [item for sublist in grams for item in sublist]

remaining_grams = grams
available_grams = []
words = []
used_words = []
points = 0
left_to_flip = 144

while len(remaining_grams) != 0:
    action = input("\npoints: " + str(points) + "\ngrams left to flip: " +  str(left_to_flip) + "\nwords: " + str(words) + "\nlist: " + str(available_grams) + "\nwhat would you like to do?\naction: ")
    if action == "f":
        rand_num = random.randint(0, len(remaining_grams)-1)
        letter = remaining_grams[rand_num]
        available_grams.append(letter)
        del remaining_grams[rand_num]
        left_to_flip -= 1
    elif action == "q":
        break
    else:
        word_attempt = action
        if len(list(word_attempt)) < 4:
            print("the word you entered is not long enough")
        elif d.check(word_attempt) == False:
            print("the word you entered is not a word")
        elif word_attempt in used_words:
            print("the word you entered was already played once before")
        elif set(list(word_attempt)).issubset(set(available_grams)) == True: #add new word
            words.append(word_attempt)
            used_words.append(word_attempt)
            for x in list(word_attempt):
                available_grams.remove(x)
            points += 1
        elif parse_check(word_attempt, words) != False: #rearrange word
            temp = parse_check(word_attempt, words)
            if list(temp) == list(word_attempt):
                words.remove(temp)
                words.append(word_attempt)         
                used_words.append(word_attempt)
                points += 1
            else: #combine words and available grams
                intersection = mset(word_attempt) & mset(temp) #note
                #print(intersection)
                diff = list(intersection.elements()) #n, o, t, e
                #print(diff)
                remaining_letters = list(word_attempt) #gotten
                #print(remaining_letters)
                for letter in diff: #g, t
                    remaining_letters.remove(letter)
                    #print(remaining_letters)
                if set({False}).issubset(set(x in available_grams for x in remaining_letters)) == True:
                    print("the word that you entered does not have the necessary letters available to be formed")
                else:
                    #print(set(x in available_grams for x in remaining_letters))
                    words.append(word_attempt)
                    words.remove(parse_check(word_attempt, words))
                    used_words.append(word_attempt)
                    for x in remaining_letters:
                        available_grams.remove(x)
                    points += 1
        elif set(list(word_attempt)).issubset(set(available_grams)) == False: 
            print("the word that you entered does not have the necessary letters available to be formed")
        else:
            print("break")

print("done")

