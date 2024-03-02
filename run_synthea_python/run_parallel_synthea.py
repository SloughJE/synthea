from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import subprocess
import os
import random
import pandas as pd
from datetime import datetime

def run_synthea_for_state(state, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    command = f"./run_synthea \"{state}\" -c params.txt --exporter.baseDirectory=\"{output_dir}\""
    subprocess.run(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return output_dir


def generate_synthea_data(num_states):

    print(f"generate data for {num_states} patients from random States")

    states = [
        "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado",
        "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho",
        "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana",
        "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota",
        "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada",
        "New Hampshire", "New Jersey", "New Mexico", "New York",
        "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon",
        "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota",
        "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington",
        "West Virginia", "Wisconsin", "Wyoming"
    ]
    base_output_dir = "synthea_output"
    combined_output_dir = "csv_combined_output"
    os.makedirs(combined_output_dir, exist_ok=True)

    with ThreadPoolExecutor(max_workers=6) as executor:
        futures = []
        for _ in range(num_states):
            state = random.choice(states)
            unique_output_dir = os.path.join(base_output_dir, f"{state}_{datetime.now().strftime('%Y%m%d%H%M%S%f')}")
            futures.append(executor.submit(run_synthea_for_state, state, unique_output_dir))
        
        for future in tqdm(as_completed(futures), total=len(futures), desc="Generating data"):

            _ = future.result()  

    print(f"Data generation for {num_states} patients has been completed.")


def append_csv_to_combined_file(filepath, output_filepath):
    df = pd.read_csv(filepath).drop_duplicates()
    header = not os.path.isfile(output_filepath)  # Write header only if file does not exist
    df.to_csv(output_filepath, mode='a', index=False, header=header)

def process_csv_files(output_dir, combined_output_dir):
    csv_output_dir = os.path.join(output_dir, 'csv')  # Adjusted to include 'csv' subdirectory
    if not os.path.exists(csv_output_dir):
        print(f"No CSV files found in {output_dir}. Skipping.")
        return

    for filename in os.listdir(csv_output_dir):
        if filename.endswith(".csv"):
            filepath = os.path.join(csv_output_dir, filename)
            output_filepath = os.path.join(combined_output_dir, filename)
            append_csv_to_combined_file(filepath, output_filepath)


def combine_existing_synthea_output(base_output_dir, combined_output_dir):
    if not os.path.exists(base_output_dir):
        print(f"The directory '{base_output_dir}' does not exist. Exiting function.")
        return
    
    os.makedirs(combined_output_dir, exist_ok=True)
    
    all_files = os.listdir(base_output_dir)
    for state_dir in tqdm(all_files, desc="Combining patient files"):
        state_output_dir = os.path.join(base_output_dir, state_dir)
        if os.path.isdir(state_output_dir):
            process_csv_files(state_output_dir, combined_output_dir)

    print(f"All existing CSV files in '{base_output_dir}' have been processed and combined.")
