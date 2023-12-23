import feather
import datetime

def edit_data(featherfile,editedfile,lon1=None,lon2=None,lat1=None,lat2=None,date1=None,date2=None):
    dataframe=feather.read_dataframe(featherfile)
    dataframe=dataframe[["date","icao24","origin_country","longitude","latitude","on_ground","velocity","vertical_rate","geo_altitude"]]
    if lon1==None:
        dataframe = dataframe[(dataframe["longitude"] < 500)]  #tira os dados sem longitude
    else:
        dataframe=dataframe[(dataframe["longitude"] >lon1) & (dataframe["longitude"]<lon2) & (dataframe["latitude"]>lat1) & (dataframe["latitude"]<lat2)]
    if date1!=None:
        dataframe = dataframe[(dataframe["date"] <= date2 + datetime.timedelta(0, 0, 0, 0, 0, 2, 0)) & (dataframe["date"] >= date1 - datetime.timedelta(0, 0, 0, 0, 0, 2, 0))]
    dataframe=dataframe.sort_values(["icao24","date"]).reset_index(drop=True)

    feather.write_dataframe(dataframe,editedfile+".feather")
