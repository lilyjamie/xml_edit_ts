from Tkinter import *
from xml_edit import *
import re
window = Tk()
window.title('xml_config_edit')
window.geometry("500x300")
window.resizable(width=False, height=False)
label1 = Label(window, text="input type, choose in (t2,isdbt)", bg="blue", font=("Arial", 12), width=50, height=2)
label1.pack()
var_e = StringVar()
type_e = Entry(window, show=None, textvariable=var_e, font=("Arial", 12),width=50)
type_e.pack()
var = type_e.get()
label2 = Label(window, text="input xml_file_path in config file", bg="blue", font=("Arial", 12), width=50, height=2)
label2.pack()
var_b = StringVar()
file_e = Entry(window, show=None, textvariable=var_b, font=("Arial", 12),width=50)
file_e.pack()
xml = XmlEdit()


def xml_edit():
    q = type_e.get()
    h = file_e.get()
    if len(h) == 0:
        xml.set_xml_config(q)
    else:
        w = re.split(',', h)
        print w, h, type(h), type(w)
        xml.set_xml_config(q, w)


commit_button = Button(window, text='edit xml, please click me', width=64, command=xml_edit)
commit_button.pack()
window.mainloop()