from binary_search_tree import BSTNode

words = {}

# Nacitanie dat
with open("assets/dictionary.txt", "r") as file:
    for line in file:
        count, word = line.split()
        count = int(count)
        words[word] = count

# Sortovanie dat podla abecedy
words_sorted = dict(sorted(words.items()))

# Filtrpvanie klucov s f=rekvenciou ostro vacsou ako 50 000
words_keys = dict(filter(lambda val: val[1] > 50000, words_sorted.items()))


# Pravdepodobnosti vyhladavani pre kluce
def get_keys_probabilities(arr):
    probabilities_dict = {}
    sum_of_values = sum(words.values())
    for key in arr:
        probabilities_dict[key] = arr[key] / sum_of_values
    return probabilities_dict


words_keys = get_keys_probabilities(words_keys)


# Suma pravdepodobnosti hodnot medzi klucmi
def sum_between(arr, index1, index2):
    total = 0
    index = 0
    for num in arr:
        if index1 - 1 < index < index2 - 1:
            total += num
        index += 1
    return total


# Pravdepodobnosti vyhladavania pre slova, ktore nie su klucmi
def get_unsuccessful_probabilities():
    probabilities_dict = {}
    sum_of_values = sum(words_sorted.values())

    # Manualne vypocitam hodnoty medzi nultym indexom a prvym klucom
    first_value = sum_between(list(words_sorted.values()), 0,
                              list(words_sorted.keys()).index(list(words_keys.keys())[0]))
    probabilities_dict[0] = first_value / sum_of_values

    # Iterativne ratam sumy hodnot medzi klucmi
    for i in range(len(words_keys)):
        index1 = list(words_sorted.keys()).index(list(words_keys.keys())[i])
        if i == len(words_keys) - 1:
            index2 = len(words_sorted)
        else:
            index2 = list(words_sorted.keys()).index(list(words_keys.keys())[i + 1])

        sum_between_keys = sum_between(list(words_sorted.values()), index1 + 1, index2 + 1)
        probabilities_dict[i + 1] = sum_between_keys / sum_of_values
    return probabilities_dict


words_unsuccessful = list(get_unsuccessful_probabilities().values())


# Vygenerovanie tabuliek pre OBST
def optimal_bst(p, q, n):
    """
    Resource:   Introduction to algorithms
                Third edition
                page 402
    """
    costs = [[0 for x in range(1, n + 1)] for y in range(0, n + 1)]
    weights = [[0 for x in range(1, n + 1)] for y in range(0, n + 1)]
    roots = [[0 for x in range(1, n + 1)] for y in range(1, n + 1)]
    for i in range(1, n + 1):
        # iteracia po diagonale, pridalovanie pravdepodobnosti neuspesneho vyhladavania
        costs[i][i - 1] = q[i - 1]
        weights[i][i - 1] = q[i - 1]
    # iteracia cez polovicu tabulky => v smere napravo od stredovej diagonaly
    for l in range(1, n + 1):
        for i in range(1, n - l + 1):
            j = i + l - 1
            costs[i][j] = float("inf")
            weights[i][j] = weights[i][j - 1] + p[j] + q[j]
            if (i - j) == 0:
                costs[i][j] = costs[i][j - 1] + costs[j + 1][j] + weights[i][j]
                roots[i][j] = j
            # vyber stromu s najnizsou cenou pre vyhladavanie v strome
            for r in range(i - 1, j + 1):
                t = costs[i][r - 1] + costs[r + 1][j] + weights[i][j]
                if t < costs[i][j]:
                    costs[i][j] = t
                    roots[i][j] = r
    return weights, costs, roots


p_keys = [0] + list(words_keys.values())

table_weights, table_costs, table_roots = optimal_bst(p_keys, words_unsuccessful, len(words_unsuccessful))

with open('assets/costs.txt', 'w') as f:
    for row in table_costs:
        for item1 in row:
            f.write(f"{item1} ")
        f.write("\n")

with open('assets/weights.txt', 'w') as f:
    for row in table_weights:
        for item2 in row:
            f.write(f"{item2} ")
        f.write("\n")

with open('assets/roots.txt', 'w') as f:
    for row in table_roots:
        for item3 in row:
            f.write(f"{item3} ")
        f.write("\n")


# Vytvorenie OBST z vygenerovanych tabuliek
def create_obst(keys, roots):
    """
    Resource:   https://www.youtube.com/watch?v=CTUTPSXyBO8&ab_channel=ChrisBourke
    """

    n = len(roots[0])

    root = BSTNode(keys[roots[1][n - 1]])
    stack = [[root, 1, n - 1]]
    while len(stack) != 0:
        u, i, j = stack.pop()
        l = roots[i][j]
        if l < j:
            v = BSTNode(keys[roots[l + 1][j]])
            u.right = v
            stack.append([v, l + 1, j])
        if i < l:
            v = BSTNode(keys[roots[i][l - 1]])
            u.left = v
            stack.append([v, i, l - 1])
    return root


# Funckie pre pocet porovnavani pri vyhladavani v BST
def pocet_porovnani(value):
    return bst.exists(value, 0)


table_keys = [0] + list(words_keys.keys())
bst = create_obst(table_keys, table_roots)
bst.display()

pocet_porovnani("alsoo")