# Requisitos do programa:
# 1. Implementar a maximização.
# 2. *Possuir uma interface com o usuário.
# 3. Informar o número de iterações.
# 4. Identificar o "Z" ou "C" ótimo e valores das variáveis básicas.
# 5. Apontar problemas de degeneração.
# 6. Indicar se o problema é inviável.
# 7. Indicar se o problema é sem fronteira.

# Importa a biblioteca tkinter para a criação da interface gráfica
import tkinter as tk
from tkinter import messagebox
import math
import simplex

# Função para criar a janela principal do tkinter
def createMainWindow():
    window = tk.Tk()
    window.title("Linear Programming Problem Resolution")
    window.geometry("600x400")
    return window

# Cria a janela principal do tkinter
window = createMainWindow()

# Lista para armazenar os valores da função objetivo 
objectiveVariables = []
# Mapa para armazenar os valores das restrições
restrictionsVariables = {}

# Número de variáveis para o problema
variablesQtdField = tk.StringVar()
# Número de restrições para o problema
restrictionQtdField = tk.StringVar()

# Verifica se o problema é de maximização
def checkIfIsMaximization():
    pass

# Verifica se o problema é degenerado
def checkIfIsDegenerate():
    pass

# Verifica se o problema é impraticável (inviável)
def checkIfIsImpracticable():
    pass

# Verifica se o problema é sem fronteira
def checkIfIsUnbounded():
    pass

# Retorna a janela principal
def getWindow():
    global window
    return window

def getRestrictionVariables():
    global restrictionsVariables
    return restrictionsVariables

# Cria labels de texto
def createLabel(text, row, column):
    createLabelWithColor(text, row, column, "black")

def createLabelWithColor(text, row, column, color):
    label = tk.Label(getWindow(), text = text, fg=color)
    label.grid(row = row, column = column, sticky = "n", padx=8)

# Cria entradas de texto default (tamanho 6)
def createDefaultEntry(textvariable, row, column):
    createEntry(textvariable, 6, row, column)

# Cria entradas de texto
def createEntry(textvariable, width, row, column):
    entry = tk.Entry(getWindow(), textvariable = textvariable, width = width)
    entry.grid(row = row, column = column)

# Cria botões
def createButton(text, command, row, column):
    button = tk.Button(getWindow(), text = text, command = command)
    button.grid(row = row, column = column)

# Limpa a tela removendo todos os widgets
def clearScreen():
    for widget in getWindow().winfo_children():
        widget.destroy()

# Cria os textos e as entradas para a função objetivo
def createObjectiveFunctionLabels(numVariables):
    # TODO - Tem que aceitar valores com vírgula
    global objectiveVariablesValue
    objectiveVariablesValue = []
    createLabel("Função Objetivo:", 0, 0)
    column = 1
    # Cria laço condicional para o valor das variáveis da função objetivo. A cada iteração do laço, cria-se uma nova variável (coluna)
    for variable in range(1, numVariables + 1):
        field = tk.StringVar()
        # Cria campo para a variável
        createDefaultEntry(field, 0, column)
        column += 1
        # Cria label da variável
        createLabel(f"x{variable}", 0, column)
        column += 1
        # Verifica se não é última variável
        if variable < numVariables:
            createLabel("+", 0, column)
            column += 1
        # Adiciona variável na lista de variáveis da função objetivo
        objectiveVariablesValue.append(field)
    return objectiveVariablesValue

# Cria a tabela de variáveis para as restrições
def createVariable(row, column, isBeta, varList):
    # Identifica qual a variável sendo incluída na tabela
    variable = math.ceil(column / 3)
    # Cria cópia do valor da coluna
    thisColumn = column
    # Inicializa e cria campo para a variável
    var = tk.StringVar()
    createDefaultEntry(var, row, thisColumn)
    thisColumn += 1
    # Cria label da variável
    createLabel(f"x{variable}", row, thisColumn)
    thisColumn += 1
    # Verifica se não é coluna beta
    if not isBeta:
        # Adiciona soma
        createLabel("+", row, thisColumn)
        thisColumn += 1
    # Adiciona variável na lista de variáveis
    varList.append(var)
    return thisColumn - column

