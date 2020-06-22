import PySimpleGUI as sg
import requests
from decouple import config
from collections import defaultdict

class Gui:
    """Handles gathering isbn and, if necessary, additional searches""" 
    def __init__(self, apiKey, metadata, debugOn):
        self.apiKey = apiKey
        self.debugOn = debugOn
        self.window = sg.Window('Scan a book!',layout= self.createMainLayout(), finalize=True) # Still not making the window active ??
        self.metadata = metadata
        self.data = self.getData() # having the first window read here kept the window inactive when called
        self.window.close()
        
    def createMainLayout(self):
        return [
            [sg.Text('ISBN: '), sg.InputText(key='isbn',focus=True)],
            [sg.Frame('Additional Search',visible=False,layout=self.createManualEntryLayout(),key='SEARCHFRAME')],
            [sg.Button("Search",key='SEARCH', visible=True),sg.Button('Submit', key='SUBMIT',visible=False),sg.Cancel(),sg.Quit()]
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
        query = requests.get(f'https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}&key={self.apiKey}') # mnke the query
        if query.status_code == 200: # Checking for successful query
            return query.json() # Return
        else:
            print("Problem with query") # for debugging
            return {}

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
            
            if event == "Quit": # pass Quit up to MyLibrary (there's got to be a better way of doing this)
                d['Quit'] = True
                print("Ending program")
                return d


            if event in (None, "Cancel"):
                print("Let's start over shall we...")
                return d
            
            elif event == 'SEARCH':
                print("searching...")
                r = self.queryAPI(values['isbn'])
                

                if r['totalItems'] == 1:
                    print("Found exactly 1 match!")
                    data = r['items'][0]['volumeInfo']
                    print(f"Data: {data}")
                    for datapoint in self.metadata: # Iterate through metadata and extract as relevant
                        d[datapoint] = self.extract(datapoint, data)
                    d['isbn'] = values['isbn'] # Set the isbn from the scanned value (stored elsewhere in data)
                    print("Submitting the following data:")
                    [print(f"{k} : {v}") for k,v in d.items()]
                    print("\n")
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
                print("\n")
                return d