# steamprofilechanger
A python script that uses requests to change a user's profile picture to a random picture from the internet at given time intervals.

### Setup
As long as the script has an "images" folder in the same directory that consists of a "test.jpg" that can be any image you want, it'll work. It overwrites the test.jpg each time.

A `sId`, `sessionid`, `steamLogin`, and `steamLoginSecure` need to be filled in so Steam can authenticate you.
 - `sId` is just your SteamID64.
 - `sessionid`, `steamLogin`, and `steamLoginSecure` can all be obtained by going to Chrome Settings -> Content Settings -> Cookies -> See All Cookies and Site Data -> steamcommunity.

### Process
At each specified interval in time, the script:

1) Picks a random word in the English language
2) Picks a random number between 1 and 5
3) Uses the word as a search query in google images
4) Downloads the nth search result, where n is the random number between 1 and 5
5) Uploads it to Steam using the FileUploader

### Note
There are better ways to accomplish this/the code can be improved. I just starting using it once I got it working.
