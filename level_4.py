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
    
    subtree = [[] for _ in range(len(result))]
    impact = [{} for _ in range(len(result))]

    for i in range(0, len(operands[0])):
        for j in range(0, len(operands[1])):
            id = i + j
            char1 = operands[0][i]
            char2 = operands[1][j]

            if char1 not in subtree[id]:
                subtree[id].append(char1)
            if char2 not in subtree[id]:
                subtree[id].append(char2)

            if char1 not in impact[id]:
                impact[id].update({char1: {char2: 1}})
            else:
                if char2 not in impact[id][char1]:
                    impact[id][char1].update({char2: 1})
                else:
                    temp = impact[id][char1][char2] + 1
                    impact[id][char1].update({char2: temp})

    for i in range(0, len(result)):
        if result[i] not in subtree[i]:
            subtree[i].append(result[i])

    return start, subtree, impact, result

def check_assign_multiply(problem, assign, subRes, factor, preCarry):
    pos = 0

    for char1 in problem:
        if char1 in factor:
            for item in factor[char1].items():
                char2 = item[0]
                imp = item[1]

                pos += assign[char1]*assign[char2]*imp

    pos += preCarry

    if pos % 10 == assign[subRes]:
        return int(pos/10)

    return None

def solve_sub_multiply(idSP, carry, id, localState, subtree, impact, result):
    if id == len(subtree[idSP]):
        temp = check_assign_multiply(subtree[idSP], localState, result[idSP], impact[idSP], carry)

        if temp != None:
            res = solve_multiply(idSP+1, localState, temp, subtree, impact, result)

            if res != None:
                return res

        return None

    # subtree(set))
    char = subtree[idSP][id]
    res = dict()

    if localState[char] == -1:
        for val in range(0, 10):
            if val not in localState.values():
                localState[char] = val

                res = solve_sub_multiply(idSP, carry, id+1, localState, subtree, impact, result)
                if res != None:
                    return res

                localState[char] = -1
    else:
        res = solve_sub_multiply(idSP, carry, id+1, localState, subtree, impact, result)

    return res

def solve_multiply(idSP, state, carry, subtree, impact, result):
    if len(state) > 10:
        return

    if idSP == len(subtree):
        if carry == 0:
            return state
        else:
            return None

    str_state = to_string(state)
    state_space = set()

    if str_state in state_space:
        return None

    res = solve_sub_multiply(idSP, carry, 0, state, subtree, impact, result)
    state_space.add(str_state)

    return res