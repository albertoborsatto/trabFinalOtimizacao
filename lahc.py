import random
import time

timeout = time.time() + 4

def lista_com_menor_comprimento(lista_de_listas):
    if not lista_de_listas:
        return None  # Retorna None se a lista estiver vazia

    return min(lista_de_listas, key=len)

# HB: isso retorna o peso da bin de maior peso não? Isso não é o objetivo
# do problema, o fitness da solução tem de ser o número de bins usadas
# (e você quer minimizar esse número). Vocês podem ter tiebreakers em caso
# de empate, mas o principal número é o número de bins usadas.
def evaluate_solution(old_solution, new_solution):
    if(len(old_solution) <= len(new_solution)):
        return old_solution
    else:
        return new_solution

# HB: Essa função cria um vizinho aleatório, não explora a vizinhança.  É
# necessário que para cada solução, vocês vão gerando todos os possíveis
# vizinhos sistematicamente (de preferência um por vez para não encher a
# memória), e dai peguem o primeiro que melhora, ou o que melhora mais de todos
# (é necessário implementar algum critério de desempate, já que grande parte
# das soluções vai ter o mesmo valor de solução, como considerar melhor as
# soluções com pouco peso na bin de menor peso). EDIT: eu acho que vocês
# interpretaram mal o "Escolhe s' em N(s)" do slide, ele é escolher um vizinho
# por "first improvement" ou por "best improvement" como eu mencionei acima.
#escolher um cesto aleatório e adicionar um item aleatório a ele (verificando se é uma solução válida, onde a restrição de capacidade é respeitada)
def neighbor(current_solution, bin_capacity, s, lh):
    num_bins = len(current_solution)

    for i in range(num_bins):
        for j in range(len(current_solution[i])):
            # Tenta mover o item de uma bin para outra
            item_to_move = current_solution[i][j]

            for k in range(num_bins):
                if k != i:
                    if sum(current_solution[k]) + item_to_move <= bin_capacity:
                        # Move o item para a nova bin
                        new_solution = [bin.copy() for bin in current_solution]
                        new_solution[i].remove(item_to_move)
                        new_solution[k].append(item_to_move)
                        late_acceptance(s, lh, new_solution)
                        return new_solution
    
    return None  # Retorna None se nenhuma solução melhor for encontrada

def late_acceptance(s, lh, new_solution):
    # HB: Performance: As soluções nunca deveriam ser avaliadas a partir
    # do zero, lembrem-se que na aula eu falei que a principal coisa a ser
    # avaliada sobre performance é que o valor das soluções deve ser
    # calculado quando elas são modificadas e de forma incremental.
    best_solution1 = evaluate_solution(s, new_solution)
    best_solution2 = evaluate_solution(lh[0], new_solution)
    best_solution3 = evaluate_solution(s, lh[0])

    if(best_solution1 == new_solution or best_solution2 == new_solution):
        s = new_solution
    
    if(best_solution3 == s):
        lh[0] = s

    return lista_com_menor_comprimento(lh)


    # HB: Esse código abaixo é completo nonsense. O LAHC não usa critério de
    # aleatoriedade para aceitação. O único critério do LAHC é se a solução é
    # melhor que a solução há h iterações atrás (onde h é o único parâmetro da
    # meta-heurística). Não há uma lista de valores de solução de tamanho h
    # sendo mantida/passada onde verificar essa informação. Essa lista é a
    # única estrutura de dados obrigatória do LAHC.
def bin_packing_lahc(items, bin_capacity):
    current_solution = [[]]

    # HB: essa não é uma inicialização muito boa, melhor que cada item em uma
    # bin distinta, sem dúvida. Entretanto, uma solução inicial melhor seria
    # colocar o item na primeira bin das já usadas que ele cabe, não sempre na
    # última usada ou abrir outra uma nova.
    #current solution population
    
    for item in items:
        new_bin = False
        for bin in current_solution:
            if sum(bin) + item <= bin_capacity:
                bin.append(item)
                new_bin = True
                break
        if(not new_bin):
          current_solution.append([item])
    print(current_solution)
        

    # HB: lembrando que o critério de parada não pode ser tempo. O
    # critério pode ser um número de iterações. Não confundam esse
    # critério com o parâmetro h que é o tamanho da lista do LAHC
    # (e que se refere a quantas iterações atrás você olha para decidir
    # se vai aceitar ou não a solução).
    # apply late acceptance hill climbing with timeout (pretendemos colocar timeout após verificar que implementação está correta)
    lh = [[current_solution] * 20]
    s = lh[0]
    for i in range(1000):
        new_solution = neighbor(current_solution, bin_capacity, s, lh)
        final_solution = late_acceptance(s, lh, new_solution)

    return final_solution

# exemplo
items = [3,5,2,7,1,4,8,6]
bin_capacity = 10
result = bin_packing_lahc(items, bin_capacity)

print("Result:")
for bin in result:
    print(bin)