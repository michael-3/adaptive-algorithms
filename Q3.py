import csv
import numpy as np

flow = list(csv.reader(open("q3_csv/Flow.csv"), delimiter=','))
distance = list(csv.reader(open("q3_csv/Distance.csv"), delimiter=','))

p = [2, 4, 1, 5, 3]
p = [4, 2, 1, 5, 3]
p = [1, 4, 2, 5, 3]

f = np.array([
    [0, 5, 2, 4, 1],
    [5, 0, 3, 0, 2],
    [2, 3, 0, 0, 0],
    [4, 0, 0, 0, 5],
    [1, 2, 0, 5, 0]
])

d = np.array([
    [0, 1, 1, 2, 3],
    [1, 0, 2, 1, 2],
    [1, 2, 0, 1, 2],
    [2, 1, 1, 0, 1],
    [3, 2, 2, 1, 0]
])

# p = [1, 2, 3, 4]

# d = np.array([
#     [0, 22, 53, 53],
#     [22, 0, 40, 62],
#     [53, 40, 0, 55],
#     [53, 62, 55, 0],
# ])

# f = np.array([
#     [0, 3, 0, 2],
#     [3, 0, 0, 1],
#     [0, 0, 0, 4],
#     [2, 1, 4, 0]
# ])


def swap(f, d, p):
    temp1 = np.copy(f)
    for i, elem in enumerate(f):
        temp1[i, :] = f[p[i] - 1, :]

    temp2 = np.copy(temp1)
    for i, elem in enumerate(temp1):
        temp2[:, i] = temp1[:, p[i] - 1]

    return sum(np.diag(temp2.dot(d)))

cost = swap(f, d, p)
print cost

# my_array = np.arange(9).reshape(3, 3)
# swap_rows(my_array, 0, 2)
# print my_array

# print pfp

# print flow
# print distance
