from runner import *
import sys, curses, time, copy


def print_state(stdscr, p, g, runners, GOAL, steps, best):
    stdscr.addstr(0, 0, "time {:3}  pool {}    generation {}   best {}  ".format(steps, p, g, best))
    for i, r in enumerate(runners):
        stdscr.addstr(i+1, 0, r.print_state() + "  :" + "|" * int(r.distance/256.) + " " * (100))#
    stdscr.refresh()

def main():
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    
    
    structure = [4, 10, 2]
    winners = []
    
    best = 999
    try:
        for g in xrange(GENERATIONS):
            #GOAL += 1
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
            runners[i].brain.mutate(MUTATION_RATE * p / g / N)

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
        if arrived >= 1 + WIN_CONDITION or steps > 2 * best/0.0334:
            winner = sorted([r for r in runners], key= lambda x: x.distance, reverse=True)[WIN_CONDITION]
            print winner.time
            if winner.time < best:
            	#with open("champion.drag", "w") as f:
            	#	f.write() 
            	best = winner.time
            break

    return winner, best

N = 50
GOAL = 97 * 256
TIME_OUT = 20/0.0334
GENERATIONS = 20
WIN_CONDITION = 0
MUTATION_RATE = 0.5
if __name__ == '__main__':
    main()
