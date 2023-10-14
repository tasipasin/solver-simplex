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

# Retorna a iteração atual
def getCurrIteration():
    return currIteration

# Retorna a lista de variáveis
def getVariables():
    return variables

# Retorna a lista de variáveis de excesso
def getExcessVariables():
    return excessVariables

# Retorna a lista de variáveis base
def getBaseVariables():
    return baseVariables

# Retorna o mapa de restrições
def getRestrictions():
    return restrictions

# Retorna a lista de valores do beta 
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
        thetaValue = theta[i]
        # Verifica se o valor do índice ainda não foi atribuido
        # ou se o valor presente na coluna Theta é menor que o anterior
        if thetaValue > 0 and (minorValueIndex < 0 or thetaValue < theta[minorValueIndex]):
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

# Realiza os cálculos da iteração e verifica se é necessário mais uma iteração
def executeIteration():
    zj = []
    # Laço de repetição para todas as variáveis
    for value in range(len(variables)):
        sumZj = 0
        functionNmbr = 1
        # Laço para multiplicar o valor da variável base para cada respectivo elemento na coluna e somar o resultado
        # Calculo do Zj
        for index in baseVariables:
            sumZj += funcObj[index] * restrictions[functionNmbr][value]
            functionNmbr += 1
        zj.append(sumZj)
    # Calcula Cj-Zj
    cjZj = __subtract(cj, zj)
    # Verifica a coluna pivô
    pivotColumnIndex = __evaluatePivotColumn(cjZj)
    # Realiza cálculo da coluna theta
    theta = []
    pivotRowIndex = -1
    # Verifica se encontrou coluna pivô, indicando que existe valor positivo em Cj-Zj
    if pivotColumnIndex >= 0:
        theta = __divide(beta, pivotColumnIndex)
        # Valida linha pivô
        pivotRowIndex = __evaluatePivotRow(theta)
    return zj, cjZj, pivotColumnIndex, theta, pivotRowIndex

# Função para realizar o pivoteamento
def performPivoting(pivotRowIndex, pivotColumnIndex):
    global restrictions
    restTemp = restrictions
    # Incrementa a iteração
    __incrementIteration()
    global beta
    # Recupera o elemento pivô
    pivotElement = restTemp[pivotRowIndex + 1][pivotColumnIndex]
    # Recupera a linha pivô
    pivotRow = [round(element / pivotElement, 2) for element in restTemp[pivotRowIndex + 1]]
    # Atualiza a linha pivô para ter "1" no elemento pivô
    restTemp[pivotRowIndex + 1] = pivotRow
    multiplicationFactor = 1
    beta[pivotRowIndex] = round(beta[pivotRowIndex] / pivotElement, 2)

    for key in restTemp:
        if key != pivotRowIndex + 1:
            # Recupera a linha inteira
            manipRow = restTemp[key]
            # Recupera o valor de multiplicação
            multiplicationFactor = manipRow[pivotColumnIndex]
            # Multiplica cada elemento da linha pelo valor de multiplicação
            pivotRowMultiplied = [round(item * multiplicationFactor, 2) for item in pivotRow]
            # Subtrai a linha "antiga" pelo valor da linha do pivo multiplicada
            manipRow = __subtract(manipRow, pivotRowMultiplied)
            restTemp[key] = manipRow
            
            # Atualiza os valores de Beta
            beta[key - 1] = round(beta[key - 1] - multiplicationFactor * beta[pivotRowIndex], 2)

    # Atualiza a variável base para refletir o pivoteamento
    baseVariables[pivotRowIndex] = pivotColumnIndex
    restrictions = restTemp


def calculateZFinal():
    z = 0
    for index in range(len(baseVariables)):
        z += funcObj[baseVariables[index]] * beta[index]
    return z
