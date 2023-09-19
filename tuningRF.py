# -*- coding: utf-8 -*-
"""
Created on Wed May 17 13:14:13 2023

@author: Premananda Setyo
"""

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import time
import pickle
from imblearn.under_sampling import RandomUnderSampler
from imblearn.under_sampling import NearMiss


def nearMissUnderSampler(x,y):
    nm1 = NearMiss(version=1, n_jobs=(6))
    x_res, y_res = nm1.fit_resample(x, y)
    return x_res, y_res

def randomUnderSampler(x,y):
    rus = RandomUnderSampler(random_state=233759)
    X_resampled, y_resampled = rus.fit_resample(x, y)
    return X_resampled, y_resampled

def readDf(pathR):
    df=pd.read_excel(pathR)
    df=df.dropna()
    print(df.shape)
    return df

def writeNewDF(df,warna):
    df=df.dropna()
    if warna=='HSV':
        df.to_csv('D:\\Skripsi\\LabelingProgram\\label\\Iter_7\\Total\\TotalKotaHSV.csv')
    elif warna == 'RGB':
        df.to_csv('D:\\Skripsi\\LabelingProgram\\label\\Iter_7\\Kota\\Total\\TotalKotaRGB.csv')
        
def feature(modelWarna,df):
    if modelWarna=='RGB':
        x = df[['R1','G1','B1', 'Proporsi1','R2','G2','B2','Proporsi2','R3','G3','B3','Proporsi3','stdev','min_R',
                                                    'min_G','min_B','max_R','max_G','max_B',
                                                    'dissimilarity_0_LL','correlation_0_LL','homogeneity_0_LL','contrast_0_LL','energy_0_LL',
                                                    'dissimilarity_45_LL','correlation_45_LL','homogeneity_45_LL','contrast_45_LL','energy_45_LL',
                                                    'dissimilarity_90_LL','correlation_90_LL','homogeneity_90_LL','contrast_90_LL','energy_90_LL',
                                                    'dissimilarity_135_LL','correlation_135_LL','homogeneity_135_LL','contrast_135_LL','energy_135_LL',
                                                    'dissimilarity_180_LL','correlation_180_LL','homogeneity_180_LL','contrast_180_LL','energy_180_LL',
                                                    'dissimilarity_0_LH','correlation_0_LH','homogeneity_0_LH','contrast_0_LH','energy_0_LH',
                                                    'dissimilarity_45_LH','correlation_45_LH','homogeneity_45_LH','contrast_45_LH','energy_45_LH',
                                                    'dissimilarity_90_LH','correlation_90_LH','homogeneity_90_LH','contrast_90_LH','energy_90_LH',
                                                    'dissimilarity_135_LH','correlation_135_LH','homogeneity_135_LH','contrast_135_LH','energy_135_LH',
                                                    'dissimilarity_180_LH','correlation_180_LH','homogeneity_180_LH','contrast_180_LH','energy_180_LH',
                                                    'dissimilarity_0_HL','correlation_0_HL','homogeneity_0_HL','contrast_0_HL','energy_0_HL',
                                                    'dissimilarity_45_HL','correlation_45_HL','homogeneity_45_HL','contrast_45_HL','energy_45_HL',
                                                    'dissimilarity_90_HL','correlation_90_HL','homogeneity_90_HL','contrast_90_HL','energy_90_HL',
                                                    'dissimilarity_135_HL','correlation_135_HL','homogeneity_135_HL','contrast_135_HL','energy_135_HL',
                                                    'dissimilarity_180_HL','correlation_180_HL','homogeneity_180_HL','contrast_180_HL','energy_180_HL',
                                                    'dissimilarity_0_HL','correlation_0_HL','homogeneity_0_HL','contrast_0_HL','energy_0_HL',
                                                    'dissimilarity_45_HH','correlation_45_HH','homogeneity_45_HH','contrast_45_HH','energy_45_HH',
                                                    'dissimilarity_90_HH','correlation_90_HH','homogeneity_90_HH','contrast_90_HH','energy_90_HH',
                                                    'dissimilarity_135_HH','correlation_135_HH','homogeneity_135_HH','contrast_135_HH','energy_135_HH',
                                                    'dissimilarity_180_HH','correlation_180_HH','homogeneity_180_HH','contrast_180_HH','energy_180_HH']]
    elif modelWarna=='HSV':
        x=df[['H1','S1','V1', 'Proporsi1','H2','S2','V2','Proporsi2','H3','S3','V3','Proporsi3','stdev','min_H',
                                                            'min_S','min_V','max_H','max_S','max_V',
                                                            'dissimilarity_0_LL','correlation_0_LL','homogeneity_0_LL','contrast_0_LL','energy_0_LL',
                                                            'dissimilarity_45_LL','correlation_45_LL','homogeneity_45_LL','contrast_45_LL','energy_45_LL',
                                                            'dissimilarity_90_LL','correlation_90_LL','homogeneity_90_LL','contrast_90_LL','energy_90_LL',
                                                            'dissimilarity_135_LL','correlation_135_LL','homogeneity_135_LL','contrast_135_LL','energy_135_LL',
                                                            'dissimilarity_180_LL','correlation_180_LL','homogeneity_180_LL','contrast_180_LL','energy_180_LL',
                                                            'dissimilarity_0_LH','correlation_0_LH','homogeneity_0_LH','contrast_0_LH','energy_0_LH',
                                                            'dissimilarity_45_LH','correlation_45_LH','homogeneity_45_LH','contrast_45_LH','energy_45_LH',
                                                            'dissimilarity_90_LH','correlation_90_LH','homogeneity_90_LH','contrast_90_LH','energy_90_LH',
                                                            'dissimilarity_135_LH','correlation_135_LH','homogeneity_135_LH','contrast_135_LH','energy_135_LH',
                                                            'dissimilarity_180_LH','correlation_180_LH','homogeneity_180_LH','contrast_180_LH','energy_180_LH',
                                                            'dissimilarity_0_HL','correlation_0_HL','homogeneity_0_HL','contrast_0_HL','energy_0_HL',
                                                            'dissimilarity_45_HL','correlation_45_HL','homogeneity_45_HL','contrast_45_HL','energy_45_HL',
                                                            'dissimilarity_90_HL','correlation_90_HL','homogeneity_90_HL','contrast_90_HL','energy_90_HL',
                                                            'dissimilarity_135_HL','correlation_135_HL','homogeneity_135_HL','contrast_135_HL','energy_135_HL',
                                                            'dissimilarity_180_HL','correlation_180_HL','homogeneity_180_HL','contrast_180_HL','energy_180_HL',
                                                            'dissimilarity_0_HH','correlation_0_HH','homogeneity_0_HH','contrast_0_HH','energy_0_HH',
                                                            'dissimilarity_45_HH','correlation_45_HH','homogeneity_45_HH','contrast_45_HH','energy_45_HH',
                                                            'dissimilarity_90_HH','correlation_90_HH','homogeneity_90_HH','contrast_90_HH','energy_90_HH',
                                                            'dissimilarity_135_HH','correlation_135_HH','homogeneity_135_HH','contrast_135_HH','energy_135_HH',
                                                            'dissimilarity_180_HH','correlation_180_HH','homogeneity_180_HH','contrast_180_HH','energy_180_HH']]
        
    y = df['LabelZona']
    return x, y

