# Import
import talib
import pandas as pd
import quandl
quandl.ApiConfig.api_key = "ZDfv2NCGxLMv-KNxuWVV"
    


# Define function
def SourceData(GetSource, SourceStart, SourceEnd):
    
    # Print title
    print ("\n******************** B) Import source data  ********************")
    
    # Import data source
    if GetSource == 1:
        
        # Get from quandl
        Data1 = {
                "close " : quandl.get("LBMA/GOLD", start_date=SourceStart, end_date=SourceEnd)["USD (PM)"].dropna(),
                }
        Data2 = {
                "MA    " : talib.MA(Data1["close "], timeperiod=30, matype=0),
                "EMA   " : talib.EMA(Data1["close "], timeperiod=30),
                "CMO   " : talib.CMO(Data1["close "], timeperiod=14),
                "MACD1 " : talib.MACD(Data1["close "], fastperiod=12, slowperiod=26, signalperiod=9)[0],
                "MACD2 " : talib.MACD(Data1["close "], fastperiod=12, slowperiod=26, signalperiod=9)[1],
                "MACD3 " : talib.MACD(Data1["close "], fastperiod=12, slowperiod=26, signalperiod=9)[2],
                }
        Data3 = {
                "Crude " : quandl.get("EIA/PET_RWTC_D", start_date=SourceStart, end_date=SourceEnd)["Value"],
                "CNY   " : quandl.get("FED/RXI_N_B_CH", start_date=SourceStart, end_date=SourceEnd)["Value"],
                }
        df_data = pd.DataFrame.from_dict({**Data1, **Data2, **Data3})
        
        # Define target
        closeN1  = df_data.iloc[:, 0].shift(periods=-1)
        closeN2  = df_data.iloc[:, 0].shift(periods=-2)
        closeN3  = df_data.iloc[:, 0].shift(periods=-3)
        closeN4  = df_data.iloc[:, 0].shift(periods=-4)
        closeN5  = df_data.iloc[:, 0].shift(periods=-5)
        closeN6  = df_data.iloc[:, 0].shift(periods=-6)
        closeN7  = df_data.iloc[:, 0].shift(periods=-7)
        closeN8  = df_data.iloc[:, 0].shift(periods=-8)
        closeN9  = df_data.iloc[:, 0].shift(periods=-9)
        closeN10 = df_data.iloc[:, 0].shift(periods=-10)
        MeanCloseN10 = (closeN1+closeN2+closeN3+closeN4+closeN5+closeN6+closeN7+closeN8+closeN9+closeN10) / 10
        df_data["NC10 Pcent Cge"] = (MeanCloseN10 - df_data["close "]) /df_data["close "] *100
        
        # Drop empty
        df_data = df_data.dropna()
        
        # Save to file
        df_data.to_csv("Sourcedata.csv")
        print ("Import source OK\n")

    # Import data source
    else:
        df_data = pd.read_csv("Sourcedata.csv", index_col=0)
        print ("Read source OK\n")
        
    return (df_data)



# Test function
if __name__ == '__main__':

    # Parameter
    from A_Parameters import Parameters
    Params_fix, Params_var = Parameters()
    GetSource, GetScale, SourceStart, SourceEnd, perc_train = Params_fix[0],  Params_fix[1],  Params_fix[2],  Params_fix[3],  Params_fix[4]  
    TestFrom, TestTill, change, epoch, batch, drop = Params_var[0][0], Params_var[0][1], Params_var[0][2], Params_var[0][3], Params_var[0][4], Params_var[0][5]
    
    # Debug code
    df_data = SourceData(GetSource, SourceStart, SourceEnd)
    print (df_data, "\n\nTEST PRINT   TEST PRINT   TEST PRINT \n\n")