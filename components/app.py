""" Gui class used for the covid simulation """

import tkinter as tk
import threading
from pathlib import Path
from .markov import Markov

class App:
    def __init__(self):
        """ initialization for the app class """

        self.app = tk.Tk()
        self.app.title("Covid Simulator")

        self.bus = tk.PhotoImage(file = image_loader("bus.png"))
        self.hospital = tk.PhotoImage(file = image_loader("hospital.png"))
        self.house = tk.PhotoImage(file = image_loader("house.png"))
        self.store = tk.PhotoImage(file = image_loader("shopping_cart.png"))

        self.width = 900
        self.height = 350

        frame = tk.Frame(self.app)
        frame.pack()

        self.canvas = tk.Canvas(frame, bg="white", width = self.width, height = self.height)
        self.canvas.pack()

        self.insert_text_box()
        self.insert_icons()
        self.insert_button()        

        self.app.mainloop()

    def insert_button(self):
        """ method used for adding the start button """

        start_btn = tk.Button(text = "Start Simulation")
        start_btn["command"] = self.simulate

        self.canvas.create_window(775, 300, window = start_btn)

    def insert_icons(self):
        """ method used for adding the graphical location nodes """

        #Row 1
        self.canvas.create_image(100, 100, image= self.house, tags = "house_1")
        self.canvas.create_image(250, 100, image= self.house, tags = "house_2")
        self.canvas.create_image(400, 100, image= self.house, tags = "house_3")
        self.canvas.create_image(550, 100, image= self.house, tags = "house_4")
        
        #Row 2
        self.canvas.create_image(100, 250, image= self.bus, tags = "bus")
        self.canvas.create_image(250, 250, image= self.hospital, tags = "hospital")
        self.canvas.create_image(400, 250, image= self.store, tags = "store")
        self.canvas.create_image(550, 250, image= self.house, tags = "house_5")

        self.insert_icon_text()

    def insert_icon_text(self):
        """ method used for inserting text inside each node """
        
        #Row 1
        self.node_text(100, 100, "house_1_txt")
        self.node_text(250, 100, "house_2_txt")
        self.node_text(400, 100, "house_3_txt")
        self.node_text(550, 100, "house_4_txt")

        #Row 2
        self.node_text(100, 250, "bus_txt")
        self.node_text(250, 250, "hospital_txt")
        self.node_text(400, 250, "store_txt")
        self.node_text(550, 250, "house_5_txt")

    def insert_text_box(self):
        """ method used for inserting text box where total/infected/cured/death/suceptible status will be shown """

        text = "Total: 0\nSusceptible: 0\nInfected: 0\nCured: 0\nDead: 0"

        self.canvas.create_rectangle(650, 0, self.width, self.height, fill="#FFE6CC", outline="")
        self.canvas.create_text(660, self.height/2.5, text=text, tag = "movement_log", fill="black", anchor="w", font="Times 20")

    def set_text_box(self, values: list):
        """ method used for setting new text for the text box """
        
        text = "Total: %d\nSusceptible: %d\nInfected: %d\nCured: %d\nDead: %d" %(values[0], values[1], values[2], values[3], values[4]) 

        txt_len = self.canvas.itemcget("movement_log", "text")
        self.canvas.dchars("movement_log", 0, len(txt_len))
        self.canvas.insert("movement_log", 0, text)

    def node_text(self, x, y, tag):
        """ method for initializing text in nodes """
    
        text = "T: 0\nS: 0\nI: 0\nC: 0\nD: 0"
        self.canvas.create_text(x+52, y, text=text, tag=tag, fill="black", anchor="w")

    def set_node_text(self, tag: str, values: list):
        """ method used for setting new text for the node text box """

        text = "T: %d\nS: %d\nI: %d\nC: %d\nD: %d" %(values[0], values[1], values[2], values[3], values[4])
        txt_len = self.canvas.itemcget(tag, "text")
        self.canvas.dchars(tag, 0, len(txt_len))
        self.canvas.insert(tag, 0, text)

    def simulate(self):
        """ method for the inizialization of the simulation after button has been clicked """
        print("test")
        m = Markov()
        self.run(m)

    def run(self, m):
        values = [m.city.total, m.city.susceptible, m.city.infected, m.city.recovered, m.city.death]
        self.set_text_box(values)
        
        # for i in m.city.nodes:
        #     self.set_node_text(i.tag, [i.])

        m.run()
        self.app.after(2000, lambda: self.run(m))
        


def image_loader(image_name):
    """ method used for the image loading """

    image_folder = Path("components/images/100")
    return (image_folder/image_name)