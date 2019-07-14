import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import re

# Funciones -------------------------------------

def move_subs(file, sec, mil):
    
    if sec == '': sec = 0
    if mil == '': mil = 0

    try:
        sec = int(sec)
        mil = int(mil)
    except:
        messagebox.showwarning('Invalid Input', 'Seconds and Miliseconds must be positive numbers!')
        raise Exception

    if not (sec >= 0 and mil >= 0):
        messagebox.showwarning('Invalid Input', 'Seconds and Miliseconds must be positive numbers!')
        raise Exception

    if ade_o_ret.get() == 2:
        sec = -sec
        mil = -mil

    new_text = ''

    try:
        fil = open(file)
    except:
        messagebox.showwarning('Invalid File', 'Please enter an existing subtitle file.')
        raise Exception

    rex = "(\d{2}):(\d{2}):(\d{2}),(\d{3}) --> (\d{2}):(\d{2}):(\d{2}),(\d{3})"
    for line in fil.readlines():
        match = re.search(rex, line)
        if match:
            times = [list(match.groups()[:4]), list(match.groups()[4:])]
            new_times = []
            for t in times:
                a = (int(t[3]) + mil) % 1000
                b = (int(t[2]) + sec + ((int(t[3]) + mil) // 1000)) % 60
                c = (int(t[1]) + (int(t[2]) + sec + ((int(t[3]) + mil) // 1000)) // 60) % 60
                d = int(t[0]) + ((int(t[1]) + (int(t[2]) + sec + ((int(t[3]) + mil) // 1000)) // 60) // 60)
                new_times.append([d,c,b,a])
            
            new_line = "{}:{}:{},{} --> {}:{}:{},{}\n".format(add_zeros(str(new_times[0][0]), 2),
                                                            add_zeros(str(new_times[0][1]), 2),
                                                            add_zeros(str(new_times[0][2]), 2),
                                                            add_zeros(str(new_times[0][3]), 3),
                                                            add_zeros(str(new_times[1][0]), 2),
                                                            add_zeros(str(new_times[1][1]), 2),
                                                            add_zeros(str(new_times[1][2]), 2),
                                                            add_zeros(str(new_times[1][3]), 3))
        
        else:
            new_line = line
        
        new_text = new_text + new_line
    
    return(new_text)

def add_zeros(string, num_digits):
    while len(string) < num_digits:
        string = "0" + string
    return(string)
        
def OpenFile():
    global name_subfile
    name_subfile = filedialog.askopenfilename(master=root,
                                    initialdir="C:/",
                                    filetypes =(("Subs file", "*.srt"),("All Files","*.*")),
                                    title = "Choose a file."
                                    )
    file_entry_load.insert(0, name_subfile)


def SaveFile():
    global name_save
    name_save = filedialog.asksaveasfilename(master=root,
                                    initialdir="C:/",
                                    filetypes =(("Subs file", "*.srt"),("All Files","*.*")),
                                    title = "Choose a file."
                                    )

    if name_save[-4:] != '.srt':
        name_save = '{}.srt'.format(name_save)

    file_entry_save.insert(0, name_save)

def CreateFile():

    saved = False
    cont = True
    
    try:
        new_subs = move_subs(name_subfile, secs.get(), mils.get())
    except:
        cont = False

    if cont:
        try:
            with open(name_save, 'w') as f:
                f.write(new_subs)
                saved = True
        except:
            messagebox.showwarning('Invalid File', 'Please enter a correct saving file.')

    if saved:
        created_text.configure(text='Subtitle File Created!')


root = tk.Tk(className='SubFixer')
root.iconbitmap('icon.ico')

# Variables:

secs = tk.StringVar(master=root)
mils = tk.StringVar(master=root)
ade_o_ret = tk.IntVar(master=root)
ade_o_ret.set(1)
secs.set('0')
mils.set('0')


def character_limit(entry_text, limit):
    if len(entry_text.get()) > limit:
        entry_text.set(entry_text.get()[:-1])

mils.trace("w", lambda *args: character_limit(mils, limit=3))

# Widgets

file_entry_load = tk.Entry(master=root, justify="left", width=40)
file_button = tk.Button(master=root, text='Open File', command=OpenFile, width=7)

sec_entry = tk.Entry(master=root, textvariable=secs, width=4)
mil_entry = tk.Entry(master=root, textvariable=mils, width=4)

button_ade = tk.Radiobutton(master=root, text='Set Forward', var=ade_o_ret, value=1)
button_ret = tk.Radiobutton(master=root, text='Set Back', var=ade_o_ret, value=2)

sec_label = tk.Label(master=root, text='Seconds')
mil_label = tk.Label(master=root, text='Milliseconds')

file_entry_save = tk.Entry(master=root, justify="left", width=40)
save_button = tk.Button(master=root, text='Save As', command=SaveFile, width=7)

ok_button = tk.Button(master=root, text='Save!', command=CreateFile)
created_text = tk.Label(master=root, fg='green', text="")

# Positioning

file_entry_load.grid(row=0, pady=(10,0), padx=(20,5))
file_button.grid(row=0, column=1, pady=(10,0), padx=(10,10))

sec_entry.grid(row=1, sticky=tk.W, padx=(120,0), pady=(5,0))
sec_label.grid(row=1, sticky=tk.W, padx=(160,0), pady=(5,0))
mil_entry.grid(row=2, sticky=tk.W, padx=(120,0), pady=(5,0))
mil_label.grid(row=2, sticky=tk.W, padx=(160,0), pady=(5,0))

button_ade.grid(row=3, sticky=tk.W, padx=(50,0), pady=(5,0))
button_ret.grid(row=3, sticky=tk.E, pady=(5,0))

file_entry_save.grid(row=4, padx=(20,5), pady=(5,0))
save_button.grid(row=4, column=1, pady=(5,0), padx=(10,10))

ok_button.grid(row=5, padx=(130,50), pady=(10,10))
created_text.grid(row=6, padx=(105,50), pady=(0,10))

root.geometry("350x230")

root.resizable(width=False, height=False)
root.mainloop()