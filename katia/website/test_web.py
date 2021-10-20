from flask import *
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
import pandas as pd
from pyowm.owm import OWM
import pandas as pd
from datetime import datetime, timedelta
import pickle
import os
key = "b4a8cf502c2afc3ecbfed7b30c2b831c"

app = Flask(__name__)
model_arrivals = pickle.load(open('website/model_arrivals.pkl','rb'))
model_departures = pickle.load(open('website/model_departures.pkl','rb'))

@app.route("/")
def index():
    predictions = run_model()
    return render_template("index.html",predictions = predictions)

def run_model():
    current_bikes = get_bike_data()
    date = pd.DataFrame(columns=['datetime'])
    date.loc[0]=datetime.now().strftime('%Y-%m-%d %H:%M:00')
    current_bikes = current_bikes.merge(date,how='cross')
    current_bikes.rename(columns={'bikesAvailable':'bikes_evolution','spacesAvailable':'spaces_evolution','stationId':'id'},inplace=True)

    station_id = pd.DataFrame([76.0, 64.0, 30.0, 69.0,  6.0, 11.0, 118.0, 130.0, 44.0, 46.0, 86.0, 89.0,  8.0, 31.0, 122.0, 29.0, 123.0, 38.0, 114.0, 24.0, 33.0,  7.0, 23.0, 60.0, 120.0, 17.0, 21.0, 22.0, 70.0, 18.0, 27.0, 28.0, 63.0, 25.0, 26.0,  5.0,  1.0, 78.0, 117.0, 12.0, 19.0, 137.0, 39.0, 75.0, 53.0, 43.0, 121.0, 10.0, 127.0, 133.0,  3.0, 129.0, 48.0, 14.0, 83.0, 20.0, 58.0, 125.0, 116.0, 113.0, 62.0, 42.0, 68.0, 115.0, 128.0, 40.0, 134.0, 110.0, 61.0, 105.0, 149.0, 36.0, 73.0, 109.0, 34.0, 45.0, 32.0, 81.0, 54.0, 57.0, 95.0, 101.0, 74.0, 15.0,  4.0, 50.0, 52.0, 144.0, 150.0, 13.0, 108.0, 16.0, 96.0, 141.0, 147.0,  2.0, 136.0, 65.0, 135.0, 146.0, 142.0, 56.0, 71.0, 82.0, 94.0, 119.0, 79.0, 111.0, 131.0, 140.0, 138.0, 106.0, 103.0, 112.0, 139.0, 148.0, 107.0, 104.0, 99.0, 93.0, 51.0, 91.0, 41.0, 997.0, 66.0, 145.0, 47.0, 157.0, 162.0, 59.0, 77.0, 88.0, 90.0, 84.0, 132.0, 100.0, 92.0, 49.0, 67.0, 80.0, 72.0, 155.0, 161.0, 163.0, 124.0, 156.0, 35.0, 87.0, 999.0, 159.0, 55.0, 143.0, 126.0, 547.0, 531.0, 545.0, 543.0, 507.0, 527.0, 529.0, 597.0, 563.0, 555.0, 537.0, 533.0, 631.0, 619.0, 617.0, 607.0, 601.0, 603.0, 609.0, 615.0, 541.0, 587.0, 539.0, 621.0, 611.0, 613.0, 623.0, 589.0, 585.0, 583.0, 653.0, 523.0, 581.0, 651.0, 575.0, 517.0, 573.0, 521.0, 557.0, 637.0, 647.0, 577.0, 509.0, 511.0, 645.0, 519.0, 595.0, 633.0, 591.0, 571.0, 565.0, 639.0, 561.0, 635.0, 525.0, 643.0, 641.0, 513.0, 627.0, 559.0, 629.0, 515.0, 505.0, 593.0, 625.0, 579.0, 553.0, 503.0, 551.0, 85.0, 37.0, 98.0, 596.0, 715.0, 713.0, 717.0, 707.0, 735.0, 723.0, 649.0, 701.0, 711.0, 721.0, 705.0, 727.0, 719.0, 729.0, 725.0, 733.0, 737.0, 769.0, 741.0, 749.0, 761.0, 763.0, 751.0, 739.0, 745.0, 753.0, 755.0, 757.0, 767.0, 765.0, 747.0, 709.0, 549.0, 501.0, 731.0, 901.0, 998.0, 235.0, 202.0, 240.0, 233.0, 230.0, 206.0, 239.0, 703.0, 231.0, 532.0, 242.0, 241.0, 518.0, 203.0, 228.0, 224.0, 221.0, 207.0, 236.0, 208.0, 234.0, 227.0, 210.0, 244.0, 246.0, 226.0, 229.0, 220.0, 259.0, 213.0, 237.0, 225.0, 217.0, 232.0, 268.0, 218.0, 258.0, 219.0, 222.0, 256.0, 262.0, 260.0, 211.0, 245.0, 255.0, 254.0, 238.0, 223.0, 257.0, 261.0, 263.0, 273.0, 270.0, 275.0, 265.0, 284.0, 276.0, 274.0, 272.0, 209.0, 214.0, 215.0, 271.0, 249.0, 538.0, 264.0, 248.0, 247.0, 253.0, 279.0, 252.0, 280.0, 285.0, 243.0, 286.0, 278.0, 212.0, 269.0, 281.0, 250.0, 200.0, 201.0, 283.0, 277.0, 216.0, 205.0, 282.0, 267.0, 266.0, 900.0, 251.0, 204.0, 290.0, 292.0, 291.0, 151.0])
    station_id.rename(columns ={0:'id'},inplace=True)

    now = datetime.now()
    
    prediction_time = pd.date_range(now,(now+timedelta(hours=6)),freq='5T')
    prediction_time = prediction_time.round("5min")
    if prediction_time[0] <= pd.to_datetime(now.strftime('%Y-%m-%d %H:%M:00')):
        prediction_time = prediction_time+timedelta(minutes=5)

    weather = get_weather_data()
    weather_data = pd.DataFrame(index=prediction_time,columns=['Cloud amount (1/8)','Relative humidity (%)','Precipitation intensity (mm/h)','Air temperature (degC)','Wind speed (m/s)'])
    empty_hour = []
    for i in weather_data.iterrows():
        weather_row = weather.loc[weather['datetime'] == i[0].strftime('%Y-%m-%d %H:00:00')]
        if weather_row.empty :
            weather_data.drop(index = i[0])
            continue
        i[1]['Cloud amount (1/8)'] = weather_row['Cloud amount (1/8)'].iloc[0]
        i[1]['Relative humidity (%)'] = weather_row['Relative humidity (%)'].iloc[0]
        i[1]['Precipitation intensity (mm/h)'] = weather_row['Precipitation intensity (mm/h)'].iloc[0]
        i[1]['Air temperature (degC)'] = weather_row['Air temperature (degC)'].iloc[0]
        i[1]['Wind speed (m/s)'] = weather_row['Wind speed (m/s)'].iloc[0]
    
    weather_data['time'] = weather_data.index.strftime('%H:%M:00')
    time_convert = pd.DataFrame(pd.date_range(start="00:00:00",end="23:55:00",freq ='5T').strftime('%H:%M:%S'))
    time_convert.rename(columns = {0:'time'}, inplace = True)
    time_convert['to_int'] = pd.RangeIndex(start=1,stop=time_convert.shape[0]+1)
    time_convert = time_convert.set_index('time')
    weather_data = weather_data.join(time_convert,on="time")
    weather_data.drop(columns="time",inplace=True)
    weather_data.rename(columns = {'to_int':'time'}, inplace = True)

    weather_data['day_of_week'] = weather_data.index.dayofweek
    weather_data['day_of_year'] = weather_data.index.dayofyear
    weather_data['datetime'] = weather_data.index
    
    data = weather_data.merge(station_id,how='cross')

    predictions = [ round(elem) for elem in model_departures.predict(data[['id','time','day_of_week','day_of_year','Cloud amount (1/8)','Relative humidity (%)','Precipitation intensity (mm/h)','Air temperature (degC)','Wind speed (m/s)']].values.reshape(-1, 9))]
    departures_prediction = pd.concat([pd.DataFrame(predictions),pd.DataFrame(data[['id','datetime']])],axis=1).rename(columns={0:'bike_departures'})

    predictions = [ round(elem) for elem in model_arrivals.predict(data[['id','time','day_of_week','day_of_year','Cloud amount (1/8)','Relative humidity (%)','Precipitation intensity (mm/h)','Air temperature (degC)','Wind speed (m/s)']].values.reshape(-1, 9))]
    arrivals_prediction = pd.concat([pd.DataFrame(predictions),pd.DataFrame(data[['id','datetime']])],axis=1).rename(columns={0:'bike_arrivals'})

    predict_df = arrivals_prediction.merge(departures_prediction, how='outer', on=['id','datetime'])
    predict_df = predict_df.fillna(0)
    predict_df['bikes_evolution'] = predict_df['bike_arrivals'] - predict_df['bike_departures']
    predict_df['spaces_evolution'] = -1 * predict_df['bikes_evolution']
    predict_df.drop(columns=['bike_arrivals','bike_departures'],inplace=True)
    predict_df = pd.concat([predict_df[['datetime','id','bikes_evolution','spaces_evolution']],current_bikes[['datetime','id','bikes_evolution','spaces_evolution']]])
    predict_df['datetime'] = pd.to_datetime(predict_df['datetime'] )
    predict_df = predict_df.sort_values(by='datetime')
    predict_df2 = predict_df.groupby(['id']).cumsum()
    predict_df2 = predict_df2.assign(id=predict_df['id'])
    predict_df2 = predict_df2.assign(datetime = predict_df['datetime'])
    return predict_df2.sort_values(by=['id','datetime'])


