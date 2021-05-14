# CoWIN
A simple script to monitor vaccine's availability using CoWIN's public APIs. I've tried to simplify the process so anyone can set it up and use in no time.

Requirements:
1. Must have MS Outlook installed and running when using this script.
2. Must have Python installed.

Process:
1. Download and install Python 3.7.3 from the following link: https://www.python.org/downloads/release/python-373/ (use the link highlighted in blue)
![image](https://user-images.githubusercontent.com/3834741/118314992-87f5be00-b512-11eb-85b5-202c32ce2337.png)

2. Install it. Also, if you do not want to deal with complicated setup of **Environment Variables**, remember to check this option highlighted below on the very first page of Python setup:
![image](https://user-images.githubusercontent.com/3834741/118315257-ea4ebe80-b512-11eb-824d-be72e7845904.png)

3. Open the **CoWIN.py** file with a text editor and go down to the bottom. You'll find three important variables that should be modified:
```
    Age = 25
    PinCode = 560029
    SendEmailTo = "destination@domain.ext"
    OutlookExists = False

    # If OutlookExists variable is set to False, enter the details below, i.e., 
    # UserName and Passwd. This is the email ID from which mail would be sent.
    # Go to https://support.google.com/accounts/answer/185833 for instructions on
    # how to generate an 'App Password' which must be assigned to Passwd instead of 
    # your actual password.
    EmailID = "from@gmail.com"
    Passwd = "tzfgmtovoqpomjxz"
```
Modify these to suit your search criteria. Save it and exit.

4. Before we run the script, we need to make sure that the required packages are installed. To do so, open _Command Prompt_ from under the Start menu, navigate to folder where you've saved this Python scipt (check **Note** section below if you don't know how) and run:
```
pip install -r requirements.txt
```

You need to run this step only once.

5. Now, open _Command Prompt_ from under Start menu, navigate to the folder where you've saved this Python scipt and run it using the command:
```
python CoWIN.py
```

## Note:
A. The image below shows that I'm under **C:\WINDOWS\system32**. 

![image](https://user-images.githubusercontent.com/3834741/118316250-3817f680-b514-11eb-9744-13644e77c370.png)

Likewise, you must navigate to the script's folder on _Command Prompt_ for this script to work.

For example, if your script is under **C:\Users\Admin\Downloads\CoWIN\CoWIN.py**, you must execute the following command first for step 4 and 5 to work:
```
cd C:\Users\Admin\Downloads\CoWIN\
```
B. If you get an error stating:
```
'python' is not recognized as an internal or external command,
operable program or batch file.
```
you messed up step 2. Try reinstalling or try adding Python's folder manually under **Environment Variables**.
