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


def help_options_fun():
    help_options_text = "\nTutaj możesz zmienić ścieżkę lub utworzyć nową bazę danych w której będą zapisywane pomiary ciśnień"
    messagebox.showinfo(title="Wskazówka", message=help_options_text)


def back(screen):
    if screen == 'add_screen':
        menu_screen()
        add_welcome_label.destroy()
        measure1_label.destroy()
        measure2_label.destroy()
        measure1_entry.destroy()
        measure2_entry.destroy()
        add_button.destroy()
        help_button.destroy()
        back_from_adding_button.destroy()

    elif screen == 'database_screen':
        menu_screen()
        database_welcome_label.destroy()
        scroll_record.destroy()
        record_print.destroy()
        filter_button.destroy()
        back_from_database_button.destroy()
        plot_button.destroy()

    elif screen == 'filter_screen':
        database_screen()
        filtered_frame.destroy()
        filter_welcome_label.destroy()
        filtered_scroll_record.destroy()
        filtered_record_print.destroy()
        filter_entry.destroy()
        dropdown_menu.destroy()
        dropdown_menu_button.destroy()
        back_from_filter_button.destroy()

    elif screen == 'options_screen':
        menu_screen()
        brand_new_path.destroy()
        existed_path.destroy()
        options_label.destroy()
        help_options.destroy()
        back_from_options_button.destroy()


def filter_screen():
    # Create a database or connect to one
    file = open('paths/path_file.txt', 'a+')
    file.seek(0)
    path = file.readline()
    data = sqlite3.connect(f'{path}.db')
    file.close()

    # Create cursor
    cursor = data.cursor()

    # Create table
    global filtered_frame, filtered_scroll_record, filtered_record_print

    cursor.execute("SELECT *, oid FROM addresses")
    records = cursor.fetchall()

    filtered_frame = LabelFrame(root, bd=0)
    filtered_frame.grid(row=1, column=0, columnspan=3)
    filtered_scroll_record = Scrollbar(filtered_frame, orient='vertical')
    filtered_scroll_record.grid(row=1, column=1, sticky=NS)
    filtered_record_print = Text(filtered_frame, width=45, height=9, wrap=NONE, bg='#2e2e3d', fg='white', bd=0,
                                 yscrollcommand=filtered_scroll_record.set)
    for record in records:
        filtered_record_print.insert(END,
                                     "\t" + str(record[3]) + '.  ' + str(record[2]) + "     " + str(record[0]) + " / " + str(
                                        record[1]) + "  " + "\t\t\n")

    filtered_record_print.grid(row=1, column=0)
    filtered_scroll_record.config(command=filtered_record_print.yview)

    def filter_action(action):
        # Create a database or connect to one
        file = open('paths/path_file.txt', 'a+')
        file.seek(0)
        path = file.readline()
        data = sqlite3.connect(f'{path}.db')
        file.close()

        # Create cursor
        cursor = data.cursor()

        # Create table
        if action == 'FILTRUJ PO DACIE':
            filtered_record_print.delete(1.0, END)
            date = filter_entry.get()
            cursor.execute("SELECT *, oid FROM addresses WHERE formatted_date = ?", (date,))
            date_filtered_records = cursor.fetchall()
            for date_filtered in date_filtered_records:
                filtered_record_print.insert(END, str(date_filtered[3]) + '.  ' + str(date_filtered[2]) + "     " + str(
                    date_filtered[0]) + " / " + str(date_filtered[1]) + "\n")

        elif action == 'FILTRUJ PO WARTOŚCI':
            filtered_record_print.delete(1.0, END)
            value = filter_entry.get()
            cursor.execute(
                "SELECT *, oid FROM addresses WHERE systolic_arterial_pressure = ? or diastolic_blood_pressure = ?",
                (value, value))
            value_filtered_records = cursor.fetchall()
            for value_filtered in value_filtered_records:
                filtered_record_print.insert(END, str(value_filtered[3]) + '.  ' + str(value_filtered[2]) + "     " + str(
                    value_filtered[0]) + " / " + str(value_filtered[1]) + "\n")

        elif action == 'USUŃ':
            cursor.execute(f"DELETE from addresses WHERE oid = {filter_entry.get()}")
            messagebox.showinfo(title='Delete',
                                message=f'Pozycja numer {filter_entry.get()} została pomyślnie usunięta')
            filter_entry.delete(0, END)

        # Commit Changes
        data.commit()

        # Close Connection
        data.close()

    # Destroying redundant widgets
    database_welcome_label.destroy()
    scroll_record.destroy()
    record_print.destroy()
    back_from_database_button.destroy()
    filter_button.destroy()
    plot_button.destroy()

    # Defining new widgets
    global filter_var, filter_welcome_label, back_from_filter_button, filter_entry, dropdown_menu, dropdown_menu_button

    filter_var = StringVar()
    filter_var.set("-- wybierz --")
    filter_options = ['FILTRUJ PO DACIE', 'FILTRUJ PO WARTOŚCI', 'USUŃ']

    filter_welcome_label = Label(root, text='BAZA DANYCH', width=19, height=2, font="Verdana 32", bg='#161618',
                                 fg="white", relief="solid")
    filter_welcome_label.grid(row=0, column=0, padx=40, pady=15, columnspan=3)
    filter_entry = Entry(root, width=30, borderwidth=5)
    filter_entry.grid(row=2, column=0, pady=(15, 10), sticky=E, ipady=1.6)
    dropdown_menu = OptionMenu(root, filter_var, *filter_options)
    dropdown_menu.grid(row=2, column=1)
    dropdown_menu_button = Button(root, text='ZATWIERDŹ', width=10, command=lambda: filter_action(filter_var.get()))
    dropdown_menu_button.grid(row=2, column=2, sticky=W, ipady=1.7)
    back_from_filter_button = Button(root, text='POWRÓT', width=20, height=4, command=lambda: back('filter_screen'))
    back_from_filter_button.grid(row=4, column=0, pady=5, columnspan=3)

    # Commit Changes
    data.commit()

    # Close Connection
    data.close()


