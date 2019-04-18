import cv2
from darkflow.net.build import TFNet
import numpy as np
import time
from dialog import dialog
from multiprocessing.pool import ThreadPool
import tkinter
import PIL.Image, PIL.ImageTk

window = tkinter.Tk()
window.title('Agent Q')

# def ObjectDetection(window):
options = {
'model': 'cfg/tiny-yolo-voc.cfg',  # yolo.cfg
'load': 'bin/tiny-yolo-voc.weights', # tiny-yolo-voc.weights # yolo.weights
'threshold': 0.4,
#'gpu': 1.0
}

tfnet = TFNet(options)
colors = [tuple(255 * np.random.rand(3)) for _ in range(10)]

capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

imageFrame = tkinter.Frame(window, width=600, height=500)
imageFrame.grid(row=0, column=0, padx=10, pady=2)

lmain = tkinter.Label(imageFrame)
lmain.grid(row=0, column=0)

def show_frame():
# while True:
    stime = time.time()
    ret, frame = capture.read()
    if ret:
        results = tfnet.return_predict(frame)
        for color, result in zip(colors, results):
            tl = (result['topleft']['x'], result['topleft']['y'])
            br = (result['bottomright']['x'], result['bottomright']['y'])
            label = result['label']
            discription = ""
            confidence = result['confidence']
            text = '{}: {:.0f}%, {}'.format(label, confidence * 100, discription)
            frame = cv2.rectangle(frame, tl, br, color, 5)
            frame = cv2.putText(
                frame, text, tl, cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)
        photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
        lmain.imgtk = imgtk
        lmain.configure(image=imgtk)
        lmain.after(5, show_frame)
        #cv2.imshow('frame', frame)
        print('FPS {:.1f}'.format(1 / (time.time() - stime)))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        return 0
        # break

capture.release()
cv2.destroyAllWindows()
show_frame()
window.mainloop()