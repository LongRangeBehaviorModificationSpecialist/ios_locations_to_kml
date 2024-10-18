# !/usr/bin/env python3

def cacheEncBLteSqlQuery(
        begin_time: int,
        end_time: int) -> str:
    CACHE_ENCRYPTEDB_LTE_QUERY = f'''
SELECT
    ROW_NUMBER() OVER() AS 'RecordNo.',
    strftime('%Y-%m-%dT%H:%M:%SZ', datetime(Timestamp + 978307200, 'UNIXEPOCH')) AS 'Timestamp(UTC)',
    strftime('%Y-%m-%d %H:%M:%S', datetime(Timestamp + 978307200, 'UNIXEPOCH', 'localtime')) AS 'Timestamp(Local)',
    Latitude AS 'Latitude',
    Longitude AS 'Longitude',
    MCC AS 'MCC',
    MNC AS 'MNC',
    TAC AS 'TAC',
    CI AS 'CI',
    HorizontalAccuracy AS 'HorizontalAccuracy',
    Altitude AS 'Altitude',
    Confidence AS 'Confidence',
    'cache_encryptedB.db(Table:LteCellLocations)' AS 'DataSource'

FROM LteCellLocation

WHERE Timestamp BETWEEN {begin_time} AND {end_time}

ORDER BY timestamp ASC
'''
    return CACHE_ENCRYPTEDB_LTE_QUERY


def cacheEncBLteKmlFileHeader() -> str:
    CACHE_ENCRYPTEDB_LTE_KML_FILE_HEADER = f'''<?xml version='1.0' encoding='UTF-8'?>
<kml xmlns='http://www.opengis.net/kml/2.2'
  xmlns:gx='http://www.google.com/kml/ext/2.2'
  xmlns:kml='http://www.opengis.net/kml/2.2'
  xmlns:atom='http://www.w3.org/2005/Atom'>
  <Document>
    <Folder>
      <name>LTE Locations From cache_encryptedB.db</name>
      <open>1</open>
      <description>View All Records</description>
      <Style id='recordfolder'>
        <IconStyle>
          <scale>1.5</scale>
          <Icon>
            <href>
              https://d2gol1mk3n0ygp.cloudfront.net/tower-icons/RedTower.png
            </href>
          </Icon>
          <hotSpot x='0.5' y='0' xunits='fraction' yunits='fraction' />
        </IconStyle>
        <BalloonStyle>
          <text>
            <![CDATA[<html lang='en'>
              <head>
                <title>Bootstrap Theme Simply Me</title>
                <meta charset='utf-8' />
                <meta name='author' content='@mikey_spon' />
                <meta name='viewport' content='width=device-width, \
height=device-height, initial-scale=1.0, minimum-scale=1.0' />
                <meta name='robots' content='noindex' />
                <link rel='stylesheet' \
href='https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css' />
                <script \
src='https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js'>\
</script>
                <script \
src='https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js'>\
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
                <table cellpadding='3' cellspacing='3' bgcolor='#FFF'>
                  <thead>
                    <tr>
                      <th class='heading' id='record_id' colspan='2'>
                        <h4>Record No.: $[rowid_text]</h4>
                      </th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td class='heading'>Date/Time (UTC)</td>
                      <td class='data'>$[date_time_utc]</td>
                    </tr>
                    <tr>
                      <td class='heading'>Date/Time (Local)</td>
                      <td class='data'>$[date_time_local]</td>
                    </tr>
                    <tr>
                      <td class='heading'>Latitude</td>
                      <td class='data'>$[latitude]</td>
                    </tr>
                    <tr>
                      <td class='heading'>Longitude</td>
                      <td class='data'>$[longitude]</td>
                    </tr>
                    <tr>
                      <td class='heading'>Site Info</td>
                      <td class='data'>$[site_info]</td>
                    </tr>
                    <tr>
                      <td class='heading'>Horiz. Accuracy</td>
                      <td class='data'>$[horiz_accuracy]</td>
                    </tr>
                    <tr>
                      <td class='heading'>Altitude</td>
                      <td class='data'>$[altitude]</td>
                    </tr>
                    <tr>
                      <td class='heading'>Confidence</td>
                      <td class='data'>$[confidence]</td>
                    </tr>
                    <tr>
                      <td class='heading'>Record Source</td>
                      <td class='data'>
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
'''
    return CACHE_ENCRYPTEDB_LTE_KML_FILE_HEADER


def cacheEncBLteKmlFileBody(
        record: str,
        local_time: str,
        latitude: int,
        longitude: int,
        horiz_accuracy: str,
        utc_time: str,
        site_info: str,
        altitude: str,
        confidence: str,
        data_source: str) -> str:
    CACHE_ENCRYPTEDB_LTE_KML_FILE_BODY = f'''
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
          <range>{horiz_accuracy}</range>
        </LookAt>
        <TimeStamp>
          <when>{utc_time}</when>
        </TimeStamp>
        <styleUrl>#recordfolder</styleUrl>
        <ExtendedData>
          <Data name='rowid_text'>
            <value>{str(record).zfill(6)}</value>
          </Data>
          <Data name='date_time_utc'>
            <value>{utc_time}</value>
          </Data>
          <Data name='date_time_local'>
            <value>{local_time}</value>
          </Data>
          <Data name='latitude'>
            <value>{latitude:.6f}</value>
          </Data>
          <Data name='longitude'>
            <value>{longitude:.6f}</value>
          </Data>
          <Data name='site_info'>
            <value>{site_info}</value>
          </Data>
          <Data name='horiz_accuracy'>
            <value>{horiz_accuracy} meters</value>
          </Data>
          <Data name='altitude'>
            <value>{altitude} meters</value>
          </Data>
          <Data name='confidence'>
            <value>{confidence}</value>
          </Data>
          <Data name='data_source'>
            <value>{data_source}</value>
          </Data>
        </ExtendedData>
        <Point>
          <coordinates>{longitude},{latitude},0</coordinates>
        </Point>
      </Placemark>
'''
    return CACHE_ENCRYPTEDB_LTE_KML_FILE_BODY
