# Convert dict to string
def to_string(data_dict):
    return "".join(str(value) for value in data_dict.values())

# Process input data from file, handle parentheses and change signs
def read_file(filename):
    f = open(filename)
    data = f.read()
    result = ""
    sign = 0

    for i in range(0, len(data)):
        if data[i].isalpha():
            result += data[i]
        else:
            if data[i] == '(':
                if i > 0 and data[i-1] == '-':
                    sign = 1
                continue
            if data[i] == ')':
                sign = 0
                continue

            if sign == 1:
                if data[i] == '+':
                    result += '-'
                else:
                    if data[i] == '-':
                        result += '+'
            else:
                result += data[i]

    return result

# Write the result to output file
def write_file(filename, result):
    try:
        with open(filename, "w") as f:
            f.write(result)
        return True
    except:
        return False
    

def get_first_chars(data):
    # Split the expression by '+' and '-' to extract individual words
    words = data.replace('=', '+').split('+')
    first_chars = set(word[0] for word in words)
    return first_chars

def is_first_chars(char, first_chars):
    return char in first_chars