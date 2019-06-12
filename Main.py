# Simplify
# Regression model
# Add more signal
# D debuging


# Import
from A_Parameters import Parameters
from B_SourceData import SourceData
from C_StructureData import StructureData
from D_ModelTrain import ModelTrain
from E_PredicAll import PreicNew
from F_BackTesting import BackTesting



# Run mode define
RunSourceData    = 1
RunStructureData = 1
RunModelTrain    = 0
RunPredicNew     = 1
RunBackTesting   = 1



# Initial variable
Cum_number = 0
Cum_portofolio = 0



# A) Import parameters for Grid search
Params_fix, Params_var = Parameters()
GetSource, GetScale, SourceStart, SourceEnd, perc_train = Params_fix[0],  Params_fix[1],  Params_fix[2],  Params_fix[3],  Params_fix[4]  
for i in range(len(Params_var)):
    TestFrom, TestTill, change, epoch, batch, drop = Params_var[i][0], Params_var[i][1], Params_var[i][2], Params_var[i][3], Params_var[i][4], Params_var[i][5]



    # B) Import source data 
    if RunSourceData  == 1:
        df_data = SourceData(GetSource, SourceStart, SourceEnd)



    # C) Structuring data 
    if RunStructureData  == 1:
        train_X, train_y, val_X, val_y, test_X, test_y, test_dt = StructureData(df_data, perc_train, TestFrom, TestTill, GetScale)



    # D) Model train and validation
    if RunModelTrain == 1:
        ModelTrain(train_X, train_y, val_X, val_y, test_X, test_y, epoch, batch, drop)



    # E) Predict all data
    if RunPredicNew == 1:
        #PreicNew(test_X, epoch, batch, drop, GetScale): 

        
        # Import
        import keras
        import numpy as np
        import pandas as pd
        import pickle
        from pandas import DataFrame

        
        # Print title
        print ("\n******************** E) Prediction process  ********************")


        # Prediction
        model = keras.models.load_model("model.h5")
        data_X = np.concatenate((train_X, val_X, test_X), axis = 0)
        data_yhat = model.predict(data_X)
        data_hat = np.concatenate((data_X, data_yhat), axis = 1)

        # Use data to NoTestTo
        NoTestTo    = data_X.shape[0]
        IndexTestTo = df_data.iloc[:NoTestTo, 0].index

        # Scalar recover
        if GetScale == 1:
            scaler = pickle.load(open("Par-scaler.sav", 'rb'))
            data_hat = scaler.inverse_transform(data_hat)
        df_data_yhat = DataFrame(data_hat[:, -1], index=IndexTestTo)
        
        # All_y dataframe
        change = 3
        data_y = pd.read_csv("Sourcedata.csv", index_col=0).iloc[:NoTestTo, -1].values
        df_data_y = DataFrame(data_y, index=IndexTestTo)

        all_y = np.zeros((len(IndexTestTo), 1))
        all_y[df_data_y.values>=change] = 1
        all_y[df_data_y.values<=change] = -1
        df_all_y = DataFrame(all_y, index=IndexTestTo, columns=["y"])
        
        # All_yhat dataframe
        all_yhat = np.zeros((len(IndexTestTo), 1))
        all_yhat[df_data_yhat.values>=change] = 1
        all_yhat[df_data_yhat.values<=change] = -1
        df_all_yhat = DataFrame(all_yhat, index=IndexTestTo, columns=["yhat"])

        # All yyhat dataframe
        df_all_yyhat = np.concat([df_all_y, df_all_yhat], axis=1)
        df_all_yyhat.to_csv("Allyyhat.csv")

        # Save to dataSinal
        df_all_close = pd.read_csv("Alldata.csv", index_col=0, usecols=[0,1])
        df_all_close.columns = ['Close']
        df_all_open = df_all_close.shift(1)
        df_all_open.columns = ['Open']
        df_all_sig = df_all_yhat.shift(-1)
        df_all_sig.columns = ['Signal']
        df_all_signal = np.concat([df_all_close, df_all_open, df_all_sig], axis=1)
        df_all_signal.to_csv("Allsignal.csv")



    # F) Backtest
    if RunBackTesting == 1:
        print ("\n******************** F) Backtesting process ********************")
    
        # Load parameters
        param = load("Par-DataStructure.npy")
        test_dt = param[7]
        fromdate = test_dt.date()
        
        # Backtesting
        Porto_TrainVal = BackTesting()
        Porto_Test     = BackTesting(fromdate)
        
        # Average potofolio
        Cum_number += 1
        Cum_portofolio += Porto_Test
        Av_Porto_Test = Cum_portofolio / Cum_number
    
        # Save result
        with open("Log-Result.txt", "a") as f:
            print ("\nTest from : "+str(fromdate), file=f)
            print ("Case   /  Change  /  epoch  /  batch  /  drop", file=f)
            print ("No."+str(i+1)+"  /  "+str(change)+"   /  "+str(epoch)+"    /  "+str(batch)+"     /  "+str(drop), file=f)
            print ("Portofolio at the end of all period is  : "+str(round(Porto_TrainVal)), file=f)
            print ("Portofolio at the end of test period is : "+str(round(Porto_Test)), file=f)
            print ("Mean portofolio for test period is      : "+str(round(Av_Porto_Test)), file=f)

