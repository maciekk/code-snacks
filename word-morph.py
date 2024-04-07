#!/usr/bin/env python3

# Word Morph

import igraph
import random
import sys
import time

# This is the OSX location.
WORDS_FILE = "/usr/share/dict/words"

def get_word(prompt):
    # TODO: provide implementation with actual user input.
    return random.choice(["book", "lock", "flip", "cook", "past"])

class Solver:
    """Simple solver."""
    def __init__(self, word_start, word_finish):
        self.word_start = word_start
        self.word_finish = word_finish
        self.load_dictionary(WORDS_FILE, len(word_start))

    def load_dictionary(self, fname, word_length):
        """Loads dictionary of words of matching word_length."""
        tick = time.perf_counter()

        fl = open(fname, "r")
        self.words = [w for w in map(str.strip, fl.readlines())
                      if len(w) == word_length]

        tock = time.perf_counter()
        print(f"Read in {len(self.words)} words "
              f"of length {len(self.word_start)} "
              f"in {tock-tick:0.3f} seconds.")

    @staticmethod
    def word_distance(word1, word2):
        """Return the number of letters that differ between the 2 words."""
        return len(list(
                # Shame, PEP 3113 removed tuple unpacking...
                filter(lambda xy: xy[0] != xy[1],
                       zip(word1, word2))))

    def words_one_away(self, word_src):
        """Return list of words that are 1 letter away from 'word_src'."""
        return [w for w in self.words
                if Solver.word_distance(word_src, w) == 1]

    def solve(self):
        """Overall solve API which selects an implementation underneath."""
        return self.solve_bfs()

    # A breadth-first-search solution. Slow. Need graph-based approach.
    def solve_bfs(self):
        "Returns array of progressive words if solution exists."

        # Each work item on the queue is a list of words so far.
        work_q = [[self.word_start]]

        while work_q:
            words_so_far = work_q.pop(0)
            for w in self.words_one_away(words_so_far[-1]):
                if w == self.word_finish:
                    # Found (one) solution!
                    return words_so_far + [w]

                if w in words_so_far:
                    # Do not reuse words.
                    continue

                work_q.append(words_so_far + [w])

        # No solutions found at all.
        return None


def main():
    word_start = get_word("Starting word: ")
    word_finish = get_word("Final word: ")

    # Sanity check
    if not word_start or not word_finish:
        sys.exit("One of the words you provided is empty")

    if len(word_start) != len(word_finish):
        sys.exit("Words are not of the same length!")

    if word_start == word_finish:
        sys.exit("Start and finish words are identical.")

    solver = Solver(word_start, word_finish)

    print("Problem: [%s -> %s]" % (word_start, word_finish))
    print("Solution: ", solver.solve())

if __name__ == "__main__":
    # execute only if run as a script
    main()
