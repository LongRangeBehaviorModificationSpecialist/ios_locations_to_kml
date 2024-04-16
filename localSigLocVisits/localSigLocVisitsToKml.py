# !/usr/bin/env python3

from rich.console import Console
import time

from functions.functions import HelperFunctions as hf
from localSigLocVisits.localSigLocVisitsVars import(
    localSigLocVisitSqlQuery,
    localSigLocVisitKmlFileHeader,
    localSigLocVisitKmlFileBody)

c = Console()

def localSigLocVisitToKml(
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
    LOCAL_SIG_LOC_VISIT_QUERY = localSigLocVisitSqlQuery(
        begin_time=begin_time,
        end_time=end_time
    )

    # Query the database file.
    df = hf.query_database(
        source=source,
        query=LOCAL_SIG_LOC_VISIT_QUERY
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
        kml_header = localSigLocVisitKmlFileHeader()
        f.write(kml_header)

        # Initialize a counter variable to keep track of number of records.
        count = 0

        # Set variables from the dataframe.
        for index, row in df.iterrows():
            record = row['Record']
            data_point_count = row['Data Point Count']
            location_of_interest_id = row['Location Of Interest ID']
            creation_date_utc = row['Creation Date (UTC)']
            entry_date_utc = row['Entry Date (UTC)']
            exit_date_utc = row['Exit Date (UTC)']
            expiration_date_utc = row['Expiration Date (UTC)']
            latitude = row['Latitude']
            longitude = row['Longitude']
            location_horiz_uncertainty = row['LocationHorizontalUncertainty']
            location_confidence = row['LocationConfidence']
            data_source = row['Data Source']

            # Print message to screen with each record number added.
            c.print(f'[grey66]Processing Row #: [dodger_blue1]{record:,}')

            # Write the data from each record to the output .kml file.
            kml_body = localSigLocVisitKmlFileBody(
                record=record,
                data_point_count=data_point_count,
                location_of_interest_id=location_of_interest_id,
                creation_date_utc=creation_date_utc,
                entry_date_utc=entry_date_utc,
                exit_date_utc=exit_date_utc,
                expiration_date_utc=expiration_date_utc,
                latitude=latitude,
                longitude=longitude,
                location_horiz_uncertainty=location_horiz_uncertainty,
                location_confidence=location_confidence,
                data_source=data_source
            )
            f.write(kml_body)

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
