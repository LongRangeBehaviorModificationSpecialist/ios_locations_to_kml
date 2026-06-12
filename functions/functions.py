# !/usr/bin/env python3

from datetime import datetime
from rich.console import Console
import pandas as pd
from pathlib import Path
import sqlite3
import sys
import webbrowser

from rich.prompt import Confirm


c = Console()


class HelperFunctions:

    def query_database(
            source: Path,
            query: str) -> str:
        """Query the Cache.sqlite database file.

        Args:
            Path: path to the database to be queried
            query: query to run against the database

        Returns: Pandas dataframe from the database query.
        """
        # Connect to the database
        conn = sqlite3.connect(source)

        # Define your SQL query
        sql_query = query

        # Execute the query and load results into a DataFrame
        df = pd.read_sql_query(sql_query, conn)

        # Close the database connection
        conn.close()

        # Return the dataframe
        return df


    def get_destf_name(
            dest: Path,
            destf: str,
            time: str) -> str:
        """Add date/time and proper file extension to output file name."""
        output_kml_file = Path(f"{dest}\\{time}_{destf}.kml")
        return output_kml_file


    def get_csv_file_name(
            dest: Path,
            destf: str,
            time: str) -> str:
        """Get the file path to save the csv file, if selected."""
        output_csv_file = Path(f"{dest}\\{time}_{destf}.csv")
        return output_csv_file


    def convert_db_timestamp(
            timestamp: int) -> str:
        """Converts a Cocoa Core Data timestamp to local time.

        Args:
            timestamp: A Cocoa Core Data timestamp, which is the number of
            seconds since midnight, January 1, 2001, GMT.

        Returns:
            A datetime object representing the local time equivalent of the
            given Cocoa Core Data timestamp.
        """
        # Convert the Cocoa Core Data timestamp to a Unix timestamp
        unix_timestamp = timestamp + 978307200

        # Convert seconds since Unix epoch to datetime object
        dt_object = datetime.fromtimestamp(unix_timestamp)

        # Format datetime object to "%m-%d-%Y %H:%M:%S" format
        formatted_dt = dt_object.strftime("%a, %d-%b-%Y at %H:%M:%S")

        return formatted_dt


    def write_kml_closing() -> str:
        kml_closing_text = """
        </Folder>
    </Document>
    </kml>"""
        return kml_closing_text


    def end_program(
            number_of_rows: int,
            start_time: str,
            end_time: str,
            output_csv_file: str,
            count: int,
            output_kml_file: str,
            total_time: str,
            query_command_string: str,) -> None:
        """Function used to display overall information about the records that
        were parsed from the database and the location of the output files
        within the file path.
        """

        c.print("\n[light_goldenrod1]===== RESULTS =====")

        # Display the time frame between which the records were obtained
        c.print(f"""[grey66]
[-] Processed [italic][dodger_blue1]{count:,}[/italic] [grey66]records from \
the database...

[-] Query command:
    [italic][dodger_blue1]{query_command_string}[/italic]

    [grey66]Beginning Date/Time Input (Local Time)  : [italic][dodger_blue1] \
{HelperFunctions.convert_db_timestamp(start_time)}[/italic]
    [grey66]End Date/Time Input (Local Time)        : [italic][dodger_blue1] \
{HelperFunctions.convert_db_timestamp(end_time)}[/italic]""")

        try:
            if output_csv_file:
                # Print verification that the .csv file was created
                c.print(f"[grey66]\n[-] The .csv file was created successfully \
and is saved as:\n\t[italic][dodger_blue1]{Path(output_csv_file).name}[/italic]")
            else:
                pass
        except UnboundLocalError:
            pass

        # Show the name of the output .kml file (including appended date/time)
        c.print(f"\n[grey66][-] The .kml file was created with [italic]\
[dodger_blue1]{count:,}[/italic] [grey66]records and is saved as:\n\
\t[italic][dodger_blue1]{Path(output_kml_file).name}[/italic]")

        # Show directory where the output .kml file is saved
        c.print(f"[grey66][-] The output file(s) are saved in the [italic]\
[dodger_blue1]{Path(output_kml_file).parent}[/italic] [grey66]directory")
        # Print the output to the screen
        c.print(f"[grey66][-] Program completed in [italic][dodger_blue1]\
{total_time:.4f}[/italic] [grey66]seconds")


    def ask_open_output_kml_file(kml_file: Path) -> None:
        """Asks the user if they want to open the .kml file in Google Earth.

        If the user answers "y", then the .kml file is opened and this
        program is closed.

        If the user answers "n", then the this program is closed and no
        additional is taken.
        """
        open_choice = Confirm.ask("""[light_goldenrod1][-] Do you want to \
open the .kml file now?""")
        if open_choice == True:
            c.print("[dodger_blue1] Opening the .kml file with Google Earth \
and then exiting...")
            webbrowser.open(kml_file)
        else:
            c.print(f"\n[light_goldenrod1][-] Very good then. Exiting now...")
            # Exit the program
            sys.exit(0)
