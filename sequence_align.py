'''
This is the file which contains the algorithm for determining the distance between two words using sequence alignment.
Uses list objects to form arrays because I cannot be arsed dealing with installing NumPy right now.
I miss R.

Append: Toby: I created an argument that forces the sequence_align function to spit out the resulting alignment. I.e. Test - f_est
'''

def print_array(m):
    for i in range(len(m)):
        print(m[i])

def sequence_align(w1, w2, delta, alpha, distance_return = False, alignment_return = False):
    m = len(w1) + 1
    n = len(w2) + 1

    # Save prev
    prev = [[None for _ in range(n)] for _ in range(m)]

    M = [[0 for _ in range(n)] for _ in range(m)]
    for i in range(m):
        M[i][0] = i * delta
        prev[i][0] = (i-1, 0)
    for j in range(n):
        M[0][j] = j * delta
        prev[0][j] = (0, j-1)

    for i in range(1, m):
        for j in range(1, n):
            considerations = [int(w1[i-1] != w2[j-1]) * alpha + M[i-1][j-1],
                delta + M[i-1][j],
                delta + M[i][j-1]]
            
            min_val = min(considerations)
            # Determine path
            min_val_i = considerations.index(min_val)
            if min_val_i == 0: prev[i][j] = (i-1, j-1)
            elif min_val_i == 1: prev[i][j] = (i-1, j)
            else: prev[i][j] = (i, j-1)
            M[i][j] = min_val
    

    if alignment_return:
        # If show_alignment is true, then it will overwrite the returning of a matrix or min distance.
        curr = (m-1, n-1)
        nex = prev[curr[0]][curr[1]]

        s1 = ''
        s2 = ''
        while nex != (0, -1):
            # Determine the direction of the prev
            # If it came from the top:
            if curr[1] == nex[1]:
                s2 = '_' + s2
                s1 = w1[curr[0]-1] + s1
            # If it came from the left:
            elif curr[0] == nex[0]:
                s1 = '_' + s1
                s2 = w2[curr[1]-1] + s2
            # If it came from the diagonal:
            else:
                s1 = w1[curr[0]-1] + s1
                s2 = w2[curr[1]-1] + s2
            
            curr = nex
            nex = prev[curr[0]][curr[1]]
        
        return (s1, s2)





    if distance_return:
        return M[m-1][n-1]
    return M
