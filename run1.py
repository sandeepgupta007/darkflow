import numpy as np
import cv2
import tkinter as tk
from PIL import Image, ImageTk
from darkflow.net.build import TFNet
import time
from queue import Queue#  as Queue
import upload_imgur
import threading
#import urllib.request as urllib2
import urllib.request# import urlopen
from http.cookiejar import CookieJar
import re
from datetime import datetime
from bs4 import BeautifulSoup as bs
import tkinter.scrolledtext as ScrolledText
from tkinter.ttk import Progressbar
import requests
import speech_recognition as sr

#Set up GUI
window = tk.Tk()  #Makes main window
window.wm_title("Agent Q")
window.config(background="#FFFFFF")

#Graphics window
imageFrame = tk.Frame(window, width=600, height=500)
imageFrame.grid(row=0, column=0, padx=10, pady=2)

#Capture video frames
lmain = tk.Label(imageFrame)
lmain.grid(row=0, column=0)

style = tk.ttk.Style()
style.theme_use('default')
style.configure("black.Horizontal.TProgressbar", background='black')
bar = Progressbar(window, length=625, style='black.Horizontal.TProgressbar')

options = {
'model': 'cfg/tiny-yolo-voc.cfg',  # yolo.cfg
'load': 'bin/tiny-yolo-voc.weights', # tiny-yolo-voc.weights # yolo.weights
'threshold': 0.4,
'gpu': 1.0
}

tfnet = TFNet(options)
colors = [tuple(255 * np.random.rand(3)) for _ in range(10)]

cap = cv2.VideoCapture(0) # 
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

list_of_queries = Queue()
cj = CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36')]
headers = {'User-Agent': 'Mozilla/5.0'}

def search(query,crop_image):
	print ('inside search')
	try:
		bar['value'] = 25
		# cv2.imshow("frame",crop_image)
		cv2image1 = cv2.cvtColor(crop_image, cv2.COLOR_BGR2RGBA)
		img1 = Image.fromarray(cv2image1)
		name_of_image = re.sub("\D","",str(datetime.now()))
		img1.save(name_of_image+'.png')
		# imgtk1 = ImageTk.PhotoImage(image=img1)
		upload_link = upload_imgur.upload_image("/home/sandeep/Desktop/projects/patternProject/darkflow/"+ name_of_image +".png")
		print (upload_link)
		bar['value'] = 50
		google_path = "http://images.google.com/searchbyimage?image_url=" + upload_link
		source_code =  opener.open(google_path,timeout=10).read() # requests.get(google_path,headers=headers)
		bar['value'] = 75
		source_code = source_code.decode("utf8")
		soup = bs(source_code,'lxml')
		tags = soup.findAll("div",{"class" : "rc"})
		related_search_tag = soup.find('a',{"class" : "fKDtNb"})
		related_search = ""
		search_print = ""
		if related_search_tag:
			related_search = related_search_tag.contents[0]
			search_print = "Looks like : " + related_search
			print ("Related Search : {}".format(related_search))
		search_results = []
		for tag in tags:
			search_results.append([tag.find("h3").text, tag.find("div",{"class" : "s"}).text, tag.find('a').get('href')])
		# rank = []
		i = 0
		for search_result in search_results:
			cnt = 0
			#qr = query.split()
			for word in query:
				cnt += search_result[1].count(word)
			search_results[i].insert(0,cnt)	
			i+=1
		search_results.sort(reverse=True)
		
		for search_result in search_results:
			search_print += "Title : " + search_result[1] + "\n Description " + search_result[2] + "\n Link " + search_result[3] + "\n \n"
		label2['state'] = 'normal'
		label2.insert(tk.END,search_print)
		label2.yview(tk.END)
		bar['value'] = 100
		print (search_results)
	except Exception as e:
		bar['value'] = 0
		print (e)
	finally :
		bar['value'] = 0
#capture = cv2.VideoCapture(0)

def show_frame():
    '''if not cap.isOpened():
    	return ""'''
    _, frame = cap.read()
    if _:
    	results = tfnet.return_predict(frame)
    	query = ""
    	if list_of_queries.qsize() > 0:
    		query = list_of_queries.get()
    		query = query.split()
    		[x.lower() for x in query]
    	for color, result in zip(colors, results):
            tl = (result['topleft']['x'], result['topleft']['y'])
            br = (result['bottomright']['x'], result['bottomright']['y'])
            label = result['label']
            if label.lower() in query:
            	# search(query,frame[tl[1]:br[1],tl[0]:br[0]])
            	roi = frame[tl[1]:br[1],tl[0]:br[0]].copy()
            	t1 = threading.Thread(target=search,args=(query,roi,))
            	t1.start()
            discription = ""
            confidence = result['confidence']
            text = '{}: {:.0f}%, {}'.format(label, confidence * 100, discription)
            frame = cv2.rectangle(frame, tl, br, color, 5)
            frame = cv2.putText(
                frame, text, tl, cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(10, show_frame)

def add_task(t):
	list_of_queries.put(entry1.get())
	print ('Search about this Query {}'.format(entry1.get()))

label1 = tk.Label(window, text='Search')
label1.grid(row=1, column=1)

entry1 = tk.Entry(window,width=78)
entry1.grid(row=1, column=0)

entry1.bind('<Return>',add_task)
entry1.focus()

label2 = ScrolledText.ScrolledText(window,state="disabled",font=('Arial',12))
label2.grid(row=0,column=2,rowspan=2)

bar.grid(row=2,column=0)
show_frame()  #Display 2
window.mainloop()  #Starts GUI