import os
# import eel
import requests
import traceback
from appJar import gui
from datetime import datetime
import pandas as pd
import xlsxwriter
from openpyxl.workbook import Workbook as wb
import json
import ast
import numpy as np
from sklearn.preprocessing import StandardScaler
from keras.models import Sequential
from keras.layers import LSTM, Dense, Bidirectional, Dropout
import tensorflow as tf
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.model_selection import cross_val_score
from tensorflow import keras
from tensorflow.keras.optimizers import Adam
import xml.etree.ElementTree as ET 
import warnings
warnings.filterwarnings("ignore")
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1' 

def standardScaling(df):
    scaler = StandardScaler().fit(df.values)
    transformed_dataset = scaler.transform(df.values)
    transformed_df = pd.DataFrame(data=transformed_dataset, index=df.index)
    # transformed_df.head() 
    number_of_rows = df.values.shape[0]
    # print(number_of_rows)
    window_length = number_of_rows -1
    # print(window_length)
    number_of_features = df.values.shape[1]
    X = np.empty([ number_of_rows - window_length, window_length, number_of_features], dtype=float)
    y = np.empty([ number_of_rows - window_length, number_of_features], dtype=float)
    for i in range(0, number_of_rows-window_length):
        X[i] = transformed_df.iloc[i : i+window_length, 0 : number_of_features]
        y[i] = transformed_df.iloc[i+window_length : i+window_length+1, 0 : number_of_features]

    print(X.shape)
    print(y.shape)
    model = Sequential()
    model.add(Bidirectional(LSTM(240, input_shape = (window_length, number_of_features), return_sequences = True)))
    model.add(Dropout(0.2))
    model.add(Bidirectional(LSTM(240, input_shape = (window_length, number_of_features), return_sequences = True)))
    model.add(Dropout(0.2))
    model.add(Bidirectional(LSTM(240, input_shape = (window_length, number_of_features), return_sequences = True)))
    model.add(Bidirectional(LSTM(240, input_shape = (window_length, number_of_features), return_sequences = False)))
    model.add(Dense(59))
    model.add(Dense(number_of_features))
    model.compile(optimizer=Adam(learning_rate=0.0001), loss ='mse', metrics=['accuracy'])
    model.fit(x=X, y=y, batch_size=100, epochs=30, verbose=2)

    to_predict = df.tail(8)
    to_predict.drop([to_predict.index[-1]],axis=0, inplace=True)
    prediction = df.tail(1)
    to_predict = np.array(to_predict)

    scaled_to_predict = scaler.transform(to_predict)
    y_pred = model.predict(np.array([scaled_to_predict]))
    print('The predicted numbers in the last lottery game are:', scaler.inverse_transform(y_pred).astype(int)[0])
    prediction = np.array(prediction)
    print('The actual numbers in the last lottery game were:', prediction[0])
    return(prediction)


def randomClass(df):
    try:
        window_size = 2
        X = []
        y = []
        for i in range(window_size, len(df)):
            X.append(df.iloc[i-window_size:i].values.flatten())
            y.append(df.iloc[i].values)
        # Predicion 0
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.233, random_state=0)
        model = RandomForestClassifier(n_estimators=df.shape[0], random_state=333)
        model.fit(X_train, y_train)
        latest_data = df.iloc[-window_size:].values.flatten().reshape(1, -1)
        prediction0 = model.predict(latest_data)
        print("prediction0 numbers:", prediction0[0])
        # Predicion 1
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.333, random_state=1)
        model = RandomForestClassifier(n_estimators=df.shape[0], random_state=888)
        model.fit(X_train, y_train)
        latest_data = df.iloc[-window_size:].values.flatten().reshape(1, -1)
        prediction1 = model.predict(latest_data)
        print("prediction1 numbers:", prediction1[0])
        # Predicion 2
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.333, random_state=8)
        model = RandomForestClassifier(n_estimators=df.shape[0], random_state=555)
        model.fit(X_train, y_train)
        latest_data = df.iloc[-window_size:].values.flatten().reshape(1, -1)
        prediction2 = model.predict(latest_data)
        print("prediction2 numbers:", prediction2[0])
        # Predicion 3
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.333, random_state=3)
        model = RandomForestClassifier(n_estimators=df.shape[0], random_state=1300)
        model.fit(X_train, y_train)
        latest_data = df.iloc[-window_size:].values.flatten().reshape(1, -1)
        prediction3 = model.predict(latest_data)
        print("prediction3 numbers:", prediction3[0])
        # Predicion 4
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.333, random_state=13)
        model = RandomForestClassifier(n_estimators=df.shape[0], random_state=2100)
        model.fit(X_train, y_train)
        latest_data = df.iloc[-window_size:].values.flatten().reshape(1, -1)
        prediction4 = model.predict(latest_data)
        print("prediction4 numbers:", prediction4[0])
    except:
        traceback.print_exc()
    t = list(prediction0[0]), list(prediction1[0]), list(prediction2[0]), list(prediction3[0]), list(prediction4[0])
    
    return(t)

