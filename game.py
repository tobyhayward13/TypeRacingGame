'''
Word Typing Game
Inspired by typeracer.com, I want to create a game in python that gives a random sentence from a file and 
expects you to type it out as fast as you can. 
A few things I want to achieve with this game are listed below:
    - Fork a dataset that contains a bunch of different sentences. 
    - Create a text base UI. Y
    - Create a simple typing game that measures time and accuracy of your attempt. Y
    -   - Create a better scoring system to detemine the distances between words that goes beyond sequence alignment.
    -   -   - Allocate a compensation for letters that are capitilised.
    - Upload to GitHub. Y
    - Create a typing game that takes previous scores and uses it to measure progress. 
    -   - This involves saving previous scores.
    - Create a timer window that tracks the time spent on the task.
    - Save 
'''

import random as r
import time as t
import sequence_align as sa
import math as m

class Game:
    def __init__(self) -> None:
        # Open the file of sentences. 
        file_in = open('sentences.txt')
        self.sentences = file_in.read().split('\n')
        file_in.close()
        
        self.mode = 1   # Standard Time tracking mode. 
        self.mismatches = None
        self.mismatches_score = None
        self.last_sentence = None
        self.start_ui()
    
    def start_ui(self):
        print('Welcome to Typing Practice!')
        print('Enter the mode that you wish to play in:')
        print('1.   Standard: Simple time and accuracy tracking.')
        print('0.   Quit Game.')

        mode = int(input('Mode: '))
        self.mode = mode
        if mode != 0:
            self.play()

    def play(self):
        print('\n'*2)
        if self.mode == 1:
            self.play_standard()
        
    
    def play_standard(self, replay = False):
        self.mismatches = list();   self.mismatches_score = list()
        i = r.randrange(0, len(self.sentences))
        sentence = self.sentences[i]
        if replay:
            sentence = self.last_sentence
        self.last_sentence = sentence

        print('Please read and prepare to write the following sentence:')
        print(sentence)
        t.sleep(5)
        # Count down
        for x in range(5, 0, -1):
            print(x, end = ' ')
            t.sleep(1)
        print('GO!')
        start_time = t.perf_counter()
        user_sentence = input()
        time_elapsed = t.perf_counter() - start_time

        percent_correct = self.compare(sentence, user_sentence)


        print('\n'*3)
        print('Summary:')
        print('Time:', round(time_elapsed, 3), 'Seconds')
        print('Accuracy:', str(round(percent_correct*100, 3)) + '%')
        print('Type:')
        print('1.   For a breakdown of your mismatched words.')
        print('2.   To try this sentence again.')
        print('0.   To return to the main screen.')

        next = int(input())
        while next == 1:
            self.print_mistmatches()
            print('\n'*2)
            print('Type:')
            print('1.   For a breakdown of your mismatched words.')
            print('2.   To try this sentence again.')
            print('0.   To return to the main screen.')

            next = int(input())
        
        if next == 2:
            self.play_standard(replay=True)
        else:
            self.start_ui()
        

    
    def compare(self, s1, s2):
        '''
        Compares two sentences and returns a percentage match.
        Assumes s2 is user sentence.
        '''
        # Split the sentences into words.
        s1_split = s1.split(' ');   s2_split = s2.split(' ')
        correct_count = 0
        w1_i = 0; w2_i = 0
        while w1_i < len(s1_split) and w2_i < len(s2_split):
            w1 = s1_split[w1_i];    w2 = s2_split[w2_i]
            if w1 == w2:
                correct_count += 1
                w1_i += 1;  w2_i += 1
            # If the words are deemed to be the similar enough.
            elif self.prob_w_w(w1, w2) > 0.592:
                self.mismatches.append([w1, w2])
                self.mismatches_score.append(self.prob_w_w(w1, w2))
                # Split the words up and count the number of matching characters.
                # # Alternatively, we can incorporate the distance statistic.
                correct_count += self.char_count(w1, w2)
                w1_i += 1;  w2_i += 1
            # If the words are not deemed to be the same
            else:
                self.mismatches.append([w1, w2])
                self.mismatches_score.append(self.prob_w_w(w1, w2))
                # Search ahead 3 words on the user side and see if there is a close enough match.
                better_match = False
                for i in range(1, 4):
                    # Check to see if index is out of range.
                    if w2_i + i >= len(s2_split):
                        break
                    w2_potential = s2_split[w2_i + i]
                    # If the words are close enough:
                    if self.prob_w_w(w1, w2_potential) > 0.592:
                        better_match = True
                        correct_count += self.word_compare(w1, w2) # char_count also works.
                        w1_i += 1;  w2_i += i + 1
                        break
                
                if not better_match:
                    correct_count += self.word_compare(w1, w2) # char_count also works.
                    w1_i += 1;  w2_i += 1

        
        return correct_count / max(len(s1_split), len(s2_split))

    def prob_w_w(self, w1, w2):
        def plogis(x):
            return m.exp(x) / (1 + m.exp(x))

        # Calculate the probability that two mismatching words are meant to be the same.
        d = sa.sequence_align(w1, w2, delta = 1, alpha = 1, distance_return = True)
        s = len(w1)

        return plogis(2 - 2.15 * d + 0.15 * s)
    
    def char_count(self, w1, w2):
        # Primitave word comparison algorithm.
        # Goes through the smallest word and counts the proportion of matching characters.
        # # Like mentioned, could use the distance statistic or output to better determine a more fair result.
        char_count = 0
        for i in range(min(len(w1), len(w2))):
            if w1[i] == w2[i]:
                char_count += 1
        return char_count / max(len(w1), len(w2))

    def word_compare(self, w1, w2):
        # Uses Sequence-Alignment algorithm to determine how closely related the two words are. 
        # Returns 1 - size / length_largest_word
        # Careful with this if you choose to change alpha and delta. 
        # Experimental.
        d = sa.sequence_align(w1, w2, delta = 1, alpha = 1, distance_return = True)
        return 1 - d/max(len(w1), len(w2))

    def print_mistmatches(self):
        for i in range(len(self.mismatches)):
            print(self.mismatches[i], round(self.mismatches_score[i], 4), end = '')
            print('% match.')



def main():
    Game()

main()