def database_screen():
    # Create a database or connect to one
    file = open('paths/path_file.txt', 'a+')
    file.seek(0)
    path = file.readline()
    data = sqlite3.connect(f'{path}.db')
    file.close()

    # Create cursor
    cursor = data.cursor()

    # Create table
    cursor.execute("SELECT *, oid FROM addresses")
    records = cursor.fetchall()

    global scroll_record, record_print
    scroll_record = Scrollbar(root, orient='vertical')
    scroll_record.grid(row=1, column=1, sticky=NS)
    record_print = Text(root, width=33, height=9, wrap=NONE, bg='#2e2e3d', fg='white', bd=0, yscrollcommand=scroll_record.set)

    for record in records:
        record_print.insert(END, "  " + str(record[3]) + '.  ' + str(record[2]) + "     " + str(record[0]) + " / " + str(record[1]) + "  " + "\n")

    record_print.grid(row=1, column=0, sticky=E)
    scroll_record.config(command=record_print.yview)

    # Destroying redundant widgets
    menu_label.destroy()
    add_label.destroy()
    database_button.destroy()
    new_path_button.destroy()
    quit_button.destroy()

    # Defining new widgets
    global database_welcome_label, back_from_database_button, filter_button, plot_button

    database_welcome_label = Label(root, text='BAZA DANYCH', width=19, height=2, font="Verdana 32", bg='#161618',
                                   fg="white", relief="solid")
    database_welcome_label.grid(row=0, column=0, padx=40, pady=15, columnspan=2)
    filter_button = Button(root, text='FILTRY', width=20, height=4, command=filter_screen)
    filter_button.grid(row=2, column=0, pady=(10, 5), columnspan=2)
    plot_button = Button(root, text='WYKRES', width=20, height=4, command=plot)
    plot_button.grid(row=3, column=0, pady=5, columnspan=2)
    back_from_database_button = Button(root, text='POWRÓT', width=20, height=4, command=lambda: back('database_screen'))
    back_from_database_button.grid(row=4, column=0, pady=5, columnspan=2)

    # Commit Changes
    data.commit()

    # Close Connection
    data.close()


def plot():
    # Create a database or connect to one
    file = open('paths/path_file.txt', 'a+')
    file.seek(0)
    path = file.readline()
    data = sqlite3.connect(f'{path}.db')
    file.close()

    # Create cursor
    cursor = data.cursor()

    # Create table
    cursor.execute("SELECT systolic_arterial_pressure, diastolic_blood_pressure FROM addresses")
    plot_pressure_records = cursor.fetchall()

    cursor.execute("SELECT oid, formatted_date FROM addresses")
    plot_oid_date_records = cursor.fetchall()
    plot_oid_date_list = []
    for plot_pressure_record in plot_oid_date_records:
        plot_oid_date_list.append(str(plot_pressure_record[0]) + '. ' + str(plot_pressure_record[1]))

    plt.figure(figsize=(9.2, 7))
    plt.plot(plot_oid_date_list, plot_pressure_records)
    plt.xticks(rotation=90, fontsize=6)
    plt.rc('xtick', labelsize=20)
    orange_patch = mpatches.Patch(color='orange', label='ciśnienie tętnicze rozkurczowe')
    blue_patch = mpatches.Patch(color='blue', label='ciśnienie tętnicze skurczowe')
    plt.legend(handles=[blue_patch, orange_patch], bbox_to_anchor=(0., 1.05, 1., .105), loc='lower left', ncol=2,
               mode="expand", borderaxespad=-0.4)
    plt.grid()
    plt.show()

    # Commit Changes
    data.commit()

    # Close Connection
    data.close()

    # Plot close
    root.quit()


def help_info():
    help_text = "\n- Pomiar wykonuje się w pozycji siedzącej, w spokoju, po minimum 5-minutowym odpoczynku\n- Przed " \
                "pomiarem przez minimum 30 minut nie należy palić tytoniu, pić kawy i wykonywać ćwiczeń fizycznych\n- "\
                "Przedramię ręki, na której dokonujemy pomiaru, powinno znajdować się na wysokości serca, " \
                "ręka powinna być podparta\n- Badanie należy wykonać na obydwu rękach\n- Należy wykonać 2 pomiary, " \
                "w odstępach około minuty i przyjąć wartość średnią "

    messagebox.showinfo(title="Wskazówka", message=help_text)


