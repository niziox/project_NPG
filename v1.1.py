#!/usr/bin/python
# -*- coding: utf-8 -*-

from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter import simpledialog
import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

root = Tk()
root.title('Dziennik cisnieniowca')
root.iconbitmap("images/icon.ico")
root.geometry('600x550')
root.config(background='#2e2e3d')


def leaving():
    messagebox.showinfo(title='Autorzy',
                        message='Created by \n\n 1. Arkadiusz Kontek \n 2. Dawid Bogon \n 3. Konrad Kropornicki \n 4. Michał Święciło')
    root.quit()


def back(screen):
    pass


def database_screen():
    pass


def help_info():
    help_text = "\n- Pomiar wykonuje się w pozycji siedzącej, w spokoju, po minimum 5-minutowym odpoczynku\n- Przed " \
                "pomiarem przez minimum 30 minut nie należy palić tytoniu, pić kawy i wykonywać ćwiczeń fizycznych\n- "\
                "Przedramię ręki, na której dokonujemy pomiaru, powinno znajdować się na wysokości serca, " \
                "ręka powinna być podparta\n- Badanie należy wykonać na obydwu rękach\n- Należy wykonać 2 pomiary, " \
                "w odstępach około minuty i przyjąć wartość średnią "

    messagebox.showinfo(title="Wskazówka", message=help_text)


def add():
    pass


def add_screen():
    # Destroying redundant widgets
    menu_label.destroy()
    add_label.destroy()
    database_button.destroy()
    new_path_button.destroy()
    quit_button.destroy()

    # Defining new widgets
    global add_welcome_label, measure1_label, measure2_label, measure1_entry, measure2_entry, add_button, help_button, back_from_adding_button

    add_welcome_label = Label(root, text='NOWY WPIS', width=19, height=2, font="Verdana 32", bg='#161618', fg="white",
                              relief="solid")
    add_welcome_label.grid(row=0, column=0, padx=40, pady=15, columnspan=2)
    measure1_label = Label(root, text='Podaj ciśnienie tętnicze skurczowe', bg='#2e2e3d', fg='white')
    measure1_label.grid(row=1, column=0, padx=10, pady=10, sticky=E)
    measure1_entry = Entry(root, width=30, borderwidth=5)
    measure1_entry.grid(row=1, column=1, padx=10, sticky=W)
    measure2_label = Label(root, text='Podaj ciśnienie tętnicze rozkurczowe', bg='#2e2e3d', fg='white')
    measure2_label.grid(row=2, column=0, padx=10, pady=10, sticky=E)
    measure2_entry = Entry(root, width=30, borderwidth=5)
    measure2_entry.grid(row=2, column=1, padx=10, sticky=W)
    add_button = Button(root, text='Dodaj', width=20, height=4, command=add)
    add_button.grid(row=3, column=0, pady=(20, 10), columnspan=2)
    help_button = Button(root, text='JAK WYKONAĆ POMIAR ?', width=20, height=4, command=help_info)
    help_button.grid(row=4, column=0, pady=5, columnspan=2)
    back_from_adding_button = Button(root, text='POWRÓT', width=20, height=4, command=lambda: back('add_screen'))
    back_from_adding_button.grid(row=5, column=0, pady=5, columnspan=2)


def options_screen():
    pass
    

def menu_screen():
    global menu_label, add_label, database_button, new_path_button, quit_button

    menu_label = Label(root, text='MENU GŁÓWNE', width=19, height=2, font="Verdana 32", bg='#161618', fg="white",
                       relief="solid")
    menu_label.grid(row=0, column=0, padx=40, pady=15)
    add_label = Button(root, text='NOWY WPIS', width=20, height=4, command=add_screen)
    add_label.grid(row=1, column=0, pady=5)
    database_button = Button(root, text='BAZA DANYCH', width=20, height=4, command=database_screen)
    database_button.grid(row=2, column=0, pady=5)
    new_path_button = Button(root, text='OPCJE', width=20, height=4, command=options_screen)
    new_path_button.grid(row=3, column=0, pady=5)
    quit_button = Button(root, text='WYJŚCIE', width=20, height=4, command=leaving)
    quit_button.grid(row=4, column=0, pady=5)


if __name__ == "__main__":
    menu_screen()

root.mainloop()
