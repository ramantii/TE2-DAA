import random
import time
from DP import minSizeVertexCover
from BNB import main as BnB_main
import tracemalloc


def generate_random_tree(num_vertices):
    cur_vertex = 1
    N = num_vertices[1]
    adj_list = [[] for _ in range(N + 1)]

    for i in range(1, N + 1):
        vertices_left = N - cur_vertex
        num_child = min(vertices_left, random.randrange(1, 15))
        adj_list[i] = [cur_vertex + j for j in range(1, num_child + 1)]
        cur_vertex += num_child

    return adj_list


def truncate_tree(num_vertices, adj_list):
    adj = adj_list.copy()
    M = num_vertices[0]
    for i in range(1, M + 1):
        if i <= M:
            adj[i] = [elem for elem in adj[i] if elem <= M]
    return adj[: M + 1]


def save_tree_to_file(tree, filename):
    with open(filename, "w") as f:
        f.write(f"{len(tree) - 1} {sum(len(neighbors) for neighbors in tree[1:])} 0\n")
        for i, neighbors in enumerate(tree[1:], start=1):
            f.write(f"{' '.join(map(str, neighbors))}\n")


def generate_and_run_algorithms(num_vertices, dp_filename, bnb_filename, cutoff_time):
    dp_tree = generate_random_tree(num_vertices)
    save_tree_to_file(dp_tree, dp_filename)

    bnb_tree = truncate_tree(num_vertices, dp_tree)
    save_tree_to_file(bnb_tree, bnb_filename)

    print(f"\nRunning DP Algorithm on {num_vertices[1]} vertices...")
    tracemalloc.start()
    start_time = time.time()
    minSizeVertexCover(dp_tree, num_vertices[1])
    dp_execution_time = time.time() - start_time
    _, dp_memory_usage = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print(f"\nRunning BnB Algorithm on {num_vertices[0]} vertices...")
    tracemalloc.start()
    BnB_main(bnb_filename, "Output/", cutoff_time, None)
    bnb_execution_time = time.time() - start_time - dp_execution_time
    _, bnb_memory_usage = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return dp_execution_time, dp_memory_usage, bnb_execution_time, bnb_memory_usage


def main():
    sizes = [
        (100, 10**4),
        (300, 10**5),
        (900, 10**6),
    ]
    cutoff_time = 600  # set cutoff time for BnB algorithm

    for num_vertices in sizes:
        dp_filename = f"tree_DP_{num_vertices[1]}.txt"
        bnb_filename = f"tree_BnB_{num_vertices[0]}.txt"

        dp_time, dp_memory, bnb_time, bnb_memory = generate_and_run_algorithms(
            num_vertices, dp_filename, bnb_filename, cutoff_time
        )

        print(f"\nResults for {num_vertices[1]} vertices:")
        print(f"DP Algorithm Execution Time: {dp_time} seconds")
        print(f"DP Algorithm Memory Usage: {dp_memory} bytes")
        print(f"BnB Algorithm Execution Time: {bnb_time} seconds")
        print(f"BnB Algorithm Memory Usage: {bnb_memory} bytes")
        print("=" * 40)


if __name__ == "__main__":
    main()