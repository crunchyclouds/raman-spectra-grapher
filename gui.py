import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Raman Spectra")

w=1000
h=600
ws = root.winfo_screenwidth() # width of the screen
hs = root.winfo_screenheight()
x = (ws/2) - (w/2)
y = (hs/2) - (h/2) - 40
root.geometry('%dx%d+%d+%d' % (w, h, x, y))

#col_count, row_count = root.grid_size()
#for col in xrange(col_count):
#    root.grid_columnconfigure(col, minsize=x/12)
#for row in xrange(row_count):
#    root.grid_rowconfigure(row, minsize=y/12)

root.columnconfigure(12, minsize=y/12)
root.rowconfigure(12, minsize=x/12)
root.resizable(True,True)

def title_command():
    print('Raman spectroscopy is a versatile, nondestructive technique '
          'that yields detailed information about chemical structure.')

title_B = ttk.Button(root, text='Raman Spectra Analysis', command= lambda: title_command())
title_B.grid(row=1, column=6)


def file_OM():
    opts_list = ['Single ".xlsx" type file', 'Folder of ".xlsx" type files']
    retained_opt = tk.StringVar(root)
    retained_opt.set('Select a file type')

    input_OM = tk.OptionMenu(root, retained_opt, *opts_list)
    input_OM.grid(row=9, column=6)
    input_OM.configure(height=0, width=0)

input_B = ttk.Button(root, text='Upload your files', command= lambda: file_OM())
input_B.grid(row=8,column=6)


root.mainloop()