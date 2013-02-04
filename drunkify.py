# Let's practice using a dispatch design pattern!

import random
import string
import copy
import math

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

TO_INSERT = ['g', 'p']
def insert_letter(word):
    word_list = list(word)
    random_index = random.choice(range(len(word)))
    random_letter = random.choice(TO_INSERT)
    word_list.insert(random_index, random_letter)
    return ''.join(word_list)

# This dictionary needs to be at the end for the function names to be defined
TABLE = {'vowelswap':vowelswap, 'letterswap':letterswap, 'double':double,
         'delete_double':delete_double, 'insert_letter':insert_letter}

# Putting it all together
# Change the drunkify algorithm so that some changes are more likely than
# others
# Create dictionary of 'function': integer, such that the probability of
# choosing a particular thing is num/total num?
# Easier to have absolute probabilities, and use random.random()
# sums of probabilities must equal 1

PROBABILITY_TABLE = [(0.5, 'vowelswap'), (0.2, 'letterswap'), (0.1, 'double'),
                     (0.1, 'delete_double'), (0.1, 'insert_letter')]


def choose_function():
    '''
    Returns a random function in proportions determined by probability_table
    '''
    # Create random number
    # iterate thru PROBABILITY_TABLE
    r = random.random()
    function = None
    for element in PROBABILITY_TABLE:
        if element[0] < r:
            r -= element[0]
        else:
            function = element[1]
            break
    return function

def drunkify(in_string, drunklevel):
    '''
    string - any string
    drunklevel - a float/int, which is interpreted as the expected probability of
    one word being changed
    take a string, split it into words
    for each of those words, randomly "drunkify" them
    then paste them back into a paragraph
    '''
    # remove uppercase, remove punctuation
    in_string = copy.copy(in_string)
    in_string = in_string.lower()
    in_string = in_string.translate(None, string.punctuation)
    # split string into words
    string_list = in_string.split()
    # remove punctuation
    num_words_to_change = int(math.ceil(drunklevel*len(string_list)))
    for i in range(num_words_to_change):
        index = random.choice(range(len(string_list)))
        changed = None
        while changed == None:
            action = choose_function()
            changed = dispatch(TABLE, action, string_list[index])
        string_list[index] = changed
    return ' '.join(string_list)

def play_drunkify():
    drunklevel = parse_drunkness(raw_input('How drunk are you? '))
    while True:
        phrase = raw_input('Say something, or "quit" to quit: ')
        if phrase == 'quit':
            break
        print drunkify(phrase, drunklevel)

INTENSIFIER = {'very':0.5, 'really':0.5, 'tipsy':0.5, 'buzzed':0.5,
               'drunk':1.0, 'intoxicated':1.0,
               'sloshed':2.0, 'roxy':2.0, 'wasted':2.0, 'smashed':2.0,
               'plastered':2.0}

def parse_drunkness(in_string):
    '''Given an input, parses the drunkedness level of player'''
    try:
        return float(in_string)
    except:
        '''Calculate drunkedness based on words in description
        '''
        in_string = in_string.lower()
        split_string = in_string.split()
        drunklevel = 0
        for word in split_string:
            if word == 'not':
                pass
            if word in INTENSIFIER:
                drunklevel += INTENSIFIER[word]
        return drunklevel

if __name__ == '__main__':
    play_drunkify()
    

 
