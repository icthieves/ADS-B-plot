# ADS-B-plot
A simple script for plotting the flight path of aircraft from ADS-B packet data

## Demonstration
![Screenshot of Plot](http://i.imgur.com/cTYEhHb.png "One day's worth of Aircraft")

[Demo](https://www.youtube.com/watch?v=sP1jinxQsgs&feature=youtu.be)


## Usage:
I'm using Tedsluis's modified Dump1090:

https://github.com/tedsluis/dump1090

And i'm also using his socket30003 perl scripts, which clean up the data a bit:

 https://github.com/icthieves/dump1090.socket30003

#### Basic workflow:

* start dump1090

* capture data to a file (Option 1: use socket3003.pl) remember to edit socket30003.cfg to change the save location!

> ./socket30003.pl

* capture the data to a file (Option 2: loses no data, but much noisier)

> sudo wget -O - -q http://localhost:30003 >> /path/to/file.csv

_Note: this command safely appends to a file (>>), you can run it multiple times and it will pick up where it left off._

* collect a day or two's worth of data

* If using Option 2, then run socket3003.pl from Tedluis' perl scripts and point it at your CSV instead. (Note: my pull request that adds this feature has not yet been merged, [but my fork of Ted's scripts is available here](https://github.com/icthieves/dump1090.socket30003)) Don't forget to edit socket30003.cfg!

* After running socket30003.pl (either directly or on a CSV), You'll have a file named something like **dump1090-127_0_0_2-170627** in the directory set in socket30003.cfg

* now, you can point ADS-B-Plot at **dump1090-127_0_0_2-170627** with:

> ./adsbplot -f /path/to/dump1090-127_0_0_2-170627.txt

*The file extension doesn't matter. It's still a CSV*




## Dependencies:
MatPlotLib

NumPy

SciPy
