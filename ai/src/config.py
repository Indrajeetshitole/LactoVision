from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATASET_DIR = ROOT / "dataset"
OUTPUT_DIR = ROOT / "outputs"
EDA_DIR = OUTPUT_DIR / "eda"
MODEL_DIR = ROOT / "models"
PREPROCESS_DIR = ROOT / "preprocessing"

TARGET = "daily_milk_yield_kg"

ANIMAL_FEATURES = [
    "breed", "breed_group", "sex", "age_years", "body_weight_kg", "parity",
]
LACTATION_FEATURES = [
    "lactation_number", "days_in_milk", "lactation_stage", "days_since_calving",
]
FEED_FEATURES = [
    "feed_type", "feed_quantity_kg_dm", "feed_frequency", "morning_feed_kg",
    "afternoon_feed_kg", "evening_feed_kg", "feed_quality_score",
]
NUTRITION_FEATURES = [
    "dry_matter_kg", "crude_protein_g", "metabolizable_energy_mj", "ndf_g",
    "fat_g", "calcium_g", "phosphorus_g", "water_intake_l",
]
HEALTH_FEATURES = [
    "body_condition_score", "health_status", "disease_status", "disease_type",
    "symptoms", "vaccination_status", "treatment_status", "body_temperature_c",
    "heart_rate_bpm", "respiration_rate_bpm",
]
ENVIRONMENT_FEATURES = [
    "ambient_temperature_c", "relative_humidity_pct", "thi", "weather_condition", "season",
]
FEATURES = (
    ANIMAL_FEATURES + LACTATION_FEATURES + FEED_FEATURES + NUTRITION_FEATURES
    + HEALTH_FEATURES + ENVIRONMENT_FEATURES
)

CATEGORICAL_FEATURES = [c for c in FEATURES if c in {
    "breed", "breed_group", "sex", "lactation_stage", "feed_type", "health_status",
    "disease_status", "disease_type", "symptoms", "vaccination_status", "treatment_status",
    "weather_condition", "season"
}]
NUMERICAL_FEATURES = [c for c in FEATURES if c not in CATEGORICAL_FEATURES]

LEAKAGE_COLUMNS = [
    "daily_milk_yield_kg", "milk_morning_kg", "milk_evening_kg", "daily_revenue",
    "daily_profit", "feed_cost_per_kg_milk"
]
IDENTIFIER_COLUMNS = ["record_id", "source_dataset", "source_record_id", "cow_id", "farm_id", "record_date"]
