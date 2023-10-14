import math


# Inicializa a variável que contém a iteração atual
currIteration = 0
# Lista de identificação das variáveis pela posição na lista
variables = []
# Índices da lista 'variables' que são as variáveis de excesso
excessVariables = []
# Contém o ÍNDICE das variáveis que são base relativos à lista 'variables'
baseVariables = []
# Lista para a função objetivo do problema
funcObj = []

# Mapeamento de restrições. Chave é o número da equação e Valor é a lista de valores
restrictions = {}
# Contém os valores índices da função objetivo
cj = []
# Contém os valores de beta para cada 'key' (índice) de restrictions
beta = []


def getVariables():
    return variables

def getBaseVariables():
    return baseVariables

def getRestrictions():
    return restrictions

# Retorna a iteração atual
def getCurrIteration():
    return currIteration

def getBeta():
    return beta

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
    for variable in range(0, len(restList) + len(funcObj)):
        # Cria o nome da variável
        variableName = "x{0}".format(variable + 1)
        variables.append(variableName)
        # Verifica se a variável está na função objetivo
        if variable >= len(funcObj):
            funcObj.append(0)
            excessVariables.append(variable)
            baseVariables.append(variable)
    # Atribui que a quantidade de restrição é igual a quantidade de variáveis de excesso. Exemplo: 2 restrições, 2 variáveis de excesso
    excessVariablesQtd = len(restList)
    # Laço condicional responsável em criar as restrições com preenchimento de 0 e 1 conforme matriz identidade
    for key in restList:
        # Armazena o valor da restrição
        value = restList[key]
        # Atribui a quantidade de variáveis de excesso que faltam para as variáveis faltantes
        variablesMissing = excessVariablesQtd
        # Inicializa a variável de comparação identidade
        identity = 1
        # Enquanto houver variáveis de excesso faltando:
        while variablesMissing > 0:
            # Se a variável de excesso for igual a variável de comparação identidade, adiciona 1, senão 0
            if key == identity:
                value.append(1)
            else:
                value.append(0)
            # Decrementa a quantidade de variáveis de excesso faltando
            variablesMissing -= 1
            # Aumenta o valor da variável de comparação identidade
            identity += 1
        restrictions[key] = value
    # Atribui a função objetivo na lista de cj
    cj = funcObj
    # Atribui as desigualdades na lista de beta
    beta = inequalities
    print(f"\nVariaveis do problema e com preenchimento do excesso: {variables}")
    print(f"Função objetivo: {funcObj}")
    print(f"Variáveis base: {baseVariables}")
    print(f"Beta: {beta}")
    print(f"Restrições com preenchimento da identidade: {restrictions}\n")
    # TODO: Remover
    # nextIteration()

# Verifica se as variáveis base tem valor de Cj-Zj igual a zero
def verifyZeroInBaseVariables(cjZj):
    result = True
    for i in range(len(cjZj)):
        if i in baseVariables and cjZj[i] != 0 and not result:
            result = False
    return result
            

# Verifica coluna Pivô
def __evaluatePivotColumn(cjZj):
    higherValueIndex = -1
    # Verifica se as variáveis base tem valor de Cj-Zj igual a zero
    if verifyZeroInBaseVariables(cjZj):
        for i in range(len(cjZj)):
            # Verifica se o valor do índice ainda não foi atribuido
            # ou se o valor presente em Cj-Zj é maior que o valor de retorno
            if cjZj[i] > 0 and (higherValueIndex < 0 or cjZj[i] > cjZj[higherValueIndex]):
                higherValueIndex = i
    return higherValueIndex

# Verifica a linha pivô
def __evaluatePivotRow(theta):
    minorValueIndex = -1
    for i in range(len(theta)):
        # Verifica se o valor do índice ainda não foi atribuido
        # ou se o valor presente na coluna Theta é menor que o anterior
        if minorValueIndex < 0 or theta[i] < theta[minorValueIndex]:
            minorValueIndex = i
    return minorValueIndex

# Subtrai o Cj do Zj
def __subtract(cj, zj):
    result = []
    for index in range(len(cj)):
        result.append(cj[index] - zj[index])
    return result

# Divide o beta pelo valor da restrição em determinada posição
def __divide(beta, position):
    result = []
    functionNmbr = 1
    # Laço de repetição para cada elemento em 'beta'
    for value in beta:
        # Adiciona o conteúdo da iteração divididos pelo valor da restrição na determinada posição
        if restrictions[functionNmbr][position] == 0:
            # Quando é a coluna Pivo, e vai dividir Theta por 0, o valor é infinito
            result.append(math.inf)
        else:
            result.append(round(value / restrictions[functionNmbr][position], 2))
        # Incrementa a variável para ir para o valor da próxima restrição
        functionNmbr += 1
    return result

# Realiza a próxima iteração
def nextIteration():
    zj = []
    # Laço de repetição para todas as variáveis
    for value in range(len(variables)):
        sumZj = 0
        functionNmbr = 1
        # Laço para multiplicar o valor da variável base para cada respectivo elemento na coluna e somar o resultado
        for index in baseVariables:
            print("Índice da Variável Base: {0}, RestVal: {1}, Variável: {2}".format(funcObj[index], restrictions[functionNmbr][value], variables[value]))
            sumZj += funcObj[index] * restrictions[functionNmbr][value]
            functionNmbr += 1
        print()
        zj.append(sumZj)
    # print(f"Zj's da iteração {getCurrIteration()}: {zj}")
    cjZj = __subtract(cj, zj)
    # print(f"Cj-Zj da iteração {getCurrIteration()}: {cjZj}")
    pivotColumnIndex = __evaluatePivotColumn(cjZj)
    # print(f"> Coluna Pivô - índice [{pivotColumnIndex}] com valor [{cjZj[pivotColumnIndex]}]")
    theta = []
    pivotRowIndex = -1
    # Verifica se encontrou coluna pivô, indicando que existe valor positivo em Cj-Zj
    if pivotColumnIndex >= 0:
        theta = __divide(beta, pivotColumnIndex)
        # print(f"Theta: {theta}")
        pivotRowIndex = __evaluatePivotRow(theta)
        # print(f"> Linha Pivô - índice [{pivotRowIndex}] com valor [{theta[pivotRowIndex]}]")
        pivotElement = restrictions[pivotRowIndex + 1][pivotColumnIndex]
        # print(f"Elemento Pivô com valor {pivotElement}")
        # print(f"Iteração atual: {getCurrIteration()}")
        # TODO: arrumar as equações para a próxima iteração
        __incrementIteration()
    else:
        # TODO: Calcula zj para coluna beta
        pass
    return zj, cjZj, pivotColumnIndex, theta, pivotRowIndex
