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
        # Create a database or connect to one
        data = sqlite3.connect(f'{path}')

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
        plt.legend(handles=[blue_patch, orange_patch], bbox_to_anchor=(0., 1.05, 1., .105), loc='lower left', ncol=2, mode="expand", borderaxespad=-0.4)
        plt.show()

        # Commit Changes
        data.commit()

        # Close Connection
        data.close()

        root.quit()

    # Third screen
    def results():
        # Create a database or connect to one
        data = sqlite3.connect(f'{path}')

        # Create cursor
        cursor = data.cursor()

        # Create table

        def back_to_second_screen():
            second_screen(2)
            results_label.destroy()
            record_label.destroy()
            filter_entry.destroy()
            date_filter_button.destroy()
            value_filter_button.destroy()
            back_to_second_screen_button.destroy()
            delete_button.destroy()

        def delete():
            # Create a database or connect to one
            data = sqlite3.connect(f'{path}')

            # Create cursor
            cursor = data.cursor()

            # Create table
            cursor.execute(f"DELETE from addresses WHERE oid = {filter_entry.get()}")
            messagebox.showinfo(title='Delete', message=f'Pozycja numer {filter_entry.get()} została pomyślnie usunięta')
            back_to_second_screen()

            # Commit Changes
            data.commit()

            # Close Connection
            data.close()

        def date_filter():
            # Create a database or connect to one
            data = sqlite3.connect(f'{path}')

            # Create cursor
            cursor = data.cursor()

            # Create table
            date = filter_entry.get()
            cursor.execute("SELECT *, oid FROM addresses WHERE formatted_date = ?", (date,))
            date_filtered_records = cursor.fetchall()
            date_record_print = ''
            for date_filtered in date_filtered_records:
                date_record_print += str(date_filtered[3]) + '.  ' + str(date_filtered[2]) + "     " + str(date_filtered[0]) + " / " + str(date_filtered[1]) + "\n"

            def clear_filters():
                results()
                date_filtered_label.destroy()
                clear_filters_button.destroy()
                filter_entry.destroy()
                date_filter_button.destroy()
                value_filter_button.destroy()
                back_to_second_screen_button.destroy()
                results_label.destroy()
                delete_button.destroy()

            date_filtered_label = Label(root, text=date_record_print)
            date_filtered_label.grid(row=2, column=0, pady=20, columnspan=2)
            clear_filters_button = Button(root, text='Wyczyć filtry', command=clear_filters)
            clear_filters_button.grid(row=5, column=1)

            # Commit Changes
            data.commit()

            # Close Connection
            data.close()

            record_label.destroy()
            date_filter_button.config(state=DISABLED)
            value_filter_button.config(state=DISABLED)
            back_to_second_screen_button.config(state=DISABLED)
            delete_button.config(state=DISABLED)

        def value_filter():
            # Create a database or connect to one
            data = sqlite3.connect(f'{path}')

            # Create cursor
            cursor = data.cursor()

            # Create table
            value = filter_entry.get()
            cursor.execute("SELECT *, oid FROM addresses WHERE systolic_arterial_pressure = ? or diastolic_blood_pressure = ?", (value, value))
            value_filtered_records = cursor.fetchall()
            value_record_print = ''
            for value_filtered in value_filtered_records:
                value_record_print += str(value_filtered[3]) + '.  ' + str(value_filtered[2]) + "     " + str(value_filtered[0]) + " / " + str(value_filtered[1]) + "\n"

            def clear_filters():
                results()
                value_filtered_label.destroy()
                clear_filters_button.destroy()
                filter_entry.destroy()
                date_filter_button.destroy()
                value_filter_button.destroy()
                back_to_second_screen_button.destroy()
                results_label.destroy()
                delete_button.destroy()

            value_filtered_label = Label(root, text=value_record_print)
            value_filtered_label.grid(row=2, column=0, pady=20, columnspan=2)
            clear_filters_button = Button(root, text='Wyczyć filtry', command=clear_filters)
            clear_filters_button.grid(row=5, column=1)

            # Commit Changes
            data.commit()

            # Close Connection
            data.close()

            record_label.destroy()
            date_filter_button.config(state=DISABLED)
            value_filter_button.config(state=DISABLED)
            back_to_second_screen_button.config(state=DISABLED)
            delete_button.config(state=DISABLED)

        cursor.execute("SELECT *, oid FROM addresses")
        records = cursor.fetchall()

        record_print = ''
        for record in records:
            record_print += str(record[3]) + '.  ' + str(record[2]) + "     " + str(record[0]) + " / " + str(record[1]) + "\n"

        title_label.grid(columnspan=3)
        results_label = Label(root, text='Wyniki:')
        results_label.grid(row=1, column=0, pady=20, columnspan=3)
        record_label = Label(root, text=record_print)
        record_label.grid(row=2, column=0, columnspan=3)
        filter_entry = Entry(root, width=40, borderwidth=5)
        filter_entry.grid(row=3, column=0, pady=(20, 10), padx=10, columnspan=3)
        date_filter_button = Button(root, text='Filtruj po dacie', command=date_filter)
        date_filter_button.grid(row=4, column=0)
        value_filter_button = Button(root, text='Filtruj po wartości', command=value_filter)
        value_filter_button.grid(row=4, column=1)
        delete_button = Button(root, text='Usuń', command=delete)
        delete_button.grid(row=4, column=2)
        back_to_second_screen_button = Button(root, text='Wróć', command=back_to_second_screen)
        back_to_second_screen_button.grid(row=5, column=0, pady=10)

        # Commit Changes
        data.commit()

        # Close Connection
        data.close()

        measure1_entry.destroy()
        measure2_entry.destroy()
        measure1_label.destroy()
        measure2_label.destroy()
        add_button.destroy()
        results_button.destroy()
        plot_button.destroy()
        quit_button.destroy()

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
