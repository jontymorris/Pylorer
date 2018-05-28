from tkinter import *
from tkinter import filedialog

import os, shutil, zipfile


# Centers a window on the screen
def center_window(window, width: str, height: str):
    x = (window.winfo_screenwidth() - width) // 2
    y = (window.winfo_screenheight() - height) // 2
    window.geometry("{}x{}+{}+{}".format(width, height, x, y))


class DialogueWindow:

    def __init__(self, title: str, message: str):
        # Init the window
        self.root = Tk()
        self.root.title(title)
        self.root.resizable(0, 0)
        self.root.tk.call("tk", "scaling", 2.0)
        
        center_window(self.root, 250, 100)

        # Create the message
        self.message_label = Label(self.root, text=message, wraplength=200)
        self.message_label.pack()

        self.root.focus_force()
        self.root.mainloop()


class OptionsPanel:

    def __init__(self, window):
        self.window = window

        # Init the frame
        self.frame = Frame(window.root)

        Label(self.frame, text="File Options\n").grid(row=0, column=0)

        # Create all of the buttons
        self.move_button = Button(self.frame, text="Move", command=self.move_file)
        self.delete_button = Button(self.frame, text="Delete", command=self.delete_file)
        self.extract_button = Button(self.frame, text="Extract", command=self.extract_file)

        self.buttons = [
            self.move_button,
            self.delete_button,
            self.extract_button
        ]

        # Add the buttons to the window
        for i in range(0, len(self.buttons)):
            self.buttons[i].grid(row=i+1, column=0, sticky=EW)

        self.set_buttons_state(DISABLED)

        self.frame.grid(row=2, column=1, sticky=NSEW, padx=30)
    
    # Changes all of the file options buttons state
    def set_buttons_state(self, state: str):
        for button in self.buttons:
            button["state"] = state
    
    # Enables the buttons when a file is selected
    def file_selected(self, is_zip: bool):
        self.set_buttons_state(ACTIVE)

        if not is_zip:
            self.extract_button["state"] = DISABLED
    
    # Deletes the currently selected file
    def delete_file(self):
        try:
            selected_file = self.window.get_selected_file()

            if os.path.isfile(selected_file):
                os.remove(selected_file)
            else:
                shutil.rmtree(selected_file)
            
            self.window.update_files_list()
        except:
            DialogueWindow("Error", "Something went wrong.")
    
    # Extracts the currently selected file to the current directory
    def extract_file(self):
        try:
            selected_file = self.window.get_selected_file()
            
            selected_zip = zipfile.ZipFile(selected_file, "r")
            selected_zip.extractall(self.window.explorer.current_dir)
            selected_zip.close()

            self.window.update_files_list()
        except:
            DialogueWindow("Error", "Something went wrong.")
    
    # Moves the currently selected file
    def move_file(self):
        try:
            selected_file = self.window.get_selected_file()
            destination = filedialog.askdirectory()

            if destination:
                shutil.move(selected_file, destination)
                self.window.update_files_list()
        except:
            DialogueWindow("Error", "Something went wrong.")


class Explorer:

    def __init__(self):
        self.current_dir = os.path.abspath("/")
    
    # Returns the contents of the current directory
    def get_files(self):
        try:
            return os.listdir(self.current_dir)
        except PermissionError:
            DialogueWindow("Permission Error", "You do not have permission to view that folder.")
    
    # Returns whether an item in the current directory is a file
    def is_file(self, name: str):
        return os.path.isfile(os.path.join(self.current_dir, name))
    
    # Changes the directory completely
    def set_dir(self, path: str):
        abs_path = os.path.abspath(path)

        if os.path.isdir(abs_path):
            self.current_dir = abs_path

        else:
            os.startfile(path)
    
    # Opens a file or folder in the current directory.
    def open_file(self, name: str):
        path = os.path.join(self.current_dir, name)
        if self.is_file(name):
            os.startfile(path)
        else:
            self.current_dir = path
    
    # Returns the parent dir of the current dir
    def get_parent_dir(self):
        return os.path.dirname(self.current_dir)
    
    # Checks if a file is a zip
    def is_zip(self, name: str):
        return name.endswith(".zip")

class Window:

    def __init__(self):
        # Init the window
        self.root = Tk()
        self.root.title("Pylorer")
        self.root.resizable(0, 0)
        self.root.tk.call("tk", "scaling", 2)

        center_window(self.root, 365, 350)
        
        # Add the level button
        self.level_button = Button(self.root, text="Up one level", command=self.level_button_command)
        self.level_button.grid(row=0, column=0, columnspan=2, sticky=EW)

        # Add the path entry
        self.path_entry = Entry(self.root)
        self.path_entry.grid(row=1, column=0, columnspan=2, sticky=EW)
        self.path_entry.bind("<Return>", self.path_enter)

        # Init the explorer
        self.files_list = Listbox(self.root)
        self.files_list.grid(row=2, column=0)
        self.files_list.bind("<<ListboxSelect>>", self.files_select)
        self.files_list.bind("<Double-1>", self.files_double_click)

        # Add the file options frame
        self.options_panel = OptionsPanel(self)

        # Init the 
        self.explorer = Explorer()
        self.update_files_list()

        self.root.mainloop()
    
    # Displays all of the files in the current directory inside the explorer list box
    def update_files_list(self):
        self.path_entry.delete(0, END)
        self.path_entry.insert(0, self.explorer.current_dir)
        self.path_entry.xview_moveto(1)

        self.files_list.delete(0, END)
        self.options_panel.set_buttons_state(DISABLED)

        try:
            files = self.explorer.get_files()
            for i in range(0, len(files)):
                self.files_list.insert(END, files[i])

                if self.explorer.is_file(files[i]):
                    self.files_list.itemconfig(i, {"bg": "#e1ffbc"})
                else:
                    self.files_list.itemconfig(i, {"bg": "#ffd3bc"})
        except FileNotFoundError:
            DialogueWindow("Path Error", "That path does not exist.")
    
    # Updates the path
    def path_enter(self, event):
        try:
            self.explorer.set_dir(self.path_entry.get())
            self.update_files_list()
        except FileNotFoundError:
            DialogueWindow("File Error", "The file wasn't found.")
        except:
            DialogueWindow("Error", "Something went wrong.")
    
    # Opens the selected item
    def files_double_click(self, event):
        selected_file = self.files_list.selection_get()
            
        self.explorer.open_file(selected_file)
        self.update_files_list()
    
    # Called when a file/folder is selected in the explorer
    def files_select(self, event):
        try:
            selected_file = self.files_list.selection_get()
            self.options_panel.file_selected(self.explorer.is_zip(selected_file))
        except TclError:
            pass

    # Goes up one level on the path
    def level_button_command(self):
        self.explorer.set_dir(self.explorer.get_parent_dir())
        self.update_files_list()
    
    # Gets the currently selected file
    def get_selected_file(self):
        return os.path.join(self.explorer.current_dir, self.files_list.selection_get())


if __name__ == "__main__":
    Window()