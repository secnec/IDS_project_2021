from pyowm.owm import OWM
import pandas as pd
from datetime import datetime, timedelta
key = "b4a8cf502c2afc3ecbfed7b30c2b831c"
now = datetime.now()


owm = OWM(key)
mgr = owm.weather_manager()

one_call = mgr.one_call(lat=60.1733244, lon=24.9410248, exclude='minutely,daily,alerts', units='metric')
n = 0
for i in one_call.forecast_hourly:
    print("Time :",(now+timedelta(hours=n)).strftime("%d/%m/%Y %H:00:00"))
    print('Wind speed :', i.wind()['speed'],'m/s')
    print('Humidity :',i.humidity,'%')
    print('Temperature :',i.temperature()['temp'], '°C')
    print('Precipitation intensity :',i.rain, 'mm/h')
    print('Cloudiness :',i.clouds, '%')
    n +=1


df = pd.DataFrame(columns=["datetime",'Wind speed','Humidity','Temperature','Precipitation intensity','Cloudiness'])
print(df)