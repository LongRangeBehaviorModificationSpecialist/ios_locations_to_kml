# !/usr/bin/env python3

import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from vars.timezones import US_TIME_ZONES
from functions.get_options import GetOptions
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from rich.console import Console
from rich.traceback import install
from rich.panel import Panel


__author__ = "@mikes"
__dlu__ = "11-Jun-2026"
__version__ = "1.2.1"


# Create the console object
c = Console()
install()


def print_help() -> None:
    # A standard docstring-style help menu
    help_text = f"""
Usage: python .\make_kml_prompted.py ["-h", "--help"]

An interactive tool to process location database caches.

Options:
    -h, --help    Show this help message and exit.

Author:
    {__author__}

Version:
    {__version__}

Last Updated:
    {__dlu__}

Arguments:
    None

Database Options:
    1 = Cache.sqlite (Location History)
    2 = cache_encryptedB.db (WiFi locations)
    3 = cache_encryptedB.db (LTE locations)
    4 = Cloud-V2.sqlite (Significant Locations)
    5 = Local.sqlite (Significant Location Visits) or
    6 = Local.sqlite (Vehicle Locations)

Date/Time Entries:
    Must be entered using the following format: "YYYY-MM-DD HHMMSS"
    Do not use quotes around the input values

Timezone Option:
    Valid options are:
        ["ET","EST","EDT"] = "America/New_York",
        ["CT","CST","CDT"] = "America/Chicago",
        ["MT","MST","MDT"] = "America/Denver",
        ["AZ"]             = "America/Phoenix" (no DST),
        ["PT","PST","PDT"] = "America/Los_Angeles",
        ["AKT"]            = "America/Anchorage",
        ["HT","HST"]       = "Pacific/Honolulu",
        ["UTC","GMT"]      = UTC timezone
"""
    c.print(f"[yellow]{help_text}")
    # Exit cleanly
    sys.exit(0)


def convert_input_time_to_apple_time(
        date_string: str,
        input_tz_name: str) -> float:
    """Converts the time string to Apple Absolute Time based on the
    user-defined timezone.

    Args:
        date_string: Formatted as 'YYYY-MM-DD HHMMSS'
        input_tz_name: IANA timesone string (e.g., 'America/New_York', 'UTC')
    """
    try:
        date_format = "%Y-%m-%d %H%M%S"
        # Parse the date_string into a native datetime
        native_dt = datetime.strptime(date_string, date_format)
        # Interpret the input datetime as Eastern Time
        input_dt = native_dt.replace(tzinfo=ZoneInfo(input_tz_name))
        # Convert input datetime to UTC
        utc_dt = input_dt.astimezone(timezone.utc)
        # Define Apple Epoch
        apple_epoch = datetime(2001, 1, 1, tzinfo=timezone.utc)
        # Calculate the difference in seconds between the input datetime and
        # the Apple Epoch time
        absolute_time = (utc_dt - apple_epoch).total_seconds()

        return absolute_time

    except ZoneInfoNotFoundError:
        return f"Error: '{input_tz_name}' is not a valid IANA timezone."
    except ValueError as e:
        return f"Error: Please check the date format. {e}"


def get_options():
    """Get the required options to pass to the make_kml() function."""

    # Display a script header panel
    c.print("")
    c.print(
        Panel.fit(
            "[bold cyan]Make .kml from database file[/bold cyan]\n"
            "[dim]Please answer the following questions to configure the application.[/dim]",
            border_style="cyan"
        )
    )

    # Ask questions to get the variables to pass to the make_kml_prompted() function
    # Using rich to display the final arguments beautifully
    source     = GetOptions.get_source_path()
    dest       = GetOptions.get_dest_path()
    destf      = GetOptions.get_destf_name()
    csv        = GetOptions.get_csv_option()
    db         = GetOptions.get_db_option()
    start_time = GetOptions.get_start_time()
    end_time   = GetOptions.get_end_time()
    tz         = GetOptions.get_tz_options()

    make_kml(
        source=source,
        dest=dest,
        destf=destf,
        csv=csv,
        db=db,
        start_time=start_time,
        end_time=end_time,
        tz=tz
    )


def make_kml(
        source: Path,
        dest: Path,
        destf: str,
        csv: str,
        db: int,
        start_time: str,
        end_time: str,
        tz: str) -> None:

    python_file = str(Path(__file__).name)

    tz_code = tz.upper()
    iana_name = US_TIME_ZONES.get(tz_code)

    # Convert the input time strings to Apple Absolute Time
    # Handle the string -> Apple time conversion just one time, rather than
    # have seperate functions in each .py file
    start_time = convert_input_time_to_apple_time(start_time, iana_name)
    end_time = convert_input_time_to_apple_time(end_time, iana_name)


    # Get local time when the script begins
    t = time.localtime()

    # Print the local time when the script began
    c.print(f"""[grey66]
=================================

Program started : [dodger_blue1]\
{time.strftime("%d-%b-%Y at %H:%M:%S", t)} ET

[grey66]=================================""")

    # Format the local time to append to the beginning of the output file name
    file_time = time.strftime("%Y-%m-%d_%H%M%S", t)

    if db == 1:
        from cache_sqlite_to_kml import (
            write_cache_sqlite_to_kml
        )
        write_cache_sqlite_to_kml(
            python_file=python_file,
            source=source,
            dest=dest,
            destf=destf,
            make_csv=csv,
            start_time=start_time,
            end_time=end_time,
            file_time=file_time
        )

    elif db == 2:
        from cache_encb_db_wifi_to_kml import (
            write_cache_encb_db_wifi_to_kml
        )
        write_cache_encb_db_wifi_to_kml(
            python_file=python_file,
            source=source,
            dest=dest,
            destf=destf,
            make_csv=csv,
            start_time=start_time,
            end_time=end_time,
            file_time=file_time
        )

    elif db == 3:
        from cache_encb_db_lte_to_kml import (
            write_cache_encb_db_lte_to_kml
        )
        write_cache_encb_db_lte_to_kml(
            python_file=python_file,
            source=source,
            dest=dest,
            destf=destf,
            make_csv=csv,
            start_time=start_time,
            end_time=end_time,
            file_time=file_time
        )

    elif db == 4:
        from cloud_v2_sqlite_signif_loc_to_kml import (
            write_cache_v2_signif_loc_to_kml
        )
        write_cache_v2_signif_loc_to_kml(
            ppython_file=python_file,
            source=source,
            dest=dest,
            destf=destf,
            make_csv=csv,
            start_time=start_time,
            end_time=end_time,
            file_time=file_time
        )

    elif db == 5:
        from local_sqlite_signif_loc_visits_to_kml import (
            write_local_sqlite_signif_visits_to_kml
        )
        write_local_sqlite_signif_visits_to_kml(
            python_file=python_file,
            source=source,
            dest=dest,
            destf=destf,
            make_csv=csv,
            start_time=start_time,
            end_time=end_time,
            file_time=file_time
        )

    elif db == 6:
        from local_sqlite_vehicle_loc_to_kml import (
            write_local_sqlite_vehicle_loc_to_kml
        )
        write_local_sqlite_vehicle_loc_to_kml(
            python_file=python_file,
            source=source,
            dest=dest,
            destf=destf,
            make_csv=csv,
            start_time=start_time,
            end_time=end_time,
            file_time=file_time
        )


if __name__ == "__main__":

    if len(sys.argv) > 1 and sys.argv[1] in ["-h", "--help"]:
        print_help()
    else:
        get_options()