def add():
    # Create a database or connect to one
    file = open('paths/path_file.txt', 'a+')
    file.seek(0)
    path = file.readline()
    data = sqlite3.connect(f'{path}.db')
    file.close()

    # Create cursor
    cursor = data.cursor()

    # Create table
    systolic_arterial_pressure = int(measure1_entry.get())
    diastolic_blood_pressure = int(measure2_entry.get())
    current_date = datetime.now()
    formatted_date = current_date.strftime('%d.%m.%Y')

    if 0 <= systolic_arterial_pressure < 120 and 0 <= diastolic_blood_pressure < 80:
        messagebox.showinfo(title='Powiadominenie o normie', message='Twoje ciśnienie jest optymalne')
    elif 0 <= systolic_arterial_pressure <= 129 and 0 <= diastolic_blood_pressure <= 84:
        messagebox.showinfo(title='Powiadominenie o normie', message='Twoje ciśnienie jest prawidłowe')
    elif 0 <= systolic_arterial_pressure <= 139 and 0 <= diastolic_blood_pressure <= 89:
        messagebox.showinfo(title='Powiadominenie o normie', message='Twoje ciśnienie jest prawidłowe wysokie')
    elif 0 <= systolic_arterial_pressure <= 159 and 0 <= diastolic_blood_pressure <= 99:
        messagebox.showwarning(title='Powiadominenie o normie', message='Masz łagodne nadciśnienie')
    elif 0 <= systolic_arterial_pressure <= 179 and 0 <= diastolic_blood_pressure <= 109:
        messagebox.showwarning(title='Powiadominenie o normie', message='Masz umiarkowane nadciśnienie')
    elif 0 <= systolic_arterial_pressure <= 1000 and 0 <= diastolic_blood_pressure <= 1000:
        messagebox.showwarning(title='Powiadominenie o normie', message='Masz ciężkie nadciśnienie')
    else:
        messagebox.showerror(title='Powiadominenie o normie', message='Ciężko określić')

    cursor.execute(
        "INSERT INTO addresses VALUES (:systolic_arterial_pressure, :diastolic_blood_pressure, :formatted_date)",
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


def new_path_window(status):
    file = open('paths/path_file.txt', 'a+')
    file.seek(0)
    path = file.readline()
    file.close()
    previous_path = path
    try:
        global new_path

        if status == 'new':
            root.dic_name = filedialog.askdirectory(title='Wybierz folder zapisu')
            name = simpledialog.askstring('Nazwa pliku', 'Podaj nazwe pliku')
            new_path = root.dic_name + '/' + name
        elif status == 'existed':
            root.file_name = filedialog.askopenfilename(title='Wybierz plik', filetype=[('db files', '*.db')])
            root.file_name = root.file_name
            new_path = root.file_name.replace('.db', '')

        # Changing database's path in the path_file.txt
        writing_file = open("paths/path_file.txt", "w")
        if new_path == '':
            writing_file.write(previous_path)
        else:
            writing_file.write(new_path)
        writing_file.close()

        file = open("paths/path_file.txt", "a+")
        file.seek(0)
        path = file.readline()
        data = sqlite3.connect(f'{path}.db')
        file.close()

        # Create cursor
        cursor = data.cursor()

        # Create table
        if status == 'new':
            cursor.execute("""CREATE TABLE addresses (
                                        systolic_arterial_pressure integer,
                                        diastolic_blood_pressure integer,
                                        formatted_date text) 
                                    """)

        # Commit Changes
        data.commit()

        # Close Connection
        data.close()
    except TypeError:
        pass


def options_screen():
    # Destroying redundant widgets
    menu_label.destroy()
    add_label.destroy()
    database_button.destroy()
    new_path_button.destroy()
    quit_button.destroy()

    # Defining new widgets
    global brand_new_path, existed_path, options_label, back_from_options_button, help_options

    options_label = Label(root, text='OPCJE', width=19, height=2, font="Verdana 32", bg='#161618', fg="white",
                          relief="solid")
    options_label.grid(row=0, column=0, padx=40, pady=15)
    brand_new_path = Button(root, text='NOWY ZAPIS', width=20, height=4, command=lambda: new_path_window('new'))
    brand_new_path.grid(row=1, column=0, pady=5)
    existed_path = Button(root, text='OTWÓRZ ZAPIS', width=20, height=4, command=lambda: new_path_window('existed'))
    existed_path.grid(row=2, column=0, pady=5)
    help_options = Button(root, text='POMOC', width=20, height=4, command=help_options_fun)
    help_options.grid(row=3, column=0, pady=5)
    back_from_options_button = Button(root, text='POWRÓT', width=20, height=4, command=lambda: back('options_screen'))
    back_from_options_button.grid(row=4, column=0, pady=5)
    

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
