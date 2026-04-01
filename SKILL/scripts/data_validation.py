import pandas as pd
import numpy as np
import argparse
import json
import sys
import os

REQUIRED_COLUMNS = [
    'cik', 'ddate', 'revenue', 'net_income',
    'debt', 'equity', 'assets','cash_flow'
]


# -----------------------------
# Validation Function
# -----------------------------
def validate_dataset(df):
    errors = []
    warnings = []

    # Check columns
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        errors.append(f"Missing columns: {missing}")

    # Parse date
    try:
        df['ddate'] = pd.to_datetime(df['ddate'])
    except Exception:
        errors.append("Invalid date format")

    # Null check
    null_pct = df.isnull().mean().to_dict()

    for col in REQUIRED_COLUMNS:
        if col in df.columns and null_pct[col] > 0.3:
            errors.append(f"{col} has >30% nulls")

    # Duplicates
    dup_pct = df.duplicated().mean()
    if dup_pct > 0.1:
        warnings.append("High duplicate rows")

    return errors, warnings, null_pct


# -----------------------------
# Profiling Function
# -----------------------------
def profile_dataset(df):
    profile = {}

    profile['row_count'] = len(df)
    profile['column_count'] = len(df.columns)
    profile['columns'] = list(df.columns)

    # Null %
    profile['null_percentage'] = df.isnull().mean().to_dict()

    # Basic stats
    profile['summary_stats'] = df.describe(include='all').to_dict()

    # Outlier detection (IQR)
    outliers = {}
    for col in df.select_dtypes(include=np.number).columns:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1

        outlier_count = df[
            (df[col] < (Q1 - 1.5 * IQR)) |
            (df[col] > (Q3 + 1.5 * IQR))
        ].shape[0]

        outliers[col] = outlier_count

    profile['outliers'] = outliers

    return profile


# -----------------------------
# Main Entry Function
# -----------------------------

def run_validation():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-data", required=True)
    args = parser.parse_args()

    try:
        df = pd.read_csv(args.input_data)

        errors, warnings, null_pct = validate_dataset(df)

        if errors:
            print(json.dumps({
                "status": "failed",
                "errors": errors
            }))
            sys.exit(1)
        os.makedirs("outputs", exist_ok=True)

        output = {
            "status": "success",
            "row_count": len(df),
            "column_count": len(df.columns),
            "null_percentage": null_pct,
            "warnings": warnings,
            "errors": errors
        }

        with open("outputs/validation.json", "w") as f:
            json.dump(output, f, indent=4)

        print(json.dumps(output))

        
        profile = profile_dataset(df)

        return {
            "status": "success",
            "warnings": warnings,
            "profile": profile
        }
        
    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}))
        sys.exit(1)


if __name__ == "__main__":
    run_validation()