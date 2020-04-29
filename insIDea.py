# -*- coding: utf-8 -*-
"""
Created on Sat Nov 30 21:08:25 2019

@author: melhe
"""
import sys, string, os ,glob, cv2 ,os.path
import subprocess
import numpy as np
#import matplotlib.pyplot as plt
import subprocess ,tkinter
import time
import random
import PIL
import io
import pandas
import glob
import os
#from numpy import array
from tkinter import *
from tkinter import messagebox 
from tkinter import filedialog
from PIL import ImageTk, Image, ImageDraw, ImageGrab

window = Tk()
window.geometry("1300x600+50+50")
window.title("insIDea")
window.configure(background='grey')
v = IntVar()
v.set(1) 
def UploadAction(event=None):
    filelist = glob.glob(os.path.join("C:/Users/arcee/darknet/build/darknet/x64/result_img", "*.jpg"))
    for f in filelist:
        os.remove(f)    
    filename = filedialog.askopenfilename()
    global path
    path= filename

#    img = ImageTk.PhotoImage(Image.open(path).resize((409,440), Image.ANTIALIAS))
    img = ImageTk.PhotoImage(Image.open(path), Image.ANTIALIAS)

    panel = Label(window, image=img)
    panel.photo = img
    panel.place(x=270,y=100)
    print('',path)
   
def GenerateAction(event=None):
    print('',path) 
    command = "darknet_no_gpu.exe detector test data/obj.data yolo-obj.cfg backup/yolo-obj_2000.weights %s -dont_show" %(path)
    process = subprocess.Popen(command,cwd="C:/Users/arcee/darknet/build/darknet/x64"
                              , stdout=subprocess.PIPE, shell=True)
    output = process.stdout.readline()
    print(output)
    time.sleep(5)

    predicted_image = "C:/Users/arcee/darknet/build/darknet/x64/predictions.jpg"
#    img = ImageTk.PhotoImage(Image.open(predicted_image).resize((409,440), Image.ANTIALIAS))
    img = ImageTk.PhotoImage(Image.open(predicted_image), Image.ANTIALIAS)
    panel = Label(window, image=img) 
    panel.photo = img
    panel.place(x=270,y=100)
    im = Image.open(path)
    
    pix = im.load()
#    print (im.size)
    height, width = im.size
#    print(width)
#    print(height)
    a1 = 0
    aa1 = 0
    aaa1=0
    for x in range(height):
        for y in range(width):        
#            global r,g,b 
            r,g,b = pix[x,y]
            if(r<10 and g<10 and b<10): #black
                a1 = a1 + 1
                aa1 = aa1+1
                aaa1=aaa1+1
               
    listX = [0 for i in range(a1)]
    listY= [0 for i in range(aa1)]
    listXY= [0 for i in range(aaa1)]
    b_ctr = 0
    for x in range(height):
        for y in range(width):  
            r,g,b = pix[x,y]
            if(r<10 and g<10 and b<10): #black
                listX[b_ctr] = x
                listY[b_ctr] = y
                listXY[b_ctr] = x,y
                b_ctr = b_ctr + 1
                
    global btm_bdry,right_bdry, top_bdry, left_bdry
    btm_bdry = max(listY)
    right_bdry = max(listX)
    top_bdry = min(listY)
    left_bdry = min(listX)
#    print(top_bdry,left_bdry)
    
    y1 = btm_bdry /75
    x1 = right_bdry /75
    xy= y1*x1
    print("%.2f sqm" %xy)
    global floor_size_pix
    floor_size_pix = "%.2f sqm" %xy
#    print(yy,xx)
#    print(width, height)
#    print(pix[0,0])
    room_size = Label(window, text="Floor Plan Size = "+floor_size_pix,relief="solid",font=("arial",12,"bold"))
    room_size.place(x=240, y=70)
   
    languages = [
    "Bed room",
    "Living room"
    
    ]
    sp = 0
    for val, language in enumerate(languages):
        but = Radiobutton(window, 
                      text=language,
                      indicatoron = 0,
                      width = 10,
                      variable=v, 
                      command=ShowChoice,
                      value=val,font=("arial",12,"bold"))
        but.place(x = 860 , y = 50 + sp)
        sp = sp + 30
        
def ShowChoice():
    print(v.get())
    global type_room 
    type_room = v.get()
    if(type_room == 0):
#        print("Bed Room")
        typeofroom="Bed Room"
    if(type_room == 1):
        typeofroom="Living Room"
#        print("Living Room")
    else:
        typeofroom="Bed Room"
#        print("Bed Room")
    room_label = Label(window, text=typeofroom,relief="solid",font=("arial",12,"bold"), width = 15)
    room_label.place(x=480, y=70)
def Fuzzy(event=None):
#    print('',path)
#    path_imp = ImageTk.PhotoImage(Image.open(path).resize((409,440), Image.ANTIALIAS))
    path_imp = ImageTk.PhotoImage(Image.open(path), Image.ANTIALIAS)    
    predicted_image = "C:/Users/arcee/darknet/build/darknet/x64/predictions.jpg"
#    img = ImageTk.PhotoImage(Image.open(predicted_image).resize((409,440), Image.ANTIALIAS))
    img = ImageTk.PhotoImage(Image.open(predicted_image), Image.ANTIALIAS)
    
#    panel = Label(window, image=img) 
#    panel.photo = img
    panel = Label(window, image=path_imp) 
    panel.photo = path_imp
    panel.place(x=270,y=100)
    
    im = Image.open(predicted_image)
    pix = im.load()
    width, height = im.size
#    print(width,height)
    a1 = 0
    aa1 = 0
    aaa1=0
    colorListX=0
    colorListY =0
    for x in range(width):
        for y in range(height):        
#            global r,g,b
#            print(x,y)
            r,g,b = pix[x,y]
            if(r<250 and g<250 and b<250):
                colorListX= colorListX +1
                colorListY= colorListY +1
            if(r>240 and g>165 and b<15): #orange / walls
                a1 = a1 + 1
                aa1 = aa1+1
                aaa1=aaa1+1
               
    listX = [0 for i in range(a1)]
    listY= [0 for i in range(aa1)]
    listXY= [0 for i in range(aaa1)]
    listColorX = [0 for i in range(colorListX)]
    listColorY = [0 for i in range(colorListY)]    
    c_ctr=0
    b_ctr = 0
    for x in range(width):
        for y in range(height):  
            r,g,b = pix[x,y]
            if(r<250 and g<250 and b<250):
                listColorX[c_ctr] = x
                listColorY[c_ctr] = y
                c_ctr = c_ctr + 1
            if(r>240 and g>165 and b<15): #orange / walls
                listX[b_ctr] = x
                listY[b_ctr] = y
                listXY[b_ctr] = x,y
                b_ctr = b_ctr + 1
#    print(listColorX, listColorY)
    a2 = 0
    aa2 = 0
    aaa2=0
    for x in range(width):
        for y in range(height):        
            r,g,b = pix[x,y]
            if(r>240 and g<5 and b>240): #violet / doors
                a2 = a2 + 1
                aa2 = aa2+1
                aaa2=aaa2+1
               
    listX2 = [0 for i in range(a2)]
    listY2= [0 for i in range(aa2)]
    listXY2= [0 for i in range(aaa2)]
    b_ctr2 = 0
    for x in range(width):
        for y in range(height):  
            r,g,b = pix[x,y]
            if(r>240 and g<5 and b>240): #violet / doors
                listX2[b_ctr2] = x
                listY2[b_ctr2] = y
                listXY2[b_ctr2]= x,y
                b_ctr2 = b_ctr2 + 1
    aWhite = 0
    aaWhite = 0
    aaaWhite=0
    for x in range(width):
        for y in range(height):        
            r,g,b = pix[x,y]
            if(r>240 and g>240 and b>240): #violet / doors
                aWhite = aWhite + 1
                aaWhite = aaWhite + 1
                aaaWhite=aaaWhite + 1
               
    listXWhite = [0 for i in range(aWhite)]
    listYWhite= [0 for i in range(aaWhite)]
    listXYWhite= [0 for i in range(aaaWhite)]
    b_ctrWhite = 0
    for x in range(width):
        for y in range(height):  
            r,g,b = pix[x,y]
            if(r>240 and g>240 and b>240): #violet / doors
                listXWhite[b_ctrWhite] = x
                listYWhite[b_ctrWhite] = y
                listXYWhite[b_ctrWhite]= x,y
                b_ctrWhite = b_ctrWhite + 1
#    print(listXY2)
    floor_height = height /75
    floor_width = width /75
    floor_size= floor_height*floor_width            
#    print(floor_size)
    if(floor_size>25):                                 #large room
        if(type_room == 0):                            #Bed room
            
            bed_path = "C:/Users/arcee/Desktop/ui/furnitures/bed room/large/king bed.JPG"
            bed = ImageTk.PhotoImage(Image.open(bed_path), Image.ANTIALIAS)
            
            bed_path1 = "C:/Users/arcee/Desktop/ui/furnitures/bed room/large/king1.JPG"
            bed1 = ImageTk.PhotoImage(Image.open(bed_path1), Image.ANTIALIAS)
            
            bed_path2 = "C:/Users/arcee/Desktop/ui/furnitures/bed room/large/king2.JPG"
            bed2 = ImageTk.PhotoImage(Image.open(bed_path2), Image.ANTIALIAS)
            
            bed_path3 = "C:/Users/arcee/Desktop/ui/furnitures/bed room/large/king3.JPG"
            bed3 = ImageTk.PhotoImage(Image.open(bed_path3), Image.ANTIALIAS)
            
            pot_path = "C:/Users/arcee/Desktop/ui/furnitures/bed room/large/pot.JPG"
            pot = ImageTk.PhotoImage(Image.open(pot_path), Image.ANTIALIAS)
            
            cabinet_path = "C:/Users/arcee/Desktop/ui/furnitures/bed room/large/cabinet.JPG"
            cabinet = ImageTk.PhotoImage(Image.open(cabinet_path), Image.ANTIALIAS)
            
            cabinet_path1 = "C:/Users/arcee/Desktop/ui/furnitures/bed room/large/cabinet1.JPG"
            cabinet1 = ImageTk.PhotoImage(Image.open(cabinet_path1), Image.ANTIALIAS)
            
            sofa_path = "C:/Users/arcee/Desktop/ui/furnitures/bed room/large/sofa.JPG"
            sofa = ImageTk.PhotoImage(Image.open(sofa_path), Image.ANTIALIAS)
            
            sofa_path1 = "C:/Users/arcee/Desktop/ui/furnitures/bed room/large/sofa1.JPG"
            sofa1 = ImageTk.PhotoImage(Image.open(sofa_path1), Image.ANTIALIAS)
            
            sofa_path3 = "C:/Users/arcee/Desktop/ui/furnitures/bed room/large/sofa3.JPG"
            sofa3 = ImageTk.PhotoImage(Image.open(sofa_path3), Image.ANTIALIAS)
            
            tvset_path = "C:/Users/arcee/Desktop/ui/furnitures/bed room/large/tvset.JPG"
            tvset = ImageTk.PhotoImage(Image.open(tvset_path), Image.ANTIALIAS)
            
            tvset_path1 = "C:/Users/arcee/Desktop/ui/furnitures/bed room/large/tvset1.JPG"
            tvset1 = ImageTk.PhotoImage(Image.open(tvset_path1), Image.ANTIALIAS)
            
            
        if(type_room == 1):                             #Living Room
            
            bookcase_path = "C:/Users/arcee/Desktop/ui/furnitures/living room/l/bookcase.JPG"
            bookcase = ImageTk.PhotoImage(Image.open(bookcase_path), Image.ANTIALIAS)
            
            cabinet_path = "C:/Users/arcee/Desktop/ui/furnitures/living room/l/cabinet.JPG"
            cabinet = ImageTk.PhotoImage(Image.open(cabinet_path), Image.ANTIALIAS)   
            
            cabinet_path1 = "C:/Users/arcee/Desktop/ui/furnitures/bed room/large/cabinet1.JPG"
            cabinet1 = ImageTk.PhotoImage(Image.open(cabinet_path1), Image.ANTIALIAS)
            
            cabinet_path2 = "C:/Users/arcee/Desktop/ui/furnitures/living room/l/cabinet2.JPG"
            cabinet2 = ImageTk.PhotoImage(Image.open(cabinet_path2), Image.ANTIALIAS)
            
            sofa_path = "C:/Users/arcee/Desktop/ui/furnitures/living room/l/sofa.JPG"
            sofa = ImageTk.PhotoImage(Image.open(sofa_path), Image.ANTIALIAS) 
            
            sofa_path = "C:/Users/arcee/Desktop/ui/furnitures/living room/l/sofa_h.JPG"
            sofa_h = ImageTk.PhotoImage(Image.open(sofa_path), Image.ANTIALIAS)
            
            tvset_path = "C:/Users/arcee/Desktop/ui/furnitures/living room/l/tvset.JPG"
            tvset = ImageTk.PhotoImage(Image.open(tvset_path), Image.ANTIALIAS) 
            
            tvset1_path = "C:/Users/arcee/Desktop/ui/furnitures/living room/l/tvset1.JPG"
            tvset1 = ImageTk.PhotoImage(Image.open(tvset1_path), Image.ANTIALIAS) 
            
            pot_path = "C:/Users/arcee/Desktop/ui/furnitures/living room/l/pot.JPG"
            pot = ImageTk.PhotoImage(Image.open(pot_path), Image.ANTIALIAS) 
