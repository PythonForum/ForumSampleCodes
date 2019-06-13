import tkinter as tk
 
 
class MainFrame(tk.Frame):
 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.entry1 = tk.Entry(self.master)
        self.entry1.pack()
        self.entry2 = tk.Entry(self.master)
        self.entry2.pack()
        self.entry3 = tk.Entry(self.master)
        self.entry3.pack()
        self.entry1.bind('<Return>', self.on_entry1_return)
        self.entry2.bind('<Return>', self.on_entry2_return)
 
    def on_entry1_return(self, event):
        self.entry2.focus_set()
 
    def on_entry2_return(self, event):
        self.entry3.focus_set()
 
 
if __name__ == '__main__':
    app = tk.Tk()
    main_frame = MainFrame()
    app.mainloop()