def getMegamillions():
    global app
    try:
        directoryLoc = app.getEntry("selectLocation")
        
        if not directoryLoc:
            raise Exception
    except:
        app.errorBox("Need_Location", "YOU MUST SELECT A DIRECTORY TO EXPORT RESULTS", parent=None)
        
    #https://www.megamillions.com/Winning-Numbers/Previous-Drawings.aspx?pageNumber=1&pageSize=20&startDate=01/01/2020&endDate=01/18/2024
    baseLink = "https://www.megamillions.com/Winning-Numbers/Previous-Drawings.aspx?pageNumber=1&pageSize=200"
    sdate = app.getDatePicker("sd")
    edate = app.getDatePicker("ed")
    if sdate.month < 10:
        smonth = "0" + str(sdate.month)
    else:
        smonth = str(sdate.month)
    if sdate.day < 10:
        sday = "0" + str(sdate.day)
    else:
        sday = str(sdate.day)

    if edate.month < 10:
        emonth = "0" + str(edate.month)
    else:
        emonth = str(edate.month)
    if edate.day < 10:
        eday = "0" + str(edate.day)
    else:
        eday = str(edate.day)

    startDate = str(smonth) + "/" + str(sday) + "/" + str(sdate.year)
    endDate = str(emonth) + "/" + str(eday) + "/" + str(edate.year)
    # startDate = "&startDate=" + str(smonth) + "/" + str(sday) + "/" + str(sdate.year)
    # endDate = "&endDate=" + str(emonth) + "/" + str(eday) + "/" + str(edate.year)
    url = baseLink + startDate + endDate
    # app.infoBox("damd", url)
    # /https://www.megamillions.com/Winning-Numbers/Previous-Drawings.aspx?pageNumber=1&pageSize=20&startDate=01/01/2020&endDate=01/18/2024

    payload = {
        "endDate": endDate,
        "pageNumber":"1",
        "pageSize": "2000",
        "startDate":startDate,
    }

    try:                    #https://www.megamillions.com/cmspages/utilservice.asmx/GetLatestDrawData   https://www.megamillions.com/cmspages/utilservice.asmx/GetDrawingPagingData
        res = requests.post("https://www.megamillions.com/cmspages/utilservice.asmx/GetDrawingPagingData", data=payload)
        tree = ET.fromstring(res.text)
        f = json.loads(tree.text)
        l = []
        for row in f['DrawingData']:
            date = row['PlayDate'].split('T')[0]
            n1 = row['N1']
            n2 = row['N2']
            n3 = row['N3']
            n4 = row['N4']
            n5 = row['N5']
            mb = row['MBall']
            l.append([date, n1, n2, n3, n4, n5, mb])

        wbook = wb()
        page = wbook.active
        page.title = 'mmillions'
        for r in l:
            page.append(r)
 
        df = pd.DataFrame(l, index=None)
        dfForSheet = df.set_axis(['A', 'B', 'C', 'D', 'E', 'F', 'G'], axis=1)
        dfOnlyNumbers = dfForSheet.drop(columns=['A'])
        dfOnlyNumbers = dfOnlyNumbers.set_axis(['A', 'B', 'C', 'D', 'E', 'F'], axis=1)
        x =  dfOnlyNumbers.groupby(['A','B','C','D','E']).size().div(len(dfOnlyNumbers))
        aProb = dfOnlyNumbers.groupby('A').size().div(len(dfOnlyNumbers))
        # bProb = df.groupby('B').size().div(len(df))
        # cProb = df.groupby('C').size().div(len(df))
        # dProb = df.groupby('D').size().div(len(df))
        # eProb = df.groupby('E').size().div(len(df))
        lnProb = dfOnlyNumbers.groupby('F').size().div(len(dfOnlyNumbers))
        topUnique = dfOnlyNumbers.describe()

        # df.to_excel(r'/home/dad/Documents/test.xlsx', index=True)
        sDat = startDate.replace("/", "-")
        eDat = endDate.replace("/", "-")
        t = datetime.now()
        timemark= str(t.minute) + str(t.second)
        
        saveFileName = directoryLoc + "/" + "MEGA_" + sDat + " _TO_" + eDat + "_" + timemark + ".xlsx" 
        try:
            writer = pd.ExcelWriter(saveFileName, engine='xlsxwriter')
        except:
            app.errorBox("FILE SEEMS TO BE ALREADY OPEN. CLOSE IT AND TRY AGAIN...")
            return
        # df.to_excel(writer,sheet_name='Validation',startrow=20, startcol=0) 
        dfForSheet.to_excel(writer, sheet_name='Sheet1',startrow=0, startcol=0)
        # addedPd.to_excel(writer, sheet_name='Sheet1',startrow=0, startcol=9)
        # addedLnPd.to_excel(writer, sheet_name='Sheet1',startrow=0, startcol=12)
        
        aProb.to_excel(writer, sheet_name='Sheet1',startrow=0, startcol=15) #
        # bProb.to_excel(writer, sheet_name='Sheet1',startrow=0, startcol=12)
        # cProb.to_excel(writer, sheet_name='Sheet1',startrow=0, startcol=15)
        # dProb.to_excel(writer, sheet_name='Sheet1',startrow=0, startcol=18)
        # eProb.to_excel(writer, sheet_name='Sheet1',startrow=0, startcol=21)
        lnProb.to_excel(writer, sheet_name='Sheet1',startrow=0, startcol=22)
        topUnique.to_excel(writer, sheet_name='Sheet1',startrow=0, startcol=25)
        
        # print(df)
        
        try:
            dfpre = dfOnlyNumbers.reset_index()
            dfforai = dfpre.drop(dfpre.columns[[0]], axis=1)

            fpredcs = randomClass(dfforai)
            d1 = pd.DataFrame(fpredcs[0])
            d2 = pd.DataFrame(fpredcs[1])
            d3 = pd.DataFrame(fpredcs[2])
            d4 = pd.DataFrame(fpredcs[3])
            d5 = pd.DataFrame(fpredcs[4])
            d1.T.to_excel(writer, sheet_name='Sheet1',startrow=7, startcol=26, header=False, index=False)
            d2.T.to_excel(writer, sheet_name='Sheet1',startrow=8, startcol=26, header=False, index=False)
            d3.T.to_excel(writer, sheet_name='Sheet1',startrow=9, startcol=26, header=False, index=False)
            d4.T.to_excel(writer, sheet_name='Sheet1',startrow=10, startcol=26, header=False, index=False)
            d5.T.to_excel(writer, sheet_name='Sheet1',startrow=11, startcol=26, header=False, index=False)



            fivePrediction = standardScaling(dfforai)
            d1 = pd.DataFrame(fivePrediction[0])
            # d2 = pd.DataFrame(fivePrediction[1])
            # d3 = pd.DataFrame(fivePrediction[2])
            # d4 = pd.DataFrame(fivePrediction[3])
            # d5 = pd.DataFrame(fivePrediction[4])
            d1.T.to_excel(writer, sheet_name='Sheet1',startrow=13, startcol=26, header=False, index=False)
            # d2.T.to_excel(writer, sheet_name='Sheet1',startrow=14, startcol=26, header=False, index=False)
            # d3.T.to_excel(writer, sheet_name='Sheet1',startrow=15, startcol=26, header=False, index=False)
            # d4.T.to_excel(writer, sheet_name='Sheet1',startrow=16, startcol=26, header=False, index=False)
            # d5.T.to_excel(writer, sheet_name='Sheet1',startrow=17, startcol=26, header=False, index=False)
            try:
                writer.close()
                os.startfile(saveFileName)
            except:
                app.errorbox("SOMETHING WENT WRONG.. UNABLE TO OPEN FILE")
        except:
            traceback.print_exc()
        
    except Exception as e:
        app.infoBox("shit", e)
        print(str(traceback.print_exc()))

    # try:
    #     res = requests.get(url, headers=headers)
    #     l = res.text
    #     l = l.split('View Winners')
    #     l.pop(-1)
    #     dict = {}
    #     for line in l:
    #         if "form method=" in line:
    #             p = line.split('<td>')
    #             dat = p[1].replace('</td>', '')
    #             dat = p[5].split('<a href="/winners/')
    #             try:
    #                 dat = dat[1].split('"')[0]
    #             except:
    #                 dat = dat[1].split('"')[0]
    #                 app.message(title = "INVALID DATES")
    #             numbs = p[2].replace('</td>', '')
    #             numbs = numbs.replace('-', '')
    #             ln = p[3].replace('</td>', '')
    #             allNumbers = numbs +  '  ' + ln
    #             allNs = allNumbers.split("  ")
    #             dict.update({dat:allNs})
    #         else:
    #             dat = line.split('winners/')
    #             dat = dat[1].split('"')[0]
    #             numbs = line.split('</td><td>')
    #             n = numbs[1]
    #             n = n.replace('-', '')
    #             ln = numbs[2]
    #             allNumbers = n +  '  ' + ln 
    #             allNs = allNumbers.split("  ")
    #             dict.update({dat:allNs})
                

    #     df = pd.DataFrame.from_dict(dict, orient = 'index')
    #     df1 = pd.DataFrame.from_dict(dict, orient = 'index')
    #     df1 =  df1.drop(df1.columns[-1],axis=1)
    #     df = df.set_axis(['A', 'B', 'C', 'D', 'E', 'F'], axis=1)
    #     ldf = df.drop(columns=['A', 'B', 'C', 'D', 'E'])
        
    #     # dfC= df.groupby(['A', 'B', 'C','D', 'E']).size()
    #     counterDict = {
    #         "1" : [],
    #         "2" : [],
    #         "3" : [],
    #         "4" : [],
    #         "5" : [],
    #         "6" : [],
    #         "7" : [],
    #         "8" : [],
    #         "9" : [],
    #         "10" : [],
    #         "11" : [],
    #         "12" : [],
    #         "13" : [],
    #         "14" : [],
    #         "15" : [],
    #         "16" : [],
    #         "17" : [],
    #         "18" : [],
    #         "19" : [],
    #         "20" : [],
    #         "21" : [],
    #         "22" : [],
    #         "23" : [],
    #         "24" : [],
    #         "25" : [],
    #         "26" : [],
    #         "27" : [],
    #         "28" : [],
    #         "29" : [],
    #         "30" : [],
    #         "31" : [],
    #         "32" : [],
    #         "33" : [],
    #         "34" : [],
    #         "35" : [],
    #         "36" : [],
    #         "37" : [],
    #         "38" : [],
    #         "39" : [],
    #         "40" : [],
    #         "41" : [],
    #         "42" : [],
    #         "43" : [],
    #         "44" : [],
    #         "45" : [],
    #         "46" : [],
    #         "47" : [],
    #         "48" : [],
    #     }
    #     counterLn = {
    #          "1" : [],
    #         "2" : [],
    #         "3" : [],
    #         "4" : [],
    #         "5" : [],
    #         "6" : [],
    #         "7" : [],
    #         "8" : [],
    #         "9" : [],
    #         "10" : [],
    #         "11" : [],
    #         "12" : [],
    #         "13" : [],
    #         "14" : [],
    #         "15" : [],
    #         "16" : [],
    #         "17" : [],
    #         "18" : [],
    #     }
    #     for column in df1:
    #         columnSeriesObj = df1[column]
    #         for key in counterDict.keys():
    #             listToCount = list(columnSeriesObj.values)
    #             x = listToCount.count(key)
    #             counterDict[key].append(x)
                
    #     for column in ldf:
    #         columnSeriesObj = ldf[column]
    #         for key in counterLn.keys():
    #             listToCount = list(columnSeriesObj.values)
    #             x = listToCount.count(key)
    #             counterLn[key].append(x)        
        
        
    #     addedCounterDict = {}
    #     for key in counterDict:
    #         v = sum(counterDict[key])
    #         addedCounterDict.update({key:v})
            
    #     addedPd = pd.DataFrame.from_dict(addedCounterDict, orient = 'index')  
    #     addedLnPd =  pd.DataFrame.from_dict(counterLn, orient = 'index')
    #     x =  df.groupby(['A','B','C','D','E']).size().div(len(df))
    #     aProb = df.groupby('A').size().div(len(df))
    #     # bProb = df.groupby('B').size().div(len(df))
    #     # cProb = df.groupby('C').size().div(len(df))
    #     # dProb = df.groupby('D').size().div(len(df))
    #     # eProb = df.groupby('E').size().div(len(df))
    #     lnProb = df.groupby('F').size().div(len(df))
    #     topUnique = df.describe()

    #     # df.to_excel(r'/home/dad/Documents/test.xlsx', index=True)
    #     sDat = startDate.replace("/", "-")
    #     eDat = endDate.replace("/", "-")
    #     t = datetime.now()
    #     timemark= str(t.minute) + str(t.second)
        
    #     saveFileName = directoryLoc + "/" + "LUCKY_" + sDat + " _TO_" + eDat + "_" + timemark + ".xlsx" 
    #     try:
    #         writer = pd.ExcelWriter(saveFileName, engine='xlsxwriter')
    #     except:
    #         app.errorBox("FILE SEEMS TO BE ALREADY OPEN. CLOSE IT AND TRY AGAIN...")
    #         return
    #     # df.to_excel(writer,sheet_name='Validation',startrow=20, startcol=0) 
    #     df.to_excel(writer, sheet_name='Sheet1',startrow=0, startcol=0)
    #     addedPd.to_excel(writer, sheet_name='Sheet1',startrow=0, startcol=9)
    #     addedLnPd.to_excel(writer, sheet_name='Sheet1',startrow=0, startcol=12)
        
    #     aProb.to_excel(writer, sheet_name='Sheet1',startrow=0, startcol=15) #
    #     # bProb.to_excel(writer, sheet_name='Sheet1',startrow=0, startcol=12)
    #     # cProb.to_excel(writer, sheet_name='Sheet1',startrow=0, startcol=15)
    #     # dProb.to_excel(writer, sheet_name='Sheet1',startrow=0, startcol=18)
    #     # eProb.to_excel(writer, sheet_name='Sheet1',startrow=0, startcol=21)
    #     lnProb.to_excel(writer, sheet_name='Sheet1',startrow=0, startcol=22)
    #     topUnique.to_excel(writer, sheet_name='Sheet1',startrow=0, startcol=25)
        
    #     # print(df)
        
    #     try:
    #         dfpre = df.reset_index()
    #         dfforai = dfpre.drop(dfpre.columns[[0]], axis=1)

    #         fpredcs = randomClass(dfforai)
    #         d1 = pd.DataFrame(fpredcs[0])
    #         d2 = pd.DataFrame(fpredcs[1])
    #         d3 = pd.DataFrame(fpredcs[2])
    #         d4 = pd.DataFrame(fpredcs[3])
    #         d5 = pd.DataFrame(fpredcs[4])
    #         d1.T.to_excel(writer, sheet_name='Sheet1',startrow=7, startcol=26, header=False, index=False)
    #         d2.T.to_excel(writer, sheet_name='Sheet1',startrow=8, startcol=26, header=False, index=False)
    #         d3.T.to_excel(writer, sheet_name='Sheet1',startrow=9, startcol=26, header=False, index=False)
    #         d4.T.to_excel(writer, sheet_name='Sheet1',startrow=10, startcol=26, header=False, index=False)
    #         d5.T.to_excel(writer, sheet_name='Sheet1',startrow=11, startcol=26, header=False, index=False)



    #         fivePrediction = standardScaling(dfforai)
    #         d1 = pd.DataFrame(fivePrediction[0])
    #         # d2 = pd.DataFrame(fivePrediction[1])
    #         # d3 = pd.DataFrame(fivePrediction[2])
    #         # d4 = pd.DataFrame(fivePrediction[3])
    #         # d5 = pd.DataFrame(fivePrediction[4])
    #         d1.T.to_excel(writer, sheet_name='Sheet1',startrow=13, startcol=26, header=False, index=False)
    #         # d2.T.to_excel(writer, sheet_name='Sheet1',startrow=14, startcol=26, header=False, index=False)
    #         # d3.T.to_excel(writer, sheet_name='Sheet1',startrow=15, startcol=26, header=False, index=False)
    #         # d4.T.to_excel(writer, sheet_name='Sheet1',startrow=16, startcol=26, header=False, index=False)
    #         # d5.T.to_excel(writer, sheet_name='Sheet1',startrow=17, startcol=26, header=False, index=False)
    #     except:
    #         traceback.print_exc()


    #     try:
    #         writer.close()
    #         os.startfile(saveFileName)
    #     except:
    #         app.errorbox("SOMETHING WENT WRONG.. UNABLE TO OPEN FILE")

    # except:
    #     traceback.print_exc()

