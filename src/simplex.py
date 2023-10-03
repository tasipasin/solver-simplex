# Inicializa a variável que contém a iteração atual
currIteration = 0
# Lista de identificação das variáveis pela posição na lista
variables = []
# Índices da lista 'variables' que são as variáveis de excesso
excessVariables = []
# Contém o ÍNDICE das variáveis que são base relativos à lista 'variables'
baseVariables = []

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
def initial(funcObj, restrictions, inequalities):
    global cj
    global beta

    # cada restrição tem uma variável a mais
    for variable in range(0, len(restrictions)* 2):
        # Cria o nome da variável
        variableName = "x{0}".format(variable + 1)
        variables.append(variableName)
        # Verifica se a variável está na função objetivo
        if variable >= len(restrictions):
            funcObj.append(0)
            excessVariables.append(variable)
            baseVariables.append(variable)

    # Atribui que a quantidade de restrição é igual a quantidade de variáveis de excesso. Exemplo: 2 restrições, 2 variáveis de excesso
    excessVariablesQtd = len(restrictions)
    # Laço condicional responsável em criar as restrições com preenchimento de 0 e 1 conforme matriz identidade
    for key in restrictions:
        # Armazena o valor da restrição
        value = restrictions[key]
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
    # Atribui a função objetivo na lista de cj
    cj = funcObj
    # Atribui as desigualdades na lista de beta
    beta = inequalities
    print(f"\nVariaveis do problema e com preenchimento do excesso: {variables}")
    print(f"Função objetivo: {funcObj}")
    print(f"Variáveis base: {baseVariables}")
    print(f"Restrições com preenchimento da identidade: {restrictions}\n")


# Calcula o valor de Zj
def __evaluateZj():
    pass

# Calcula o valor de Cj - Zj
def __evaluateCjZj():
    pass

# Realiza a próxima iteração
def nextIteration():
    pass

##################################### Teste
initial([2,3], {1:[8,7], 2:[5,4]}, [42,44])
