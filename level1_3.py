from utility import *

# Initialize data from input string
def initialize_data(data):
    start = {char: -1 for char in data if char.isalpha()}
    operators = ['+'] + [char for char in data if char in ('+', '-')]

    data = data.replace('+', ' ')
    data = data.replace('-', ' ')

    temp = data.split('=') 
    operands = temp[0].split(' ')
 
    result = temp[1]

    max_len_operand = max(len(opr) for opr in operands)
    tmp = max(len(result), max_len_operand)

    subtree = [[] for _ in range(tmp)]
    impact = [{} for _ in range(tmp)]

    for i in range(len(operands)):
        opr = operands[i] 

        for j in range(len(opr)):
            id = len(opr) - j - 1

            if not opr[j] in impact[id]:
                if operators[i] == '+':
                    pos = 1
                    neg = 0
                else:
                    pos = 0
                    neg = 1

                subtree[id].append(opr[j])
                impact[id].update({opr[j]: (pos, neg)})
            else:
                pos = impact[id][opr[j]][0]
                neg = impact[id][opr[j]][1]

                if operators[i] == '+':
                    pos = pos + 1
                else:
                    neg = neg + 1

                impact[id].update({opr[j]: (pos, neg)})

    for i in range(len(result)):
        char = result[len(result)-i-1]

        if char not in subtree[i]:
            subtree[i].append(char)
            impact[i].update({char: (0, 1)})
        else:
            pos = impact[i][char][0]
            neg = impact[i][char][1] + 1
            impact[i].update({char: (pos, neg)})
    
    return start, subtree, impact

# Check if the subproblem's assign is valid 
# # If it is, return carry. Otherwise, None
def check_assign(problem, assign, factor, precarry):
    pos, neg = 0, 0

    for char in problem:
        pos = pos + assign[char]*factor[char][0]
        neg = neg + assign[char]*factor[char][1]

    A = pos + precarry
    B = neg
    
    if A < 0:
        return None

    temp = A % 10 - B % 10

    if (temp == 0):
        return int(A/10) - int(B/10)

    return None

# solveSub[1]  0 1 2 3 4 5 six SP[2] SP[3] 
def solve_sub(idSP, carry, id, localState, subtree, impact, first_chars):
    if id == len(subtree[idSP]):
        temp = check_assign(subtree[idSP], localState, impact[idSP], carry)

        if temp is not None:
            res = solve(idSP+1, localState, temp, subtree, impact, first_chars)

            if res is not None:
                return res

        return None

    # subtree(set))
    char = subtree[idSP][id]
    res = dict()

    if localState[char] == -1:
        # If the character is in first_chars, start from 1 instead of 0
        start_val = 1 if is_first_chars(char, first_chars) else 0

        for val in range(start_val, 10):
            if val not in localState.values():
                localState[char] = val

                res = solve_sub(idSP, carry, id+1, localState, subtree, impact, first_chars)
                if res != None:
                    return res

                localState[char] = -1
    else:
        res = solve_sub(idSP, carry, id+1, localState, subtree, impact, first_chars)

    return res

def solve(idSP, state, carry, subtree, impact, first_chars):
    if len(state) > 10:
        return None

    if idSP == len(subtree):
        if carry == 0:
            return state
        else:
            return None

    str_state = to_string(state)
    state_space = set()

    if str_state in state_space:
        return None

    res = solve_sub(idSP, carry, 0, state, subtree, impact, first_chars)
    state_space.add(str_state)

    return res