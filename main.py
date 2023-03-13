import PIL
from PIL import Image, ImageTk
from tkinter import *
from tkinter import ttk
import tkinter as tk
import tkinter
import datetime
import pyodbc
import sys
import cv2
import numpy as np
import time
from threading import Thread

sys.stdin.reconfigure(encoding='utf-8') 
sys.stdout.reconfigure(encoding='utf-8')

class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.vid = cv2.VideoCapture(0)
        self.conx = pyodbc.connect(
            "driver={SQL Server}; server=192.168.1.254; database=QUANLYSANLUONG; uid=sa; pwd=123;")
        date = datetime.datetime.now()
        self.ngaygio = date.strftime("%m/%d/%Y %I:%M:%S %p")
        self.parent = parent

        self.border1 = tkinter.Frame(parent, relief=tkinter.SOLID,width=300, height=300)
        self.border1.pack(side="left",padx=5, pady=5)
        self.fr_trai = tkinter.Frame(self.border1,borderwidth=1)
        self.fr_trai.pack( pady=5,padx=20)

        self.fr_trai_tren = tkinter.Frame(self.fr_trai,borderwidth=1)
        self.fr_trai_tren.pack(side="top", pady=5,padx=20)
        self.label1 = tkinter.Label(self.fr_trai_tren, text="MÃ CODE:",font=("Helvetica", 25))
        self.label1.grid(row = 0, column = 0, padx=5, pady=5)
        self.inputtxt = tkinter.Entry(self.fr_trai_tren, bg='white',fg='black',font=("Helvetica", 25))
        self.inputtxt.grid(row = 0, column =1,padx=5,pady=5)
        self.inputtxt.bind("<Return>", self.enter)

        self.fr_trai_duoi = tkinter.Frame(self.fr_trai,borderwidth=1)
        self.fr_trai_duoi.pack(side="bottom", pady=5,padx=5)
        self.lb0 = tkinter.Label(self.fr_trai_duoi, text="• Date:", font=("Helvetica", 20))
        self.lb0.grid(row = 0, column = 0, sticky="w")
        self.label_date = tkinter.Label(self.fr_trai_duoi, text=str(self.ngaygio) ,font=("Helvetica", 20))
        self.label_date.grid(row = 0, column = 1)
        self.lb1 = tkinter.Label(self.fr_trai_duoi, text="• Mã code:", font=("Helvetica", 20))
        self.lb1.grid(row = 1, column = 0, sticky="w")
        self.label_macode = tkinter.Label(self.fr_trai_duoi, text="",font=("Helvetica", 20))
        self.label_macode.grid(row = 1, column = 1)
        self.lb2 = tkinter.Label(self.fr_trai_duoi, text="• Mã id:", font=("Helvetica", 20))
        self.lb2.grid(row = 2, column = 0, sticky="w")
        self.label_maid = tkinter.Label(self.fr_trai_duoi, text="",font=("Helvetica", 20))
        self.label_maid.grid(row = 2, column = 1)
        self.lb3 = tkinter.Label(self.fr_trai_duoi, text="• Họ tên:", font=("Helvetica", 20))
        self.lb3.grid(row = 3, column = 0, sticky="w")
        self.label_hoten = tkinter.Label(self.fr_trai_duoi, text="",font=("Helvetica", 20))
        self.label_hoten.grid(row = 3, column = 1)
        self.lb4 = tkinter.Label(self.fr_trai_duoi, text="• Chức vụ:", font=("Helvetica", 20))
        self.lb4.grid(row = 4, column = 0, sticky="w")
        self.label_chucvu = tkinter.Label(self.fr_trai_duoi, text="",font=("Helvetica", 20))
        self.label_chucvu.grid(row = 4, column = 1)
        self.lb5 = tkinter.Label(self.fr_trai_duoi, text="• Model:", font=("Helvetica", 20))
        self.lb5.grid(row = 5, column = 0, sticky="w")
        self.label_model = tkinter.Label(self.fr_trai_duoi, text="",font=("Helvetica", 20))
        self.label_model.grid(row = 5, column = 1)

   
        self.label_status = tkinter.Label(parent, text="          Ready          ", fg="white", bg="blue",font=("Helvetica", 60),width=600, height=600)

        self.label_status.pack(side="right" ,fill='both', padx=5, pady=5,anchor=CENTER)

        
    def enter(self, *args):
        self.timdulieuSQL()

    def daluong(self):
        thread = Thread(target=self.xuly)
        thread.start()

    def xuly(self):
        self.label_status.configure(text="                    ", foreground="white", background="orange",font=("Helvetica", 60))
        tries = 0
        self.xanh = 0
        while tries < 10:                       
            if (self.xanh == 1):
                self.label_status.configure(text="          OK          ", foreground="white", background="green",font=("Helvetica", 60))
                print("OK")
                self.luudulieu()
                self.clearInput()
                break
            #if (self.do == 1):
            #    self.label_status.configure(text="RESULT NG", foreground="white", background="red",font=("Helvetica", 50))
            #    print("NG")
            #    self.clearInput()
            #    break
            print(tries)
            self.chupanh() 
            tries += 1
            if tries == 9:
                self.label_status.configure(text="          NG          ", foreground="white", background="red",font=("Helvetica", 60))
                
                self.clearInput()
                break

    def timdulieuSQL(self):
        macode = self.inputtxt.get()
        datenow = datetime.datetime.now()
        ngay = str(f'{datenow:%Y/%m/%d}')
        print(ngay)
        ngaygiohientai = datenow.strftime("%m/%d/%Y %I:%M:%S %p")

        cursor = self.conx.cursor()
        cursor.execute("SELECT * from dbo.dotinhdien where macode=? and ngay=?",(macode,ngay))

        row = cursor.fetchone()
        try:
            self.label_date.configure(text=str(ngaygiohientai))
            self.label_macode.configure(text=str(row.macode))
            self.label_maid.configure(text=str(row.id))
            self.label_hoten.configure(text=str(row.hovaten))
            self.label_chucvu.configure(text=str(row.chucvu))
            self.label_model.configure(text=str(row.model))
            print("mã code: "+ row.macode)
            print("họ và tên: " + row.hovaten)
            print("chức vụ: " + row.chucvu)
            print("mã id: "+ str(row.id))
            print("model: "+ row.model)
            print("cell: "+ row.cell)
            print("công đoạn: " +row.station)

            self.maid = str(row.id)
            self.hoten = str(row.hovaten)
            self.model = str(row.model)


            self.daluong()
        except:
            print("sai ma code")
            self.label_status.configure(text="KHÔNG CÓ DỮ LIỆU TỪ ASSY", foreground="black", background="red", font=("Helvetica", 40))
            self.clearInput()

        
    def chupanh(self):
        ret, frame = self.vid.read()
        if ret:
                self.tenAnh = "Anhcheck-" + time.strftime("%d-%m-%Y-%H-%M-%S")
                cv2.imwrite(self.tenAnh + ".jpg", frame)
                time.sleep(0.2)
                #self.showanhvuachup()
                self.kiemtra()
        
    def showanhvuachup(self):
        pic = cv2.imread(self.tenAnh + ".jpg", 1)
        cvt_pic = cv2.cvtColor(pic, cv2.COLOR_BGR2RGB)
        pil_pic = PIL.Image.fromarray(cvt_pic)
        imgtk_pic = ImageTk.PhotoImage(image=pil_pic)
        self.anh.imgtk = imgtk_pic
        self.anh.configure(image=imgtk_pic)
        
    
    def kiemtra(self):
        img_path = self.tenAnh + ".jpg"
        img = cv2.imread(img_path)
        hsvFrame = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        green_lower = np.array([40, 40, 245], np.uint8)
        green_upper = np.array([90, 255, 255], np.uint8)
        green_mask = cv2.inRange(hsvFrame, green_lower, green_upper)

        kernal = np.ones((5, 5), "uint8")

         # For green color
        green_mask = cv2.dilate(green_mask, kernal)
        res_green = cv2.bitwise_and(img, img,mask = green_mask)
        contours, hierarchy = cv2.findContours(green_mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)     
        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if(int(area) > 300):
                print("pass")
                self.xanh = 1

    def luudulieu(self):
        try:
            dotinhdien = "1"
            cursor = self.conx.cursor()
            datenow = datetime.datetime.now()
            ngay = str(f'{datenow:%Y/%m/%d}')
            macode = self.inputtxt.get()
            #maid = self.maid
            #hoten = self.hoten
            model = self.model
            cursor.execute("Update dotinhdien set dotinhdien = ? where macode = ? and model = ? and ngay = ?", (dotinhdien, macode, model,ngay))
            self.conx.commit()
        except:
            print("Failed to update dotinhdien")


    def clearInput(self):
        time.sleep(2)
        self.label_date.configure(text="")
        self.label_macode.configure(text="")
        self.label_maid.configure(text="")
        self.label_hoten.configure(text="")
        self.label_chucvu.configure(text="")
        self.label_model.configure(text="")
        self.label_status.configure(text="          READY          ", foreground="white", background="blue",font=("Helvetica", 60))
        self.inputtxt.delete(0, END)
        self.inputtxt.focus()


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1000x600")
    root.title("Đo thông điện application - S")
    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.mainloop()

