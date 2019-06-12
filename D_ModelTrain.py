# Import
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import BatchNormalization, Dropout
from keras.callbacks import ModelCheckpoint



# Define function
def ModelTrain(train_X, train_y, val_X, val_y, test_X, test_y, epoch, batch, drop): 

    # Print title
    print ("\n******************** D) Training process    ********************")

    # Design network
    print ("\nModel's structure: ")
    model = Sequential()
    model.add(Dense(50, activation='relu', kernel_initializer='glorot_uniform'))
    model.add(BatchNormalization())
    model.add(Dropout(drop))
    model.add(Dense(30, activation='relu', kernel_initializer='glorot_uniform'))
    model.add(BatchNormalization())
    model.add(Dropout(drop))
    model.add(Dense(10, activation='relu', kernel_initializer='glorot_uniform'))
    model.add(BatchNormalization())
    model.add(Dropout(drop))
    model.add(Dense(1))
    #model.add(Dense(1, activation='softmax'))
    checkpoint = ModelCheckpoint('model.h5', verbose=0, monitor='val_loss', save_best_only=True, mode='auto')  
    model.compile(optimizer='adam', loss='mean_squared_error')
    #model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    #print(model.summary())
    #model.fit(train_X, train_y, epochs=ep, batch_size=bs, validation_data=(val_X, val_y), callbacks=[checkpoint], verbose=2, shuffle=False)

    # Fit network
    print ("\nModel's training process: ")    
    history = model.fit(train_X.values, train_y.values, epochs=epoch, batch_size=batch, validation_data=(val_X, val_y), callbacks=[checkpoint], verbose=2, shuffle=False)
    
    # Plot history
    plt.plot(history.history['loss'], label='train')
    plt.plot(history.history['val_loss'], label='val')
    plt.ylim(top=1.2)
    plt.legend()
    plt.show()
    
    return ()



# Test function
if __name__ == '__main__':

    # Parameter
    from A_Parameters import Parameters
    Params_fix, Params_var = Parameters()
    GetSource, GetScale, SourceStart, SourceEnd, perc_train = Params_fix[0],  Params_fix[1],  Params_fix[2],  Params_fix[3],  Params_fix[4]  
    TestFrom, TestTill, change, epoch, batch, drop = Params_var[0][0], Params_var[0][1], Params_var[0][2], Params_var[0][3], Params_var[0][4], Params_var[0][5]
    
    # Debug code
    ModelTrain(train_X, train_y, val_X, val_y, test_X, test_y, epoch, batch, drop)
