import pandas as pd
import matplotlib.pyplot as plt
from .config import *
from .preprocessing import load_train_test


def save():
    EDA_DIR.mkdir(parents=True, exist_ok=True)
    master = pd.read_csv(DATASET_DIR / "LactoVision_Master_Dataset_50000.csv")

    plt.figure(figsize=(9, 6)); plt.hist(master[TARGET].dropna(), bins=30); plt.title("Daily Milk Yield Distribution"); plt.tight_layout(); plt.savefig(EDA_DIR / "milk_yield_distribution.png", dpi=160); plt.close()
    for col, name in [("breed","breed"),("lactation_stage","lactation_stage"),("health_status","health_status")]:
        plt.figure(figsize=(11,6)); master.boxplot(column=TARGET, by=col, rot=30); plt.suptitle(""); plt.xticks(rotation=30, ha="right"); plt.title(f"Milk Yield by {col}"); plt.tight_layout(); plt.savefig(EDA_DIR / f"milk_yield_by_{name}.png", dpi=160); plt.close()
    for col in ["feed_quantity_kg_dm","body_weight_kg","age_years","water_intake_l","ambient_temperature_c","thi"]:
        plt.figure(figsize=(8,6)); plt.scatter(master[col], master[TARGET], alpha=.25); plt.title(f"Milk Yield vs {col}"); plt.tight_layout(); plt.savefig(EDA_DIR / f"milk_yield_vs_{col}.png", dpi=160); plt.close()
    numeric = master.select_dtypes(include="number")
    plt.figure(figsize=(16,12)); plt.imshow(numeric.corr(), aspect="auto"); plt.xticks(range(len(numeric.columns)), numeric.columns, rotation=90, fontsize=6); plt.yticks(range(len(numeric.columns)), numeric.columns, fontsize=6); plt.title("Correlation Heatmap"); plt.colorbar(); plt.tight_layout(); plt.savefig(EDA_DIR / "correlation_heatmap.png", dpi=160); plt.close()
    print(f"EDA saved to {EDA_DIR}")

if __name__ == "__main__": save()
