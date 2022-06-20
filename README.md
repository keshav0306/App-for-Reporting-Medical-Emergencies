# App-for-Reporting-Medical-Emergencies

The project consists of 2 applications:

1) The reporting side : In case anyone spots or faces an emergency in the campus, they can use this app. Opening the app for the fist time will ask the person for their phone-number. After that they will be asked to fill in their name, and also an optional text message to be sent to the Apex body. This message can be used to tell the location of the person, and any other information related to the emergency. The user can finally submit and all the Apex members will be notified. After that the person will have the option to call any of the Apex members and the ambulance.

2) The Apex side : When any Apex (or any other concerned) member opens the app, they will be asked to fill in their name, phone number and their email-id.
When any emergency comes up, all the people who have registered in this app will be notified through a spam of emails. On being notified by this spam, the member will open the app, and will find the details regarding the emergenc(y|ies) including the name, the phone number and the text message from the person(s) facing the emergenc(y|ies). If the member thinks that the issue(s) is/are solved, he/she can remove the emergenc(y|ies) from the app.

The apps are cross-platform (will work on both ios and android). Here the desktop version of the apps are provided. Any person who wants to run these apps can directly run these in the terminal by writing '''python main.py''' in the respective folder.

The user has to first install these 4 modules : 

1) Kivy
2) Plyer
3) Yagmail
4) Firebase_admin

by '''pip install <module_name>'''
