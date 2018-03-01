import sys
import math
from tqdm import tqdm

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

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
        

current_ride_id = 0

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
        global current_ride_id
        self.id = current_ride_id
        current_ride_id += 1
        
        self.start               = Intersection(int(line[0]), int(line[1]))
        self.end                 = Intersection(int(line[2]), int(line[3]))
        self.earliest_start      = int(line[4])
        self.latest_finish       = int(line[5])
        self.is_handled          = False
        self.length              = self.start.calculate_distance(self.end)




current_vehicle_id = 0



class Vehicle(Printable):

    def __init__(self):
        global current_vehicle_id
        self.id = current_vehicle_id
        current_vehicle_id += 1
        
        self.rides = []
        self.location = Intersection(int(0),int(0))
        self.currentTime = int(0)

def get_next_vehicle():
    best_vehicle_id = None
    lowest_time = 99999999999
    for vehicle in vehicles:
        if vehicle.currentTime < lowest_time:
            best_vehicle_id = vehicle.id
            lowest_time = vehicle.currentTime

    return vehicles[best_vehicle_id]

def get_best_ride_for_vehicle(vehicle):
    closest_deadline = 9999999999
    best_score = -9999999999
    best_ride = None
    best_time_required = None
    for ride in rides:
        if ride.is_handled:
            continue
        time_required = max(ride.earliest_start - vehicle.currentTime - ride.start.calculate_distance(vehicle.location), 0) + ride.start.calculate_distance(vehicle.location) + ride.length
        if not vehicle.currentTime + time_required < ride.latest_finish:
            continue
        closeness = ride.latest_finish - (vehicle.currentTime + time_required)
        # if closeness < closest_deadline:
        #     best_ride = ride
        #     best_time_required = time_required
        score = ride.length - (max(ride.earliest_start - vehicle.currentTime - ride.start.calculate_distance(vehicle.location), 0))
        if ride.earliest_start > vehicle.currentTime + ride.start.calculate_distance(vehicle.location):
            score += config.on_time_start_bonus
        if score > best_score:
            best_ride = ride
            best_score = score
            best_time_required = time_required
    return (best_ride, best_time_required)

def preprocess(rides):
    filtered = 0
    threshold = 20
    dist_threshold = 200
    for ride in tqdm(rides):
        # found_start = 0
        # found_end = 0
        # for other in rides:
        #     if ride.id == other.id:
        #         continue
        #     if ride.start.calculate_distance(other.start) < dist_threshold or ride.start.calculate_distance(other.end) < dist_threshold:
        #         found_start += 1
        #     if ride.end.calculate_distance(other.start) < dist_threshold or ride.end.calculate_distance(other.end) < dist_threshold:
        #         found_end += 1
        #     if found_start >= threshold and found_end >= threshold:
        #         break
        if ride.start.y > 2222 or ride.end.y > 2222 or 6111 < ride.start.x or 6111 < ride.end.x or ride.start.x > 8333 or ride.end.x > 8333:
        #if not (found_start >= threshold and found_end >= threshold):
            ride.is_handled = True
            filtered += 1
    eprint("Filtered", filtered, "of", len(rides))

if __name__ == '__main__':
    # Read line from std in
    line = sys.stdin.readline().split()


    config = Config(line)
    rides  = []

    #print(config)

    for ride in range(0, config.rides):
        line = sys.stdin.readline().split()
        rides.append(Ride(line))
    preprocess(rides)
    #for ride in rides:
    #    print(ride)

    vehicles = []
    for _ in range(config.vehicles):
        vehicles.append(Vehicle())

    # Do shit with Vehciles
    file = open("output.txt", "w")



    for i in tqdm(range(len(rides))):
        next_vehicle = get_next_vehicle()
        
        #print(next_vehicle.currentTime)
        
        (next_ride, time) = get_best_ride_for_vehicle(next_vehicle)
        if next_ride is None:
            break
        next_vehicle.currentTime += time
        

        next_vehicle.rides.append(next_ride)
        next_ride.is_handled = True
        next_vehicle.location = next_ride.end

    for vehicle in vehicles:
        line = str(len(vehicle.rides))
        for ride in vehicle.rides:
            line += " " + str(ride.id)
        print(line)
