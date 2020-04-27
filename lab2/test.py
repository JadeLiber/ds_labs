import spyre.server
import datetime
import os
import pandas as pd
import matplotlib.pyplot as plt 

class VHIApp(spyre.server.App):
    title = "VHI analysis"
    inputs = [{ "type":'dropdown',
               "label": 'Province',
               "options" : [{"label":"Cherkasy",         "value": 22},
                            {"label":"Chernihiv",        "value": 24},
                            {"label":"Chernivtsi",       "value": 23},
                            {"label":"Crimea",           "value": 25},
                            {"label":"Dnipropetrovs'k",  "value": 3},
                            {"label":"Donets'k",         "value": 4},
                            {"label":"Ivano-Frankivs'k", "value": 8},
                            {"label":"Kharkiv",          "value": 19},
                            {"label":"Kherson",          "value": 20},
                            {"label":"Khmel'nyts'kyy",   "value": 21},
                            {"label":"Kiev",             "value": 9},
                            {"label":"Kiev City",        "value": 26},
                            {"label":"Kirovohrad",       "value": 10},
                            {"label":"Luhans'k",         "value": 11},
                            {"label":"L'viv",            "value": 12},
                            {"label":"Mykolayiv",        "value": 13},
                            {"label":"Odessa",           "value": 14},
                            {"label":"Poltava",          "value": 15},
                            {"label":"Rivne",            "value": 16},
                            {"label":"Sevastopol'",      "value": 27},
                            {"label":"Sumy",             "value": 17},
                            {"label":"Ternopil'",        "value": 18},
                            {"label":"Transcarpathia",   "value": 6},
                            {"label":"Vinnytsya",        "value": 1},
                            {"label":"Volyn",            "value": 2},
                            {"label":"Zaporizhzhya",     "value": 7},
                            {"label":"Zhytomyr",         "value": 5}],
                "key": 'province'},
    
                {"type":'dropdown',
                 "label": 'Index',
                 "options" : [{"label":"VHI", "value":"VHI"},
                              {"label":"TCI","value":"TCI"},
                              {"label":"VCI","value":"VCI"}],
                 "key": 'index'
                 },
                 
                {"type": 'dropdown',
                  "label": "Year",
                  "options": [{'label': str(i), 'value': i} for i in range(1982, int(datetime.datetime.now().strftime("%Y"))+1)],
                  'key': 'year',
                  'value': '1982'},
                  
                {"type": 'text',
                  "label": "first week",
                  'key': 'first_week',
                  'value': '1'},
                   
                {"type": 'text',
                  "label": "last week",
                  'key': 'last_week',
                  'value': '52'
                  }]

    controls = [
        {
            "type": "button",
            "id": "update_data",
            "label": "Show data"
        }]

    tabs = ["Plot", "Table"]

    outputs = [
        {
            "type": "plot",
            "id": "plot",
            "control_id": "update_data",
            "tab": "Plot",
            "on_page_load": True
        },
        {
            "type": "table",
            "id": "mean_table",
            "control_id": "update_data",
            "tab": "Table"
        }
        ]
    def __init__(self):
        df = pd.DataFrame(columns=['year','week', 'SMN','SMT','VCI','TCI','VHI','province'])
        colnames=['year','week', 'SMN','SMT','VCI','TCI','VHI','province']
        for i in range (1, 28):
            file_name = f"data\_id_{i}.csv"
            temp = pd.read_csv(file_name, sep=",", names = colnames, index_col=False, header=None)
            temp['province']=i
            temp = temp[temp.VHI!=-1]
            df = df.append(temp, ignore_index=True)
        self.df = df
    def getData(self, params):      
        province = params['province']
        year = params['year']
        first_week = int(params['first_week'])
        last_week =int( params['last_week'])
        index = params ['index']
        df = self.df
        df['year'] = df['year'].astype(str)
        df['province'] = df['province'].astype(str)
        df = df[(df.year==year)&(df.province == province)]
        df['week'] = df['week'].astype(int)
        df = df[(df.week>=first_week)& (df.week<=last_week)]   
        return df[['year','week',index]]
     
    def getPlot(self, params):
        index = params['index']
        df = self.getData(params) 
        df1 = df[[index]]
        return df1.set_index(df['week']).plot()

    

app = VHIApp()
app.launch(port = 2020)