def get_bike_data():
    transport = RequestsHTTPTransport(
    url="https://api.digitransit.fi/routing/v1/routers/hsl/index/graphql", verify=True, retries=3)

    client = Client(transport=transport, fetch_schema_from_transport=True)

    query = gql(
        """
        query {
            bikeRentalStations {
                bikesAvailable
                spacesAvailable
                stationId
                }
            }
    """
    )

    result = client.execute(query)
    
    return pd.DataFrame(result['bikeRentalStations'])

def get_weather_data():
    now = datetime.now()
    df = pd.DataFrame(columns=["datetime",'Wind speed (m/s)','Relative humidity (%)','Air temperature (degC)','Precipitation intensity (mm/h)','Cloud amount (1/8)'])

    owm = OWM(key)
    mgr = owm.weather_manager()

    one_call = mgr.one_call(lat=60.1733244, lon=24.9410248, exclude='minutely,daily,alerts', units='metric')
    n = 0
    for i in one_call.forecast_hourly:
        row = {"datetime":(now+timedelta(hours=n)).strftime("%d/%m/%Y %H:00:00"),'Wind speed (m/s)':i.wind()['speed'],'Relative humidity (%)':i.humidity,'Air temperature (degC)':i.temperature()['temp'],'Precipitation intensity (mm/h)':i.rain,'Cloud amount (1/8)':i.clouds}
        if row['Precipitation intensity (mm/h)'] == {}:
            row['Precipitation intensity (mm/h)'] = 0
        else:
            row['Precipitation intensity (mm/h)'] = row['Precipitation intensity (mm/h)']['1h']
        row['Cloud amount (1/8)'] = round((row['Cloud amount (1/8)']*8)/100)
        df = df.append(row,ignore_index=True)
        n +=1
        if n == 7:
            break

    df['datetime'] = pd.to_datetime(df['datetime'])
    return df



@app.route("/about")
def presentation():
    return render_template("index.html")

@app.route("/project")
def project():
    return render_template("index.html")

if __name__ == "__main__":
   app.run(debug=True, host='0.0.0.0', port='5000')