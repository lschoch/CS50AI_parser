import nltk
import sys
import re

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP | NP VP Conj VP

AP -> Adj | Adj AP
NP -> N | Det N | AP NP | Det AP NP | N PP | 
PP -> P NP | P NP PP
VP -> V | V NP | V NP PP
"""
# I had a little moist red paint in the palm of my hand.

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    word_list = nltk.tokenize.wordpunct_tokenize(sentence)
    word_list = [w.lower() for w in word_list if re.match('[A-Za-z]+', w)]
    return word_list

def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    npcs = []

    """Function to recursively check for noun phrases in subtrees."""
    def drill_down(subtree):
        for t in subtree.subtrees():
            # print(f"\nsubtree: {subtree} t: {t}")
            if t.height() == 3:
                npcs.append(t)
                continue
            if t.label() == 'NP' and t != subtree:
                drill_down(t)

    # Generate list of subtrees labelled 'NP'.
    list = [t for t in tree.subtrees() if t.label() == 'NP']
    # Driil down on each item to check for NP in subtrees.
    for subtree in list:
        drill_down(subtree)

    return npcs
               
if __name__ == "__main__":
    main()
