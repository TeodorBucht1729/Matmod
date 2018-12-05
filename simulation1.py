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

def dir_to_ind(curr_dir):
    if(curr_dir == 1):
        return 0
    else:
        return 1
    

def smartsim():
    
    floors = 10
    door_time = 15 + 8
    peoples = 100000
    people_per_minute = 0.5
    each_floor_time = 2
    (weights1, weights2) = genweights(floors)

    queries = grh.get_rand_people(floors, peoples, 60/people_per_minute,  weights1, weights2)
#    print(queries)
    curr_floor = 0
    curr_time = 0
    tot_arg = 0
    #curr_dir är 1 om hissen är på väg upp, och -1 om det är på väg ner.
    curr_dir = 1
    people_up = []
    people_down = []
    waiting_up = [[] for i in range(floors)]
    waiting_down = [[] for i in range(floors)]
    goal_dest = 0
    curr_in_elev = []
    elev_size = 10
    for que in queries:
        if(que[1] > que[0]):
            waiting_up[que[0]].append(que)
        else:
            waiting_down[que[0]].append(que)

    waiting = [waiting_up, waiting_down]
    #denna loopen går igenom alla våningar som hissen är på
    for counter in range(1000000):
        if(curr_floor == goal_dest or curr_floor*(floors - 1 - curr_floor) == 0):
            curr_dir *= -1

            #lägg till att man först tar ut alla som ska av här.
            #kanske lättare att först fundera ut på hur folk som är i hissen ska komma in, och hur det ska registreras. 
        #kolla om det finns nån som ska av på den här våningen och släpper av dem
        leave_people = False
        for pep in curr_in_elev:
            if(pep[0][1] == curr_floor):
                leave_people = True
                t_fak = curr_time - pep[1]
                t_fak += door_time/2
                t_opt = door_time*(3/2) + 2*abs(curr_floor - pep[0][0])
                tot_arg += grh.arg(t_fak, t_opt)
                curr_in_elev.remove(pep)     


        people_wait = 0
        #kolla hur många vi kan plocka upp från den nuvarande våningen
        print(curr_floor)
        while(people_wait < len(waiting[dir_to_ind(curr_dir)][curr_floor]) and len(curr_in_elev) < elev_size and waiting[dir_to_ind(curr_dir)][curr_floor][people_wait][2] < curr_time):
            people_wait += 1
        for i in range(people_wait):
            if(len(curr_in_elev) < elev_size):
                #lägg till informationen om personen som går på och vid vilken tidpunkt detta sker. Ta också bort personen ur väntelistan
                curr_in_elev.append((waiting[dir_to_ind(curr_dir)][curr_floor][0], curr_time + door_time/2))
                temp_goal = curr_in_elev[len(curr_in_elev) - 1][0][1]
                if(curr_dir * temp_goal > curr_dir * goal_dest):
                    goal_dest = temp_goal
                waiting[dir_to_ind(curr_floor)][curr_floor].pop(0)
            else:
                break
        if(people_wait > 0 or leave_people):
            curr_time += door_time
        curr_time += each_floor_time

        curr_floor += curr_dir
        curr_floor = max(curr_floor, 0)

    return tot_arg/peoples

             

    

print(smartsim())




