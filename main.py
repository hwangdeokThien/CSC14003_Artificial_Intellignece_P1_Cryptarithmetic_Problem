import time
import tracemalloc
from level1_3 import *
from level_4 import *

def main():
    # Start tracking running time & memory usage
    tracemalloc.start()
    start_time = time.time()

    data = read_file("input.txt")
    first_chars = get_first_chars(data)  

    if '*' not in data:
        state, columns, impact  = initialize_data(data)
        solution = solve(0, state, 0, columns, impact, first_chars)
    elif '*' in data:
        state, columns, impact, result = initialize_data_multiply(data)
        solution = solve_multiply(0, state, 0, columns, impact, result)    

    # Stop tracking running time & memory usage
    end_time = time.time()
    peak = tracemalloc.get_traced_memory()[1]
    tracemalloc.stop()

    output = ""
    if solution != None:
        sorted_solution = sorted(solution.items(), key = lambda x: x[0])
        print("Sorted solution: ", sorted_solution)
        for item in sorted_solution:
            output += str(item[1])
    else:
        output = "NO SOLUTION"
        print("NO SOLUTION")

    print(f"Time execute: {end_time-start_time:.5f} s")
    print(f"Memory use: {peak/1024**2:.5f} mb")
    write_file("output.txt", output)

if __name__ == '__main__':
    main()
    

