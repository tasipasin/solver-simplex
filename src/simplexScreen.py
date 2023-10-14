import tkinter as tk
from tkinter import messagebox

# Função para criar a janela principal do tkinter
def createMainWindow():
    window = tk.Tk()
    window.title("Linear Programming Problem Resolution")
    window.geometry("600x400")
    return window

# Cria a janela principal do tkinter
window = createMainWindow()

# Retorna a janela principal
def getWindow():
    global window
    return window

# Cria labels de texto
def createLabel(text, row, column):
    createLabelWithColor(text, row, column, "black")

# Cria labels de texto com cor
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
        
# Altera a cor do texto na linha x coluna
def changeTextColor(row, column, newColor):
    window.grid_slaves(row, column)[0].config(fg=newColor)
    
# Destroi o elemento na linha x coluna
def destroyElement(row, column):
    window.grid_slaves(row, column)[0].destroy()
    
# Mostra mensagem de erro
def showError(title, message):
    messagebox.showerror(title, message)

# Retorna uma variável de texto do tkinter
def createTextVar():
    return tk.StringVar()
