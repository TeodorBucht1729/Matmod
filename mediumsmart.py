import genrandhiss as grh

def dir_to_ind(curr_dir):
    if(curr_dir == 1):
        return 0
    else:
        return 1

def genweights(floors):
    weights1 = [1 for i in range(floors)]
    weights2 = []
    for i in range(floors):
        temp = [1 for i in range(floors)]
        temp[i] = 0
        weights2.append(temp)
    return (weights1, weights2)


def mediumsim():
    
    floors = 10
    door_time = 15 + 8
    peoples = 1000
    people_per_minute = 4
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
    for counter in range(1000):
#        if(curr_floor == goal_dest or curr_floor*(floors - 1 - curr_floor) == 0):
#            curr_dir *= -1
        print("direction: ", curr_dir)
        print("goal_dest: ", goal_dest)
            #lägg till att man först tar ut alla som ska av här.
            #kanske lättare att först fundera ut på hur folk som är i hissen ska komma in, och hur det ska registreras. 
        #kolla om det finns nån som ska av på den här våningen och släpper av dem
        print(curr_in_elev)
        leave_people = False
        rem = []
        for pep in curr_in_elev:
            if(pep[0][1] == curr_floor):
                leave_people = True
                t_fak = curr_time - pep[1]
                t_fak += door_time/2
                t_opt = door_time*(3/2) + 2*abs(curr_floor - pep[0][0])
                tot_arg += grh.arg(t_fak, t_opt)
                print("remove: ", pep)
                rem.append(pep)
             #   curr_in_elev.remove(pep)     
        for re in rem:
            curr_in_elev.remove(re)

        print(curr_in_elev)
        people_wait = 0
        #kolla hur många vi kan plocka upp från den nuvarande våningen
        print(curr_floor)
        while(people_wait < len(waiting[dir_to_ind(curr_dir)][curr_floor]) and len(curr_in_elev) < elev_size and waiting[dir_to_ind(curr_dir)][curr_floor][people_wait][2] < curr_time):
            people_wait += 1
        for i in range(people_wait):
            if(len(curr_in_elev) < elev_size):
                #lägg till informationen om personen som går på och vid vilken tidpunkt detta sker. Ta också bort personen ur väntelistan
                curr_in_elev.append((waiting[dir_to_ind(curr_dir)][curr_floor][0], curr_time + door_time/2))
                print("add: ", curr_in_elev[-1])
                #temp_goal är våningen som personen ska till.
                temp_goal = curr_in_elev[-1][0][1]
            
                if(curr_dir * temp_goal > curr_dir * goal_dest):
                    goal_dest = temp_goal
                waiting[dir_to_ind(curr_dir)][curr_floor].pop(0)
            else:
                break
        #kolla vad goal_dest ska vara genom att kolla alla uppåt och se om nån ska i samma riktning. 
        #det ska även kolla nerdåt, om det finns folk som ska i samma riktning prioriteras dessa, annars sätts goal_dest till den längst bort som har knapptryckningar. 

        indek = max(curr_floor + curr_dir, 0)
        people_same = False
        adder = curr_dir
        if(curr_floor == 0):
            adder = 1
        while(indek < floors and indek >= 0):
#            print("checking: ", indek)
            
            for pep in waiting[dir_to_ind(curr_dir)][indek]:
                if(pep[2] <= curr_time and goal_dest * curr_dir < pep[0] * curr_dir):
                    goal_dest = pep[0]
                    people_same = True
                    break
            if(not people_same):
                for pep in waiting[dir_to_ind(-1*curr_dir)][indek]:
                    if(pep[2] <= curr_time and len(curr_in_elev) == 0):
                        goal_dest = pep[0]
                        break
            indek += adder


        if(people_wait > 0 or leave_people):
            curr_time += door_time
        curr_time += each_floor_time
    
        if(curr_floor == 0 or curr_floor == floors - 1):
            curr_dir *= -1

        curr_floor += curr_dir
        curr_floor = max(curr_floor, 0)


    return tot_arg/peoples

             

    

print(mediumsim())




