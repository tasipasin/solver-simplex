# Requisitos do programa:
# 1. Implementar a maximização. (Feito)
# 2. Possuir uma interface com o usuário. (Feito)
# 3. Informar o número de iterações. (Feito)
# 4. Identificar o "Z" ou "C" ótimo e valores das variáveis básicas. (Feito)
# 5. Apontar problemas de degeneração. (Feito)
# 6. Indicar se o problema é inviável - Trocando inicialmente por Ótimos alternados.
# 7. Indicar se o problema é sem fronteira. (Feito)

import math
import simplex
import simplexScreen

# Lista para armazenar os valores da função objetivo 
objectiveVariables = []
# Mapa para armazenar os valores das restrições
restrictionsVariables = {}

# Número de variáveis para o problema
variablesQtdField = simplexScreen.createTextVar()
# Número de restrições para o problema
restrictionQtdField = simplexScreen.createTextVar()

# Verifica condições de parada normal
def checkStopCondition(cjZj, baseVariables):
    stop = True
    index = 0
    while index < len(cjZj) and stop:
        stop = (index in baseVariables and cjZj[index] == 0) or (index not in baseVariables and cjZj[index] < 0)
        index += 1
    return stop

# Verifica se o problema é degenerado
def checkIfIsDegenerate(theta, pivotRowIndex):
    # Quando os valores de theta são iguais, o problema é degenerado
    return theta.count(theta[pivotRowIndex]) > 1

# Verifica se o problema é impraticável (inviável)
def checkIfIsImpracticable():
    pass

# Verifica se o problema é sem fronteira
def checkIfIsUnbounded(theta):
    # Quando não é identificado qual variável que entra, mas não sabe qual sai, o problema é sem fronteira
    # Isso significa que theta apresenta valores negativos E infinitos, e não há outra possibilidade de escolha
    unbounded = True
    for i in range(len(theta)):
        if theta[i] == math.inf:
            theta[i] = -math.inf
        if theta[i] > 0:
            unbounded = False
    return unbounded

# Verifica se o problema é ótimos alternados
def checkIfIsAlternatedOptimum():
    # Quando em Cj-Zj há algum valor "0" sendo que essa respectiva variável não é base, o problema é ótimos alternados
    pass

# Retorna a lista de variáveis do mapa de restrições
def getRestrictionVariables():
    global restrictionsVariables
    return restrictionsVariables

# Retorna o resultado de uma fração como float, permitindo entrada de frações na interface
def getFractionAsFloat(value):
    result = 0
    if "/" in value:
        splitted = value.split("/")
        firstValue = float(splitted[0])
        secondValue = float(splitted[1]) if splitted[1].strip() else 1
        result = firstValue / secondValue
    else:
        result = float(value)
    return result

# Botão para confirmar os valores de variáveis e restrições
def confirmProblemValues():
    # Obtém os valores da quantidade de "variáveis" e "restrições" como um inteiro
    numVariables = int(variablesQtdField.get())
    numRestrictions = int(restrictionQtdField.get())
    simplexScreen.clearScreen()

    # Define os valores para a função objetivo e restrições
    createObjectiveFunctionLabels(numVariables)
    createRestrictionsLabels(numVariables, numRestrictions)

    # Cria botão para confirmar os valores (valores da função objetivo e restrições)
    simplexScreen.createLabel("", (numRestrictions + 3), 0)
    simplexScreen.createButton("Confirmar valores", initResolution, (numRestrictions + 4), 0)

# Cria os textos e as entradas para a função objetivo
def createObjectiveFunctionLabels(numVariables):
    global objectiveVariablesValue
    objectiveVariablesValue = []
    simplexScreen.createLabel("Função Objetivo:", 0, 0)
    column = 1
    # Cria laço condicional para o valor das variáveis da função objetivo. A cada iteração do laço, cria-se uma nova variável (coluna)
    for variable in range(1, numVariables + 1):
        field = simplexScreen.createTextVar()
        # Cria campo para a variável
        simplexScreen.createDefaultEntry(field, 0, column)
        column += 1
        # Cria label da variável
        simplexScreen.createLabel(f"x{variable}", 0, column)
        column += 1
        # Verifica se não é última variável
        if variable < numVariables:
            simplexScreen.createLabel("+", 0, column)
            column += 1
        # Adiciona variável na lista de variáveis da função objetivo
        objectiveVariablesValue.append(field)
    return objectiveVariablesValue

