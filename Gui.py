import PySimpleGUI as sg
import requests
from decouple import config
from collections import defaultdict

class Gui:
    """Handles gathering isbn and, if necessary, additional searches""" 
    def __init__(self, apiKey, metadata, debugOn):
        self.apiKey = apiKey
        self.debugOn = debugOn
        self.window = sg.Window('Scan a book!',layout= self.createMainLayout(), use_default_focus=False) # focus changed to specify the isbn input
        self.window.BringToFront() # make sure this is set to focus
        self.metadata = metadata
        self.data = self.getData()
        self.window.close()
        
    def createMainLayout(self):
        return [
            [sg.Text('ISBN: '), sg.InputText(key='isbn', focus=True)],
            [sg.Frame('Additional Search',visible=False,layout=self.createManualEntryLayout(),key='SEARCHFRAME')],
            [sg.Button("Search",key='SEARCH', visible=True),sg.Button('Submit', key='SUBMIT',visible=False),sg.Cancel()]
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
            [sg.Text('Ratings Count: '), sg.InputText(key='ratingsCount')],
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
            if self.debugOn:
                print(f"event: {event}, values: {values}")
            
            if event in (None, "Cancel"):
                print("Quitting...")
                return d
                
            
            elif event == 'SEARCH':
                print("searching...")
                r = self.queryAPI(values['isbn'])
                d['isbn'] = values['isbn'] # Add the isbn into the return data

                if r['totalItems'] == 1:
                    print("Found exactly 1 match!")
                    data = r['items'][0]['volumeInfo']
                    for datapoint in self.metadata:
                        d[datapoint] = self.extract(datapoint, data)
                    print("Submitting the following data:")
                    [print(f"{k} : {v}") for k,v in d.items()]
                    return d

                else:
                    "Print found no matches or multiple matches..."
                    self.window['SEARCHFRAME'].update(visible=True)
                    self.window['SEARCH'].update(visible=False) # Hide Search (can't search twice)
                    self.window['SUBMIT'].update(visible=True) # Show submit
                    print("No volumes found. Enter data manually.")

            elif event == 'SUBMIT': # no validation as yet - any missing data will be filled in
                for k, v in values.items():
                    if v != '':
                        d[k] = v # grab the values that have been filled in
                print("Submitting the following data:")
                [print(f"{k} : {v}") for k,v in d.items()]
                return d