#            print(type_room)
    if(floor_size < 25 and floor_size > 15):                                    #medium room
         if(type_room == 0):                            #Bed room
            
            bed_path = "C:/Users/arcee/Desktop/ui/furnitures/bed room/mid/queen bed.JPG"
            bed = ImageTk.PhotoImage(Image.open(bed_path), Image.ANTIALIAS)
            
            bed2_path = "C:/Users/arcee/Desktop/ui/furnitures/bed room/mid/queenbed2.JPG"
            bed2 = ImageTk.PhotoImage(Image.open(bed2_path), Image.ANTIALIAS)
            
            bed_path3 = "C:/Users/arcee/Desktop/ui/furnitures/bed room/mid/queenbed3.JPG"
            bed3 = ImageTk.PhotoImage(Image.open(bed_path3), Image.ANTIALIAS)
            
            pot_path = "C:/Users/arcee/Desktop/ui/furnitures/bed room/mid/pot.JPG"
            pot = ImageTk.PhotoImage(Image.open(pot_path), Image.ANTIALIAS)
            
            cabinet_path = "C:/Users/arcee/Desktop/ui/furnitures/bed room/mid/cabinet.JPG"
            cabinet = ImageTk.PhotoImage(Image.open(cabinet_path), Image.ANTIALIAS)
            
            sofa_path = "C:/Users/arcee/Desktop/ui/furnitures/bed room/mid/sofa.JPG"
            sofa = ImageTk.PhotoImage(Image.open(sofa_path), Image.ANTIALIAS)
            
            tvset_path = "C:/Users/arcee/Desktop/ui/furnitures/bed room/mid/tvset.JPG"
            tvset = ImageTk.PhotoImage(Image.open(tvset_path), Image.ANTIALIAS)
            
            bookcase_path = "C:/Users/arcee/Desktop/ui/furnitures/bed room/mid/bookcase.JPG"
            bookcase = ImageTk.PhotoImage(Image.open(bookcase_path), Image.ANTIALIAS)
            
         if(type_room == 1):                             #Living Room
            
            bookcase_path = "C:/Users/arcee/Desktop/ui/furnitures/living room/m/bookcase.JPG"
            bookcase = ImageTk.PhotoImage(Image.open(bookcase_path), Image.ANTIALIAS)
            
            cabinet_path = "C:/Users/arcee/Desktop/ui/furnitures/living room/m/cabinet.JPG"
            cabinet = ImageTk.PhotoImage(Image.open(cabinet_path), Image.ANTIALIAS)   
            
            cabinet_path1 = "C:/Users/arcee/Desktop/ui/furnitures/living room/m/cabinet1.JPG"
            cabinet1 = ImageTk.PhotoImage(Image.open(cabinet_path1), Image.ANTIALIAS)   
            
            sofa_path = "C:/Users/arcee/Desktop/ui/furnitures/living room/m/sofa.JPG"
            sofa = ImageTk.PhotoImage(Image.open(sofa_path), Image.ANTIALIAS) 
            
            sofa_path1 = "C:/Users/arcee/Desktop/ui/furnitures/living room/m/sofa1.JPG"
            sofa1 = ImageTk.PhotoImage(Image.open(sofa_path1), Image.ANTIALIAS)
            
            tvset_path = "C:/Users/arcee/Desktop/ui/furnitures/living room/m/tvset.JPG"
            tvset = ImageTk.PhotoImage(Image.open(tvset_path), Image.ANTIALIAS) 
            
            pot_path = "C:/Users/arcee/Desktop/ui/furnitures/living room/m/pot.JPG"
            pot = ImageTk.PhotoImage(Image.open(pot_path), Image.ANTIALIAS) 
        
    if(floor_size<=15):                                 #small room
        if(type_room == 0):                            #Bed room
            
            bed_path = "C:/Users/arcee/Desktop/ui/furnitures/bed room/small/single.JPG"
            bed = ImageTk.PhotoImage(Image.open(bed_path), Image.ANTIALIAS)
            
            bed1_path = "C:/Users/arcee/Desktop/ui/furnitures/bed room/small/single1.JPG"
            bed1 = ImageTk.PhotoImage(Image.open(bed1_path), Image.ANTIALIAS)
            
            bed2_path = "C:/Users/arcee/Desktop/ui/furnitures/bed room/small/single2.JPG"
            bed2 = ImageTk.PhotoImage(Image.open(bed2_path), Image.ANTIALIAS)
            
            pot_path = "C:/Users/arcee/Desktop/ui/furnitures/bed room/small/pot.JPG"
            pot = ImageTk.PhotoImage(Image.open(pot_path), Image.ANTIALIAS)
            
            cabinet_path = "C:/Users/arcee/Desktop/ui/furnitures/bed room/small/cabinet.JPG"
            cabinet = ImageTk.PhotoImage(Image.open(cabinet_path), Image.ANTIALIAS)
            
            cabinet1_path = "C:/Users/arcee/Desktop/ui/furnitures/bed room/small/cabinet1.JPG"
            cabinet1 = ImageTk.PhotoImage(Image.open(cabinet1_path), Image.ANTIALIAS)
            
            cabinet2_path = "C:/Users/arcee/Desktop/ui/furnitures/bed room/small/cabinet2.JPG"
            cabinet2 = ImageTk.PhotoImage(Image.open(cabinet2_path), Image.ANTIALIAS)
            
            cabinet3_path = "C:/Users/arcee/Desktop/ui/furnitures/living room/m/cabinet.JPG"
            cabinet3 = ImageTk.PhotoImage(Image.open(cabinet3_path), Image.ANTIALIAS) 
            
        if(type_room == 1):                             #Living Room
            
            bookcase_path = "C:/Users/arcee/Desktop/ui/furnitures/living room/s/bookcase.JPG"
            bookcase = ImageTk.PhotoImage(Image.open(bookcase_path), Image.ANTIALIAS)
            
            bookcase_path1 = "C:/Users/arcee/Desktop/ui/furnitures/living room/s/bookcase1.JPG"
            bookcase1 = ImageTk.PhotoImage(Image.open(bookcase_path1), Image.ANTIALIAS)
            
            bookcase_path2 = "C:/Users/arcee/Desktop/ui/furnitures/living room/s/bookcase2.JPG"
            bookcase2 = ImageTk.PhotoImage(Image.open(bookcase_path2), Image.ANTIALIAS)
            
            bookcase_path3 = "C:/Users/arcee/Desktop/ui/furnitures/living room/s/bookcase3.JPG"
            bookcase3 = ImageTk.PhotoImage(Image.open(bookcase_path3), Image.ANTIALIAS)
            
            cabinet_path = "C:/Users/arcee/Desktop/ui/furnitures/living room/m/cabinet2.JPG"
            cabinet = ImageTk.PhotoImage(Image.open(cabinet_path), Image.ANTIALIAS) 
            
            sofa_path2 = "C:/Users/arcee/Desktop/ui/furnitures/living room/s/sofa2.JPG"
            sofa2 = ImageTk.PhotoImage(Image.open(sofa_path2), Image.ANTIALIAS) 
            
            sofa_path = "C:/Users/arcee/Desktop/ui/furnitures/living room/s/sofa.JPG"
            sofa = ImageTk.PhotoImage(Image.open(sofa_path), Image.ANTIALIAS) 
            
            sofa3_path = "C:/Users/arcee/Desktop/ui/furnitures/living room/m/sofa.JPG"
            sofa3 = ImageTk.PhotoImage(Image.open(sofa3_path), Image.ANTIALIAS) 
            
            sofa4_path = "C:/Users/arcee/Desktop/ui/furnitures/living room/s/sofa3.JPG"
            sofa4 = ImageTk.PhotoImage(Image.open(sofa4_path), Image.ANTIALIAS)
            
            sofa_path1 = "C:/Users/arcee/Desktop/ui/furnitures/living room/s/sofa1.JPG"
            sofa1 = ImageTk.PhotoImage(Image.open(sofa_path1), Image.ANTIALIAS) 

            tvset_path = "C:/Users/arcee/Desktop/ui/furnitures/living room/s/tvset.JPG"
            tvset = ImageTk.PhotoImage(Image.open(tvset_path), Image.ANTIALIAS)
            
            tvset1_path1 = "C:/Users/arcee/Desktop/ui/furnitures/living room/s/tvset1.JPG"
            tvset1 = ImageTk.PhotoImage(Image.open(tvset1_path1), Image.ANTIALIAS)
            
            tvset2_path = "C:/Users/arcee/Desktop/ui/furnitures/living room/s/tvset.JPG"
            tvset2 = ImageTk.PhotoImage(Image.open(tvset2_path), Image.ANTIALIAS)
            
            pot_path = "C:/Users/arcee/Desktop/ui/furnitures/living room/s/pot.JPG"
            pot = ImageTk.PhotoImage(Image.open(pot_path), Image.ANTIALIAS) 
            
    if(path == "C:/Users/arcee/Desktop/ui/Import/room1.JPG"):
        if(type_room == 0):   
            panel = Label(window, image=bed) 
            panel.photo = bed
            panel.place(x=270 + 20,y=100 + 18)
            panel = Label(window, image=pot) 
            panel.photo = pot
            panel.place(x=270 + 100,y=100 + 20)
            panel = Label(window, image=cabinet) 
            panel.photo = cabinet
            panel.place(x=270 + 140,y=100 + 20)
            
        if(type_room == 1): 
        
            panel = Label(window, image=tvset) 
            panel.photo = tvset
            panel.place(x=270 + 20,y=100 + 165)
            
            panel = Label(window, image=sofa) 
            panel.photo = sofa
            panel.place(x=270 + 20,y=100 + 18)
            
            panel = Label(window, image=bookcase) 
            panel.photo = bookcase
            panel.place(x=270 + 160,y=100 + 18)
            
    if(path == "C:/Users/arcee/Desktop/ui/Import/room2.JPG"):
        if(type_room == 0):   
            panel = Label(window, image=bed) 
            panel.photo = bed
            panel.place(x=270 + 20,y=100 + 18)
            panel = Label(window, image=pot) 
            panel.photo = pot
            panel.place(x=270 + 100,y=100 + 20)
            panel = Label(window, image=cabinet) 
            panel.photo = cabinet
            panel.place(x=270 + 130,y=100 + 20)
            
        if(type_room == 1): 
        
            panel = Label(window, image=tvset) 
            panel.photo = tvset
            panel.place(x=270 + 60,y=100 + 165)
            
            panel = Label(window, image=sofa) 
            panel.photo = sofa
            panel.place(x=270 + 20,y=100 + 18)
            
            panel = Label(window, image=bookcase) 
            panel.photo = bookcase
            panel.place(x=270 + 160,y=100 + 18)
            
    if(path == "C:/Users/arcee/Desktop/ui/Import/room3.JPG"):
        if(type_room == 0):   
            panel = Label(window, image=bed) 
            panel.photo = bed
            panel.place(x=270 + 118,y=100 + 20)
            panel = Label(window, image=pot) 
            panel.photo = pot
            panel.place(x=270 + 92,y=100 + 20)
            panel = Label(window, image=cabinet2) 
            panel.photo = cabinet2
            panel.place(x=270 + 28,y=100 + 20)
            
        if(type_room == 1): 
        
            panel = Label(window, image=tvset) 
            panel.photo = tvset
            panel.place(x=270 + 30,y=100 + 130)
            
            panel = Label(window, image=sofa) 
            panel.photo = sofa
            panel.place(x=270 + 30,y=100 + 18)
            
            panel = Label(window, image=bookcase) 
            panel.photo = bookcase
            panel.place(x=270 + 170,y=100 + 18)
            
    if(path == "C:/Users/arcee/Desktop/ui/Import/room4.JPG"):
        if(type_room == 0):   
            panel = Label(window, image=bed) 
            panel.photo = bed
            panel.place(x=270 + 20,y=100 + 18)
            
            panel = Label(window, image=cabinet2) 
            panel.photo = cabinet2
            panel.place(x=270 + 100,y=100 + 20)
            
            panel = Label(window, image=pot) 
            panel.photo = pot
            panel.place(x=270 + 100,y=100 + 20)
        if(type_room == 1): 
        
            panel = Label(window, image=tvset1) 
            panel.photo = tvset1
            panel.place(x=270 + 25,y=100 + 25)
            
            panel = Label(window, image=sofa1) 
            panel.photo = sofa1
            panel.place(x=270 + 95,y=100 + 25)  
            
            panel = Label(window, image=bookcase1) 
            panel.photo = bookcase1
            panel.place(x=270 + 90,y=100 + 190)
    if(path == "C:/Users/arcee/Desktop/ui/Import/room5.JPG"):
        if(type_room == 0):   
            panel = Label(window, image=bed) 
            panel.photo = bed
            panel.place(x=270 + 90,y=100 + 25)
            panel = Label(window, image=cabinet1) 
            panel.photo = cabinet1
            panel.place(x=270 + 25,y=100 + 80)
            panel = Label(window, image=pot) 
            panel.photo = pot
            panel.place(x=270 + 25,y=100 + 30)
        if(type_room == 1): 
        
            panel = Label(window, image=tvset1) 
            panel.photo = tvset1
            panel.place(x=270 + 20,y=100 + 35)
            
            panel = Label(window, image=sofa1) 
            panel.photo = sofa1
            panel.place(x=270 + 95,y=100 + 30)
            
            panel = Label(window, image=bookcase1) 
            panel.photo = bookcase1
            panel.place(x=270 + 90,y=100 + 190)
            
    if(path == "C:/Users/arcee/Desktop/ui/Import/room6.JPG"):
        if(type_room == 0):   
            panel = Label(window, image=bed2) 
            panel.photo = bed2
            panel.place(x=270 + 27 ,y=100 + 70)
            panel = Label(window, image=cabinet2) 
            panel.photo = cabinet2
            panel.place(x=270 + 27,y=100 + 23   )
            panel = Label(window, image=pot) 
            panel.photo = pot
            panel.place(x=270 + 105,y=100 + 190)
        if(type_room == 1): 
        
            panel = Label(window, image=tvset) 
            panel.photo = tvset
            panel.place(x=270 + 27,y=100 + 30)
            
            panel = Label(window, image=sofa2) 
            panel.photo = sofa2
            panel.place(x=270 + 45,y=100 + 150)
            
            panel = Label(window, image=bookcase2) 
            panel.photo = bookcase2
            panel.place(x=270 + 27,y=100 + 100)
            
    if(path == "C:/Users/arcee/Desktop/ui/Import/room7.JPG"):
        if(type_room == 0):   
            panel = Label(window, image=bed2) 
            panel.photo = bed2
            panel.place(x=270 + 85 ,y=100 + 70)
            panel = Label(window, image=cabinet1) 
            panel.photo = cabinet1
            panel.place(x=270 + 20,y=100 + 70   )
            panel = Label(window, image=pot) 
            panel.photo = pot
            panel.place(x=270 + 55,y=100 + 190)
        if(type_room == 1): 
        
            panel = Label(window, image=tvset1) 
            panel.photo = tvset1
            panel.place(x=270 + 20,y=100 + 80)
            
            panel = Label(window, image=sofa1) 
            panel.photo = sofa1
            panel.place(x=270 + 100,y=100 + 80)
            
            panel = Label(window, image=bookcase3) 
            panel.photo = bookcase3
            panel.place(x=270 + 70,y=100 + 24)
            
    if(path == "C:/Users/arcee/Desktop/ui/Import/room8.JPG"):
        if(type_room == 0):   
            panel = Label(window, image=bed2) 
            panel.photo = bed2
            panel.place(x=270 + 90 ,y=100 + 70)
            panel = Label(window, image=cabinet2) 
            panel.photo = cabinet2
            panel.place(x=270 + 27,y=100 + 30)
            panel = Label(window, image=pot) 
            panel.photo = pot
            panel.place(x=270 + 60,y=100 + 200)
        if(type_room == 1): 
        
            panel = Label(window, image=tvset) 
            panel.photo = tvset
            panel.place(x=270 + 27,y=100 + 30)
            
            panel = Label(window, image=sofa2) 
            panel.photo = sofa2
            panel.place(x=270 + 27,y=100 + 160)
            
            panel = Label(window, image=bookcase) 
            panel.photo = bookcase
            panel.place(x=270 + 140,y=100 + 80)
            
    if(path == "C:/Users/arcee/Desktop/ui/Import/room9.JPG"):
        if(type_room == 0):   
            panel = Label(window, image=bed2) 
            panel.photo = bed2
            panel.place(x=270 + 90 ,y=100 + 60)
            panel = Label(window, image=cabinet2) 
            panel.photo = cabinet2
            panel.place(x=270 + 27,y=100 + 20)
            panel = Label(window, image=pot) 
            panel.photo = pot
            panel.place(x=270 + 60,y=100 + 190)
        if(type_room == 1): 
        
            panel = Label(window, image=tvset) 
            panel.photo = tvset
            panel.place(x=270 + 27,y=100 + 20)
            
            panel = Label(window, image=sofa2) 
            panel.photo = sofa2
            panel.place(x=270 + 27,y=100 + 150)
            
            panel = Label(window, image=bookcase) 
            panel.photo = bookcase
            panel.place(x=270 + 140,y=100 + 70)
            
    if(path == "C:/Users/arcee/Desktop/ui/Import/room10.JPG"):
        if(type_room == 0):   
            panel = Label(window, image=bed2) 
            panel.photo = bed2
            panel.place(x=270 + 90 ,y=100 + 70)
            panel = Label(window, image=cabinet1) 
            panel.photo = cabinet1
            panel.place(x=270 + 27,y=100 + 110)
            panel = Label(window, image=pot) 
            panel.photo = pot
            panel.place(x=270 + 60,y=100 + 190)
        if(type_room == 1): 
        
            panel = Label(window, image=tvset) 
            panel.photo = tvset
            panel.place(x=270 + 50,y=100 + 25)
            
            panel = Label(window, image=sofa2) 
            panel.photo = sofa2
            panel.place(x=270 + 27,y=100 + 150)
            
#            panel = Label(window, image=bookcase3) 
#            panel.photo = bookcase3
#            panel.place(x=270 + 27,y=100 + 20)
            
    if(path == "C:/Users/arcee/Desktop/ui/Import/room11.JPG"):
        if(type_room == 0):   
            panel = Label(window, image=bed) 
            panel.photo = bed
            panel.place(x=270 + 150 ,y=100 + 95)
            panel = Label(window, image=cabinet3) 
            panel.photo = cabinet3
            panel.place(x=270 + 20,y=100 + 95)
            panel = Label(window, image=pot) 
            panel.photo = pot
            panel.place(x=270 + 250,y=100 + 95)
            panel = Label(window, image=cabinet2) 
            panel.photo = cabinet2
            panel.place(x=270 + 200,y=100 + 30)
            
        if(type_room == 1): 
        
            panel = Label(window, image=tvset1) 
            panel.photo = tvset1
            panel.place(x=270 + 225,y=100 + 100)
            
            panel = Label(window, image=sofa4) 
            panel.photo = sofa4
            panel.place(x=270 + 27,y=100 + 100)
            
            panel = Label(window, image=bookcase3) 
            panel.photo = bookcase3
            panel.place(x=270 + 70,y=100 + 25)
            panel = Label(window, image=bookcase3) 
            panel.photo = bookcase3
            panel.place(x=270 + 150,y=100 + 25)
            
    if(path == "C:/Users/arcee/Desktop/ui/Import/room12.JPG"):
        if(type_room == 0):   
            panel = Label(window, image=bed) 
            panel.photo = bed
            panel.place(x=270 + 30,y=100 + 220)
            panel = Label(window, image=pot) 
            panel.photo = pot
            panel.place(x=270 + 145,y=100 + 340)
            panel = Label(window, image=cabinet) 
            panel.photo = cabinet
            panel.place(x=270 + 265,y=100 + 20)
            panel = Label(window, image=tvset) 
            panel.photo = tvset
            panel.place(x=270 + 25,y=100 + 25)
        if(type_room == 1): 
#        
            panel = Label(window, image=tvset) 
            panel.photo = tvset
            panel.place(x=270 + 260,y=100 + 50)
#            
            panel = Label(window, image=sofa) 
            panel.photo = sofa
            panel.place(x=270 + 25,y=100 + 20)
