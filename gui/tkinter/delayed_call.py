import tkinter as tk
import time
 
class MainFrame(tk.Frame):
 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label = tk.Label(self, text='Player 1 turn')
        self.label.pack()
        self.button = tk.Button(
            self, text='Player 1 Move', command=self.on_button)
        self.button.pack(pady=15)
        self.pack()
 
    def on_button(self):
        print('Button clicked')
        self.label['text'] = 'player 2 thinking'
        self.button['state'] = 'disabled'
        self.after(3000, self.delayed_player_2)
 
 
    def delayed_player_2(self):
        self.label['text'] = 'player 2 moving'
        self.after(1000, self.player_2_finsihed)
 
    def player_2_finsihed(self):
        self.label['text'] = 'player 1 turn'
        self.button['state'] = 'normal'
 
 
if __name__ == '__main__':
    app = tk.Tk()
    main_frame = MainFrame()
    app.mainloop()