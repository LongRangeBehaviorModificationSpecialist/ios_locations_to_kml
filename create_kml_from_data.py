# !/usr/bin/env python3

import argparse
from argparse import RawDescriptionHelpFormatter
import time
from pathlib import Path
from rich.console import Console


__author__ = '@mikespon'
__dlu__ = '2024-04-15'

# Create the console object.
c = Console()


def main() -> None:

    # Set up the argument parser syntax for the command line.
    parser = argparse.ArgumentParser(
        formatter_class=RawDescriptionHelpFormatter,
        prog='create_kml_from_data.py',
        usage='%(prog)s [options]',
        description=f'''
    create_kml_from_data.py
    -----------------------\n
    [-] Create a .kml file by reading the location records from the database
        specified by the user.
    [-] The --begin_time/-bt and --end_time/-et values should be given in "Apple
        Absolute Time" (a/k/a) "Cocoa Core Data" format. To convert time values
        to/from the required input, see: https://www.gaijin.at/en/tools/time-converter.
    [-] For the "--database" argument, enter the corresponding number for the
        database you want to examine:\n
        1=Cache.sqlite (Location History),
        2=cache_encryptedB.db (WiFi locations),
        3=cache_encryptedB.db (LTE locations),
        4=Cloud-V2.sqlite (Significant Locations),
        5=Local.sqlite (Significant Location Visits), or
        6=Local.sqlite (Vehicle Locations)\n''',
        epilog=f'''  [-] DEVELOPED BY: {__author__} | LAST UPDATED: {__dlu__}'''
    )

    parser.add_argument(
        '--source',
        type=Path,
        required=True,
        help='*Path of database file to use as the basis of the query.'
    )

    parser.add_argument(
        '--dest',
        type=Path,
        required=True,
        help='*Path to save the resulting .kml file.'
    )

    parser.add_argument(
        '--destf',
        type=str,
        required=True,
        help='*Name to use for the created .kml file.'
    )

    parser.add_argument(
        '--csv',
        type=str,
        choices=['y','n'],
        required=True,
        help='*Create a .csv file to store the results of the query.'
    )

    parser.add_argument(
        '--database',
        type=int,
        choices=[1,2,3,4,5,6],
        required=True,
        help='*Number of the corresponding database file you want to examine.'
    )

    parser.add_argument(
        '--btime',
        type=int,
        required=True,
        help='*Timestamp of the first record to return.'
    )

    parser.add_argument(
        '--etime',
        type=int,
        required=True,
        help='*Timestamp of the last record to return.'
    )

    args = parser.parse_args()
    argv = vars(args)

    source = argv['source']
    dest = argv['dest']
    destf = argv['destf']
    make_csv = argv['csv']
    db_type = argv['database']
    begin_time = argv['btime']
    end_time = argv['etime']

    # Get local time to print to screen when program begins.
    t = time.localtime()
    c.print(f'''
[grey66]Program started: [dodger_blue1] {time.strftime("%m-%d-%Y at %H:%M:%S", t)}''')

    # Format the local time to append to the beginning of the output file name.
    file_time = time.strftime('%Y-%m-%d_%H%M%S', t)


    if db_type == 1:
        from cacheSqlite.cacheSqliteToKml import cacheSqliteToKml
        cacheSqliteToKml(
            source=source,
            dest=dest,
            destf=destf,
            make_csv=make_csv,
            begin_time=begin_time,
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
            begin_time=begin_time,
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
            begin_time=begin_time,
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
            begin_time=begin_time,
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
            begin_time=begin_time,
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
            begin_time=begin_time,
            end_time=end_time,
            file_time=file_time
        )

    else:
        c.print('The code to examine the database you entered is not complete.')


if __name__ == '__main__':
    main()
