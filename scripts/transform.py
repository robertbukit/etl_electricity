import pandas as pd
import os
import json


all_files = os.listdir("data/raw")
master_metrics_data = []

for file_name in all_files:
    file_path = os.path.join("data", "raw", file_name)

    # we read each file in data/raw and load to this (data variable)
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # we using .get() instead directly using data["metrics"] for avoiding corruopt json file
    metrics_dict = data.get("metrics", {})

    for metric_name, details in metrics_dict.items():
        master_metrics_data.append({
            "Zone": data["zone"],
            "Metric": metric_name,
            "Value": details["value"],
            "Unit": details["unit"],
            "Timestamp": details["ts"],
            "Resolution": details["resolution"],
            "Updated": data["updated"],
            "Attribution": data["attribution"],
            "License": data["license"]
        })

if master_metrics_data:
    df_group = pd.DataFrame(master_metrics_data)

    # now we've got dataframe format, and applying several data cleaning & validation
    df_group["Timestamp"] = pd.to_datetime(df_group["Timestamp"], unit="s")

    print(df_group.head())

    # after we did transformation, we save temporary to data lake before we load to warehouse
    temp_file_path = os.path.join("data", "processed", "master_data_electricity_latest.csv")

    df_group.to_csv(temp_file_path, index=False)
    print(f"Transformation Success. Latest data already saved to {temp_file_path}")

else:
    print("Nothing JSON file available to process")




