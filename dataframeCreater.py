import feather
import pandas as pd
import os


def readparquet_folder(folder,feather_name):   #read parquets de um folder e cria um dataframe
    dataframe=pd.DataFrame()
    for filename in os.listdir(folder):
        a=pd.read_parquet(folder+"/"+filename)
        dataframe=dataframe.append(a)
    feather.write_dataframe(dataframe, feather_name+".feather")

def readparquet(filename,feather_name):  #read parquets de uma file ou uma lista de files
    if type(filename)==str:
        filename=[filename]
    dataframe=pd.DataFrame()
    for i in filename:
        a=pd.read_parquet(i)
        dataframe=dataframe.append(a)
    feather.write_dataframe(dataframe, feather_name+".feather")