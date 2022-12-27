from collections import deque
import re
import threading
import tkinter as tk
import math

from click import command

class NeoPixel():
    def __init__(self, pin, led_count):
        self.pin = pin
        self.led_count = led_count
        self.messageQueue = deque()

        x = threading.Thread(target=self.__tkinter_thread)
        x.start()

    def __setitem__(self, item, value):
        """
        set a specifc index to a tuple rgb value
        """
        self.messageQueue.append("set,{0}{1}".format(item,value))
    def __setitem(self, index, rgb):
        self.led_object_array[index].configure(bg=self.__tuple_to_hex(rgb))
    def __tuple_to_hex(self, rgb):
        hex = "#{0:02X}{1:02X}{2:02X}".format(rgb[0],rgb[1],rgb[2])
        return hex.lower()
    
    def __fill(self,rgb):
        """
        sets whole strip to one color
        Takes a RGB tuple
        """
        for led in self.led_object_array:
            led.configure(bg=self.__tuple_to_hex(rgb))

    def __clear(self):
        """
        sets strip to black. No arguments
        """
        for led in self.led_object_array:
            led.configure(bg="#000000")
    def clear(self):
        self.messageQueue.append("clear")

    def fill(self, rgb):
        self.messageQueue.append("fill {}".format(rgb))

    def show(self):
        return

    def __tkinter_thread(self):
        window = tk.Tk()

        rows = math.ceil(self.led_count / 10)
        self.led_object_array = []

        for led in range(self.led_count):
            row = math.floor(led / 10)
            column = led % 10
            self.led_object_array.append( tk.Entry(window, width=5,bg="#000000") )
            self.led_object_array[led].grid(row=row,column=column)
            self.led_object_array[led].insert(led, "")

        while True:
            try:
                command = self.messageQueue.popleft()
                if command.find("clear") > -1:
                    self.__clear()
                elif command.find("fill") > -1:
                    parsed = command.replace("(",",").replace(")",",").replace(" ", "").split(",")[1:4]
                    rgb = (int(parsed[0]),int(parsed[1]),int(parsed[2]))
                    self.__fill(rgb)
                elif command.find("set") > -1:
                    parsed = command.replace("(",",").replace(")",",").replace(" ", "").split(",")[1:5]
                    rgb = (int(float(parsed[1])),int(float(parsed[2])),int(float(parsed[3])))
                    self.__setitem(int(parsed[0]), rgb)
            except IndexError:
                pass
            window.update()