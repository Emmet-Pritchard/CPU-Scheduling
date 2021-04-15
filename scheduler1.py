import sys
import csv
import copy

# FCFS is where I began because it was the easiest
# to comprehend. I first declare a variable time as well
# as a list that I will hold the process IDs after they
# run. I use a simple for loop and check the time against
# the data held in fcfs[i][1] which will be the arrival
# time. In this first for loop I am appending the completion
# time of the processes in order to do my calculations for 
# the waiting time and turnaround time. I choose to create 
# a list that is sorted in order to match up what was shown
# in the example output. This was sorted by the process ID. 
# After this it was time to build the Gantt Chart. This was 
# tricky in fcfs because I needed to loop through again in
# order to print the processes and their run time. I had 
# some fun with the formatting because Python has some cool 
# features since it is a scripting language. I then did my 
# average time calculations which were pretty straight 
# forward. This was easy since I appended all of my times
# to the original list in order to do my comparisons.


def fcfs(to_fcfs):
    time = 0
    curr_p = []
    for i in range(len(to_fcfs)):
        if time < to_fcfs[i][1]:
            time = to_fcfs[i][1]
        if time > to_fcfs[i][1]:
            time = time + to_fcfs[i][2]
            to_fcfs[i].append(time)
        else:
            time = time + to_fcfs[i][2]
            to_fcfs[i].append(time)
    for i in range(len(to_fcfs)):
        to_fcfs[i].append(to_fcfs[i][3] - to_fcfs[i][1])
    for i in range(len(to_fcfs)):
        to_fcfs[i].append(to_fcfs[i][4] - to_fcfs[i][2])
    sorted_list = sorted(to_fcfs, key=lambda x: x[0])
    print("----------------------FCFS-----------------------")
    print("  Process ID   |  Waiting Time  | Turnaround Time")
    for i in range(len(sorted_list)):
        print('{:^14}'.format(sorted_list[i][0]), "|",
              '{:^14}'.format(sorted_list[i][5]), "|",
              '{:^14}'.format(sorted_list[i][4]))
    # section below deals with Gantt Chart formatting
    time = 0
    print("\nGantt Chart is:")
    for i in range(len(to_fcfs)):
        if time < to_fcfs[i][1]:
            print("[", '{:^4}'.format(time), "]-- IDLE --[",
                  '{:^4}'.format(to_fcfs[i][1]), "]")
            curr_p.append(0)
            time = to_fcfs[i][1]
        if time > to_fcfs[i][1]:
            print("[", '{:^4}'.format(time), "]--",
                  '{:^4}'.format(to_fcfs[i][0]), "--[",
                  '{:^4}'.format(time + to_fcfs[i][2]), "]")
            curr_p.append(to_fcfs[i][0])
            time = time + to_fcfs[i][2]
        else:
            print("[", '{:^4}'.format(to_fcfs[i][1]),
                  "]--", '{:^4}'.format(to_fcfs[i][0]), "--[",
                  '{:^4}'.format(to_fcfs[i][1] + to_fcfs[i][2]), "]")
            curr_p.append(to_fcfs[i][0])
            time = time + to_fcfs[i][2]
    # section below deals with Average Time calculations and output
    awt = 0
    atat = 0
    for i in range(len(to_fcfs)):
        awt = awt + to_fcfs[i][5]
        atat = atat + to_fcfs[i][4]
    awt = awt / len(to_fcfs)
    atat = atat / len(to_fcfs)
    thpt = len(to_fcfs) / time
    print("\nAverage Waiting Time:", awt)
    print("Average Turnaround Time:", atat)
    print("Throughput:", "{:.12f}".format(thpt))
    print("")

# Next was sjfp. This function was pretty fun to work with since
# prior to this program I had struggled with preemption. I first 
# made a copy of the incoming data so that I can delete burst 
# times as I go and not worry about losing that data forever. 
# Really I could have just copied the burst times and used it in
# later calculations but it was easy to just copy the whole list.
# I declare the same variables as before except this time I have
# a counter as well as a ready_q that I will use when a process 
# gets preempted. I begin by checking to see if any processes 
# are ready at time = 0. If they are I add them to the ready_q.
# I then sort those by their burst time since this scheduling
# deals with shortest jobs. I go into a while loop where I check 
# again for processes to append to the ready queue at the top of 
# each iteration. Sort again. If the ready_q contains data, then
# set the current process to the first element in the list. Run
# the burst and check if it completes or if another process 
# comes along with shorter burst time. Once all processes have
# entered the ready_q, then it is just simple execution based 
# off of burst times from there. No need to check if another 
# process will come along. My Gantt chart building method was a
# little different here as I am using my list of process ID's. 
# Essentially, if it is a 0, then I will print the IDLE option. 
# If it is the end of the list, I will simply format it with 
# the element at the end of the list. If it is anything else, I
# will use my count and i variables to keep track of where I am
# in the list. I also account for duplicates, since I only want
# to know that a process is running for 3 units. I don't want 
# to see it every time. Again, I got to have a little fun with 
# the formatting that Python has to offer. I don't have a lot 
# of exposure to Python but this assignment has encouraged me 
# to look more into it. Average time calculations are the same 
# as in fcfs.


