# Inicializa a variável que contém a iteração atual
currIteration = 0
# Lista de identificação das variáveis pela posição na lista
variables = []
# Índices da lista 'variables' que são as variáveis de excesso
excessVariables = []
# Contém o ÍNDICE das variáveis que são base relativos à lista 'variables'
baseVariables = []
# Contém o ÍNDICE das variáveis que são base relativos à lista 'variables'
funcObj = []

# Mapeamento de restrições. Chave é o número da equação e Valor é a lista de valores
restrictions = {}
# Contém os valores índices da função objetivo
cj = []
# Contém os valores de beta para cada 'key' (índice) de restrictions
beta = []

def getVariables():
    return variables

# Retorna a iteração atual
def getCurrIteration():
    return currIteration

# Incrementa a iteração atual
def __incrementIteration():
    global currIteration
    currIteration += 1

# Define todo o conteúdo da primeira iteração com base nos valores inseridos
def initial(funcObjR, restList, inequalities):
    global cj
    global beta
    global restrictions
    global funcObj
    funcObj = funcObjR

    # cada restrição tem uma variável a mais
    for variable in range(0, len(restList)* 2):
        # Cria o nome da variável
        variableName = "x{0}".format(variable + 1)
        variables.append(variableName)
        # Verifica se a variável está na função objetivo
        if variable >= len(restList):
            funcObj.append(0)
            excessVariables.append(variable)
            baseVariables.append(variable)
    # Laço condicional responsável em criar as restrições com preenchimento de 0 e 1 conforme matriz identidade
    for key in restList:
        # Armazena o valor da restrição
        value = restList[key]
        # Inicializa a variável de comparação identidade
        identity = 1
        base = 0
        # Enquanto houver variáveis de excesso faltando:
        for base in baseVariables:
            # Se a variável de excesso for igual a variável de comparação identidade, adiciona 1, senão 0
            if key == identity:
                value.append(1)
            else:
                value.append(0)
            # Aumenta o valor da variável de comparação identidade
            identity += 1
        restrictions[base] = value
    # Atribui a função objetivo na lista de cj
    cj = funcObj
    # Atribui as desigualdades na lista de beta
    beta = inequalities
    print(f"\nVariaveis do problema e com preenchimento do excesso: {variables}")
    print(f"Função objetivo: {funcObj}")
    print(f"Variáveis base: {baseVariables}")
    print(f"Restrições com preenchimento da identidade: {restrictions}\n")
    nextIteration()


# Calcula o valor de Zj
def __evaluateZj():
    pass

# Calcula o valor de Cj - Zj
def __evaluateCjZj():
    pass

# Realiza a próxima iteração
def nextIteration():
    zj = []
    for value in range(len(variables)):
        sumZj = 0
        for index in baseVariables:
            print(index)
            print("Índice da Variável Base: {0}, RestVal: {1}, Variável: {2}".format(index, restrictions[index][value], variables[value]))
            sumZj += funcObj[index] * restrictions[index][value]
        zj.append(sumZj)
    print(zj)

##################################### Teste
initial([2,3], {1:[8,7], 2:[5,4]}, [42,44])
