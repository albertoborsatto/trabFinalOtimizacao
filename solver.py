from pulp import LpProblem, LpVariable, lpSum, LpMinimize, LpInteger

def read_input_file(fileName):
    with open(fileName, 'r') as file:
        bin = int(file.readline())
        bin_capacity = int(file.readline())
        weights = []
        for item in range(bin):
            weights.append(int(file.readline()))

        return bin, bin_capacity, weights


def bin_packing_integer(items, bin_capacity, num_weights):
    # Criação do problema de programação inteira
    prob = LpProblem("BinPackingInteger", LpMinimize)

    # Variáveis de decisão binárias
    x = LpVariable.dicts("item", (range(len(items)), range(bin_capacity)), 0, 1, LpInteger)
    y = LpVariable.dicts("bin", (range(bin_capacity)), 0, 1, LpInteger)

    # Função objetivo: Minimizar o número total de contêineres usados
    prob += lpSum(y[j] for j in range(bin_capacity))

    # Restrição: Cada item só pode ser alocado a um contêiner
    for i in range(len(items)):
        prob += lpSum(x[i][j] for j in range(bin_capacity)) == 1

    # Restrição: A soma dos tamanhos dos itens em cada contêiner não pode exceder a capacidade
    for j in range(bin_capacity):
        prob += lpSum(items[i] * x[i][j] for i in range(len(items))) <= bin_capacity

    """ # Restrição: Xij <= Yj
    for i in range(len(items)):
        for j in range(len(bin_capacity)):
            prob += x[i][j] <= y[j] """

    # Resolve o problema
    prob.solve()

num_weights, bin_capacity, weights = read_input_file('instances/Falkenauer_t60_00.txt')

bin_packing_integer(weights, bin_capacity, num_weights)
