from tkinter import *
from tkinter.ttk import *
from tkinter import font, colorchooser, filedialog, messagebox
import os
import tempfile
from datetime import datetime


#Functionality part

def date_time(event=None):
    currentdatetime = datetime.now()
    formatteddatetime = currentdatetime.strftime('%d/%m/%y %H:%M:%S')     #02/07/22 13:37:22
    # formatteddatetime = currentdatetime.strftime('%b-%d-%y %H:%M:%S')   #Jul-02-22 13:36:37
    # formatteddatetime = currentdatetime.strftime('%m, %d, %y %H:%M:%S') #07, 02, 22 13:37:49
    textArea.insert(1.0, formatteddatetime)


def printout(event=None):
    file = tempfile.mktemp('.txt')
    open(file, 'w').write(textArea.get(1.0, END))
    os.startfile(file, 'print')

def change_theme(bg_color, fg_color):
    textArea.config(bg=bg_color, fg=fg_color)


def toolbarFunc():
    if show_toolbar.get()==False:
        too_bar.pack_forget()
    if show_toolbar.get()==True:
        textArea.pack_forget()
        too_bar.pack(fill=X)
        textArea.pack(fill=BOTH, expand=1)

def statusbarFunc():
    if show_statusbar.get()==False:
        status_bar.pack_forget()
    else:
        status_bar.pack()


def find(event=None):

    #funtionality

    def find_words():
        textArea.tag_remove('match', 1.0, END)
        start_pos = '1.0'
        word = findentryField.get()
        if word:
            while True: #I am a boy I am 16 yrs old
                start_pos = textArea.search(word, start_pos, stopindex=END) #1.0
                if not start_pos:
                    break
                end_pos = f'{start_pos}+{len(word)}c' #1.0+1c
                textArea.tag_add('match', start_pos, end_pos)

                textArea.tag_config('match', foreground='red', background='yellow')
                start_pos = end_pos

    def replace_text():
        word = findentryField.get()
        replaceword = replaceentryField.get()
        conntent = textArea.get(1.0, END)
        new_content = conntent.replace(word, replaceword)
        textArea.delete(1.0, END)
        textArea.insert(1.0, new_content)


    #GUI
    root1 = Toplevel()

    root1.title('Find')
    root1.geometry('450x250+500+200')
    root1.resizable(0,0)

    labelFrame = LabelFrame(root1, text='Find/Replace')
    labelFrame.pack(pady=50)

    findLabel = Label(labelFrame, text='Find')
    findLabel.grid(row=0, column=0, padx=5, pady=5)
    findentryField = Entry(labelFrame)
    findentryField.grid(row=0, column=1, padx=5, pady=5)

    replaceLabel = Label(labelFrame, text='Replace')
    replaceLabel.grid(row=1, column=0, padx=5, pady=5)
    replaceentryField = Entry(labelFrame)
    replaceentryField.grid(row=1, column=1, padx=5, pady=5)

    findButton = Button(labelFrame, text='FIND',command=find_words)
    findButton.grid(row=2, column=0, padx=5, pady=5)

    replaceButton = Button(labelFrame, text='REPLACE', command=replace_text)
    replaceButton.grid(row=2, column=1, padx=5, pady=5)

    def doSomething():
        textArea.tag_remove('match', 1.0, END)
        root1.destroy()

    root1.protocol('WM_DELETE_WINDOW',doSomething)

    root1.mainloop()

def statusBarFunction(event):
    if textArea.edit_modified():
        words = len(textArea.get(0.0, END).split())
        characters = len(textArea.get(0.0, 'end-1c').replace(' ', '')) #1.0 also correct
        status_bar.config(text=f'Charecters: {characters} Words: {words}')

    textArea.edit_modified(False)


url = ''
def new_file(event=None):
    global url
    if textArea.edit_modified():
        result = messagebox.askyesnocancel('Confirm', 'Do you want to save this file?')
        if result == True:
            save_file()
    url = ''
    textArea.delete(0.0, END)

def open_file(event=None):
    global url
    textArea.delete(1.0, END)
    url = filedialog.askopenfilename(initialdir=os.getcwd(), title='Select File', filetypes=(('Text File', 'txt'),
                                                                                        ('All File', '*.*')))
    if url != '':
        data = open(url, 'r')
        textArea.insert(0.0, data.read())
    root.title(os.path.basename(url))

def save_file(event=None):
    if url == '':
        save_url = filedialog.asksaveasfile(mode='w', defaultextension='.txt', filetypes=(('Text File', 'txt'),
                                                                               ('All File', '*.*')))
        if save_url is None:
            pass
        else:
            content = textArea.get(0.0, END)
            save_url.write(content)
            save_url.close()
    else:
        content = textArea.get(0.0, END)
        file = open(url, 'w')
        file.write(content)

def saveas_file(event=None):
    save_url = filedialog.asksaveasfile(mode='w', defaultextension='.txt', filetypes=(('Text File', 'txt'),
                                                                                      ('All File', '*.*')))
    content = textArea.get(0.0, END)
    save_url.write(content)
    save_url.close()
    if url != '':
        os.remove(url)

def iexit(event=None):
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


# created window
root = Tk()   # we have created object of tk class
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
printImage = PhotoImage(file='Assets/print.png')

