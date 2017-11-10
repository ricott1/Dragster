from runner import *
import sys, curses, time, copy, json


def print_state(stdscr, p, g, runners, GOAL, steps, best):
    stdscr.addstr(0, 0, "time {:3}  pool {}    generation {}   best {}  ".format(steps, p, g, best))
    for i, r in enumerate(runners):
        stdscr.addstr(i+1, 0, r.print_state() + "  :" + "|" * int(r.distance/256.) + " " * (100))#
    stdscr.refresh()

def main():
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    structure = STRUCTURE
    winners = []
    
    best = 999
    try:
        for g in xrange(GENERATIONS):
            start_tach, frame_count = 21, 0
            pool = [[Runner(j, p, g, structure, start_tach, frame_count) for j in xrange(N)] for p in xrange(N)]
            if winners:
                evolve_runners(pool, g, winners)                
            winners = []
            for p, runners in enumerate(pool):
                winner, best = run_pool(p, g, runners, best, stdscr)
                winners.append(winner)            
    finally:
        curses.echo()
        curses.nocbreak()
        
        raw_input()
        curses.endwin()
        print best

def evolve_runners(pool, g, winners):
    for p, runners in enumerate(pool):
        for i, r in enumerate(runners):
            runners[i].brain = copy.deepcopy(winners[i].brain)
            runners[i].id += winners[i].id
            runners[i].brain.mutate(MUTATION_RATE * p / N / g**1/2)

def run_pool(p, g, runners, best, stdscr):
    arrived = 0
    steps = 0
    start = time.time()
    while True:
        state = ""
        for j, r in enumerate(sorted([run for run in runners], key= lambda x: x.distance, reverse=True)):
            #r.recover(j)
            if not r.isArrived:
                inputs = [r.frame, r.distance, r.tach, r.speed]
                r.update(inputs)
            if r.distance >= GOAL and not r.isArrived and not r.blowup:
                arrived += 1
                r.isArrived = arrived
            #time.sleep(0.15)    
        steps += 1
        print_state(stdscr, p, g, runners, GOAL, steps, best)
        if arrived >= 1 or steps > 2 * best/0.0334:
            winner = sorted([r for r in runners if r.blowup == 0], key= lambda x: x.distance, reverse=True)[0]
            print winner.time
            if winner.time < best:
                with open("champion.drag", "w") as f:
                    json.dump(winner.log, f) 
                best = winner.time
            break

    return winner, best

N = 40
GOAL = 97 * 256
TIME_OUT = 20/0.0334
GENERATIONS = 50
MUTATION_RATE = 0.515
STRUCTURE = [4, 6, 6, 2]
if __name__ == '__main__':
    main()
