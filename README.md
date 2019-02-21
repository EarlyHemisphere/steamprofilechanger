# steamprofilechanger
A python script that uses requests and ValvePython to change a user's profile picture to a random picture from the internet at given time intervals.

### Setup
As long as the script has an "images" folder in the same directory that consists of a "test.jpg" that can be any image you want, it'll work. It overwrites the test.jpg each time.

After running the following imports:

    pip install gevent
    pip install urllib
    pip install beautifulsoup4
    pip install -u steam

the script can be run successfully if their steam username and password is known. 2FA is also taken care of by ValvePython.

### Process
At each specified interval in time, the script:

1) Picks a random word in the English language
2) Picks a random number between 1 and 5
3) Uses the word as a search query in google images
4) Downloads the nth search result, where n is the random number between 1 and 5
5) Uploads it to Steam using the FileUploader

### Note
There are better ways to accomplish this/the code can be improved.

### Small bug
Currently, there are two known issues brought by ValvePython.
 1. Script will crash without error at a get_web_session_cookies() or urlopen() request. Suspect max recursion depth reached.
 2. Running the script multiple times could cause it to be unable to upload images. Tried to combat this by adding client.logout() and client.disconnect() on KeyboardInterrupt.

Issues are to be looked into in the future.
