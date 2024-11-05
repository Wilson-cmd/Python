from random import randint

x = int(12)
z = int(0)

matrix_1 = [[0 for i in range(x)] for j in range(x)]
matrix_2 = []

n = int(input())

operator = input().upper()

for k in range(x):
    for l in range(x):
        y = round(randint(1000, 1500), 2)
        matrix_1[k][l] = y

for m in range(x):
    matrix_2.append(matrix_1[z][n])
    z +=1

if(operator == "S"):
    print(round(sum(matrix_2), 1))

elif(operator == "M"):
    print(round(sum(matrix_2)/len(matrix_2), 1))
else:
    0
