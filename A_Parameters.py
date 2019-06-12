# Import
import datetime



# Define function
def Parameters():

    # Print title
    print ("\n\n=======>>=======>>=======>>=======>>=======>>=======>>=======>>>>>>>")
    print ("\n******************** A) Set parameters    ********************")

    
    # Set parameters
    GetSource    = 1  # 1 to get new source, 0 to read source
    GetScale     = 1  # 1 for scaling, 0 not scaling
    SourceStart  = ["2005-01-01"]
    SourceEnd    = str(datetime.date.today())
    perc_train   = 90

    TestPeriod   = [
                   ["2018-11-02", "2018-12-06"],
                   ]
    change       = [0.001]
    epoch        = [100]
    batch        = [72]
    drop         = [0.1]


    Params_fix    = [GetSource, GetScale, SourceStart, SourceEnd, perc_train]
    
    Params_var = []
    for i, j in TestPeriod:
        for k in change:
            for l in epoch:
                for m in batch:
                    for n in drop:
                            p = [i, j, k, l, m, n]
                            Params_var.append(p)

    print ("Set parameters OK\n")
       
    return (Params_fix, Params_var)



# Test function
if __name__ == '__main__':

    # Debug code
    Params_fix, Params_var = Parameters()
    GetSource, GetScale, SourceStart, SourceEnd, perc_train = Params_fix[0],  Params_fix[1],  Params_fix[2],  Params_fix[3],  Params_fix[4]  
    for i in range(len(Params_var)):
        TestFrom, TestTill, change, epoch, batch, drop = Params_var[i][0], Params_var[i][1], Params_var[i][2], Params_var[i][3], Params_var[i][4], Params_var[i][5]
