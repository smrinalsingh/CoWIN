import requests as r
import time
import datetime
import hashlib
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import win32com.client as win32

class CoWIN:
    def __init__(self, Age, PinCode, NoDays, SendEmailTo):
        #self.Mobile = Mobile
        self.Age = Age
        self.PinCode = PinCode
        self.NoDays = NoDays
        self.SendEmailTo = SendEmailTo
        self.httpsVerify = True
        self.ApiHost = "https://cdn-api.co-vin.in/api"
        self.GetOTPAPI = "/v2/auth/generateOTP"
        self.AuthOtpAPI = "/v2/auth/confirmOTP"
        self.GetBenefsAPI = "/v2/appointment/beneficiaries"
        self.headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"}

    def Authenticate(self):
        data = {"mobile": self.Mobile}
        genOtp = self.ApiHost + self.GetOTPAPI
        genOtpResp = r.post(genOtp, params=data, headers=self.headers, verify=self.httpsVerify)

        authOtpResp = False
        if (genOtpResp.ok):
            OTP = input("Enter the OTP: ")
            encOTP = hashlib.sha256(OTP.encode())
            data = {"otp": encOTP,
                    "txnId": ((genOtpResp.json())["txnId"])}
            authOtp = self.ApiHost + self.AuthOtpAPI
            authOtpResp = r.post(authOtp, params=data, headers=self.headers, verify=self.httpsVerify)
            
        else:
            print ("%s: %s"%(genOtpResp.status_code, (genOtpResp.json())["message"]))
        return authOtpResp

    def GetNearestAvailableSlot(self):
        timeNow = datetime.datetime.today()
        date_list = [timeNow + datetime.timedelta(days=x) for x in range(self.NoDays)]
        date_str = [x.strftime("%d-%m-%Y") for x in date_list]
        
        for date in date_str:
            GetCalendarByPinAPI = self.ApiHost + "/v2/appointment/sessions/public/calendarByPin?pincode={}&date={}".format(self.PinCode, date)

            getSlotsResp = r.get(GetCalendarByPinAPI, headers=self.headers, verify=self.httpsVerify)
            if getSlotsResp.ok:
                resp_json = getSlotsResp.json()

                # If there are centers available
                if resp_json["centers"]:
                    # Loop over each center's data
                    for center in resp_json["centers"]:
                        for session in center["sessions"]:
                            if session["min_age_limit"] <= self.Age:
                                if (int(session["available_capacity"]) > 0):
                                    print ("Slot Available!\nDate: %s\nCenter: %s\nAge: %s+\nBlock Name: %s\nAvailable Capacity: %s"%(date, center["name"], session["min_age_limit"], center["block_name"], session["available_capacity"]))
                                    return session["session_id"]
                                else:
                                    #print ("Availability 0 at %s"%(center["name"]))
                                    pass # If num of vaccine is 0
                            else:
                                #print ("Age criteria not met: %s"%(center["name"]))
                                pass # If age criteria isn't met
                else:
                    pass # No centers available
        
        return ""

    def GetAvailableSlotsString(self):
        timeNow = datetime.datetime.today()
        date_list = [timeNow + datetime.timedelta(days=x) for x in range(self.NoDays)]
        date_str = [x.strftime("%d-%m-%Y") for x in date_list]
        allAvailableData = []
        
        for date in date_str:
            GetCalendarByPinAPI = self.ApiHost + "/v2/appointment/sessions/public/calendarByPin?pincode={}&date={}".format(self.PinCode, date)

            getSlotsResp = r.get(GetCalendarByPinAPI, headers=self.headers, verify=self.httpsVerify)
            if getSlotsResp.ok:
                resp_json = getSlotsResp.json()

                # If there are centers available
                if resp_json["centers"]:
                    # Loop over each center's data
                    for center in resp_json["centers"]:
                        for session in center["sessions"]:
                            if session["min_age_limit"] <= self.Age:
                                if (int(session["available_capacity"]) > 0):
                                    if (int(session["available_capacity"]) > 0):
                                        body = "Vaccine available on %s \n Pin: %s \n Name: %s \n Block: %s \n Available: %s \n Vaccine: %s"%(session["date"], self.PinCode, center["name"], center["block_name"], session["available_capacity"], session["vaccine"])
                                        allAvailableData.append(body)
                                
                        else:
                            #print ("Age criteria not met: %s"%(center["name"]))
                            pass # If age criteria isn't met
                
                else:
                    pass # No centers available
        
        #return allAvailableData
        if (len(allAvailableData) > 0): 
            allAvailDataStr = "\n\n".join(allAvailableData)
            return allAvailDataStr

        return

    def SendOutlookEmail(self, body):
        outlook = win32.Dispatch("outlook.application")
        mail = outlook.CreateItem(0)
        mail.To = self.SendEmailTo
        mail.Subject = "Slot Available | %s"%(self.PinCode)
        mail.Body = body
        mail.Send()

    def SendSMTPEmail(self, body, emailID, passwd):
        message = MIMEMultipart()
        message['From'] = emailID
        message['To'] = self.SendEmailTo
        message['Subject'] = "Slot Available | %s"%(self.PinCode)
        message.attach(MIMEText(body, 'plain'))
        session = smtplib.SMTP('smtp.gmail.com', 587)
        session.starttls()
        session.login(emailID, passwd) #login with mail_id and password
        text = message.as_string()
        session.sendmail(emailID, self.SendEmailTo, text)
        session.quit()