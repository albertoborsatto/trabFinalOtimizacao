import random
import time

timeout = time.time() + 4

# Global variables
bin_capacity = 0
s = [[]]
lh = []
randomize = False

def read_input_file(fileName):
    global bin_capacity
    with open(fileName, 'r') as file:
        bin_count = int(file.readline())
        bin_capacity = int(file.readline())
        weights = []
        for item in range(bin_count):
            weights.append(int(file.readline()))

        return bin_count, bin_capacity, weights

def lista_com_menor_comprimento(lista_de_listas):
    if not lista_de_listas:
        return None  # Returns None if the list is empty

    return min(lista_de_listas, key=len)

def evaluate_solution(old_solution, new_solution):
    if(len(old_solution) < len(new_solution)):
        return old_solution
    elif(len(new_solution) < len(old_solution)):
        return new_solution
    else:
        menor_soma_old = min(map(sum, old_solution))
        menor_soma_new = min(map(sum, new_solution))
        if(menor_soma_new <= menor_soma_old): return new_solution
        else: return old_solution

def neighbor():
    global bin_capacity, s, lh
    num_bins = len(s)

    for i in range(num_bins):
        for j in range(len(s[i])):
            # Try to move the item from one bin to another
            item_to_move = s[i][j]

            for k in range(num_bins):
                if k != i:
                    if sum(s[k]) + item_to_move <= bin_capacity:
                        # Move the item to the new bin
                        new_solution = [bin.copy() for bin in s]
                        new_solution[i].remove(item_to_move)
                        new_solution[k].append(item_to_move)
                        if(len(new_solution[i])==0):
                            new_solution.pop(i)
                        late_acceptance(new_solution)
                        return

def late_acceptance(new_solution):
    global bin_capacity, s, lh, randomize
    best_solution1 = evaluate_solution(s, new_solution)
    best_solution2 = evaluate_solution(lh[0], new_solution)

    if(best_solution1 == s):
        randomize = True
        return
    
    if(best_solution1 == new_solution or best_solution2 == new_solution):
        s = new_solution
    
    best_solution3 = evaluate_solution(lh[0], s)

    if(best_solution3 == s):
        lh.pop(0)
        lh.append(s)

def bin_packing_lahc(items):
    global bin_capacity, s, lh, randomize
    current_solution = [[]]

    # First fit
    """ for item in items:
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
        print(bin) """
    
    current_solution = [[3],[5], [2], [7], [1], [4], [8], [6]]

    lh = [current_solution] * 20
    s = lh[0]
    for i in range(1000):
        if(randomize):
            random.shuffle(s)
            randomize = False
            print(s)
        neighbor()

'''
# exemplo
items = [3,5,2,7,1,4,8,6]
bin_capacity = 10
'''

#bin, bin_capacity, items = read_input_file('instances/BPP_100_150_0.1_0.7_0.txt')

if __name__ == '__main__':
    bin_capacity = 10
    items = [3,5,2,7,1,4,8,6]

    bin_packing_lahc(items)
    print("Result:")
    for bin in s:
        print(bin)
