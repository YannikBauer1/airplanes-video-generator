import feather
import pandas as pd
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import datetime
from geographiclib.geodesic import Geodesic



geod=Geodesic.WGS84
def interpolate(lon1, lat1, lon2, lat2,t):
    path=geod.InverseLine(lat1,lon1,lat2,lon2)
    point=path.Position(path.s13*t, Geodesic.STANDARD)
    return (point["lon2"], point["lat2"])


def createImages(featherfile,frames_folder,t0,t1,frames,where=None): #o where pode ser "europe" e toda outra entrada no where vai dar o mundo inteiro
    dataframe = feather.read_dataframe(featherfile)
    dataframe = dataframe[(dataframe["date"] <= t1 + datetime.timedelta(0, 0, 0, 0, 0, 2, 0)) & (dataframe["date"] >= t0 - datetime.timedelta(0, 0, 0, 0, 0, 2, 0))]

    if where=="europe":  #tira os dados fora da europa se escolha para fazer um video sobre europa
        dataframe=dataframe[(dataframe["longitude"] >-40) & (dataframe["longitude"]<50) & (dataframe["latitude"]>30) & (dataframe["latitude"]<72)]
    dataframe = dataframe.reset_index(drop=True)

    fig, ax = plt.subplots(figsize=(10, 10))
    #dataframe[["icao24"]].drop_duplicates().T.values[0]
    air = pd.DataFrame([dataframe[["icao24"]].drop_duplicates().T.values[0], dataframe.drop_duplicates("icao24", keep="first").index.values,
                        dataframe.drop_duplicates("icao24", keep="last").index.values,
                        dataframe.drop_duplicates("icao24", keep="first")[["date"]].T.values[0],   #faz um datrame com colunas:icao24, index dos primeiros dados,
                        dataframe.drop_duplicates("icao24", keep="last")[["date"]].T.values[0]])  #index dos ultimos dados, data dos primeiros dados, data dos ultimos dados
    print(air)
    air = air.transpose()
    print(air)
    air.columns = ["icao24", "index1", "index2", "date1", "date2"]
    air.set_index("icao24", inplace=True)

    def findposition(airplane, time):  #retorna o date,lon,lat do aviao mais proximo antes e depois do tempo e um boolen h que diz se o voo tem dados antes e depois do t
        t0 = air.loc[airplane, "index1"]
        t1 = air.loc[airplane, "index2"]
        h = True
        if (dataframe.loc[t0, "date"] > time) or (dataframe.loc[t1, "date"] < time):
            h = False
        else:
            while t1 - t0 > 1:    #pesquisa binária
                m = (t1 + t0) // 2
                if dataframe.loc[m, "date"] > time:
                    t1 = m
                else:
                    t0 = m
        return (dataframe.loc[t0, "date"], dataframe.loc[t0, "longitude"], dataframe.loc[t0, "latitude"],
                dataframe.loc[t1, "date"], dataframe.loc[t1, "longitude"], dataframe.loc[t1, "latitude"], h)
    def drawFrame(t):
        if where=="europe":
            m = Basemap(projection='merc', llcrnrlat=30, urcrnrlat=72, llcrnrlon=-40, urcrnrlon=50, resolution='c')
        else:
            m = Basemap(projection="mill", llcrnrlat=-60, urcrnrlat=90, llcrnrlon=-180, urcrnrlon=180, resolution='c')
        m.drawcoastlines()
        m.fillcontinents(color='coral', lake_color='aqua')
        m.drawmapboundary(fill_color='aqua')
        m.drawcountries(linewidth=1, color='black')
        m.nightshade(t)
        newAirplanes = air[(air["date1"] < t) & (air["date2"] > t)].index.values  #os avioes que tem dados antes e depois o t
        for i in newAirplanes:
            t1, lon1, lat1, t2, lon2, lat2, h = findposition(i, t)
            if t2 - t1 > datetime.timedelta(0, 0, 0, 0, 0, 2, 0) or h == False:  #se a diferenca de t2,t1 maior que duas horas ou h false continue
                continue
            else:
                time = (t - t1) / (t2 - t1)
                lon, lat = interpolate(lon1, lat1, lon2, lat2, time)
                x, y = m(lon, lat)
                m.plot(x, y, 'k*', markersize=5)
        st=str(t).replace(":","-").replace(".","-")
        plt.annotate(st[0:19], xy=(0.005, 0.005), xycoords='axes fraction') #escreve o tempo no canto em baixo esquerdo
        st = frames_folder+"\out" + st + ".png"
        print(st)
        fig.set_size_inches(16.5, 8.5)   #faz o imagem mais grande
        fig.savefig(st)
        plt.cla()      #limpa o plt

    step=(t1-t0)/(frames-1)
    for i in range(frames):
        t=t0+i*step
        drawFrame(t)

createImages("dadosEdited(1.1-15.1).feather","imagens3",datetime.datetime(2020,1,1,0,0,0,0),datetime.datetime(2020,1,2,0,0,0,0),1440)