# Função para criar labels das restrições
def createRestrictionsLabels(totalVariables, totalRestrictions):
    global restrictionsVariables
    restrictionsVariables = {}
    createLabel("", 2, 0)
    createLabel("Restrições:", 3, 0)
    column = 1
    # Cria laço condicional para as restricoes. A cada iteração do laço, cria-se uma nova restrição
    for row in range((1+2), (totalRestrictions+2) + 1):
        rowVariableList = []
        # Cria laço condicional para as variáveis. A cada iteração do laço, cria-se uma nova variável (coluna)
        for variable in range(1, totalVariables + 1):
            column += createVariable(row, column, variable >= totalVariables, rowVariableList)
        # Após laço das variáveis, cria-se a label de <= e o campo de valor
        createLabel("<=", row, column)
        column += 1
        var = tk.StringVar()
        createDefaultEntry(var, row, column)
        column += 1
        rowVariableList.append(var)
        # Cria uma sublista para cada restrição (linha)
        restrictionsVariables[row - 2] = rowVariableList
        # Reseta a coluna para a próxima restrição (linha)
        column = 1

# Função para criar a tabela Simplex
def createSimplexTable(restrictionsVariables, objectiveVariablesValue):
    # Monta a tabela inicial do simplex
    linha = 0
    coluna = 0
    createLabel("", linha, coluna)
    linha += 1
    createLabel("", linha, coluna)
    linha += 1
    createLabel(f"Iteração {simplex.getCurrIteration()}", linha, coluna)
    coluna += 1
    createLabel("", linha, coluna)
    coluna += 1
    createLabel("|", linha, coluna)
    coluna += 1
    for i in range(len(simplex.getVariables())):
        createLabel(f"x{i + 1}", linha, coluna)
        coluna += 1
    createLabel("|", linha, coluna)
    coluna += 1
    createLabel("beta", linha, coluna)
    coluna += 1
    createLabel("|", linha, coluna)
    coluna += 1
    createLabel("theta", linha, coluna)

    linha += 1
    coluna = 1
    for value in simplex.getBaseVariables():
        createLabel(simplex.getVariables()[value], linha, coluna)
        linha += 1
    createLabel("---", linha, coluna)
    linha += 1
    createLabel("Zj", linha, coluna)
    linha += 1
    createLabel("Cj-Zj", linha, coluna)
    linha += 1
    createLabel("---", linha, coluna)
    
    linhaInsert = 3
    for key in simplex.getRestrictions():
        coluna = 3
        listOfValues = restrictionsVariables[key]
        for item in listOfValues:
            createLabel(str(item), linhaInsert, coluna)
            coluna += 1
        # Coluna da barrinha
        createLabel("|", linhaInsert, coluna)
        # Insere o valor de Beta da equação
        coluna += 1
        createLabel(simplex.getBeta()[key - 1], linhaInsert, coluna)
        coluna += 1
        createLabel("|", linhaInsert, coluna)
        linhaInsert += 1

    createButton("Próxima iteração", lambda: iteration(linha), linha + 1, 0)
    
    # 60 40
    # 2 3 100
    # 4 2 120
    
