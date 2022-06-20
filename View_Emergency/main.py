import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.storage.jsonstore import JsonStore
from functools import partial
# connecting to firebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred_obj = firebase_admin.credentials.Certificate('secret_key.json')
default_app = firebase_admin.initialize_app(cred_obj, {
    'databaseURL':  "https://medical-emergency-62d60-default-rtdb.firebaseio.com/"
})

# local storage
store = JsonStore('storage.json')
phone_no = "0"


class daily(GridLayout):  # in case the phone number has already been set up
    def __init__(self, **kwargs):
        super(daily, self).__init__(**kwargs)
        ref = db.reference("/")
        data = ref.get()
        fields = []
        idx = 0
        for a in data.keys():
            fields.append(a)

        def delete(idx, a):
            ref = db.reference("/" + str(fields[idx]))
            print(ref)
            ref.set({})

        self.cols = 1

        for entry in data:
            if entry == 'Apex':
                    continue
            values = list(data[entry].values())
            my_entry_obj = OneEntry(
                values[0], values[1], values[2], values[3])
            self.inside = GridLayout()
            self.inside.cols = 2
            self.inside.add_widget(
                Label(text="Name of the affected person: "))
            self.inside.add_widget(Label(text=my_entry_obj.victim))
            self.inside.add_widget(Label(text="Name of the reporter: "))
            self.inside.add_widget(Label(text=my_entry_obj.reporter))
            self.inside.add_widget(
                Label(text="Phone number of the reporter: "))
            self.inside.add_widget(
                Label(text=my_entry_obj.phone_no_reporter))
            self.inside.add_widget(Label(text="Message: "))
            self.inside.add_widget(Label(text=my_entry_obj.msg))
            self.add_widget(self.inside)
            self.inside2 = FloatLayout()
            self.flag_btn = Button(text="Case Handled",
                                    on_press=partial(delete, idx),
                                    size_hint=(.2, .4),
                                    pos_hint={'x': .4, 'y': .5},
                                    background_color='green',
                                    color='white')
            self.inside2.add_widget(self.flag_btn)
            self.add_widget(self.inside2)
            idx = idx + 1


class OneEntry(daily):
    def __init__(self, victim, reporter, phone_no_reporter, msg):
        self.victim = victim
        self.reporter = reporter
        self.phone_no_reporter = phone_no_reporter
        self.msg = msg

        # permissions ko goli maar di


class login(GridLayout):  # in case the app is first time being opened and the phone number of the user has not been set up
    def __init__(self, **kwargs):
        super(login, self).__init__(**kwargs)
        self.cols = 1
        self.inside = GridLayout()
        self.inside.cols = 2
        self.inside.add_widget(Label(text="Name: "))
        self.name = TextInput()
        self.inside.add_widget(self.name)
        self.inside.add_widget(Label(text="Phone Number: "))
        self.phone = TextInput()
        self.inside.add_widget(self.phone)
        self.inside.add_widget(Label(text="Email: "))
        self.email = TextInput()
        self.inside.add_widget(self.email)
        self.add_widget(self.inside)
        self.submit = Button(
            text="If AM READY TO BE RESPONSIBLE!", on_press=self.finish,
            font_size="20sp",
            background_color=(1, 1, 1, 1),
            color=(1, 1, 1, 1),
            size=(32, 32),
            size_hint=(.2, .2),
            pos=(300, 250))
        self.add_widget(self.submit)

    def finish(self, instance):
        App.get_running_app().stop()
        store.put('phone_no', value=str(self.phone.text))
        store.put('name', value=str(self.name.text))
        store.put('email', value=str(self.email.text))
        ref = db.reference('/Apex/')
        ref.push(
            {"Name": store.get('name')['value'],
             "Phone_Number": store.get('phone_no')['value'],
             "Email": store.get('email')['value'],
             }


        )
        MyApp().run()


class MyApp(App):
    def build(self):
        if (store.exists('phone_no')):
            return daily()
        else:
            return login()


MyApp().run()