#            
            panel = Label(window, image=bookcase) 
            panel.photo = bookcase
            panel.place(x=270 + 30,y=100 + 340)
            
            panel = Label(window, image=pot) 
            panel.photo = pot
            panel.place(x=270 + 25,y=100 + 220)
            
            panel = Label(window, image=cabinet) 
            panel.photo = cabinet
            panel.place(x=270 + 25,y=100 + 260)
            
    if(path == "C:/Users/arcee/Desktop/ui/Import/room13.JPG"):
        if(type_room == 0):   
            panel = Label(window, image=bed) 
            panel.photo = bed
            panel.place(x=270 + 370,y=100 + 175)
            panel = Label(window, image=pot) 
            panel.photo = pot
            panel.place(x=270 + 333,y=100 + 330)
            panel = Label(window, image=cabinet) 
            panel.photo = cabinet
            panel.place(x=270 + 35,y=100 + 30)
            panel = Label(window, image=cabinet) 
            panel.photo = cabinet
            panel.place(x=270 + 150,y=100 + 30)
            panel = Label(window, image=tvset) 
            panel.photo = tvset
            panel.place(x=270 + 380,y=100 + 25)
            panel = Label(window, image=sofa) 
            panel.photo = sofa
            panel.place(x=270 + 50,y=100 + 290)
            panel = Label(window, image=sofa) 
            panel.photo = sofa
            panel.place(x=270 + 180,y=100 + 290)
        if(type_room == 1): 
#        
            panel = Label(window, image=tvset) 
            panel.photo = tvset
            panel.place(x=270 + 300,y=100 + 290)
#            
            panel = Label(window, image=sofa) 
            panel.photo = sofa
            panel.place(x=270 + 265,y=100 + 30)
#           
            panel = Label(window, image=sofa_h) 
            panel.photo = sofa_h
            panel.place(x=270 + 450,y=100 + 100)
            
            panel = Label(window, image=bookcase) 
            panel.photo = bookcase
            panel.place(x=270 + 30,y=100 + 310)
            
            panel = Label(window, image=pot) 
            panel.photo = pot
            panel.place(x=270 + 470,y=100 + 40)
            
            panel = Label(window, image=cabinet) 
            panel.photo = cabinet
            panel.place(x=270 + 35,y=100 + 35)
    if(path == "C:/Users/arcee/Desktop/ui/Import/room14.JPG"):
        if(type_room == 0):   
            panel = Label(window, image=bed2) 
            panel.photo = bed2
            panel.place(x=270 + 30,y=100 + 25)
            panel = Label(window, image=pot) 
            panel.photo = pot
            panel.place(x=270 + 50,y=100 + 200)
            panel = Label(window, image=cabinet1) 
            panel.photo = cabinet1
            panel.place(x=270 + 480,y=100 + 180)
            panel = Label(window, image=tvset1) 
            panel.photo = tvset1
            panel.place(x=270 + 480,y=100 + 30)
            panel = Label(window, image=sofa) 
            panel.photo = sofa
            panel.place(x=270 + 50,y=100 + 290)
            panel = Label(window, image=sofa) 
            panel.photo = sofa
            panel.place(x=270 + 180,y=100 + 290)
        if(type_room == 1): 
#        
            panel = Label(window, image=tvset) 
            panel.photo = tvset
            panel.place(x=270 + 40,y=100 + 120)
#            
            panel = Label(window, image=sofa) 
            panel.photo = sofa
            panel.place(x=270 + 265,y=100 + 30)
#           
            panel = Label(window, image=sofa_h) 
            panel.photo = sofa_h
            panel.place(x=270 + 450,y=100 + 100)
            
            panel = Label(window, image=bookcase) 
            panel.photo = bookcase
            panel.place(x=270 + 30,y=100 + 310)
            
            panel = Label(window, image=pot) 
            panel.photo = pot
            panel.place(x=270 + 470,y=100 + 40)
            
            panel = Label(window, image=cabinet) 
            panel.photo = cabinet
            panel.place(x=270 + 130,y=100 + 30)
            
    if(path == "C:/Users/arcee/Desktop/ui/Import/room15.JPG"):
        if(type_room == 0):   
            panel = Label(window, image=bed2) 
            panel.photo = bed2
            panel.place(x=270 + 35,y=100 + 30)
            panel = Label(window, image=pot) 
            panel.photo = pot
            panel.place(x=270 + 40,y=100 + 205)
            panel = Label(window, image=cabinet1) 
            panel.photo = cabinet1
            panel.place(x=270 + 500,y=100 + 260)
            panel = Label(window, image=tvset1) 
            panel.photo = tvset1
            panel.place(x=270 + 350,y=100 + 30)
            panel = Label(window, image=sofa) 
            panel.photo = sofa
            panel.place(x=270 + 50,y=100 + 290)
            panel = Label(window, image=sofa) 
            panel.photo = sofa
            panel.place(x=270 + 180,y=100 + 290)
        if(type_room == 1): 
#        
            panel = Label(window, image=tvset1) 
            panel.photo = tvset1
            panel.place(x=270 + 40,y=100 + 120)
#            
            panel = Label(window, image=sofa) 
            panel.photo = sofa
            panel.place(x=270 + 100,y=100 + 30)
#           
            panel = Label(window, image=sofa_h) 
            panel.photo = sofa_h
            panel.place(x=270 + 285,y=100 + 100)
            
            panel = Label(window, image=bookcase) 
            panel.photo = bookcase
            panel.place(x=270 + 30,y=100 + 310)
            
            panel = Label(window, image=pot) 
            panel.photo = pot
            panel.place(x=270 + 470,y=100 + 40)
            
            panel = Label(window, image=cabinet) 
            panel.photo = cabinet
            panel.place(x=270 + 150,y=100 + 310)
            
    if(path == "C:/Users/arcee/Desktop/ui/Import/room16.JPG"):
        if(type_room == 0):   
            panel = Label(window, image=bed2) 
            panel.photo = bed2
            panel.place(x=270 + 30,y=100 + 25)
            panel = Label(window, image=pot) 
            panel.photo = pot
            panel.place(x=270 + 50,y=100 + 200)
            panel = Label(window, image=cabinet1) 
            panel.photo = cabinet1
            panel.place(x=270 + 480,y=100 + 180)
            panel = Label(window, image=tvset1) 
            panel.photo = tvset1
            panel.place(x=270 + 480,y=100 + 30)
            panel = Label(window, image=sofa) 
            panel.photo = sofa
            panel.place(x=270 + 50,y=100 + 290)
            panel = Label(window, image=sofa) 
            panel.photo = sofa
            panel.place(x=270 + 180,y=100 + 290)
        if(type_room == 1): 
#        
            panel = Label(window, image=tvset) 
            panel.photo = tvset
            panel.place(x=270 + 225,y=100 + 290)
#            
            panel = Label(window, image=sofa) 
            panel.photo = sofa
            panel.place(x=270 + 265,y=100 + 30)
#           
            panel = Label(window, image=sofa_h) 
            panel.photo = sofa_h
            panel.place(x=270 + 450,y=100 + 100)
            
            panel = Label(window, image=bookcase) 
            panel.photo = bookcase
            panel.place(x=270 + 30,y=100 + 310)
            
            panel = Label(window, image=pot) 
            panel.photo = pot
            panel.place(x=270 + 470,y=100 + 40)
            
            panel = Label(window, image=cabinet2) 
            panel.photo = cabinet2
            panel.place(x=270 + 30,y=100 + 160)
            
    if(path == "C:/Users/arcee/Desktop/ui/Import/room17.JPG"):
        if(type_room == 0):   
            panel = Label(window, image=bed2) 
            panel.photo = bed2
            panel.place(x=270 + 30,y=100 + 25)
            panel = Label(window, image=pot) 
            panel.photo = pot
            panel.place(x=270 + 50,y=100 + 200)
            panel = Label(window, image=cabinet1) 
            panel.photo = cabinet1
            panel.place(x=270 + 480,y=100 + 180)
            panel = Label(window, image=tvset1) 
            panel.photo = tvset1
            panel.place(x=270 + 480,y=100 + 30)
            panel = Label(window, image=sofa) 
            panel.photo = sofa
            panel.place(x=270 + 50,y=100 + 290)
            panel = Label(window, image=sofa) 
            panel.photo = sofa
            panel.place(x=270 + 180,y=100 + 290)
        if(type_room == 1): 
#        
            panel = Label(window, image=tvset) 
            panel.photo = tvset
            panel.place(x=270 + 225,y=100 + 290)
#            
            panel = Label(window, image=sofa) 
            panel.photo = sofa
            panel.place(x=270 + 305,y=100 + 30)
#           
            panel = Label(window, image=sofa) 
            panel.photo = sofa
            panel.place(x=270 + 120,y=100 + 30)
            
            panel = Label(window, image=bookcase) 
            panel.photo = bookcase
            panel.place(x=270 + 30,y=100 + 310)
            
            panel = Label(window, image=pot) 
            panel.photo = pot
            panel.place(x=270 + 30,y=100 + 40)
            
            panel = Label(window, image=cabinet2) 
            panel.photo = cabinet2
            panel.place(x=270 + 30,y=100 + 160)   
            
    if(path == "C:/Users/arcee/Desktop/ui/Import/room18.JPG"):
        if(type_room == 0):   
            panel = Label(window, image=bed) 
            panel.photo = bed
            panel.place(x=270 + 370,y=100 + 200)
            panel = Label(window, image=pot) 
            panel.photo = pot
            panel.place(x=270 + 340,y=100 + 350)
            panel = Label(window, image=cabinet1) 
            panel.photo = cabinet1
            panel.place(x=270 + 485,y=100 + 80)
            panel = Label(window, image=tvset) 
            panel.photo = tvset
            panel.place(x=270 + 100,y=100 + 70)
            panel = Label(window, image=sofa) 
            panel.photo = sofa
            panel.place(x=270 + 50,y=100 + 330)
            panel = Label(window, image=sofa) 
            panel.photo = sofa
            panel.place(x=270 + 180,y=100 + 330)
        if(type_room == 1): 
#        
            panel = Label(window, image=tvset) 
            panel.photo = tvset
            panel.place(x=270 + 225,y=100 + 310)
#            
            panel = Label(window, image=sofa) 
            panel.photo = sofa
            panel.place(x=270 + 305,y=100 + 70)
#           
            panel = Label(window, image=sofa) 
            panel.photo = sofa
            panel.place(x=270 + 120,y=100 + 70)
            
            panel = Label(window, image=bookcase) 
            panel.photo = bookcase
            panel.place(x=270 + 30,y=100 + 330)
            
            panel = Label(window, image=pot) 
            panel.photo = pot
            panel.place(x=270 + 500,y=100 + 70)
            
            panel = Label(window, image=cabinet2) 
            panel.photo = cabinet2
            panel.place(x=270 + 30,y=100 + 160)     
            
    if(path == "C:/Users/arcee/Desktop/ui/Import/room19.JPG"):
        if(type_room == 0):   
            panel = Label(window, image=bed1) 
            panel.photo = bed1
            panel.place(x=270 + 30,y=100 + 30)
            panel = Label(window, image=pot) 
            panel.photo = pot
            panel.place(x=270 + 200,y=100 + 200)
            panel = Label(window, image=cabinet1) 
            panel.photo = cabinet1
            panel.place(x=270 + 485,y=100 + 50)
            panel = Label(window, image=tvset) 
            panel.photo = tvset
            panel.place(x=270 + 250,y=100 + 30)
            panel = Label(window, image=sofa) 
            panel.photo = sofa
            panel.place(x=270 + 100,y=100 + 290)
            panel = Label(window, image=sofa) 
            panel.photo = sofa
            panel.place(x=270 + 230,y=100 + 290)
        if(type_room == 1): 
#        
            panel = Label(window, image=tvset) 
            panel.photo = tvset
            panel.place(x=270 + 225,y=100 + 290)
#            
            panel = Label(window, image=sofa) 
            panel.photo = sofa
            panel.place(x=270 + 305,y=100 + 30)
#           
            panel = Label(window, image=sofa) 
            panel.photo = sofa
            panel.place(x=270 + 120,y=100 + 30)
            
            panel = Label(window, image=bookcase) 
            panel.photo = bookcase
            panel.place(x=270 + 30,y=100 + 310)
            
            panel = Label(window, image=pot) 
            panel.photo = pot
            panel.place(x=270 + 500,y=100 + 30)
            
            panel = Label(window, image=cabinet2) 
            panel.photo = cabinet2
            panel.place(x=270 + 30,y=100 + 160)   
            
    if(path == "C:/Users/arcee/Desktop/ui/Import/room20.JPG"):
        if(type_room == 0):   
            panel = Label(window, image=bed3) 
            panel.photo = bed3
            panel.place(x=270 + 30,y=100 + 30)
            panel = Label(window, image=pot) 
            panel.photo = pot
            panel.place(x=270 + 200,y=100 + 40)
            panel = Label(window, image=cabinet1) 
            panel.photo = cabinet1
            panel.place(x=270 + 485,y=100 + 200)
            panel = Label(window, image=tvset) 
            panel.photo = tvset
            panel.place(x=270 + 250,y=100 + 300)
            panel = Label(window, image=sofa1) 
            panel.photo = sofa1
            panel.place(x=270 + 240,y=100 + 30)
            panel = Label(window, image=sofa1) 
            panel.photo = sofa1
            panel.place(x=270 + 370,y=100 + 30)
        if(type_room == 1): 
#        
            panel = Label(window, image=tvset) 
            panel.photo = tvset
            panel.place(x=270 + 225,y=100 + 290)
#            
            panel = Label(window, image=sofa) 
            panel.photo = sofa
            panel.place(x=270 + 305,y=100 + 30)
#           
            panel = Label(window, image=sofa) 
            panel.photo = sofa
            panel.place(x=270 + 120,y=100 + 30)
            
            panel = Label(window, image=bookcase) 
            panel.photo = bookcase
            panel.place(x=270 + 30,y=100 + 310)
            
            panel = Label(window, image=pot) 
            panel.photo = pot
            panel.place(x=270 + 100,y=100 + 30)
            
            panel = Label(window, image=cabinet2) 
            panel.photo = cabinet2
            panel.place(x=270 + 30,y=100 + 160)           
                    
    if(path == "C:/Users/arcee/Desktop/ui/Import/room21.JPG"):
        if(type_room == 0):   
            panel = Label(window, image=bed1) 
            panel.photo = bed1
            panel.place(x=270 + 30,y=100 + 30)
            panel = Label(window, image=pot) 
            panel.photo = pot
            panel.place(x=270 + 200,y=100 + 200)
            panel = Label(window, image=cabinet1) 
            panel.photo = cabinet1
            panel.place(x=270 + 485,y=100 + 200)
            panel = Label(window, image=tvset) 
            panel.photo = tvset
            panel.place(x=270 + 250,y=100 + 30)
            panel = Label(window, image=sofa) 
            panel.photo = sofa
            panel.place(x=270 + 100,y=100 + 290)
            panel = Label(window, image=sofa) 
            panel.photo = sofa
            panel.place(x=270 + 230,y=100 + 290)
        if(type_room == 1): 
#        
            panel = Label(window, image=tvset) 
            panel.photo = tvset
            panel.place(x=270 + 225,y=100 + 290)
#            
            panel = Label(window, image=sofa) 
            panel.photo = sofa
            panel.place(x=270 + 255,y=100 + 30)
#           
            panel = Label(window, image=sofa) 
            panel.photo = sofa
            panel.place(x=270 + 70,y=100 + 30)
            
            panel = Label(window, image=bookcase) 
            panel.photo = bookcase
            panel.place(x=270 + 30,y=100 + 310)
            
#            panel = Label(window, image=pot) 
#            panel.photo = pot
#            panel.place(x=270 + 100,y=100 + 30)
#            
            panel = Label(window, image=cabinet2) 
            panel.photo = cabinet2
            panel.place(x=270 + 30,y=100 + 160)        
            
    if(path == "C:/Users/arcee/Desktop/ui/Import/room25.JPG" or path == "C:/Users/arcee/Desktop/ui/Import/25.JPG"):
        if(type_room == 0):   
            panel = Label(window, image=bed1) 
            panel.photo = bed1
            panel.place(x=270 + 250,y=100 + 215)
            panel = Label(window, image=pot) 
            panel.photo = pot
            panel.place(x=270 + 420,y=100 + 160)
            panel = Label(window, image=cabinet) 
            panel.photo = cabinet
            panel.place(x=270 + 200,y=100 + 70)
            panel = Label(window, image=tvset1) 
            panel.photo = tvset1
            panel.place(x=270 + 30,y=100 + 250)
            panel = Label(window, image=sofa1) 
            panel.photo = sofa1
            panel.place(x=270 + 320,y=100 + 65)
        if(type_room == 1): 
            panel = Label(window, image=tvset) 
            panel.photo = tvset
            panel.place(x=270 + 270,y=100 + 315)
#            
            panel = Label(window, image=sofa) 
            panel.photo = sofa
            panel.place(x=270 + 265,y=100 + 60)