def sjfp(to_sjfp):
    for_calc = copy.deepcopy(to_sjfp)
    time = 0
    counter = 0
    ready_q = []
    curr_p = []

    for i in range(len(to_sjfp)):
        if to_sjfp[i][1] == time:
            ready_q.append(to_sjfp[i])
    ready_q = sorted(ready_q, key=lambda x: x[2])
    while counter != len(to_sjfp):
        for i in range(len(to_sjfp)):
            if to_sjfp[i][1] == time and to_sjfp[i] not in ready_q:
                ready_q.append(to_sjfp[i])
        ready_q = sorted(ready_q, key=lambda x: x[2])
        if ready_q:
            up_now = ready_q[0]
            curr_p.append(up_now[0])
            up_now[2] = up_now[2] - 1
            time = time + 1
            if up_now[2] == 0:
                up_now.append(time)
                ready_q.pop(0)
                counter = counter + 1
        else:
            curr_p.append(0)
            time = time + 1

    for i in range(len(for_calc)):
        for_calc[i].append(to_sjfp[i][3])
    for_calc = sorted(for_calc, key=lambda x: x[0])
    for i in range(len(for_calc)):
        for_calc[i].append(for_calc[i][3] - for_calc[i][1])
    for i in range(len(for_calc)):
        for_calc[i].append(for_calc[i][4] - for_calc[i][2])

    print("----------------------SJFP-----------------------")
    print("  Process ID   |  Waiting Time  | Turnaround Time")
    for i in range(len(for_calc)):
        print('{:^14}'.format(for_calc[i][0]), "|",
              '{:^14}'.format(for_calc[i][5]), "|",
              '{:^14}'.format(for_calc[i][4]))

    # section below deals with Gantt Chart formatting
    print("\nGantt Chart is:")
    count = 0
    i = 0
    while i < len(curr_p):
        if i == len(curr_p)-1 or i != 0 and curr_p[i] != curr_p[i-1]:
            if i == len(curr_p)-1:
                print("[", '{:^4}'.format(count), "]--",
                      '{:^4}'.format(curr_p[i-1]), "--[",
                      '{:^4}'.format(len(curr_p)), "]")
                count = i
            elif curr_p[i-1] == 0:
                print("[", '{:^4}'.format(count), "]-- IDLE --[",
                      '{:^4}'.format(i), "]")
                count = i
            else:
                print("[", '{:^4}'.format(count), "]--",
                      '{:^4}'.format(curr_p[i-1]), "--[",
                      '{:^4}'.format(i), "]")
                count = i
        i = i + 1

    # section below deals with Average Time calculations and output
    atat = awt = thpt = 0
    for i in range(len(for_calc)):
        awt = awt + for_calc[i][5]
        atat = atat + for_calc[i][4]
    awt = awt / len(for_calc)
    atat = atat / len(for_calc)
    thpt = len(for_calc) / time
    print("\nAverage Waiting Time:", awt)
    print("Average Turnaround Time:", atat)
    print("Throughput:", thpt)
    print("")

# to_add() is a helper function for my round robin 
# function. This function is a constant checker for
# new processes. It made my code hard to read so I 
# chose to break it up and just call this helper 
# instead. Essentially, if the element in to_rr is
# at its arrival time and it is not already in the 
# ready_q, then this helper function adds it.


def to_add(time, ready_q, to_rr):
    for i in range(len(to_rr)):
        if to_rr[i][1] == time and to_rr[i] not in ready_q:
            ready_q.append(to_rr[i])

# rr() was definitely the bulky function, but it was 
# surprisingly easier than sjfp and fcfs since I did most 
# of the learning within those first two functions. I 
# again make a copy of the incoming data so that I can use 
# if for calculations later and not have to worry about
# losing the original burst times of the processes. A lot 
# of this function was carry over from sjfp. I begin with 
# adding any processes that arrived at time = 0 to the 
# ready_q. If the ready_q contains elements, I pop the
# first element off of the queue and use it as the current
# process. Since round robin is cyclical, it is important 
# to pop the process off of the ready_q or else the queue
# will just keep getting longer. From here, we need to 
# compare the burst time to the time quantum. If the burst
# time is less, then the process will run until completion.
# If it is not, we have to run it for the duration of the 
# time quantum while always checking for any new processes
# that might arrive in that burst. In order to add spaces
# for my Gantt chart to recognize IDLE, if the ready_q is 
# empty, then it appends a 0. The ready_q will be empty at
# the end of the process though so it is important to 
# remove the trailing 0 so that the time is updated for the
# throughput calculation. My Gantt Chart format as well as
# my average time calculations are pulled straight from my
# sjfp function since I am using a similar algorithm.


