
# !/usr/bin/env python3

from datetime import datetime
from pathlib import Path
import sys

from rich.console import Console
from rich.traceback import install
from rich.prompt import Prompt


c = Console()
install()


class GetOptions:
    """Class to handle the functions to get all of the options from the prompts
    that are presented to the user.
    """


    db_option_list = {
        1: "Cache.sqlite (Location History)",
        2: "cache_encryptedB.db (WiFi locations)",
        3: "cache_encryptedB.db (LTE locations)",
        4: "Cloud-V2.sqlite (Significant Locations)",
        5: "Local.sqlite (Significant Location Visits)",
        6: "Local.sqlite (Vehicle Locations)"
    }


    @staticmethod
    def get_source_path():
        """Get and return the source path of the database to analyze."""
        source = Path(Prompt.ask(
            "\n[-] Enter the file path to the database")
        )
        c.print(
            f"\[i] Path to database file: [italic][cyan]\
{source}[/italic]")
        existing_databases = {entry.split(' ', 1)[0] for entry in GetOptions.db_option_list.values()}
        if source.name in existing_databases:
            c.print(
                f"\n[green]    [-] Database file: {source.name} IS IN the \
approved file list. Continuing...")
            return source
        else:
            c.print(
                f"\n[red]    [!] Database file: {source.name} IS NOT IN the \
approved list. Please choose a different file...")
            sys.exit(1)


    @staticmethod
    def get_dest_path():
        """Get and return the destination path to save the results file(s)."""
        dest = Path(Prompt.ask(
            "\n[-] Enter the file path to where results will be saved"))
        c.print(
            f"\[i] Path to where results will be saved: [italic][cyan]\
{dest}[/italic]")
        return dest


    @staticmethod
    def get_destf_name():
        """Get and return the base file name for the results file(s)."""
        destf = Path(Prompt.ask(
            "\n[-] Enter the file name of the output .kml file"))
        c.print(
            f"\[i] The base name of the .kml file will be: [italic][cyan]\
{destf}[/italic]")
        return destf


    @staticmethod
    def get_csv_option():
        """Get and return the option to create a .csv file with the results."""
        responses = [
            "Yes, a .csv file will be created",
            "No, a .csv file will NOT be created",
            "[bold red][!] A valid option was not entered"
        ]
        csv = Prompt.ask(
            "\n[-] Create a .csv file with the results of the query? \[y/n]")
        if csv.lower().strip() == "y":
            c.print(
                f"\[i] Will a .csv file be created: [italic][cyan]\
{responses[0]}[/italic]")
            return csv
        elif csv.lower().strip() == "n":
            c.print(
                f"\[i] Will a .csv file be created: [italic][cyan]\
{responses[1]}[/italic]")
            return csv
        else:
            c.print(f"{responses[2]}")
            GetOptions.get_csv_option()


    @staticmethod
    def get_db_option():
        """Get and return the specific location option to examine."""
        db = Prompt.ask(
            "\n[-] Type of location data to examine (see help for options)")
        try:
            # Convert user input to an integer
            db = int(db)
            c.print(
                f"\[i] Type of location data to be examined: \
[italic][cyan]{db}[/italic]")
            return db
        except ValueError:
            # Handles where input cannot be converted to an integer
            c.print(
                "[red][!] Error: [italic]Invalid input. Please enter a valid \
number.[/italic]")
        except KeyError:
            # Handles where the number is an integer, but not in dictionary
            c.print(
                f"[red][!] Error: [italic]Number: {db} does not match any \
options in the database.[/italic]")


    @staticmethod
    def get_start_time():
        """Get and return the date/time of the first record to return
        from the query.
        """
        try:
            start_time = Prompt.ask(str(
                "\n[-] Enter the date/time of the [bold]first[/bold] record to \
be returned (use 'YYYY-MM-DD HHMMSS' format)"))
            datetime.strptime(start_time, "%Y-%m-%d %H%M%S")
            c.print(
                f"\[i] Date/Time of [bold]first[/bold] record to be returned: \
[i][cyan]{start_time}")
            return start_time
        except ValueError as e:
            c.print(f"[bold red][!] An error occured: {e}")
            GetOptions.get_start_time()


    @staticmethod
    def get_end_time():
        """Get and return the date/time of the last record to return
        from the query.
        """
        try:
            end_time = Prompt.ask(str(
                "\n[-] Enter the date/time of the [bold]last[/bold] record to \
be returned (use 'YYYY-MM-DD HHMMSS' format)"))
            if datetime.strptime(end_time, "%Y-%m-%d %H%M%S"):
                c.print(
                    f"\[i] Date/Time of [bold]last[/bold] record to be \
returned: [italic][cyan]{end_time}[/italic]")
                return end_time
            else:
                raise ValueError
        except ValueError as e:
            c.print(f"[bold red][!] An error occured: [italic{e}[/italic]")
            GetOptions.get_end_time()


    @staticmethod
    def get_tz_options():
        """Get and return the timezone of the start and end times input
        by the user.
        """
        tz = Prompt.ask(
            "\n[-] Enter the timezone used for the date/time values")
        c.print(
            f"\[i] Entered timezone is: [italic][cyan]{tz}[/italic]")
        return tz
