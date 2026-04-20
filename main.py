# !/usr/bin/env python3

import argparse
from argparse import RawDescriptionHelpFormatter
import time
from datetime import datetime, timezone
from pathlib import Path
from rich.console import Console
from rich.traceback import install
from vars.timezones import US_TIME_ZONES
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


__author__ = "@mikespon"
__dlu__ = "20-Apr-2026"
__version__ = "1.2.1"

# Create the console object.
c = Console()
install()


def convert_input_time_to_apple_time(date_string: str,
        input_tz_name: int) -> int:
    """Converts the time string to Apple Absolute Time based on the user-defined
    timezone.

    Args:
        date_string: Formatted as 'YYYY-MM-DD HHMMSS'
        input_tz_name: IANA timesone string (e.g., 'America/New_York', 'UTC')
    """
    try:
        date_format = "%Y-%m-%d %H%M%S"
        # Parse the date_string into a native datetime
        native_dt = datetime.strptime(date_string, date_format)
        # Interpret the native datetime as Eastern Time
        eastern_dt = native_dt.replace(tzinfo=ZoneInfo(input_tz_name))
        # Convert Eastern datetime to UTC
        utc_dt = eastern_dt.astimezone(timezone.utc)
        # Define Apple Epoch
        apple_epoch = datetime(2001, 1, 1, tzinfo=timezone.utc)
        # Calculate the difference in seconds
        absolute_time = (utc_dt - apple_epoch).total_seconds()

        return absolute_time

    except ZoneInfoNotFoundError:
        return f"Error: '{input_tz_name}' is not a valid IANA timezone."
    except ValueError as e:
        return f"Error: Please check the date format. {e}"



