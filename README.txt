bomWind.py
=================

Summary
----
Simple function that takes an Australian place name as input and returns
the most recent 72hrs of wind speed and gust data from the Australian
Bureau of Meteorology.

You could automate it to run every few days and commit to a database,
building up the entire wind speed database over time.

The full dataset is available but behind a paywall.

Note:
* I haven't checked all the timezones or if daylight savings would have
  an impact
* To find the right input values, search the BOM website and get it from
  the URL:
  - "http://www.bom.gov.au/places/{state}/{place}/observations/{station}/"


Inputs
----
* state: string code for Australian state, eg. 'nsw'
* place: string name of place, eg. 'sydney'
* station: string name of weather station, eg. 'sydney---observatory-hill'

Returns
----
* dataframe of the wind speed data, in km/h and m/s
* string relevant timeZone

