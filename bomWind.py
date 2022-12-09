import pandas as pd
import requests
from datetime import datetime, timedelta

def bomDF(state, place, station):
    if state == "wa":
        timeZone = "AWST"
    elif state == "nsw":
        timeZone = "AEDT"
    elif state == "vic":
        timeZone = "AEDT"
    elif state == "qld":
        timeZone = "AEST"
    elif state == "sa":
        timeZone = "ACST"
    elif state == "tas":
        timeZone = "AEDT"
    elif state == "nt":
        timeZone = "ACST"
    elif state == "act":
        timeZone = "AEDT"

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    }

    bomWebsite = requests.get('http://www.bom.gov.au/places/{}/{}/observations/{}/'.format(state, place, station), headers=headers)
    html = bomWebsite.text

    tables = pd.read_html(html, match = "Wind Speed")

    columns = ["Time ({})".format(timeZone), "Wind Speed (km/h) (knots)", "Wind Gust (km/h) (knots)"]

    today = datetime.today()

    masterDF = pd.DataFrame(columns=columns)
    for index, subTable in enumerate(tables[1:]):

        # Get the relevant date
        date = today - timedelta(days=index)
        dateString = date.strftime("%Y-%m-%d")

        bomData = subTable[columns]
        bomData[columns[0]] = bomData[columns[0]].apply(lambda x: pd.to_datetime("{} {}".format(dateString, x)).strftime("%Y-%m-%d %H:%M"))
        bomData[columns[0]] = bomData[columns[0]].apply(lambda x: datetime.strptime("{}:00".format(x), "%Y-%m-%d %H:%M:%S"))


        bomData[columns[1]] = bomData[columns[1]].apply(lambda x: int(str(x)[:2]))
        try:
            bomData[columns[2]] = bomData[columns[2]].apply(lambda x: int(str(x)[:2]))
        except:
            bomData[columns[2]] = [0 for i in range(len(bomData))]

        bomData["Wind Speed (m/s)"] = bomData[columns[1]].apply(lambda x: x*1000/(60*60))
        bomData["Wind Gust (m/s)"] = bomData[columns[2]].apply(lambda x: x*1000/(60*60))

        masterDF = pd.concat([masterDf, bomData])

    masterDF = masterDF.sort_values(by="Time ({})".format(timeZone)).reset_index(drop=True)

    return masterDF, timeZone

# EXAMPLE
if __name__ == "__main__":
    df = bomDF("wa", "perth", "perth-airport")
