# runwayMagHeading
This Python script utilizes [Geomag 7.0] to add magnetic headings to the open-source runway data [open data].
### Files
runway_data/runways.csv: Original file from open data, downloaded on April 2016.
runway_data/runways_with_true_heading.csv: Converted runway file with 2016 magnetic variation data.

### Usage
On Windows, run main.py and an output file will be generated at runway_data/runways_with_true_heading.csv

14th and 21st columns in the .csv are the magnetic headings, with values between 0.0 and 360.0.

Magnetic variation changes over time. The year is set to 2016 in the follwing line in main.py:
```
year = '2016'
```

The year can be changed and its can be:
- decimal (2017, 2019.8855)
- YYYY,MM,DD (2018,4,7)

### License
This application is dedicated to public domain.


   [Geomag 7.0]: <http://www.ngdc.noaa.gov/IAGA/vmod/igrf.html>
   [open data]: <http://ourairports.com/data/>