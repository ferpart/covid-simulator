import tkinter as tk

class App:
    def __init__(self):
        self.app = tk.Tk()
        self.app.title("Covid Simulator")
        self.width = 800
        self.height = 400

        frame = tk.Frame(self.app)
        frame.pack()

        self.canvas = tk.Canvas(frame, bg="white", width = self.width, height = self.height)
        self.canvas.pack()
        
        self.app.mainloop()

