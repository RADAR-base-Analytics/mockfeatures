# mock-features
Mock Features pipeline

A example pipeline ilustrative of loading RADAR-data and generating some simple features from this.

# mock-features
Mock Features pipeline

# Description
This Mock pipeline downloads the data from the [mockdata](https://github.com/RADAR-base-Analytics/mockdata) repository and saves it as a submodule. mockfeatures pipeline uses this mock data to calculate mock features for illustrative purposes.

## Data
The data is stored as .csv.gz. format, which the I/O module reads and convert into a Spark DataFrame for further processing.

## Features
### PhoneBatteryChargingDuration

The duration of the phone battery charging every day by each user
### StepCountPerDay

The number of steps per day taken by each user.

## Mock Output

The output is 2 csv files`phone_battery_charging_duration.csv` and `step_count_per_day.csv`. 

[![DOI](https://zenodo.org/badge/523666760.svg)](https://zenodo.org/badge/latestdoi/523666760)

