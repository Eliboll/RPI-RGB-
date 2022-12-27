import time
import board
import neopixel
import threading
import random

#----------------------------------------------------------------------
#   All light effects utilize threading. This is to allow them to be
#   efficently stopped when a new request is received, instead of
#   having to wait until the previous sequence is ended
#
#   all threads constatly check the stop flag, and when it goes high,
#   the thread ends what it is currently doing, sets the running thread
#   flag to false, then ends. Whatever call set the stop flag to true
#   waits until the running flag goes to false, then spins off a new
#   thread for whatever effect, repeating the whole process
#----------------------------------------------------------------------

class rgb():
    """
    Class for controlling rgb. Functions:
    full_rotate:    cycles through the color wheel
    set_stop:       stops any animations occuring
    set_a_tile      sets any index to any RGB value
    random_fill     randomly selects an unselected tile and fills and
                    fills it until no tiles are unfilled, then repeats
                    in reverse
    fill            sets the entire strip to one color
    uniqlo          moves repeating sections of a color through the strip
    rainbow_cycle   cycles entire strip through RGB colorwheel

    """
    def __init__(self, led_count, pin=board.D18, brightness=0.50, max_brightness=.8):
        self.__led_count = led_count
        self.__strip = neopixel.NeoPixel(pin, self.__led_count,)# auto_write=False)
        self.__stop_flag = False
        self.__running_thread = False
        self.__thread = None
        self.brightness=brightness
        self.max_brightness= max_brightness

    def __full_rotate_slave(self,timing=.01):
        self.__running_thread = True
        while self.__stop_flag == False:
            # Red to Amber
            for g in range(255):
                self.__strip.fill(self.__rgb_normalizer((255,g,0)))
                if self.__stop_flag:
                    self.__stop_flag = False
                    self.__running_thread = False
                    return
                self.__strip.show()
                time.sleep(timing)
            # Amber to Green
            for r in range(255,-1,-1):
                self.__strip.fill(self.__rgb_normalizer((r,255,0)))
                if self.__stop_flag:
                    self.__stop_flag = False
                    self.__running_thread = False
                    return
                self.__strip.show()
                time.sleep(timing)
            # Green to cyan
            for b in range(255):
                self.__strip.fill(self.__rgb_normalizer((0,255,b)))
                if self.__stop_flag:
                    self.__stop_flag = False
                    self.__running_thread = False
                    return
                self.__strip.show()
                time.sleep(timing)
            # Cyan to blue
            for g in range(255,-1,-1):
                self.__strip.fill(self.__rgb_normalizer((0,g,255)))
                if self.__stop_flag:
                    self.__stop_flag = False
                    self.__running_thread = False
                    return
                self.__strip.show()
                time.sleep(timing)
            # Blue to Purple
            for r in range(255):
                self.__strip.fill(self.__rgb_normalizer((r,0,255)))
                if self.__stop_flag:
                    self.__stop_flag = False
                    self.__running_thread = False
                    return
                self.__strip.show()
                time.sleep(timing)
            # Purple to Red
            for b in range(255,-1,-1):
                self.__strip.fill(self.__rgb_normalizer((255,0,b)))
                if self.__stop_flag:
                    self.__stop_flag = False
                    self.__running_thread = False
                    return
                self.__strip.show()
                time.sleep(timing)
        self.__stop_flag = False

    def full_rotate(self):
        """
        Rotates through all possible rgb values
        """
        if self.__running_thread:
            self.__stop_flag = True
            while self.__running_thread:
                time.sleep(0.1)
        self.__thread = threading.Thread(target=self.__full_rotate_slave)
        self.__thread.start()

    def set_stop(self):
        self.__stop_flag = True

    def set_a_tile(self, index, rgb):
        if self.__running_thread:
            self.__stop_flag = True
            while self.__running_thread:
                time.sleep(0.1)
        self.__strip[index] = self.__rgb_normalizer(rgb)
        self.__strip.show()

    def __random_fill(self, rgb):
        self.__running_thread = True
        while self.__stop_flag == False:
            leds = [*range(self.__led_count)] # All leds
            while len(leds) != 0:   #Do until everything is filled
                if self.__stop_flag:
                    self.__stop_flag = False
                    self.__running_thread = False
                    return
                led = random.choice(leds)   #select an LED that isn't filled
                #Gradually increase brightness
                for i in range(1,9):
                    div8 = (rgb[0]/8, rgb[1]/8, rgb[2]/8 )
                    self.__strip[led] = self.__rgb_normalizer((div8[0]*i, div8[1]*i, div8[2]*i ))
                    self.__strip.show()
                    time.sleep(0.05)
                leds.remove(led)        #remove the filled LED from unseleccted list
            leds = [*range(self.__led_count)]
            while len(leds) != 0:
                if self.__stop_flag:
                    self.__stop_flag = False
                    self.__running_thread = False
                    return
                led = random.choice(leds)
                #gradually lower brightness
                for i in range(7,-1,-1):
                    div8 = (rgb[0]/8, rgb[1]/8, rgb[2]/8 )
                    self.__strip[led] = self.__rgb_normalizer((div8[0]*i, div8[1]*i, div8[2]*i ))
                    self.__strip.show()
                    time.sleep(0.05)
                leds.remove(led)

    def random_fill(self, rgb):
        """
        randomly chooses led and fills it with rgb value
        """
        if self.__running_thread:
            self.__stop_flag = True
            while self.__running_thread:
                time.sleep(0.1)
        self.__thread = threading.Thread(target=self.__random_fill, args=(rgb,))
        self.__thread.start()

    def fill(self, rgb):
        if self.__running_thread:
            self.__stop_flag = True
            while self.__running_thread:
                time.sleep(0.1)
        self.__strip.fill(self.__rgb_normalizer(rgb))
        self.__strip.show()
        self.__running_thread = False

    def __uniqlo(self, rgb=(255,0,0),buffer=5,length=3,wait=0.05):
        self.__running_thread = True
        repeat = buffer + length
        while self.__stop_flag == False:
            #loop through all possible variations of LED strip
            for offset in range(repeat):
                #go through entire led strip and check if its index
                #should be on or off
                for index in range(self.__led_count):
                    i = index + offset
                    #Removed for preformance, only at most saves 1/4 second but costs a lot each refresh
                    
                    # if self.__stop_flag:
                    #     self.__stop_flag = False
                    #     self.__running_thread = False
                    #     return
                    if i % repeat < length:
                        self.__strip[index] = self.__rgb_normalizer(rgb)
                    else:
                        self.__strip[index] = 0
                self.__strip.show()
                time.sleep(wait)

    def uniqlo(self, rgb=(255,0,0),buffer=5,length=3,wait=0.05):
        """
        moves sections of colour through strip
        """
        if self.__running_thread:
            self.__stop_flag = True
            while self.__running_thread:
                time.sleep(0.1)
        self.__thread = threading.Thread(target=self.__uniqlo, args=(rgb,buffer,length,wait))
        self.__thread.start()

    def __wheel(self, pos):
        # Input a value 0 to 255 to get a color value.
        # The colours are a transition r - g - b - back to r.
        if pos < 0 or pos > 255:
            return (0, 0, 0)
        if pos < 85:
            return (255 - pos * 3, pos * 3, 0)
        if pos < 170:
            pos -= 85
            return (0, 255 - pos * 3, pos * 3)
        pos -= 170
        return (pos * 3, 0, 255 - pos * 3)

    def __rainbow_cycle(self,wait=0.05):
        self.__running_thread = True
        while self.__stop_flag == False:
            for j in range(255):
                for i in range(self.__led_count):
                    rc_index = (i * 256 // self.__led_count) + j
                    self.__strip[i] = self.__rgb_normalizer(self.__wheel(rc_index & 255))
                if self.__stop_flag:
                    self.__stop_flag = False
                    self.__running_thread = False
                    return
                self.__strip.show()
                time.sleep(wait)

    def rainbow_cycle(self, wait=0.05):
        """
        rotating raibow effect
        """
        if self.__running_thread:
            self.__stop_flag = True
            while self.__running_thread:
                time.sleep(0.1)
        self.__thread = threading.Thread(target=self.__rainbow_cycle, args=(wait,))
        self.__thread.start()

    def __rgb_normalizer(self, rgb):
        """
        Function returns an RGB value normalized to the system brightness
        """
        if self.brightness > self.max_brightness:
            self.brightness= self.max_brightness
        elif self.brightness < 0.0:
            self.brightness=0.0
        r = int(rgb[0] * self.brightness)
        g = int(rgb[1] * self.brightness)
        b = int(rgb[2] * self.brightness)
        return (r,g,b)