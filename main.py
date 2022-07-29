from tkinter import *
import json
from PIL import Image, ImageTk
import requests
from io import BytesIO
from random import randint


# Grabs new, random info from data/*.json. Entries NEED a name, color (hex), and a valid image URL
def grabRandomRectangleInfo():
    f = open('data/pokemon.json')
    data = json.load(f)
    random_index = randint(0, len(data) - 1)
    return {"name": data[random_index]["name"],
            "color": data[random_index]["color"],
            "imgUrl": data[random_index]["imgUrl"]}


def moveUp():
    x0, y0, x1, y1 = battleCanvas.coords(topRectangle)
    battleCanvas.coords(topRectangle, x0, y0, x1, y1 - 20)
    x0, y0, x1, y1 = battleCanvas.coords(bottomRectangle)
    battleCanvas.coords(bottomRectangle, x0, y0 - 20, x1, y1)

def moveDown():
    x0, y0, x1, y1 = battleCanvas.coords(topRectangle)
    battleCanvas.coords(topRectangle, x0, y0, x1, y1 + 20)
    x0, y0, x1, y1 = battleCanvas.coords(bottomRectangle)
    battleCanvas.coords(bottomRectangle, x0, y0 + 20, x1, y1)

# Grab initial rectangle info
rec1Info = grabRandomRectangleInfo()
rec2Info = grabRandomRectangleInfo()

# Make sure they're not the same
while rec2Info['name'] == rec1Info['name']:
    print(rec1Info['name'], rec2Info['name'])
    rec2Info = grabRandomRectangleInfo()

# Create root
root = Tk()
root.title("TikTok Royale")
root.iconbitmap("icon.ico")
root.geometry("400x750")

# Create battle canvas
battleCanvas = Canvas(root, width=350, height=450, bg="white")
battleCanvas.pack()

# Top rectangle
topRectangle = battleCanvas.create_rectangle(0, 0, 355, 225, fill=rec1Info['color'], outline="")

# Bottom rectangle
bottomRectangle = battleCanvas.create_rectangle(0, 225, 355, 450, fill=rec2Info['color'], outline="")

buttonAdjustUp = Button(root, text="move up", command=moveUp)
buttonAdjustUp.pack()

buttonAdjustDown = Button(root, text="move down", command=moveDown)
buttonAdjustDown.pack()

root.mainloop()