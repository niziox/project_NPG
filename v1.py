#!/usr/bin/python
# -*- coding: utf-8 -*-

from tkinter import *
from tkinter import messagebox
import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


root = Tk()
root.title('Dziennik cisnieniowca')
root.iconbitmap("images/icon.ico")


def second_screen(status):
    # Create a database or connect to one
    if status != 2:
        global path
        path = path_entry.get()
    data = sqlite3.connect(f'{path}')

    # Create cursor
    cursor = data.cursor()

    # Create table
    if status == 1:
        cursor.execute("""CREATE TABLE addresses (
                        systolic_arterial_pressure integer,
                        diastolic_blood_pressure integer,
                        formatted_date text) 
                    """)

    def leaving():
        pass

    def add():
        pass

    def plot():
        pass

    # Third screen
    def results():
        pass

    measure1_label = Label(root, text='Podaj ciśnienie tętnicze skurczowe')
    measure1_label.grid(row=1, column=0, padx=10, pady=10)
    measure1_entry = Entry(root, width=30, borderwidth=5)
    measure1_entry.grid(row=1, column=1, padx=(0, 10))
    measure2_label = Label(root, text='Podaj ciśnienie tętnicze rozkurczowe')
    measure2_label.grid(row=2, column=0, padx=10, pady=10)
    measure2_entry = Entry(root, width=30, borderwidth=5)
    measure2_entry.grid(row=2, column=1, padx=(0, 10))
    add_button = Button(root, text='Dodaj', command=add, width=35)
    add_button.grid(row=3, column=0, columnspan=2, pady=10)
    results_button = Button(root, text='Wyniki', width=35, command=results)
    results_button.grid(row=4, column=0, columnspan=2, pady=(0, 10))
    plot_button = Button(root, text='Wykres', width=35, command=plot)
    plot_button.grid(row=5, column=0, columnspan=2)
    quit_button = Button(root, text='Wyjście', command=leaving)
    quit_button.grid(row=6, column=1, sticky='e', pady=5, padx=5)

    # Commit Changes
    data.commit()

    # Close Connection
    data.close()

    welcome_label.destroy()
    path_entry.destroy()
    load_path_button.destroy()
    new_path_button.destroy()


# first screen
title_label = Label(root, text='Dziennik ciśnieniowca')
title_label.grid(row=0, column=0, columnspan=2, pady=10)
welcome_label = Label(root, text='Podaj śćieżkę pliku')
welcome_label.grid(row=1, column=0, pady=10, padx=10)
path_entry = Entry(root, width=30, borderwidth=5)
path_entry.grid(row=1, column=1,  padx=(0, 10))
path_entry.insert(0, '.db')
load_path_button = Button(root, text='Wczytaj plik', command=lambda: second_screen(0))
load_path_button.grid(row=2, column=0, columnspan=2, pady=10)
new_path_button = Button(root, text='Nowy plik', command=lambda: second_screen(1))
new_path_button.grid(row=3, column=0,  columnspan=2, pady=(0, 10))


root.mainloop()
