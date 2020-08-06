# Imports
from __future__ import print_function
from tkinter import *
from tkinter import ttk
import mysql.connector as sql
from PIL import ImageTk, Image
import time
import requests
import smtplib
import os
from datetime import date
from tkinter import messagebox
from tkinter import filedialog
import pyAesCrypt as pY
from dotenv import load_dotenv


load_dotenv()
LARGE_FONT = ("Verdana", 12)


class Archer(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.container = Frame(self)

        self.container.pack(side=TOP, fill=BOTH, expand=True)

        self.container.rowconfigure(0, weight=1)
        self.container.columnconfigure(0, weight=1)

        self.frames = {}

        for F in (Home, Admin, Login, SMS, Email, Weather, Journal, Personal, Exercise, ToDo, Encryption, Decryption):
            frame = F(self.container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

            self.show_frame(Home)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class Home(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        controller.geometry("1200x800")
        controller.title("Archer")
        controller.resizable(height=False, width=False)

        self.icon = os.path.join("Images", "favicon.ico")

        controller.iconbitmap(self.icon)

        self.title = ttk.Label(self, text="Archer Home Page", font=LARGE_FONT, width=20)
        self.title.pack(side=TOP)

        self.image = ImageTk.PhotoImage(Image.open(os.path.join("Images", "Screen_image.jpg")))

        self.screen_image = Label(self, image=self.image)
        self.screen_image.pack()

        self.login = ttk.Button(self, text="Login Page", width=23, command=lambda: controller.show_frame(Login))
        self.login.place(x=490, y=390)


class Login(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        # Image
        self.image = ImageTk.PhotoImage(Image.open(os.path.join("Images", "Admin_screen.jpg")))

        self.screen_image = Label(self, image=self.image)

        # Labels
        self.username_label = ttk.Label(self, text="Username: ", font=LARGE_FONT)
        self.password_label = ttk.Label(self, text="Password: ", font=LARGE_FONT)
        self.title = ttk.Label(self, text="Login Page", font=LARGE_FONT)

        # Entry's
        self.admin = ttk.Entry(self, textvariable=StringVar(), width=30)
        self.adminpass = ttk.Entry(self, textvariable=StringVar(), show="*", width=30)

        # Buttons
        self.login = ttk.Button(self, text="Login", command=lambda: self.Login(), width=27)

        # Grid Placements
        self.username_label.place(x=410, y=290)
        self.admin.place(x=505, y=290)

        self.password_label.place(x=410, y=340)
        self.adminpass.place(x=505, y=340)

        self.login.place(x=510, y=390)

        self.title.pack(side=TOP)
        self.screen_image.pack()

    def Login(self):
        # Database
        db = sql.connect(host="yourHost",
                         user="yourUser",
                         password="yourPass",
                         database="yourDatabase")

        cursor = db.cursor()

        while True:

            user = self.admin.get()
            passwd = self.adminpass.get()

            cursor.execute(f"select * from login where Username='{user}' and Password='{passwd}'")
            account = cursor.fetchall()

            if account:
                self.controller.show_frame(Admin)
                break
            else:
                self.controller.show_frame(Home)
                break

        cursor.close()
        db.close()

        self.admin.delete(0, END)
        self.adminpass.delete(0, END)


class Admin(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        # Labels
        self.title = ttk.Label(self, text="Admin Control Window", font=LARGE_FONT)

        self.title.pack(side=TOP)

        self.image = ImageTk.PhotoImage(Image.open(os.path.join("Images", "Admin_screen.jpg")))

        self.screen_image = Label(self, image=self.image)

        # Archer Functions
        self.sms = ttk.Button(self, text="SMS", command=lambda: controller.show_frame(SMS), width=22)
        self.email = ttk.Button(self, text="SMTP", command=lambda: controller.show_frame(Email), width=22)
        self.weather = ttk.Button(self, text="Weather", command=lambda: controller.show_frame(Weather), width=22)
        self.mood = ttk.Button(self, text="Mood", command=lambda: controller.show_frame(Mood), width=22)
        self.journal = ttk.Button(self, text="Journal", command=lambda: controller.show_frame(Journal), width=22)
        self.personal = ttk.Button(self, text="Personal", command=lambda: controller.show_frame(Personal), width=22)
        self.exercise = ttk.Button(self, text="Exercise", command=lambda: controller.show_frame(Exercise), width=22)
        self.meds = ttk.Button(self, text="Meds", command=lambda: controller.show_frame(Meds), width=22)
        self.todo = ttk.Button(self, text="To Do", command=lambda: controller.show_frame(ToDo), width=22)
        self.encrypt = ttk.Button(self, text="Encrypt File", command=lambda: controller.show_frame(Encryption), width=22)
        self.decrypt = ttk.Button(self, text="Decrypt File", command=lambda: controller.show_frame(Decryption), width=22)
        self.logout = ttk.Button(self, text="Logout", command=lambda: controller.show_frame(Home), width=22)

        # Placements
        self.screen_image.pack()
        # Column 1
        self.sms.place(x=120, y=260)

        self.email.place(x=120, y=360)

        self.weather.place(x=120, y=460)
        # Column 2
        self.mood.place(x=360, y=260)

        self.journal.place(x=360, y=360)

        self.personal.place(x=360, y=460)
        # Column 3
        self.exercise.place(x=600, y=260)

        self.meds.place(x=600, y=360)

        self.todo.place(x=600, y=460)
        # Column 4
        self.encrypt.place(x=840, y=260)

        self.decrypt.place(x=840, y=360)

        self.logout.place(x=840, y=460)


class SMS(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        # Image
        self.image = ImageTk.PhotoImage(Image.open(os.path.join("Images", "Screen_image.jpg")))
        self.screen_image = Label(self, image=self.image)
        self.screen_image.pack()

        # Carriers
        self.carriers = {
            'att': '@mms.att.net',
            'tmobile': "@tmomail.net",
            'verizon': '@vtext.com',
            'sprint': '@page.nextel.com'}

        self.contacts = {
            'person': "number",
            'person': "number",
            'person': "number",
            'person': "number"
        }

        self.contacts_carrier = {
            "person": "carrier",
            "person": "carrier",
            "person": "carrier",
            "person": "carrier"
        }

        # Text Entry
        self.text_box = ttk.Entry(self, font=LARGE_FONT, width=120)
        self.text_box.place(x=0, y=777)

        # Number Entry
        self.number_entry = ttk.Entry(self, font=LARGE_FONT)
        self.number_entry.place(x=505, y=290)
        self.number_label = ttk.Label(self, text="Number: ")
        self.number_label.place(x=410, y=290)

        # Carrier Entry
        self.carrier_entry = ttk.Entry(self, font=LARGE_FONT)
        self.carrier_entry.place(x=505, y=340)
        self.carrier_label = ttk.Label(self, text="Phone Carrier: ")
        self.carrier_label.place(x=410, y=340)

        # Carrier Label
        self.att = ttk.Label(self, text="att " + self.carriers['att'], font=LARGE_FONT)
        self.tmobile = ttk.Label(self, text="tmobile " + self.carriers['tmobile'], font=LARGE_FONT)
        self.verizon = ttk.Label(self, text="verizon " + self.carriers['verizon'], font=LARGE_FONT)
        self.sprint = ttk.Label(self, text="sprint " + self.carriers['sprint'], font=LARGE_FONT)

        # Carrier Label Placements
        self.att.place(x=120, y=150)
        self.tmobile.place(x=120, y=220)
        self.verizon.place(x=120, y=290)
        self.sprint.place(x=120, y=360)

        # Send Button
        self.send_button = ttk.Button(self, text="Send Message", command=self.send_message, width=22)
        self.send_button.place(x=530, y=400)

        # back Button
        self.back = ttk.Button(self, text="Back to Admin", command=lambda: controller.show_frame(Admin), width=22)
        self.back.place(x=530, y=440)

        # Time and Date
        self.t = time.localtime()
        self.systemTime = time.strftime("%I:%M:%S %p", self.t)
        self.date = str(date.today())

    def send_message(self):
        number = self.number_entry.get()
        number_carrier = self.carrier_entry.get()
        auth = ["youEmail", "yourPass"]

        # Mail Server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(auth[0], auth[1])

        # Send Text message
        if number == "Mom" and number_carrier == "Mom":
            server.sendmail(auth[0], self.contacts["Mom"] + self.contacts_carrier['Mom'], self.text_box.get())

        if number == "Kayla" and number_carrier == "Kayla":
            server.sendmail(auth[0], self.contacts["Kayla"] + self.contacts_carrier['Kayla'], self.text_box.get())

        if number == "Dad" and number_carrier == "Dad":
            server.sendmail(auth[0], self.contacts["Dad"] + self.contacts_carrier['Dad'], self.text_box.get())

        if number == "Caden" and number_carrier == "Caden":
            server.sendmail(auth[0], self.contacts["Caden"] + self.contacts_carrier['Caden'], self.text_box.get())

        else:
            server.sendmail(auth[0], number + number_carrier, self.text_box.get())

        if smtplib.SMTPException is not True:
            print("Text Sent")

            db = sql.connect(host="192.168.1.21",
                             user="ZaneColeRiley",
                             password="CadenRiley214569",
                             database="archer")
            cursor = db.cursor()

            stmt = f"""INSERT INTO archer.sms (carrier, to_, from_, msg, date_time) VALUES ('{self.carrier_entry.get()}', '{self.number_entry.get()}', 
                                                                                                    '{auth[0]}', '{self.text_box.get()}', 
                                                                                                    '{self.date + ' ' + self.systemTime}');"""

            cursor.execute(stmt)

            print(cursor.rowcount, "Record added to database")

            db.commit()
            db.close()

        self.number_entry.delete(0, END)
        self.text_box.delete(0, END)
        self.carrier_entry.delete(0, END)


class Email(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        # Image
        self.image = ImageTk.PhotoImage(Image.open(os.path.join("Images", "Screen_image.jpg")))

        self.screen_image = Label(self, image=self.image)

        # Title

        self.title = ttk.Label(self, text="SMTP", font=LARGE_FONT)

        # Text Box
        self.message = Text(self, height=4, width=50, font=LARGE_FONT)

        # Entry's
        self.senders_email = ttk.Entry(self, width=27)
        self.recipients_email = ttk.Entry(self, width=27)
        self.password = ttk.Entry(self, width=27, show="*")

        # Labels
        self.senders_email_label = ttk.Label(self, text="Your email address")
        self.recipients_email_label = ttk.Label(self, text="recipients email address")
        self.password_label = ttk.Label(self, text="Your email password")

        # Buttons
        self.email = ttk.Button(self, text="Send Email", command=self.send_mail, width=22)
        self.back = ttk.Button(self, text="Back to Admin", command=lambda: controller.show_frame(Admin), width=22)

        # Placements
        self.screen_image.pack()
        self.title.pack()

        self.senders_email_label.place(x=380, y=290)
        self.senders_email.place(x=505, y=290)

        self.recipients_email_label.place(x=370, y=340)
        self.recipients_email.place(x=505, y=340)

        self.password_label.place(x=380, y=390)
        self.password.place(x=505, y=390)

        self.message.place(x=310, y=450)

        self.email.place(x=512, y=570)
        self.back.place(x=512, y=620)

        self.t = time.localtime()
        self.systemTime = str(time.strftime("%I:%M %p", self.t))
        self.date = str(date.today())

    def send_mail(self):
        message = self.message.get("1.0", END)
        senders_email = self.senders_email.get()
        recipients_email = self.recipients_email.get()
        senders_password = self.password.get()
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(senders_email, senders_password)
            server.sendmail(senders_email, recipients_email, message)

        except smtplib.SMTPException as e:
            print(e)
            print("Error: Message not sent.")

        finally:
            if smtplib.SMTPException is False:
                print("Email sent.")

                db = sql.connect(host="yourHost",
                         user="yourUser",
                         password="yourPass",
                         database="yourDatabase")
                cursor = db.cursor()

                stmt = f"""INSERT INTO archer.smtp (senderEmail, recipientsEmail, msg, date_time) VALUES  ('{self.senders_email.get()}', '{self.recipients_email.get()}', 
                                                                                                                   '{self.message.get('1.0', END)}', '{self.date + ' ' + self.systemTime}');"""

                cursor.execute(stmt)

                db.commit()
                print(cursor.rowcount, "Record Successfully Added in to table")
                db.close()

                self.password.delete(0, END)
                self.senders_email.delete(0, END)
                self.recipients_email.delete(0, END)
                self.message.delete("1.0", END)


class Weather(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        # Screen Image
        self.image = ImageTk.PhotoImage(Image.open(os.path.join("Images", "Screen_image.jpg")))
        self.screen_image = Label(self, image=self.image)
        self.screen_image.pack()

        # Weather aip links
        self.url = "http://api.weatherapi.com/v1/current.json?key=9d1a06cf296748bba91154256201606&q=77494"
        self.url_air = "http://www.airnowapi.org/aq/observation/zipCode/current/?format=application/json&zipCode=77494&distance=35&API_KEY=1069D93A-9C50-44C5-B70D-F10624F40038"

        # System Time
        self.t = time.localtime()
        self.systemTime = str(time.strftime("%I:%M %p", self.t))

        # Function Buttons
        self.weather = ttk.Button(self, text="Weather", command=self.printWeather, width=22)
        self.weather.place(x=512, y=570)
        self.back = ttk.Button(self, text="Back", command=lambda: controller.show_frame(Admin), width=22)
        self.back.place(x=512, y=620)
        self.data = ttk.Button(self, text="Commit data", command=self.toDataBase, width=22)
        self.data.place(x=512, y=720)

    def printWeather(self):

        # Weather data collection
        response = requests.get(url=self.url)
        response_air = requests.get(url=self.url_air)

        response_json = response.json()
        air_response = response_air.json()

        # Weather Labels
        condition_label = ttk.Label(self, text=str(response_json["current"]["condition"]["text"]), font=LARGE_FONT)
        currentTemp_label = ttk.Label(self, text=str(response_json["current"]["temp_f"]) + " degrees Fahrenheit", font=LARGE_FONT)
        humidity_label = ttk.Label(self, text=str(response_json["current"]["humidity"]) + " Percent humidity", font=LARGE_FONT)
        feelsLike_label = ttk.Label(self, text="Feels Like " + str(response_json["current"]["feelslike_f"]) + " degrees Fahrenheit", font=LARGE_FONT)
        uvIndex_label = ttk.Label(self, text="UV Index is " + str(response_json["current"]["uv"]), font=LARGE_FONT)
        precip_in = ttk.Label(self, text="It rained " + str(response_json['current']['precip_in']) + "Inches", font=LARGE_FONT)
        airQ = ttk.Label(self, text="Current Air Quality " + str(air_response[1]['Category']['Name']), font=LARGE_FONT)
        uvSafetyIndex = ttk.Label(self, text="UV Safety Index", font=LARGE_FONT)
        uvSafetyIndex1 = ttk.Label(self, text="0 to 2 is Low Danger", font=LARGE_FONT)
        uvSafetyIndex2 = ttk.Label(self, text="3 to 5 is Moderate Danger", font=LARGE_FONT)
        uvSafetyIndex3 = ttk.Label(self, text="6 to 7 is High Danger", font=LARGE_FONT)
        uvSafetyIndex4 = ttk.Label(self, text="8 to 10 is Danger is Very High", font=LARGE_FONT)
        uvSafetyIndex5 = ttk.Label(self, text="11 or more is Extreme Danger", font=LARGE_FONT)

        # Placements

        condition_label.place(x=312, y=50)
        currentTemp_label.place(x=312, y=120)
        humidity_label.place(x=312, y=190)
        feelsLike_label.place(x=312, y=260)
        precip_in.place(x=312, y=330)
        airQ.place(x=312, y=400)
        uvIndex_label.place(x=312, y=470)
        uvSafetyIndex.place(x=780, y=120)
        uvSafetyIndex1.place(x=612, y=120)
        uvSafetyIndex2.place(x=612, y=190)
        uvSafetyIndex3.place(x=612, y=260)
        uvSafetyIndex4.place(x=612, y=330)
        uvSafetyIndex5.place(x=612, y=50)

    def toDataBase(self):
        try:
            response = requests.get(self.url)
            response_air = requests.get(self.url_air)

            response_json = response.json()
            air_response = response_air.json()

            db = sql.connect(host="yourHost",
                         user="yourUser",
                         password="yourPass",
                         database="yourDatabase")
            cursor = db.cursor()

            insertTableInfo = f"""INSERT INTO archer.weather (condition_, temp_f, feelsLike, humidity, uvIndex, precip_in , air_Q, date_)  VALUES 
                                            ('{str(response_json["current"]["condition"]["text"])}', '{str(response_json["current"]["temp_f"])}',
                                              '{str(response_json["current"]["feelslike_f"])}', '{str(response_json["current"]["humidity"])}', '{str(response_json["current"]["uv"])}',
                                              '{str(response_json['current']['precip_in'])}', '{str(air_response[1]['Category']['Name'])}', '{str(date.today()) + ' ' + self.systemTime}')"""

            cursor.execute(insertTableInfo)

            db.commit()
            print(cursor.rowcount, "Record Successfully Added in to table")
            cursor.close()
            db.close()
        except sql.Error as error:
            print("Failed to input data {}".format(error))


class Journal(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        # Screen Image
        self.image = ImageTk.PhotoImage(Image.open(os.path.join("Images", 'Journal.jpg')))
        self.screenImage = Label(self, image=self.image)
        self.screenImage.pack()

        # Entry's
        self.morning = Text(self, width=50, height=3, font=LARGE_FONT)
        self.afternoon = Text(self, width=50, height=3, font=LARGE_FONT)
        self.evening = Text(self, width=50, height=3, font=LARGE_FONT)

        # Labels
        self.morning_label = ttk.Label(self, text="Morning", font=LARGE_FONT)
        self.afternoon_label = ttk.Label(self, text="Afternoon", font=LARGE_FONT)
        self.evening_label = ttk.Label(self, text="Evening", font=LARGE_FONT)

        # Buttons
        self.commitEntry = ttk.Button(self, text="Commit Entry", width=22, command=self.addEntry)
        self.back = ttk.Button(self, text="Back to Admin", width=22, command=lambda: controller.show_frame(Admin))

        # Placements
        self.morning_label.place(x=280, y=280)
        self.morning.place(x=505, y=260)

        self.afternoon_label.place(x=280, y=380)
        self.afternoon.place(x=505, y=370)

        self.evening_label.place(x=280, y=500)
        self.evening.place(x=505, y=480)

        self.commitEntry.place(x=640, y=610)
        self.back.place(x=640, y=660)

    def addEntry(self):
        db = sql.connect(host="yourHost",
                         user="yourUser",
                         password="yourPass",
                         database="yourDatabase")

        cursor = db.cursor()

        # Time
        t = time.localtime()
        systemTime = str(time.strftime("%I:%M:%S %p", t))

        stmt = f"""INSERT INTO archer.journal (morning, afternoon, evening, date_time) VALUES 
                                              ('{self.morning.get('1.0', END)}', '{self.afternoon.get('1.0', END)}', 
                                               '{self.evening.get('1.0', END)}', '{str(date.today()) + ' ' + systemTime}')"""

        cursor.execute(stmt)
        print(cursor.rowcount, "Record added to your DataBase Journal")
        cursor.close()

        db.commit()
        db.close()
        self.morning.delete('1.0', END)
        self.afternoon.delete('1.0', END)
        self.evening.delete('1.0', END)


class Personal(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        # Labels
        self.title = ttk.Label(self, text="Write Your personal Entry Here", font=LARGE_FONT)
        self.title.pack(side=TOP)

        # Screen Image
        self.image = ImageTk.PhotoImage(Image.open(os.path.join("Images", 'Journal.jpg')))
        self.screenImage = Label(self, image=self.image)
        self.screenImage.pack()

        # Entry's
        self.entry = Text(self, width=50, height=3, font=LARGE_FONT)

        # Buttons
        self.commit = ttk.Button(self, text="Commit Entry", command=self.addEntry, width=22)
        self.back = ttk.Button(self, text="Back to admin", command=lambda: controller.show_frame(Admin), width=22)

        # Placements
        self.entry.place(x=335, y=410)

        self.commit.place(x=520, y=510)
        self.back.place(x=520, y=560)

    def addEntry(self):
        db = sql.connect(host="yourHost",
                         user="yourUser",
                         password="yourPass",
                         database="yourDatabase")

        cursor = db.cursor()

        # Time
        t = time.localtime()
        systemTime = str(time.strftime("%I:%M:%S %p", t))

        stmt = f"INSERT INTO archer.personal (dataEntry, date_time) VALUES ('{self.entry.get('1.0', END)}', '{str(date.today()) + ' ' + systemTime}')"

        cursor.execute(stmt)
        print(cursor.rowcount, "Record added to your Personal DataBase Journal")
        cursor.close()

        db.commit()
        db.close()
        self.entry.delete("1.0", END)


class Exercise(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        # Screen Image
        self.image = ImageTk.PhotoImage(Image.open(os.path.join("Images", 'Journal.jpg')))
        self.screenImage = Label(self, image=self.image)
        self.screenImage.pack()

        # Time
        self.t = time.localtime()
        self.systemTime = str(time.strftime("%I:%M:%S %p", self.t))

        # Entry's
        self.type_ = ttk.Entry(self, width=22, font=LARGE_FONT)
        self.timeOfDay = ttk.Entry(self, width=22, font=LARGE_FONT)
        self.howLong = ttk.Entry(self, width=22, font=LARGE_FONT)
        self.env = ttk.Entry(self, width=22, font=LARGE_FONT)
        self.miles = ttk.Entry(self, width=22, font=LARGE_FONT)

        # Labels
        self.type__label = ttk.Label(self, text="Type", font=LARGE_FONT)
        self.timeOfDay_label = ttk.Label(self, text="Time of Day", font=LARGE_FONT)
        self.howLong_label = ttk.Label(self, text="Total Time", font=LARGE_FONT)
        self.env_label = ttk.Label(self, text="Environment", font=LARGE_FONT)
        self.miles_label = ttk.Label(self, text="Miles", font=LARGE_FONT)

        # Buttons
        self.commit = ttk.Button(self, text="Commit Entry", command=self.addEntry, width=22)
        self.back = ttk.Button(self, text="Back to admin", command=lambda: controller.show_frame(Admin), width=22)

        # Placements
        self.type__label.place(x=360, y=260)
        self.type_.place(x=505, y=260)

        self.timeOfDay_label.place(x=360, y=310)
        self.timeOfDay.place(x=505, y=310)

        self.howLong_label.place(x=360, y=360)
        self.howLong.place(x=505, y=360)

        self.env_label.place(x=360, y=410)
        self.env.place(x=505, y=410)

        self.miles_label.place(x=360, y=460)
        self.miles.place(x=505, y=460)

        self.commit.place(x=560, y=510)
        self.back.place(x=560, y=540)

    def addEntry(self):
        db = sql.connect(host="yourHost",
                         user="yourUser",
                         password="yourPass",
                         database="yourDatabase")

        cursor = db.cursor()

        stmt = f"""INSERT INTO archer.exercise (type_, timeOfDay, howLong, environment, miles, date_time) VALUES 
                                               ('{self.type_.get()}', '{self.timeOfDay.get()}', '{self.howLong.get()}',
                                               ' {self.env.get()}', '{self.miles.get()}' ,'{str(date.today()) + ' ' + self.systemTime}')"""

        cursor.execute(stmt)
        print(cursor.rowcount, "Record Added to DataBase")
        cursor.close()

        db.commit()
        db.close()
        self.type_.delete(0, END)
        self.timeOfDay.delete(0, END)
        self.howLong.delete(0, END)
        self.env.delete(0, END)
        self.miles.delete(0, END)


class ToDo(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        # title
        self.title = ttk.Label(self, text="To Do", font=LARGE_FONT)
        self.title.pack(side=TOP)

        # Image
        self.image = ImageTk.PhotoImage(Image.open(os.path.join("Images", 'Journal.jpg')))
        self.screen_image = Label(self, image=self.image)
        self.screen_image.pack()

        # Time
        self.t = time.localtime()
        self.systemTime = str(time.strftime("%I:%M %p", self.t))

        # Labels
        self.shower_Label = ttk.Label(self, text="Shower: ", font=LARGE_FONT)
        self.teeth_Label = ttk.Label(self, text="Brushed Teeth: ", font=LARGE_FONT)

        # Entry's
        self.shower = ttk.Entry(self, width=25, font=LARGE_FONT)
        self.teeth = ttk.Entry(self, width=25, font=LARGE_FONT)

        # Buttons
        self.commit = ttk.Button(self, text="Commit Data", command=self.addEntry, width=22)
        self.back = ttk.Button(self, text="Back to admin", command=lambda: controller.show_frame(Admin), width=22)

        # Placements
        self.shower_Label.place(x=380, y=260)
        self.shower.place(x=505, y=260)

        self.teeth_Label.place(x=370, y=310)
        self.teeth.place(x=505, y=310)

        self.commit.place(x=515, y=360)
        self.back.place(x=515, y=390)

    def addEntry(self):
        db = sql.connect(host="yourHost",
                         user="yourUser",
                         password="yourPass",
                         database="yourDatabase")
        cursor = db.cursor()

        stmt = f"INSERT INTO archer.todo (shower, teeth, date_time) VALUES ('{self.shower.get()}', '{self.teeth.get()}', '{str(date.today()) + ' ' + self.systemTime}')"

        cursor.execute(stmt)
        print(cursor.rowcount, "Record Added")
        cursor.close()

        db.commit()
        db.close()
        self.shower.delete(0, END)
        self.teeth.delete(0, END)


class Encryption(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        # Title
        self.title = ttk.Label(self, text="Encryption", font=LARGE_FONT)
        self.title.pack(side=TOP)

        # Screen Image
        self.image = ImageTk.PhotoImage(Image.open(os.path.join("Images", "Screen_image.jpg")))
        self.screen_image = Label(self, image=self.image)
        self.screen_image.pack()

        # Encryption button
        self.encrypt = ttk.Button(self, text='Encrypt File', width=22, command=self.encryption)

        # File Button
        self.file_Button = Button(self, width=22, text="Open File", command=self.openFile)

        # Back Button
        self.back = ttk.Button(self, text="Back to admin", width=22, command=lambda: controller.show_frame(Admin))

        # Entry's
        self.file = ttk.Entry(self, width=22)
        self.password = ttk.Entry(self, width=22)

        # Labels
        self.file_Label = ttk.Label(self, text="File", font=LARGE_FONT)
        self.password_Label = ttk.Label(self, text="Password", font=LARGE_FONT)

        # Placements
        self.file_Label.place(x=380, y=260)
        self.file.place(x=505, y=260)

        self.password_Label.place(x=380, y=310)
        self.password.place(x=505, y=310)

        self.encrypt.place(x=515, y=360)
        self.file_Button.place(x=650, y=260)
        self.back.place(x=515, y=410)

    def encryption(self):
        db = sql.connect(host="yourHost",
                         user="yourUser",
                         password="yourPass",
                         database="yourDatabase")
        cursor = db.cursor()
        stmt = f"INSERT INTO crypt.passwords (filename, password) VALUES ('{self.file.get()}', '{self.password.get()}')"
        cursor.execute(stmt)
        bufferSize = 64 * 1024
        pY.encryptFile(self.file.get(), 'Archer.encrypted.file', self.password.get(), bufferSize=bufferSize)
        return messagebox.showinfo(title="Encrypted", message="Encrypted you file")

    def openFile(self):
        File = filedialog.askopenfilename(title="Select a file", initialdir="C:/Users/smithOneDrive/Desktop", filetypes=(('txt', "*.txt"), ("csv", "*.csv"), ("all files", "*.*")))
        return self.file.insert(0, File)


class Decryption(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        # Title
        self.title = ttk.Label(self, text="Encryption", font=LARGE_FONT)
        self.title.pack(side=TOP)

        # Screen Image
        self.image = ImageTk.PhotoImage(Image.open(os.path.join("Images", "Screen_image.jpg")))
        self.screen_image = Label(self, image=self.image)
        self.screen_image.pack()

        # Decryption button
        self.decrypt = ttk.Button(self, text='Decrypt File', width=22, command=self.decryption)

        # File Button
        self.File = ttk.Button(self, text="Open File", command=self.openFile)

        # Back Button
        self.back = ttk.Button(self, text="Back to admin", width=22, command=lambda: controller.show_frame(Admin))

        # Entry's
        self.file = ttk.Entry(self, width=22)
        self.password = ttk.Entry(self, width=22)

        # Labels
        self.file_Label = ttk.Label(self, text="File", font=LARGE_FONT)
        self.password_Label = ttk.Label(self, text="Password", font=LARGE_FONT)

        # Placements
        self.file_Label.place(x=380, y=260)
        self.file.place(x=505, y=260)

        self.password_Label.place(x=380, y=310)
        self.password.place(x=505, y=310)

        self.decrypt.place(x=515, y=360)
        self.File.place(x=650, y=260)
        self.back.place(x=515, y=410)

    def decryption(self):
        bufferSize = 64 * 1024
        pY.decryptFile(self.file.get(), "Archer.decrypted.data.file", self.password.get(), bufferSize)

    def openFile(self):
        File = filedialog.askopenfilename(title="Select a file", initialdir="C:/Users/smithOneDrive/Desktop", filetypes=(('txt', "*.txt"), ("csv", "*.csv"), ("all files", "*.*")))
        return self.file.insert(0, File)


if __name__ == '__main__':
    archer = Archer()
    archer.mainloop()