def iteration(linha):
    zj, cjZj, pivotColumnIndex, theta, pivotRowIndex = simplex.nextIteration()
    print(f"\nZj's da iteração {simplex.getCurrIteration()}: {zj}")
    print(f"Cj-Zj da iteração {simplex.getCurrIteration()}: {cjZj}")
    print(f"> Coluna Pivô - índice [{pivotColumnIndex}] com valor [{cjZj[pivotColumnIndex]}]")
    print(f"Theta: {theta}")
    print(f"> Linha Pivô - índice [{pivotRowIndex}] com valor [{theta[pivotRowIndex]}]")
    print(f"Elemento Pivô: {restrictionsVariables[pivotRowIndex + 1][pivotColumnIndex]}")

    linha = linha - 2
    coluna = 3
    for i in range(len(zj)):
        createLabel(str(zj[i]), linha, coluna)
        coluna += 1
    createLabel("|", linha, coluna)
    linha += 1
    coluna = 3
    for i in range(len(cjZj)):
        createLabel(str(cjZj[i]), linha, coluna)
        coluna += 1
    createLabel("|", linha, coluna)
    linha += 1
    
    linha = 3
    coluna = 3 + len(simplex.getVariables()) + 3
    for i in range(len(theta)):
        createLabel(str(theta[i]), linha, coluna)
        linha += 1

    window.grid_slaves(5 + len(simplex.getBaseVariables()), 3 + pivotColumnIndex)[0].config(fg="red")
    window.grid_slaves(3 + pivotRowIndex, 3 + len(simplex.getVariables()) + 3)[0].config(fg="red")
    window.grid_slaves(pivotRowIndex + 3, pivotColumnIndex + 3)[0].config(fg="red")
    # createLabelWithColor()


# Inicializa a resolução com os dados inseridos
def initResolution():
    global restrictionsVariables
    global objectiveVariablesValue
    try:
        # Lista para armazenar os valores das desigualdades
        inequalities = []

        # Recupera os valores dos campos como inteiro
        for key in restrictionsVariables:
            toGet = restrictionsVariables[key]
            asNumber = []
            for item in toGet[:-1]:
                asNumber.append(int(item.get()))
            # Adiciona o valor da variável na lista
            restrictionsVariables[key] = asNumber
            # Adiciona o valor da desigualdade na lista
            inequalities.append(int(toGet[-1].get()))
        
        # Recupera os valores dos campos como inteiro
        asNumber = []
        for value in objectiveVariablesValue:
            asNumber.append(int(value.get()))
        # Adiciona o valor da variável na lista
        objectiveVariablesValue = asNumber
        simplex.initial(objectiveVariablesValue, restrictionsVariables, inequalities)
        # Limpa a tela
        clearScreen()
        # Monta a tabela do simplex
        createSimplexTable(restrictionsVariables, objectiveVariablesValue)

    except ValueError:
        messagebox.showerror("Erro", "Valores inválidos")


# Botão para confirmar os valores de variáveis e restrições
def confirmProblemValuesCallback():
    # Obtém os valores da quantidade de "variáveis" e "restrições" como um inteiro
    numVariables = int(variablesQtdField.get())
    numRestrictions = int(restrictionQtdField.get())

    # Limpa a tela
    clearScreen()

    # Define os valores para a função objetivo e restrições
    createObjectiveFunctionLabels(numVariables)
    createRestrictionsLabels(numVariables, numRestrictions)

    # Cria botão para confirmar os valores (valores da função objetivo e restrições)
    createLabel("", (numRestrictions + 3), 0)
    createButton("Confirmar valores", initResolution, (numRestrictions + 4), 0)


def main():
    # Campo de Quantidade de Variáveis
    createLabel("Número de Variáveis:", 0, 0)
    createDefaultEntry(variablesQtdField, 0, 1)

    # Campo de Quantidade de Restrições
    createLabel("Número de Restrições:", 1, 0)
    createDefaultEntry(restrictionQtdField, 1, 1)

    # Cria botão para confirmar os valores do problema (quantidade de variáveis e restrições)
    createLabel("", 2, 0)
    createButton("Confirmar valores para o problema", confirmProblemValuesCallback, 3, 0)

    # Mantém a janela principal aberta até que o usuário feche
    getWindow().mainloop()


if __name__ == "__main__":
    main()
