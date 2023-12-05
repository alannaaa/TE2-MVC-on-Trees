from TE2.dp import min_size_vertex_cover as dp
from TE2.bnb import BnB as bnb, create_graph
from time import time
import tracemalloc

def dataset_to_array(filename):
    n = -1
    result_array = []

    with open(filename, 'r') as file:
        for line_number, line in enumerate(file, start=1):
            if line_number == 1:
                n = line.strip()
                continue
            
            # Split the line into a list of integers
            values = list(map(int, line.strip().split()))
            
            # Append the values to the result array
            result_array.append(values)
    
    return result_array, int(n)

def bnb_main(adj_list, size_type):
	# CONSTRUCT THE GRAPH BASED ON ADJACENT LIST
	g = create_graph(adj_list)

	tracemalloc.start()
	sol_vc, time = bnb(g)
	mem = str(tracemalloc.get_traced_memory()[1])
	tracemalloc.stop()

	for element in sol_vc:
		if element[1]==0:
			sol_vc.remove(element)

	#WRITE SOL FILES
	with open(f'output/{size_type}_bnb.sol', 'w') as f:
		f.write('%i\n' % (len(sol_vc)))
		f.write(','.join([str(x[0]) for x in sol_vc]))
		f.write(f"\nTime: {time}, Memory: {mem} bytes\n\n")


	return (time, mem)

def dp_main(adj, n, size_type):
    t0 = time()
    tracemalloc.start()
    sol_vc = dp(adj,n)
    delta_time = time() - t0
    mem = str(tracemalloc.get_traced_memory()[1])
    tracemalloc.stop()

    with open(f'output/{size_type}_dp.sol', 'w') as f:
            f.write(f'{sol_vc}\n')
            f.write(f"Time: {delta_time}, Memory: {mem} bytes\n\n")

    return (delta_time, mem)


def main():
    datasets = [
        "s_dp.txt",
        "m_dp.txt",
        "l_dp.txt",
        "s_bnb.txt",
        "m_bnb.txt",
        "l_bnb.txt",
    ]

    with open("results.txt", 'w') as result_file:
        for dataset in datasets:
            adj_list, n = dataset_to_array("dataset/" + dataset)
         
            size_type, algo = dataset.strip(".txt").split("_")
            if algo == "dp":
                result = dp_main([[]] + adj_list, n, size_type)
            elif algo == "bnb":
                result = bnb_main(adj_list, size_type)

            # Write results to the file
            result_file.write(f"Size Type: {size_type.capitalize()}, Algorithm: {algo.capitalize()}\n")
            result_file.write(f"Time: {result[0]}, Memory: {result[1]} bytes\n\n")

if __name__ == "__main__":
    main()
