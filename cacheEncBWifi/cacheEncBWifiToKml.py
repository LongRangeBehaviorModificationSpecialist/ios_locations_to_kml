# !/usr/bin/env python3

from rich.console import Console
import time

from functions.functions import HelperFunctions as hf
from cacheEncBWifi.cacheEncBWifiVars import(
    cacheEncBWifiSqlQuery,
    cacheEncBWifiKmlFileHeader,
    cacheEncBWifiKmlFileBody)


# EXAMPLE SYNTAX:

# python .\create_kml_from_data.py --source "C:\Users\mikes\Desktop\temp\dbs\cache_encryptedB.db" --dest "C:\Users\mikes\Desktop\temp\results" --destf "cache_encryptedB_Wifi_locations" --csv y --database 2 --btime 723993933 --etime 724000738

c = Console()


def cacheEncBWifiToKml(
        source: str,
        dest: str,
        destf: str,
        make_csv: str,
        begin_time: int,
        end_time: int,
        file_time: str) -> None:

    # Get the time the program began to execute.
    start_time = time.perf_counter()

    # Generate the SQL query to include the begin_time and end_time values.
    CACHE_ENCRYPTEDB_WIFI_QUERY = cacheEncBWifiSqlQuery(
        begin_time=begin_time,
        end_time=end_time
    )

    # Query the database file.
    df = hf.query_database(
        source=source,
        query=CACHE_ENCRYPTEDB_WIFI_QUERY
    )

    # Get the total number of records in the worksheet.
    number_of_rows = len(df)

    # Print verification message to screen.
    c.print(f'\n[grey66]Found [dodger_blue1]{number_of_rows:,} \
[grey66]rows of data\n')

    # Set output file to the correct format.
    output_kml_file = hf.get_destf_name(
        dest=dest,
        destf=destf,
        time=file_time
    )

    # Open the output file using the context manager.
    with open(f'{output_kml_file}', 'w', encoding='utf-8') as f:

        # Write the header data of the output .kml file.
        cacheEncBWifiKmlHeader = cacheEncBWifiKmlFileHeader()
        f.write(cacheEncBWifiKmlHeader)

        # Initialize a counter variable to keep track of number of records.
        count = 0

        # Set variables from the dataframe.
        for index, row in df.iterrows():
            record = row['Record']
            mac_address = row['MAC Address']
            utc_time = row['Timestamp (UTC)']
            local_time = row['Timestamp (Local)']
            latitude = row['Latitude']
            longitude = row['Longitude']
            channel = row['Channel']
            horiz_accuracy = row['HorizontalAccuracy']
            altitude = row['Altitude']
            confidence = row['Confidence']
            data_source = row['Data Source']

            # Print message to screen with each record number added.
            c.print(f'[grey66]Processing Row #: [dodger_blue1]{record:,}')

            # Write the data from each record to the output .kml file.
            cacheEncBWifiKmlBody = cacheEncBWifiKmlFileBody(
                record=record,
                local_time=local_time,
                latitude=latitude,
                longitude=longitude,
                mac_address=mac_address,
                channel=channel,
                horiz_accuracy=horiz_accuracy,
                utc_time=utc_time,
                altitude=altitude,
                confidence=confidence,
                data_source=data_source
            )
            f.write(cacheEncBWifiKmlBody)

            # Increment the counter variable for the next record.
            count += 1

        # Write the closing data to the output .kml file.
        f.write(f'{hf.write_kml_closing()}')

    # If the user chose to make a .csv file containing the parsed records.
    if make_csv.lower() == 'y':
        output_csv_file = hf.get_csv_file_name(
            dest=dest,
            destf=destf,
            time=file_time
        )
        df.to_csv(
            output_csv_file,
            index=False
        )
    else:
        pass

    # Get the time the script completed.
    ending_time = time.perf_counter()
    # Get the total time the script took to complete.
    total_time = ending_time - start_time

    hf.end_program(
        number_of_rows=number_of_rows,
        begin_time=begin_time,
        end_time=end_time,
        output_csv_file=output_csv_file,
        count=count,
        output_kml_file=output_kml_file,
        total_time=total_time
    )

    # Ask user if they want to automatically open the output file.
    hf.ask_open_output_kml_file(kml_file=output_kml_file)