def trainTestSplit(x, y, ts=0.7):
    x_train, x_test, y_train, y_test = train_test_split(x, y, train_size=ts, random_state=(110647760))
    return x_train, x_test, y_train, y_test

def time_convert(sec):
  mins = sec // 60
  sec = sec % 60
  hours = mins // 60
  mins = mins % 60
  elapsed_time="{0}:{1}:{2}".format(int(hours),int(mins),sec)
  print(elapsed_time)
  return elapsed_time

def tuningRFNumTrees(x_train, x_test, y_train, y_test):
    res_metric=[]
    column=['num_tree','accuracy','precision','recall','f1-score','support','time']
    for n in range(100,1201,100):
        metric=[]
        print(n)
        start_time=time.time()
        RF_model = RandomForestClassifier(n_estimators=n, random_state=13785960)
        

        RF_model.fit(x_train, y_train)
        

        y_pred = RF_model.predict(x_test)
        
        stop_time=time.time()
        elapsed_time=stop_time-start_time
        runtime=time_convert(elapsed_time)
        
        
        rep=classification_report(y_test, y_pred,output_dict=True)

        metric.append(n)
        metric.append(rep['accuracy'])
        metric.append(rep['weighted avg']['precision'])
        metric.append(rep['weighted avg']['recall'])
        metric.append(rep['weighted avg']['f1-score'])
        metric.append(rep['weighted avg']['support'])
        metric.append(runtime)
        
        print(rep['accuracy'])
      
        confusion = confusion_matrix(y_test, y_pred)
        print('Confusion Matrix\n')
        print(confusion)
        res_metric.append(metric)


    df=pd.DataFrame(data=res_metric,columns=column)
    df.to_excel('D:\\Skripsi\\DownloadGambar\\CitraNew\\Eval\\Iter 2\\Kota\\RGB\\RFNumTrees.xlsx')

