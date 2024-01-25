import random
import time

timeout = time.time() + 4

def evaluate_solution(solution):
    #retorna solução melhor
    return max(sum(bin) for bin in solution)

#escolher um cesto aleatório e adicionar um item aleatório a ele (verificando se é uma solução válida, onde a restrição de capacidade é respeitada)
def neighbor(current_solution):
    new_solution = [list(bin) for bin in current_solution]  # copiar solução atual
    random_bin_item = random.choice(range(len(new_solution)))   # escolher um cesto aleatório (1)
    random_item = random.choice(range(len(new_solution[random_bin_item])))  # escolher um item aleatório do random_bin_item
    random_bin = random.choice(range(len(new_solution)))    # escolher outro cesto aleatório (2)

    #print(sum(new_solution[random_bin]), " - ", new_solution[random_bin_item][random_item])

    #caso o item do cesto aleatório 'random_bin_item' + a soma dos item do cesto aleatório random_bin seja menor ou igual que a capacidade do cesto:
    if sum(new_solution[random_bin]) + new_solution[random_bin_item][random_item] <= bin_capacity:
        try:
            new_solution[random_bin].append(new_solution[random_bin_item][random_item]) #fazer um append do item ao cesto
            new_solution[random_bin_item].remove(new_solution[random_bin_item][random_item])    #remover item de seu cesto original
            if(len(new_solution[random_bin_item])==0):  #caso o cesto original do item estiver vazio após sua retirada
                new_solution.pop(random_bin_item)           #remover cesto vazio
            new_solution[random_bin].sort() #sort do cesto 
        except:
            print("nao sei porque sort da out_of_range exception")  #às vezes o sort dá exceção por alguma razão
        
        #print("new solution2: ", new_solution)
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

    # apply late acceptance hill climbing with timeout (pretendemos colocar timeout após verificar que implementação está correta)
    for i in range(1000):
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