from tkinter import *
from tkinter.ttk import *
from tkinter import font, colorchooser, filedialog, messagebox
import os


#Functionality part

def statusBarFunction(event):
    if textArea.edit_modified():
        words = len(textArea.get(0.0, END).split())
        characters = len(textArea.get(0.0, 'end-1c').replace(' ', ''))
        status_bar.config(text=f'Charecters: {characters} Words: {words}')

    textArea.edit_modified(False)


url = ''
def new_file():
    global url
    url = ''
    textArea.delete(0.0, END)

def open_file():
    global url
    url = filedialog.askopenfilename(initialdir=os.getcwd(), title='Select File', filetypes=(('Text File', 'txt'),
                                                                                        ('All File', '*.*')))
    if url != '':
        data = open(url, 'r')
        textArea.insert(0.0, data.read())
    root.title(os.path.basename(url))

def save_file():
    if url == '':
        save_url = filedialog.asksaveasfile(mode='w', defaultextension='.txt', filetypes=(('Text File', 'txt'),
                                                                               ('All File', '*.*')))
        content = textArea.get(0.0, END)
        save_url.write(content)
        save_url.close()
    else:
        content = textArea.get(0.0, END)
        file = open(url, 'w')
        file.write(content)

def saveas_file():
    save_url = filedialog.asksaveasfile(mode='w', defaultextension='.txt', filetypes=(('Text File', 'txt'),
                                                                                      ('All File', '*.*')))
    content = textArea.get(0.0, END)
    save_url.write(content)
    save_url.close()
    if url != '':
        os.remove(url)

def iexit():
    if textArea.edit_modified():
        result = messagebox.askyesnocancel('Warning', 'Do you want to save the file')
        if result is True:
            if url != '':
                content = textArea.get(0.0, END)
                file = open(url, 'w')
                file.write(content)
                root.destroy()
            else:
                content = textArea.get(0.0, END)
                save_url = filedialog.asksaveasfile(mode='w', defaultextension='.txt', filetypes=(('Text File', 'txt'),
                                                                                                  ('All File', '*.*')))
                save_url.write(content)
                save_url.close()
                root.destroy()

        elif result is False:
            root.destroy()

        else:
            pass

    else:
        root.destroy()


fontSize = 12
fontStyle='arial'
def font_style(even):
    global  fontStyle
    fontStyle = font_family_variable.get()
    textArea.config(font=(fontStyle, fontSize))

def font_size(even):
    global fontSize
    fontSize=size_variable.get()
    textArea.config(font=(fontStyle, fontSize))

def bold_text():
    text_property = font.Font(font=textArea['font']).actual()
    if text_property['weight'] == 'normal':
        textArea.config(font=(fontStyle, fontSize, 'bold'))

    if text_property['weight'] == 'bold':
        textArea.config(font=(fontStyle, fontSize, 'normal'))

def italic_text():
    text_property = font.Font(font=textArea['font']).actual()
    if text_property['slant'] == 'roman':
        textArea.config(font=(fontStyle, fontSize, 'italic'))

    if text_property['slant'] == 'italic':
        textArea.config(font=(fontStyle, fontSize, 'roman'))

def underline_text():
    text_property = font.Font(font=textArea['font']).actual()
    if text_property['underline'] == 0:
        textArea.config(font=(fontStyle, fontSize, 'underline'))

    if text_property['underline'] == 1:
        textArea.config(font=(fontStyle, fontSize))

def color_select():
    color = colorchooser.askcolor()
    textArea.config(fg=color[1])

def align_right():
    data = textArea.get(0.0, END)
    textArea.tag_config('right', justify=RIGHT)
    textArea.delete(0.0, END)
    textArea.insert(INSERT, data, 'right')

def align_left():
    data = textArea.get(0.0, END)
    textArea.tag_config('left', justify=LEFT)
    textArea.delete(0.0, END)
    textArea.insert(INSERT, data, 'left')

def align_center():
    data = textArea.get(0.0, END)
    textArea.tag_config('center', justify=CENTER)
    textArea.delete(0.0, END)
    textArea.insert(INSERT, data, 'center')


root = Tk()
root.title('Text Editor by Imran')
root.geometry('1230x620+10+10')
root.resizable(False, False)

#creating menubar
menubar = Menu(root)
root.config(menu=menubar)

#creating FILE menu section
filemenu = Menu(menubar, tearoff=False)
menubar.add_cascade(label='File', menu=filemenu)
newImage = PhotoImage(file='Assets/new.png')
openImage = PhotoImage(file='Assets/open.png')
saveImage = PhotoImage(file='Assets/save.png')
saveasImage = PhotoImage(file='Assets/save_as.png')
exitImage = PhotoImage(file='Assets/exit.png')

filemenu.add_command(label='New', accelerator='Ctrl+N', image=newImage, compound=LEFT, command=new_file)
filemenu.add_command(label='Open', accelerator='Ctrl+O', image=openImage, compound=LEFT, command=open_file)
filemenu.add_command(label='Save', accelerator='Ctrl+S', image=saveImage, compound=LEFT, command=save_file)
filemenu.add_command(label='Save As', accelerator='Ctrl+All+S', image=saveasImage, compound=LEFT, command=saveas_file)
#drow a horizontal line
filemenu.add_separator()
filemenu.add_command(label='Exit', accelerator='Ctrl+Q', image=exitImage, compound=LEFT, command=iexit)

