import random
import math
from copy import deepcopy
import matplotlib.pyplot as plt
import numpy as np

prob_mutate = 0.08


class Point:
    def __init__(self, xx, yy):
        self.x = xx
        self.y = yy


def check_intersection(point1, point2, point3, point4):
    px12 = point1.x - point2.x
    py12 = point2.y - point1.y
    pz12 = py12 * point1.x + px12 * point1.y
    px34 = point3.x - point4.x
    py34 = point4.y - point3.y
    pz34 = py34 * point3.x + px34 * point3.y
    det = py12 * px34 - py34 * px12
    if det == 0:
        return 0
    else:
        next_x = (px34 * pz12 - px12 * pz34)/det
        next_y = (py12 * pz34 - py34 * pz12) / det
        min_x1 = min(point1.x, point2.x)
        max_x1 = max(point1.x, point2.x)
        min_y1 = min(point1.y, point2.y)
        max_y1 = max(point1.y, point2.y)
        min_x2 = min(point3.x, point4.x)
        max_x2 = max(point3.x, point4.x)
        min_y2 = min(point3.y, point4.y)
        max_y2 = max(point3.y, point4.y)

        if (not(max_x1 >= next_x >= min_x1)) or (not (max_x2 >= next_x >= min_x2)) or (not(max_y1 >= next_y >= min_y1)) or (not(max_y2 >= next_y >= min_y2)):
            return 0
    return 1


def get_angle(a, b, c):
    angle = math.degrees(math.atan2(c[1]-b[1], c[0]-b[0]) - math.atan2(a[1]-b[1], a[0]-b[0]))
    return angle + 360 if angle < 0 else angle


def convex_angles(chromosome, total_points):
    all_angles = []
    for p in range(total_points):       # angles against all points
        all_angles.append(get_angle([int(chromosome[p - 1][0], 2), int(chromosome[p - 1][1], 2)],
                                    [int(chromosome[p][0], 2), int(chromosome[p][1], 2)],
                                    [int(chromosome[(p + 1) % total_points][0], 2),
                                     int(chromosome[(p + 1) % total_points][1], 2)]))
    greater = 0
    for angle in all_angles:        # counting number of convex angles
        if angle > 180:
            greater += 1
    if greater > total_points / 2:      # if more than half points have angles > 180
        for ind in range(len(all_angles)):      # then exterior angles are considered So,
            all_angles[ind] = 360 - all_angles[ind]     # subtracting from 360 to convert into interior
    conv_angles = 0
    for angle in all_angles:        # counting number of convex angles
        if angle > 180:
            conv_angles += 1
    return conv_angles


def fitness_calculator_csp(all_points, total_points):
    fitness = 0
    length = len(all_points)
    for i in range(0, length-1):
        for j in range(i+2, length-1):      # counting intersections against each edge
            fitness += check_intersection(Point(int(all_points[i][0], 2), int(all_points[i][1], 2)),
                                          Point(int(all_points[i+1][0], 2), int(all_points[i+1][1], 2)),
                                          Point(int(all_points[j][0], 2), int(all_points[j][1], 2)),
                                          Point(int(all_points[j+1][0], 2), int(all_points[j+1][1], 2)))
        if i+1 != length-1 and i != 0:      # for last edge
            fitness += check_intersection(Point(int(all_points[i][0], 2), int(all_points[i][1], 2)),
                                          Point(int(all_points[i+1][0], 2), int(all_points[i+1][1], 2)),
                                          Point(int(all_points[0][0], 2), int(all_points[0][1], 2)),
                                          Point(int(all_points[length-1][0], 2), int(all_points[length-1][1], 2)))
    fitness *= 100
    fitness += convex_angles(all_points, total_points)      # convex angles fitness
    return fitness


def binary_string_conversion(num):
    binary_num = str(bin(num))[2:]      # binary string of num
    zeros = ''
    for x in range(len(binary_num), 8):
        zeros += '0'        # calculating number of zeros required at start for 8 bits
    binary_num = zeros + binary_num     # adding zeros in the start
    return binary_num


def mutation(chromosome1):
    length = len(chromosome1)
    point_no = random.randint(0, length - 1)
    split_bit_no = random.randint(0, 7)
    split_bit_no2 = random.randint(0, 7)
    if chromosome1[point_no][0][split_bit_no] == '1':       # if x-axis is 1 then make it 0
        chromosome1[point_no][0] = chromosome1[point_no][0][0:split_bit_no] + '0' + chromosome1[point_no][0][
                                                                                    split_bit_no + 1: 8]
    else:                                                   # if x-axis is 0 then make it 1
        chromosome1[point_no][0] = chromosome1[point_no][0][0:split_bit_no] + '1' + chromosome1[point_no][0][
                                                                                    split_bit_no+1: 8]
    if chromosome1[point_no][1][split_bit_no2] == '1':      # if y-axis is 1 then make it 0
        chromosome1[point_no][1] = chromosome1[point_no][1][0:split_bit_no2] + '0' + chromosome1[point_no][1][
                                                                                     split_bit_no2 + 1: 8]
    else:                                                   # if y-axis is 0 then make it 1
        chromosome1[point_no][1] = chromosome1[point_no][1][0:split_bit_no2] + '1' + chromosome1[point_no][1][
                                                                                     split_bit_no2 + 1: 8]


