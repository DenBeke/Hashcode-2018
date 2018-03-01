import sys


class Printable:
    def __str__(self):
        temp = vars(self)
        out = ""
        for item in temp:
            out += str(item) + ' : ' + str(temp[item]) + '\n'
        return out

class Config(Printable):
    def __init__(self, line):
        '''
        Initialize config struct based on input line
        
        File format
        The first line of the input file contains the following integer numbers separated by single spaces:
        - R – numberofrowsofthegrid (1≤R≤10000)
        - C – number of columns of the grid (1 ≤ C ≤ 10000)
        - F – number of vehicles in the fleet (1 ≤ F ≤ 1000)
        - N–numberofrides (1≤N ≤10000)
        - B – per-ride bonus for starting the ride on time (1 ≤ B ≤ 10000)
        - T – number of steps in the simulation (1 ≤ T ≤ 109)
        '''
        self.rows                = int(line[0])
        self.cols                = int(line[1])
        self.vehicles            = int(line[2])
        self.rides               = int(line[3])
        self.on_time_start_bonus = int(line[4])
        self.steps               = int(line[5])



class Intersection(Printable):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def calculate_distance(self, other):
        '''
        |a − x| + |b − y|
        '''
        return abs(self.x - other.x) + abs(self.y - other.y)
        
    def __str__(self):
        return '(' + str(self.x) + ',' + str(self.y) + ')'
        

class Ride(Printable):
    def __init__(self, line):
        '''
        N subsequent lines of the input file describe the individual rides, from ride 0 to ride N − 1 . Each line contains the following integer numbers separated by single spaces:
        - a – the row of the start intersection (0 ≤ a < R)
        - b – the column of the start intersection (0 ≤ b < C )
        - x – the row of the finish intersection (0 ≤ x < R)
        - y – the column of the finish intersection (0 ≤ y < C )
        - s–theearlieststart(0≤s<T)
        - f–thelatestfinish(0≤f ≤T), (f ≥s+|x−a|+|y−b|)
            note that f can be equal to T – this makes the latest finish equal to the end of the simulation
        '''
        self.start               = Intersection(int(line[0]), int(line[1]))
        self.end                 = Intersection(int(line[2]), int(line[3]))
        self.earliest_start      = int(line[4])
        self.latest_finish       = int(line[5])
        self.is_handled          = False
        self.length              = self.start.calculate_distance(self.end)




current_vehicle_id = 0

class Vehicle:

    def __init__(self):
        global current_vehicle_id
        current_vehicle_id += 1
        self.id = current_vehicle_id
        self.rides = []
        self.location = Intersection(int(0),int(0))
        self.currentTime = int(0)

if __name__ == '__main__':
    # Read line from std in
    line = sys.stdin.readline().split()


    config = Config(line)
    rides  = []

    print(config)

    for ride in range(0, config.rides):
        line = sys.stdin.readline().split()
        rides.append(Ride(line))

    vehicles = []
    for _ in range(config.vehicles):
        vehicles.append(Vehicle())

    # Do shit with Vehciles
    file = open("output.txt", "w")

    for vehicle in vehicles:
        line = str(vehicle.id)
        for ride in vehicle.rides:
            line += " " + str(ride)

        print(line)