#           
            panel = Label(window, image=bookcase) 
            panel.photo = bookcase
            panel.place(x=270 + 30,y=100 + 340)
            
            panel = Label(window, image=cabinet) 
            panel.photo = cabinet
            panel.place(x=270 + 145,y=100 + 60)
            
            panel = Label(window, image=pot) 
            panel.photo = pot
            panel.place(x=270 + 205,y=100 + 65)
    if(path == "C:/Users/arcee/Desktop/ui/Import/room26.JPG" or path == "C:/Users/arcee/Desktop/ui/Import/26.JPG"):
        if(type_room == 0):   
            panel = Label(window, image=bed1) 
            panel.photo = bed1
            panel.place(x=270 + 230,y=100 + 235)
            panel = Label(window, image=pot) 
            panel.photo = pot
            panel.place(x=270 + 400,y=100 + 170)
            panel = Label(window, image=cabinet) 
            panel.photo = cabinet
            panel.place(x=270 + 180,y=100 + 25)
            panel = Label(window, image=tvset1) 
            panel.photo = tvset1
            panel.place(x=270 + 30,y=100 + 250)
            panel = Label(window, image=sofa1) 
            panel.photo = sofa1
            panel.place(x=270 + 300,y=100 + 30)
        if(type_room == 1): 
            panel = Label(window, image=tvset) 
            panel.photo = tvset
            panel.place(x=270 + 250,y=100 + 345)
#            
            panel = Label(window, image=sofa) 
            panel.photo = sofa
            panel.place(x=270 + 245,y=100 + 30)
#           
            panel = Label(window, image=bookcase) 
            panel.photo = bookcase
            panel.place(x=270 + 30,y=100 + 370)
            
            panel = Label(window, image=cabinet) 
            panel.photo = cabinet
            panel.place(x=270 + 95,y=100 + 30)
            
            panel = Label(window, image=pot) 
            panel.photo = pot
            panel.place(x=270 + 205,y=100 + 45)
    if(path == "C:/Users/arcee/Desktop/ui/Import/room27.JPG"or path == "C:/Users/arcee/Desktop/ui/Import/27.JPG"):
        if(type_room == 0):   
            panel = Label(window, image=bed3) 
            panel.photo = bed3
            panel.place(x=270 + 265,y=100 + 30)
            panel = Label(window, image=pot) 
            panel.photo = pot
            panel.place(x=270 + 220,y=100 + 30)
            panel = Label(window, image=cabinet) 
            panel.photo = cabinet
            panel.place(x=270 + 60,y=100 + 30)
            panel = Label(window, image=tvset) 
            panel.photo = tvset
            panel.place(x=260 + 260,y=100 + 360)
            panel = Label(window, image=sofa3) 
            panel.photo = sofa3
            panel.place(x=270 + 25,y=100 + 130)
        if(type_room == 1): 
            panel = Label(window, image=tvset1) 
            panel.photo = tvset1
            panel.place(x=270 + 25,y=100 + 55)
#            
            panel = Label(window, image=sofa_h) 
            panel.photo = sofa_h
            panel.place(x=270 + 340,y=100 + 50)
#           
            panel = Label(window, image=bookcase) 
            panel.photo = bookcase
            panel.place(x=270 + 175,y=100 + 380)
            
            panel = Label(window, image=cabinet) 
            panel.photo = cabinet
            panel.place(x=270 + 300,y=100 + 380)
            
            panel = Label(window, image=pot) 
            panel.photo = pot
            panel.place(x=270 + 370,y=100 + 250)
    if(path == "C:/Users/arcee/Desktop/ui/Import/room28.JPG"or path == "C:/Users/arcee/Desktop/ui/Import/28.JPG"):
        if(type_room == 0):   
            panel = Label(window, image=bed) 
            panel.photo = bed
            panel.place(x=270 + 195,y=100 + 155)
            panel = Label(window, image=pot) 
            panel.photo = pot
            panel.place(x=270 + 145,y=100 + 270)
            panel = Label(window, image=cabinet) 
            panel.photo = cabinet
            panel.place(x=270 + 25,y=100 + 25)
            panel = Label(window, image=tvset) 
            panel.photo = tvset
            panel.place(x=270 + 200,y=100 + 25)
        if(type_room == 1): 
#        
            panel = Label(window, image=tvset) 
            panel.photo = tvset
            panel.place(x=270 + 25,y=100 + 40)
#            
            panel = Label(window, image=sofa1) 
            panel.photo = sofa1
            panel.place(x=270 + 225,y=100 + 30)
#            
            panel = Label(window, image=bookcase) 
            panel.photo = bookcase
            panel.place(x=270 + 70,y=100 + 280)
            
            panel = Label(window, image=pot) 
            panel.photo = pot
            panel.place(x=270 + 260,y=100 + 230)
            
            panel = Label(window, image=cabinet1) 
            panel.photo = cabinet1
            panel.place(x=270 + 180,y=100 + 270)
    if(path == "C:/Users/arcee/Desktop/ui/Import/room29.JPG"or path == "C:/Users/arcee/Desktop/ui/Import/29.JPG"):
        if(type_room == 0):   
            panel = Label(window, image=bed3) 
            panel.photo = bed3
            panel.place(x=270 + 25,y=100 + 25)
            panel = Label(window, image=pot) 
            panel.photo = pot
            panel.place(x=270 + 145,y=100 + 30)
            panel = Label(window, image=cabinet) 
            panel.photo = cabinet
            panel.place(x=270 + 265,y=100 + 30)
            panel = Label(window, image=tvset) 
            panel.photo = tvset
            panel.place(x=270 + 30,y=100 + 270)
        if(type_room == 1): 
#        
            panel = Label(window, image=tvset) 
            panel.photo = tvset
            panel.place(x=270 + 260,y=100 + 50)
#            
            panel = Label(window, image=sofa) 
            panel.photo = sofa
            panel.place(x=270 + 25,y=100 + 20)
#            
            panel = Label(window, image=bookcase) 
            panel.photo = bookcase
            panel.place(x=270 + 140,y=100 + 285)
            
            panel = Label(window, image=pot) 
            panel.photo = pot
            panel.place(x=270 + 25,y=100 + 220)
            
            panel = Label(window, image=cabinet1) 
            panel.photo = cabinet1
            panel.place(x=270 + 25,y=100 + 270)
    if(path == "C:/Users/arcee/Desktop/ui/Import/room30.JPG" or path == "C:/Users/arcee/Desktop/ui/Import/30.JPG"):
        if(type_room == 0):   
            panel = Label(window, image=bed) 
            panel.photo = bed
            panel.place(x=270 + 30,y=100 + 150)
            panel = Label(window, image=pot) 
            panel.photo = pot
            panel.place(x=270 + 145,y=100 + 260)
            panel = Label(window, image=cabinet) 
            panel.photo = cabinet
            panel.place(x=270 + 265,y=100 + 190)
            panel = Label(window, image=tvset) 
            panel.photo = tvset
            panel.place(x=270 + 25,y=100 + 25)
        if(type_room == 1): 
#        
            panel = Label(window, image=tvset) 
            panel.photo = tvset
            panel.place(x=270 + 260,y=100 + 120)
#            
            panel = Label(window, image=sofa) 
            panel.photo = sofa
            panel.place(x=270 + 25,y=100 + 125)
#            
            panel = Label(window, image=bookcase) 
            panel.photo = bookcase
            panel.place(x=270 + 30,y=100 + 25)
            
            panel = Label(window, image=pot) 
            panel.photo = pot
            panel.place(x=270 + 25,y=100 + 80)
            
            panel = Label(window, image=cabinet1) 
            panel.photo = cabinet1
            panel.place(x=270 + 200,y=100 + 270)
    if(path == "C:/Users/arcee/Desktop/ui/Import/room31.JPG"or path == "C:/Users/arcee/Desktop/ui/Import/31.JPG"):
        if(type_room == 0):   
            panel = Label(window, image=bed2) 
            panel.photo = bed2
            panel.place(x=270 + 155,y=100 + 110)
            
            panel = Label(window, image=cabinet2) 
            panel.photo = cabinet2
            panel.place(x=270 + 160,y=100 + 20)
            
            panel = Label(window, image=pot) 
            panel.photo = pot
            panel.place(x=270 + 125,y=100 + 235)
        if(type_room == 1): 
        
            panel = Label(window, image=tvset1) 
            panel.photo = tvset1
            panel.place(x=270 + 25,y=100 + 150)
            
            panel = Label(window, image=sofa1) 
            panel.photo = sofa1
            panel.place(x=270 + 160,y=100 + 120)  
            
            panel = Label(window, image=bookcase1) 
            panel.photo = bookcase1
            panel.place(x=270 + 165,y=100 + 30)
    if(path == "C:/Users/arcee/Desktop/ui/Import/room32.JPG"or path == "C:/Users/arcee/Desktop/ui/Import/32.JPG"):
        if(type_room == 0):   
            panel = Label(window, image=bed2) 
            panel.photo = bed2
            panel.place(x=270 + 30,y=100 + 105)
            panel = Label(window, image=cabinet) 
            panel.photo = cabinet
            panel.place(x=270 + 180,y=100 + 200)
            panel = Label(window, image=pot) 
            panel.photo = pot
            panel.place(x=270 + 130,y=100 + 235)
        if(type_room == 1): 
        
            panel = Label(window, image=tvset1) 
            panel.photo = tvset1
            panel.place(x=270 + 30,y=100 + 130)
            
            panel = Label(window, image=sofa1) 
            panel.photo = sofa1
            panel.place(x=270 + 165,y=100 + 130)
            
            panel = Label(window, image=bookcase1) 
            panel.photo = bookcase1
            panel.place(x=270 + 30,y=100 + 20)
    if(path == "C:/Users/arcee/Desktop/ui/Import/room33.JPG" or path == "C:/Users/arcee/Desktop/ui/Import/33.JPG"):
        if(type_room == 0):   
            panel = Label(window, image=bed) 
            panel.photo = bed
            panel.place(x=270 + 30,y=100 + 30)
            panel = Label(window, image=cabinet) 
            panel.photo = cabinet
            panel.place(x=270 + 190,y=100 + 40)
            panel = Label(window, image=pot) 
            panel.photo = pot
            panel.place(x=270 + 150,y=100 + 40)
        if(type_room == 1): 
            
            panel = Label(window, image=tvset) 
            panel.photo = tvset
            panel.place(x=270 + 30,y=100 + 50)
            
            panel = Label(window, image=sofa1) 
            panel.photo = sofa1
            panel.place(x=270 + 165,y=100 + 30)
            
            

                  
def Size(event=None):
     cv_img = []
     xy = []
     sp = 0
     sp2 =0

     entries = os.listdir("C:/Users/arcee/darknet/build/darknet/x64/result_img/")
     li=[x.split('.')[0] for x in entries]
#     for entry in entries:
#     print(li)
     for entry in li:
#         print(entry)
         mytext = StringVar(value=str(entry) )
         myentry = Entry(window, textvariable=mytext, state = 'readonly')
         myentry.place(x = 1010 , y = 90 + sp)
#         myscroll = Scrollbar(window, orient='horizontal', command=myentry.xview)
#         myentry.config(xscrollcommand=myscroll.set)
#             myscroll.place(x = 1050 , y = 70 + sp)
         sp = sp + 30
     for img in glob.glob("C:/Users/arcee/darknet/build/darknet/x64/result_img/*.jpg"):    
         n= cv2.imread(img)
#         print(img)
         cv_img.append(n)
         im=Image.open(img)
         pix=im.load()
         height,width = im.size
     
#         print(entries)
         if(height>width):
#             print(height)
             mytext = StringVar(value=str(height) )
             myentry2 = Entry(window, textvariable=mytext, state = 'readonly')
             myentry2.place(x = 1100 , y = 90 + sp2)
             myscroll = Scrollbar(window, orient='horizontal', command=myentry.xview)
             myentry.config(xscrollcommand=myscroll.set)
#             myscroll.place(x = 1050 , y = 70 + sp)
             sp2 = sp2 + 30
         if(width>height):
#             print(width)  
             mytext = StringVar(value= str(width) )
             myentry2 = Entry(window, textvariable=mytext, state = 'readonly')
             myentry2.place(x = 1100 , y = 90 + sp2)
             myscroll = Scrollbar(window, orient='horizontal', command=myentry.xview)
             myentry.config(xscrollcommand=myscroll.set)
#             myscroll.place(x = 1050 , y = 70 + sp)
             sp2 = sp2 + 30
#         sizelabel = Label(window, 
#                          text="" + str(img) + "\n" + str(height) + "\n" + str(window))
#         sizelabel.place(x = 1050 , y = 70 + sp)
     if(path == "C:/Users/arcee/Desktop/ui/Import/room1.JPG"):
         if(type_room == 0):   
             objects = os.listdir("C:/Users/arcee/Desktop/ui/furnitures/bed room/small_1/")
             list=[x.split('.')[0] for x in objects]
             for entry in list:
                 print(entry)
                 mytext = StringVar(value=str(entry) )
                 myentry = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry.place(x = 1010 , y = 90 + sp)
                 sp = sp +30
             for img in glob.glob("C:/Users/arcee/Desktop/ui/furnitures/bed room/small_1/*.JPG"): 
                 n= cv2.imread(img)
                 cv_img.append(n)
                 im=Image.open(img)
                 pix=im.load()
                 height,width = im.size
                 mytext = StringVar(value= str(width)+ "x" + str(height))
                 myentry2 = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry2.place(x = 1100 , y = 90 + sp2)
                 myscroll = Scrollbar(window, orient='horizontal', command=myentry.xview)
                 myentry.config(xscrollcommand=myscroll.set)
#              myscroll.place(x = 1050 , y = 70 + sp)
                 sp2 = sp2 + 30
         if(type_room == 1):   
             objects = os.listdir("C:/Users/arcee/Desktop/ui/furnitures/living room/s_1/")
             list=[x.split('.')[0] for x in objects]
             for entry in list:
                 print(entry)
                 mytext = StringVar(value=str(entry) )
                 myentry = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry.place(x = 1010 , y = 90 + sp)
                 sp = sp +30
             for img in glob.glob("C:/Users/arcee/Desktop/ui/furnitures/living room/s_1/*.JPG"): 
                 n= cv2.imread(img)
                 cv_img.append(n)
                 im=Image.open(img)
                 pix=im.load()
                 height,width = im.size
                 mytext = StringVar(value= str(width)+ "x" + str(height))
                 myentry2 = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry2.place(x = 1100 , y = 90 + sp2)
                 myscroll = Scrollbar(window, orient='horizontal', command=myentry.xview)
                 myentry.config(xscrollcommand=myscroll.set)
#              myscroll.place(x = 1050 , y = 70 + sp)
                 sp2 = sp2 + 30
                
     if(path == "C:/Users/arcee/Desktop/ui/Import/room2.JPG"):
         if(type_room == 0):   
             objects = os.listdir("C:/Users/arcee/Desktop/ui/furnitures/bed room/small_1/")
             list=[x.split('.')[0] for x in objects]
             for entry in list:
                 print(entry)
                 mytext = StringVar(value=str(entry) )
                 myentry = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry.place(x = 1010 , y = 90 + sp)
                 sp = sp +30
             for img in glob.glob("C:/Users/arcee/Desktop/ui/furnitures/bed room/small_1/*.JPG"): 
                 n= cv2.imread(img)
                 cv_img.append(n)
                 im=Image.open(img)
                 pix=im.load()
                 height,width = im.size
                 mytext = StringVar(value= str(width)+ "x" + str(height))
                 myentry2 = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry2.place(x = 1100 , y = 90 + sp2)
                 myscroll = Scrollbar(window, orient='horizontal', command=myentry.xview)
                 myentry.config(xscrollcommand=myscroll.set)
#              myscroll.place(x = 1050 , y = 70 + sp)
                 sp2 = sp2 + 30
         if(type_room == 1):   
             objects = os.listdir("C:/Users/arcee/Desktop/ui/furnitures/living room/s_1/")
             list=[x.split('.')[0] for x in objects]
             for entry in list:
                 print(entry)
                 mytext = StringVar(value=str(entry) )
                 myentry = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry.place(x = 1010 , y = 90 + sp)
                 sp = sp +30
             for img in glob.glob("C:/Users/arcee/Desktop/ui/furnitures/living room/s_1/*.JPG"): 
                 n= cv2.imread(img)
                 cv_img.append(n)
                 im=Image.open(img)
                 pix=im.load()
                 height,width = im.size
                 mytext = StringVar(value= str(width)+ "x" + str(height))
                 myentry2 = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry2.place(x = 1100 , y = 90 + sp2)
                 myscroll = Scrollbar(window, orient='horizontal', command=myentry.xview)
                 myentry.config(xscrollcommand=myscroll.set)
