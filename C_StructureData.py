# Import
import numpy as np
from pandas import DataFrame
from sklearn import preprocessing
import pickle



# File definition
logfile   = 'Log-DataSet.txt'
datafile  = 'Alldata.csv'
datafileY = 'AlldataY.csv'



# Define function
def PrintLog(logfile, overwrite, txt):
    with open(logfile, overwrite) as f:
        print(txt, file=f)
    print(txt)


def StructureData(df_data, perc_train, TestFrom, TestTill, GetScale): 

    # Print title
    print ("\n******************** C) Structuring data    ********************")

    # date index and number samples
    SeNb_TestFrom = np.sum(df_data.index <= TestFrom)
    SeNb_TestTill = np.sum(df_data.index <= TestTill)
    Nb_train = int ((SeNb_TestFrom) * perc_train/100)
    Nb_val   = int ((SeNb_TestFrom) * (1-perc_train/100))

    # split into train and val sets
    df_train_X = df_data.iloc[:Nb_train, :-1]
    df_train_y = df_data.iloc[:Nb_train, -1]
    df_val_X   = df_data.iloc[Nb_train:(Nb_train+Nb_val), :-1]
    df_val_y   = df_data.iloc[Nb_train:(Nb_train+Nb_val), -1]
    df_test_X  = df_data.iloc[(Nb_train+Nb_val):SeNb_TestTill, :-1]
    df_test_y  = df_data.iloc[(Nb_train+Nb_val):SeNb_TestTill, -1]

    # save to csv
    DataFrame(df_train_X).to_csv("Sourcedata_train_X.csv")
    DataFrame(df_train_y).to_csv("Sourcedata_train_y.csv")
    DataFrame(df_val_X).to_csv("Sourcedata_val_X.csv")
    DataFrame(df_val_y).to_csv("Sourcedata_val_y.csv")
    DataFrame(df_test_X).to_csv("Sourcedata_test_X.csv")
    DataFrame(df_test_y).to_csv("Sourcedata_test_y.csv")

    # Data scaling
    if GetScale == 1:
        
        # Scaler calculation
        scaler = preprocessing.MinMaxScaler()
        data_scaled = scaler.fit_transform(df_data.values)
        df_data_scaled = DataFrame(data_scaled, index=df_data.index, columns=df_data.columns)
        pickle.dump(scaler, open("Par-Scaler.sav", 'wb'))

        # split into train and val sets
        df_train_X_scaled = df_data_scaled.iloc[:Nb_train, :-1]
        df_train_y_scaled = df_data_scaled.iloc[:Nb_train, -1]
        df_val_X_scaled   = df_data_scaled.iloc[Nb_train:(Nb_train+Nb_val), :-1]
        df_val_y_scaled   = df_data_scaled.iloc[Nb_train:(Nb_train+Nb_val), -1]
        df_test_X_scaled  = df_data_scaled.iloc[(Nb_train+Nb_val):SeNb_TestTill, :-1]
        df_test_y_scaled  = df_data_scaled.iloc[(Nb_train+Nb_val):SeNb_TestTill, -1]

        # save to csv
        DataFrame(df_train_X_scaled).to_csv("Sourcedata_train_X_scaled.csv")
        DataFrame(df_train_y_scaled).to_csv("Sourcedata_train_y_scaled.csv")
        DataFrame(df_val_X_scaled).to_csv("Sourcedata_val_X_scaled.csv")
        DataFrame(df_val_y_scaled).to_csv("Sourcedata_val_y_scaled.csv")
        DataFrame(df_test_X_scaled).to_csv("Sourcedata_test_X_scaled.csv")
        DataFrame(df_test_y_scaled).to_csv("Sourcedata_test_y_scaled.csv")
    
        # Define return value
        df_train_X, df_train_y, df_val_X, df_val_y, df_test_X, df_test_y = df_train_X_scaled, df_train_y_scaled, df_val_X_scaled, df_val_y_scaled, df_test_X_scaled, df_test_y_scaled
    
    test_dt = df_data.index[(Nb_train+Nb_val)]
    
    # reshape input to be 3D [samples, timesteps, features]
    PrintLog(logfile, 'a', "\nTotal sample nb :  "+str(df_data.shape[0]))
    PrintLog(logfile, 'a', "Train set shape :  "+str(df_train_X.shape)+str(df_train_y.shape))
    PrintLog(logfile, 'a', "Valid set shape :  "+str(df_val_X.shape)+str(df_val_y.shape))
    PrintLog(logfile, 'a', "Test  set shape :  "+str(df_test_X.shape)+str(df_test_y.shape))
    PrintLog(logfile, 'a', "Train/Val period:  "+str(df_data.index[0])+str(" to ")+str(df_data.index[len(df_train_y)+len(df_val_y)-1]))
    PrintLog(logfile, 'a', "Test  set period:  "+str(df_data.index[len(df_train_y)+len(df_val_y)])+str(" to ")+str(df_data.index[len(df_train_y)+len(df_val_y)+len(df_test_y)-1]))
    
    return (df_train_X, df_train_y, df_val_X, df_val_y, df_test_X, df_test_y, test_dt)



# Test function
if __name__ == '__main__':
    
    # Parameter
    from A_Parameters import Parameters
    Params_fix, Params_var = Parameters()
    GetSource, GetScale, SourceStart, SourceEnd, perc_train = Params_fix[0],  Params_fix[1],  Params_fix[2],  Params_fix[3],  Params_fix[4]  
    TestFrom, TestTill, change, epoch, batch, drop = Params_var[0][0], Params_var[0][1], Params_var[0][2], Params_var[0][3], Params_var[0][4], Params_var[0][5]
    
    # Debug code
    train_X, train_y, val_X, val_y, test_X, test_y, test_dt = StructureData(df_data, perc_train, TestFrom, TestTill, GetScale)

