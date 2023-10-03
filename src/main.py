# Requisitos do programa:
# 1. Implementar a maximização.
# 2. Possuir uma interface com o usuário.
# 3. Informar o número de iterações.
# 4. Identificar o "Z" ou "C" ótimo e valores das variáveis básicas.
# 5. Apontar problemas de degeneração.
# 6. Indicar se o problema é inviável.
# 7. Indicar se o problema é sem fronteira.

import tkinter as tk
from tkinter import messagebox
import math

# Função para criar a janela principal do tkinter
def createMainWindow():
    window = tk.Tk()
    window.title("Linear Programming Problem Resolution")
    window.geometry("600x400")
    return window

window = createMainWindow()

objectiveVariables = []
restrictionsVariables = []
# Número de variáveis para o problema
variablesQtdField = tk.StringVar()
# Número de restrições para o problema
restrictionQtdField = tk.StringVar()

# Função para verificar se o problema é de maximização
def checkIfIsMaximization():
    pass

# Função para verificar se o problema é degenerado
def checkIfIsDegenerate():
    pass

# Função para verificar se o problema é impraticável (inviável)
def checkIfIsImpracticable():
    pass

# Função para verificar se o problema é sem fronteira
def checkIfIsUnbounded():
    pass

# Função para retornar a janela principal
def getWindow():
    global window
    return window

# Função para criar labels de texto
def createLabel(text, row, column):
    label = tk.Label(getWindow(), text = text)
    label.grid(row = row, column = column, sticky = "n")

# Função para criar entradas de texto
def createDefaultEntry(textvariable, row, column):
    createEntry(textvariable, 6, row, column)

# Função para criar entradas de texto
def createEntry(textvariable, width, row, column):
    entry = tk.Entry(getWindow(), textvariable = textvariable, width = width)
    entry.grid(row = row, column = column)

# Função para criar botões
def createButton(text, command, row, column):
    button = tk.Button(getWindow(), text = text, command = command)
    button.grid(row = row, column = column)

# Função para limpar a tela removendo todos os widgets
def clearScreen():
    for widget in getWindow().winfo_children():
        widget.destroy()

# Função para criar labels da função objetivo
def createObjectiveFunctionLabels(numVariables):
    createLabel("Função Objetivo:", 0, 0)
    column = 1
    objectiveVariablesValue = []
    # Adiciona os campos de variável
    for variable in range(1, numVariables + 1):
        createDefaultEntry(tk.StringVar(), 0, column)
        column += 1
        createLabel(f"x{variable}", 0, column)
        column += 1
        if variable < numVariables:
            createLabel("+", 0, column)
            column += 1
        objectiveVariablesValue.append(tk.StringVar())
    return objectiveVariablesValue


def createVariable(row, column, isBeta, varList):
    variable = math.ceil(column / 3)
    thisColumn = column
    var = tk.StringVar()
    createDefaultEntry(var, row, thisColumn)
    thisColumn += 1
    createLabel(f"x{variable}", row, thisColumn)
    thisColumn += 1
    if not isBeta:
        createLabel("+", row, thisColumn)
        thisColumn += 1
    varList.append(var)
    return thisColumn - column


# Função para criar labels das restrições
def createRestrictionsLabels(totalVariables, totalRestrictions):
    createLabel("", 2, 0)
    createLabel("Restrições:", 3, 0)
    column = 1
    restrictionsVariablesValue = {}

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
        restrictionsVariablesValue[row] = rowVariableList
        # Reseta a coluna para a próxima restrição (linha)
        column = 1
    return restrictionsVariablesValue

def initResolution():
    global restrictionsVariables
    try:
        for key in restrictionsVariables:
            toGet = restrictionsVariables[key]
            asNumber = []
            for item in toGet:
                asNumber.append(int(item.get()))
            restrictionsVariables[key] = asNumber
            print(asNumber)
            ## A PARTIR DAQUI DA PRA FAZER OS CALCULOS!
        # messagebox.showinfo("Valores", f"Função Objetivo: {objectiveVariables}\nRestrições: {restrictionsVariables}")
    except ValueError:
        messagebox.showerror("Erro", "Valores inválidos")


# Botão para confirmar os valores de variáveis e restrições
def confirmProblemValuesCallback():
    numVariables = int(variablesQtdField.get())
    numRestrictions = int(restrictionQtdField.get())
    clearScreen()

    global objectiveVariables
    global restrictionsVariables
    # Define os valores para a função objetivo e restrições
    objectiveVariables = createObjectiveFunctionLabels(numVariables)
    restrictionsVariables = createRestrictionsLabels(numVariables, numRestrictions)
    
    createButton("Confirmar valores", initResolution, (numRestrictions + 3), 0)


def main():
    # Campo de Quantidade de Variáveis
    createLabel("Número de Variáveis:", 0, 0)
    createDefaultEntry(variablesQtdField, 0, 1)

    # Campo de Quantidade de Restrições
    createLabel("Número de Restrições:", 1, 0)
    createDefaultEntry(restrictionQtdField, 1, 1)

    # Botão para confirmar os valores de variáveis e restrições
    createLabel("", 2, 0)
    createButton("Confirmar valores para o problema", confirmProblemValuesCallback, 3, 0)

    # checkIfIsMaximization()
    # checkIfIsDegenerate()
    # checkIfIsImpracticable()
    # checkIfIsUnbounded()

    getWindow().mainloop()


if __name__ == "__main__":
    main()
