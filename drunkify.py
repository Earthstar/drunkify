# Let's practice using a dispatch design pattern!
# goal: take a string, split it into words
# for each of those words, randomly "drunkify" them
# then paste them back into a paragraph

# Misspellings: replace vowel with another vowel, delete a double letter
# Add multiple letters, d -> g, swap letters
# Want to test whether the word can be altered before altering it.
# Randomly choose a word to be altered
# copying from _dispatch in courseware/access
# where do I check if function works on word? In the function
# each word operation needs a boolean function to test?

import random


VOWELS = set(['a','e','i','o','u'])

def dispatch(table, action, word):
    '''assumes action can be applied to word'''
    return table[action](word)

def can_vowelswap(word):
    for v in VOWELS:
        if v in word:
            return True
    return False

def vowelswap(word):
    if can_vowelswap(word):
        # split word into list, identify vowels, pick random vowel, and swap out
        word_list = list(word)
        vowel_index = []
        for i in range(len(word_list)):
            if word_list[i] in VOWELS:
                vowel_index.append(i)
        to_change = random.choice(vowel_index)
        word_list[to_change] = random.choice(list(VOWELS - set(word_list[to_change])))
        return ''.join(word_list)
    return None

def can_letterswap(word):
    return len(word) > 1

def letterswap(word):
    if can_letterswap(word):
        # randomly pick an index to swap words
        word_list = list(word)
        random_index = random.choice(range(len(word_list)-1))
        # swap index with index to left
        placeholder = word_list[random_index]
        word_list[random_index] = word_list[random_index+1]
        word_list[random_index+1] = placeholder
        return ''.join(word_list)
    return None

def double(word):
    word_list = list(word)
    random_index = random.choice(range(len(word_list)))
    word_list.insert(random_index, word_list[random_index])
    return ''.join(word_list)

def can_delete_double(word):
    if len(word) <= 1:
        return False
    for i in range(len(word)-1):
        if word[i] == word[i+1]:
            return True
    return False

def delete_double(word):
    if can_delete_double(word):
        # identify doubles, and randomly pick one to delete
        double_index = []
        word_list = list(word)
        for i in range(len(word_list)-1):
            if word_list[i] == word_list[i+1]:
                double_index.append(i)
        random_double = random.choice(double_index)
        word_list.pop(random_double)
        return ''.join(word_list)

def insert_g(word):
    word_list = list(word)
    random_index = random.choice(range(len(word)))
    word_list.insert(random_index, 'g')
    return ''.join(word_list)

# This dictionary needs to be at the end for the function names to be defined
TABLE = {'vowelswap':vowelswap, 'letterswap':letterswap, 'double':double,
         'delete_double':delete_double, 'insert_g':insert_g}

# Putting it all together
# what to do about punctuation?
def drunkify(string, drunklevel):
    '''
    string - any string
    drunklevel - a float/int, which is interpreted as the expected probability of
    one word being changed
    '''
    string = string.lower()
    # split string into words
    string_list = string.split()
    num_words_to_change = int(drunklevel*len(string_list))
    print num_words_to_change
    for i in range(num_words_to_change):
        index = random.choice(range(len(string_list)))
        changed = None
        while changed == None:
            action = random.choice(TABLE.keys())
            changed = dispatch(TABLE, action, string_list[index])
        string_list[index] = changed
    return ' '.join(string_list)

print drunkify('now that the airsealers have taught me the amazing technique of putting things near cracks its amazing how much you can find out', 10)