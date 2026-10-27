import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from .config import OUTPUT_DIR

def main():
    p=OUTPUT_DIR/'model_comparison_sklearn.csv'
    if p.exists():
        d=pd.read_csv(p)
        plt.figure(figsize=(10,6)); plt.bar(d['Model'], d['RMSE']); plt.xticks(rotation=25,ha='right'); plt.ylabel('RMSE (kg/day)'); plt.title('Model Comparison - RMSE'); plt.tight_layout(); plt.savefig(OUTPUT_DIR/'model_comparison.png',dpi=160); plt.close()
    fi=OUTPUT_DIR/'feature_importance_random_forest.csv'
    if fi.exists():
        d=pd.read_csv(fi).head(20).sort_values('importance')
        plt.figure(figsize=(10,8)); plt.barh(d['feature'],d['importance']); plt.xlabel('Importance'); plt.title('Top 20 Random Forest Features'); plt.tight_layout(); plt.savefig(OUTPUT_DIR/'feature_importance.png',dpi=160); plt.close()
if __name__=='__main__': main()
