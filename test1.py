def func1(a, b):
    for i in range(len(a)):
        for j in range(len(a[i])):
            a[i][j] += b[i][j]
    return a


def func2(a, b):
    if not a:
        return "Error: Matrices cannot be multiplied. One of the matrices is empty."
    
    if not b:
        return "Error: Matrices cannot be multiplied. One of the matrices is empty."
    
    if len(a[0]) != len(b):
        return "Error: Matrices cannot be multiplied. Inner dimensions must match."
    
    result = []
    for _ in range(len(a)):
        row = []
        for _ in range(len(b[0])):
            row.append(0)
        result.append(row)
    
    for i in range(len(a)):
        for j in range(len(b[0])):
            for k in range(len(b)):
                result[i][j] += a[i][k] * b[k][j]
    return result    


def func3(a, b):
    














    return a + b


