import tkinter
from tkinter import *
from PIL import Image, ImageTk
import whiteHouse as wh

def solveCAPTCHA_manually(session, images, word):
    answers = []
    root = Tk()
    root.title("Solve CAPTCHA")
    root.geometry("800x360")
    for i in range(len(images)):
        image = Image.open("temp_images/img" + str(i) + ".png")
        imageData = ImageTk.PhotoImage(image)
        label = tkinter.Label(image=imageData)
        label.image = imageData
        number = tkinter.Label(text=i+1)
        if i<=7:
            label.place(x=100*i, y=0)
            number.place(x=100*i, y=0)
        elif i>7:
            label.place(x=100*(i-8), y=100)
            number.place(x=100*(i-8), y=100)
    label2 = tkinter.Label(root, text="Select " + word).place(x=270,y=200)
    entry = tkinter.Entry(root)
    entry.place(x=270,y=220)
    submitButton = tkinter.Button(root, text="submit",width=10,height=2,command=lambda:[root.destroy(), wh.whiteHouseLogin(session, answers)]).place(x=330,y=240)
    addAnswerButton = tkinter.Button(root, text="add", width=10,height=2,command=lambda:[addAnswer(answers, (entry.get())), entry.delete(0, 'end')]).place(x=240,y=240)
    root.mainloop()

def addAnswer(answers, newAnswer):
    for answer in answers:
        if answer == newAnswer:
            return
    answers.append(int(newAnswer))