def tuningRFMaxDepth(x_train, x_test, y_train, y_test, nTree):
    res_metric=[]
    column=['num_tree','accuracy','precision','recall','f1-score','support','time']
    for n in range(5,51,5):
        metric=[]
        print(n)
        start_time=time.time()
        RF_model = RandomForestClassifier(n_estimators=nTree, max_depth=(n), random_state=13785960)
        

        RF_model.fit(x_train, y_train)
        

        y_pred = RF_model.predict(x_test)
        
        stop_time=time.time()
        elapsed_time=stop_time-start_time
        runtime=time_convert(elapsed_time)
        
        
        rep=classification_report(y_test, y_pred,output_dict=True)

        metric.append(n)
        metric.append(rep['accuracy'])
        metric.append(rep['weighted avg']['precision'])
        metric.append(rep['weighted avg']['recall'])
        metric.append(rep['weighted avg']['f1-score'])
        metric.append(rep['weighted avg']['support'])
        metric.append(runtime)
        
        print(rep['accuracy'])
      
        confusion = confusion_matrix(y_test, y_pred)
        print('Confusion Matrix\n')
        print(confusion)
        res_metric.append(metric)


    df=pd.DataFrame(data=res_metric,columns=column)
    df.to_excel('D:\\Skripsi\\DownloadGambar\\CitraNew\\Eval\\Iter 2\\Kota\\RGB\\RFMaxDepth.xlsx')

def tuningRFCrit(x_train, x_test, y_train, y_test, nTree, maxD):
    res_metric=[]
    column=['num_tree','accuracy','precision','recall','f1-score','support','time']
    crit=['gini','entropy']
    for n in crit:
        metric=[]
        print(n)
        start_time=time.time()
        RF_model = RandomForestClassifier(n_estimators=nTree, max_depth=maxD, criterion=n ,random_state=13785960)
        

        RF_model.fit(x_train, y_train)
        

        y_pred = RF_model.predict(x_test)
        
        stop_time=time.time()
        elapsed_time=stop_time-start_time
        runtime=time_convert(elapsed_time)
        
        
        rep=classification_report(y_test, y_pred,output_dict=True)

        metric.append(n)
        metric.append(rep['accuracy'])
        metric.append(rep['weighted avg']['precision'])
        metric.append(rep['weighted avg']['recall'])
        metric.append(rep['weighted avg']['f1-score'])
        metric.append(rep['weighted avg']['support'])
        metric.append(runtime)
        
        print(rep['accuracy'])
      
        confusion = confusion_matrix(y_test, y_pred)
        print('Confusion Matrix\n')
        print(confusion)
        res_metric.append(metric)


    df=pd.DataFrame(data=res_metric,columns=column)
    df.to_excel('D:\\Skripsi\\DownloadGambar\\CitraNew\\Eval\\Iter 2\\Kota\\RGB\\RFCrit.xlsx')


