# db_login.py
# main file
from tkinter import Tk
import ui_form   # ui window code

root = Tk()
root.state("zoomed")   # make main root window full screen
root.withdraw()   # hide initially

if __name__ == "__main__":
    ui_form.set_root(root)   # share root with ui_form
    ui_form.open_login()     # start with login window
    root.mainloop()