#              myscroll.place(x = 1050 , y = 70 + sp)
                 sp2 = sp2 + 30
     if(path == "C:/Users/arcee/Desktop/ui/Import/room3.JPG"):
         if(type_room == 0):   
             objects = os.listdir("C:/Users/arcee/Desktop/ui/furnitures/bed room/small_3/")
             list=[x.split('.')[0] for x in objects]
             for entry in list:
                 print(entry)
                 mytext = StringVar(value=str(entry) )
                 myentry = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry.place(x = 1010 , y = 90 + sp)
                 sp = sp +30
             for img in glob.glob("C:/Users/arcee/Desktop/ui/furnitures/bed room/small_3/*.JPG"): 
                 n= cv2.imread(img)
                 cv_img.append(n)
                 im=Image.open(img)
                 pix=im.load()
                 height,width = im.size
                 mytext = StringVar(value= str(width)+ "x" + str(height))
                 myentry2 = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry2.place(x = 1100 , y = 90 + sp2)
                 myscroll = Scrollbar(window, orient='horizontal', command=myentry.xview)
                 myentry.config(xscrollcommand=myscroll.set)
#              myscroll.place(x = 1050 , y = 70 + sp)
                 sp2 = sp2 + 30
         if(type_room == 1):   
             objects = os.listdir("C:/Users/arcee/Desktop/ui/furnitures/living room/s/")
             list=[x.split('.')[0] for x in objects]
             for entry in list:
                 print(entry)
                 mytext = StringVar(value=str(entry) )
                 myentry = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry.place(x = 1010 , y = 90 + sp)
                 sp = sp +30
             for img in glob.glob("C:/Users/arcee/Desktop/ui/furnitures/living room/s/*.JPG"): 
                 n= cv2.imread(img)
                 cv_img.append(n)
                 im=Image.open(img)
                 pix=im.load()
                 height,width = im.size
                 mytext = StringVar(value= str(width)+ "x" + str(height))
                 myentry2 = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry2.place(x = 1100 , y = 90 + sp2)
                 myscroll = Scrollbar(window, orient='horizontal', command=myentry.xview)
                 myentry.config(xscrollcommand=myscroll.set)
#              myscroll.place(x = 1050 , y = 70 + sp)
                 sp2 = sp2 + 30            
     if(path == "C:/Users/arcee/Desktop/ui/Import/room4.JPG"):
         if(type_room == 0):   
             objects = os.listdir("C:/Users/arcee/Desktop/ui/furnitures/bed room/small_4/")
             list=[x.split('.')[0] for x in objects]
             for entry in list:
                 print(entry)
                 mytext = StringVar(value=str(entry) )
                 myentry = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry.place(x = 1010 , y = 90 + sp)
                 sp = sp +30
             for img in glob.glob("C:/Users/arcee/Desktop/ui/furnitures/bed room/small_4/*.JPG"): 
                 n= cv2.imread(img)
                 cv_img.append(n)
                 im=Image.open(img)
                 pix=im.load()
                 height,width = im.size
                 mytext = StringVar(value= str(width)+ "x" + str(height))
                 myentry2 = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry2.place(x = 1100 , y = 90 + sp2)
                 myscroll = Scrollbar(window, orient='horizontal', command=myentry.xview)
                 myentry.config(xscrollcommand=myscroll.set)
#              myscroll.place(x = 1050 , y = 70 + sp)
                 sp2 = sp2 + 30
         if(type_room == 1):   
             objects = os.listdir("C:/Users/arcee/Desktop/ui/furnitures/living room/s_4/")
             list=[x.split('.')[0] for x in objects]
             for entry in list:
                 print(entry)
                 mytext = StringVar(value=str(entry) )
                 myentry = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry.place(x = 1010 , y = 90 + sp)
                 sp = sp +30
             for img in glob.glob("C:/Users/arcee/Desktop/ui/furnitures/living room/s_4/*.JPG"): 
                 n= cv2.imread(img)
                 cv_img.append(n)
                 im=Image.open(img)
                 pix=im.load()
                 height,width = im.size
                 mytext = StringVar(value= str(width)+ "x" + str(height))
                 myentry2 = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry2.place(x = 1100 , y = 90 + sp2)
                 myscroll = Scrollbar(window, orient='horizontal', command=myentry.xview)
                 myentry.config(xscrollcommand=myscroll.set)
#              myscroll.place(x = 1050 , y = 70 + sp)
                 sp2 = sp2 + 30
     if(path == "C:/Users/arcee/Desktop/ui/Import/room5.JPG"):
         if(type_room == 0):   
             objects = os.listdir("C:/Users/arcee/Desktop/ui/furnitures/bed room/small_5/")
             list=[x.split('.')[0] for x in objects]
             for entry in list:
                 print(entry)
                 mytext = StringVar(value=str(entry) )
                 myentry = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry.place(x = 1010 , y = 90 + sp)
                 sp = sp +30
             for img in glob.glob("C:/Users/arcee/Desktop/ui/furnitures/bed room/small_5/*.JPG"): 
                 n= cv2.imread(img)
                 cv_img.append(n)
                 im=Image.open(img)
                 pix=im.load()
                 height,width = im.size
                 mytext = StringVar(value= str(width)+ "x" + str(height))
                 myentry2 = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry2.place(x = 1100 , y = 90 + sp2)
                 myscroll = Scrollbar(window, orient='horizontal', command=myentry.xview)
                 myentry.config(xscrollcommand=myscroll.set)
#              myscroll.place(x = 1050 , y = 70 + sp)
                 sp2 = sp2 + 30
         if(type_room == 1):   
             objects = os.listdir("C:/Users/arcee/Desktop/ui/furnitures/living room/s_5/")
             list=[x.split('.')[0] for x in objects]
             for entry in list:
                 print(entry)
                 mytext = StringVar(value=str(entry) )
                 myentry = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry.place(x = 1010 , y = 90 + sp)
                 sp = sp +30
             for img in glob.glob("C:/Users/arcee/Desktop/ui/furnitures/living room/s_5/*.JPG"): 
                 n= cv2.imread(img)
                 cv_img.append(n)
                 im=Image.open(img)
                 pix=im.load()
                 height,width = im.size
                 mytext = StringVar(value= str(width)+ "x" + str(height))
                 myentry2 = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry2.place(x = 1100 , y = 90 + sp2)
                 myscroll = Scrollbar(window, orient='horizontal', command=myentry.xview)
                 myentry.config(xscrollcommand=myscroll.set)
#              myscroll.place(x = 1050 , y = 70 + sp)
                 sp2 = sp2 + 30
     if(path == "C:/Users/arcee/Desktop/ui/Import/room6.JPG"):
         if(type_room == 0):   
             objects = os.listdir("C:/Users/arcee/Desktop/ui/furnitures/bed room/small_6/")
             list=[x.split('.')[0] for x in objects]
             for entry in list:
                 print(entry)
                 mytext = StringVar(value=str(entry) )
                 myentry = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry.place(x = 1010 , y = 90 + sp)
                 sp = sp +30
             for img in glob.glob("C:/Users/arcee/Desktop/ui/furnitures/bed room/small_6/*.JPG"): 
                 n= cv2.imread(img)
                 cv_img.append(n)
                 im=Image.open(img)
                 pix=im.load()
                 height,width = im.size
                 mytext = StringVar(value= str(width)+ "x" + str(height))
                 myentry2 = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry2.place(x = 1100 , y = 90 + sp2)
                 myscroll = Scrollbar(window, orient='horizontal', command=myentry.xview)
                 myentry.config(xscrollcommand=myscroll.set)
#              myscroll.place(x = 1050 , y = 70 + sp)
                 sp2 = sp2 + 30
         if(type_room == 1):   
             objects = os.listdir("C:/Users/arcee/Desktop/ui/furnitures/living room/s_6/")
             list=[x.split('.')[0] for x in objects]
             for entry in list:
                 print(entry)
                 mytext = StringVar(value=str(entry) )
                 myentry = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry.place(x = 1010 , y = 90 + sp)
                 sp = sp +30
             for img in glob.glob("C:/Users/arcee/Desktop/ui/furnitures/living room/s_6/*.JPG"): 
                 n= cv2.imread(img)
                 cv_img.append(n)
                 im=Image.open(img)
                 pix=im.load()
                 height,width = im.size
                 mytext = StringVar(value= str(width)+ "x" + str(height))
                 myentry2 = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry2.place(x = 1100 , y = 90 + sp2)
                 myscroll = Scrollbar(window, orient='horizontal', command=myentry.xview)
                 myentry.config(xscrollcommand=myscroll.set)
#              myscroll.place(x = 1050 , y = 70 + sp)
                 sp2 = sp2 + 30
     if(path == "C:/Users/arcee/Desktop/ui/Import/room7.JPG"):
         if(type_room == 0):   
             objects = os.listdir("C:/Users/arcee/Desktop/ui/furnitures/bed room/small_7/")
             list=[x.split('.')[0] for x in objects]
             for entry in list:
                 print(entry)
                 mytext = StringVar(value=str(entry) )
                 myentry = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry.place(x = 1010 , y = 90 + sp)
                 sp = sp +30
             for img in glob.glob("C:/Users/arcee/Desktop/ui/furnitures/bed room/small_7/*.JPG"): 
                 n= cv2.imread(img)
                 cv_img.append(n)
                 im=Image.open(img)
                 pix=im.load()
                 height,width = im.size
                 mytext = StringVar(value= str(width)+ "x" + str(height))
                 myentry2 = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry2.place(x = 1100 , y = 90 + sp2)
                 myscroll = Scrollbar(window, orient='horizontal', command=myentry.xview)
                 myentry.config(xscrollcommand=myscroll.set)
#              myscroll.place(x = 1050 , y = 70 + sp)
                 sp2 = sp2 + 30
         if(type_room == 1):   
             objects = os.listdir("C:/Users/arcee/Desktop/ui/furnitures/living room/s/")
             list=[x.split('.')[0] for x in objects]
             for entry in list:
                 print(entry)
                 mytext = StringVar(value=str(entry) )
                 myentry = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry.place(x = 1010 , y = 90 + sp)
                 sp = sp +30
             for img in glob.glob("C:/Users/arcee/Desktop/ui/furnitures/living room/s/*.JPG"): 
                 n= cv2.imread(img)
                 cv_img.append(n)
                 im=Image.open(img)
                 pix=im.load()
                 height,width = im.size
                 mytext = StringVar(value= str(width)+ "x" + str(height))
                 myentry2 = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry2.place(x = 1100 , y = 90 + sp2)
                 myscroll = Scrollbar(window, orient='horizontal', command=myentry.xview)
                 myentry.config(xscrollcommand=myscroll.set)
#              myscroll.place(x = 1050 , y = 70 + sp)
                 sp2 = sp2 + 30
     if(path == "C:/Users/arcee/Desktop/ui/Import/room8.JPG"):
         if(type_room == 0):   
             objects = os.listdir("C:/Users/arcee/Desktop/ui/furnitures/bed room/small_7/")
             list=[x.split('.')[0] for x in objects]
             for entry in list:
                 print(entry)
                 mytext = StringVar(value=str(entry) )
                 myentry = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry.place(x = 1010 , y = 90 + sp)
                 sp = sp +30
             for img in glob.glob("C:/Users/arcee/Desktop/ui/furnitures/bed room/small_7/*.JPG"): 
                 n= cv2.imread(img)
                 cv_img.append(n)
                 im=Image.open(img)
                 pix=im.load()
                 height,width = im.size
                 mytext = StringVar(value= str(width)+ "x" + str(height))
                 myentry2 = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry2.place(x = 1100 , y = 90 + sp2)
                 myscroll = Scrollbar(window, orient='horizontal', command=myentry.xview)
                 myentry.config(xscrollcommand=myscroll.set)
#              myscroll.place(x = 1050 , y = 70 + sp)
                 sp2 = sp2 + 30
         if(type_room == 1):   
             objects = os.listdir("C:/Users/arcee/Desktop/ui/furnitures/living room/s_8/")
             list=[x.split('.')[0] for x in objects]
             for entry in list:
                 print(entry)
                 mytext = StringVar(value=str(entry) )
                 myentry = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry.place(x = 1010 , y = 90 + sp)
                 sp = sp +30
             for img in glob.glob("C:/Users/arcee/Desktop/ui/furnitures/living room/s_8/*.JPG"): 
                 n= cv2.imread(img)
                 cv_img.append(n)
                 im=Image.open(img)
                 pix=im.load()
                 height,width = im.size
                 mytext = StringVar(value= str(width)+ "x" + str(height))
                 myentry2 = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry2.place(x = 1100 , y = 90 + sp2)
                 myscroll = Scrollbar(window, orient='horizontal', command=myentry.xview)
                 myentry.config(xscrollcommand=myscroll.set)
#              myscroll.place(x = 1050 , y = 70 + sp)
                 sp2 = sp2 + 30
     if(path == "C:/Users/arcee/Desktop/ui/Import/room9.JPG"):
         if(type_room == 0):   
             objects = os.listdir("C:/Users/arcee/Desktop/ui/furnitures/bed room/small_7/")
             list=[x.split('.')[0] for x in objects]
             for entry in list:
                 print(entry)
                 mytext = StringVar(value=str(entry) )
                 myentry = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry.place(x = 1010 , y = 90 + sp)
                 sp = sp +30
             for img in glob.glob("C:/Users/arcee/Desktop/ui/furnitures/bed room/small_7/*.JPG"): 
                 n= cv2.imread(img)
                 cv_img.append(n)
                 im=Image.open(img)
                 pix=im.load()
                 height,width = im.size
                 mytext = StringVar(value= str(width)+ "x" + str(height))
                 myentry2 = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry2.place(x = 1100 , y = 90 + sp2)
                 myscroll = Scrollbar(window, orient='horizontal', command=myentry.xview)
                 myentry.config(xscrollcommand=myscroll.set)
#              myscroll.place(x = 1050 , y = 70 + sp)
                 sp2 = sp2 + 30
         if(type_room == 1):   
             objects = os.listdir("C:/Users/arcee/Desktop/ui/furnitures/living room/s_7/")
             list=[x.split('.')[0] for x in objects]
             for entry in list:
                 print(entry)
                 mytext = StringVar(value=str(entry) )
                 myentry = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry.place(x = 1010 , y = 90 + sp)
                 sp = sp +30
             for img in glob.glob("C:/Users/arcee/Desktop/ui/furnitures/living room/s_7/*.JPG"): 
                 n= cv2.imread(img)
                 cv_img.append(n)
                 im=Image.open(img)
                 pix=im.load()
                 height,width = im.size
                 mytext = StringVar(value= str(width)+ "x" + str(height))
                 myentry2 = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry2.place(x = 1100 , y = 90 + sp2)
                 myscroll = Scrollbar(window, orient='horizontal', command=myentry.xview)
                 myentry.config(xscrollcommand=myscroll.set)
#              myscroll.place(x = 1050 , y = 70 + sp)
                 sp2 = sp2 + 30
     if(path == "C:/Users/arcee/Desktop/ui/Import/room10.JPG"):
         if(type_room == 0):   
             objects = os.listdir("C:/Users/arcee/Desktop/ui/furnitures/bed room/small_7/")
             list=[x.split('.')[0] for x in objects]
             for entry in list:
                 print(entry)
                 mytext = StringVar(value=str(entry) )
                 myentry = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry.place(x = 1010 , y = 90 + sp)
                 sp = sp +30
             for img in glob.glob("C:/Users/arcee/Desktop/ui/furnitures/bed room/small_7/*.JPG"): 
                 n= cv2.imread(img)
                 cv_img.append(n)
                 im=Image.open(img)
                 pix=im.load()
                 height,width = im.size
                 mytext = StringVar(value= str(width)+ "x" + str(height))
                 myentry2 = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry2.place(x = 1100 , y = 90 + sp2)
                 myscroll = Scrollbar(window, orient='horizontal', command=myentry.xview)
                 myentry.config(xscrollcommand=myscroll.set)
#              myscroll.place(x = 1050 , y = 70 + sp)
                 sp2 = sp2 + 30
         if(type_room == 1):   
             objects = os.listdir("C:/Users/arcee/Desktop/ui/furnitures/living room/s_7/")
             list=[x.split('.')[0] for x in objects]
             for entry in list:
                 print(entry)
                 mytext = StringVar(value=str(entry) )
                 myentry = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry.place(x = 1010 , y = 90 + sp)
                 sp = sp +30
             for img in glob.glob("C:/Users/arcee/Desktop/ui/furnitures/living room/s_7/*.JPG"): 
                 n= cv2.imread(img)
                 cv_img.append(n)
                 im=Image.open(img)
                 pix=im.load()
                 height,width = im.size
                 mytext = StringVar(value= str(width)+ "x" + str(height))
                 myentry2 = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry2.place(x = 1100 , y = 90 + sp2)
                 myscroll = Scrollbar(window, orient='horizontal', command=myentry.xview)
                 myentry.config(xscrollcommand=myscroll.set)