def tuningRFMinSampleLeaf(x_train, x_test, y_train, y_test, nTree, maxD, crit):
    res_metric=[]
    column=['num_tree','accuracy','precision','recall','f1-score','support','time']
    minS=[2, 4, 6, 8]
    for n in minS:
        metric=[]
        print(n)
        start_time=time.time()
        RF_model = RandomForestClassifier(n_estimators=nTree, max_depth=maxD, criterion=crit, min_samples_leaf=n, random_state=13785960)
        

        RF_model.fit(x_train, y_train)
        

        y_pred = RF_model.predict(x_test)
        
        stop_time=time.time()
        elapsed_time=stop_time-start_time
        runtime=time_convert(elapsed_time)
        
        
        rep=classification_report(y_test, y_pred,output_dict=True)

        metric.append(n)
        metric.append(rep['accuracy'])
        metric.append(rep['weighted avg']['precision'])
        metric.append(rep['weighted avg']['recall'])
        metric.append(rep['weighted avg']['f1-score'])
        metric.append(rep['weighted avg']['support'])
        metric.append(runtime)
        
        print(rep['accuracy'])
      
        confusion = confusion_matrix(y_test, y_pred)
        print('Confusion Matrix\n')
        print(confusion)
        res_metric.append(metric)
        
        # y_pred = RF_model.predict(x_train)
        # rep=classification_report(y_train, y_pred)
        # print(rep, n)
        # confusion = confusion_matrix(y_train, y_pred)
        # print('Confusion Matrix Train\n')
        # print(confusion)

        # y_pred = RF_model.predict(x_test)
        # rep=classification_report(y_test, y_pred)
        # print(rep, n)
        # confusion = confusion_matrix(y_test, y_pred)
        # print('Confusion Matrix Test\n')
        # print(confusion)


    df=pd.DataFrame(data=res_metric,columns=column)
    df.to_excel('D:\\Skripsi\\DownloadGambar\\CitraNew\\Eval\\Iter 2\\Kota\\RGB\\RFMinSampleLeaf.xlsx')

def save_model(x_train, x_test, y_train, y_test, nTree, maxD, crit, minSL):
    RF_model = RandomForestClassifier(n_estimators=nTree, max_depth=maxD, criterion=crit, min_samples_leaf=minSL,  random_state=13785960)
    RF_model.fit(x_train, y_train)
    y_pred = RF_model.predict(x_test)
    print(classification_report(y_test, y_pred))
    filename='rf_kota_oversampling.pkl'
    with open("rf_kota_oversampling.pkl", "wb") as file:
        pickle.dump(RF_model, file)
        
        
        


# Kota HSV
df=readDf('D:\\Skripsi\\LabelingProgram\\label\\Iter_7\\Kota\\Total\\TotalHSV.xlsx')
# Kab HSV
# df=readDf('D:\\Skripsi\\LabelingProgram\\label\\Iter_7\\Total\\TotalRGB.xlsx')
# writeNewDF(df,'HSV')
x,y=feature('HSV', df)
# Random Undersapling
# x,y=randomUnderSampler(x,y)
# Nearmiss undersampling
# x,y=nearMissUnderSampler(x,y)

x_train, x_test, y_train, y_test=trainTestSplit(x, y)


# tuningRFNumTrees(x_train, x_test, y_train, y_test)
# tuningRFMaxDepth(x_train, x_test, y_train, y_test, 600)
# tuningRFCrit(x_train, x_test, y_train, y_test, 600, 25)
# tuningRFMinSampleLeaf(x_train, x_test, y_train, y_test, 600, 25, 'entropy')

# tuningRFMinSampleLeaf(x_train, x_test, y_train, y_test, 900, 30, 'gini')
# tuningRFMinSampleLeaf(x_train, x_test, y_train, y_test, 800, 40, 'entropy')
tuningRFMinSampleLeaf(x_train, x_test, y_train, y_test, 600, 25, 'entropy')

# Model Kabupaten
# save_model(x_train, x_test, y_train, y_test, 900, 30, 'gini', 8)
# Model Kota
# save_model(x_train, x_test, y_train, y_test, 800, 40, 'entropy', 8)

# Model Kota
# RF_model = RandomForestClassifier(n_estimators=800, max_depth=(40), criterion='entropy', min_samples_leaf=8,  random_state=13785960)
# Model Kab
# RF_model = RandomForestClassifier(n_estimators=900, max_depth=(30), criterion='gini', min_samples_leaf=8,  random_state=13785960)

# Model Kab RGB
# RF_model = RandomForestClassifier(n_estimators=1200, max_depth=(30), criterion='gini', random_state=13785960, min_samples_leaf=8)
 
# RF_model.fit(x_train, y_train)
# #Predict the response for test dataset
# y_pred = RF_model.predict(x_train)
# rep=classification_report(y_train, y_pred)
# print(rep)
# confusion = confusion_matrix(y_train, y_pred)
# print('Confusion Matrix Train\n')
# print(confusion)

# y_pred = RF_model.predict(x_test)
# rep=classification_report(y_test, y_pred)
# print(rep)
# confusion = confusion_matrix(y_test, y_pred)
# print('Confusion Matrix Test\n')
# print(confusion)