from level1_3 import *
from level_4 import *

if __name__ == '__main__':
    data = read_file("input.txt")
    first_chars = get_first_chars(data)

    if '*' not in data: 
        start, subtree, impact  = initialize_data(data)
        res = solve(0, start, 0, subtree, impact, first_chars)
    elif '*' in data:
        start, subtree, impact, result = initialize_data_multiply(data)
        res = solve_multiply(0, start, 0, subtree, impact, result)    

    output = ""
    if res != None:
        for item in sorted(res.items(), key = lambda x: x[0]):
            print(item[1], end = "")
            output += str(item[1])
        write_file("output.txt", output)
    else:
        print("NO SOLUTION")
    

