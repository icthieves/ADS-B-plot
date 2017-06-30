import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate
import csv
from collections import defaultdict
import time
import datetime
import sys, argparse

#mpl.rcParams['legend.fontsize']=10


# parallel (i know, i know...) lists for each relevant column
alt = defaultdict(list)
lat = defaultdict(list)
lon = defaultdict(list)
timestamp = defaultdict(list)

FILENAME = ""

if __name__ == '__main__':
	parse = argparse.ArgumentParser()
	parse.add_argument('f')
	args = parse.parse_args()
	
	if args.f:
		FILENAME = args.f
	else:
		print("No input file specified.")
		sys.exit(1)

# open a file of ADS-B records and parse it
with open(FILENAME) as f:
	reader = csv.DictReader(f)
	# skip header
	next(reader, None)
	
	# read each aircraft Ident into 
	# its own set of altitude, latitude, and longitude lists.
	for row in reader:
		print(row['hex_ident'], row['altitude(meter)'], row['latitude'], row['longitude'], row['date'], row['time'])
		
		# convert the timestamp to Unix time
		t = time.mktime(datetime.datetime.strptime(row['date']+" "+row['time'],"%Y/%m/%d %H:%M:%S.%f").timetuple())

		# add the relevant columns to the list for this aircraft
		alt[row['hex_ident']].append(float(row['altitude(meter)']))
		lat[row['hex_ident']].append(float(row['latitude']))
		lon[row['hex_ident']].append(float(row['longitude']))
		timestamp[row['hex_ident']].append(t)



# interpolation sample points
num_sample_pts = 100

# maximum tolerated spatial change between any two packets
# Altitude delta maximum in meters
DELTA_THRESHOLD = 10000
# lat/lon maximum in degrees
LATLON_THRESHOLD = .12

# maximum time between ADB-S packets to consider, in seconds
TIME_THRESHOLD = 900

# create the plot
fig = plt.figure(1)
ax3d = fig.add_subplot(1, 1.5, 1, projection='3d')
#ax3d.set_zlim([-500, 15000])

# for each aircraft Ident
for key in alt:
	# check that there's at least 25 points to interpolate
	if len(alt[key]) < 25:
		continue
	
	# check that the dataset for this plane Ident isn't nonsensical
	
	# first, check that there isn't a huge gap between two ADB-S packets
	# this line finds the maximum difference between any two elements in a list
	max_time_delta = max(abs(x-y) for (x, y) in zip(timestamp[key][1:], timestamp[key][:-1]))
	if max_time_delta > TIME_THRESHOLD:
		print("[!] Ignoring flight "+key+": Delta in Timestamp too large ("+str(max_time_delta)+")")
		continue

	# it's very likely that the time delta will fail first, but if it doesn't, check spatial deltas as well
	max_delta_alt = max(abs(x-y) for (x, y) in zip(alt[key][1:], alt[key][:-1]))
	max_delta_lat = max(abs(x-y) for (x, y) in zip(lat[key][1:], lat[key][:-1]))
	max_delta_lon = max(abs(x-y) for (x, y) in zip(lon[key][1:], lon[key][:-1]))
	
	if max_delta_alt > DELTA_THRESHOLD:
		print("[!] Ignoring flight " +key+": Delta in Altitude too large ("+str(max_delta_alt)+")")
		continue

	if max_delta_lat > LATLON_THRESHOLD:
		print("[!] Ignoring flight " +key+": Delta in Latitude too large ("+str(max_delta_lat)+")")
		continue

	if max_delta_lon > LATLON_THRESHOLD:
		print("[!] Ignoring flight " +key+": Delta in Longitude too large ("+str(max_delta_lon)+")")
		continue

	# otherwise, the data for this aircraft is good enough to interpolate and plot

	# print the current aircraft
	print("[PLOT]: "+ key)
	
	# apply SciPy's magic interpolation
	tck, u = interpolate.splprep([lat[key], lon[key], alt[key]], s=2)
	#x_knots, y_knots, z_knots = interpolate.splev(tck[0], tck)

	u_fine = np.linspace(0, 1, num_sample_pts)
	x_fine, y_fine, z_fine = interpolate.splev(u_fine, tck)

		
	# build the curve

	#plot the raw data
	#ax3d.plot(x_knots, y_knots, z_knots, label=key)

	#plot the interpolated points
	ax3d.plot(x_fine, y_fine, z_fine, label=key)

# print out the Ident codes of each plotted aircraft
handles, labels = ax3d.get_legend_handles_labels()
plt.legend(handles, labels)

# draw the plot
plt.show()