# Função para criar labels das restrições
def createRestrictionsLabels(totalVariables, totalRestrictions):
    global restrictionsVariables
    restrictionsVariables = {}
    simplexScreen.createLabel("", 2, 0)
    simplexScreen.createLabel("Restrições:", 3, 0)
    column = 1
    # Cria laço condicional para as restricoes. A cada iteração do laço, cria-se uma nova restrição
    for row in range((1+2), (totalRestrictions+2) + 1):
        rowVariableList = []
        # Cria laço condicional para as variáveis. A cada iteração do laço, cria-se uma nova variável (coluna)
        for variable in range(1, totalVariables + 1):
            column += createVariable(row, column, variable >= totalVariables, rowVariableList)
        # Após laço das variáveis, cria-se a label de <= e o campo de valor
        simplexScreen.createLabel("<=", row, column)
        column += 1
        var = simplexScreen.createTextVar()
        simplexScreen.createDefaultEntry(var, row, column)
        column += 1
        rowVariableList.append(var)
        # Cria uma sublista para cada restrição (linha)
        restrictionsVariables[row - 2] = rowVariableList
        # Reseta a coluna para a próxima restrição (linha)
        column = 1

# Cria a tabela de variáveis para as restrições
def createVariable(row, column, isBeta, varList):
    # Identifica qual a variável sendo incluída na tabela
    variable = math.ceil(column / 3)
    # Cria cópia do valor da coluna
    thisColumn = column
    # Inicializa e cria campo para a variável
    var = simplexScreen.createTextVar()
    simplexScreen.createDefaultEntry(var, row, thisColumn)
    thisColumn += 1
    # Cria label da variável
    simplexScreen.createLabel(f"x{variable}", row, thisColumn)
    thisColumn += 1
    # Verifica se não é coluna beta
    if not isBeta:
        # Adiciona soma
        simplexScreen.createLabel("+", row, thisColumn)
        thisColumn += 1
    # Adiciona variável na lista de variáveis
    varList.append(var)
    return thisColumn - column

# Inicializa a resolução com os dados inseridos
def initResolution():
    global restrictionsVariables
    global objectiveVariablesValue
    try:
        # Lista para armazenar os valores das desigualdades
        inequalities = []

        # Recupera os valores dos campos
        for key in restrictionsVariables:
            toGet = restrictionsVariables[key]
            asNumber = []
            for item in toGet[:-1]:
                asNumber.append(getFractionAsFloat(item.get()))
            # Adiciona o valor da variável na lista
            restrictionsVariables[key] = asNumber
            # Adiciona o valor da desigualdade na lista
            inequalities.append(getFractionAsFloat(toGet[-1].get()))
        
        # Recupera os valores dos campos
        asNumber = []
        for value in objectiveVariablesValue:
            asNumber.append(getFractionAsFloat(value.get()))
        # Adiciona o valor da variável na lista
        objectiveVariablesValue = asNumber
        simplex.initial(objectiveVariablesValue, restrictionsVariables, inequalities)
        # Monta a tabela do simplex
        createSimplexTable()

    except ValueError:
        simplexScreen.showerror("Erro", "Valores inválidos")

# Função para criar a tabela Simplex
def createSimplexTable():
    # Limpa a tela
    simplexScreen.clearScreen()

    restrictionsVariables = simplex.getRestrictions()
    # Monta a tabela inicial do simplex
    linha = 0
    coluna = 0
    simplexScreen.createLabel("", linha, coluna)
    linha += 1
    simplexScreen.createLabel("", linha, coluna)
    linha += 1
    simplexScreen.createLabel(f"Iteração {simplex.getCurrIteration()}", linha, coluna)
    coluna += 1
    simplexScreen.createLabel("", linha, coluna)
    coluna += 1
    simplexScreen.createLabel("|", linha, coluna)
    coluna += 1
    # Adiciona as informações das variáveis do problema
    for i in range(len(simplex.getVariables())):
        simplexScreen.createLabel(f"x{i + 1}", linha, coluna)
        coluna += 1
    simplexScreen.createLabel("|", linha, coluna)
    coluna += 1
    # Adiciona coluna do elemento beta
    simplexScreen.createLabel("beta", linha, coluna)
    coluna += 1
    simplexScreen.createLabel("|", linha, coluna)
    # Adiciona coluna do elemento theta
    coluna += 1
    simplexScreen.createLabel("theta", linha, coluna)

    linha += 1
    coluna = 1
    # Adiciona a informação das variáveis base
    for value in simplex.getBaseVariables():
        simplexScreen.createLabel(simplex.getVariables()[value], linha, coluna)
        linha += 1
    simplexScreen.createLabel("---", linha, coluna)
    linha += 1
    simplexScreen.createLabel("Zj", linha, coluna)
    linha += 1
    simplexScreen.createLabel("Cj-Zj", linha, coluna)
    linha += 1
    simplexScreen.createLabel("---", linha, coluna)
    
    linhaInsert = 3
    # Adiciona os valores das restrições
    for key in simplex.getRestrictions():
        coluna = 3
        listOfValues = restrictionsVariables[key]
        for item in listOfValues:
            simplexScreen.createLabel(str(round(item, 2)), linhaInsert, coluna)
            coluna += 1
        # Coluna da barrinha
        simplexScreen.createLabel("|", linhaInsert, coluna)
        # Insere o valor de Beta da equação
        coluna += 1
        simplexScreen.createLabel(round(simplex.getBeta()[key - 1], 2), linhaInsert, coluna)
        coluna += 1
        simplexScreen.createLabel("|", linhaInsert, coluna)
        linhaInsert += 1

    simplexScreen.createButton("Calcular Pivô", lambda: evaluatePivotElement(linha), linha + 1, 0)

