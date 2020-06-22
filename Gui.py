import PySimpleGUI as sg
from Book import Book
import requests
from decouple import config
from collections import defaultdict

class Gui:
    """Handles gathering isbn and, if necessary, additional searches""" 
    def __init__(self, apiKey, metadata):
        self.apiKey = apiKey
        self.window = sg.Window('Scan a book!',layout= self.createMainLayout())
        self.metadata = metadata
        self.data = self.getData()
        self.window.close()
        
    def createMainLayout(self):
        return [
            [sg.Text('ISBN: '), sg.InputText(key='ISBN')],
            [sg.Frame('Additional Search',visible=False,layout=self.createManualEntryLayout,key='SEARCHFRAME')],
            [sg.Button("Search",key='SEARCH', visible=True),sg.Button(key='SUBMIT',visible=False),sg.Cancel()]
        ]
    
    def createManualEntryLayout(self):
        return [
            [sg.Text('Title: '), sg.InputText(key='title')],
            [sg.Text('Subtitle: '), sg.InputText(key='subtitle')],
            [sg.Text('Edition: '), sg.InputText(key='edition')],
            [sg.Text('Page count: '), sg.InputText(key='pageCount')],
            [sg.Text('Authors: '), sg.InputText(key='authors')],
            [sg.Text('Categories: '), sg.InputText(key='categories')],
            [sg.Text('Average Rating: '), sg.InputText(key='averageRating')],
            [sg.Text('Ratings Count: '), sg.InputText('ratingsCount')],
            [sg.Text('Publisher: '), sg.InputText(key='publisher')],
            [sg.Text('Published Date: '), sg.InputText(key='publishedDate')],
            [sg.Text('Description: '), sg.InputText(key='description')]
        ]

    def queryAPI(self, isbn):
        """Queries google books api for isbn using apiKey"""
        return requests.get(f'https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}&key={self.apiKey}').json()

    def extract(self, target, data):
        """If list data, join together. Otherwise, check to see if it exists in the query data"""
        if target in data:
            contents = data[target]
            if type(contents) == list:
                return ", ".join(contents)
            else:
                return contents
        else :
            return "Missing Data"
  
    def getData(self):
        """Handles scanning of isbn. If no search results, prompts manual entry."""
        d = defaultdict(lambda: "Missing Data") # using a default dict will safeguard against errors down the line
        
        while True:
            event, values = self.window.Read(timeout = 1000) # poll the window each second
            print(f"event: {event}, values: {values}")
            
            if event in (None, "Cancel"):
                print("Quitting...")
                return d
                
            
            elif event == 'SEARCH':
                r = self.queryAPI(values['ISBN'])
                if r['totalItems'] == 0:
                    self.window['SEARCHFRAME'].update(visible=True)
                    self.window['SEARCH'].update(visible=False) # Hide Search (can't search twice)
                    self.window['SUBMIT'].update(visible=True) # Show submit
                    print("No volumes found. Enter data manually.")

                elif r['totalItems'] == 1:
                    data = r['items'][0]['volumeInfo']
                    for datapoint in self.metadata:
                        d[datapoint] = self.extract(datapoint, data)
                        print("Submitting the following data:")
                        [print(f"{k} : {v}") for k,v in d.items()]
                        return d

            elif event == 'SUBMIT': # no validation as yet - any missing data will be filled in
                for k, v in values.items():
                    if v != '':
                        d[k] = v # grab the values that have been filled in
                print("Submitting the following data:")
                [print(f"{k} : {v}") for k,v in d.items()]
                return d