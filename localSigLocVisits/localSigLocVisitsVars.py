# !/usr/bin/env python3

def localSigLocVisitSqlQuery(
        start_time: int,
        end_time: int) -> str:
    LOCAL_SIG_LOC_VISITS_QUERY = f"""
SELECT
    ROW_NUMBER() OVER() AS 'Record',
    Z_PK AS 'Z_PK',
    ZDATAPOINTCOUNT AS 'Data Point Count',
    ZLOCATIONOFINTEREST AS 'Location Of Interest ID',
    strftime('%Y-%m-%dT%H:%M:%SZ', datetime(ZCREATIONDATE + 978307200, 'UNIXEPOCH')) AS 'Creation Date (UTC)',
    strftime('%Y-%m-%dT%H:%M:%SZ', datetime(ZENTRYDATE + 978307200, 'UNIXEPOCH')) AS 'Entry Date (UTC)',
    strftime('%Y-%m-%dT%H:%M:%SZ', datetime(ZEXITDATE + 978307200, 'UNIXEPOCH')) AS 'Exit Date (UTC)',
    strftime('%Y-%m-%dT%H:%M:%SZ', datetime(ZEXPIRATIONDATE + 978307200, 'UNIXEPOCH')) AS 'Expiration Date (UTC)',
    ZLOCATIONLATITUDE AS 'Latitude',
    ZLOCATIONLONGITUDE AS 'Longitude',
    ZLOCATIONHORIZONTALUNCERTAINTY AS 'LocationHorizontalUncertainty',
    ZLOCATIONOFINTERESTCONFIDENCE AS 'LocationConfidence',
    'Local.sqlite [ZRTLEARNEDLOCATIONOFINTERESTVISITMO(Z_PK:' || Z_PK || ')]' AS 'Data Source'

FROM ZRTLEARNEDLOCATIONOFINTERESTVISITMO

WHERE ZCREATIONDATE BETWEEN {start_time} AND {end_time}

ORDER BY Z_PK ASC
"""
    return LOCAL_SIG_LOC_VISITS_QUERY


def localSigLocVisitKmlFileHeader() -> str:
    LOCAL_SIG_LOC_VISITS_KML_FILE_HEADER = f"""<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2"
  xmlns:gx="http://www.google.com/kml/ext/2.2"
  xmlns:kml="http://www.opengis.net/kml/2.2"
  xmlns:atom="http://www.w3.org/2005/Atom">
  <Document>
    <Folder>
      <name>Significant Location Visits Local.sqlite</name>
      <open>1</open>
      <description>View All Records</description>
      <Style id="recordfolder">
        <IconStyle>
          <scale>1.5</scale>
          <Icon>
            <href>
              https://d2gol1mk3n0ygp.cloudfront.net/tower-icons/RedTower.png
            </href>
          </Icon>
          <hotSpot x="0.5" y="0" xunits="fraction" yunits="fraction" />
        </IconStyle>
        <BalloonStyle>
          <text>
            <![CDATA[<html lang="en">
              <head>
                <title>Bootstrap Theme Simply Me</title>
                <meta charset="utf-8" />
                <meta name="author" content="@mikey_spon" />
                <meta name="viewport" content="width=device-width, \
height=device-height, initial-scale=1.0, minimum-scale=1.0" />
                <meta name="robots" content="noindex" />
                <link rel="stylesheet" \
href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" />
                <script \
src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js">\
</script>
                <script \
src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js">\
</script>
                <style>
                  table {{table-layout:fixed;}}
                  table, th, td {{border: 1px solid #000; border-collapse:\
collapse; word-wrap:break-word;}}
                  th, td {{padding:4px; text-align:left;}}
                  table#t01 tr:nth-child(even) {{background-color:#A3A4A4;}}
                  table#t01 tr:nth-child(odd) {{background-color:#FFF;}}
                  table#t01 th {{background-color:grey; color:#FFF;}}
                  table thead tr th {{background-color:#474E5D; color:#FFF; \
padding:4px 8px;}}
                  th.heading {{width:100%;}}
                  td.heading {{background-color:#474E5D; color:#FFF; \
font-size:1.15em; font-weight:bold; padding:5px 8px; width:40%;}}
                  td.data {{font-size:1.15em; padding:5px 8px; width:60%;}}
                </style>
              </head>
              <body>
                <table cellpadding="3" cellspacing="3" bgcolor="#FFF">
                  <thead>
                    <tr>
                      <th class="heading" id="record_id" colspan="2">
                        <h4>Record No.: $[rowid_text]</h4>
                      </th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td class="heading">Data Point Count</td>
                      <td class="data">$[data_point_count]</td>
                    </tr>
                    <tr>
                      <td class="heading">Location of Interest ID</td>
                      <td class="data">$[location_of_interest_id]</td>
                    </tr>
                    <tr>
                      <td class="heading">Latitude</td>
                      <td class="data">$[latitude]</td>
                    </tr>
                    <tr>
                      <td class="heading">Longitude</td>
                      <td class="data">$[longitude]</td>
                    </tr>
                    <tr>
                      <td class="heading">Creation Date (UTC)</td>
                      <td class="data">$[creation_date_utc]</td>
                    </tr>
                    <tr>
                      <td class="heading">Entry Date (UTC)</td>
                      <td class="data">$[entry_date_utc]</td>
                    </tr>
                    <tr>
                      <td class="heading">Exit Date (UTC)</td>
                      <td class="data">$[exit_date_utc]</td>
                    </tr>
                    <tr>
                      <td class="heading">Expiration Date (UTC)</td>
                      <td class="data">$[expiration_date_utc]</td>
                    </tr>
                    <tr>
                      <td class="heading">Location Horiz Uncertainty</td>
                      <td class="data">$[location_horiz_uncertainty]</td>
                    </tr>
                    <tr>
                      <td class="heading">Location Confidence</td>
                      <td class="data">$[location_confidence]</td>
                    </tr>
                    <tr>
                      <td class="heading">Record Source</td>
                      <td class="data">
                        <b>Table:</b><br/>
                        $[data_source]
                      </td>
                    </tr>
                  </tbody>
                </table>
              </body>
            </html>]]>
          </text>
          <bgColor>501400B4</bgColor>
        </BalloonStyle>
        <ListStyle>
          <ItemIcon>
            <href>
              https://d2gol1mk3n0ygp.cloudfront.net/tower-icons/RedTower.png
            </href>
          </ItemIcon>
        </ListStyle>
      </Style>
"""
    return LOCAL_SIG_LOC_VISITS_KML_FILE_HEADER


