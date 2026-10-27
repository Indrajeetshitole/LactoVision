import json, time, joblib
from pathlib import Path
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, AdaBoostRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from .config import *
from .preprocessing import prepare, build_preprocessors

MODELS = {
    "Linear Regression": LinearRegression(),
    "Decision Tree": DecisionTreeRegressor(max_depth=14, min_samples_split=10, min_samples_leaf=3, random_state=42),
    "Random Forest": RandomForestRegressor(n_estimators=60, max_depth=20, min_samples_split=5, min_samples_leaf=2, n_jobs=-1, random_state=42),
    "AdaBoost": AdaBoostRegressor(n_estimators=80, learning_rate=0.05, loss="square", random_state=42),
}


def evaluate(model, X, y):
    pred = model.predict(X)
    mae = mean_absolute_error(y, pred)
    rmse = mean_squared_error(y, pred) ** 0.5
    r2 = r2_score(y, pred)
    mape = float((abs((y - pred) / y.clip(lower=1e-8))).mean() * 100)
    return {"MAE": mae, "RMSE": rmse, "R2": r2, "MAPE": mape}


def main():
    train, test, X_train, y_train, X_test, y_test = prepare()
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    rows=[]
    for name, estimator in MODELS.items():
        pre, tree_pre = build_preprocessors()
        processor = pre if name == "Linear Regression" else tree_pre
        pipe = Pipeline([("preprocessor", processor), ("model", estimator)])
        start=time.perf_counter(); pipe.fit(X_train,y_train); seconds=time.perf_counter()-start
        metrics=evaluate(pipe,X_test,y_test); metrics.update({"Model":name,"Training_Time_Seconds":seconds})
        rows.append(metrics)
        fname={"Linear Regression":"linear_regression.pkl","Decision Tree":"decision_tree_regression.pkl","Random Forest":"random_forest_regression.pkl","AdaBoost":"adaboost_regression.pkl"}[name]
        joblib.dump(pipe, MODEL_DIR/fname)
        if name in {"Decision Tree","Random Forest"}:
            try:
                feature_names=pipe.named_steps["preprocessor"].get_feature_names_out()
                imp=pipe.named_steps["model"].feature_importances_
                fi=pd.DataFrame({"feature":feature_names,"importance":imp}).sort_values("importance",ascending=False)
                fi.to_csv(OUTPUT_DIR/f"feature_importance_{name.lower().replace(' ','_')}.csv",index=False)
            except Exception as e: print("Feature importance warning:",e)
        print(name, metrics)
    comp=pd.DataFrame(rows)[["Model","MAE","RMSE","R2","MAPE","Training_Time_Seconds"]]
    comp.to_csv(OUTPUT_DIR/"model_comparison_sklearn.csv",index=False)
    print(comp.to_string(index=False))

if __name__ == "__main__": main()
