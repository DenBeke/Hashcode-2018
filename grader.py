from main import *
import sys


car_count = 4

car_locs = 4 * [(0,0)]

# Read line from std in
line = sys.stdin.readline().split()

config = Config(line)
rides = []

for ride in range(0, config.rides):
    line = sys.stdin.readline().split()
    rides.append(Ride(line))

vehicles = []
for _ in range(config.vehicles):
    vehicles.append(Vehicle())

with open("b.txt") as sol:
    score = 0
    sols = sol.readlines()
    i = -1
    for line in sols:
        i += 1
        vehicle = vehicles[i]
        t = 0
        instructions = line.split(' ')
        assert(len(instructions) - 1 == int(instructions[0]))
        for ride_attempt in instructions[1:]:
            ride_attempt = int(ride_attempt)
            ride = rides[ride_attempt]
            dist = vehicle.location.calculate_distance(ride.start)
            is_good = True
            has_bonus = False
            if t < ride.earliest_start:
                has_bonus = True
                t = ride.earliest_start
            print(has_bonus)
            t += dist
            t += ride.length
            if t >= ride.latest_finish:
                is_good = False
            vehicle.location = ride.end
            if is_good:
                score += ride.length
                if has_bonus:
                    score += config.on_time_start_bonus

    print(score)



