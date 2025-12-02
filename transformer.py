import pandas as pd
import os

# --- 1. Transformation Function (Updated) ---
# This function now takes an output folder as an argument to know where to save the file.

def transform_and_save(input_filepath, output_folder):
    """
    Reads a CSV, skips the first 9 rows, transforms its data, and saves it
    to a new '_parsed.csv' file in the specified output folder.
    """
    try:
        # Tell pandas to skip the first 9 rows of the file.
        df = pd.read_csv(input_filepath, skiprows=9)
        
        # The 'name' column is the one we need to parse
        name = df['name']

        # Split the 'name' column into multiple parts
        splits = name.str.split('_', expand=True)

        # Extract each part and slice off the prefixes
        length = splits[0].str.slice(start=3)
        gc = splits[1].str.slice(start=2)
        entropy = splits[2].str.slice(start=1)
        obs_gc = splits[3].str.slice(start=5)
        obs_entropy = splits[4].str.slice(start=4)

        # Insert the new, clean columns at the beginning of the DataFrame
        df.insert(0, 'obs_entropy', obs_entropy)
        df.insert(0, 'obs_gc', obs_gc)
        df.insert(0, 'entropy', entropy)
        df.insert(0, 'gc', gc)
        df.insert(0, 'length', length)

        # Remove the original 'name' column
        df.drop(columns='name', inplace=True)

        # --- NEW: Construct the output path ---
        # Get the base filename from the full input path (e.g., "synth_bp_results_25")
        base_filename = os.path.splitext(os.path.basename(input_filepath))[0]
        
        # Create the full path for the new file in the output folder
        output_filepath = os.path.join(output_folder, f"{base_filename}_parsed.csv")

        # Save the transformed DataFrame to the new CSV file
        df.to_csv(output_filepath, index=False)
        
        print(f"✅ Successfully processed: {input_filepath} -> {output_filepath}")

    except FileNotFoundError:
        print(f"❌ Error: File not found at {input_filepath}")
    except KeyError as e:
        print(f"❌ Error processing {input_filepath}: A required column is missing. Check if the header is correct after skipping 9 rows. Details: {e}")
    except Exception as e:
        print(f"❌ An error occurred while processing {input_filepath}: {e}")


# --- 2. Main Loop (Updated) ---
# This part now creates the output folder and passes it to the function.

if __name__ == "__main__":
    base_name = "synth_kmp_results"
    input_folder_name = "kmp"
    output_folder_name = "kmp_parsed"  # <-- Name of the new folder for results
    
    print("Starting batch processing of CSV files...\n")

    # --- NEW: Create the output directory if it doesn't exist ---
    # exist_ok=True prevents an error if the folder is already there.
    os.makedirs(output_folder_name, exist_ok=True)
    print(f"📁 Output will be saved in the '{output_folder_name}' directory.\n")

    # Loop from 1 to 50 (inclusive)
    for i in range(1, 51):
        # Handle the special case of the first file (which has no number)
        if i == 1:
            input_filename = os.path.join(input_folder_name, f"{base_name}.csv")
        else:
            input_filename = os.path.join(input_folder_name, f"{base_name}_{i}.csv")
        
        # Check if the file actually exists before trying to process it
        if os.path.exists(input_filename):
            # --- UPDATED: Pass the output folder to the function ---
            transform_and_save(input_filename, output_folder_name)
        else:
            print(f"⚠️  Skipping, file not found: {input_filename}")
            
    print("\n🎉 Batch processing complete.")