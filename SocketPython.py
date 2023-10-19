import socketio
import asyncio
import time
import board
import neopixel

numberLedByLine = 168
numberLed = numberLedByLine*2
pixels = neopixel.NeoPixel(board.D21, numberLed, brightness=1, auto_write=False)

color = (0,0,255)
pixels.fill(color)
pixels.show()

fct = 0

url = "https://potter.digital-wizards.ovh/api"


sio = socketio.Client()

def ChangeColor(Data):
    global color
    global fct
    if Data == "red":
        color = (255,0,0)
    elif Data == "green":
        color = (0,255,0)
    elif Data == "blue":
        color = (0,0,255)
    elif Data == "yellow":
        color = (255,255,0)
    elif Data == "purple":
        color = (128,0,128)
    elif Data == "white":
        color = (255,255,255)
    elif Data == "cyan":
        color = (0,255,255)
    elif Data == "magenta":
        color = (255,0,255)
    elif Data == "pink":
        color = (255,0,127)
    elif Data == "orange":
        color = (255,165,0)
    elif Data == "switch":
        fct = Switch
    elif Data == "load":
        fct = Load
    elif Data == "fill":
        fct = Fill
 
def Switch():
    global color
    global numberLed
    global pixels
    # on 1/2 of the led
    for i in range(numberLed):
        if i%2 == 0:
            pixels[i] = color
        else:
            pixels[i] = (0,0,0)
    pixels.show()
    time.sleep(0.5)
    for i in range(numberLed):
        if i%2 == 0:
            pixels[i] = (0,0,0)
        else:
            pixels[i] = color
    pixels.show()
    time.sleep(0.5)

def Load():
    global color
    global numberLed
    global pixels
    pixels.fill((0,0,0))
    pixels.show()
    for i in range(numberLed/2):
        pixels[i] = color
        pixels[(numberLed/2)+i] = color
        pixels.show()
        time.sleep(0.01)

def Fill():
    global color
    global numberLed
    global pixels
    pixels.fill(color)
    pixels.show()
      
def main():
    global sio
    global fct
    fct = Fill
    while True:
        if not sio.connected:
            sio.connect(url)
            time.sleep(5)
        
        while sio.connected:
            try:
                fct()
            except:
                print("error")
  
@sio.event
def connect():
    sio.emit("rpi:server:init","");
    print('connect ')

@sio.event
def disconnect():
    print('disconnect ')

@sio.on("hashtags")
def on_message(data):
    for i in data:
        ChangeColor(i)
        print(i)



main()

