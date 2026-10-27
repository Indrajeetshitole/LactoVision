import json, joblib
import pandas as pd
from .config import *

def main():
    frames=[]
    p=OUTPUT_DIR/"model_comparison_sklearn.csv"
    if p.exists(): frames.append(pd.read_csv(p))
    p=OUTPUT_DIR/"keras_model_comparison.csv"
    if p.exists(): frames.append(pd.read_csv(p))
    if not frames: raise SystemExit("No model comparison files found. Train models first.")
    comp=pd.concat(frames,ignore_index=True)
    comp=comp.sort_values(["RMSE","MAE","R2"],ascending=[True,True,False]).reset_index(drop=True)
    comp.to_csv(OUTPUT_DIR/"model_comparison.csv",index=False)
    best=comp.iloc[0]
    model_name=best["Model"]
    if model_name in {"Linear Regression","Decision Tree","Random Forest","AdaBoost"}:
        fname={"Linear Regression":"linear_regression.pkl","Decision Tree":"decision_tree_regression.pkl","Random Forest":"random_forest_regression.pkl","AdaBoost":"adaboost_regression.pkl"}[model_name]
        model=joblib.load(MODEL_DIR/fname)
        joblib.dump({"model":model,"model_name":model_name,"metrics":best.to_dict()},MODEL_DIR/"best_model.pkl")
    else:
        raise RuntimeError("Keras best-model selection requires a Keras-aware prediction artifact; use the deployment helper after Keras training.")
    print("BEST MODEL:",model_name)
    print(best.to_dict())

if __name__ == "__main__": main()
