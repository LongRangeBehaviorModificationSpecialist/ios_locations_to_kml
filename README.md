## Introduction

- This main script take data from various databases present in the iOS file system and pulls the location data and formats the data into .kml files.
- The user will have the option to save the parsed data into a .csv file by using the `--csv y` option.

#### Syntax

---

`python .\create_kml_from_data.py --source [SOURCE] --dest [DESTINATION] --destf [DESTINATION_FILENAME] --csv {y,n} --db [DATABASE_OPTION] --starttime [START_TIME] --endtime [END_TIME]`

#### Script Help

---

- Create a .kml file by reading the location records from the database specified by the user.

- Enclose the `--source` and `--dest` file paths using double quotes.

- The `--starttime` and `--endtime` values can be given as a string. Enter the time as America/New_York timezone using `YYYY-MM-DD HHMMSS` format (e.g., "2026-02-02 130000"). Enter the hours using 24-hour format.

- For the `--db` argument, use the corresponding number for the database you want to examine:

  - 1 = **Cache.sqlite** (Location History),
  - 2 = **cache_encryptedB.db** (WiFi locations),
  - 3 = **cache_encryptedB.db** (LTE locations),
  - 4 = **Cloud-V2.sqlite** (Significant Locations),
  - 5 = **Local.sqlite** (Significant Location Visits), or
  - 6 = **Local.sqlite** (Vehicle Locations)


#### To Do

---

- Add error handling for all functions.
