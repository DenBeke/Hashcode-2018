car_count = 4

car_locs = 4 * [(0,0)]


with open("solution.txt") as sol:
    sols = sol.readlines()
    for line in sols:
        instructions = line.split(' ')
        assert(len(instructions) - 1 == int(instructions[0]))

