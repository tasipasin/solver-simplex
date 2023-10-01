# Requisitos do programa:
# 1. Implementar a maximização.
# 2. Possuir uma interface com o usuário.
# 3. Informar o número de iterações.
# 4. Identificar o "Z" ou "C" ótimo e valores das variáveis básicas.
# 5. Apontar problemas de degeneração.
# 6. Indicar se o problema é inviável.
# 7. Indicar se o problema é sem fronteira.

import tkinter as tk


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


# Função para criar a janela principal do tkinter
def createMainWindow():
    window = tk.Tk()
    window.title("Linear Programming Problem Resolution")
    window.geometry("700x400")
    return window


# Função para criar labels de texto
def createLabel(window, text, row, column):
    label = tk.Label(window, text = text)
    label.grid(row = row, column = column, sticky = "n")


# Função para criar entradas de texto
def createEntry(window, textvariable, width, row, column):
    entry = tk.Entry(window, textvariable = textvariable, width = width)
    entry.grid(row = row, column = column)


# Função para criar botões
def createButton(window, text, command, row, column):
    button = tk.Button(window, text = text, command = command)
    button.grid(row = row, column = column)


# Função para limpar a tela removendo todos os widgets
def clearScreen(window):
    for widget in window.winfo_children():
        widget.destroy()


# Função para criar labels da função objetivo
def createObjectiveFunctionLabels(window, numVariables):
    createLabel(window, "Função Objetivo:", 0, 0)
    column = 1
    objectiveVariablesValue = []
    
    for i in range(1, numVariables + 1):
        createLabel(window, f"X{i}:", 0, column)
        column += 1
        createEntry(window, tk.StringVar(), 10, 0, column)
        column += 1
        if i < numVariables:
            createLabel(window, "+", 0, column)
            column += 1
        objectiveVariablesValue.append(tk.StringVar())
    return objectiveVariablesValue


# Função para criar labels das restrições
def createRestrictionsLabels(window, numVariables, numRestrictions):
    createLabel(window, "", 2, 0)
    createLabel(window, "Restrições:", 3, 0)
    column = 1
    restrictionsVariablesValue = []

    for i in range((1+2), (numRestrictions+2) + 1):
        for j in range(1, numVariables + 1):
            createLabel(window, f"X{j}:", i, column)
            column += 1
            createEntry(window, tk.StringVar(), 10, i, column)
            column += 1
            if j < numVariables:
                createLabel(window, "+", i, column)
                column += 1
        createLabel(window, "<=", i, column)
        column += 1
        createEntry(window, tk.StringVar(), 10, i, column)
        column += 1
        restrictionsVariablesValue.append(tk.StringVar())
        column = 1
    return restrictionsVariablesValue


# Função para tratar a confirmação dos valores de variáveis e restrições
def confirmProblemValues(window, numberVariablesVar, numberRestrictionsVar):
    numVariables = int(numberVariablesVar.get())
    numRestrictions = int(numberRestrictionsVar.get())
    clearScreen(window)

    objectiveVariablesValue = createObjectiveFunctionLabels(window, numVariables)
    restrictionsVariablesValue = createRestrictionsLabels(window, numVariables, numRestrictions)


def main():
    window = createMainWindow()

    numberVariablesVar = tk.StringVar()
    numberVariablesLabel = createLabel(window, "Número de Variáveis:", 0, 0)
    entryNumberVariables = createEntry(window, numberVariablesVar, 10, 0, 1)

    numberRestrictionsVar = tk.StringVar()
    restrictionsLabel = createLabel(window, "Número de Restrições:", 1, 0)
    entryRestrictions = createEntry(window, numberRestrictionsVar, 10, 1, 1)

    confirmButton = createButton(window, "Confirmar valores", lambda: confirmProblemValues(window, numberVariablesVar, numberRestrictionsVar), 2, 0)

    # checkIfIsMaximization()
    # checkIfIsDegenerate()
    # checkIfIsImpracticable()
    # checkIfIsUnbounded()

    window.mainloop()

if __name__ == "__main__":
    main()
