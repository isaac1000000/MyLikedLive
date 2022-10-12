Hello!
This is a bit of a side project to play around with gathering API data.
If you find it useful, would like to help out, or want to contact me for any reason, you can reach me at isaac.fisher@nyu.edu
Feel free to take this framework and improve it! Just let me know so I can see what cool things people are doing.
Cheers🥂

Working list of used libraries:
spotipy

Procedure for using this program:
Set local variables using these commands:
     export SPOTIPY_CLIENT_ID=(your spotipy client id)
     export SPOTIPY_CLIENT_SECRET=(your spotipy client secret)
     export TICKETMASTER_API_KEY=(your spotipy api key)
Choose your local market:
     In resources/dmaIDs.csv, find an appropriate local market
     Change the value in MyLikedLive/loc.txt to the number listed (default NYC)
These will set environment variables in your shell and allow you to run the program without hardcoding your keys
