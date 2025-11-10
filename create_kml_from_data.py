# !/usr/bin/env python3

import argparse
from argparse import RawDescriptionHelpFormatter
import time
from pathlib import Path
from rich.console import Console


__author__ = "@mikespon"
__dlu__ = "20-Aug-2025"
__version__ = "1.2"

# Create the console object.
c = Console()


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
    Michael Sponheimer (@mikespon)

Last Updated:
    {__dlu__}

Description:
    Create a .kml file by reading the location records from the database \
specified in the '--db' option.
    The '--starttime' and '--endtime' values should be given in Apple Absolute \
Time (a/k/a Cocoa Core Data) format.
    To convert time values to/from the required input, see: \
'https://www.gaijin.at/en/tools/time-converter'.

URL:
    github.com/LongRangeBehaviorModificationSpecialist/ios_locations_to_kml

Examples:
    python .\create_kml_from_data.py --source [SOURCE] --dest [DESTINATION] \
--destf [DESTINATION_FILENAME] --csv [y,n] --db [DATABASE_CHOICE] --starttime \
[START_TIME] --endtime [END_TIME]

Notes:
    Enclose the full path in double quotes if it contains spaces."""
)

    parser.add_argument(
        "--source",
        type=Path,
        required=True,
        help="[str] Directory where database file is located (include file \
name in path)."
    )

    parser.add_argument(
        "--dest",
        type=Path,
        required=True,
        help="[str] Directory to save resulting .kml file."
    )

    parser.add_argument(
        "--destf",
        type=str,
        required=True,
        help="[str] File name of the resulting .kml file. The current date and \
time will be appended to the beginning of the file name with the following \
format: 'year-month-day_hhmmss'."
    )

    parser.add_argument(
        "--csv",
        type=str,
        choices=["y","n"],
        required=True,
        help="[str] Create a .csv file with the results of the query ('y' or \
'n')."
    )

    parser.add_argument(
        "--db",
        type=int,
        choices=[1,2,3,4,5,6],
        required=True,
        help="""[int] Type of location data you want to examine. Enter the \
corresponding number for the database/table containing the records you want \
to examine:
1=Cache.sqlite (Location History);
2=cache_encryptedB.db (WiFi locations);
3=cache_encryptedB.db (LTE locations);
4=Cloud-V2.sqlite (Significant Locations);
5=Local.sqlite (Significant Location Visits); or
6=Local.sqlite (Vehicle Locations)."""
    )

    parser.add_argument(
        "--starttime",
        type=int,
        required=True,
        help="[int] Timestamp of the first record to return (in Cocoa Core \
Data format)."
    )

    parser.add_argument(
        "--endtime",
        type=int,
        required=True,
        help="[int] Timestamp of the last record to return (in Cocoa Core \
Data format)."
    )

    args = parser.parse_args()
    argv = vars(args)

    source = argv["source"]
    dest = argv["dest"]
    destf = argv["destf"]
    make_csv = argv["csv"]
    db_type = argv["db"]
    start_time = argv["starttime"]
    end_time = argv["endtime"]

    # Get local time when the script begins.
    t = time.localtime()

    # Print the local time when the script began.
    c.print(f"""[grey66]
  =================================
  Program started : [dodger_blue1] \
{time.strftime("%d-%b-%Y at %H:%M:%S", t)} ET
  [grey66]=================================""")

    # Format the local time to append to the beginning of the output file name.
    file_time = time.strftime("%Y-%m-%d_%H%M%S", t)


    if db_type == 1:
        from cacheSqlite.cacheSqliteToKml import cacheSqliteToKml
        cacheSqliteToKml(
            source=source,
            dest=dest,
            destf=destf,
            make_csv=make_csv,
            start_time=start_time,
            end_time=end_time,
            file_time=file_time
        )

    elif db_type == 2:
        from cacheEncBWifi.cacheEncBWifiToKml import cacheEncBWifiToKml
        cacheEncBWifiToKml(
            source=source,
            dest=dest,
            destf=destf,
            make_csv=make_csv,
            start_time=start_time,
            end_time=end_time,
            file_time=file_time
        )

    elif db_type == 3:
        from cacheEncBLte.cacheEncBLteToKml import cacheEncBLteToKml
        cacheEncBLteToKml(
            source=source,
            dest=dest,
            destf=destf,
            make_csv=make_csv,
            start_time=start_time,
            end_time=end_time,
            file_time=file_time
        )

    elif db_type == 4:
        from cloudV2SigLoc.cloudV2SigLocToKml import cacheV2SigLocToKml
        cacheV2SigLocToKml(
            source=source,
            dest=dest,
            destf=destf,
            make_csv=make_csv,
            start_time=start_time,
            end_time=end_time,
            file_time=file_time
        )

    elif db_type == 5:
        from localSigLocVisits.localSigLocVisitsToKml import localSigLocVisitToKml
        localSigLocVisitToKml(
            source=source,
            dest=dest,
            destf=destf,
            make_csv=make_csv,
            start_time=start_time,
            end_time=end_time,
            file_time=file_time
        )


    elif db_type == 6:
        from localVehicleLoc.localVehicleLocToKml import localVehicleLocToKml
        localVehicleLocToKml(
            source=source,
            dest=dest,
            destf=destf,
            make_csv=make_csv,
            start_time=start_time,
            end_time=end_time,
            file_time=file_time
        )

    else:
        c.print("The code to examine the database you entered is not complete.")


if __name__ == "__main__":
    main()


# python .\create_kml_from_data.py --source "C:\Users\mikes\Proton Drive\mikespon\My files\TEMP\Work_iPhone_XS_FFS\temp\Cache.sqlite" --dest "C:\Users\mikes\Desktop" --destf "test.kml" --csv y --db 1 --starttime 776779200 --endtime 776786400