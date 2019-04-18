from tkinter import *
from tkinter import ttk
import webbrowser
import speech_recognition as sr
import datetime

class dialog:
    def callback(self,btn2):
        if btn2.get() == 'google' and entry1.get() != '':
            webbrowser.open('http://google.com/search?q='+entry1.get())
            
        elif btn2.get() == 'duck' and entry1.get() != '':
            webbrowser.open('http://duckduckgo.com/?q='+entry1.get())

        elif btn2.get() == 'youtube' and entry1.get() != '':
            webbrowser.open('https://www.youtube.com/results?search_query='+entry1.get())

        else:
            pass

    def get(self,event):

        if btn2.get() == 'google' and entry1.get() != '':
            webbrowser.open('http://google.com/search?q='+entry1.get())
            
        elif btn2.get() == 'duck' and entry1.get() != '':
            webbrowser.open('http://duckduckgo.com/?q='+entry1.get())

        elif btn2.get() == 'youtube' and entry1.get() != '':
            webbrowser.open('https://www.youtube.com/results?search_query='+entry1.get())

        else:
            pass

    def buttonClick(self):
        r = sr.Recognizer()
        with sr.Microphone(device_index = 1) as source:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
            try:
                message = str(r.recognize_google(audio))
                entry1.focus()
                entry1.delete(0, END)
                entry1.insert(0, message)

                if btn2.get() == 'google':
                    webbrowser.open('http://google.com/search?q='+message)
            
                elif btn2.get() == 'duck':
                    webbrowser.open('http://duckduckgo.com/?q='+message)
                    
                elif btn2.get() == 'youtube':
                    webbrowser.open('https://www.youtube.com/results?search_query='+message)

                else:
                    pass

            except sr.UnknownValueError:
                print('Google Speech Recognition could not understand audio')

            except sr.RequestError as e:
                print('Could not request results from Google Speech Recognition Service')

            else:
                pass    

    def __init__(self):
        root = Tk()
        root.title('Agent Q')
        style = ttk.Style()
        style.theme_use('classic')
        label1 = ttk.Label(root, text='Query:')
        label1.grid(row=0, column=0)
        entry1 = ttk.Entry(root, width=40)
        entry1.grid(row=0, column=1, columnspan=4)
        btn2 = StringVar()
        entry1.bind('<Return>', self.get)

        MyButton1 = ttk.Button(root, text='Search', width=10, command=self.callback(btn2))
        MyButton1.grid(row=0, column=6)

        MyButton2 = ttk.Radiobutton(root, text='Google', value='google', variable=btn2)
        MyButton2.grid(row=1, column=1, sticky=W)

        MyButton3 = ttk.Radiobutton(root, text='Duck', value='duck', variable=btn2)
        MyButton3.grid(row=1, column=2, sticky=W)

        MyButton5 = ttk.Radiobutton(root, text='YouTube', value='youtube', variable=btn2)
        MyButton5.grid(row=1, column=3, sticky=E)

        MyButton6 = Button(root, command=self.buttonClick, bd=0, activebackground='#c1bfbf', overrelief='groove', relief='sunken')
        MyButton6.grid(row=0, column=5)

        entry1.focus()
        root.wm_attributes('-topmost', 1)
        btn2.set('google')
        root.mainloop()