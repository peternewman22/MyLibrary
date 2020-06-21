import pandas as pd
from decouple import config
import requests
import csv
from collections import defaultdict
from datetime import datetime
import logging

apiKey = config('KEY')
apiUser = config('USER')

logging.basicConfig(filename = 'mylibrary.log', filemode = 'w', level=logging.DEBUG, format='%(asctime)s - %(message)s')






def main():
    getDeets("9781316618165")
    # try:
    #     # load in dataframe
    #     df = pd.read_clipboard(header=0)
        
    #     # write timestamp
    #     write2csv("MyLibrary.csv",[f"Session Start: {datetime.now()}"])
        
    #     # write heading row
    #     headingRow = ["ISBN", "title", "subtitle", "authors", "edition", "pageCount", "categories", "averageRating", "ratingsCount", "publishedDate", "publisher", "description"]
    #     write2csv("MyLibrary.csv", headingRow)
        
    #     # fill in the data from the dataframe
    #     for eachISBN in df['ISBN'].to_list():
    #         info = getDeets(eachISBN)
    #         write2csv("MyLibrary.csv", info)
    
    # except Exception as e:
    #     print(f"Problem loading the initial df: \n{e}")


def getDeets(isbn):
    row = defaultdict(lambda: "Missing Data") # will never throw an error
    row['ISBN'] = isbn
    
    # send the request
    payload = {'key' : apiKey}
    data = requests.get(f'https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}', params=payload)
    
    # process request
    try:
        jsonData = data.json()
        logging.debug(f"Success! \n{jsonData}")
    except Exception as e:
        print(f"Trouble with the request: \n{e}")
        logging.error(data.text)
        return [row['ISBN'], row['title'], row['subtitle'],row['edition'], row['authors'], row['pageCount'], row['categories'], row['averageRating'], row['ratingsCount'],row['publishedDate'], row['publisher'], row['description']]
    
    # process request
    try:
        info = jsonData['items'][0]['volumeInfo']
    except Exception as e:
        info = {}
        print(f"Trouble retrieving data:\n{e}")
    
    # Extracting the info
    metadata = ['title', 'subtitle', 'authors', 'edition', 'pageCount', 'categories', 'averageRating','ratingsCount','publishedDate','publisher','description']
    try:
        for data in metadata:
            row[data] = extract(data, info) # Go through the metadata list and extract the info
    except Exception as e:
        print(f"Problem with extracting info: \n{e}" )
        
    # for debugging purposes, print all the things    
    for k, v in row.items():
        print(f"{k} : {v}")
    print("\n")
    
    # now print to csv
    try:
        row2write = [row['ISBN'], 
                    row['title'], 
                    row['subtitle'],
                    row['edition'], 
                    row['authors'], 
                    row['pageCount'], 
                    row['categories'], 
                    row['averageRating'], 
                    row['ratingsCount'],
                    row['publishedDate'], 
                    row['publisher'], 
                    row['description']]
        return row2write
    except Exception as e:
        print(f"Problem with writing to file: \n{e}" )

def write2csv(fileName, row):
    with open(fileName, "a", newline='') as csvFile:
        writer = csv.writer(csvFile, delimiter=',')
        writer.writerow(row)

def extract(target, data):
    if target in data:
        contents = data[target]
        if type(contents) == list:
            return ", ".join(contents)
        else:
            return contents
    else :
        return "Missing Data"

if __name__ == "__main__":
    main()