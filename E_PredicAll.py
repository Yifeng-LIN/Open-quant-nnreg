# Import
import keras



# Define function
def PreicNew(new_X, change, ep, bs, dr): 

    # make a prediction
    new_yhat = model.predict(new_X)

    return ()



if __name__ == '__main__':

    print ("\n******************** E) Prediction process  ********************")

    change     = 0.003

    # Load parameters
    param = load("Par-DataStructure.npy")
    train_X, train_y = param[0], param[1]
    val_X, val_y     = param[2], param[3]
    test_X, test_y   = param[4], param[5]
    dateindex = param[7]

    # Prediction
    model = keras.models.load_model("model.h5")
    data_X = concatenate((train_X, val_X, test_X), axis = 0)
    data_y = concatenate((train_y, val_y, test_y))
    data_yhat_scaled = model.predict(data_X)
    data_mix_scaled = concatenate((data_X, data_yhat_scaled), axis = 1)

    # Scalar recover
    scaler = pickle.load(open("Par-Scaler.sav", 'rb'))
    data_mix = scaler.inverse_transform(data_mix_scaled) 
    data_yhat = data_mix[:, -1]
    df_data_yhat = DataFrame(data_yhat, index=dateindex, columns=["yhat"])
    #data_scaled = pd.DataFrame(data_scaled_np, index=data.index)
    
    
    
    ddyh = df_data_yhat.iloc[:,0]
    ddy = df_data.iloc[:,-1]


    print (df_data_yhat)#"TESTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT"


    # All_y dataframe
    all_y = np.zeros(len(dateindex))
    all_y[dummy_y[:,0]==1] = 1
    all_y[dummy_y[:,1]==1] = 0
    all_y[dummy_y[:,2]==1] = -1
    df_all_y = DataFrame(all_y, index=dateindex, columns=["y"])
    print (df_all_y)#"TESTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT"
    
    # All_yhat dataframe
    all_yhat = np.zeros(len(dateindex))
    all_yhat[dummy_yhat[:,0] == np.max(dummy_yhat,axis=1)] = 1
    all_yhat[dummy_yhat[:,1] == np.max(dummy_yhat,axis=1)] = 0
    all_yhat[dummy_yhat[:,2] == np.max(dummy_yhat,axis=1)] = -1
    df_all_yhat = DataFrame(all_yhat, index=dateindex, columns=["yhat"])

    # All yyhat dataframe
    df_all_yyhat = concat([df_all_y, df_all_yhat], axis=1)
    df_all_yyhat.to_csv("Allyyhat.csv")

    # Save to dataSinal
    df_all_close = read_csv("Alldata.csv", index_col=0, usecols=[0,1])
    df_all_close.columns = ['Close']
    df_all_open = df_all_close.shift(1)
    df_all_open.columns = ['Open']
    df_all_sig = df_all_yhat.shift(-1)
    df_all_sig.columns = ['Signal']
    df_all_signal = concat([df_all_close, df_all_open, df_all_sig], axis=1)
    df_all_signal.to_csv("Allsignal.csv")
