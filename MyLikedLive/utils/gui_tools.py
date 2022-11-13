# A set of functions to help with making the gui look pretty

# Returns a string of the list in the desired style
line_length = 67

def list_styling(l):
    result = [""]
    for item in l:
        if len(item) > line_length:
            if result[-1]:
                result[-1] = result[-1][:-2]
            else:
                result.pop(-1)
            result += [item[:line_length-3] + "\n     " + item[line_length-3:] + "  "]
        elif len(result[-1]) + len(item) < line_length:
            result[-1] += item + ", "
        else:
            result[-1] = result[-1][:-2]
            result += [item + ", "]
    result[-1] = result[-1][:-2]


    return ">>> " + "\n>>> ".join(result)
