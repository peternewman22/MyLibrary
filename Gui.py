import PySimpleGUI as sg
from Book import Book
import requests
from decouple import config

# class Gui:
#     """Handles gathering isbn and, if necessary, additional searches""" 
#     def __init__(self):
#         self.window = sg.Window('Scan a book',layout= self.generateLayout)
#         self.data = 
    
#     def generateLayout(self):
#         return [
#             [sg.Text('ISBN:'),sg.InputText(key='ISBN',enable_events=True)]
#         ]
    
#     def loop(self):
#         while True:
#             event, values = window.Read(timeout = 1000)

# titleSearchLayout = [
#     [sg.Text('Title: '), sg.InputText(key='title')],
#     [sg.Text('Author: '), sg.InputText(key='author')],
#     [sg.Listbox([],key='SELECTION',enable_events=True)]
#     ]

# layout = [
#     [sg.Text('ISBN: '), sg.InputText(key='ISBN')],
#     [sg.Frame('Additional Search',visible=False,layout=titleSearchLayout,key='SEARCHFRAME')],
#     [sg.Button("Search",disabled=True,key='SEARCH'),sg.Cancel()]
# ]

# window = sg.Window('Enter ISBN',layout)
# apiKey = config('KEY')
# isbnSuccess = True


# while True:
#     event, values = window.Read(timeout=1000)
#     print(f"event: {event}, values: {values}")
#     if event in (None, "Cancel"):
#         print("Quitting...")
#         break
#     # turning on and off submit
#     if values['ISBN'] != '':
#         window['SEARCH'].update(disabled=False)
#     else:
#         window['SEARCH'].update(disabled=True)

#     if event == 'SEARCH' and isbnSuccess:
#         # print(f"isbn: {values['ISBN']}")
#         r = getData(values['ISBN'])
#         if r['totalItems'] == 1:
#             print(r)
#             break
#         elif r['totalItems'] == 0:
#             isbnSuccess = False
#             window['SEARCHFRAME'].update(visible=True)
#             print("No volumes found... Try again...")
    
#     if event == 'SEARCH' and not isbnSuccess:
#         r = getData(values['ISBN'])
            

# window.close()
# apiKey = config('KEY')
# def getData(isbn, **payload):
#     # return requests.get(f"https://www.googleapis.com/books/v1/volumes?q=isbn+{isbn}&key:{apiKey}",params=payload)
#     return requests.get(f"https://www.googleapis.com/books/v1/volumes?q=isbn+{isbn}&key:{apiKey}")

# r = getData(isbn='9780140265019',intitle='Oscar Wilde',inauthor='Richard Ellman')
# print(r.url)

apiKey = config('KEY')
isbn = "9780140265019"
title = "Oscar+Wilde"
author = "Richard+Ellmann"
r = requests.get(f"https://www.googleapis.com/books/v1/volumes?q=isbn+{isbn}&intitle:{title}&inauthor:{author}&key:{apiKey}")
print(r.json()['totalItems'])
