# ========================
# (c) 2018 law offices of reed yurchak
# contact mark.phillips@gmail.com for any questions 206-607-9415
# ========================

import datetime as dt
import calendar
import pandas as pd
import dateutil
import datetime

print pd.__version__

def next_weekday(d, weekday=0):
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0: # Target day already happened this week
        days_ahead += 7
    return d + datetime.timedelta(days_ahead-7)

# Opening the king county dataset
dataset = open("king.csv","r").read().split("\n")[1:][:-1]

# Just for bad entries stats
noint = 0
bad = 0

data = []

# Parsing the dataset to get the city and weekdate for each accident
for line in dataset[:-1]:
	line = line.split(",")
	city = line[2]
	if len(city) == 0:
		bad += 1
		continue
	date = line[14]
	if len(date) == 0:
		bad += 1
		continue
	dum = date.split("/")
	if len(dum[0]) == 1: date = "0"+date
	dum = date.split("/")

	if len(dum[1]) == 1: date = dum[0]+"/0"+dum[1]+"/"+dum[2]
	# We want to get the monday of that week, and not the actual date, so we can ARIMA by week (since by day would be less precise)
	date = dt.datetime.strptime(date,"%m/%d/%Y")
	weekdate = next_weekday(date)

	data.append([city, weekdate, calendar.day_name[date.weekday()]])


cities = set(zip(*data)[0])
min_date = min(zip(*data)[1])
max_date = max(zip(*data)[1])

delta = max_date - min_date

dates = []

for i in range(int(delta.days/7)+1):
    dates.append(min_date + datetime.timedelta(7*i))

df = pd.DataFrame(index=dates, columns=cities).fillna(0)
df.index.name = "Date"
for entry in data:
	df.set_value(str(entry[1]),entry[0],df[entry[0]][entry[1]]+1)

df.to_csv("weekly_table.csv")

# Now we want the weekday table. This table will have coefficients based on historical data per weekday. The ARIMA forecast will account for the whole week, and to get the prediction for a day the ARIMA number will be multiplied for the coefficient for that weekday for that city.

weekdays_name = set(zip(*data)[2])


df = pd.DataFrame(index=weekdays_name, columns=cities).fillna(0.)
df.index.name = "Weekday"
for entry in data:
	df.set_value(str(entry[2]),entry[0],float(df[entry[0]][entry[2]]+1))

for column in cities:
	total = df[column].sum()
	for row in weekdays_name:
		df.set_value(row, column, float(df[column][row])/total)

df.to_csv("weekday_coeffs.csv")

