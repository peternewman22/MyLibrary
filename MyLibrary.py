import pandas as pd
from decouple import config
import requests
import csv
from collections import defaultdict
from datetime import datetime

apiKey = config('KEY')
apiUser = config('USER')

def main():
    
    try:
        # load in dataframe
        df = pd.read_clipboard(header=0)
        
        # write timestamp
        write2csv("MyLibrary.csv",[f"Session Start: {datetime.now()}"])
        
        # write heading row
        headingRow = ["ISBN", "title", "subtitle", "authors", "edition", "pageCount", "categories", "averageRating", "ratingsCount", "publishedDate", "publisher", "description"]
        write2csv("MyLibary.csv", headingRow)
        
        # fill in the data from the dataframe
        for eachISBN in df['ISBN'].to_list():
            info = getDeets(eachISBN)
            write2csv("MyLibrary.csv", info)
    
    except Exception as e:
        print(f"Problem loading the initial df: \n{e}")


def getDeets(isbn):
    row = defaultdict(lambda: "Missing Data") # will never throw an error
    row['ISBN'] = isbn
    
    # query the info
    try:
        info = requests.get(f'https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}&key={apiKey}').json()['items'][0]['volumeInfo']
    except Exception as e:
        print("Trouble retrieving data:\n{e}")
    
    # Extracting the info
    try:
        row['title'] = extract('title', info)
        row['subtitle'] = extract('subtitle', info)
        row['authors'] = ", ".join(extract('authors', info))
        row['edition'] = extract('edition', info)
        row['pageCount'] = extract('pageCount', info)
        row['categories'] = ", ".join(extract('categories', info)) # returns string
        row['averageRating'] = extract('averageRating', info)
        row['ratingsCount'] =  extract('ratingsCount', info)
        row['publishedDate'] = extract('publishedDate',info)
        row['publisher'] = extract('publisher', info)
        row['description'] = extract('description', info) # in case description is missing
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
        return data[target]
    else :
        return "Missing Data"

if __name__ == "__main__":
    main()