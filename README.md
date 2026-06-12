## Introduction

- This main script take data from various databases present in the iOS file system and pulls the location data and formats the data into .kml files.

#### Syntax

---

`python .\make_kml.py --source [SOURCE] --dest [DESTINATION] --destf [DESTINATION_FILENAME] --csv {y,n} --db [DATABASE_OPTION] --starttime [START_TIME] --endtime [END_TIME] --tz [TIMEZONE]`

#### Script Help

---

- Create a .kml file by reading the location records from the database specified by the user.

- The `--source` argument is the file path to the database file.

- The `--dest` argument is the directory in which you would like the results file(s) written.

  - Enclose the `--source` and `--dest` file paths in double quotes.

- Do not add a file extension to the file name provided in the `--destf` argument. It will automatically be added by the script (e.g. `--destf "location_results"` will be saved as `location_results.kml`).

- For the `--csv` argument, add `y` or `n` to indicate whether you would like a .csv file created containing the data returned from the query.

- For the `--db` argument, use the corresponding number for the database you want to examine:

  - `1` = **Cache.sqlite** (Location History),
  - `2` = **cache_encryptedB.db** (WiFi locations),
  - `3` = **cache_encryptedB.db** (LTE locations),
  - `4` = **Cloud-V2.sqlite** (Significant Locations),
  - `5` = **Local.sqlite** (Significant Location Visits), or
  - `6` = **Local.sqlite** (Vehicle Locations)

- The `--starttime` and `--endtime` values can be given as a string. Enter the time using `YYYY-MM-DD HHMMSS` format (e.g., `"2026-02-02 130000"`). Enter the hours using 24-hour format.

- For the `--tz` argument, use the values listed below to indicate the time zone of the `--starttime` and `--endtime` values. Use double quotes around the values (e.g., `--tz "ET"`):

  - `ET` = America/New_York
  - `CT` = America/Chicago
  - `MT` = America/Denver
  - `AZ` = America/Phoenix
  - `PT` = America/Los_Angeles
  - `AKT` = America/Anchorage
  - `HT` = Pacific/Honolulu
  - `UTC` = UTC Time Zone (+00:00)

#### To Do

---

- Add error handling for all functions.
