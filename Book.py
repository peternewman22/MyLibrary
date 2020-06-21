import requests
from decouple import config


class Book:
    """Each book collects its own data, either from Google Books API and returns a row to write to csv"""
    def __init__(self, isbn):
        self.isbn = isbn
        self.row = None
        self.payload = {'key':config('KEY')}
        self.data = self.query()
        self.success = False

    def query(self):
        """ Makes the request """
        try: 
            r = requests.get(f'https://www.googleapis.com/books/v1/volumes?q=isbn:{self.isbn}', params=self.payload).json()
        except Exception as e:
            print(f'Trouble with request: \t{e}')
        
        if r['totalItems'] == 0:
            pass # do something

        elif r['totalItems' == 1]:
            self.success = True

    def getData(self,**argv):

        
        
