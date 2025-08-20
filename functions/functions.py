# !/usr/bin/env python3

from datetime import datetime
from rich.console import Console
import pandas as pd
from pathlib import Path
import sqlite3
import sys
import webbrowser


c = Console()


class HelperFunctions:

    def query_database(
            source: Path,
            query: str) -> str:
        """Query the Cache.sqlite database file.

        Returns: Pandas dataframe from the database query.
        """

        # Connect to the database.
        conn = sqlite3.connect(source)
        # Define your SQL query.
        sql_query = query
        # Execute the query and load results into a DataFrame.
        df = pd.read_sql_query(sql_query, conn)
        # Close the database connection.
        conn.close()
        # Return the dataframe.
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


    def convert_db_timestamp(timestamp: int) -> str:
        """Converts a Cocoa Core Data timestamp to local time.
        Args:
            timestamp: A Cocoa Core Data timestamp, which is the number of
            seconds since midnight, January 1, 2001, GMT.
        Returns:
            A datetime object representing the local time equivalent of the
            given Cocoa Core Data timestamp.
        """
        # Convert the Cocoa Core Data timestamp to a Unix timestamp.
        unix_timestamp = timestamp + 978307200
        # Convert seconds since Unix epoch to datetime object
        dt_object = datetime.fromtimestamp(unix_timestamp)
        # Format datetime object to "%m-%d-%Y %H:%M:%S" format
        formatted_dt = dt_object.strftime("%a, %m-%d-%Y at %H:%M:%S %p")
        return formatted_dt


    def write_kml_closing() -> str:
        kml_closing_text = """
        </Folder>
    </Document>
    </kml>"""
        return kml_closing_text


    def end_program(
        number_of_rows: int,
        begin_time: str,
        end_time: str,
        output_csv_file: str,
        count: int,
        output_kml_file: str,
        total_time: str,
        query_command_string: str,) -> None:

        c.print("\n  [light_goldenrod1]===== RESULTS =====")

        # Display the time frame between which the database records were obtained.
        c.print(f"""[grey66]
  [-] Processed [dodger_blue1]{count:,} [grey66]records from the database\n
  [-] Query Data\n
      Query command :
      [dodger_blue1]{query_command_string}\n
      [grey66]Beginning Date/Time Input : [dodger_blue1]\
{HelperFunctions.convert_db_timestamp(begin_time)}
      [grey66]End Date/Time Input       : [dodger_blue1]\
{HelperFunctions.convert_db_timestamp(end_time)}""")

        try:
            if output_csv_file:
                # Print verification that the .csv file was created.
                c.print(f"""[grey66]
  [-] The .csv file was created successfully. The file is saved as :
      [dodger_blue1]{Path(output_csv_file).name}""")
            else:
                pass
        except UnboundLocalError:
            pass

        # Show the name of the output .kml file (including appended date/time).
        c.print(f"""[grey66]
  [-] The .kml file was created with [dodger_blue1]{count:,} \
[grey66]data points. The .kml file is saved as :
      [dodger_blue1]{Path(output_kml_file).name}""")

        # Show directory where the output .kml file is saved.
        c.print(f"""[grey66]
  [-] The results file(s) are saved in the following directory :
      [dodger_blue1]{Path(output_kml_file).parent}\\""")

        # Print the output to the screen.
        c.print(f"""[grey66]
  Program completed in [dodger_blue1]{total_time:.4f} [grey66]seconds""")


    def ask_open_output_kml_file(kml_file: Path) -> None:
        closing = """  [light_goldenrod1]>>> Exiting program..."""

        # Ask user if they want to open the output file.
        open_choice = c.input("""[light_goldenrod1]
  [-] Do you want to open the .kml file now? \[y/n] >> """)

        # If the user enters "y", the .kml file will be opened in Google Earth.
        if open_choice.lower().strip() == "y":

            # Open the output file in Google Earth.
            c.print("""[dodger_blue1]
  Opening the .kml file with Google Earth...""")
            webbrowser.open(kml_file)

            # Print closing message on the screen.
            c.print(f"\n{closing}")

        # If the user enteres anything other than "y" the program will close.
        else:
            # Print closing message on the screen.
            c.print(f"\n{closing}")

            # Exit the program.
            sys.exit(0)