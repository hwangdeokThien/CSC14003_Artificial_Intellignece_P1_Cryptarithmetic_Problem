from utility import *

# Initialize data from input string
def initialize_data_multiply(data):
    start = {char: -1 for char in data if char.isalpha()}
    
    data = data.replace('*', ' ')
    temp = data.split('=')
    operands = temp[0].split(' ')

    for i in range(0, len(operands)):
        operands[i] = operands[i][::-1] 

    result = temp[1]
    result = result[::-1]
    
    columns = [[] for _ in range(len(result))]
    impact = [{} for _ in range(len(result))]

    for i in range(0, len(operands[0])):
        for j in range(0, len(operands[1])):
            id = i + j
            char1 = operands[0][i]
            char2 = operands[1][j]

            if char1 not in columns[id]:
                columns[id].append(char1)
            if char2 not in columns[id]:
                columns[id].append(char2)

            if char1 not in impact[id]:
                impact[id].update({char1: {char2: 1}})
            else:
                if char2 not in impact[id][char1]:
                    impact[id][char1].update({char2: 1})
                else:
                    temp = impact[id][char1][char2] + 1
                    impact[id][char1].update({char2: temp})

    for i in range(0, len(result)):
        if result[i] not in columns[i]:
            columns[i].append(result[i])

    return start, columns, impact, result

# Check if the columns's assign is true. If it is, return carry. Otherwise, None
def check_assign_multiply(problem, assign, subres, factor, precarry):
    pos = 0

    for char1 in problem:
        if char1 in factor:
            for item in factor[char1].items():
                char2 = item[0]
                imp = item[1]

                pos += assign[char1]*assign[char2]*imp

    pos += precarry

    if pos % 10 == assign[subres]:
        return int(pos/10)

    return None

# CSP in each columns of problem
def solve_col_multiply(id_col, carry, count, state, columns, impact, result):
    if count == len(columns[id_col]):
        flag_carry = check_assign_multiply(columns[id_col], state, result[id_col], impact[id_col], carry)

        if flag_carry != None:
            res = solve_multiply(id_col+1, state, flag_carry, columns, impact, result)

            if res != None:
                return res

        return None

    char = columns[id_col][count]
    res = dict()

    if state[char] == -1:
        for val in range(0, 10):
            if val not in state.values():
                state[char] = val

                res = solve_col_multiply(id_col, carry, count+1, state, columns, impact, result)
                if res != None:
                    return res

                state[char] = -1
    else:
        res = solve_col_multiply(id_col, carry, count+1, state, columns, impact, result)

    return res

# Main solve
def solve_multiply(id_col, state, carry, columns, impact, result):
    if len(state) > 10:
        return

    if id_col == len(columns):
        if carry == 0:
            return state
        else:
            return None

    str_state = to_string(state)
    state_space = set()

    if str_state in state_space:
        return None

    res = solve_col_multiply(id_col, carry, 0, state, columns, impact, result)
    state_space.add(str_state)

    return res