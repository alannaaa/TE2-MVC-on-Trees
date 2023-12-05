import random

def generate_tree(n, n_small, size_type):
    tree = [[] for _ in range(n)]

    for i in range(2, n + 1):
        parent = random.randint(1, i - 1)
        tree[parent - 1].append(i)
        tree[i - 1].append(parent)

    write_to_file(tree, f"{size_type}_dp")
    generate_smaller(tree, n_small, size_type)

def generate_smaller(adj_list, n_small, size_type):
    bnb_adj_list = adj_list[:n_small]

    for i in range(len(bnb_adj_list)):
        bnb_adj_list[i] = [neighbor for neighbor in bnb_adj_list[i] if neighbor < n_small+1]

    write_to_file(bnb_adj_list, f"{size_type}_bnb")

def write_to_file(adj_list, filename):
    filename = "dataset/" + filename + ".txt"
    with open(filename, 'w') as file:
        file.write(f"{len(adj_list)}\n")
        for neighbors in adj_list:
            file.write(f"{' '.join(map(str, neighbors))}\n")

def main():
    dp_sizes = [10**4, 10**5, 10**6]
    bnb_sizes = [100, 300, 900]

    generate_tree(dp_sizes[0], bnb_sizes[0], "s")
    generate_tree(dp_sizes[1], bnb_sizes[1], "m")
    generate_tree(dp_sizes[2], bnb_sizes[2], "l")

if __name__ == "__main__":
    main()