def cross_over(chromosome1, chromosome2):
    length = len(chromosome1)
    split_bit_no = random.randint(0, 7)     # point to split x_axis
    split_bit_no2 = random.randint(0, 7)    # point to split y_axis
    chromosome3 = deepcopy(chromosome1)
    chromosome4 = deepcopy(chromosome2)
    for point in range(length):
        chromosome3[point][0] = chromosome1[point][0][0:split_bit_no] + chromosome2[point][0][split_bit_no:8]
        chromosome3[point][1] = chromosome1[point][1][0:split_bit_no2] + chromosome2[point][1][split_bit_no2:8]
        chromosome4[point][0] = chromosome2[point][0][0:split_bit_no] + chromosome1[point][0][split_bit_no:8]
        chromosome4[point][1] = chromosome2[point][1][0:split_bit_no2] + chromosome1[point][1][split_bit_no2:8]
    return [chromosome3, chromosome4]


def roulette_wheel_selection(all_fitnesses):
    max_fitness = 0
    for chromosome in all_fitnesses:
        if chromosome == 0:     # solving contradiction (1/chromosome) == infinity
            return chromosome
        max_fitness += 1/chromosome     # making max_value to divide
    select_prob = [(1/chromosome) / max_fitness for chromosome in all_fitnesses]
    return np.random.choice(all_fitnesses, p=select_prob)


def polygon_plot(points_int, total_points):
    for point in range(total_points):
        plt.plot([int(points_int[point][0],2), int(points_int[(point+1) % total_points][0], 2)], [int(points_int[point][1],2), int(points_int[(point+1) % total_points][1],2)])
    plt.show()


def genetic_algorithm(chromosomes, mutate_prob, total_points, total_chromosomes):

    print("GA----------------------------------------")
    length = len(chromosomes)
    if length % 2 == 1:
        length -= 1
    # cross-over
    for ind in range(length-1):
        chromosomes.extend(cross_over(chromosomes[ind], chromosomes[ind + 1]))
        ind += 1
    # mutation
    for ind in range(len(chromosomes)):
        if random.random() < mutate_prob:
            mutation(chromosomes[ind])
    all_fitness = []
    # fitness calculation
    for chrome in range(len(chromosomes)):
        all_fitness.append(fitness_calculator_csp(chromosomes[chrome], total_points))

    # Roulette-wheel Selection
    chrome_copy = deepcopy(chromosomes)
    new_chromes = []        # new chromosome after selection
    new_fitness = []
    for chrome in range(total_chromosomes):
        fit = roulette_wheel_selection(all_fitness)
        index = all_fitness.index(fit)
        new_chromes.append(chrome_copy[index])
        new_fitness.append(fit)
        all_fitness.pop(index)
        chrome_copy.pop(index)

    return new_chromes, new_fitness


def print_points(chromosome):
    for i in chromosome:
        print("({}, {}) ,".format(int(i[0], 2), int(i[1], 2)), end='')
    print()


def main():
    total_chromosomes = 50
    mutation_prob = 0.5
    chromosomes = []
    all_fitness = []
    total_points = int(input("Enter number of points : "))
    for val in range(total_chromosomes):
        points = []
        for point in range(total_points):
            x_axis = random.randint(0, 255)             # generating random int
            y_axis = random.randint(0, 255)
            x_axis = binary_string_conversion(x_axis)   # converting into binary of 8 bits
            y_axis = binary_string_conversion(y_axis)

            points.append([x_axis, y_axis])     # appending all points to form chromosome
        chromosomes.append(points)              # appending all chromosome in the list
    for chrome in range(len(chromosomes)):
        all_fitness.append(fitness_calculator_csp(chromosomes[chrome], total_points))

    generation = 1
    min_chrome = chromosomes[np.argmin(all_fitness)]        # chromosome with minimum fitness
    min_fitness = all_fitness[np.argmin(all_fitness)]
    max_generation = 100
    for gen in range(max_generation):
        print("Generation == {}------------------------------".format(generation))      # GA function
        chromosomes, all_fitness = genetic_algorithm(chromosomes, mutation_prob, total_points, total_chromosomes)
        for i in range(len(chromosomes)):
            print("\tFit = {} , Chromosome {} = {}".format(all_fitness[i], i+1, chromosomes[i]))
        print()
        for ind in range(len(chromosomes)):
            if all_fitness[ind] == 0:
                print("Best polygon found ---")
                print(" Polygon points : ", end='')
                print_points(chromosomes[ind])
                print(" Best Chromosome : {}".format(chromosomes[ind]))
                polygon_plot(chromosomes[ind], total_points)
                return
            if all_fitness[ind] < min_fitness:
                min_fitness = all_fitness[ind]
                min_chrome = chromosomes[ind]
        if gen == max_generation - 1:
            if min_fitness < 100:
                print("Possible Polygon(may be convex) is : ")
                print(" Polygon points : ", end='')
                print_points(min_chrome)
                print(" Best Chromosome : {}".format(min_chrome))
                polygon_plot(min_chrome, total_points)
            else:
                print("Polygon not found")
            return
        generation += 1


if __name__ == "__main__":
    main()

