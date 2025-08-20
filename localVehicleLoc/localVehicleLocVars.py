# !/usr/bin/env python3

def localVehicleLocSqlQuery(
        begin_time: int,
        end_time: int) -> str:
    LOCAL_VEH_LOC_QUERY = f"""
SELECT
    ROW_NUMBER() OVER() AS 'Record',
    Z_PK AS 'Z_PK',
    strftime('%Y-%m-%dT%H:%M:%SZ', datetime(ZDATE + 978307200, 'UNIXEPOCH')) AS 'Date (UTC)',
    strftime('%Y-%m-%d %H:%M:%S', datetime(ZDATE + 978307200, 'UNIXEPOCH', 'localtime')) AS 'Date (Local)',
    strftime('%Y-%m-%dT%H:%M:%SZ', datetime(ZLOCDATE + 978307200, 'UNIXEPOCH')) AS 'Location Date (UTC)',
    strftime('%Y-%m-%d %H:%M:%S ', datetime(ZLOCDATE + 978307200, 'UNIXEPOCH', 'localtime')) AS 'Location Date (Local)',
    ZLOCLATITUDE AS 'Latitude',
    ZLOCLONGITUDE AS 'Longitude',
    ZLOCUNCERTAINTY AS 'Location Uncertainty',
    ZIDENTIFIER AS 'Identifier',
    'Local.sqlite [ZRTVEHICLEEVENTHISTORYMO(Z_PK:' || Z_PK || ')]' AS 'Data Source'

FROM ZRTVEHICLEEVENTHISTORYMO

WHERE ZDATE BETWEEN {begin_time} AND {end_time}

ORDER BY ZDATE ASC
"""
    return LOCAL_VEH_LOC_QUERY


def localVehicleLocKmlFileHeader() -> str:
    LOCAL_VEH_LOC_KML_FILE_HEADER = f"""<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2"
  xmlns:gx="http://www.google.com/kml/ext/2.2"
  xmlns:kml="http://www.opengis.net/kml/2.2"
  xmlns:atom="http://www.w3.org/2005/Atom">
  <Document>
    <Folder>
      <name>Vehicle Locations From Local.sqlite</name>
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
                      <td class="heading">Date/Time (UTC)</td>
                      <td class="data">$[utc_time]</td>
                    </tr>
                    <tr>
                      <td class="heading">Date/Time (Local)</td>
                      <td class="data">$[local_time]</td>
                    </tr>
                    <tr>
                      <td class="heading">Location Date/Time (UTC)</td>
                      <td class="data">$[location_time_utc]</td>
                    </tr>
                    <tr>
                      <td class="heading">Location Date/Time (Local)</td>
                      <td class="data">$[location_time_local]</td>
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
                      <td class="heading">Uncertainty</td>
                      <td class="data">$[location_uncertainty]</td>
                    </tr>
                    <tr>
                      <td class="heading">Identifier</td>
                      <td class="data">$[identifier]</td>
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
    return LOCAL_VEH_LOC_KML_FILE_HEADER


def localVehicleLocKmlFileBody(
        record: str,
        utc_time: str,
        local_time: str,
        location_time_utc: str,
        location_time_local: str,
        latitude: int,
        longitude: int,
        location_uncertainty: int,
        identifier: str,
        data_source: str) -> str:
    LOCAL_VEH_LOC_KML_FILE_BODY = f"""
      <Placemark>
        <name>{str(record).zfill(6)}</name>
        <visibility>1</visibility>
        <description>
          <![CDATA[
            <p style="color:green">{local_time[0:10]} at {local_time[11:19]} ET<br />
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
          <when>{utc_time}</when>
        </TimeStamp>
        <styleUrl>#recordfolder</styleUrl>
        <ExtendedData>
          <Data name="rowid_text">
            <value>{str(record).zfill(6)}</value>
          </Data>
          <Data name="utc_time">
            <value>{utc_time}</value>
          </Data>
          <Data name="local_time">
            <value>{local_time}</value>
          </Data>
          <Data name="location_time_utc">
            <value>{location_time_utc}</value>
          </Data>
          <Data name="location_time_local">
            <value>{location_time_local}</value>
          </Data>
          <Data name="latitude">
            <value>{latitude:.6f}</value>
          </Data>
          <Data name="longitude">
            <value>{longitude:.6f}</value>
          </Data>
          <Data name="location_uncertainty">
            <value>{location_uncertainty:.6f}</value>
          </Data>
          <Data name="identifier">
            <value>{identifier}</value>
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
    return LOCAL_VEH_LOC_KML_FILE_BODY