filemenu.add_command(label='New', accelerator='Ctrl+N', image=newImage, compound=LEFT, command=new_file)
filemenu.add_command(label='Open', accelerator='Ctrl+O', image=openImage, compound=LEFT, command=open_file)
filemenu.add_command(label='Save', accelerator='Ctrl+S', image=saveImage, compound=LEFT, command=save_file)
filemenu.add_command(label='Save As', accelerator='Ctrl+Alt+S', image=saveasImage, compound=LEFT, command=saveas_file)
filemenu.add_command(label='Print', accelerator='Ctrl+P', image=printImage, compound=LEFT, command=printout)
#drow a horizontal line
filemenu.add_separator()
filemenu.add_command(label='Exit', accelerator='Ctrl+Q', image=exitImage, compound=LEFT, command=iexit)

#creating EDIT menu section
cutImage = PhotoImage(file='Assets/cut.png')
copyImage = PhotoImage(file='Assets/copy.png')
pasteImage = PhotoImage(file='Assets/paste.png')
clearImage = PhotoImage(file='Assets/clear_all.png')
findImage = PhotoImage(file='Assets/find.png')
selectImage = PhotoImage(file='Assets/select-all.png')
datetimeImage = PhotoImage(file='Assets/datetime.png')
undoImage = PhotoImage(file='Assets/undo.png')



#creating First TOOLBAR section
too_bar = Label(root)
too_bar.pack(side=TOP, fill=X)

# created comboboxes
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
textArea = Text(root, yscrollcommand=scrollbar.set, font=('arial', 12), undo=True)
textArea.pack(fill=BOTH, expand=True)
scrollbar.config(command=textArea.yview)

# created status bar
status_bar = Label(root, text='Status Bar')
status_bar.pack(side=BOTTOM)

textArea.bind('<<Modified>>', statusBarFunction)
selectImage = PhotoImage(file='Assets/checked.png')
undoImage = PhotoImage(file='Assets/undo.png')
datetimeImage = PhotoImage(file='Assets/calender.png')

editmenu = Menu(menubar, tearoff=False)
editmenu.add_command(label='Cut', accelerator='Ctrl+X', image=cutImage, compound=LEFT,
                     command=lambda :textArea.event_generate('<Control x>'))
editmenu.add_command(label='Copy', accelerator='Ctrl+C', image=copyImage, compound=LEFT,
                     command=lambda :textArea.event_generate('<Control c>'))
editmenu.add_command(label='Paste', accelerator='Ctrl+V', image=pasteImage, compound=LEFT,
                     command=lambda :textArea.event_generate('<Control v>'))
editmenu.add_command(label='Clear', accelerator='Ctrl+Alt+X', image=clearImage, compound=LEFT,
                     command=lambda :textArea.delete(0.0, END))
editmenu.add_command(label='Find', accelerator='Ctrl+F', image=findImage, compound=LEFT, command=find)
editmenu.add_command(label='Select All', accelerator='Ctrl+A', image=selectImage, compound=LEFT)
editmenu.add_command(label='Date/Time', accelerator='Ctrl+D', image=datetimeImage, compound=LEFT,
                     command=date_time)
menubar.add_cascade(label='Edit', menu=editmenu)
editmenu.add_command(label='Undo', accelerator='Ctrl+Z', image=undoImage, compound=LEFT)


#creating VIEW menu section
show_toolbar = BooleanVar()
show_statusbar= BooleanVar()

toolImage = PhotoImage(file='Assets/tool_bar.png')
statusImage = PhotoImage(file='Assets/status_bar.png')

viewmenu = Menu(menubar, tearoff=False)
viewmenu.add_checkbutton(label='Tool Bar', variable=show_toolbar, onvalue=True, offvalue=False, image=toolImage,
                         compound=LEFT, command=toolbarFunc)
show_toolbar.set(True)
viewmenu.add_checkbutton(label='status Bar', variable=show_statusbar, onvalue=True, offvalue=False, image=statusImage,
                         compound=LEFT, command=statusbarFunc)
show_statusbar.set(True)
menubar.add_cascade(label='View', menu=viewmenu)

#creating THEME menu section
thememenu = Menu(menubar, tearoff=False)
menubar.add_cascade(label='Theme', menu=thememenu)

theme_choice = StringVar()
lightImage = PhotoImage(file='Assets/light_default.png')
darkImage = PhotoImage(file='Assets/dark.png')
pinkImage = PhotoImage(file='Assets/red.png')
monokaiImage = PhotoImage(file='Assets/monokai.png')

thememenu.add_radiobutton(label='Light Default', image=lightImage, variable=theme_choice, compound=LEFT,
                          command=lambda :change_theme('white', 'black'))
thememenu.add_radiobutton(label='Dark', image=darkImage, variable=theme_choice, compound=LEFT,
                          command=lambda :change_theme('gray20', 'white'))
thememenu.add_radiobutton(label='Pink', image=pinkImage, variable=theme_choice, compound=LEFT,
                          command=lambda :change_theme('pink', 'blue'))
thememenu.add_radiobutton(label='Monokai', image=monokaiImage, variable=theme_choice, compound=LEFT,
                          command=lambda :change_theme('orange', 'white'))

root.bind("<Control-o>", open_file)
root.bind("<Control-n>", new_file)
root.bind("<Control-s>", save_file)
root.bind("<Control-Alt-s>", saveas_file)
root.bind("<Control-q>", iexit)
root.bind("<Control-p>", printout)
root.bind("<Control-d>", date_time)
root.bind("<Control-f>", find)

root.mainloop()


root.mainloop()    #this method is used to keep window on hold so that user can see it continiously
