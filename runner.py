import random, math
import brain


class Runner(object):
    def __init__(self, index, pool, generation, structure, start_tach, frame_count):
        self.index = index
        self.pool = pool
        self.generation = generation
        self.id = str(self.pool)
        
        
        self.log = {"gas" : [], "shift" : [], "tach" : []}

        self.distance = 0
        self.speed = 0
        self.gear = 0
        self.gas = 1
        self.tach = start_tach
        self.advance = 1
        self.frame = frame_count
        self.limit = self.get_initial_limit()
        self.posttach = self.get_initial_posttach()
        self.shift = 1

        self.output = 0
        self.isArrived = 0
        self.time = 0
        self.blowup = 0
        self.brain = brain.Brain(structure)
        self.log["gas"].append(self.gas)
        self.log["shift"].append(self.shift)
        self.log["tach"].append(self.tach)

    def update(self, inputs):
        if self.blowup == 0:
            results = self.brain.propagate(inputs, 0)
            #print results
            self.gear = self.update_gear()
            #print "gear is {}".format(self.gear)
            self.gas = int(results[0] > 0.5)

            self.distance = self.update_distance()

            self.frame = self.update_frame()
            self.advance = self.update_advance()
            self.tach = self.update_tach()
            self.limit = self.update_limit()
            self.posttach = self.update_posttach()
            
            self.speed = self.update_speed()
            self.shift = int(results[1] > 0.5)
            self.time += 0.0334
            self.log["gas"].append(self.gas)
            self.log["shift"].append(self.shift)
            self.log["tach"].append(self.tach)

            if self.tach >= 32:
                self.blowup = 1
            
            
            
            
            self.posttach = self.update_posttach()

    def get_initial_limit(self):
        return self.update_limit()

    def get_initial_posttach(self):
        if self.limit - self.speed >= 16:
            return self.tach - 1
        else:
            return self.tach

    def update_gear(self):
        return min(self.gear + self.shift, 4)

    def update_distance(self):
        return self.distance + self.speed

    def update_frame(self):
        return self.frame + 2

    def update_advance(self):
        if self.frame % 2**(self.gear) == 0:
            return 1
        else:
            return 0

    def update_tach(self):
        if self.shift == 1:
            if self.gas == 1:
                return self.posttach + 3
            else:
                return self.posttach - 3
        else:
            if self.advance == 1:
                if self.gas == 1:
                    return self.posttach + 1
                else:
                    return self.posttach - 1
            else:
                return self.posttach

    def update_posttach(self):
        if self.shift == 1:
            return self.tach
        else:
            if self.limit - self.speed >= 16:
                return self.tach - 1
            else:
                return self.tach

    def update_limit(self):
        if self.tach >= 20:
            limit = self.tach * 2**(self.gear - 1) + 2**(self.gear - 2)
        else:
            limit = self.tach * 2**(self.gear - 1)
        return math.floor(limit)

    def update_speed(self):
        if self.gear > 0:
            if self.shift == 1:
                return self.speed
            else:
                if self.speed < self.limit:
                    return self.speed + 2
                elif self.speed == self.limit:
                    return self.speed
                else:
                    return self.speed - 1
        else:
            return 0

    def print_state(self):
    #print "{}: {} d = {}; s = {}; g = {}".format(self.id[-5:], self.frame, self.distance, self.speed, self.gear)
    #raw_input()
        return "{:1s}: {:4.2f} d={:3d}; s={:2d}; g={:1d} gas={:1d} sh={:1d}".format("B" * self.blowup, round(self.time,2), int(self.distance/256), self.speed,
        self.gear, self.gas, self.shift)