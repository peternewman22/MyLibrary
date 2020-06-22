# MyLibrary
* A small project to practice interaction with APIs: searching and categorising books in my personal library using the Google Books API.
* After some experimentation, I decided to use a GUI and categorise books as I go. If the google books search fails (some ISBN's don't return results), then the information can be entered manually as this doesn't happen to often.
* Saves results to csv but could be integrated with a database.
* At the moment, uses keyboard interrupt to stop the program. I'm still working on how best to use a GUI.
* I've been using a barcode scanner to scan in the isbn from the barcode on the back of books

## Structure
**main** creates instance of **MyLibrary** class that calls **MyLibrary.run()** to
* collect data using a **Gui** object until data contains *Quit* = *True*
* append rows to the target file using **MyLibrary.write2csv()**

### Target metadata
* Title
* Subtitle
* Pagecount
* Edition
* Category
* Average Review
* Review Count
* Publisher
* Publish date

## TODO / Progress / Targets
* ~~Create API credentials~~
* ~~Restrict API credentials~~
* ~~Store apikeys in environment variables~~
* ~~Successfully create test request~~
* ~~Successfully extract data~~
* ~~Write function to extract data~~
* ~~Handle Missing Data~~
* ~~Improve transparency with logging~~
* ~~Handle listed data eg: 'authors' and 'categories'~~
* ~~General refactoring~~
* ~~GUI design~~
* ~~Choose output file from GUI~~
* ~~Test for bad query / server response~~
* ~~End program from GUI instead of using a keyboard interrupt~~
* Handle bad query
* Detect if the same book has been scanned twice
* Add persistent GUI window behind: close program (?)
* Pretty up interface
* Implement [efficiency measures](https://developers.google.com/books/docs/v1/performance): partial query
* Implement [efficiency measures](https://developers.google.com/books/docs/v1/performance): compressed query

## Current Bugs / Frustrations
* Issue where each window doesn't automatically focus itself - after investigating, it seems like a persistent windows problem. Will try in linux and see if it persists.
* ~~Can't encode u2032 when writing to csv~~ (explicitly set csv writer to use utf8 encoding)
* ~~Fix issue where the ISBN isn't saved where api requests are successful~~ (isbn was stored elsewhere in the response)

## Abandoned Approaches
* Adding additional search parameters (still wasn't bringing up the target books)

## Stretch Goals
* Synchronise with Google Books account (?)
* Show book data including thumbnail etc with GUI
* Interact with Goodreads account (?)
* Data analysis dashboard / visualise data

## Reflection
* Requests makes life lovely and simple
* Need to look into design patterns: there HAS to be a better way of passing variables up the class tree (?)
