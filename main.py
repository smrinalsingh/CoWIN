import pythoncom
import CoWIN
import CoWINUI
import threading as th
import time

global STOP_FLAG

def ExecuteCowin():
    global STOP_FLAG
    STOP_FLAG = False
    def CowinThread():
        pythoncom.CoInitialize()
        # Fill in these
        Age = int(co.VarAge.get())
        PinCode = int(co.VarPinCode.get())
        SendEmailTo = co.VarDestEmail.get()
        OutlookExists = co.OutlookSelected

        # If OutlookExists variable is set to False, enter the details below, i.e., 
        # UserName and Passwd. This is the email ID from which mail would be sent.
        # Go to https://support.google.com/accounts/answer/185833 for instructions on
        # how to generate an 'App Password' which must be assigned to Passwd variable below 
        # instead of your actual password.
        EmailID = co.VarGmailID.get()
        Passwd = co.VarGmailPasswd.get()

        # Don't change it. Looks like next 7 days' data anyways comes with API call.
        NoDays = 1

        # This defines the delay between each check. Try to keep it above 2 mins, 
        # i.e. 120 second, otherwise your IP may get blocked temporarily.
        DelayUnsuccessful = int(co.VarDelayNoSuccess.get())

        # This is incase vaccine is available. Keep it high if you don't want to be 
        # spammed with mails when vaccines becomes available.
        DelaySuccessful = int(co.VarDelaySuccess.get())
        
        # Don't bother.
        co.btnRun.config(state="disabled")
        co.btnStop.config(state="normal")
        co.VarLog.set("Execution Started")
        try:
            register = CoWIN.CoWIN(Age, PinCode, NoDays, SendEmailTo)
            IsExecutable = True
            while (not STOP_FLAG and IsExecutable):
                SlotsAvailable = register.GetAvailableSlotsString()
                if SlotsAvailable:
                    if (OutlookExists):
                        register.SendOutlookEmail(SlotsAvailable)
                    else:
                        try:
                            register.SendSMTPEmail(SlotsAvailable, EmailID, Passwd)
                        except Exception as e:
                            try:
                                co.VarLog.set("Error: %s"%e)
                                IsExecutable = False
                            except:
                                pass
                    time.sleep(DelaySuccessful)
                else:
                    time.sleep(DelayUnsuccessful)
        except Exception as e:
            print ("Error: %s"%e)
        finally:
            try:
                co.btnRun.config(state="normal")
                co.btnStop.config(state="disabled")
                co.VarLog.set("Execution Stopped")
            except RuntimeError:
                print ("Monitoring Terminated")

    th.Thread(target=CowinThread).start()

def StopExecution():
    global STOP_FLAG
    STOP_FLAG = True

def on_closing():
    global STOP_FLAG
    STOP_FLAG = True
    co.window.destroy()

if __name__ == "__main__":
    co = CoWINUI.CoWINUI()
    co.window.protocol("WM_DELETE_WINDOW", on_closing)
    co.btnRun.config(command=ExecuteCowin)
    co.btnStop.config(command=StopExecution)
    co.window.mainloop()