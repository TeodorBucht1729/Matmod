import genrandhiss as grh

def genweights(floors):
    weights1 = [1 for i in range(floors)]
    weights2 = []
    for i in range(floors):
        temp = [1 for i in range(floors)]
        temp[i] = 0
        weights2.append(temp)
    return (weights1, weights2)

def stupidsim():
    #generera vikter, kommer ändras senare
    floors = 10
    door_time = 15
    peoples = 100000
    people_per_minute = 0.5
    (weights1, weights2) = genweights(floors)

    queries = grh.get_rand_people(floors, peoples, 60/people_per_minute,  weights1, weights2)
#    print(queries)
    curr_floor = 0
    curr_time = 0
    tot_arg = 0
    while(len(queries) > 0): 
        if(queries[0][2] > curr_time):
            curr_time = queries[0][2]

        curr_time += grh.time_of_difference(curr_floor, queries[0][0])
        #travel_start är tidpunkten resan börjar
        travel_start = curr_time
        curr_time += door_time
        curr_floor = queries[0][0]
        curr_time += grh.time_of_difference(curr_floor, queries[0][1])
        curr_time += door_time
        curr_floor = queries[0][1]
        pass_finished = curr_time - door_time/2
        t_fak = pass_finished - queries[0][2]
        t_opt = pass_finished - travel_start
#        print(t_fak, t_opt)
        tot_arg += grh.arg(t_fak, t_opt)
#        print(grh.arg(t_fak, t_opt))
        queries.pop(0)
        
    return tot_arg/peoples

def smartsim():
    return "hej"

print(stupidsim())




