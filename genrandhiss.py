import random
import math

def arg(t_fak, t_opt):
    return min(1.037**min(150, t_fak - t_opt), 100)

def time_of_difference(a, b):
    d = abs(a-b)
    if(a == b): return 0
    return 8 + 2*d

def get_rand_people(n, n_people, expected, weigths1, weigths2):
    """
    n är antalet våningar i huset
    n_people är antalet personer i slutlistan
    expected är väntevärdet för tiden mellan personerna
    weigths1 är en list av vikter för hur ofta personerna kommer på våning i
    weigths2 är en lista av listor, en för varje våning för hur sannolikt det är att åka till de andra våningarna
    """
    floors = [i for i in range(n)]
    peoples_floors = random.choices(floors, weights = weigths1, k = n_people)
    
    rand_people = []
    rand_people = peoples_floors
    for i in range(n_people):
        rand_people[i] = [rand_people[i], random.choices(floors, weights = weigths2[rand_people[i]])[0]]

    n_people = len(rand_people)
    T = 0
    for i in range(n_people):
        U = random.random()
        rand_people[i].append(T)
        T += -math.log(U) * expected

    return rand_people

#print(get_rand_people(10, 100, 20, [1 for i in range(10)], [1]))

