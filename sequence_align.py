'''
This is the file which contains the algorithm for determining the distance between two words using sequence alignment.
Uses list objects to form arrays because I cannot be arsed dealing with installing NumPy right now.
I miss R.
'''

def print_array(m):
    for i in range(len(m)):
        print(m[i])

def sequence_align(w1, w2, delta, alpha, distance_return = False):
    m = len(w1) + 1
    n = len(w2) + 1

    M = [[0 for _ in range(n)] for _ in range(m)]
    for i in range(m):
        M[i][0] = i * delta
    for j in range(n):
        M[0][j] = j * delta

    for i in range(1, m):
        for j in range(1, n):
            M[i][j] = min(
                int(w1[i-1] != w2[j-1]) * alpha + M[i-1][j-1],
                delta + M[i-1][j],
                delta + M[i][j-1]
            )
    
    # print(M)
    
    if distance_return:
        return M[m-1][n-1]
    return M
