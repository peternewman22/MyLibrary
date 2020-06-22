# MyLibrary
A small project to practice interaction with APIs: searching and categorising books in my personal library using the Google Books API.
After some experimentation, I decided to use a GUI and categorise books as I go. If the google books search fails (some ISBN's don't return results), then the information can be entered manually as this doesn't happen to often.
Saves results to csv but could be integrated with a database.
At the moment, uses keyboard interrupt to stop the program. I'm still working on how best to use a GUI.

## Target metadata
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
* Detect if the same book has been scanned twice
* Add persistent GUI window behind: close program (?)
* Pretty up interface
* Implement [efficiency measures](https://developers.google.com/books/docs/v1/performance): partial query
* Implement [efficiency measures](https://developers.google.com/books/docs/v1/performance): compressed query

## Current Bugs
* Fix issue where each window doesn't automatically focus itself
* Fix issue where the ISBN isn't saved where api requests are successful

## Abandoned Approaches
* Adding additional search parameters (still wasn't bringing up the target books)

## Stretch Goals
* Synchronise with Google Books account (?)
* Show book data including thumbnail etc with GUI
* Interact with Goodreads account (?)
* Data analysis dashboard
* Visualise data

## Reflection
* Requests makes life lovely and simple