#creating EDIT menu section
cutImage = PhotoImage(file='Assets/cut.png')
copyImage = PhotoImage(file='Assets/copy.png')
pasteImage = PhotoImage(file='Assets/paste.png')
clearImage = PhotoImage(file='Assets/clear_all.png')
findImage = PhotoImage(file='Assets/find.png')

editmenu = Menu(menubar, tearoff=False)
editmenu.add_command(label='Cut', accelerator='Ctrl+X', image=cutImage, compound=LEFT)
editmenu.add_command(label='Copy', accelerator='Ctrl+C', image=copyImage, compound=LEFT)
editmenu.add_command(label='Paste', accelerator='Ctrl+V', image=pasteImage, compound=LEFT)
editmenu.add_command(label='Clear', accelerator='Ctrl+Alt+X', image=clearImage, compound=LEFT)
editmenu.add_command(label='Find', accelerator='Ctrl+F', image=findImage, compound=LEFT)
menubar.add_cascade(label='Edit', menu=editmenu)

#creating VIEW menu section
show_toolbar = BooleanVar()
show_statusbar= BooleanVar()

toolImage = PhotoImage(file='Assets/tool_bar.png')
statusImage = PhotoImage(file='Assets/status_bar.png')

viewmenu = Menu(menubar, tearoff=False)
viewmenu.add_checkbutton(label='Tool Bar', variable=show_toolbar, onvalue=True, offvalue=False, image=toolImage, compound=LEFT)
viewmenu.add_checkbutton(label='status Bar', variable=show_statusbar, onvalue=True, offvalue=False, image=statusImage, compound=LEFT)
menubar.add_cascade(label='View', menu=viewmenu)

#creating THEME menu section
thememenu = Menu(menubar, tearoff=False)
menubar.add_cascade(label='Theme', menu=thememenu)

theme_choice = StringVar()
lightImage = PhotoImage(file='Assets/light_default.png')
darkImage = PhotoImage(file='Assets/dark.png')
pinkImage = PhotoImage(file='Assets/red.png')
monokaiImage = PhotoImage(file='Assets/monokai.png')

thememenu.add_radiobutton(label='Light Default', image=lightImage, variable=theme_choice, compound=LEFT)
thememenu.add_radiobutton(label='Dark', image=darkImage, variable=theme_choice, compound=LEFT)
thememenu.add_radiobutton(label='Pink', image=pinkImage, variable=theme_choice, compound=LEFT)
thememenu.add_radiobutton(label='Monokai', image=monokaiImage, variable=theme_choice, compound=LEFT)

#creating First TOOLBAR section
too_bar = Label(root)
too_bar.pack(side=TOP, fill=X)
font_families = font.families()
font_family_variable = StringVar()
fontfamily_Combobox = Combobox(too_bar, width=30, values=font_families, state='readonly', textvariable=font_family_variable)
fontfamily_Combobox.current(font_families.index('Arial'))
fontfamily_Combobox.grid(row=0, column=0, padx=5)


#creating Second TOOLBAR section
size_variable = IntVar()
font_size_combobox = Combobox(too_bar, width=14, textvariable=size_variable, state='readonly', values=tuple(range(8, 81)))
font_size_combobox.current(4)
font_size_combobox.grid(row=0, column=1, padx=5)

fontfamily_Combobox.bind('<<ComboboxSelected>>', font_style)
font_size_combobox.bind('<<ComboboxSelected>>', font_size)

#creating BUTTON section
boldImage = PhotoImage(file='Assets/bold.png')
boldButton = Button(too_bar, image=boldImage, command=bold_text)
boldButton.grid(row=0, column=2, padx=5)

italicImage = PhotoImage(file='Assets/italic.png')
italicButton = Button(too_bar, image=italicImage, command=italic_text)
italicButton.grid(row=0, column=3, padx=5)

underlineImage = PhotoImage(file='Assets/underline.png')
underlineButton = Button(too_bar, image=underlineImage, command=underline_text)
underlineButton.grid(row=0, column=4, padx=5)

fontColorImage = PhotoImage(file='Assets/font_color.png')
fontColorButton = Button(too_bar, image=fontColorImage, command=color_select)
fontColorButton.grid(row=0, column=5, padx=5)

leftAlighnImage = PhotoImage(file='Assets/left.png')
leftAlighnButton = Button(too_bar, image=leftAlighnImage, command=align_left)
leftAlighnButton.grid(row=0, column=6, padx=5)

rightAlighnImage = PhotoImage(file='Assets/right.png')
rightAlighnButton = Button(too_bar, image=rightAlighnImage, command=align_right)
rightAlighnButton.grid(row=0, column=7, padx=5)

centerImage = PhotoImage(file='Assets/center.png')
centerButton = Button(too_bar, image=centerImage, command=align_center)
centerButton.grid(row=0, column=8, padx=5)

#creating SCROLLBAR
scrollbar = Scrollbar(root)
scrollbar.pack(side=RIGHT, fill=Y)
#creating TEXT area
textArea = Text(root, yscrollcommand=scrollbar.set, font=('arial', 12))
textArea.pack(fill=BOTH, expand=True)
scrollbar.config(command=textArea.yview)

status_bar = Label(root, text='Status Bar')
status_bar.pack(side=BOTTOM)

textArea.bind('<<Modified>>', statusBarFunction)

root.mainloop()
