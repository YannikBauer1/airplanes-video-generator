import cv2
import os


def video(folder,video_name):
    img = cv2.imread(folder+"/"+os.listdir(folder)[0])
    h,w,l = img.shape
    size=(w,h)
    out = cv2.VideoWriter(video_name+".avi", cv2.VideoWriter_fourcc(*'DIVX'), 150,size)
    for filename in os.listdir(folder):
        img=cv2.imread(folder+"/"+filename)
        out.write(img)
    out.release()

#video("imagens3","Mundo(1.1-2.1)")