#              myscroll.place(x = 1050 , y = 70 + sp)
                 sp2 = sp2 + 30
     if(path == "C:/Users/arcee/Desktop/ui/Import/room11.JPG"):
         if(type_room == 0):   
             objects = os.listdir("C:/Users/arcee/Desktop/ui/furnitures/bed room/small_7/")
             list=[x.split('.')[0] for x in objects]
             for entry in list:
                 print(entry)
                 mytext = StringVar(value=str(entry) )
                 myentry = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry.place(x = 1010 , y = 90 + sp)
                 sp = sp +30
             for img in glob.glob("C:/Users/arcee/Desktop/ui/furnitures/bed room/small_7/*.JPG"): 
                 n= cv2.imread(img)
                 cv_img.append(n)
                 im=Image.open(img)
                 pix=im.load()
                 height,width = im.size
                 mytext = StringVar(value= str(width)+ "x" + str(height))
                 myentry2 = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry2.place(x = 1100 , y = 90 + sp2)
                 myscroll = Scrollbar(window, orient='horizontal', command=myentry.xview)
                 myentry.config(xscrollcommand=myscroll.set)
#              myscroll.place(x = 1050 , y = 70 + sp)
                 sp2 = sp2 + 30
         if(type_room == 1):   
             objects = os.listdir("C:/Users/arcee/Desktop/ui/furnitures/living room/s_7/")
             list=[x.split('.')[0] for x in objects]
             for entry in list:
                 print(entry)
                 mytext = StringVar(value=str(entry) )
                 myentry = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry.place(x = 1010 , y = 90 + sp)
                 sp = sp +30
             for img in glob.glob("C:/Users/arcee/Desktop/ui/furnitures/living room/s_7/*.JPG"): 
                 n= cv2.imread(img)
                 cv_img.append(n)
                 im=Image.open(img)
                 pix=im.load()
                 height,width = im.size
                 mytext = StringVar(value= str(width)+ "x" + str(height))
                 myentry2 = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry2.place(x = 1100 , y = 90 + sp2)
                 myscroll = Scrollbar(window, orient='horizontal', command=myentry.xview)
                 myentry.config(xscrollcommand=myscroll.set)
#              myscroll.place(x = 1050 , y = 70 + sp)
                 sp2 = sp2 + 30
     if(path == "C:/Users/arcee/Desktop/ui/Import/room12.JPG"):
         if(type_room == 0):   
             objects = os.listdir("C:/Users/arcee/Desktop/ui/furnitures/bed room/mid_12/")
             list=[x.split('.')[0] for x in objects]
             for entry in list:
                 print(entry)
                 mytext = StringVar(value=str(entry) )
                 myentry = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry.place(x = 1010 , y = 90 + sp)
                 sp = sp +30
             for img in glob.glob("C:/Users/arcee/Desktop/ui/furnitures/bed room/mid_12/*.JPG"): 
                 n= cv2.imread(img)
                 cv_img.append(n)
                 im=Image.open(img)
                 pix=im.load()
                 height,width = im.size
                 mytext = StringVar(value= str(width)+ "x" + str(height))
                 myentry2 = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry2.place(x = 1100 , y = 90 + sp2)
                 myscroll = Scrollbar(window, orient='horizontal', command=myentry.xview)
                 myentry.config(xscrollcommand=myscroll.set)
#              myscroll.place(x = 1050 , y = 70 + sp)
                 sp2 = sp2 + 30
         if(type_room == 1):   
             objects = os.listdir("C:/Users/arcee/Desktop/ui/furnitures/living room/m/")
             list=[x.split('.')[0] for x in objects]
             for entry in list:
                 print(entry)
                 mytext = StringVar(value=str(entry) )
                 myentry = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry.place(x = 1010 , y = 90 + sp)
                 sp = sp +30
             for img in glob.glob("C:/Users/arcee/Desktop/ui/furnitures/living room/m/*.JPG"): 
                 n= cv2.imread(img)
                 cv_img.append(n)
                 im=Image.open(img)
                 pix=im.load()
                 height,width = im.size
                 mytext = StringVar(value= str(width)+ "x" + str(height))
                 myentry2 = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry2.place(x = 1100 , y = 90 + sp2)
                 myscroll = Scrollbar(window, orient='horizontal', command=myentry.xview)
                 myentry.config(xscrollcommand=myscroll.set)
#              myscroll.place(x = 1050 , y = 70 + sp)
                 sp2 = sp2 + 30
     if(path == "C:/Users/arcee/Desktop/ui/Import/room13.JPG"):
         if(type_room == 0):   
             objects = os.listdir("C:/Users/arcee/Desktop/ui/furnitures/bed room/large_25/")
             list=[x.split('.')[0] for x in objects]
             for entry in list:
                 print(entry)
                 mytext = StringVar(value=str(entry) )
                 myentry = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry.place(x = 1010 , y = 90 + sp)
                 sp = sp +30
             for img in glob.glob("C:/Users/arcee/Desktop/ui/furnitures/bed room/large_25/*.JPG"): 
                 n= cv2.imread(img)
                 cv_img.append(n)
                 im=Image.open(img)
                 pix=im.load()
                 height,width = im.size
                 mytext = StringVar(value= str(width)+ "x" + str(height))
                 myentry2 = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry2.place(x = 1100 , y = 90 + sp2)
                 myscroll = Scrollbar(window, orient='horizontal', command=myentry.xview)
                 myentry.config(xscrollcommand=myscroll.set)
#              myscroll.place(x = 1050 , y = 70 + sp)
                 sp2 = sp2 + 30
         if(type_room == 1):   
             objects = os.listdir("C:/Users/arcee/Desktop/ui/furnitures/living room/l_25/")
             list=[x.split('.')[0] for x in objects]
             for entry in list:
                 print(entry)
                 mytext = StringVar(value=str(entry) )
                 myentry = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry.place(x = 1010 , y = 90 + sp)
                 sp = sp +30
             for img in glob.glob("C:/Users/arcee/Desktop/ui/furnitures/living room/l_25/*.JPG"): 
                 n= cv2.imread(img)
                 cv_img.append(n)
                 im=Image.open(img)
                 pix=im.load()
                 height,width = im.size
                 mytext = StringVar(value= str(width)+ "x" + str(height))
                 myentry2 = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry2.place(x = 1100 , y = 90 + sp2)
                 myscroll = Scrollbar(window, orient='horizontal', command=myentry.xview)
                 myentry.config(xscrollcommand=myscroll.set)
#              myscroll.place(x = 1050 , y = 70 + sp)
                 sp2 = sp2 + 30
     if(path == "C:/Users/arcee/Desktop/ui/Import/room14.JPG"):
         if(type_room == 0):   
             objects = os.listdir("C:/Users/arcee/Desktop/ui/furnitures/bed room/large_25/")
             list=[x.split('.')[0] for x in objects]
             for entry in list:
                 print(entry)
                 mytext = StringVar(value=str(entry) )
                 myentry = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry.place(x = 1010 , y = 90 + sp)
                 sp = sp +30
             for img in glob.glob("C:/Users/arcee/Desktop/ui/furnitures/bed room/large_25/*.JPG"): 
                 n= cv2.imread(img)
                 cv_img.append(n)
                 im=Image.open(img)
                 pix=im.load()
                 height,width = im.size
                 mytext = StringVar(value= str(width)+ "x" + str(height))
                 myentry2 = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry2.place(x = 1100 , y = 90 + sp2)
                 myscroll = Scrollbar(window, orient='horizontal', command=myentry.xview)
                 myentry.config(xscrollcommand=myscroll.set)
#              myscroll.place(x = 1050 , y = 70 + sp)
                 sp2 = sp2 + 30
         if(type_room == 1):   
             objects = os.listdir("C:/Users/arcee/Desktop/ui/furnitures/living room/l_25/")
             list=[x.split('.')[0] for x in objects]
             for entry in list:
                 print(entry)
                 mytext = StringVar(value=str(entry) )
                 myentry = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry.place(x = 1010 , y = 90 + sp)
                 sp = sp +30
             for img in glob.glob("C:/Users/arcee/Desktop/ui/furnitures/living room/l_25/*.JPG"): 
                 n= cv2.imread(img)
                 cv_img.append(n)
                 im=Image.open(img)
                 pix=im.load()
                 height,width = im.size
                 mytext = StringVar(value= str(width)+ "x" + str(height))
                 myentry2 = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry2.place(x = 1100 , y = 90 + sp2)
                 myscroll = Scrollbar(window, orient='horizontal', command=myentry.xview)
                 myentry.config(xscrollcommand=myscroll.set)
#              myscroll.place(x = 1050 , y = 70 + sp)
                 sp2 = sp2 + 30
     if(path == "C:/Users/arcee/Desktop/ui/Import/room15.JPG"):
         if(type_room == 0):   
             objects = os.listdir("C:/Users/arcee/Desktop/ui/furnitures/bed room/large_25/")
             list=[x.split('.')[0] for x in objects]
             for entry in list:
                 print(entry)
                 mytext = StringVar(value=str(entry) )
                 myentry = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry.place(x = 1010 , y = 90 + sp)
                 sp = sp +30
             for img in glob.glob("C:/Users/arcee/Desktop/ui/furnitures/bed room/large_25/*.JPG"): 
                 n= cv2.imread(img)
                 cv_img.append(n)
                 im=Image.open(img)
                 pix=im.load()
                 height,width = im.size
                 mytext = StringVar(value= str(width)+ "x" + str(height))
                 myentry2 = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry2.place(x = 1100 , y = 90 + sp2)
                 myscroll = Scrollbar(window, orient='horizontal', command=myentry.xview)
                 myentry.config(xscrollcommand=myscroll.set)
#              myscroll.place(x = 1050 , y = 70 + sp)
                 sp2 = sp2 + 30
         if(type_room == 1):   
             objects = os.listdir("C:/Users/arcee/Desktop/ui/furnitures/living room/l_25/")
             list=[x.split('.')[0] for x in objects]
             for entry in list:
                 print(entry)
                 mytext = StringVar(value=str(entry) )
                 myentry = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry.place(x = 1010 , y = 90 + sp)
                 sp = sp +30
             for img in glob.glob("C:/Users/arcee/Desktop/ui/furnitures/living room/l_25/*.JPG"): 
                 n= cv2.imread(img)
                 cv_img.append(n)
                 im=Image.open(img)
                 pix=im.load()
                 height,width = im.size
                 mytext = StringVar(value= str(width)+ "x" + str(height))
                 myentry2 = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry2.place(x = 1100 , y = 90 + sp2)
                 myscroll = Scrollbar(window, orient='horizontal', command=myentry.xview)
                 myentry.config(xscrollcommand=myscroll.set)
#              myscroll.place(x = 1050 , y = 70 + sp)
                 sp2 = sp2 + 30
     if(path == "C:/Users/arcee/Desktop/ui/Import/room16.JPG"):
         if(type_room == 0):   
             objects = os.listdir("C:/Users/arcee/Desktop/ui/furnitures/bed room/large_25/")
             list=[x.split('.')[0] for x in objects]
             for entry in list:
                 print(entry)
                 mytext = StringVar(value=str(entry) )
                 myentry = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry.place(x = 1010 , y = 90 + sp)
                 sp = sp +30
             for img in glob.glob("C:/Users/arcee/Desktop/ui/furnitures/bed room/large_25/*.JPG"): 
                 n= cv2.imread(img)
                 cv_img.append(n)
                 im=Image.open(img)
                 pix=im.load()
                 height,width = im.size
                 mytext = StringVar(value= str(width)+ "x" + str(height))
                 myentry2 = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry2.place(x = 1100 , y = 90 + sp2)
                 myscroll = Scrollbar(window, orient='horizontal', command=myentry.xview)
                 myentry.config(xscrollcommand=myscroll.set)
#              myscroll.place(x = 1050 , y = 70 + sp)
                 sp2 = sp2 + 30
         if(type_room == 1):   
             objects = os.listdir("C:/Users/arcee/Desktop/ui/furnitures/living room/l_25/")
             list=[x.split('.')[0] for x in objects]
             for entry in list:
                 print(entry)
                 mytext = StringVar(value=str(entry) )
                 myentry = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry.place(x = 1010 , y = 90 + sp)
                 sp = sp +30
             for img in glob.glob("C:/Users/arcee/Desktop/ui/furnitures/living room/l_25/*.JPG"): 
                 n= cv2.imread(img)
                 cv_img.append(n)
                 im=Image.open(img)
                 pix=im.load()
                 height,width = im.size
                 mytext = StringVar(value= str(width)+ "x" + str(height))
                 myentry2 = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry2.place(x = 1100 , y = 90 + sp2)
                 myscroll = Scrollbar(window, orient='horizontal', command=myentry.xview)
                 myentry.config(xscrollcommand=myscroll.set)
#              myscroll.place(x = 1050 , y = 70 + sp)
                 sp2 = sp2 + 30
     if(path == "C:/Users/arcee/Desktop/ui/Import/room17.JPG"):
         if(type_room == 0):   
             objects = os.listdir("C:/Users/arcee/Desktop/ui/furnitures/bed room/large_25/")
             list=[x.split('.')[0] for x in objects]
             for entry in list:
                 print(entry)
                 mytext = StringVar(value=str(entry) )
                 myentry = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry.place(x = 1010 , y = 90 + sp)
                 sp = sp +30
             for img in glob.glob("C:/Users/arcee/Desktop/ui/furnitures/bed room/large_25/*.JPG"): 
                 n= cv2.imread(img)
                 cv_img.append(n)
                 im=Image.open(img)
                 pix=im.load()
                 height,width = im.size
                 mytext = StringVar(value= str(width)+ "x" + str(height))
                 myentry2 = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry2.place(x = 1100 , y = 90 + sp2)
                 myscroll = Scrollbar(window, orient='horizontal', command=myentry.xview)
                 myentry.config(xscrollcommand=myscroll.set)
#              myscroll.place(x = 1050 , y = 70 + sp)
                 sp2 = sp2 + 30
         if(type_room == 1):   
             objects = os.listdir("C:/Users/arcee/Desktop/ui/furnitures/living room/l_25/")
             list=[x.split('.')[0] for x in objects]
             for entry in list:
                 print(entry)
                 mytext = StringVar(value=str(entry) )
                 myentry = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry.place(x = 1010 , y = 90 + sp)
                 sp = sp +30
             for img in glob.glob("C:/Users/arcee/Desktop/ui/furnitures/living room/l_25/*.JPG"): 
                 n= cv2.imread(img)
                 cv_img.append(n)
                 im=Image.open(img)
                 pix=im.load()
                 height,width = im.size
                 mytext = StringVar(value= str(width)+ "x" + str(height))
                 myentry2 = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry2.place(x = 1100 , y = 90 + sp2)
                 myscroll = Scrollbar(window, orient='horizontal', command=myentry.xview)
                 myentry.config(xscrollcommand=myscroll.set)
#              myscroll.place(x = 1050 , y = 70 + sp)
                 sp2 = sp2 + 30
     if(path == "C:/Users/arcee/Desktop/ui/Import/room18.JPG"):
         if(type_room == 0):   
             objects = os.listdir("C:/Users/arcee/Desktop/ui/furnitures/bed room/large_25/")
             list=[x.split('.')[0] for x in objects]
             for entry in list:
                 print(entry)
                 mytext = StringVar(value=str(entry) )
                 myentry = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry.place(x = 1010 , y = 90 + sp)
                 sp = sp +30
             for img in glob.glob("C:/Users/arcee/Desktop/ui/furnitures/bed room/large_25/*.JPG"): 
                 n= cv2.imread(img)
                 cv_img.append(n)
                 im=Image.open(img)
                 pix=im.load()
                 height,width = im.size
                 mytext = StringVar(value= str(width)+ "x" + str(height))
                 myentry2 = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry2.place(x = 1100 , y = 90 + sp2)
                 myscroll = Scrollbar(window, orient='horizontal', command=myentry.xview)
                 myentry.config(xscrollcommand=myscroll.set)
#              myscroll.place(x = 1050 , y = 70 + sp)
                 sp2 = sp2 + 30
         if(type_room == 1):   
             objects = os.listdir("C:/Users/arcee/Desktop/ui/furnitures/living room/l_25/")
             list=[x.split('.')[0] for x in objects]
             for entry in list:
                 print(entry)
                 mytext = StringVar(value=str(entry) )
                 myentry = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry.place(x = 1010 , y = 90 + sp)
                 sp = sp +30
             for img in glob.glob("C:/Users/arcee/Desktop/ui/furnitures/living room/l_25/*.JPG"): 
                 n= cv2.imread(img)
                 cv_img.append(n)
                 im=Image.open(img)
                 pix=im.load()
                 height,width = im.size
                 mytext = StringVar(value= str(width)+ "x" + str(height))
                 myentry2 = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry2.place(x = 1100 , y = 90 + sp2)
                 myscroll = Scrollbar(window, orient='horizontal', command=myentry.xview)
                 myentry.config(xscrollcommand=myscroll.set)
