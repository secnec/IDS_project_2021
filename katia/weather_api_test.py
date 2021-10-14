from pyowm.owm import OWM
import pandas as pd
from datetime import datetime, timedelta
key = "b4a8cf502c2afc3ecbfed7b30c2b831c"
now = datetime.now()
df = pd.DataFrame(columns=["datetime",'Wind speed (m/s)','Humidity (%)','Temperature (°C)','Precipitation intensity (mm/h)','Cloudiness (%)'])

owm = OWM(key)
mgr = owm.weather_manager()

one_call = mgr.one_call(lat=60.1733244, lon=24.9410248, exclude='minutely,daily,alerts', units='metric')
n = 0
for i in one_call.forecast_hourly:
    row = {"datetime":(now+timedelta(hours=n)).strftime("%d/%m/%Y %H:00:00"),'Wind speed (m/s)':i.wind()['speed'],'Humidity (%)':i.humidity,'Temperature (°C)':i.temperature()['temp'],'Precipitation intensity (mm/h)':i.rain,'Cloudiness (%)':i.clouds}
    df = df.append(row,ignore_index=True)
    n +=1

df['datetime'] = pd.to_datetime(df['datetime'])
print(df)