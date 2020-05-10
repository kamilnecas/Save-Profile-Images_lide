# Save-Profile-Images_lide
Script process the website "https://www.lide.cz/" which is basically dating website.
* Every user has profile with an option to upload images (photos) on his/her profile.
* Script is supposed to save those images at once.

The profile of each user works as dynamic website. If profile contains more than certain amount of images, the "Load more" button appears.
To reveal more images, button needs to be clicked. Button disappears once all images are loaded.

To avoid saving already stored images, script checks images at current working directory.

Script uses Selenium to web scrape all necessary information. Browser is always executed in headless mode.
* To be able to execute the script, the Firefox browser driver needs to be stored in this location "c:\Firefox_GeckoDriver_Win64\geckodriver.exe".
* Of course, it can be omitted, if it is already set in your PATH of your system.
