import sys 
import argparse

from run_synthea_python.run_parallel_synthea import combine_existing_synthea_output, generate_synthea_data
from run_synthea_python.convert_csv_pickle import convert_csv_to_optimized_pickle

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--generate_patients",
        help="generate random patients",
        action="store_true"
    )

    parser.add_argument(
        "--combine_output_csvs",
        help="combine output csv's from generate random patients",
        action="store_true"
    )

    parser.add_argument(
        "--convert_to_pickle",
        help="convert all csvs in folder to pickle",
        action="store_true"
    )
    args = parser.parse_args()

    if len(sys.argv) == 1:
        print("No arguments, please add arguments")
    else:
  
        if args.generate_patients:
            generate_synthea_data(
                num_states=10,  # this is actually the number of patients
            )

        if args.combine_output_csvs:
            combine_existing_synthea_output(
                base_output_dir = "synthea_output",
                combined_output_dir = "csv_combined_output"
            )
        if args.convert_to_pickle:
            csv_combined_output_dir = "csv_combined_output"
            pickle_output_dir = "pickle_optimized_output" 
            convert_csv_to_optimized_pickle(csv_combined_output_dir, pickle_output_dir)
