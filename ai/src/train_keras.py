"""Train the required TensorFlow/Keras ANN and deeper regression model.
Run this after installing TensorFlow in the Phase 4 environment."""
import json, time, joblib
import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from .config import *
from .preprocessing import prepare, build_preprocessors


def metrics(y, pred):
    return {
        "MAE": float(mean_absolute_error(y,pred)),
        "RMSE": float(mean_squared_error(y,pred)**0.5),
        "R2": float(r2_score(y,pred)),
        "MAPE": float((np.abs((y-pred)/np.clip(y,1e-8,None))).mean()*100),
    }

def make_model(n_features, deep=False):
    layers = [tf.keras.layers.Input(shape=(n_features,))]
    if deep:
        layers += [tf.keras.layers.Dense(256,activation="relu"),tf.keras.layers.Dropout(.2),tf.keras.layers.Dense(128,activation="relu"),tf.keras.layers.Dropout(.2),tf.keras.layers.Dense(64,activation="relu"),tf.keras.layers.Dense(32,activation="relu")]
    else:
        layers += [tf.keras.layers.Dense(128,activation="relu"),tf.keras.layers.Dropout(.2),tf.keras.layers.Dense(64,activation="relu"),tf.keras.layers.Dropout(.15)]
    layers += [tf.keras.layers.Dense(1,activation="linear")]
    model=tf.keras.Sequential(layers)
    model.compile(optimizer=tf.keras.optimizers.Adam(),loss="mse",metrics=[tf.keras.metrics.MeanAbsoluteError()])
    return model

def main():
    _,_,X_train,y_train,X_test,y_test=prepare()
    pre,_=build_preprocessors()
    Xtr=pre.fit_transform(X_train); Xte=pre.transform(X_test)
    Xtr=Xtr.toarray() if hasattr(Xtr,"toarray") else Xtr
    Xte=Xte.toarray() if hasattr(Xte,"toarray") else Xte
    PREPROCESS_DIR.mkdir(exist_ok=True,parents=True); joblib.dump(pre,PREPROCESS_DIR/"keras_preprocessing_pipeline.pkl")
    MODEL_DIR.mkdir(exist_ok=True,parents=True)
    rows=[]
    for label,deep,fname in [("ANN",False,"ann_model.keras"),("Deep Learning",True,"deep_learning_regression.keras")]:
        model=make_model(Xtr.shape[1],deep)
        cb=[tf.keras.callbacks.EarlyStopping(monitor="val_loss",patience=12,restore_best_weights=True),tf.keras.callbacks.ReduceLROnPlateau(monitor="val_loss",factor=.5,patience=5,min_lr=1e-6)]
        start=time.perf_counter(); model.fit(Xtr,y_train.values,validation_split=.15,epochs=120,batch_size=256,callbacks=cb,verbose=1); seconds=time.perf_counter()-start
        pred=model.predict(Xte,verbose=0).ravel(); m=metrics(y_test.values,pred); m.update({"Model":label,"Training_Time_Seconds":seconds}); rows.append(m); model.save(MODEL_DIR/fname); print(label,m)
    pd.DataFrame(rows).to_csv(OUTPUT_DIR/"keras_model_comparison.csv",index=False)

if __name__ == "__main__": main()
