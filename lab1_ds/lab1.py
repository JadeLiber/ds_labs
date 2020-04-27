# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 12:24:53 2020

@author: Acer
"""

from urllib.request import urlopen
import pandas as pd 
import datetime
import os
import glob
#from spyre import server


def delete_data(directory): #удалить все чсв-шные файлы из папки
    for file in glob.glob(os.path.join(directory, "*.csv")):
        os.remove(file) 
        
        
def download_data(i, prov, directory): #загрузить файлы с адекватной первой строкой в папку
        
        url="https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/get_TS_admin.php?country=UKR&provinceID="+str(i)+"&year1=1981&year2=2020&type=Mean"
        vhi_url = urlopen(url)
        #print (type((vhi_url.readline()).decode("utf-8")))
        now=datetime.datetime.now().strftime("%Y_%m_%d-%Hh_%Mm_%Ss")
        file_name = os.path.join(directory, '_id_'+str(i)+'.csv')
        

        
        with open(file_name,'a') as out: #создание файла для хранения данных и открытие для записи
            line = vhi_url.readline().decode("utf-8")
            print (line)
            line = line.replace(line[:line.find("<pre>")+5],'')
            out.write(''.join(line.split(" ")))
            for line in vhi_url.readlines():
                if "/pre" in line.decode("utf-8"): 
                    continue
                else:
                    line=''.join((line.decode("utf-8")).split(" "))
                    #print (vhi_url.read().decode("utf-8"))
                    out.write(line) 
            #out.close() 
    
        print ("VHI is downloaded...")
        return file_name



def read_to_frame(prov, prov_id, directory):   
    df = pd.DataFrame(columns = ['year','week', 'SMN','SMT','VCI','TCI','VHI', 'Province', 'id'])
    for i in range (1,28):
         for file_name in glob.glob(os.path.join(directory, "*_{}.csv".format(i))):
             print (file_name)
             colnames=['year','week', 'SMN','SMT','VCI','TCI','VHI','unnamed'] #задаём имена столбиков
             temp = pd.read_csv(file_name, sep=",", names = colnames, usecols =['year','week', 'SMN','SMT','VCI','TCI','VHI'], index_col=False, header=None) #чтение файла в формате csv (excel)
             temp['Province']= prov[i]
             temp['id'] = prov_id [i]
             temp = temp.loc[temp.VHI!=-1]
             df = df.append(temp, ignore_index=True)
    return df



def year_and_province(df, year, prov_id):
    return (df.loc[(df.year == year) & (df.id == prov_id)])[['year', 'id', 'Province', 'VHI']]
    
def maxVHI_year_prov(df, year, prov_id):
    return (df.loc[(df.year == year) & (df.id == prov_id)])['VHI'].max()
def minVHI_year_prov(df, year, prov_id):
    return (df.loc[(df.year == year) & (df.id == prov_id)])['VHI'].min()

def province_VHI(df, prov_id):
    return (df.loc[df.id==prov_id])[['year', 'VHI']]

def years_VHI_by_procent (df, prov_id, min_procent, max_VHI):
    years = (df.loc[(df.id==prov_id)])['year'].unique()
    result_years = []
    for year in years:
        count = (df.loc[(df.id==prov_id)&(df.VHI<max_VHI)&(df.year==year)])['week'].count()
        count_all = (df.loc[(df.id==prov_id)&(df.year==year)])['week'].count()
        if count*100/count_all>=min_procent:
            result_years.append(year)
    return result_years

def years_VHI_by_procent_normal (df, prov_id, min_procent):
    years = (df.loc[(df.id==prov_id)])['year'].unique()
    result_years = []
    for year in years:
        count = (df.loc[(df.id==prov_id)&(df.VHI>60)&(df.year==year)])['week'].count()
        count_all = (df.loc[(df.id==prov_id)&(df.year==year)])['week'].count()
        if count*100/count_all>=min_procent:
            result_years.append(year)
    return result_years

province_id_first = {       1:"Cherkasy",
                            2:"Chernihiv",
                            3:"Chernivtsi",
                            4:"Crimea",
                            5:"Dnipropetrovs'k",
                            6:"Donets'k",
                            7:"Ivano-Frankivs'k",
                            8:"Kharkiv",
                            9:"Kherson",
                            10:"Khmel'nyts'kyy",
                            11:"Kiev",
                            12:"Kiev City",
                            13:"Kirovohrad",
                            14:"Luhans'k",
                            15:"L'viv",
                            16:"Mykolayiv",
                            17:"Odessa",
                            18:"Poltava",
                            19:"Rivne",
                            20:"Sevastopol'",
                            21:"Sumy",
                            22:"Ternopil'",
                            23:"Transcarpathia",
                            24:"Vinnytsya",
                            25:"Volyn", 
                            26:"Zaporizhzhya",
                            27:"Zhytomyr" 
                        }
province_id_second = {       1:22,
                            2:24,
                            3:23,
                            4:25,
                            5:3,
                            6:4,
                            7:8,
                            8:19,
                            9:20,
                            10:21,
                            11:9,
                            12:26,
                            13:10,
                            14:11,
                            15:12,
                            16:13,
                            17:14,
                            18:15,
                            19:16,
                            20:27,
                            21:17,
                            22:18,
                            23:6,
                            24:1,
                            25:2, 
                            26:7, 
                            27:5 
                        }

directory = "data"
delete_data(directory)
for i in range (1,28):
    file_name = download_data(i, province_id_first[i], directory)
    
df = read_to_frame(province_id_first, province_id_second, directory)
print (df[:10])
df = df.sort_values(["id", "year"])


"""
 VHI <40 – стресові умови;
 VHI > 60 – сприятливі умови;
 VHI < 15 – посуха, інтенсивність якої від середньої до надзвичайної; 
 VHI < 35 – посуха, інтенсивність якої від помірної до надзвичайної. 
Выборка по месяцам за конкретный год мин и макс 
перечень недель - значение года, в который среднее знач vhi - макс

"""
"""
df1 = pd.DataFrame (columns = ['year', 'min', 'max'])
for i in (df['year']).unique():
    new_line={'year':str(i), 'min': df.loc[df.year==i]['VHI'].min(), 'max': df.loc[df.year==i]['VHI'].max()}
    df1 = df1.append (new_line, ignore_index=True)
    
    
    
df3 = pd.DataFrame(columns = ['week', 'year_max_VHI'])
for i in df['week'].unique(): #для каждой недели
    temp_df = pd.DataFrame(columns = ['year', 'VHI_mean'])
    for year in df['year'].unique():
        if any(df.loc[df.year==year].week==i):
            vhi_mean = df.loc[(df.week==i) & (df.year==year) ]['VHI'].mean()
            line = {'year': str(year), 'VHI_mean':vhi_mean}
            temp_df = temp_df.append(line, ignore_index=True)
    max_mean_VHI = temp_df['VHI_mean'].max()
    year_max_VHI = temp_df.loc[temp_df.VHI_mean == max_mean_VHI]['year'].values[0]
    new_line={'week':str(i), 'year_max_VHI': year_max_VHI}
    df3 = df3.append (new_line, ignore_index=True)
       
df1 = pd.DataFrame (columns = ['year', 'min', 'max'])
for i in (df['year']).unique():
    new_line={'year':str(i), 'min': df.loc[df.year==i]['VHI'].min(), 'max': df.loc[df.year==i]['VHI'].max()}
    df1 = df1.append (new_line, ignore_index=True)
"""