##############################################################
# RPC3 Telnet Interface
# Casimir Sowinski
# 12/26/2017
##############################################################
import sys
# For getting password from user
import getpass
#For Telnet
import telnetlib
# For sleep
import time
# For GUI
import tkinter as tk
# For clock
import datetime
# For exception handling
import inspect

# Global variables
# Telnet
HOST = '192.168.1.250'
#yes = 'y'
#space = ' '
CR = '\r'
# 'enums'
status = ['OFF', 'ON']
color = ['red', 'green', 'orange']
# Control
RMSCurrent = 0.0
MaxCurrent = 0.0
Temp = 0.0
Bkr = 1
Outlet = [0, 0, 0, 0, 0, 0, 0, 0]
#doPrint = 1
#init = 1


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()
        self.getStatus(1)
        #self.update()        
    #####################################################################################        
    def create_widgets(self):
        self.master.title('RPC3 Client')
        # Constant Labels        
        self.labIP = tk.Label(self, text='RPC3 IP').grid(row=1, sticky="e")
        self.labBkr = tk.Label(self, text='Main Breaker').grid(row=2, sticky="e")
        self.labCur = tk.Label(self, text='RMS Current (A)').grid(row=3, sticky="e")
        self.labMax = tk.Label(self, text='Max Current (A)').grid(row=4, sticky="e")
        self.labOut = tk.Label(self, text='___________Outlet Breaker Control___________').grid(row=5, columnspan=5)
        self.labOut1 = tk.Label(self, text='ALL OUTLETS').grid(row=6, sticky="e", columnspan=2)
        self.labOut1 = tk.Label(self, text='Outlet 1').grid(row=7, sticky="e")
        self.labOut2 = tk.Label(self, text='Outlet 2').grid(row=8, sticky="e")
        self.labOut3 = tk.Label(self, text='Outlet 3').grid(row=9, sticky="e")
        self.labOut4 = tk.Label(self, text='Outlet 4').grid(row=10, sticky="e")
        self.labOut5 = tk.Label(self, text='Outlet 5').grid(row=11, sticky="e")
        self.labOut6 = tk.Label(self, text='Outlet 6').grid(row=12, sticky="e")
        self.labOut7 = tk.Label(self, text='Outlet 7').grid(row=13, sticky="e")
        self.labOut8 = tk.Label(self, text='Outlet 8').grid(row=14, sticky="e", pady=(0,5))
        # Variable Labels
        self.connectedTo = tk.Label(self, text='Conneceting...')
        self.connectedIP = tk.Label(self, text=str(HOST))
        self.ipVal = tk.Entry(self)
        self.bkrVal = tk.Label(self, text="On")    
        self.curVal = tk.Label(self, text="0.0")
        self.maxVal = tk.Label(self, text="0.0")
        #self.timeVal = tk.Label(self, text="12:00:00")
        self.connectedTo.grid(row=0, column=0, sticky='e', pady=(5,0))
        self.connectedTo.config(foreground=color[2])
        self.connectedIP.grid(row=0, column=1, columnspan=3, stick='w')
        self.ipVal.grid(row=1, column=2, columnspan=3, padx=(5, 5))
        self.bkrVal.grid(row=2, column=1)        
        self.curVal.grid(row=3, column=1)
        self.maxVal.grid(row=4, column=1)        
        #self.timeVal.grid(row=0, column=4, sticky="e")        
        self.outVal1 = tk.Label(self, text=str(status[Outlet[0]]), foreground=color[Outlet[0]])
        self.outVal2 = tk.Label(self, text=str(status[Outlet[1]]), foreground=color[Outlet[1]])
        self.outVal3 = tk.Label(self, text=str(status[Outlet[2]]), foreground=color[Outlet[2]])
        self.outVal4 = tk.Label(self, text=str(status[Outlet[3]]), foreground=color[Outlet[3]])
        self.outVal5 = tk.Label(self, text=str(status[Outlet[4]]), foreground=color[Outlet[4]])
        self.outVal6 = tk.Label(self, text=str(status[Outlet[5]]), foreground=color[Outlet[5]])
        self.outVal7 = tk.Label(self, text=str(status[Outlet[6]]), foreground=color[Outlet[6]])
        self.outVal8 = tk.Label(self, text=str(status[Outlet[7]]), foreground=color[Outlet[7]])
        self.outVal1.grid(row=7, column=1)
        self.outVal2.grid(row=8, column=1)
        self.outVal3.grid(row=9, column=1)
        self.outVal4.grid(row=10, column=1)
        self.outVal5.grid(row=11, column=1)
        self.outVal6.grid(row=12, column=1)
        self.outVal7.grid(row=13, column=1)        
        self.outVal8.grid(row=14, column=1, pady=(0,5))
        # Update button
        self.update = tk.Button(self, text='Update', command=self.getStatus(0))
        self.update.grid(row=0, column=4, pady=(5,0))
        # IP Entry/Button
        self.ipSet = tk.Button(self, text='Set', command=self.setIP)
        self.ipSet.grid(row=1, column=1)        
        # Max current reset Button
        self.outON1 = tk.Button(self, text='            Reset             ', command=self.reset).grid(row=4, column=2, columnspan=3)
        # Outlet Buttons
        self.outON0 = tk.Button(self, text='On', command=lambda x='ON 0': self.outlet(x)).grid(row=6, column=2)
        self.outON1 = tk.Button(self, text='On', command=lambda x='ON 1': self.outlet(x)).grid(row=7, column=2)
        self.outON2 = tk.Button(self, text='On', command=lambda x='ON 2': self.outlet(x)).grid(row=8, column=2)
        self.outON3 = tk.Button(self, text='On', command=lambda x='ON 3': self.outlet(x)).grid(row=9, column=2)
        self.outON4 = tk.Button(self, text='On', command=lambda x='ON 4': self.outlet(x)).grid(row=10, column=2)
        self.outON5 = tk.Button(self, text='On', command=lambda x='ON 5': self.outletn(x)).grid(row=11, column=2)
        self.outON6 = tk.Button(self, text='On', command=lambda x='ON 6': self.outlet(x)).grid(row=12, column=2)
        self.outON7 = tk.Button(self, text='On', command=lambda x='ON 7': self.outlet(x)).grid(row=13, column=2)
        self.outON8 = tk.Button(self, text='On', command=lambda x='ON 8': self.outlet(x)).grid(row=14, column=2, pady=(0,5))
        self.outOFF0 = tk.Button(self, text='Off', command=lambda x='OFF 0': self.outlet(x)).grid(row=6, column=3)
        self.outOFF1 = tk.Button(self, text='Off', command=lambda x='OFF 1': self.outlet(x)).grid(row=7, column=3)
        self.outOFF2 = tk.Button(self, text='Off', command=lambda x='OFF 2': self.outlet(x)).grid(row=8, column=3)
        self.outOFF3 = tk.Button(self, text='Off', command=lambda x='OFF 3': self.outlet(x)).grid(row=9, column=3)
        self.outOFF4 = tk.Button(self, text='Off', command=lambda x='OFF 4': self.outlet(x)).grid(row=10, column=3)
        self.outOFF5 = tk.Button(self, text='Off', command=lambda x='OFF 5': self.outlet(x)).grid(row=11, column=3)
        self.outOFF6 = tk.Button(self, text='Off', command=lambda x='OFF 6': self.outlet(x)).grid(row=12, column=3)
        self.outOFF7 = tk.Button(self, text='Off', command=lambda x='OFF 7': self.outlet(x)).grid(row=13, column=3)
        self.outOFF8 = tk.Button(self, text='Off', command=lambda x='OFF 8': self.outlet(x)).grid(row=14, column=3, pady=(0,5))
        self.outRB0 = tk.Button(self, text='Reboot', command=lambda x='REBOOT 0': self.outlet(x)).grid(row=6, column=4)
        self.outRB1 = tk.Button(self, text='Reboot', command=lambda x='REBOOT 1': self.outlet(x)).grid(row=7, column=4)
        self.outRB2 = tk.Button(self, text='Reboot', command=lambda x='REBOOT 2': self.outlet(x)).grid(row=8, column=4)
        self.outRB3 = tk.Button(self, text='Reboot', command=lambda x='REBOOT 3': self.outlet(x)).grid(row=9, column=4)
        self.outRB4 = tk.Button(self, text='Reboot', command=lambda x='REBOOT 4': self.outlet(x)).grid(row=10, column=4)
        self.outRB5 = tk.Button(self, text='Reboot', command=lambda x='REBOOT 5': self.outlet(x)).grid(row=11, column=4)
        self.outRB6 = tk.Button(self, text='Reboot', command=lambda x='REBOOT 6': self.outlet(x)).grid(row=12, column=4)
        self.outRB7 = tk.Button(self, text='Reboot', command=lambda x='REBOOT 7': self.outlet(x)).grid(row=13, column=4)
        self.outRB8 = tk.Button(self, text='Reboot', command=lambda x='REBOOT 8': self.outlet(x)).grid(row=14, column=4, pady=(0,5))
    #####################################################################################
    def setIP(self):
        global HOST 
        requestedIP = self.ipVal.get()
        # Doesn't update this for some reason
        self.connectedTo.config(text='Connecteing...', foreground=color[2])
        #time.sleep(1)
        print('----')
        print('Requested IP: ' + requestedIP)
        try:            
            tn = telnetlib.Telnet(requestedIP, 23, 2)   
            tn.close()
            print('Setting IP to: ' + requestedIP)
            HOST = requestedIP
            #self.connectedIP.config(text =
            self.getStatus(1)
        except IOError as e:
            self.connectedIP.config(text=requestedIP)
            self.ioError(e)
            #print('IOError in function setIP(self)')
            #print(e)
            #print('Cannot connect to ' + requestedIP)            
    #####################################################################################        
    def reset(self):
        print('----')
        print('Resetting')
        try:
            # Open Telnet session, open outlet control
            tn = telnetlib.Telnet(HOST, 23, 2)
            tn.read_until(b'Enter Selection>')
            tn.write(b'1\r')
            # Clear the max current, have to call clear twice or 'RC' to get it to flip
            tn.write(b'CLEAR\r')
            tn.read_until(b'RPC-3>')
            tn.write(b'RC\r')
            # Close Telnet session
            tn.close()
            #time.sleep(1)
            # Update UI            
            self.getStatus(0)
            print('Max: ' + str(MaxCurrent))
        except IOError as e:
            self.ioError(e)
            #print('IOError in function reset(self)')
            #print(e)
            #print('Cannot connect to ' + HOST)
    #####################################################################################        
    def outlet(self, arg):
        num = int(arg[-1])
        print(str(num))
        print('----')
        if (arg[-1] == '0'):
            print('Servicing ALL Outlets')
        else:
            print("Servicing Outlet: " + arg[-1])
        print("Command: " + arg[0:3])
        try:
            # Open Telnet session, open outlet control
            tn = telnetlib.Telnet(HOST, 23, 2)
            tn.read_until(b"Enter Selection>")
            tn.write(b"1\r")
            tn.read_until(b"RPC-3>")     
            buf = bytes(arg + CR, encoding="UTF-8")    
            tn.write(buf)
            tn.read_until(b"? (Y/N)>")
            tn.write(b"y\r")
            # Close Telnet session
            tn.close()
            time.sleep(1.0)
            self.getStatus(0)
        except IOError as e:
            self.ioError(self, e)
            #print('IOError in function outlet(self, arg)')
            #print(e)            
            #print('Cannot connect to ' + HOST)
    #####################################################################################        
    def getStatus(self, doPrint):
        global HOST, RMSCurrent, MaxCurrent, Temp, Bkr
        try:
            # Get status from PRC-3
            # Open Telnet session, open outlet control
            tn = telnetlib.Telnet(HOST, 23, 2)
            tn.read_until(b'Enter Selection>')
            tn.write(b'1\r')
            # Get current
            tn.read_until(b'current:  ')
            buffer = tn.read_until(b' Amps')
            buffer = buffer[0:3]
            RMSCurrent = float(buffer)
            # Get Max current
            tn.read_until(b'Detected:  ')
            buffer = tn.read_until(b' Amps')
            buffer = buffer[0:3]
            MaxCurrent = float(buffer)
            # Get Temperature
            tn.read_until(b'Temperature: ')
            buffer = tn.read_until(b'C')
            buffer = buffer[0:4]
            Temp = float(buffer)
            # Get main breaker status 
            tn.read_until(b'Breaker: ')
            buffer = tn.read_until(b'\n')
            buffer = buffer[0:3]
            if(buffer[1] == 'n'):
                Bkr = 1
            else:
                Brk = 0
            # Read outlet status, save in Outlet list
            for x in range(0,8):
                # Make a byte string of index+1 to find the beginning of outlet status
                buffer = str(x + 1).encode()
                # Read until 'Outlet #'
                tn.read_until(b'Outlet ' + buffer)
                tn.read_until(b'O')
                buffer = tn.read_until(b'\n')
                # If an 'n' is found then it is oN, otherwise it is oFf
                #print("buffer[" + str(x) + "]: " + buffer.decode())
                buffer2 = buffer.decode()
                #print(buffer2)
                if(buffer2[0] == 'n'):
                    Outlet[x] = 1
                    #print(str(x) + ": on")
                else:
                    Outlet[x] = 0
                    #print(str(x) + ": off")
            # Close Telnet session
            tn.close()
            # Print to console
            if(doPrint):
                print('RMS Current = ' + str(RMSCurrent) + ' Amps')
                print('Max Current = ' + str(MaxCurrent) + ' Amps')
                print('Internal Temperature = ' + str(Temp) + ' C')
                print('Circuit Breaker: ' + str(Bkr))
                for x in range(0,8):
                    if(Outlet[x]):
                        print('Outlet ' + str(x + 1) + ': on')
                    else:
                        print('Outlet ' + str(x + 1) + ': off')
            # Update UI values
            self.connectedIP.config(text=HOST)
            self.bkrVal.config(text=str(status[Bkr]))
            self.curVal.config(text=str(RMSCurrent))
            self.maxVal.config(text=str(MaxCurrent)) 
            self.connectedTo.config(text='Connected', foreground=color[1])            
            self.outVal1.config(text=str(status[Outlet[0]]), foreground=color[Outlet[0]])
            self.outVal2.config(text=str(status[Outlet[1]]), foreground=color[Outlet[1]])
            self.outVal3.config(text=str(status[Outlet[2]]), foreground=color[Outlet[2]])
            self.outVal4.config(text=str(status[Outlet[3]]), foreground=color[Outlet[3]])
            self.outVal5.config(text=str(status[Outlet[4]]), foreground=color[Outlet[4]])
            self.outVal6.config(text=str(status[Outlet[5]]), foreground=color[Outlet[5]])
            self.outVal7.config(text=str(status[Outlet[6]]), foreground=color[Outlet[6]])
            self.outVal8.config(text=str(status[Outlet[7]]), foreground=color[Outlet[7]])
        except IOError as e:
            self.ioError(e)
            #print('IOError in function getStatus(self, doPrint)')
            #print(e)            
            #print('Cannot connect to ' + HOST)
            #self.connectedTo.config(text='Not connected', foreground='red')
            #self.outVal1.config(text='?', foreground=color[2])
            #self.outVal2.config(text='?', foreground=color[2])
            #self.outVal3.config(text='?', foreground=color[2])
            #self.outVal4.config(text='?', foreground=color[2])
            #self.outVal5.config(text='?', foreground=color[2])
            #self.outVal6.config(text='?', foreground=color[2])
            #self.outVal7.config(text='?', foreground=color[2])
            #self.outVal8.config(text='?', foreground=color[2])
    #####################################################################################
    def ioError(self, e):
        print('IOError in function: ' + inspect.stack()[1][3])
        print(e)            
        print('Cannot connect to ' + HOST)
        self.connectedTo.config(text='Not connected', foreground=color[0])
        self.outVal1.config(text='?', foreground=color[2])
        self.outVal2.config(text='?', foreground=color[2])
        self.outVal3.config(text='?', foreground=color[2])
        self.outVal4.config(text='?', foreground=color[2])
        self.outVal5.config(text='?', foreground=color[2])
        self.outVal6.config(text='?', foreground=color[2])
        self.outVal7.config(text='?', foreground=color[2])
        self.outVal8.config(text='?', foreground=color[2])
        #print('0: ' + inspect.stack()[0][3]) # This function name
        #print('1: ' + inspect.stack()[1][3]) # calling function name
        #print('2: ' + inspect.stack()[2][3]) # calling function's caller, etc.
        #print('3: ' + inspect.stack()[3][3])
    #####################################################################################
    def update(self):
        print(time.strftime('%H:%M:%S'))
        root.after(100000, self.update())
    #####################################################################################

root = tk.Tk()
app = Application(master=root)
#app.update()
app.mainloop()

