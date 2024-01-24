from pulp import LpProblem, LpVariable, lpSum, LpMinimize, LpInteger

def bin_packing_integer(items, bin_capacity):
    # Criação do problema de programação inteira
    prob = LpProblem("BinPackingInteger", LpMinimize)

    # Variáveis de decisão binárias
    x = LpVariable.dicts("item", (range(len(items)), range(len(bin_capacity))), 0, 1, LpInteger)
    y = LpVariable.dicts("bin", (range(len(bin_capacity))), 0, 1, LpInteger)

    # Função objetivo: Minimizar o número total de contêineres usados
    prob += lpSum(y[j] for j in range(len(bin_capacity)))

    # Restrição: Cada item só pode ser alocado a um contêiner
    for i in range(len(items)):
        prob += lpSum(x[i][j] for j in range(len(bin_capacity))) == 1

    # Restrição: A soma dos tamanhos dos itens em cada contêiner não pode exceder a capacidade
    for j in range(len(bin_capacity)):
        prob += lpSum(items[i] * x[i][j] for i in range(len(items))) <= bin_capacity[j]

    """ # Restrição: Xij <= Yj
    for i in range(len(items)):
        for j in range(len(bin_capacity)):
            prob += x[i][j] <= y[j] """

    # Resolve o problema
    prob.solve()

    # Imprime o status da solução
    print("Status:", prob.status)
    # Imprime a solução
    for j in range(len(bin_capacity)):
        print(f"Contêiner {j + 1}:")
        for i in range(len(items)):
            if x[i][j].value() == 1:
                print(f"  Item {i + 1} (Tamanho: {items[i]})")

# Exemplo de uso
items = [2, 5, 8, 7, 3]
bin_capacity = [10, 10]

bin_packing_integer(items, bin_capacity)