#              myscroll.place(x = 1050 , y = 70 + sp)
                 sp2 = sp2 + 30
     if(path == "C:/Users/arcee/Desktop/ui/Import/room19.JPG"):
         if(type_room == 0):   
             objects = os.listdir("C:/Users/arcee/Desktop/ui/furnitures/bed room/large_25/")
             list=[x.split('.')[0] for x in objects]
             for entry in list:
                 print(entry)
                 mytext = StringVar(value=str(entry) )
                 myentry = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry.place(x = 1010 , y = 90 + sp)
                 sp = sp +30
             for img in glob.glob("C:/Users/arcee/Desktop/ui/furnitures/bed room/large_25/*.JPG"): 
                 n= cv2.imread(img)
                 cv_img.append(n)
                 im=Image.open(img)
                 pix=im.load()
                 height,width = im.size
                 mytext = StringVar(value= str(width)+ "x" + str(height))
                 myentry2 = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry2.place(x = 1100 , y = 90 + sp2)
                 myscroll = Scrollbar(window, orient='horizontal', command=myentry.xview)
                 myentry.config(xscrollcommand=myscroll.set)
#              myscroll.place(x = 1050 , y = 70 + sp)
                 sp2 = sp2 + 30
         if(type_room == 1):   
             objects = os.listdir("C:/Users/arcee/Desktop/ui/furnitures/living room/l_25/")
             list=[x.split('.')[0] for x in objects]
             for entry in list:
                 print(entry)
                 mytext = StringVar(value=str(entry) )
                 myentry = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry.place(x = 1010 , y = 90 + sp)
                 sp = sp +30
             for img in glob.glob("C:/Users/arcee/Desktop/ui/furnitures/living room/l_25/*.JPG"): 
                 n= cv2.imread(img)
                 cv_img.append(n)
                 im=Image.open(img)
                 pix=im.load()
                 height,width = im.size
                 mytext = StringVar(value= str(width)+ "x" + str(height))
                 myentry2 = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry2.place(x = 1100 , y = 90 + sp2)
                 myscroll = Scrollbar(window, orient='horizontal', command=myentry.xview)
                 myentry.config(xscrollcommand=myscroll.set)
#              myscroll.place(x = 1050 , y = 70 + sp)
                 sp2 = sp2 + 30
     if(path == "C:/Users/arcee/Desktop/ui/Import/room20.JPG"):
         if(type_room == 0):   
             objects = os.listdir("C:/Users/arcee/Desktop/ui/furnitures/bed room/large_25/")
             list=[x.split('.')[0] for x in objects]
             for entry in list:
                 print(entry)
                 mytext = StringVar(value=str(entry) )
                 myentry = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry.place(x = 1010 , y = 90 + sp)
                 sp = sp +30
             for img in glob.glob("C:/Users/arcee/Desktop/ui/furnitures/bed room/large_25/*.JPG"): 
                 n= cv2.imread(img)
                 cv_img.append(n)
                 im=Image.open(img)
                 pix=im.load()
                 height,width = im.size
                 mytext = StringVar(value= str(width)+ "x" + str(height))
                 myentry2 = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry2.place(x = 1100 , y = 90 + sp2)
                 myscroll = Scrollbar(window, orient='horizontal', command=myentry.xview)
                 myentry.config(xscrollcommand=myscroll.set)
#              myscroll.place(x = 1050 , y = 70 + sp)
                 sp2 = sp2 + 30
         if(type_room == 1):   
             objects = os.listdir("C:/Users/arcee/Desktop/ui/furnitures/living room/l_25/")
             list=[x.split('.')[0] for x in objects]
             for entry in list:
                 print(entry)
                 mytext = StringVar(value=str(entry) )
                 myentry = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry.place(x = 1010 , y = 90 + sp)
                 sp = sp +30
             for img in glob.glob("C:/Users/arcee/Desktop/ui/furnitures/living room/l_25/*.JPG"): 
                 n= cv2.imread(img)
                 cv_img.append(n)
                 im=Image.open(img)
                 pix=im.load()
                 height,width = im.size
                 mytext = StringVar(value= str(width)+ "x" + str(height))
                 myentry2 = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry2.place(x = 1100 , y = 90 + sp2)
                 myscroll = Scrollbar(window, orient='horizontal', command=myentry.xview)
                 myentry.config(xscrollcommand=myscroll.set)
#              myscroll.place(x = 1050 , y = 70 + sp)
                 sp2 = sp2 + 30
     if(path == "C:/Users/arcee/Desktop/ui/Import/room21.JPG"):
         if(type_room == 0):   
             objects = os.listdir("C:/Users/arcee/Desktop/ui/furnitures/bed room/large_25/")
             list=[x.split('.')[0] for x in objects]
             for entry in list:
                 print(entry)
                 mytext = StringVar(value=str(entry) )
                 myentry = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry.place(x = 1010 , y = 90 + sp)
                 sp = sp +30
             for img in glob.glob("C:/Users/arcee/Desktop/ui/furnitures/bed room/large_25/*.JPG"): 
                 n= cv2.imread(img)
                 cv_img.append(n)
                 im=Image.open(img)
                 pix=im.load()
                 height,width = im.size
                 mytext = StringVar(value= str(width)+ "x" + str(height))
                 myentry2 = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry2.place(x = 1100 , y = 90 + sp2)
                 myscroll = Scrollbar(window, orient='horizontal', command=myentry.xview)
                 myentry.config(xscrollcommand=myscroll.set)
#              myscroll.place(x = 1050 , y = 70 + sp)
                 sp2 = sp2 + 30
         if(type_room == 1):   
             objects = os.listdir("C:/Users/arcee/Desktop/ui/furnitures/living room/l_25/")
             list=[x.split('.')[0] for x in objects]
             for entry in list:
                 print(entry)
                 mytext = StringVar(value=str(entry) )
                 myentry = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry.place(x = 1010 , y = 90 + sp)
                 sp = sp +30
             for img in glob.glob("C:/Users/arcee/Desktop/ui/furnitures/living room/l_25/*.JPG"): 
                 n= cv2.imread(img)
                 cv_img.append(n)
                 im=Image.open(img)
                 pix=im.load()
                 height,width = im.size
                 mytext = StringVar(value= str(width)+ "x" + str(height))
                 myentry2 = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry2.place(x = 1100 , y = 90 + sp2)
                 myscroll = Scrollbar(window, orient='horizontal', command=myentry.xview)
                 myentry.config(xscrollcommand=myscroll.set)
#              myscroll.place(x = 1050 , y = 70 + sp)
                 sp2 = sp2 + 30
     if(path == "C:/Users/arcee/Desktop/ui/Import/room22.JPG"):
         if(type_room == 0):   
             objects = os.listdir("C:/Users/arcee/Desktop/ui/furnitures/bed room/large_25/")
             list=[x.split('.')[0] for x in objects]
             for entry in list:
                 print(entry)
                 mytext = StringVar(value=str(entry) )
                 myentry = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry.place(x = 1010 , y = 90 + sp)
                 sp = sp +30
             for img in glob.glob("C:/Users/arcee/Desktop/ui/furnitures/bed room/large_25/*.JPG"): 
                 n= cv2.imread(img)
                 cv_img.append(n)
                 im=Image.open(img)
                 pix=im.load()
                 height,width = im.size
                 mytext = StringVar(value= str(width)+ "x" + str(height))
                 myentry2 = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry2.place(x = 1100 , y = 90 + sp2)
                 myscroll = Scrollbar(window, orient='horizontal', command=myentry.xview)
                 myentry.config(xscrollcommand=myscroll.set)
#              myscroll.place(x = 1050 , y = 70 + sp)
                 sp2 = sp2 + 30
         if(type_room == 1):   
             objects = os.listdir("C:/Users/arcee/Desktop/ui/furnitures/living room/l_25/")
             list=[x.split('.')[0] for x in objects]
             for entry in list:
                 print(entry)
                 mytext = StringVar(value=str(entry) )
                 myentry = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry.place(x = 1010 , y = 90 + sp)
                 sp = sp +30
             for img in glob.glob("C:/Users/arcee/Desktop/ui/furnitures/living room/l_25/*.JPG"): 
                 n= cv2.imread(img)
                 cv_img.append(n)
                 im=Image.open(img)
                 pix=im.load()
                 height,width = im.size
                 mytext = StringVar(value= str(width)+ "x" + str(height))
                 myentry2 = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry2.place(x = 1100 , y = 90 + sp2)
                 myscroll = Scrollbar(window, orient='horizontal', command=myentry.xview)
                 myentry.config(xscrollcommand=myscroll.set)
#              myscroll.place(x = 1050 , y = 70 + sp)
                 sp2 = sp2 + 30
     if(path == "C:/Users/arcee/Desktop/ui/Import/room23.JPG"):
         if(type_room == 0):   
             objects = os.listdir("C:/Users/arcee/Desktop/ui/furnitures/bed room/large_25/")
             list=[x.split('.')[0] for x in objects]
             for entry in list:
                 print(entry)
                 mytext = StringVar(value=str(entry) )
                 myentry = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry.place(x = 1010 , y = 90 + sp)
                 sp = sp +30
             for img in glob.glob("C:/Users/arcee/Desktop/ui/furnitures/bed room/large_25/*.JPG"): 
                 n= cv2.imread(img)
                 cv_img.append(n)
                 im=Image.open(img)
                 pix=im.load()
                 height,width = im.size
                 mytext = StringVar(value= str(width)+ "x" + str(height))
                 myentry2 = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry2.place(x = 1100 , y = 90 + sp2)
                 myscroll = Scrollbar(window, orient='horizontal', command=myentry.xview)
                 myentry.config(xscrollcommand=myscroll.set)
#              myscroll.place(x = 1050 , y = 70 + sp)
                 sp2 = sp2 + 30
         if(type_room == 1):   
             objects = os.listdir("C:/Users/arcee/Desktop/ui/furnitures/living room/l_25/")
             list=[x.split('.')[0] for x in objects]
             for entry in list:
                 print(entry)
                 mytext = StringVar(value=str(entry) )
                 myentry = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry.place(x = 1010 , y = 90 + sp)
                 sp = sp +30
             for img in glob.glob("C:/Users/arcee/Desktop/ui/furnitures/living room/l_25/*.JPG"): 
                 n= cv2.imread(img)
                 cv_img.append(n)
                 im=Image.open(img)
                 pix=im.load()
                 height,width = im.size
                 mytext = StringVar(value= str(width)+ "x" + str(height))
                 myentry2 = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry2.place(x = 1100 , y = 90 + sp2)
                 myscroll = Scrollbar(window, orient='horizontal', command=myentry.xview)
                 myentry.config(xscrollcommand=myscroll.set)
#              myscroll.place(x = 1050 , y = 70 + sp)
                 sp2 = sp2 + 30
     if(path == "C:/Users/arcee/Desktop/ui/Import/room24.JPG"):
         if(type_room == 0):   
             objects = os.listdir("C:/Users/arcee/Desktop/ui/furnitures/bed room/large_25/")
             list=[x.split('.')[0] for x in objects]
             for entry in list:
                 print(entry)
                 mytext = StringVar(value=str(entry) )
                 myentry = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry.place(x = 1010 , y = 90 + sp)
                 sp = sp +30
             for img in glob.glob("C:/Users/arcee/Desktop/ui/furnitures/bed room/large_25/*.JPG"): 
                 n= cv2.imread(img)
                 cv_img.append(n)
                 im=Image.open(img)
                 pix=im.load()
                 height,width = im.size
                 mytext = StringVar(value= str(width)+ "x" + str(height))
                 myentry2 = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry2.place(x = 1100 , y = 90 + sp2)
                 myscroll = Scrollbar(window, orient='horizontal', command=myentry.xview)
                 myentry.config(xscrollcommand=myscroll.set)
#              myscroll.place(x = 1050 , y = 70 + sp)
                 sp2 = sp2 + 30
         if(type_room == 1):   
             objects = os.listdir("C:/Users/arcee/Desktop/ui/furnitures/living room/l_25/")
             list=[x.split('.')[0] for x in objects]
             for entry in list:
                 print(entry)
                 mytext = StringVar(value=str(entry) )
                 myentry = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry.place(x = 1010 , y = 90 + sp)
                 sp = sp +30
             for img in glob.glob("C:/Users/arcee/Desktop/ui/furnitures/living room/l_25/*.JPG"): 
                 n= cv2.imread(img)
                 cv_img.append(n)
                 im=Image.open(img)
                 pix=im.load()
                 height,width = im.size
                 mytext = StringVar(value= str(width)+ "x" + str(height))
                 myentry2 = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry2.place(x = 1100 , y = 90 + sp2)
                 myscroll = Scrollbar(window, orient='horizontal', command=myentry.xview)
                 myentry.config(xscrollcommand=myscroll.set)
#              myscroll.place(x = 1050 , y = 70 + sp)
                 sp2 = sp2 + 30
     if(path == "C:/Users/arcee/Desktop/ui/Import/room25.JPG"):
         if(type_room == 0):   
             objects = os.listdir("C:/Users/arcee/Desktop/ui/furnitures/bed room/large_25/")
             list=[x.split('.')[0] for x in objects]
             for entry in list:
                 print(entry)
                 mytext = StringVar(value=str(entry) )
                 myentry = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry.place(x = 1010 , y = 90 + sp)
                 sp = sp +30
             for img in glob.glob("C:/Users/arcee/Desktop/ui/furnitures/bed room/large_25/*.JPG"): 
                 n= cv2.imread(img)
                 cv_img.append(n)
                 im=Image.open(img)
                 pix=im.load()
                 height,width = im.size
                 mytext = StringVar(value= str(width)+ "x" + str(height))
                 myentry2 = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry2.place(x = 1100 , y = 90 + sp2)
                 myscroll = Scrollbar(window, orient='horizontal', command=myentry.xview)
                 myentry.config(xscrollcommand=myscroll.set)
#              myscroll.place(x = 1050 , y = 70 + sp)
                 sp2 = sp2 + 30
         if(type_room == 1):   
             objects = os.listdir("C:/Users/arcee/Desktop/ui/furnitures/living room/l_25/")
             list=[x.split('.')[0] for x in objects]
             for entry in list:
                 print(entry)
                 mytext = StringVar(value=str(entry) )
                 myentry = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry.place(x = 1010 , y = 90 + sp)
                 sp = sp +30
             for img in glob.glob("C:/Users/arcee/Desktop/ui/furnitures/living room/l_25/*.JPG"): 
                 n= cv2.imread(img)
                 cv_img.append(n)
                 im=Image.open(img)
                 pix=im.load()
                 height,width = im.size
                 mytext = StringVar(value= str(width)+ "x" + str(height))
                 myentry2 = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry2.place(x = 1100 , y = 90 + sp2)
                 myscroll = Scrollbar(window, orient='horizontal', command=myentry.xview)
                 myentry.config(xscrollcommand=myscroll.set)
#              myscroll.place(x = 1050 , y = 70 + sp)
                 sp2 = sp2 + 30
     if(path == "C:/Users/arcee/Desktop/ui/Import/room26.JPG"):
         if(type_room == 0):   
             objects = os.listdir("C:/Users/arcee/Desktop/ui/furnitures/bed room/large_25/")
             list=[x.split('.')[0] for x in objects]
             for entry in list:
                 print(entry)
                 mytext = StringVar(value=str(entry) )
                 myentry = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry.place(x = 1010 , y = 90 + sp)
                 sp = sp +30
             for img in glob.glob("C:/Users/arcee/Desktop/ui/furnitures/bed room/large_25/*.JPG"): 
                 n= cv2.imread(img)
                 cv_img.append(n)
                 im=Image.open(img)
                 pix=im.load()
                 height,width = im.size
                 mytext = StringVar(value= str(width)+ "x" + str(height))
                 myentry2 = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry2.place(x = 1100 , y = 90 + sp2)
                 myscroll = Scrollbar(window, orient='horizontal', command=myentry.xview)
                 myentry.config(xscrollcommand=myscroll.set)
#              myscroll.place(x = 1050 , y = 70 + sp)
                 sp2 = sp2 + 30
         if(type_room == 1):   
             objects = os.listdir("C:/Users/arcee/Desktop/ui/furnitures/living room/l_25/")
             list=[x.split('.')[0] for x in objects]
             for entry in list:
                 print(entry)
                 mytext = StringVar(value=str(entry) )
                 myentry = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry.place(x = 1010 , y = 90 + sp)
                 sp = sp +30
             for img in glob.glob("C:/Users/arcee/Desktop/ui/furnitures/living room/l_25/*.JPG"): 
                 n= cv2.imread(img)
                 cv_img.append(n)
                 im=Image.open(img)
                 pix=im.load()
                 height,width = im.size
                 mytext = StringVar(value= str(width)+ "x" + str(height))
                 myentry2 = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry2.place(x = 1100 , y = 90 + sp2)
                 myscroll = Scrollbar(window, orient='horizontal', command=myentry.xview)
                 myentry.config(xscrollcommand=myscroll.set)
