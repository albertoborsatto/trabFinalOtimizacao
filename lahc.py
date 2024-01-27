import random
import time

timeout = time.time() + 4

def read_input_file(fileName):
    with open(fileName, 'r') as file:
        bin = int(file.readline())
        bin_capacity = int(file.readline())
        weights = []
        for item in range(bin):
            weights.append(int(file.readline()))

        return bin, bin_capacity, weights

def lista_com_menor_comprimento(lista_de_listas):
    if not lista_de_listas:
        return None  # Retorna None se a lista estiver vazia

    return min(lista_de_listas, key=len)

def evaluate_solution(old_solution, new_solution):
    if(len(old_solution) <= len(new_solution)):
        return old_solution
    else:
        return new_solution

#escolher um cesto aleatório e adicionar um item aleatório a ele (verificando se é uma solução válida, onde a restrição de capacidade é respeitada)
# HB: isso está bastante melhor do que antes, mas ainda há 2 problemas:
# (1) a fila/histórico lh que não é uma fila/histórico;
# (2) em questões de performance, se deveria calcular qual o valor que a nova
# solução vai ter, e ver se vai aceitar ou não ela antes de criar a mesma,
# não criar para depois jogar fora (e deixar os tamanhos das bins já
# pré-calculados também, para não ter de chamar sum toda vez).
def neighbor(bin_capacity, s, lh):
    num_bins = len(s)

    for i in range(num_bins):
        for j in range(len(s[i])):
            # Tenta mover o item de uma bin para outra
            item_to_move = s[i][j]

            for k in range(num_bins):
                if k != i:
                    if sum(s[k]) + item_to_move <= bin_capacity:
                        # Move o item para a nova bin
                        new_solution = [bin.copy() for bin in s]
                        new_solution[i].remove(item_to_move)
                        new_solution[k].append(item_to_move)
                        if(len(new_solution[i])==0):
                            new_solution.pop(i)
                        if(len(s) > len(new_solution)):
                            solution_found = late_acceptance(s, lh, new_solution)
                            return solution_found

    return s  # Retorna None se nenhuma solução melhor for encontrada

# HB: as observações sobre performances seguem, vocês deveria calcular os
# valores das soluções quando vocês alteram elas, e não recalcular toda vez.
# A lista lh pode guardar só valores, não precisa guardar soluções.
def late_acceptance(s, lh, new_solution):
    len_newsolution = len(new_solution)
    len_s = len(s)
    
    best_solution1 = evaluate_solution(len_s, len_newsolution)
    # HB: essa lista não está sendo usada como fila, só se está utilizando
    # a primeira posição, sempre. Isso é uma variável disfarçada de lista.
    best_solution2 = evaluate_solution(lh[0], len_newsolution)

    if(best_solution1 == len_newsolution or best_solution2 == len_newsolution):
        s = new_solution

    best_solution3 = evaluate_solution(len_s, lh[0])

    if(best_solution3 == len_s):
        lh.pop(0)
        lh.append(len(s))

    return [lista_com_menor_comprimento(lh), s, lh[0]]


def bin_packing_lahc(items, bin_capacity):
    current_solution = [[]]
    best = True

    #first fit
    # HB: o nome da flag me parece invertido, mas sim, esse first fit é
    # bem melhor do que o que estava sendo usado antes.
    for item in items:
        old_bin = False
        for bin in current_solution:
            if sum(bin) + item <= bin_capacity:
                bin.append(item)
                old_bin = True
                break
        if(not old_bin):
          current_solution.append([item])
    print("Initial:")
    for bin in current_solution:
        print(bin)

    # HB: Por questões de performance é bem melhor guardar na lista só
    # o valor da solução, porque essa lista só é usada para verificar
    # tu vais aceitar ou não cada nova solução.
    lh = [len(current_solution)] * 20
    s = current_solution
    for i in range(1000):
        final_solution = neighbor(bin_capacity, s, lh)
        if(len(final_solution) == 1):
            best = False
            break
        # HB: ??? Essa lista está sendo tratada como uma fila? Porque
        # aqui parece que vocês sempre só alteram a primeira posição.
        # A ideia é sempre sobrescrever o valor que está a mais tempo
        # no array.
        s = final_solution[0]
        lh[0] = final_solution[2]

    if(best): return final_solution[0]
    else: return final_solution

'''
# exemplo
items = [3,5,2,7,1,4,8,6]
bin_capacity = 10
'''

#bin, bin_capacity, items = read_input_file('instances/BPP_100_150_0.1_0.7_0.txt')

bin_capacity = 10
items = [3,5,2,7,1,4,8,6]

result = bin_packing_lahc(items, bin_capacity)

print("Result:")
for bin in result:
    print(bin)