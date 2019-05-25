# wsdot_visualization

Code to parse, filter and forecast the WSDOT dataset

The code consists of three scripts. 

The first one, “wsdot_parser.py”, will open the WSDOT dataset. Please note that the code assumes that the dataset will be on the same folder level and named “king.csv”. This script will generate two derived datasets: “weekday_coeffs.csv” and “weekly_table.csv”.

The first is a table where the general probability of an accident per city and weekday (monday-sunday) is represented by a number (0 to 1). The second one is the aggregate accidents per week over the full dataset grouped by city. Each row represents a week and it just counts the number of accidents that happened on that week at that city.

To do the actual forecast Alteryx Designed is required. The script provided (“arima_iter.yxmc”) will produce a forecast of accidents for the selected city (you must manually choose it in the Alteryx interface). This forecast is per week and each row represents a week for that city, and is the result of an ARIMA model fit to the whole dataset per city and week.

Once all the cities have a forecast then the Python script “merger.py” will produce the final forecast for the next 16 weeks starting on the last date found on the WSDOT dataset. The general forecast for a week is spread between the days of that week, weighting each day by the weekday coefficient previously computed. At the end the file “full_forecast.csv” is produced as the final output. This file can feed Tableau to create a visualization.

Please note that the forecasts ends on the 1st of October 2018. 
