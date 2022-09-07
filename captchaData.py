from w3lib.url import parse_data_uri
import imagehash as ih
from PIL import Image
from os import listdir, makedirs, path
from shutil import copy2

def writeImages(images):
    pathName = "temp_images/imgZ.png"
    makedirs(path.dirname(pathName), exist_ok=True)
    for i in range(len(images)):
        img1 = parse_data_uri(images[i])
        data = img1[2]
        with open("temp_images/img{0}.png".format(i), "wb") as f:
            f.write(data)

def checkImages():
    answers2 = {}
    for i in range(len(listdir("temp_images"))):
        exists = False
        if list(Image.open('temp_images/img{0}.png'.format(i)).getdata())[0] == (0, 0, 0, 0):
            print("bad image/session", i)
            continue
        for y in range(len(listdir("images"))):
            a = ih.average_hash(Image.open('temp_images/img{0}.png'.format(i)))
            b = ih.average_hash(Image.open('images/img{0}.png'.format(y)))
            #print(a, "ya", b, "diff", (a-b))
            #print("comparing image temp:", i, "with final:", y)
            if a - b < 5:
                #print("image already exists")
                exists = True
                answers2[str(i)] = str(y)
                break
        if not exists:
            copy2('temp_images/img{0}.png'.format(i), 'images/img' + str(len(listdir("images"))) + ".png")
            print("new image out of 1-15:", (i+1))
    print(answers2)

def checkWords(word):
    with open("list_of_words.txt", "r") as file:
        words = file.read()
    with open("list_of_words.txt", "a") as f:
        if word not in words:
            print("new word: ", word)
            f.write(word + "\n")