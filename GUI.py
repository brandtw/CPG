import tkinter as tk
import time
from datetime import datetime, timedelta
import matplotlib
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import serial
import serial.tools.list_ports
from threading import Thread
import os
import alicat
from alicat import FlowController
from PIL import ImageTk, Image
import winsound

class CPG_GUI():
    def __init__(self):
        ports = serial.tools.list_ports.comports()
        for port, desc, hwid in sorted(ports):
            if "Arduino" in desc:
                self.port_arduino = port
            if "Prolific" in desc:
                self.port_alicat = port
        self.ser = serial.Serial(self.port_arduino, 9600)
        self.ser.timeout = 1
        self.flow_controller_air = FlowController(port=self.port_alicat, address = 'A')
        self.flow_controller_methane = FlowController(port=self.port_alicat, address = 'B')
        self.flow_controller_decane = FlowController(port=self.port_alicat, address = 'C')
        self.flow_controller_nitrogen = FlowController(port=self.port_alicat, address = 'D')
        self.pump_on = False
        self.fan_on = False
        self.alarm = True
        self.disabled = False
        self.hydrocarbon = 'Methane'
        self.ratio = 0
    
    def pWrite(self, x):
        if self.pump_on:
            self.pump_on = False
            self.button_1.config(bg='#f7ed2d', text = 'Start Pump')
        else:
            self.pump_on = True
            self.button_1.config(bg='#2cd137', text = 'Stop Pump')
        self.ser.write(x)

    def fWrite(self, x):
        if self.fan_on:
            self.fan_on = False
            self.button_2.config(bg='#f7ed2d', text = 'Start Fans')
        else:
            self.fan_on = True
            self.button_2.config(bg='#2cd137', text = 'Stop Fans')
        self.ser.write(x)

    def buildGUI(self):

        self.root = tk.Tk()

        canvas = tk.Canvas(self.root, height=700,width=800, bg='#5c5d5e', borderwidth = 0, highlightthickness = 0)
        canvas.pack()

        self.frame_left = tk.Frame(self.root, bg='#918f8e', borderwidth = 0)
        self.frame_left.place(relwidth=0.25,relheight=0.7)

        self.frame_middle = tk.Frame(self.root, bg='#918f8e', borderwidth = 0)
        self.frame_middle.place(relx=0.25, relwidth=0.5,relheight=0.7)

        self.frame_bottom = tk.Frame(self.root, bg='#918f8e', borderwidth = 0)
        self.frame_bottom.place(rely=0.7, relwidth=1, relheight=0.3)

        self.frame_right = tk.Frame(self.root, bg='#918f8e', borderwidth = 0)
        self.frame_right.place(relx=0.75, relwidth=0.25,relheight=0.7)

        self.label_1 = tk.Label(self.frame_left, font='Helvetica 10 bold', text="Methane flow rate (LPM)", bg='#918f8e')
        self.label_1.place(relx = 0.1, rely = 0.25)

        self.entry_methane= tk.Entry(self.frame_left, bg="#e0e6ef", font='Helvetica 13')
        self.entry_methane.place(relx = 0.5, rely=0.3, relwidth=0.5,relheight=0.05, anchor = 'n')

        self.label_2 = tk.Label(self.frame_left, font='Helvetica 10 bold', text="Eqivalence ratio", bg='#918f8e')
        self.label_2.place(relx = 0.22, rely = 0.4)

        self.entry_EQ= tk.Entry(self.frame_left, bg="#e0e6ef", font='Helvetica 13')
        self.entry_EQ.place(relx = 0.5, rely=0.45, relwidth=0.5,relheight=0.05, anchor = 'n')

        self.label_3 = tk.Label(self.frame_left, font='Helvetica 10 bold', text="Air flow rate (LPM)", bg='#918f8e')
        self.label_3.place(relx = 0.17, rely = 0.55)

        self.label_air = tk.Label(self.frame_left, font='Helvetica 10 bold', bg = 'light gray')
        self.label_air.place(relx = 0.25, rely = 0.6, relwidth = 0.5)

        self.label_5 = tk.Label(self.frame_left, font='Helvetica 10 bold', text="Nitrogen to bubbler (LPM)", bg='#918f8e')
        self.label_5.place(relx = 0.07, rely = 0.7)

        self.label_9 = tk.Label(self.frame_left, font='Helvetica 10 bold', text="N2 Shroud flow rate (LPM)", bg='#918f8e')
        self.label_9.place(relx = 0.1, rely = 0.1)

        self.button_stop = tk.Button(self.frame_right, text="Stop All Flows", bg='#ed392f', font='Helvetica 10 bold',command = lambda: self.stopflows())
        self.button_stop.place(relx=0.1,rely= 0.1, relheight=0.1,relwidth=0.7)

        self.button_vent = tk.Button(self.frame_right, text="Vent Chamber", bg='#ed392f', font='Helvetica 10 bold',command = lambda: self.startnitrogenshroud(40))
        self.button_vent.place(relx=0.1,rely= 0.25, relheight=0.1,relwidth=0.7)

        self.entry_N2 = tk.Entry(self.frame_left, bg="#e0e6ef", font='Helvetica 13')
        self.entry_N2.place(relx = 0.5, rely=0.15, relwidth=0.5,relheight=0.05, anchor = 'n')

        self.entry_decane = tk.Entry(self.frame_left, bg="#e0e6ef", font='Helvetica 13')
        self.entry_decane.place(relx = 0.5, rely=0.75, relwidth=0.5,relheight=0.05, anchor = 'n')

        self.button_1 = tk.Button(self.frame_bottom, text="Start Pump", bg='#f7ed2d', font='Helvetica 10 bold', command = lambda: self.pWrite(b'p'))
        self.button_1.place(relx=0.7,rely= 0.5, relheight=0.2,relwidth=0.2)

        self.button_2 = tk.Button(self.frame_bottom, text="Start Fans", bg='#f7ed2d', font='Helvetica 10 bold',command = lambda: self.fWrite(b'f'))
        self.button_2.place(relx=0.4,rely= 0.5, relheight=0.2,relwidth=0.2)

        self.button_4 = tk.Button(self.frame_bottom, text="Start Nitrogen Shroud", bg='#f7ed2d', font='Helvetica 10 bold', command = lambda: [self.startnitrogenshroud(self.entry_N2.get()),
                                                                                                                                self.button_4.config(bg='#2cd137')])
        self.button_4.place(relx=0.7,rely= 0.2, relheight=0.2,relwidth=0.2)

        self.button_5 = tk.Button(self.frame_bottom, text="Start Air", bg='#f7ed2d', font='Helvetica 10 bold', command = lambda: [self.startair(self.Vol_air),
                                                                                                                                self.button_5.config(bg='#2cd137', text = 'Update Air')])
        self.button_5.place(relx=0.1,rely= 0.2, relheight=0.2,relwidth=0.2)

        self.button_6 = tk.Button(self.frame_bottom, text="Start Methane", bg='#f7ed2d', font='Helvetica 10 bold', command = lambda: [self.startmethane(self.entry_methane.get()),
                                                                                                self.button_6.config(bg='#2cd137', text = 'Update {}'.format(self.hydrocarbon))])
        self.button_6.place(relx=0.4,rely= 0.2, relheight=0.2,relwidth=0.2)

        self.button_3 = tk.Button(self.frame_bottom, text="Start Decane", bg='#f7ed2d', font='Helvetica 10 bold',command = lambda: [self.startdecane(self.entry_decane.get()),
                                                                                                                                self.button_3.config(bg='#2cd137', text = 'Update Decane')])
        self.button_3.place(relx=0.1,rely= 0.5, relheight=0.2,relwidth=0.2)

        self.label_10 = tk.Label(self.frame_right, font='Helvetica 10 bold', text="Select Gas", bg='#918f8e')
        self.label_10.place(relx = 0.25, rely = 0.55)

        self.button_7 = tk.Button(self.frame_right, text="Methane", bg='#f7ed2d', font='Helvetica 10 bold',command = lambda: self.gasselect(0))
        self.button_7.place(relx=0.1,rely= 0.6, relheight=0.1,relwidth=0.7)

        self.button_8 = tk.Button(self.frame_right, text="Propane", bg='#f7ed2d', font='Helvetica 10 bold',command = lambda: self.gasselect(1))
        self.button_8.place(relx=0.1,rely= 0.75, relheight=0.1,relwidth=0.7)

        self.button_alarm = tk.Button(self.frame_right, text="Disable Alarm", bg='#2cd137', font='Helvetica 10 bold',command = lambda: self.setalarm())
        self.button_alarm.place(relx=0.1,rely= 0.4, relheight=0.1,relwidth=0.7)

        self.x = [1,2,3,4,5,6,7,8,9,10]
        self.xstr =  ['null', 'null', 'null', 'null', 'null', 'null', 'null', 'null', 'null', 'null']
        self.y = np.zeros((10,), dtype=int).tolist()

        self.fig = plt.figure(figsize = (4,4), dpi = 100, edgecolor= '#918f8e', facecolor = '#918f8e')
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
        self.retries = 2

        self.root.mainloop()
    
    def gasselect(self, gas):
        if gas == 0:
            self.flow_controller_methane.set_gas("CH4")
            self.button_7.config(bg='#2cd137')
            self.button_8.config(bg='#f7ed2d')
            self.button_6.config(text='Start Methane')
            self.hydrocarbon = 'Methane'
            self.ratio = 9.52
        if gas == 1:
            self.flow_controller_methane.set_gas("C3H8")
            self.button_8.config(bg='#2cd137')
            self.button_7.config(bg='#f7ed2d')
            self.button_6.config(text='Start Propane')
            self.hydrocarbon = 'Propane'
            self.ratio = 23.9
    
    def setalarm(self):
        if self.disabled == True:
            self.disabled = False
            self.button_alarm.config(bg='#2cd137', text = "Disable Alarm")
        else:
            self.button_alarm.config(bg='#ed392f', text = "Enable Alarm")
            self.disabled = True

    
    def startnitrogenshroud(self, nitrogen):
        command = '{addr}{setpoint}\r'.format(addr="D", setpoint= int((float(nitrogen)/250)*64000))
        self.flow_controller_nitrogen._test_controller_open()
        self.flow_controller_nitrogen._write_and_read(command, self.retries)
    
    def startmethane(self, methane):
        command = '{addr}{setpoint}\r'.format(addr="B", setpoint= int((float(methane)/5)*64000))
        self.flow_controller_methane._test_controller_open()
        self.flow_controller_methane._write_and_read(command, self.retries)

    def startair(self, air):
        command = '{addr}{setpoint}\r'.format(addr="A", setpoint= int((float(air)/20)*64000))
        self.flow_controller_air._test_controller_open()
        self.flow_controller_air._write_and_read(command, self.retries)

    def startdecane(self, decane):
        command = '{addr}{setpoint}\r'.format(addr="C", setpoint= int((float(decane)/5)*64000))
        self.flow_controller_decane._test_controller_open()
        self.flow_controller_decane._write_and_read(command, self.retries)

    def stopflows(self):
        self.button_3.config(bg='#f7ed2d', text = "Start Decane")
        self.button_6.config(bg='#f7ed2d', text = "Start {}".format(self.hydrocarbon))
        self.button_5.config(bg='#f7ed2d', text = "Start Air")
        self.button_4.config(bg='#f7ed2d', text = "Nitrogen Shroud")
        try:
            self.startdecane(0)
        except:
            pass
        try:
            self.startair(0)
        except:
            pass
        try:
            self.startmethane(0)
        except:
            pass
        try:
            self.startnitrogenshroud(0)
        except:
            pass     

    def update(self):
        try:
            self.Vol_air = float(self.entry_methane.get())*float(self.entry_EQ.get())*self.ratio
            display_Vol_air = round(self.Vol_air,4)
            if float(self.entry_EQ.get()) > 1:
                self.label_air.config(text = display_Vol_air, fg = '#0e8f07')
            else:
                self.label_air.config(text = display_Vol_air, fg = '#8f0909')
        except:
            self.label_air.config(text = 'nan', fg = '#000000')
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
                print(data)
                if data >= 100.0:
                    self.alarm = True
                if self.disabled == False and self.alarm == True and data < 100.0:
                    self.playsound()
                self.y.append(data)
                self.timenow = datetime.now()
                self.floattimedelta = self.timenow - self.timepast
                self.deltatime = str(int(self.floattimedelta.total_seconds()))
                self.xstr.append(self.deltatime)
                self.xstr.pop(0)
                self.y.pop(0)
        self.ser.close()

    def playsound(self):
        winsound.Beep(950, 1000)
    
    def on_closing(self):
        self.ser.write(b'r')
        try:
            self.startdecane(0)
        except:
            pass
        try:
            self.startair(0)
        except:
            pass
        try:
            self.startmethane(0)
        except:
            pass
        try:
            self.startnitrogenshroud(0)
        except:
            pass 
        os._exit(1)

gui = CPG_GUI()

thread = Thread(target = gui.buildGUI)
thread.start()
thread2 = Thread(target = gui.arduino)
thread2.start()