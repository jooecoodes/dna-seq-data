import pandas as pd
import os

algos = ['bp', 'kmp', 'boyer_moore']
stack = []

# for algo in algos:
#     for i in range(1, 51):
#         base_name = f"synth_{algo}_results_{i}_parsed.csv"
#         folder_name = f"{algo}"

#         csv = pd.read_csv(os.path.join(folder_name, base_name))
#         df = pd.DataFrame(csv)

#         for i, r in df.iterrows():
#             seq = r['sequence']
#             length = r['length']
#             gc = r['gc']
#             entropy = r['entropy']
#             obs_gc = r['obs_gc']
#             obs_entropy = r['obs_entropy']
#             execution_time = r['real_time']
#             row = [seq, length, gc, entropy, obs_gc, obs_entropy, algo]
#             stack.append(r)


# for i in range(0, 54):

#     sentinel = 1

#     while sentinel != 51:

#         base_name = f"synth_bp_rowed_results_{sentinel}_parsed.csv"
#         input_base_name = f"synth_bp_results_{sentinel}_parsed.csv"
#         input_folder_name = f"bp_parsed"

#         csv = pd.read_csv(os.path.join(input_folder_name, input_base_name))
#         df = pd.DataFrame(csv) 
    
#         print(df.loc[0])
#         # stack.append(df.loc[i])
#         sentinel += 1
def read_csv_headers(filename):
  """
  Reads only the headers from a specified CSV file.

  Args:
      filename (str): The path to the CSV file.

  Returns:
      list: A list containing the column names (headers).
  """
  try:
    # Read only 0 rows, but read the header (header=0 is default).
    df_headers = pd.read_csv(filename, nrows=0)
    # Extract and return the column names as a list
    return df_headers.columns.tolist()
  except FileNotFoundError:
    return f"Error: The file '{filename}' was not found."
  except Exception as e:
    return f"An error occurred: {e}"
  


for algo in algos:
    

    input_base_name = f"synth_{algo}_results_1_parsed.csv"
    input_folder_name = f"{algo}_parsed"

    header_list = read_csv_headers(os.path.join(input_folder_name, input_base_name))
    empty_df = pd.DataFrame(columns=header_list, index=[])

    for i in range(0, 54): 
        empty_df = pd.DataFrame(columns=header_list, index=[])

        sentinel = 1

        while sentinel != 51:

            input_base_name = f"synth_{algo}_results_{sentinel}_parsed.csv"
            input_folder_name = f"{algo}_parsed"

            csv = pd.read_csv(os.path.join(input_folder_name, input_base_name))
            df = pd.DataFrame(csv) 

            empty_df.loc[len(empty_df)] = df.loc[i]

            print(empty_df.head())

            sentinel += 1


            # empty_df.loc[len(empty_df)] = df.loc[0]


            # print(empty_df.head())

            # empty_df.loc[len(empty_df)] = df.loc[1]

            # print(empty_df.head())
            # print(df.loc[1])

        print(empty_df.to_string(index=False))

        length = empty_df.loc[0, 'length']
        gc = empty_df.loc[0, 'gc']
        entropy = empty_df.loc[0, 'entropy']
        print(length)
        print(gc)
        print(entropy)


        empty_df.to_csv(f"rowed_{algo}/synth_{algo}_{length}_{gc}_{entropy}.csv", index=False)