def getLuckyForLifeNumbers():
    global app
    # lrl = "https://www.luckyforlife.us/ajax/getWinningNumbers?s=" 01/01/2023 "&e=" 01/21/2023
    try:
        directoryLoc = app.getEntry("selectLocation")
        if not directoryLoc:
            raise Exception
    except:
        app.errorBox("Need_Location", "YOU MUST SELECT A DIRECTORY TO EXPORT RESULTS", parent=None)
        return
    baseLink = "https://www.luckyforlife.us/ajax/getWinningNumbers?s="
    sdate = app.getDatePicker("sd")
    edate = app.getDatePicker("ed")
    if sdate.month < 10:
        smonth = "0" + str(sdate.month)
    else:
        smonth = str(sdate.month)
    if sdate.day < 10:
        sday = "0" + str(sdate.day)
    else:
        sday = str(sdate.day)

    if edate.month < 10:
        emonth = "0" + str(edate.month)
    else:
        emonth = str(edate.month)
    if edate.day < 10:
        eday = "0" + str(edate.day)
    else:
        eday = str(edate.day)

    startDate = str(smonth) + "/" + str(sday) + "/" + str(sdate.year)
    endDate = str(emonth) + "/" + str(eday) + "/" + str(edate.year)
    url = baseLink + startDate + "&e=" + endDate
    
    headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0",
                "Accept": "text/html, */*; q=0.01",
                "Accept-Language": "en-US,en;q=0.5",
                "Accept-Encoding": "gzip, deflate, br",
                "X-Requested-With": "XMLHttpRequest",
                "Host": "www.luckyforlife.us",
                "Connection": "keep-alive",
                "Referer": "https://www.luckyforlife.us/winning-numbers/",
            }

    try:
        res = requests.get(url, headers=headers)
        l = res.text
        l = l.split('View Winners')
        l.pop(-1)
        dict = {}
        for line in l:
            if "form method=" in line:
                p = line.split('<td>')
                dat = p[1].replace('</td>', '')
                dat = p[5].split('<a href="/winners/')
                try:
                    dat = dat[1].split('"')[0]
                except:
                    dat = dat[1].split('"')[0]
                    app.message(title = "INVALID DATES")
                numbs = p[2].replace('</td>', '')
                numbs = numbs.replace('-', '')
                ln = p[3].replace('</td>', '')
                allNumbers = numbs +  '  ' + ln
                allNs = allNumbers.split("  ")
                dict.update({dat:allNs})
            else:
                dat = line.split('winners/')
                dat = dat[1].split('"')[0]
                numbs = line.split('</td><td>')
                n = numbs[1]
                n = n.replace('-', '')
                ln = numbs[2]
                allNumbers = n +  '  ' + ln 
                allNs = allNumbers.split("  ")
                dict.update({dat:allNs})
                

        df = pd.DataFrame.from_dict(dict, orient = 'index')
        df1 = pd.DataFrame.from_dict(dict, orient = 'index')
        df1 =  df1.drop(df1.columns[-1],axis=1)
        df = df.set_axis(['A', 'B', 'C', 'D', 'E', 'F'], axis=1)
        ldf = df.drop(columns=['A', 'B', 'C', 'D', 'E'])
        
        # dfC= df.groupby(['A', 'B', 'C','D', 'E']).size()
        counterDict = {
            "1" : [],
            "2" : [],
            "3" : [],
            "4" : [],
            "5" : [],
            "6" : [],
            "7" : [],
            "8" : [],
            "9" : [],
            "10" : [],
            "11" : [],
            "12" : [],
            "13" : [],
            "14" : [],
            "15" : [],
            "16" : [],
            "17" : [],
            "18" : [],
            "19" : [],
            "20" : [],
            "21" : [],
            "22" : [],
            "23" : [],
            "24" : [],
            "25" : [],
            "26" : [],
            "27" : [],
            "28" : [],
            "29" : [],
            "30" : [],
            "31" : [],
            "32" : [],
            "33" : [],
            "34" : [],
            "35" : [],
            "36" : [],
            "37" : [],
            "38" : [],
            "39" : [],
            "40" : [],
            "41" : [],
            "42" : [],
            "43" : [],
            "44" : [],
            "45" : [],
            "46" : [],
            "47" : [],
            "48" : [],
        }
        counterLn = {
             "1" : [],
            "2" : [],
            "3" : [],
            "4" : [],
            "5" : [],
            "6" : [],
            "7" : [],
            "8" : [],
            "9" : [],
            "10" : [],
            "11" : [],
            "12" : [],
            "13" : [],
            "14" : [],
            "15" : [],
            "16" : [],
            "17" : [],
            "18" : [],
        }
        for column in df1:
            columnSeriesObj = df1[column]
            for key in counterDict.keys():
                listToCount = list(columnSeriesObj.values)
                x = listToCount.count(key)
                counterDict[key].append(x)
                
        for column in ldf:
            columnSeriesObj = ldf[column]
            for key in counterLn.keys():
                listToCount = list(columnSeriesObj.values)
                x = listToCount.count(key)
                counterLn[key].append(x)        
        
        
        addedCounterDict = {}
        for key in counterDict:
            v = sum(counterDict[key])
            addedCounterDict.update({key:v})
            
        addedPd = pd.DataFrame.from_dict(addedCounterDict, orient = 'index')  
        addedLnPd =  pd.DataFrame.from_dict(counterLn, orient = 'index')
        x =  df.groupby(['A','B','C','D','E']).size().div(len(df))
        aProb = df.groupby('A').size().div(len(df))
        # bProb = df.groupby('B').size().div(len(df))
        # cProb = df.groupby('C').size().div(len(df))
        # dProb = df.groupby('D').size().div(len(df))
        # eProb = df.groupby('E').size().div(len(df))
        lnProb = df.groupby('F').size().div(len(df))
        topUnique = df.describe()

        # df.to_excel(r'/home/dad/Documents/test.xlsx', index=True)
        sDat = startDate.replace("/", "-")
        eDat = endDate.replace("/", "-")
        t = datetime.now()
        timemark= str(t.minute) + str(t.second)
        
        saveFileName = directoryLoc + "/" + "LUCKY_" + sDat + " _TO_" + eDat + "_" + timemark + ".xlsx" 
        try:
            writer = pd.ExcelWriter(saveFileName, engine='xlsxwriter')
        except:
            app.errorBox("FILE SEEMS TO BE ALREADY OPEN. CLOSE IT AND TRY AGAIN...")
            return
        # df.to_excel(writer,sheet_name='Validation',startrow=20, startcol=0) 
        df.to_excel(writer, sheet_name='Sheet1',startrow=0, startcol=0)
        addedPd.to_excel(writer, sheet_name='Sheet1',startrow=0, startcol=9)
        addedLnPd.to_excel(writer, sheet_name='Sheet1',startrow=0, startcol=12)
        
        aProb.to_excel(writer, sheet_name='Sheet1',startrow=0, startcol=15) #
        # bProb.to_excel(writer, sheet_name='Sheet1',startrow=0, startcol=12)
        # cProb.to_excel(writer, sheet_name='Sheet1',startrow=0, startcol=15)
        # dProb.to_excel(writer, sheet_name='Sheet1',startrow=0, startcol=18)
        # eProb.to_excel(writer, sheet_name='Sheet1',startrow=0, startcol=21)
        lnProb.to_excel(writer, sheet_name='Sheet1',startrow=0, startcol=22)
        topUnique.to_excel(writer, sheet_name='Sheet1',startrow=0, startcol=25)
        
        # print(df)
        
        try:
            dfpre = df.reset_index()
            dfforai = dfpre.drop(dfpre.columns[[0]], axis=1)

            fpredcs = randomClass(dfforai)
            d1 = pd.DataFrame(fpredcs[0])
            d2 = pd.DataFrame(fpredcs[1])
            d3 = pd.DataFrame(fpredcs[2])
            d4 = pd.DataFrame(fpredcs[3])
            d5 = pd.DataFrame(fpredcs[4])
            d1.T.to_excel(writer, sheet_name='Sheet1',startrow=7, startcol=26, header=False, index=False)
            d2.T.to_excel(writer, sheet_name='Sheet1',startrow=8, startcol=26, header=False, index=False)
            d3.T.to_excel(writer, sheet_name='Sheet1',startrow=9, startcol=26, header=False, index=False)
            d4.T.to_excel(writer, sheet_name='Sheet1',startrow=10, startcol=26, header=False, index=False)
            d5.T.to_excel(writer, sheet_name='Sheet1',startrow=11, startcol=26, header=False, index=False)



            fivePrediction = standardScaling(dfforai)
            d1 = pd.DataFrame(fivePrediction[0])
            # d2 = pd.DataFrame(fivePrediction[1])
            # d3 = pd.DataFrame(fivePrediction[2])
            # d4 = pd.DataFrame(fivePrediction[3])
            # d5 = pd.DataFrame(fivePrediction[4])
            d1.T.to_excel(writer, sheet_name='Sheet1',startrow=13, startcol=26, header=False, index=False)
            # d2.T.to_excel(writer, sheet_name='Sheet1',startrow=14, startcol=26, header=False, index=False)
            # d3.T.to_excel(writer, sheet_name='Sheet1',startrow=15, startcol=26, header=False, index=False)
            # d4.T.to_excel(writer, sheet_name='Sheet1',startrow=16, startcol=26, header=False, index=False)
            # d5.T.to_excel(writer, sheet_name='Sheet1',startrow=17, startcol=26, header=False, index=False)
        except:
            traceback.print_exc()


        try:
            writer.close()
            os.startfile(saveFileName)
        except:
            app.errorbox("SOMETHING WENT WRONG.. UNABLE TO OPEN FILE")

    except:
        traceback.print_exc()


if __name__ == '__main__':
    # lrl = Lot("https://www.luckyforlife.us/ajax/getWinningNumbers?s=" 01/01/2023 "&e=" 01/21/2023
    app = gui("GET LUCKY", "600x200")
    twoyearsago = datetime.today().year - 5
    thisyear = datetime.today().year
    month = datetime.today().month
    day = datetime.today().day
    app.addDirectoryEntry("selectLocation", 1,1,2,2)  
    app.setEntry("selectLocation", "C:/Users/Gus Bustillos/Desktop/lot") #.setEntry(title, text, callFunction=True)
    app.addDatePicker("sd", 3,1)
    app.setDatePickerRange("sd", twoyearsago, thisyear)
    dateToUse="01/01/"+str(twoyearsago)
    dtset = datetime.fromisoformat('2019-01-01T01:00:00')
    app.setDatePicker("sd", date=dtset)
    app.addDatePicker("ed",3,3)
    app.setDatePickerRange("ed", twoyearsago, thisyear)
    app.setDatePicker("ed")
    app.addButton("GET-L", getLuckyForLifeNumbers)
    app.addButton("GET-M", getMegamillions) 
    app.go()