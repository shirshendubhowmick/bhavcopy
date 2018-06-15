# BhavCopy

## Get the daily Bhav of stocks straight from Bombay Stock Exchange


This is simple Python application powered by CherryPy and Redis

The frontend is written in Vanilla CSS & JavaScript

* extract.py

    This file needs to be run manually to extract data from BSE website and loading it into Redis.
    It will always fetch last day's data, if you are running this file on Sunday & Monday it will extract data for last Friday.

    For the sake of simplicity trading holidays are ignored.

* app.py

    This is main backend file it will star the Cherrypy server, it is responsible for serving all HTML, CSS & JavaScript files and also data from Redis.


By default, the web app displays top 10 stocks entry from Redis, one can also search for a stock using the search box. For the sake of simplicity, the complete stock name needs to be entered in the search box. For example, searching with "ICICI" will not give any result, however one can search with "ICICI BANK" to get the desired result.


The web app is also mobile device friendly.