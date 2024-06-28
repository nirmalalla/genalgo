import random 
import math

def gen_initial_population(population_size, value_range):
    population = [[random.uniform(value_range[0], value_range[1]), random.uniform(value_range[0], value_range[1])] for _ in range(population_size)]
    return population

def fitness_function(x, y):
    return 1 / (math.sin(x) + math.cos(y) + 1e-6)

def evaluate_population(population):
    fitness_values = [fitness_function(x, y) for x, y in population]
    return fitness_values

def select_elites(population, fitness_values, num_elites):
    sorted_indices = sorted(range(len(fitness_values)), key=lambda k: fitness_values[k])
    elites = [population[i] for i in sorted_indices[:num_elites]]
    return elites

def roulette_wheel_selection(population, fitness_values):
    total_fitness = sum(fitness_values)
    selection_probs = [f / total_fitness for f in fitness_values]
    selected_index = random.choices(range(len(population)), weights=selection_probs, k=1)[0]
    return population[selected_index]

def crossover(parent1, parent2):
    child = []
    
    for p1, p2 in zip(parent1, parent2):
        alpha = random.random()
        child.append(alpha * p1 + (1 - alpha)  * p2)

    return child

def mutate(individual, mutation_rate, value_range):
    mutated_individual = []

    for param in individual:
        if random.random() < mutation_rate:
            mutation_value = random.uniform(-1, 1)
            mutated_param = param + mutation_value
            mutated_param = max(min(mutated_param, value_range[1]), value_range[0])
        else:
            mutated_param = param

        mutated_individual.append(mutated_param)

    return mutated_individual

population_size = 50
value_range = (-10, 10)
num_elites = 5
mutation_rate = 0.1
num_generations = 250

population = gen_initial_population(population_size, value_range)
for generation in range(num_generations):
    fitness_values = evaluate_population(population)
    elites = select_elites(population, fitness_values, num_elites)

    new_population = elites.copy()
    while len(new_population) < population_size:
        parent1 = roulette_wheel_selection(population, fitness_values)
        parent2 = roulette_wheel_selection(population, fitness_values)
        child = crossover(parent1, parent2)
        child = mutate(child, mutation_rate, value_range)
        new_population.append(child)

    population = new_population

    if generation % 10 == 0 and generation >= 10:
        print("Generation " + str(generation) + " complete")


final_fitness_values = evaluate_population(population)
best_individual_index = final_fitness_values.index(max(final_fitness_values))
best_individual = population[best_individual_index]

print("Best Individual:", best_individual)
print("Best Fitness Value:", final_fitness_values[best_individual_index])