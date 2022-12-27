'''
Word Typing Game
Inspired by typeracer.com, I want to create a game in python that gives a random sentence from a file and 
expects you to type it out as fast as you can. 
A few things I want to achieve with this game are listed below:
    - Fork a dataset that contains a bunch of different sentences. 
    - Create a text base UI.
    - Create a simple typing game that measures time and accuracy of your attempt. 
    - Upload to GitHub.
    - Create a typing game that takes previous scores and uses it to measure progress. 
    -   - This involves saving previous scores.
    - Create a timer window that tracks the time spent on the task.
    - Save 
'''

import random as r
import time as t
import numpy as np

class Game:
    def __init__(self) -> None:
        # Open the file of sentences. 
        file_in = open('sentences.txt')
        self.sentences = file_in.read().split('\n')
        file_in.close()
        
        self.mode = 1   # Standard Time tracking mode. 
        self.start_ui()
        self.play()
    
    def start_ui(self):
        print('Welcome to Typing Practice!')
        print('Enter the mode that you wish to play in:')
        print('1.   Standard: Simple time and accuracy tracking.')

        mode = int(input('Mode: '))
        self.mode = mode

    def play(self):
        if self.mode == 1:
            self.play_standard()
        
        print('Thank you.')
    
    def play_standard(self):
        i = r.randrange(0, len(self.sentences))
        sentence = self.sentences[i]
        print('Please read and prepare to write the following sentence:')
        print(sentence)
        t.sleep(5)
        # Count down
        for x in range(5, 0, -1):
            print(x)
            t.sleep(1)
        print('GO!')
        start_time = t.perf_counter()
        user_sentence = input()
        time_elapsed = t.perf_counter() - start_time

        percent_correct = self.compare(sentence, user_sentence)

        print('Summary:')
        print('Time:', round(time_elapsed, 3), 'Seconds')
        print('Accuracy:', str(round(percent_correct*100, 3)) + '%')

    
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
            # Determine if there was an extra word in the second sentence or not.
            if False: # not self.distance(w1, w2):
                w2_i += 1
            elif w1 == w2:
                correct_count += 1
            w1_i += 1;  w2_i += 1
        
        print(correct_count)
        print(max(len(s1_split), len(s2_split)))
        
        return correct_count / max(len(s1_split), len(s2_split))
    
    def distance(self, w1, w2, evaluate = True):
        '''
        This is a function I designed to measure the distance of two words. 
        The idea being that if the distance is too large that we should ignore the user word and move to the next one. 
        Super crude at the moment. 
        '''
        if evaluate:
            if abs(len(w1) - len(w2)) > 4:
                return False
            if len(w1) == len(w2):
                w1_dist = np.array(list(map(ord, list(w1))))
                w2_dist = np.array(list(map(ord, list(w2))))
                abs_dist = sum(list(np.abs(np.subtract(w1_dist, w2_dist))))
                print(abs_dist)
                if abs_dist > 200:
                    return False
            return True
        return True





                


def main():
    Game()

main()

