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
        messagebox.showinfo(title='Autorzy', message='Created by \n\n 1. Arkadiusz Kontek \n 2. Dawid Bogon \n 3. Konrad Kropornicki \n 4. Michał Święciło')
        root.quit()

    def add():
        # Create a database or connect to one
        data = sqlite3.connect(f'{path}')

        # Create cursor
        cursor = data.cursor()

        # Create table
        systolic_arterial_pressure = int(measure1_entry.get())
        diastolic_blood_pressure = int(measure2_entry.get())
        current_date = datetime.now()
        formatted_date = current_date.strftime('%d.%m.%Y')

        if systolic_arterial_pressure < 120 and diastolic_blood_pressure < 80:
            messagebox.showinfo(title='Powiadominenie o normie', message='Twoje ciśnienie jest optymalne')
        elif 120 <= systolic_arterial_pressure <= 129 and 80 <= diastolic_blood_pressure <= 84:
            messagebox.showinfo(title='Powiadominenie o normie', message='Twoje ciśnienie jest prawidłowe')
        elif 130 <= systolic_arterial_pressure <= 139 and 85 <= diastolic_blood_pressure <= 89:
            messagebox.showinfo(title='Powiadominenie o normie', message='Twoje ciśnienie jest prawidłowe wysokie')
        elif 140 <= systolic_arterial_pressure <= 159 and 90 <= diastolic_blood_pressure <= 99:
            messagebox.showwarning(title='Powiadominenie o normie', message='Masz łagodne nadciśnienie')
        elif 160 <= systolic_arterial_pressure <= 179 and 100 <= diastolic_blood_pressure <= 109:
            messagebox.showwarning(title='Powiadominenie o normie', message='Masz umiarkowane nadciśnienie')
        elif systolic_arterial_pressure >= 180 and diastolic_blood_pressure >= 110:
            messagebox.showwarning(title='Powiadominenie o normie', message='Masz ciężkie nadciśnienie')
        else:
            messagebox.showerror(title='Powiadominenie o normie', message='Ciężko określić')

        cursor.execute("INSERT INTO addresses VALUES (:systolic_arterial_pressure, :diastolic_blood_pressure, :formatted_date)",
                       {
                           'systolic_arterial_pressure': systolic_arterial_pressure,
                           'diastolic_blood_pressure': diastolic_blood_pressure,
                           'formatted_date': formatted_date
                       })

        # Commit Changes
        data.commit()

        # Close Connection
        data.close()

        measure1_entry.delete(0, END)
        measure2_entry.delete(0, END)

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
