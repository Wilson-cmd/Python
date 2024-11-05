# Referencia do estudo que realizei:
# https://www.educamaisbrasil.com.br/enem/matematica/sequencia-de-fibonacci

# Definicao da variavel de contagem:
x = str()

# Verificacao se numero
while(not x.isnumeric()):
    x = input('Informe um numero: ')

# Converte o x para um numero inteiro
x = int(x)

# Se x for maior que dois ele inicia a estrutura
if(x >= 2):
    
    # Variavel para tratamento e calculo da sequencia de Fibonacci
    y = str()
    
    # Comando para incrementar valores na variavel y
    for i in range(x):
     y = y + str(i) + " "

    # Separa os itens inclusos na lista
    y = y.split()

    # Calculo da sequencia
    for i in range(x):
        if(y[i] > "1"):
            y[i] = str(int(y[i-2]) + int(y[i-1]))
        else:
            continue

    # Variavel que armazenara o resultado da sequencia como string       
    z = str()
    for i in y:
        z = z + " " + str(i) 

    # Apresentação em tela do resultado    
    print(z)

else: 

    # Caso o valor de x seja inferior a 2  
    print("="*75)
    print(f'Com o numero {x} não foi possivel iniciar a sequencia, tente um numero maior.'.upper())
    print("="*75)



