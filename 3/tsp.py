import random

# watch out! cities are numbered from 1, not from 0!!!
costs = [[0, 2, 100, 3, 6],
         [2, 0, 4, 3, 100],
         [100, 4, 0, 7, 3],
         [3, 3, 7, 0, 3],
         [6, 100, 3, 3, 0]]



def create_random_solution():
    permutation = []
    for c in range(1, 6):
        permutation.insert(random.randint(0, len(permutation)), c)
    return permutation

# example for a solution (permutation): (3,4,2,1,5)
def evaluate_solution(permutation):
    city_a = permutation[0]
    city_b = permutation[-1]
    fitness = costs[city_a-1][city_b-1]
    for i in range(0,len(permutation)-2):
        city_a = permutation[i]
        city_b = permutation[i+1]
        fitness += costs[city_a-1][city_b-1]
    return fitness




# INITIALISE population with random candidate solutions
# a) What are the choices that you must make with regards to the population?
#    Consider different issues, such as the size and whether you will mix the
#    population of several generations. After testing with different inputs, what decisions did you make?
population_size = 10
population = []
for c in range(population_size):
    solution = create_random_solution()
    population.append(solution)

# EVALUATE each candidate



# while not TERMINATION-CONDITION is satisfied do
for i in range(100):


#     SELECT parents
#     Pick 5 parents randomly and take the two best to generate offspring.
    parent_candidates = random.sample(population, 5)
    parent_candidates.sort(key=evaluate_solution, reverse=True)
    dad = parent_candidates[0]
    mom = parent_candidates[1]

#     RECOMBINE pairs of parents
#     MUTATE the resulting offspring
#     b) Describe your strategies for mutation and/or recombination of the population.


#     EVALUATE new candidates
#     SELECT individuals for the next generation
#     c) Describe your strategy for selecting the individuals for the next generation.
#        Would you deterministically select the best individuals? Why?