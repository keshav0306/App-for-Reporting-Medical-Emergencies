import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.storage.jsonstore import JsonStore
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from plyer import call
import yagmail
from functools import partial

store = JsonStore('storage.json')

phone_no = "0"


class login(GridLayout):  # in case the app is first time being opened and the phone number of the user has not been set up
    def __init__(self, **kwargs):
        super(login, self).__init__(**kwargs)
        self.cols = 2
        self.add_widget(Label(text="Phone Number: "))
        self.phone = TextInput()
        self.add_widget(self.phone)
        self.submit = Button(text="I AM READY!", on_press=self.finish)
        self.add_widget(self.submit)

    def finish(self, instance):
        App.get_running_app().stop()
        store.put('phone_no', value=str(self.phone.text))
        MyApp().run()


class daily(GridLayout):  # in case the phone number has already been set up
    cred = credentials.Certificate('secret_key.json')
# Initialize the app with a service account, granting admin privileges
    firebase_admin.initialize_app(cred, {
        'databaseURL': "https://medical-emergency-62d60-default-rtdb.firebaseio.com/"
    })

    def __init__(self, **kwargs):
        super(daily, self).__init__(**kwargs)
        self.cols = 1
        self.inside = GridLayout()
        self.inside.cols = 2
        self.inside.add_widget(
            Label(text="Name of the affected: ", font_size=20))
        self.name_aff = TextInput()
        self.inside.add_widget(self.name_aff)
        self.inside.add_widget(
            Label(text="Name of the reporter: ", font_size=20))
        self.name_rep = TextInput()
        self.inside.add_widget(self.name_rep)
        self.inside.add_widget(
            Label(text="Enter some message (Optional)", font_size=20))
        self.message = TextInput()
        self.inside.add_widget(self.message)
        self.add_widget(self.inside)
        self.inside2 = FloatLayout()
        self.submit = Button(text="SUBMIT",
                             on_press=self.pressed,
                             size_hint=(.2, .4),
                             pos_hint={'x': .4, 'y': .5},
                             background_color='red',
                             color='white',
                             font_size=20,)
        self.inside2.add_widget(self.submit)
        self.add_widget(self.inside2)
        # self.submit = Button(text="SUBMIT", on_press=self.pressed)
        # self.add_widget(self.submit)

    def pressed(self, instance):
        store.put('flag', value=1)
        ref = db.reference('/')
        ref.push(
            {"Name_of_affected": str(self.name_aff.text),
             "Name_of_reporter": str(self.name_rep.text),
             "Phone_Number": store.get('phone_no')['value'],
             "Message": str(self.message.text),
             }
        )
        print(self.submit.text)
        self.submit.text="Please wait while we send alert to all the Apex members!"
        print(self.submit.text)
        self.name_aff.text = ""
        self.name_rep.text = ""
        self.message.text = ""
        yag = yagmail.SMTP("iamkeshav06@gmail.com",
                           "accokommdznorgsp")
        ref = db.reference('/Apex')
        data = ref.get()
        for entry in data:
            for i in range(0, 3):
                yag.send(data[entry]['Email'],
                         "Emergency",
                         "An emergency has been reported by ")
        App.get_running_app().stop()
        MyApp().run()


class Apex(GridLayout):  # in case the app is first time being opened and the phone number of the user has not been set up
    def __init__(self, **kwargs):
        super(Apex, self).__init__(**kwargs)
        self.cols = 2

        def calling(phn_num, arg):
            call.makecall(phn_num)
        ref = db.reference('/Apex')
        data = ref.get()
        for entry in data:
            self.add_widget(Label(text=data[entry]['Name']))
            self.btn = Button(text="CALL ME", on_press=partial(
                calling, data[entry]['Phone_Number']))
            self.add_widget(self.btn)
        store.delete('flag')


class MyApp(App):

    def build(self):
        if store.exists('flag'):
            return Apex()
        if (store.exists('phone_no')):
            return daily()
        else:
            return login()


MyApp().run()