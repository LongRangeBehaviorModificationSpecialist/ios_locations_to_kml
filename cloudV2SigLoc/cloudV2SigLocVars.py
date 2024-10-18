# !/usr/bin/env python3

def cloudV2SigLocSqlQuery(
        begin_time: int,
        end_time: int) -> str:
    '''Adds the `begin_time` and `end_time` values to the SQL query that will
    be run against the Cache.sqlite database file so that only records during
    the desired time frame are returned.
    '''
    CLOUDV2_SIG_LOC_QUERY = f'''
SELECT
    ROW_NUMBER() OVER() AS 'RecordNo.',
    ZRTADDRESSMO.Z_PK AS 'ZRTADDRESSMO.Z_PK',
    strftime('%Y-%m-%dT%H:%M:%SZ', datetime(ZRTADDRESSMO.ZCREATIONDATE + 978307200, 'UNIXEPOCH')) AS 'AddressCreationDate(UTC)',
    strftime('%Y-%m-%d %H:%M:%S', datetime(ZRTADDRESSMO.ZCREATIONDATE + 978307200, 'UNIXEPOCH', 'localtime')) AS 'AddressCreationDate(Local)',
    strftime('%Y-%m-%dT%H:%M:%SZ', datetime(ZRTADDRESSMO.ZEXPIRATIONDATE + 978307200, 'UNIXEPOCH')) AS 'AddressExpireDate(UTC)',
    strftime('%Y-%m-%d %H:%M:%S', datetime(ZRTADDRESSMO.ZEXPIRATIONDATE + 978307200, 'UNIXEPOCH', 'localtime')) AS 'AddressExpireDate(Local)',
    ZRTADDRESSMO.ZSUBTHOROUGHFARE || ' ' ||
    REPLACE(ZRTADDRESSMO.ZTHOROUGHFARE, '&', 'at') || ', ' ||
    ZRTADDRESSMO.ZLOCALITY || ', ' ||
    ZRTADDRESSMO.ZADMINISTRATIVEAREA || ' ' ||
    ZRTADDRESSMO.ZPOSTALCODE || ' ' ||
    ZRTADDRESSMO.ZCOUNTRYCODE AS 'AddressInfo',
    ZRTMAPITEMMO.ZLATITUDE AS 'Latitude',
    ZRTMAPITEMMO.ZLONGITUDE AS 'Longitude',
    ZRTMAPITEMMO.ZUNCERTAINTY AS 'Uncertainty',
    'Cloud-V2.sqlite [ZRTADDRESSMO(Z_PK:' || ZRTADDRESSMO.Z_PK || ')]' AS 'DataSource'

FROM ZRTADDRESSMO
    LEFT JOIN ZRTMAPITEMMO ON ZRTADDRESSMO.ZMAPITEM = ZRTMAPITEMMO.ZADDRESS

WHERE ZRTADDRESSMO.ZCREATIONDATE BETWEEN {begin_time} AND {end_time}

ORDER BY ZRTADDRESSMO.Z_PK ASC
'''
    return CLOUDV2_SIG_LOC_QUERY


def cloudV2SigLocKmlFileHeader() -> str:
    CLOUDV2_SIG_LOC_KML_FILE_HEADER = f'''<?xml version='1.0' encoding='UTF-8'?>
<kml xmlns='http://www.opengis.net/kml/2.2'
  xmlns:gx='http://www.google.com/kml/ext/2.2'
  xmlns:kml='http://www.opengis.net/kml/2.2'
  xmlns:atom='http://www.w3.org/2005/Atom'>
  <Document>
    <Folder>
      <name>Locations From Cloud-V2.sqlite</name>
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
                      <td class='heading'>Address</td>
                      <td class='data'>$[address_info]</td>
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
                      <td class='heading'>Uncertainty</td>
                      <td class='data'>$[uncertainty]</td>
                    </tr>
                    <tr>
                      <td class='heading'>Address Creation Date (UTC)</td>
                      <td class='data'>$[add_create_utc]</td>
                    </tr>
                    <tr>
                      <td class='heading'>Address Creation Date (Local)</td>
                      <td class='data'>$[add_create_local]</td>
                    </tr>
                    <tr>
                      <td class='heading'>ZRTADDRESSMO PK No.</td>
                      <td class='data'>$[zrtaddressmo_zpk]</td>
                    </tr>
                    <tr>
                      <td class='heading'>Address Expire Date (UTC)</td>
                      <td class='data'>$[add_expire_utc]</td>
                    </tr>
                    <tr>
                      <td class='heading'>Address Expire Date (Local)</td>
                      <td class='data'>$[add_expire_local]</td>
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
    return CLOUDV2_SIG_LOC_KML_FILE_HEADER


def cloudV2SigLocKmlFileBody(
        record: str,
        address_info: str,
        latitude: int,
        longitude: int,
        uncertainty: int,
        add_create_utc: str,
        add_create_local: str,
        zrtaddressmo_z_pk: str,
        add_expire_utc: str,
        add_expire_local: str,
        data_source: str) -> str:
    CLOUDV2_SIG_LOC_KML_FILE_BODY = f'''
      <Placemark>
        <name>{str(record).zfill(6)}</name>
        <visibility>1</visibility>
        <description>
          <![CDATA[
            <p style="color:green">{add_create_local[0:10]} at {add_create_local[11:19]} ET<br />
            {address_info}<br />
            ({latitude:.6f},{longitude:.6f})</p>
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
          <when>{add_create_utc}</when>
        </TimeStamp>
        <styleUrl>#recordfolder</styleUrl>
        <ExtendedData>
          <Data name='rowid_text'>
            <value>{str(record).zfill(6)}</value>
          </Data>
          <Data name='address_info'>
            <value>{address_info}</value>
          </Data>
          <Data name='latitude'>
            <value>{latitude:.6f}</value>
          </Data>
          <Data name='longitude'>
            <value>{longitude:.6f}</value>
          </Data>
          <Data name='uncertainty'>
            <value>{uncertainty:.6f}</value>
          </Data>
          <Data name='add_create_utc'>
            <value>{add_create_utc}</value>
          </Data>
          <Data name='add_create_local'>
            <value>{add_create_local}</value>
          </Data>
          <Data name='zrtaddressmo_zpk'>
            <value>{zrtaddressmo_z_pk}</value>
          </Data>
          <Data name='add_expire_utc'>
            <value>{add_expire_utc}</value>
          </Data>
          <Data name='add_expire_local'>
            <value>{add_expire_local}</value>
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
    return CLOUDV2_SIG_LOC_KML_FILE_BODY
