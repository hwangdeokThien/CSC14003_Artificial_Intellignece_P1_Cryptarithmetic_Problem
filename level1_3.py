from utility import *

# Initialize data from input string
def initialize_data(data):
    init_state = {char: -1 for char in data if char.isalpha()} # {'F': -1, 'G': -1, ...}
    operators = ['+'] + [char for char in data if char in ('+', '-')]

    data = data.replace('+', ' ')
    data = data.replace('-', ' ')

    temp = data.split('=') 
    operands = temp[0].split(' ')
 
    result = temp[1]

    max_len_operand = max(len(opr) for opr in operands)
    tmp = max(len(result), max_len_operand)

    columns = [[] for _ in range(tmp)]
    impact = [{} for _ in range(tmp)]

    for i in range(len(operands)):
        opr = operands[i] 

        for j in range(len(opr)):
            id = len(opr) - j - 1

            if not opr[j] in impact[id]:
                if operators[i] == '+':
                    upper = 1
                    lower = 0
                else:
                    upper = 0
                    lower = 1

                columns[id].append(opr[j])
                impact[id].update({opr[j]: (upper, lower)})
            else:
                upper = impact[id][opr[j]][0]
                lower = impact[id][opr[j]][1]

                if operators[i] == '+':
                    upper = upper + 1
                else:
                    lower = lower + 1

                impact[id].update({opr[j]: (upper, lower)})

    for i in range(len(result)):
        char = result[len(result)-i-1]

        if char not in columns[i]:
            columns[i].append(char)
            impact[i].update({char: (0, 1)})
        else:
            upper = impact[i][char][0]
            lower = impact[i][char][1] + 1
            impact[i].update({char: (upper, lower)})
    
    return init_state, columns, impact

# Check if the columns's assign is true 
# If it is, return carry. Otherwise, None
def check_assign(problem, assign, factor, precarry):
    upper, lower = 0, 0

    for char in problem:
        upper = upper + assign[char]*factor[char][0]
        lower = lower + assign[char]*factor[char][1]

    A = upper + precarry
    B = lower
    
    if A < 0:
        return None

    temp = A % 10 - B % 10

    if (temp == 0):
        carry = int(A/10) - int(B/10)
        return carry

    return None

def solve_col(id_col, carry, count, state, columns, impact, first_chars):
    if count == len(columns[id_col]):
        flag_carry = check_assign(columns[id_col], state, impact[id_col], carry)

        if flag_carry is not None:
            res = solve(id_col+1, state, flag_carry, columns, impact, first_chars)

            if res is not None:
                return res

        return None

    char = columns[id_col][count]
    res = dict()

    if state[char] == -1:
        # If the character is in first_chars, start from 1 instead of 0
        start_val = 1 if is_first_chars(char, first_chars) else 0

        for val in range(start_val, 10):
            if val not in state.values():
                state[char] = val

                res = solve_col(id_col, carry, count+1, state, columns, impact, first_chars)
                if res != None:
                    return res

                state[char] = -1
    else:
        res = solve_col(id_col, carry, count+1, state, columns, impact, first_chars)
    return res

def solve(id_col, state, carry, columns, impact, first_chars):
    # Number assign only 0-9
    if len(state) > 10:
        return None
        
    # Check if number of solve columns equal to length of columns or not 
    # Stop condition
    if id_col == len(columns):
        if carry == 0:
            return state
        else:
            return None

    str_state = to_string(state)
    state_space = set()

    if str_state in state_space:
        return None

    res = solve_col(id_col, carry, 0, state, columns, impact, first_chars)
    state_space.add(str_state)
    return res