def rr(to_rr, tq):
    for_calc = copy.deepcopy(to_rr)
    time = 0
    counter = 0
    ready_q = []
    curr_p = []
    up_now = []
    to_add(time, ready_q, to_rr)
    # up_now = ready_q[0]
    while counter != len(to_rr):
        for i in range(len(to_rr)):
            if to_rr[i][1] == time and to_rr[i] not in ready_q:
                ready_q.append(to_rr[i])
        if ready_q:
            up_now = ready_q.pop(0)
            if up_now[2] <= tq:
                while up_now[2] > 0:
                    time = time + 1
                    up_now[2] = up_now[2] - 1
                    to_add(time, ready_q, to_rr)
                    curr_p.append(up_now[0])
                up_now.append(time)
                counter = counter + 1
            else:
                for i in range(tq):
                    time = time + 1
                    up_now[2] = up_now[2] - 1
                    to_add(time, ready_q, to_rr)
                    curr_p.append(up_now[0])
                ready_q.append(up_now)
        if len(ready_q) == 0:
            curr_p.append(0)
            time = time + 1
    del curr_p[-1]
    time = time - 1

    for i in range(len(for_calc)):
        for_calc[i].append(to_rr[i][3])
    for_calc = sorted(for_calc, key=lambda x: x[0])
    for i in range(len(for_calc)):
        for_calc[i].append(for_calc[i][3] - for_calc[i][1])
    for i in range(len(for_calc)):
        for_calc[i].append(for_calc[i][4] - for_calc[i][2])
    print("------------------ Round Robin --------------------")
    print("  Process ID   |  Waiting Time  | Turnaround Time")
    for i in range(len(for_calc)):
        print('{:^14}'.format(for_calc[i][0]), "|",
              '{:^14}'.format(for_calc[i][5]), "|",
              '{:^14}'.format(for_calc[i][4]))

    # section below deals with Gantt Chart formatting
    print("\nGantt Chart is:")
    count = 0
    i = 0
    while i < len(curr_p):
        if i == len(curr_p)-1 or i != 0 and curr_p[i] != curr_p[i-1]:
            if i == len(curr_p)-1:
                print("[", '{:^4}'.format(count), "]--",
                      '{:^4}'.format(curr_p[i-1]), "--[",
                      '{:^4}'.format(len(curr_p)), "]")
                count = i
            elif curr_p[i-1] == 0:
                print("[", '{:^4}'.format(count), "]-- IDLE --[",
                      '{:^4}'.format(i), "]")
                count = i
            else:
                print("[", '{:^4}'.format(count), "]--",
                      '{:^4}'.format(curr_p[i-1]), "--[",
                      '{:^4}'.format(i), "]")
                count = i
        i = i + 1
    # section below deals with Average Time calculations and output
    atat = awt = thpt = 0
    for i in range(len(for_calc)):
        awt = awt + for_calc[i][5]
        atat = atat + for_calc[i][4]
    awt = awt / len(for_calc)
    atat = atat / len(for_calc)
    thpt = len(for_calc) / time
    print("\nAverage Waiting Time:", awt)
    print("Average Turnaround Time:", atat)
    print("Throughput:", thpt)
    print("")

# In main, filename is read in from the command line.
# Through some google search, I found the way to open 
# up a file and read it in using the built in csv reader
# library that Python has. After this, I popped the 
# first element off because that is the header containing
# (ProcessID, Arrival Time, and Burst Time). I first 
# sorted the list by process ID and then I sorted by 
# arrival time of the process IDs. I made a deepcopy of 
# my input for each function call because I noticed that 
# it was altered after returning from fcfs. In order to 
# do that I imported the copy library. I then called each
# function with its own input data.


if __name__ == '__main__':
    filename = sys.argv[1]
    time_quantum = int(sys.argv[2])
    input = list(csv.reader(open(filename)))
    input.pop(0)
    input = [list(map(int, i)) for i in input]
    input = sorted(input, key=lambda x: x[0])
    input = sorted(input, key=lambda x: (x[1], x[0]))
    to_fcfs = copy.deepcopy(input)
    fcfs(to_fcfs)
    to_sjfp = copy.deepcopy(input)
    sjfp(to_sjfp)
    to_rr = copy.deepcopy(input)
    rr(to_rr, time_quantum)
