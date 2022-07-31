from asyncio import base_tasks
from contextlib import nullcontext
from tkinter import *
import json
from PIL import Image, ImageTk
import requests
from io import BytesIO
from random import randint
import threading
from TikTokLive import TikTokLiveClient
from TikTokLive.types.events import CommentEvent, ConnectEvent, LikeEvent
import time
import pyglet

# Import font
pyglet.font.add_file('./font/MouseMemoirs-Regular.ttf')

# Battle canvas, top rectangle, top rectangle info, bottom rectangle, bottom rectangle info
# winner text, upcoming text
canvasRefs = []
pause = True
line = 225

def check_line():
    if line < 0:
        print(f"Winner is {canvasRefs[4]['name']}!")
        canvasRefs[0].itemconfig(canvasRefs[5], text=f"{canvasRefs[4]['name']} wins!", state='normal')
    elif line > 450:
        print(f"Winner is {canvasRefs[2]['name']}!")
        canvasRefs[0].itemconfig(canvasRefs[5], text=f"{canvasRefs[2]['name']} wins!", state='normal')

    else:
        return
    global pause
    pause = True
    time.sleep(3)
    reset_canvas()


def reset_canvas():
    canvasRefs[2] = grabRandomRectangleInfo()
    canvasRefs[4] = grabRandomRectangleInfo()

    while canvasRefs[2]['name'] == canvasRefs[4]['name']:
        print(canvasRefs[2]['name'], canvasRefs[4]['name'])
        canvasRefs[4] = grabRandomRectangleInfo()

    canvasRefs[0].itemconfig(canvasRefs[6], text=f"Upcoming: {canvasRefs[2]['name']} vs {canvasRefs[4]['name']}!", state='normal')
    time.sleep(3)
    
    canvasRefs[0].itemconfig(canvasRefs[1], fill=canvasRefs[2]['color'])
    canvasRefs[0].coords(canvasRefs[1], 0, 0, 355, 225)

    canvasRefs[0].itemconfig(canvasRefs[3], fill=canvasRefs[4]['color'])
    canvasRefs[0].coords(canvasRefs[3], 0, 225, 355, 450)

    canvasRefs[0].itemconfig(canvasRefs[5], state='hidden')
    canvasRefs[0].itemconfig(canvasRefs[6], state='hidden')

    global pause, line
    line = 225
    pause = False

def moveUp():
    if len(canvasRefs) != 7:
        print("Cannot move up, canvas refs length not 7")
    elif pause is True:
        print("Cannot move up, moving is paused")
    else:
        x0, y0, x1, y1 = canvasRefs[0].coords(canvasRefs[1])
        canvasRefs[0].coords(canvasRefs[1], x0, y0, x1, y1 - 20)
        x0, y0, x1, y1 = canvasRefs[0].coords(canvasRefs[3])
        canvasRefs[0].coords(canvasRefs[3], x0, y0 - 20, x1, y1)
        global line
        line-=20
        check_line()

def moveDown():
    if len(canvasRefs) != 7:
        print("Cannot move down, canvas refs length not 7")
    elif pause is True:
        print("Cannot move up, moving is paused")
    else:
        x0, y0, x1, y1 = canvasRefs[0].coords(canvasRefs[1])
        canvasRefs[0].coords(canvasRefs[1], x0, y0, x1, y1 + 20)
        x0, y0, x1, y1 = canvasRefs[0].coords(canvasRefs[3])
        canvasRefs[0].coords(canvasRefs[3], x0, y0 + 20, x1, y1)
        global line
        line+=20
        check_line()

# Grabs new, random info from data/*.json. Entries NEED a name, color (hex), and a valid image URL
def grabRandomRectangleInfo():
    f = open('data/pokemon.json')
    data = json.load(f)
    random_index = randint(0, len(data) - 1)
    return {"name": data[random_index]["name"],
            "color": data[random_index]["color"],
            "imgUrl": data[random_index]["imgUrl"]}


def start_connection():
    client: TikTokLiveClient = TikTokLiveClient(unique_id="@shakeoutny")

    @client.on("connect")
    async def on_connect(_: ConnectEvent):
        print("Connected to Room ID:", client.room_id)
        global pause
        pause = False

    @client.on("comment")
    async def on_comment(event: CommentEvent):
        print(f"{event.user.nickname} -> {event.comment}")
        moveUp()

    @client.on("like")
    async def on_like(event: LikeEvent):
        print(f"{event.user.nickname} hit like!")
        moveDown()
        
    client.run()

def start_thread():
    t = threading.Thread(target=start_connection)
    t.start()

def main_thread():
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
    canvasRefs.append(battleCanvas)

    # Top rectangle
    topRectangle = battleCanvas.create_rectangle(0, 0, 355, 225, fill=rec1Info['color'], outline="")
    canvasRefs.append(topRectangle)
    canvasRefs.append(rec1Info)

    # Bottom rectangle
    bottomRectangle = battleCanvas.create_rectangle(0, 225, 355, 450, fill=rec2Info['color'], outline="")
    canvasRefs.append(bottomRectangle)
    canvasRefs.append(rec2Info)

    # Create winner text
    winnerText = battleCanvas.create_text(130, 225, text="Placeholder", fill="black", font=('MouseMemoirs', 20, "bold"), state='hidden')
    canvasRefs.append(winnerText)

    # Create upcoming text
    upcomingText = battleCanvas.create_text(150, 245, text="Upcoming", fill="black", font=('MouseMemoirs', 10, "bold"), state='hidden')
    canvasRefs.append(upcomingText)

    # Create buttons (for prod, apply option state='hidden')
    buttonAdjustUp = Button(root, text="move up", command=moveUp)
    buttonAdjustUp.pack()

    buttonAdjustDown = Button(root, text="move down", command=moveDown)
    buttonAdjustDown.pack()

    root.mainloop()


threading.Thread(target=main_thread).start()
start_connection()