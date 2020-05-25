""" Gui class used for the covid simulation """

import tkinter as tk
import threading
from pathlib import Path
from PIL import ImageTk, Image

from .markov import Markov

class App:
    def __init__(self):
        """ initialization for the app class """

        self.app = tk.Tk()
        self.app.title("Covid Simulator")

        self.width = 950
        self.height = 350

        frame = tk.Frame(self.app)
        frame.pack()

        self.canvas = tk.Canvas(frame, bg="white", width = self.width, height = self.height)
        self.canvas.pack()

        bus = image_loader("bus.png")
        hospital = image_loader("hospital.png")
        house = image_loader("house.png")
        store = image_loader("shopping_cart.png")

        self.insert_icons(bus, hospital, house, store)

        self.insert_box()
        self.insert_button()        

        self.app.mainloop()

    def insert_button(self):
        """ method used for adding the start button """

        self.start_btn = tk.Button(text = "Start Simulation")
        self.start_btn["command"] = self.start

        self.stop_btn = tk.Button(text = "Stop Simulation")
        self.stop_btn["state"] = "disabled"
        self.stop_btn["command"] = self.stop

        self.canvas.create_window(730, 310, window = self.start_btn)
        self.canvas.create_window(870, 310, window = self.stop_btn)

    def insert_icons(self, bus, hospital, house, store):
        """ method used for adding the graphical location nodes """

        #Row 1
        self.canvas.create_image(100, 100, image= house, tags = "house_1")
        self.canvas.create_image(250, 100, image= house, tags = "house_2")
        self.canvas.create_image(400, 100, image= house, tags = "house_3")
        self.canvas.create_image(550, 100, image= house, tags = "house_4")
        
        #Row 2
        self.canvas.create_image(100, 250, image= bus, tags = "bus")
        self.canvas.create_image(250, 250, image= hospital, tags = "hospital")
        self.canvas.create_image(400, 250, image= store, tags = "store")
        self.canvas.create_image(550, 250, image= house, tags = "house_5")

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

    def insert_box(self):
        """ method used for inserting text box where total/infected/cured/death/suceptible status will be shown """

        text = "Acumulated Total\n\nTotal: 0\nSusceptible: 0\nInfected: 0\nCured: 0\nDead: 0"

        self.canvas.create_rectangle(650, 0, self.width, self.height, fill="#FFE6CC", outline="")
        self.canvas.create_text(660, self.height/3, text=text, tag = "movement_log", fill="black", anchor="w", font="Times 15")
        self.insert_sliders()

    def insert_sliders(self):
        self.tot = tk.IntVar()
        self.inf = tk.IntVar()
        
        total_slider = tk.Scale(variable = self.tot, label="total people")
        infected_slider = tk.Scale(variable = self.inf, label="infected people")
        self.sliders = [total_slider, infected_slider]

        for i in self.sliders:
            i["orient"] = tk.HORIZONTAL
            i["bg"] = "#FFE6CC"
            i["length"] = 120
            i["highlightthickness"] = 0     

        self.canvas.create_window(730, 240, window = self.sliders[0])
        self.canvas.create_window(870, 240, window = self.sliders[1])

    def set_text_box(self, values: list):
        """ method used for setting new text for the text box """
        
        text = "Acumulated Total\n\nTotal: %d\nSusceptible: %d\nInfected: %d\nCured: %d\nDead: %d" %(values[0], values[1], values[2], values[3], values[4]) 

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

    def start(self):
        """ method for the inizialization of the simulation after button has been clicked """
        self.start_btn["state"] = "disabled"
        self.start_btn["text"] = "Redo simulation"
        self.stop_btn["state"] = "normal"


            
        total = self.tot.get()
        infected = self.inf.get()

        if (total == 0):
            total = 50
        if (total <= infected):
            total = infected+1
        if (infected == 0):
            infected = 5

        self.sliders[0].set(total)
        self.sliders[1].set(infected)

        for i in self.sliders:
            i["state"] = "disabled"

        m = Markov(total, infected)

        self.loop(m)

    def loop(self, m):
        values = [m.city.total, m.city.susceptible, m.city.infected, m.city.recovered, m.city.death]
        self.set_text_box(values)
        
        for i in m.city.nodes:
            self.set_node_text(i.tag, [i.total, i.susceptible, i.infected, i.recovered, i.death])

        m.run()
        self._job = self.app.after(2000, lambda: self.loop(m))
    
    def stop(self):
        self.start_btn["state"] = "normal"
        self.stop_btn["state"] = "disabled"

        for i in self.sliders:
            i["state"] = "normal"
            i.set(0)

        self.app.after_cancel(self._job)
        self._job=None

def image_loader(image_name):
    """ method used for the image loading """

    image_folder = Path("components/images/100")
    img = ImageTk.PhotoImage(Image.open(image_folder/image_name))
    return (img)