def localSigLocVisitKmlFileBody(
        record: str,
        data_point_count: int,
        location_of_interest_id: int,
        creation_date_utc: str,
        entry_date_utc: str,
        exit_date_utc: str,
        expiration_date_utc: str,
        latitude: int,
        longitude: int,
        location_horiz_uncertainty: int,
        location_confidence: int,
        data_source: str) -> str:
    LOCAL_SIG_LOC_VISITS_KML_FILE_BODY = f"""
      <Placemark>
        <name>{str(record).zfill(6)}</name>
        <visibility>1</visibility>
        <description>
          <![CDATA[
            <p style="color:green">{creation_date_utc[0:10]} at {creation_date_utc[11:19]} UTC<br />
            [{latitude:.6f}, {longitude:.6f}]</p>
            ]]>
        </description>
        <LookAt>
          <longitude>{longitude}</longitude>
          <latitude>{latitude}</latitude>
          <altitude>0</altitude>
          <heading>0</heading>
          <tilt>0</tilt>
          <range>0</range>
        </LookAt>
        <TimeStamp>
          <when>{creation_date_utc}</when>
        </TimeStamp>
        <styleUrl>#recordfolder</styleUrl>
        <ExtendedData>
          <Data name="rowid_text">
            <value>{str(record).zfill(6)}</value>
          </Data>
          <Data name="data_point_count">
            <value>{data_point_count}</value>
          </Data>
          <Data name="location_of_interest_id">
            <value>{location_of_interest_id}</value>
          </Data>
          <Data name="latitude">
            <value>{latitude:.6f}</value>
          </Data>
          <Data name="longitude">
            <value>{longitude:.6f}</value>
          </Data>
          <Data name="creation_date_utc">
            <value>{creation_date_utc}</value>
          </Data>
          <Data name="entry_date_utc">
            <value>{entry_date_utc}</value>
          </Data>
          <Data name="exit_date_utc">
            <value>{exit_date_utc}</value>
          </Data>
          <Data name="expiration_date_utc">
            <value>{expiration_date_utc}</value>
          </Data>
          <Data name="location_horiz_uncertainty">
            <value>{location_horiz_uncertainty:.6f} meters</value>
          </Data>
          <Data name="location_confidence">
            <value>{location_confidence:.6f}</value>
          </Data>
          <Data name="data_source">
            <value>{data_source}</value>
          </Data>
        </ExtendedData>
        <Point>
          <coordinates>{longitude},{latitude},0</coordinates>
        </Point>
      </Placemark>
"""
    return LOCAL_SIG_LOC_VISITS_KML_FILE_BODY