def main() -> None:

    # Set up the argument parser syntax for the command line.
    parser = argparse.ArgumentParser(
        formatter_class=RawDescriptionHelpFormatter,
        prog="create_kml_from_data.py",
        usage="'%(prog)s --help' for more information",
        description=f"""
Description:
    create_kml_from_data.py version {__version__}

Author:
    {__author__}

Last Updated:
    {__dlu__}

Description:
    Create a .kml file by reading the location records from the database \
specified in the '--db' option.
    The '--starttime' and '--endtime' values can be given as a string using the \
following format: 'YYYY-MM-DD HHMMSS'.

URL:
    github.com/LongRangeBehaviorModificationSpecialist/ios_locations_to_kml

Examples:
    python .\create_kml_from_data.py --source [SOURCE] --dest [DESTINATION] \
--destf [DESTINATION_FILENAME] --csv [y,n] --db [DATABASE_CHOICE] --starttime \
[START_TIME] --endtime [END_TIME]

Notes:
    Enclose the full path in double quotes if it contains spaces.""")

    parser.add_argument(
        "--source",
        type=Path,
        required=True,
        help="[str] Directory where database file is located (include file \
name in path).")

    parser.add_argument(
        "--dest",
        type=Path,
        required=True,
        help="[str] Directory to save resulting .kml file.")

    parser.add_argument(
        "--destf",
        type=str,
        required=True,
        help="[str] File name of the resulting .kml file. The current date and \
time will be appended to the beginning of the file name with the following \
format: 'year-month-day_hhmmss'.")

    parser.add_argument(
        "--csv",
        type=str,
        choices=["y","n"],
        required=True,
        help="[str] Create a .csv file with the results of the query ('y' or \
'n').")

    parser.add_argument(
        "--db",
        type=int,
        choices=[1, 2, 3, 4, 5, 6],
        required=True,
        help="""[int] Type of location data you want to examine. Enter the \
corresponding number for the database/table containing the records you want \
to examine:
1=Cache.sqlite (Location History);
2=cache_encryptedB.db (WiFi locations);
3=cache_encryptedB.db (LTE locations);
4=Cloud-V2.sqlite (Significant Locations);
5=Local.sqlite (Significant Location Visits); or
6=Local.sqlite (Vehicle Locations).""")

    parser.add_argument(
        "--starttime",
        type=str,
        required=True,
        help="[str] Timestamp of the first record to return (enter the time as \
America/New_York timezone -- use 'YYYY-MM-DD HHMMSS' format).")

    parser.add_argument(
        "--endtime",
        type=str,
        required=True,
        help="[str] Timestamp of the last record to return (enter the time as \
America/New_York timezone -- use 'YYYY-MM-DD HHMMSS' format).")

    parser.add_argument(
        "--tz",
        type=str,
        required=True,
        default="UTC",
        help="[str] Timezone used for the `--starttime` and `--endtime` values.")

    args = parser.parse_args()
    argv = vars(args)

    source = argv["source"]
    dest = argv["dest"]
    destf = argv["destf"]
    make_csv = argv["csv"]
    db_type = argv["db"]
    start_time = argv["starttime"]
    end_time = argv["endtime"]
    tz = argv["tz"]

    tz_code = tz.upper()
    iana_name = US_TIME_ZONES.get(tz_code)


    # Convert the input time strings to Apple Absolute Time
    # Handle the string -> Apple time conversion just one time, rather
    # than have seperate functions in each .py file.
    start_time = convert_input_time_to_apple_time(start_time, iana_name)
    end_time = convert_input_time_to_apple_time(end_time, iana_name)


    # Get local time when the script begins.
    t = time.localtime()

    # Print the local time when the script began.
    c.print(f"""[grey66]
=================================

Program started : [dodger_blue1]\
{time.strftime("%d-%b-%Y at %H:%M:%S", t)} ET

[grey66]=================================""")

    # Format the local time to append to the beginning of the output file name.
    file_time = time.strftime("%Y-%m-%d_%H%M%S", t)


    if db_type == 1:

        from cache_sqlite_to_kml import write_cache_sqlite_to_kml

        write_cache_sqlite_to_kml(
            source=source,
            dest=dest,
            destf=destf,
            make_csv=make_csv,
            start_time=start_time,
            end_time=end_time,
            file_time=file_time)

    elif db_type == 2:

        from cache_encb_db_wifi_to_kml import write_cache_encb_db_wifi_to_kml

        write_cache_encb_db_wifi_to_kml(
            source=source,
            dest=dest,
            destf=destf,
            make_csv=make_csv,
            start_time=start_time,
            end_time=end_time,
            file_time=file_time)

    elif db_type == 3:

        from cache_encb_db_lte_to_kml import write_cache_encb_db_lte_to_kml

        write_cache_encb_db_lte_to_kml(
            source=source,
            dest=dest,
            destf=destf,
            make_csv=make_csv,
            start_time=start_time,
            end_time=end_time,
            file_time=file_time)

    elif db_type == 4:

        from cloud_v2_sqlite_signif_loc_to_kml import write_cache_v2_signif_loc_to_kml

        write_cache_v2_signif_loc_to_kml(
            source=source,
            dest=dest,
            destf=destf,
            make_csv=make_csv,
            start_time=start_time,
            end_time=end_time,
            file_time=file_time)

    elif db_type == 5:

        from local_sqlite_signif_loc_visits_to_kml import write_local_sqlite_signif_visits_to_kml

        write_local_sqlite_signif_visits_to_kml(
            source=source,
            dest=dest,
            destf=destf,
            make_csv=make_csv,
            start_time=start_time,
            end_time=end_time,
            file_time=file_time)

    elif db_type == 6:

        from local_sqlite_vehicle_loc_to_kml import write_local_sqlite_vehicle_loc_to_kml

        write_local_sqlite_vehicle_loc_to_kml(
            source=source,
            dest=dest,
            destf=destf,
            make_csv=make_csv,
            start_time=start_time,
            end_time=end_time,
            file_time=file_time)

    else:
        c.print("The code to examine the database you entered is not complete.")


if __name__ == "__main__":
    main()
