from tkinter import *
import os


def center_window(window, width, height):
    x = (window.winfo_screenwidth() - width) // 2
    y = (window.winfo_screenheight() - height) // 2
    window.geometry("{}x{}+{}+{}".format(width, height, x, y))


class DialogueWindow:

    def __init__(self, title, message):
        # Init the window
        self.root = Tk()
        self.root.title(title)
        self.root.resizable(0, 0)
        self.root.focus_force()
    
        center_window(self.root, 250, 100)

        # Create the message
        self.message_label = Label(self.root, text=message)
        self.message_label.pack()

        self.root.mainloop()


class OptionsPanel:

    def __init__(self, window):
        self.window = window

        # Init the frame
        self.frame = Frame(window.root)

        # Create the 'file options' label
        self.info_label = Label(self.frame, text="File options\n")
        self.info_label.grid(row=0, column=0)

        # Create all of the buttons
        self.open_button = Button(self.frame, text="Open")
        self.open_button.grid(row=1, column=0, sticky=EW)

        # Add buttons to a list for easy state changing
        self.buttons = [
            self.open_button
        ]
        
        self.set_buttons_state(DISABLED)

        self.frame.grid(row=0, column=1, sticky=NSEW, padx=30)
    
    def set_buttons_state(self, state):
        for button in self.buttons:
            button["state"] = state


class Explorer:

    def __init__(self):
        self.current_dir = "/"
    
    def get_files(self):
        return os.listdir(self.current_dir)
    
    def is_file(self, name):
        return os.path.isfile(os.path.join(self.current_dir, name))


class ExplorerPanel:

    def __init__(self, window):
        self.window = window
        self.explorer = Explorer()

        # Init the frame
        self.frame = Frame(window.root)

        # Create the path components
        self.path_entry = Entry(self.frame)
        self.path_entry.grid(row=0, column=0)
        self.path_entry.bind("<Return>", self.path_entry_callback)

        # Create the explorer
        self.files_box = Listbox(self.frame)
        self.files_box.grid(row=2, column=0, pady=15)
        
        self.update_files()

        self.frame.grid(row=0, column=0)
    
    def update_files(self):
        self.path_entry.delete(0, END)
        self.path_entry.insert(0, self.explorer.current_dir)

        self.files_box.delete(0, END)

        try:
            files = self.explorer.get_files()
            for i in range(0, len(files)):
                self.files_box.insert(END, files[i])

                if self.explorer.is_file(files[i]):
                    self.files_box.itemconfig(i, {"bg": "#e1ffbc"})
                else:
                    self.files_box.itemconfig(i, {"bg": "#ffd3bc"})
        except FileNotFoundError:
            DialogueWindow("Warning", "That path does not exist.")
    
    def path_entry_callback(self, event):
        try:
            self.explorer.current_dir = os.path.abspath(self.path_entry.get())
            self.update_files()
        except:
            DialogueWindow("Error", "Something went wrong :(")


class Window:

    def __init__(self):
        # Init the window
        self.root = Tk()
        self.root.title("Pylorer")

        center_window(self.root, 300, 200)

        # Create the panels
        self.explorer_panel = ExplorerPanel(self)
        self.options_panel = OptionsPanel(self)

        self.root.mainloop()


if __name__ == "__main__":
    Window()