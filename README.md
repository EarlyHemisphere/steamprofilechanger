# steamprofilechanger
A python script that uses requests and ValvePython to change a user's profile picture to a random picture from the internet at given time intervals.

### Setup
As long as the script has an "images" folder in the same directory that consists of a "test.jpg" that can be any image you want, it'll work. It overwrites the test.jpg each time.

After running the following imports:

    pip install urllib
    pip install beautifulsoup4

the script can be run successfully if your steam username and password is known. 2FA is also taken care of by ValvePython.

### Process
At each specified interval in time, the script:

1) Picks a random word in the English language
2) Picks a random number between 1 and 5
3) Uses the word as a search query in google images
4) Downloads the nth search result, where n is the random number between 1 and 5
5) Uploads it to Steam using the FileUploader