# Função para realizar o cálculo do elemento pivô
def evaluatePivotElement(linha):
    # Remove o botão de calcular elemento pivô
    simplexScreen.destroyElement(linha + 1, 0)
    # Realiza cálculos da iteração
    zj, cjZj, pivotColumnIndex, theta, pivotRowIndex = simplex.executeIteration()
    # Indica onde inicia o espaço de Zj
    linha = linha - 2
    coluna = 3
    for i in range(len(zj)):
        simplexScreen.createLabel(str(round(zj[i], 2)), linha, coluna)
        coluna += 1
    simplexScreen.createLabel("|", linha, coluna)
    # Indica onde inicia o espaço do Cj-Zj
    linha += 1
    coluna = 3
    for i in range(len(cjZj)):
        simplexScreen.createLabel(str(round(cjZj[i], 2)), linha, coluna)
        coluna += 1
    simplexScreen.createLabel("|", linha, coluna)
    # Insere os valores da coluna de Theta
    linha = 3
    coluna = 3 + len(simplex.getVariables()) + 3
    for i in range(len(theta)):
        simplexScreen.createLabel(str(round(theta[i], 2)), linha, coluna)
        linha += 1
    
    # Verifica sistema degenerado
    if pivotRowIndex >= 0 and checkIfIsDegenerate(theta, pivotRowIndex):
        simplexScreen.createLabelWithColor("Sistema Degenerado", linha + len(simplex.getBaseVariables()) + 4, 0, "goldenrod")
        linha += 1
    # Verifica sistema sem fronteira
    if pivotRowIndex >= 0 and checkIfIsUnbounded(theta):
        simplexScreen.createLabelWithColor("Sistema Sem Fronteira", linha + len(simplex.getBaseVariables()) + 4, 0, "goldenrod")
        linha += 1
    # Só consegue continuar a execução (próxima iteração) se não for um problema sem fronteira
    if not checkStopCondition(cjZj, simplex.getBaseVariables()) and not checkIfIsUnbounded(theta):
        # Altera as cores da coluna, linha e elementos pivô da iteração
        simplexScreen.changeTextColor(5 + len(simplex.getBaseVariables()), 3 + pivotColumnIndex, "red")
        simplexScreen.changeTextColor(3 + pivotRowIndex, 3 + len(simplex.getVariables()) + 3, "red")
        simplexScreen.changeTextColor(pivotRowIndex + 3, pivotColumnIndex + 3, "red")

        simplex.performPivoting(pivotRowIndex, pivotColumnIndex)
        # Insere botão para realizar pivoteamento e iniciar a próxima iteração
        simplexScreen.createButton("Próxima Iteração", nextIteration, linha + 4, 0)
    else:
        # Encerra processo
        zFinal = round(simplex.calculateZFinal(), 2)
        # Insere o Z final na tabela simplex
        simplexScreen.createLabel(zFinal, 3 + len(simplex.getBeta()) + 1, 3 + len(simplex.getVariables()) + 1)
        simplexScreen.createLabel("", linha + len(simplex.getBaseVariables()) + 4, 0)
        column = 1
        simplexScreen.createLabelWithColor(f"Z final: {zFinal}", linha + len(simplex.getBaseVariables()) + 5, column, "green")
        column += 1
        # TODO - Colocar os Beta em verde também
        # for index in range(len(simplex.getBeta())):
            # if simplex.getBaseVariables()[index] is not simplex.getExcessVariables():
            # simplexScreen.createLabelWithColor(f"{simplex.getVariables()[index]}: {simplex.getBeta()[index]}", linha + len(simplex.getBaseVariables()) + 5, column, "green")

# Função para realizar a próxima iteração
def nextIteration():
    # Monta a tabela do simplex
    createSimplexTable()

def main():
    # Campo de Quantidade de Variáveis
    simplexScreen.createLabel("Número de Variáveis:", 0, 0)
    simplexScreen.createDefaultEntry(variablesQtdField, 0, 1)

    # Campo de Quantidade de Restrições
    simplexScreen.createLabel("Número de Restrições:", 1, 0)
    simplexScreen.createDefaultEntry(restrictionQtdField, 1, 1)

    # Cria botão para confirmar os valores do problema (quantidade de variáveis e restrições)
    simplexScreen.createLabel("", 2, 0)
    simplexScreen.createButton("Confirmar valores para o problema", confirmProblemValues, 3, 0)

    # Mantém a janela principal aberta até que o usuário feche
    simplexScreen.getWindow().mainloop()

if __name__ == "__main__":
    main()
