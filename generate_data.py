'''
This is the script that is used to create the data that is used for the algorithm that determines if a word is a mismatch or a mis-spelling. 
'''

def main():
    # Import the words as a list.
    file_in = open('TypeRacingGame/test.text.txt') # 'TypeRacingGame/train.text.txt' for train data
    text = file_in.read().split('\n')
    file_in.close()
    # print(text[8])

    # Create the list.
    out = [None for _ in range(len(text))]
    
    # Generate the data!
    # keyword "#c#" to stop the simulation.

    for i in range(len(text)):
        print('\n'*8)
        print('test', i)
        word = text[i]
        print(word)
        word_out = input()
        if word_out == '#c#':
            break
        out[i] = word_out
    
    file_out = open('user_text_test.txt', 'w') # 'user_text.txt' for train data
    file_out.write('\n'.join(out))
    file_out.close()

main()