import save_to_excel
import tkinter as tk
from tkinter import messagebox
import traceback



window = tk.Tk()


def on_click_submit():
    search = search_textbot.get()
    url = f"https://it.pracuj.pl/praca/{search};kw?sal=1"
    try:
        save_to_excel.create_excel_file(url)
    except Exception as e:
        messagebox.showerror("Error occur", f"Application didn't find any offers for search: {search}")
        return ""
    messagebox.showinfo("Workbook created", "Workbook with data created")


window.geometry('300x100')
window.title('Pracuj.pl Scrapper')

search_label = tk.Label(window, text='Provide position, company or keywords')
search_label.pack(anchor=tk.W, padx=10)
search_textbot = tk.Entry(window)
search_textbot.pack(anchor=tk.W, padx=10)

submit_button = tk.Button(window, text='Generate spreadsheet', command=on_click_submit)
submit_button.pack(anchor=tk.W, padx=10)

# run
window.mainloop()


