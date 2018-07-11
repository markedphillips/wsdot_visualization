# ========================
# (c) 2018 law offices of reed yurchak
# contact mark.phillips@gmail.com for any questions 206-607-9415
# ========================

import pandas as pd
import datetime as dt


# This will read the alteryx output which is a forecast per week and multiply each of the previously computed probability coiefficients per weekday by the forecast of that week. This will yield the forecast for a particular day.


week_coeffs = pd.read_csv("weekday_coeffs.csv")
head = ["Date"]+list(week_coeffs.dtypes.index[1:])
cities = head[1:]

# To get the latest real time we will read the latest stored date


last_date = pd.read_csv("weekly_table.csv")["Date"]
last_date = dt.datetime.strptime(last_date[128],"%Y-%m-%d")

# Now we create 16 weeks of forward dates

dates = []
weekdays = []

for i in range(16*7):
	last_date += dt.timedelta(days= 1)
	dates.append(last_date)
	weekdays.append(last_date.weekday())

print weekdays
print len(dates)


result = pd.DataFrame(columns = head)

i = 0

for w in range(16):
	for d in range(7):
		date = str(dates[7*w+d])
		weekday = weekdays[7*w+d]

		row = [date]
		for city in cities:
			fore = pd.read_csv("partial_fore/"+city+"_forecast.csv")[city][w]
			coeff = week_coeffs[city][weekday]
			row.append(fore*coeff)
		# print result
		result.loc[i] = row
		i += 1

result.to_csv("full_forecast.csv", index = False)

