import tkinter as tk
import time
from datetime import datetime, timedelta
import matplotlib
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import serial
from threading import Thread
import os
import alicat
from alicat import FlowController
from PIL import ImageTk, Image

class CPG_GUI():
    def __init__(self):
        self.is_off_1 = True
        self.is_off_2 = True
        self.ser = serial.Serial('COM6', 9600)
        self.ser.timeout = 1
        self.flow_controller_air = FlowController(port='COM4', address = 'A')
        # self.flow_controller_propane = FlowController(port='COM4', address = 'B')
        self.flow_controller_decane = FlowController(port='COM4', address = 'C')
        # self.flow_controller_nitrogen = FlowController(port='COM4', address = 'D')
    
    def sWrite(self, x,button,is_off):
        if is_off == True:
            button.config(bg="#d12c2c")
            is_off = False
            print('nay')
        else:
            print('ye')
            button.config(bg="#2cd137")
            is_off = True
        print(x)
        self.ser.write(x)

    def buildGUI(self):

        self.root = tk.Tk()

        canvas = tk.Canvas(self.root, height=700,width=800, bg='#5c5d5e', borderwidth = 0, highlightthickness = 0)
        canvas.pack()

        self.frame_left = tk.Frame(self.root, bg='#545454', borderwidth = 0)
        self.frame_left.place(relwidth=0.25,relheight=0.7)

        self.frame_middle = tk.Frame(self.root, bg='#545454', borderwidth = 0)
        self.frame_middle.place(relx=0.25, relwidth=0.5,relheight=0.7)

        self.frame_bottom = tk.Frame(self.root, bg='#545454', borderwidth = 0)
        self.frame_bottom.place(rely=0.7, relwidth=1, relheight=0.3)

        self.frame_right = tk.Frame(self.root, bg='#545454', borderwidth = 0)
        self.frame_right.place(relx=0.75, relwidth=0.25,relheight=0.7)

        photoimage = ImageTk.PhotoImage(file="sdsur.png")
        canvas.create_image(1, 1, image=photoimage)

        self.label_1 = tk.Label(self.frame_left, font='Helvetica 10 bold', text="Methane flow rate (LPM)", bg='#545454')
        self.label_1.place(relx = 0.1, rely = 0.25)

        self.entry_1= tk.Entry(self.frame_left, bg="#e0e6ef", font='Helvetica 13')
        self.entry_1.place(relx = 0.5, rely=0.3, relwidth=0.5,relheight=0.05, anchor = 'n')

        self.label_2 = tk.Label(self.frame_left, font='Helvetica 10 bold', text="Eqivalence ratio", bg='#545454')
        self.label_2.place(relx = 0.22, rely = 0.4)

        self.entry_2= tk.Entry(self.frame_left, bg="#e0e6ef", font='Helvetica 13')
        self.entry_2.place(relx = 0.5, rely=0.45, relwidth=0.5,relheight=0.05, anchor = 'n')

        self.label_3 = tk.Label(self.frame_left, font='Helvetica 10 bold', text="Air flow rate (LPM)", bg='#545454')
        self.label_3.place(relx = 0.17, rely = 0.55)

        self.label_4 = tk.Label(self.frame_left, font='Helvetica 10 bold', bg = 'light gray')
        self.label_4.place(relx = 0.25, rely = 0.6, relwidth = 0.5)

        self.label_5 = tk.Label(self.frame_left, font='Helvetica 10 bold', text="Nitrogen to bubbler (LPM)", bg='#545454')
        self.label_5.place(relx = 0.07, rely = 0.7)

        self.label_6 = tk.Label(self.frame_middle, font='Helvetica 10 bold', bg='#545454', text = "3:00:00")
        self.label_6.place(relx = 0.78, rely = 0.87)

        self.label_7 = tk.Label(self.frame_middle, font='Helvetica 10 bold', bg='#545454')
        self.label_7.place(relx = 0.896, rely = 0.87, relwidth=0.3,relheight=0.2)

        self.label_8 = tk.Label(self.frame_middle, font='Helvetica 10 bold', bg='#545454', text = "Time Remaining")
        self.label_8.place(relx = 0.7, rely = 0.83)

        self.entry_5= tk.Entry(self.frame_left, bg="#e0e6ef", font='Helvetica 13')
        self.entry_5.place(relx = 0.5, rely=0.75, relwidth=0.5,relheight=0.05, anchor = 'n')

        self.button_1 = tk.Button(self.frame_bottom, text="Start Pump", bg='#2cd137', font='Helvetica 10 bold', command = lambda: self.sWrite(b'p',self.button_1,self.is_off_1))
        self.button_1.place(relx=0.1,rely= 0.2, relheight=0.2,relwidth=0.2)

        self.button_2 = tk.Button(self.frame_bottom, text="Start Fans", bg='#2cd137', font='Helvetica 10 bold',command = lambda: self.sWrite(b'f',self.button_2,self.is_off_2))
        self.button_2.place(relx=0.4,rely= 0.2, relheight=0.2,relwidth=0.2)

        self.button_4 = tk.Button(self.frame_bottom, text="Start Inerts", bg='#2cd137', font='Helvetica 10 bold', command = lambda: self.startflows(self.entry_1.get(), self.Vol_air))
        self.button_4.place(relx=0.7,rely= 0.2, relheight=0.2,relwidth=0.2)

        self.button_5 = tk.Button(self.frame_bottom, text="Stop gas flows", bg='#2cd137', font='Helvetica 10 bold', command = lambda: self.stopflows(self.entry_1.get()))
        self.button_5.place(relx=0.7,rely= 0.5, relheight=0.2,relwidth=0.2)

        self.button_5 = tk.Button(self.frame_bottom, text="Start Combustibles", bg='#2cd137', font='Helvetica 10 bold', command = lambda: self.startcombustibles(self.entry_1.get()))
        self.button_5.place(relx=0.4,rely= 0.5, relheight=0.2,relwidth=0.2)

        self.x = [1,2,3,4,5,6,7,8,9,10]
        self.xstr =  ['null', 'null', 'null', 'null', 'null', 'null', 'null', 'null', 'null', 'null']
        self.y = np.zeros((10,), dtype=int).tolist()

        self.fig = plt.figure(figsize = (4,4), dpi = 100, edgecolor= '#545454', facecolor = '#545454')
        self.ax = self.fig.add_subplot(111)
        self.ax.set_ylim([0,10])
        self.temp_plot, = self.ax.plot(self.x,self.y, 'r-')
        self.chart = FigureCanvasTkAgg(self.fig, self.frame_middle)
        self.chart.get_tk_widget().place(relx = 0, rely = 0)
        self.ax.set_xticks(self.x)
        self.ax.set_ylabel('Temperature (C)')
        self.ax.set_xlabel('Time (S)')
        self.ax.set_title('Live Thermocouple data')
        self.ax.grid()
        self.timepast = datetime.now()

        self.thread3 = Thread(target = gui.plot_update)
        self.thread3.start()

        self.update()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.root.mainloop()
    
    def startflows(self, methane, air):
        self.timestartflows = datetime.now()
        self.threehourset = self.timestartflows + timedelta(hours = 3)
        self.flow_controller_air.set_flow_rate(19200)
        time.sleep(1)
        # self.flow_controller_propane.set_flow_rate(3213)
    
    def startcombustibles(self, methane):
        # self.flow_controller_nitrogen.set_flow_rate(8960)
        self.flow_controller_decane.set_flow_rate(5120)

    def stopflows(self, methane):
        # self.flow_controller_nitrogen.set_flow_rate(0)
        self.flow_controller_air.set_flow_rate(0)
        # self.flow_controller_propane.set_flow_rate(0)
        self.flow_controller_decane.set_flow_rate(0)
        time.sleep(1)

    def update(self):
        self.timenow2 = datetime.now()
        try:
            self.threehourtimer = (self.threehourset - self.timenow2)
            self.label_6.config(text = str(self.threehourtimer))
        except:
            pass
        try:
            self.Vol_air = float(self.entry_1.get())*float(self.entry_2.get())*9.52
            display_Vol_air = round(self.Vol_air,4)
            if float(self.entry_2.get()) > 1:
                self.label_4.config(text = display_Vol_air, fg = '#8f0909')
            else:
                self.label_4.config(text = display_Vol_air, fg = '#0e8f07')
        except:
            self.label_4.config(text = 'nan', fg = '#000000')
        self.root.after(1000,self.update)

    def plot_update(self):
        while True:
            self.temp_plot.set_ydata(self.y)
            self.temp_plot.set_xdata(self.x)
            self.ax.set_xticklabels(self.xstr, Fontsize = 8)
            for i in self.y:
                if int(i) > 10:
                    self.ax.set_ylim([0,int(i)+10])
            self.fig.canvas.draw()
            self.fig.canvas.flush_events()
            time.sleep(1)

    def arduino(self):
        self.ser.write(b'r')
        while True:
            time.sleep(1)
            if (self.ser.inWaiting()>0):
                data = self.ser.readline()
                data = data[0:-2]
                data = float(data)
                self.y.append(data)
                self.timenow = datetime.now()
                self.floattimedelta = self.timenow - self.timepast
                self.deltatime = str(int(self.floattimedelta.total_seconds()))
                self.xstr.append(self.deltatime)
                self.xstr.pop(0)
                self.y.pop(0)
            # try:
            #     self.temperature = float(self.ser.readline().decode('ascii'))
            #     self.y.append(self.temperature)
            #     print(self.y)
            # except:
            #     pass
        self.ser.close()
    
    def on_closing(self):
        self.ser.write(b'r')
        os._exit(1)

gui = CPG_GUI()

thread = Thread(target = gui.buildGUI)
thread.start()
thread2 = Thread(target = gui.arduino)
thread2.start()