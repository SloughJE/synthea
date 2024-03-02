import pandas as pd
import os


def convert_csv_to_optimized_pickle(input_dir, output_dir):
    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    for filename in os.listdir(input_dir):
        print(f"loading {filename}")
        if filename.endswith(".csv"):
            csv_path = os.path.join(input_dir, filename)
            # Change the output path to the new directory
            pickle_path = os.path.join(output_dir, filename.replace('.csv', '.pkl'))
            
            df = pd.read_csv(csv_path)
            
            df.to_pickle(pickle_path)
            print(f"Converted {filename} to pickle format in {output_dir}.")


