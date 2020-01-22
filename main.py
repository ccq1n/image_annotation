'''
显示图像
标注图像的一些文本信息到一个文本框
保存文本信息到csv文件
'''

import cv2
import os
import csv
import numpy as np
import tkinter as tk
global _point1, _point2
global _val, _ensure


def write(entry, win):
    global _val
    _val = entry.get()
    win.destroy()


def confirm(confirm, win):
    global _ensure
    _ensure = confirm
    win.destroy()


def createWinSure():
    win=tk.Tk()
    label=tk.Label(win,text="确认图像标注正确",bg="white",fg="black")
    label.pack()
    buttony=tk.Button(win,text="正确",command=lambda:confirm(True,win))
    buttony.pack()
    buttonn=tk.Button(win,text="错误",command=lambda:confirm(False,win))
    buttonn.pack()
    win.mainloop()


def createWinWri():
    win = tk.Tk()
    label = tk.Label(win, text="请输入:", bg="white", fg="black")
    label.pack()
    entry = tk.Entry(win, width=50, bg="white", fg="black")
    entry.pack()
    button = tk.Button(win, text="确认", command=lambda :write(entry, win))
    button.pack()
    win.mainloop()


def on_mouse(event, x, y, flags, param):
    global _point1, _point2
    global _val, _ensure
    img = param[0]
    index = param[1]
    img2 = img.copy()
    if event == cv2.EVENT_LBUTTONDOWN:  # 左键点击
        _point1 = (x, y)
        cv2.circle(img2, _point1, 10, (0, 255, 0), 5)
        cv2.imshow('image', img2)
    elif event == cv2.EVENT_MOUSEMOVE and (flags & cv2.EVENT_FLAG_LBUTTON):  # 按住左键拖曳
        cv2.rectangle(img2, _point1, (x, y), (255, 0, 0), 5)
        cv2.imshow('image', img2)
    elif event == cv2.EVENT_LBUTTONUP:  # 左键释放
        _point2 = (x, y)
        cv2.rectangle(img2, _point1, _point2, (0, 0, 255), 5)
        createWinSure()
        if _ensure:
            createWinWri()
            # cv2.imwrite('./generate_data/zyh_' + str(index) + '_' + str(point1[0]) + '_' + str(point1[1]) + '_' + str(
            #     point2[0]) + '_' + str(point2[1]) + '_' + pressure + '.jpg', img2)
            cv2.imshow('image', img2)
            cv2.destroyAllWindows()
        else:
            print('请在图片上重新框选!')


def main():
    for root, dirs, files in os.walk(r'D:\Camera'):
        for i in range(0, len(files)):
            img = cv2.imread(os.path.join(r'D:\Camera', files[i]))
            cv2.namedWindow('image')
            cv2.setMouseCallback('image', on_mouse, [img, i+1])
            cv2.imshow('image', img)
            cv2.waitKey(0)

if __name__ == '__main__':
    main()
