from email.mime import text
import tkinter
from tkinter import ttk


class CoWINUI:
    def __init__(self):
        self.title = "CoWIN Status Checker"
        self.width = 375
        self.height = 250
        self.window = None
        self.GenWindow()
        self.ValHolders()
        self.InitDefaults()
        self.GenControls()
        self.InitControls()
        self.InitEventHandlers()

    def GenWindow(self):
        self.window = tkinter.Tk()
        self.window.config(background="white")
        self.window.title(self.title)
        self.window.geometry("%sx%s"%(self.width, self.height))

    def ValHolders(self):
        self.VarPinCode = tkinter.StringVar()
        self.VarAge = tkinter.StringVar()
        self.VarDestEmail = tkinter.StringVar()
        self.VarEmailType = tkinter.StringVar()
        self.VarGmailID = tkinter.StringVar()
        self.VarGmailPasswd = tkinter.StringVar()
        self.VarLog = tkinter.StringVar()
        self.VarDelaySuccess = tkinter.StringVar()
        self.VarDelayNoSuccess = tkinter.StringVar()

    def InitDefaults(self):
        self.EmailTypes = ["Outlook", "Gmail"]
        self.VarDelaySuccess.set(60)
        self.VarDelayNoSuccess.set(60)
        
    def GenControls(self):
        self.lbPinCode = tkinter.Label(self.window, text="Pin Code ", width=25, background="white")
        self.txtPinCode = tkinter.Entry(self.window, textvariable=self.VarPinCode, width=25)
        self.lbAge = tkinter.Label(self.window, text="Age ", width=25, background="white")
        self.txtAge = tkinter.Entry(self.window, textvariable=self.VarAge, width=25)
        self.lbDestEmail = tkinter.Label(self.window, text="Dest Email ", width=25, background="white")
        self.txtDestEmail = tkinter.Entry(self.window, textvariable=self.VarDestEmail, width=25)
        self.lbEmailType = tkinter.Label(self.window, text="Type ", width=25, background="white")
        self.cbEmailType = ttk.Combobox(self.window, textvariable=self.VarEmailType, state="readonly", width=22)
        self.lbGmailID = tkinter.Label(self.window, text="Gmail ID ", width=25, background="white")
        self.txtGmailID = tkinter.Entry(self.window, textvariable=self.VarGmailID, width=25)
        self.lbGmailPasswd = tkinter.Label(self.window, text="Gmail Pass ", width=25, background="white")
        self.txtGmailPasswd = tkinter.Entry(self.window, textvariable=self.VarGmailPasswd, show="*", width=25)
        self.btnRun = tkinter.Button(self.window, text="Run", width=20)
        self.btnStop = tkinter.Button(self.window, text="Stop", width=20)
        self.txtLog = tkinter.Entry(self.window, textvariable=self.VarLog, width=55, state="disabled")

        numValidation = self.window.register(self.only_numbers)
        self.lbDelaySuccess = tkinter.Label(self.window, text="DelayOnSuccess ", width=15, background="white")
        self.txtDelaySuccess = tkinter.Entry(self.window, validate="key", validatecommand=(numValidation, '%S'), textvariable=self.VarDelaySuccess, width=10, justify="center", background="white")
        self.lbDelayNoSuccess = tkinter.Label(self.window, text="DelayNoSuccess", width=15, background="white")
        self.txtDelayNoSuccess = tkinter.Entry(self.window, validate="key", validatecommand=(numValidation, '%S'), textvariable=self.VarDelayNoSuccess, width=10, justify="center", background="white")

    def InitControls(self):
        self.lbPinCode.grid(row=1, column=1)
        self.txtPinCode.grid(row=1, column=2, padx=10, pady=5)
        self.lbAge.grid(row=2, column=1)
        self.txtAge.grid(row=2, column=2, padx=10, pady=5)
        self.lbDestEmail.grid(row=3, column=1)
        self.txtDestEmail.grid(row=3, column=2, padx=10, pady=5)
        self.lbEmailType.grid(row=4, column=1)
        self.cbEmailType['values'] = self.EmailTypes
        self.cbEmailType.grid(row=4, column=2, padx=10, pady=5)
        self.lbDelaySuccess.grid(row=7, column=1, sticky='w')
        self.txtDelaySuccess.grid(row=7, column=1, sticky='e')
        self.lbDelayNoSuccess.grid(row=7, column=2, sticky='w')
        self.txtDelayNoSuccess.grid(row=7, column=2, sticky='e')
        self.btnRun.grid(row=8, column=1, padx=10, pady=5)
        self.btnStop.grid(row=8, column=2, padx=10, pady=5)
        self.txtLog.grid(row=9, column=1, rowspan=2, columnspan=2, padx=10, pady=5)
        self.btnStop.config(background="white", state="disabled")
        self.btnRun.config(background="white")

    def on_emailtype_change(self, index, value, op):
        if (self.VarEmailType.get() == "Outlook"):
            self.lbGmailID.grid_forget()
            self.txtGmailID.grid_forget()
            self.lbGmailPasswd.grid_forget()
            self.txtGmailPasswd.grid_forget()
            self.OutlookSelected = True
        
        else:
            self.lbGmailID.grid(row=5, column=1)
            self.txtGmailID.grid(row=5, column=2, padx=10, pady=5)
            self.lbGmailPasswd.grid(row=6, column=1)
            self.txtGmailPasswd.grid(row=6, column=2, padx=10, pady=5)
            self.OutlookSelected = False

    def InitEventHandlers(self):
        self.VarEmailType.trace('w', self.on_emailtype_change)

    def only_numbers(self, char):
        return char.isdigit()