#              myscroll.place(x = 1050 , y = 70 + sp)
                 sp2 = sp2 + 30
     if(path == "C:/Users/arcee/Desktop/ui/Import/room27.JPG"):
         if(type_room == 0):   
             objects = os.listdir("C:/Users/arcee/Desktop/ui/furnitures/bed room/large_25/")
             list=[x.split('.')[0] for x in objects]
             for entry in list:
                 print(entry)
                 mytext = StringVar(value=str(entry) )
                 myentry = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry.place(x = 1010 , y = 90 + sp)
                 sp = sp +30
             for img in glob.glob("C:/Users/arcee/Desktop/ui/furnitures/bed room/large_25/*.JPG"): 
                 n= cv2.imread(img)
                 cv_img.append(n)
                 im=Image.open(img)
                 pix=im.load()
                 height,width = im.size
                 mytext = StringVar(value= str(width)+ "x" + str(height))
                 myentry2 = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry2.place(x = 1100 , y = 90 + sp2)
                 myscroll = Scrollbar(window, orient='horizontal', command=myentry.xview)
                 myentry.config(xscrollcommand=myscroll.set)
#              myscroll.place(x = 1050 , y = 70 + sp)
                 sp2 = sp2 + 30
         if(type_room == 1):   
             objects = os.listdir("C:/Users/arcee/Desktop/ui/furnitures/living room/l_25/")
             list=[x.split('.')[0] for x in objects]
             for entry in list:
                 print(entry)
                 mytext = StringVar(value=str(entry) )
                 myentry = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry.place(x = 1010 , y = 90 + sp)
                 sp = sp +30
             for img in glob.glob("C:/Users/arcee/Desktop/ui/furnitures/living room/l_25/*.JPG"): 
                 n= cv2.imread(img)
                 cv_img.append(n)
                 im=Image.open(img)
                 pix=im.load()
                 height,width = im.size
                 mytext = StringVar(value= str(width)+ "x" + str(height))
                 myentry2 = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry2.place(x = 1100 , y = 90 + sp2)
                 myscroll = Scrollbar(window, orient='horizontal', command=myentry.xview)
                 myentry.config(xscrollcommand=myscroll.set)
#              myscroll.place(x = 1050 , y = 70 + sp)
                 sp2 = sp2 + 30
     if(path == "C:/Users/arcee/Desktop/ui/Import/room28.JPG"):
         if(type_room == 0):   
             objects = os.listdir("C:/Users/arcee/Desktop/ui/furnitures/bed room/mid_12/")
             list=[x.split('.')[0] for x in objects]
             for entry in list:
                 print(entry)
                 mytext = StringVar(value=str(entry) )
                 myentry = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry.place(x = 1010 , y = 90 + sp)
                 sp = sp +30
             for img in glob.glob("C:/Users/arcee/Desktop/ui/furnitures/bed room/mid_12/*.JPG"): 
                 n= cv2.imread(img)
                 cv_img.append(n)
                 im=Image.open(img)
                 pix=im.load()
                 height,width = im.size
                 mytext = StringVar(value= str(width)+ "x" + str(height))
                 myentry2 = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry2.place(x = 1100 , y = 90 + sp2)
                 myscroll = Scrollbar(window, orient='horizontal', command=myentry.xview)
                 myentry.config(xscrollcommand=myscroll.set)
#              myscroll.place(x = 1050 , y = 70 + sp)
                 sp2 = sp2 + 30
         if(type_room == 1):   
             objects = os.listdir("C:/Users/arcee/Desktop/ui/furnitures/living room/m_12/")
             list=[x.split('.')[0] for x in objects]
             for entry in list:
                 print(entry)
                 mytext = StringVar(value=str(entry) )
                 myentry = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry.place(x = 1010 , y = 90 + sp)
                 sp = sp +30
             for img in glob.glob("C:/Users/arcee/Desktop/ui/furnitures/living room/m_12/*.JPG"): 
                 n= cv2.imread(img)
                 cv_img.append(n)
                 im=Image.open(img)
                 pix=im.load()
                 height,width = im.size
                 mytext = StringVar(value= str(width)+ "x" + str(height))
                 myentry2 = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry2.place(x = 1100 , y = 90 + sp2)
                 myscroll = Scrollbar(window, orient='horizontal', command=myentry.xview)
                 myentry.config(xscrollcommand=myscroll.set)
#              myscroll.place(x = 1050 , y = 70 + sp)
                 sp2 = sp2 + 30
     if(path == "C:/Users/arcee/Desktop/ui/Import/room29.JPG"):
         if(type_room == 0):   
             objects = os.listdir("C:/Users/arcee/Desktop/ui/furnitures/bed room/mid_12/")
             list=[x.split('.')[0] for x in objects]
             for entry in list:
                 print(entry)
                 mytext = StringVar(value=str(entry) )
                 myentry = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry.place(x = 1010 , y = 90 + sp)
                 sp = sp +30
             for img in glob.glob("C:/Users/arcee/Desktop/ui/furnitures/bed room/mid_12/*.JPG"): 
                 n= cv2.imread(img)
                 cv_img.append(n)
                 im=Image.open(img)
                 pix=im.load()
                 height,width = im.size
                 mytext = StringVar(value= str(width)+ "x" + str(height))
                 myentry2 = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry2.place(x = 1100 , y = 90 + sp2)
                 myscroll = Scrollbar(window, orient='horizontal', command=myentry.xview)
                 myentry.config(xscrollcommand=myscroll.set)
#              myscroll.place(x = 1050 , y = 70 + sp)
                 sp2 = sp2 + 30
         if(type_room == 1):   
             objects = os.listdir("C:/Users/arcee/Desktop/ui/furnitures/living room/m_12/")
             list=[x.split('.')[0] for x in objects]
             for entry in list:
                 print(entry)
                 mytext = StringVar(value=str(entry) )
                 myentry = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry.place(x = 1010 , y = 90 + sp)
                 sp = sp +30
             for img in glob.glob("C:/Users/arcee/Desktop/ui/furnitures/living room/m_12/*.JPG"): 
                 n= cv2.imread(img)
                 cv_img.append(n)
                 im=Image.open(img)
                 pix=im.load()
                 height,width = im.size
                 mytext = StringVar(value= str(width)+ "x" + str(height))
                 myentry2 = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry2.place(x = 1100 , y = 90 + sp2)
                 myscroll = Scrollbar(window, orient='horizontal', command=myentry.xview)
                 myentry.config(xscrollcommand=myscroll.set)
#              myscroll.place(x = 1050 , y = 70 + sp)
                 sp2 = sp2 + 30
     if(path == "C:/Users/arcee/Desktop/ui/Import/room30.JPG"):
         if(type_room == 0):   
             objects = os.listdir("C:/Users/arcee/Desktop/ui/furnitures/bed room/mid_12/")
             list=[x.split('.')[0] for x in objects]
             for entry in list:
                 print(entry)
                 mytext = StringVar(value=str(entry) )
                 myentry = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry.place(x = 1010 , y = 90 + sp)
                 sp = sp +30
             for img in glob.glob("C:/Users/arcee/Desktop/ui/furnitures/bed room/mid_12/*.JPG"): 
                 n= cv2.imread(img)
                 cv_img.append(n)
                 im=Image.open(img)
                 pix=im.load()
                 height,width = im.size
                 mytext = StringVar(value= str(width)+ "x" + str(height))
                 myentry2 = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry2.place(x = 1100 , y = 90 + sp2)
                 myscroll = Scrollbar(window, orient='horizontal', command=myentry.xview)
                 myentry.config(xscrollcommand=myscroll.set)
#              myscroll.place(x = 1050 , y = 70 + sp)
                 sp2 = sp2 + 30
         if(type_room == 1):   
             objects = os.listdir("C:/Users/arcee/Desktop/ui/furnitures/living room/m_12/")
             list=[x.split('.')[0] for x in objects]
             for entry in list:
                 print(entry)
                 mytext = StringVar(value=str(entry) )
                 myentry = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry.place(x = 1010 , y = 90 + sp)
                 sp = sp +30
             for img in glob.glob("C:/Users/arcee/Desktop/ui/furnitures/living room/m_12/*.JPG"): 
                 n= cv2.imread(img)
                 cv_img.append(n)
                 im=Image.open(img)
                 pix=im.load()
                 height,width = im.size
                 mytext = StringVar(value= str(width)+ "x" + str(height))
                 myentry2 = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry2.place(x = 1100 , y = 90 + sp2)
                 myscroll = Scrollbar(window, orient='horizontal', command=myentry.xview)
                 myentry.config(xscrollcommand=myscroll.set)
#              myscroll.place(x = 1050 , y = 70 + sp)
                 sp2 = sp2 + 30
     if(path == "C:/Users/arcee/Desktop/ui/Import/room31.JPG"):
         if(type_room == 0):   
             objects = os.listdir("C:/Users/arcee/Desktop/ui/furnitures/bed room/small_7/")
             list=[x.split('.')[0] for x in objects]
             for entry in list:
                 print(entry)
                 mytext = StringVar(value=str(entry) )
                 myentry = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry.place(x = 1010 , y = 90 + sp)
                 sp = sp +30
             for img in glob.glob("C:/Users/arcee/Desktop/ui/furnitures/bed room/small_7/*.JPG"): 
                 n= cv2.imread(img)
                 cv_img.append(n)
                 im=Image.open(img)
                 pix=im.load()
                 height,width = im.size
                 mytext = StringVar(value= str(width)+ "x" + str(height))
                 myentry2 = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry2.place(x = 1100 , y = 90 + sp2)
                 myscroll = Scrollbar(window, orient='horizontal', command=myentry.xview)
                 myentry.config(xscrollcommand=myscroll.set)
#              myscroll.place(x = 1050 , y = 70 + sp)
                 sp2 = sp2 + 30
         if(type_room == 1):   
             objects = os.listdir("C:/Users/arcee/Desktop/ui/furnitures/living room/s_7/")
             list=[x.split('.')[0] for x in objects]
             for entry in list:
                 print(entry)
                 mytext = StringVar(value=str(entry) )
                 myentry = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry.place(x = 1010 , y = 90 + sp)
                 sp = sp +30
             for img in glob.glob("C:/Users/arcee/Desktop/ui/furnitures/living room/s_7/*.JPG"): 
                 n= cv2.imread(img)
                 cv_img.append(n)
                 im=Image.open(img)
                 pix=im.load()
                 height,width = im.size
                 mytext = StringVar(value= str(width)+ "x" + str(height))
                 myentry2 = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry2.place(x = 1100 , y = 90 + sp2)
                 myscroll = Scrollbar(window, orient='horizontal', command=myentry.xview)
                 myentry.config(xscrollcommand=myscroll.set)
#              myscroll.place(x = 1050 , y = 70 + sp)
                 sp2 = sp2 + 30
     if(path == "C:/Users/arcee/Desktop/ui/Import/room32.JPG"):
         if(type_room == 0):   
             objects = os.listdir("C:/Users/arcee/Desktop/ui/furnitures/bed room/small_7/")
             list=[x.split('.')[0] for x in objects]
             for entry in list:
                 print(entry)
                 mytext = StringVar(value=str(entry) )
                 myentry = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry.place(x = 1010 , y = 90 + sp)
                 sp = sp +30
             for img in glob.glob("C:/Users/arcee/Desktop/ui/furnitures/bed room/small_7/*.JPG"): 
                 n= cv2.imread(img)
                 cv_img.append(n)
                 im=Image.open(img)
                 pix=im.load()
                 height,width = im.size
                 mytext = StringVar(value= str(width)+ "x" + str(height))
                 myentry2 = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry2.place(x = 1100 , y = 90 + sp2)
                 myscroll = Scrollbar(window, orient='horizontal', command=myentry.xview)
                 myentry.config(xscrollcommand=myscroll.set)
#              myscroll.place(x = 1050 , y = 70 + sp)
                 sp2 = sp2 + 30
         if(type_room == 1):   
             objects = os.listdir("C:/Users/arcee/Desktop/ui/furnitures/living room/s_7/")
             list=[x.split('.')[0] for x in objects]
             for entry in list:
                 print(entry)
                 mytext = StringVar(value=str(entry) )
                 myentry = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry.place(x = 1010 , y = 90 + sp)
                 sp = sp +30
             for img in glob.glob("C:/Users/arcee/Desktop/ui/furnitures/living room/s_7/*.JPG"): 
                 n= cv2.imread(img)
                 cv_img.append(n)
                 im=Image.open(img)
                 pix=im.load()
                 height,width = im.size
                 mytext = StringVar(value= str(width)+ "x" + str(height))
                 myentry2 = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry2.place(x = 1100 , y = 90 + sp2)
                 myscroll = Scrollbar(window, orient='horizontal', command=myentry.xview)
                 myentry.config(xscrollcommand=myscroll.set)
#              myscroll.place(x = 1050 , y = 70 + sp)
                 sp2 = sp2 + 30
     if(path == "C:/Users/arcee/Desktop/ui/Import/room33.JPG"):
         if(type_room == 0):   
             objects = os.listdir("C:/Users/arcee/Desktop/ui/furnitures/bed room/small_7/")
             list=[x.split('.')[0] for x in objects]
             for entry in list:
                 print(entry)
                 mytext = StringVar(value=str(entry) )
                 myentry = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry.place(x = 1010 , y = 90 + sp)
                 sp = sp +30
             for img in glob.glob("C:/Users/arcee/Desktop/ui/furnitures/bed room/small_7/*.JPG"): 
                 n= cv2.imread(img)
                 cv_img.append(n)
                 im=Image.open(img)
                 pix=im.load()
                 height,width = im.size
                 mytext = StringVar(value= str(width)+ "x" + str(height))
                 myentry2 = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry2.place(x = 1100 , y = 90 + sp2)
                 myscroll = Scrollbar(window, orient='horizontal', command=myentry.xview)
                 myentry.config(xscrollcommand=myscroll.set)
#              myscroll.place(x = 1050 , y = 70 + sp)
                 sp2 = sp2 + 30
         if(type_room == 1):   
             objects = os.listdir("C:/Users/arcee/Desktop/ui/furnitures/living room/s_7/")
             list=[x.split('.')[0] for x in objects]
             for entry in list:
                 print(entry)
                 mytext = StringVar(value=str(entry) )
                 myentry = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry.place(x = 1010 , y = 90 + sp)
                 sp = sp +30
             for img in glob.glob("C:/Users/arcee/Desktop/ui/furnitures/living room/s_7/*.JPG"): 
                 n= cv2.imread(img)
                 cv_img.append(n)
                 im=Image.open(img)
                 pix=im.load()
                 height,width = im.size
                 mytext = StringVar(value= str(width)+ "x" + str(height))
                 myentry2 = Entry(window, textvariable=mytext, state = 'readonly')
                 myentry2.place(x = 1100 , y = 90 + sp2)
                 myscroll = Scrollbar(window, orient='horizontal', command=myentry.xview)
                 myentry.config(xscrollcommand=myscroll.set)
#              myscroll.place(x = 1050 , y = 70 + sp)
                 sp2 = sp2 + 30
     
         
        
                 
def Save(event=None):
    image = ImageGrab.grab(bbox=(330,170,1285,840))
    image.save('output.jpg')
    out=r"C:\Users\arcee\Desktop\ui\output.jpg"
#    print(path)
    command = "python img_to_dxf.py -i %s -o output_dxf.dxf -l (0,0,0) -u(200,200,200)" %(out)
    process = subprocess.Popen(command,cwd=r"C:\Users\arcee\Desktop\ui\img_to_dxf_Python-master"
                              , stdout=subprocess.PIPE, shell=True)
    output = process.stdout.readline()                
    
    
title=Label(window,text="Welcome to insIDea",fg='blue',bg='yellow',relief="solid",font=("arial",16,"bold"))
title.pack(fill=BOTH,pady=2,padx=2)

importbtn=Button(window, text="Import Image",command=UploadAction,width=15,fg='blue',bg='yellow',relief=GROOVE,font=("arial",12,"bold"))
importbtn.place(x=10,y=60)

generate=Button(window, text="Scan",command=GenerateAction,width=15,fg='blue',bg='yellow',relief=GROOVE,font=("arial",12,"bold"))
generate.place(x=10,y=160)

edit=Button(window, text="Generate",command=Fuzzy,width=15,fg='blue',bg='yellow',relief=GROOVE,font=("arial",12,"bold"))
edit.place(x=10,y=260) 

btn=Button(window, text="Sizes",command=Size,width=15,fg='blue',bg='yellow',relief=GROOVE,font=("arial",12,"bold"))
btn.place(x=10,y=360)


exportbtn=Button(window, text="Save",command=Save,width=15,fg='blue',bg='yellow',relief=GROOVE,font=("arial",12,"bold"))
exportbtn.place(x=10,y=460)

workspace=Label(window, 
                height=11, width=32
                ,bd=1
                ,relief = "solid"
                ,font="Times 32")
workspace.place(x=200,y=50)
sizespace=Label(window, text="Sizes", anchor =N,
                height=23, width=23
                ,bd=1
                ,relief = "solid"
                ,font="Times 16")
sizespace.place(x=1000,y=50)
window.mainloop()