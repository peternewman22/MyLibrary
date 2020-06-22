from decouple import config
import csv
from datetime import datetime
import logging
from Gui import Gui
import PySimpleGUI as sg

# logging.basicConfig(filename = 'mylibrary.log', filemode = 'w', level=logging.DEBUG, format='%(asctime)s - %(message)s')

class MyLibrary:
    def __init__(self, debugOn):
        self.debugMode = debugOn
        self.filename = sg.popup_get_file('Choose a document to save to')
        self.apiKey = config('KEY')
        self.metadata = ["ISBN", "title", "subtitle", "authors", "edition", "pageCount", "categories", "averageRating", "ratingsCount", "publishedDate", "publisher", "description"]

    def constructRow(self, data):
        """Constructs row in the order of metadat"""
        return list(map(lambda datapoint: data[datapoint], self.metadata))

    def write2csv(self, row):
        """Writes to csv"""
        with open(self.filename, 'a', newline='') as csv_file:
            writer=csv.writer(csv_file, delimiter=',')
            writer.writerow(row)

    def run(self):
        while True:
            gui = Gui(self.apiKey, self.metadata)
            row = self.constructRow(gui.data)
            self.write2csv(row)