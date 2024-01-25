import random
import time

timeout = time.time() + 4

def evaluate_solution(solution):
    #retorna solução melhor
    return max(sum(bin) for bin in solution)

def neighbor(current_solution):
    #escolher um cesto aleatório e adicionar um item aleatório a ele (verificando se é uma solução válida, onde a restrição de capacidade é respeitada)
    new_solution = [list(bin) for bin in current_solution]
    random_item = random.choice(range(len(items)))
    random_bin = random.choice(range(len(new_solution)))
    if sum(new_solution[random_bin]) + items[random_item] <= bin_capacity:
        new_solution[random_bin].append(items[random_item])
        new_solution[random_bin].sort()
    return new_solution

def late_acceptance(current_solution, new_solution, iterations=50):
    current_fitness = evaluate_solution(current_solution)
    new_fitness = evaluate_solution(new_solution)

    if new_fitness < current_fitness:
        return new_solution

    # probabilidade de aceitar solução pior
    for i in range(1, iterations + 1):
        if random.random() < 1 / i:
            return new_solution

    return current_solution

def bin_packing_lahc(items, bin_capacity):
    current_solution = [[]]

    #current solution population
    for item in sorted(items, reverse=True):
        if sum(current_solution[-1]) + item <= bin_capacity:
            current_solution[-1].append(item)
        else:
            current_solution.append([item])

    # apply late acceptance hill climbing with timeout
    while time.time() < timeout:
        new_solution = neighbor(current_solution)
        current_solution = late_acceptance(current_solution, new_solution)

    return current_solution

# exemplo
items = [3, 5, 2, 7, 1, 4, 8, 6]
bin_capacity = 10
result = bin_packing_lahc(items, bin_capacity)

print("Result:")
for bin in result:
    print(bin)