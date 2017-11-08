from runner import *
import sys, curses, time, copy


def print_state(stdscr, p, g, runners, GOAL, steps, best):
	stdscr.addstr(0, 0, "time {:3}  pool {}    generation {}   best {}  ".format(steps, p, g, best))
	for i, r in enumerate(runners):
		stdscr.addstr(i+1, 0, r.print_state() + "  :" + "|" * int(r.position) + " " * (GOAL - int(r.position)) + ":GOAL")
	stdscr.refresh()

def main():
	stdscr = curses.initscr()
	curses.noecho()
	curses.cbreak()
	N = 20
	GOAL = 50
	GENERATIONS = 50
	mutation_rate = 0.5
	structure = [3 * N, 10, 1]
	winners = []
	WIN_CONDITION = 0
	best = 999
	try:
		for g in xrange(GENERATIONS):
			#GOAL += 1
			TIME_OUT = 10 * GOAL
			pool = [[Runner(j, p, g, 1, structure) for j in xrange(N)] for p in xrange(N)]
			if winners:
				for p, runners in enumerate(pool):
					for i, r in enumerate(runners):
						runners[i].brain = copy.deepcopy(winners[i].brain)
						runners[i].id += winners[i].id
						
						runners[i].brain.mutate(mutation_rate * p / g / N)
			winners = []
			for p, runners in enumerate(pool):
				arrived = 0
				steps = 0
				start = time.time()
				while True:
					state = ""
					
					
					for j, r in enumerate(sorted([run for run in runners], key= lambda x: x.position, reverse=True)):
						#r.recover(j)
						if not r.isArrived:
							inputs = [r.position + 1, r.velocity + 1, r.energy + 1] + [j  for i in [[s.position + 1, s.velocity + 1, s.energy + 1] for s in runners if s != r] for j in i] 
							r.update(inputs)
						if r.position >= GOAL and not r.isArrived:
							arrived += 1
							r.isArrived = arrived
					steps += 1
					print_state(stdscr, p, g, runners, GOAL, steps, best)
					if arrived >= 1 + WIN_CONDITION or steps > TIME_OUT:
						winner = sorted([r for r in runners], key= lambda x: x.position, reverse=True)[WIN_CONDITION]
						winners.append(winner)
						best = min(1.*steps/GOAL, best)
						break
					#time.sleep(0.11)

			

			
	finally:
		curses.echo()
		curses.nocbreak()
		
		raw_input()
		curses.endwin()
		print best




if __name__ == '__main__':
	main()
