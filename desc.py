import pandas as pd
import statistics as stats
import os

base_header = f"synth_boyer_moore_64_0.2_1.1.csv"
csv2 = pd.read_csv(os.path.join("rowed_boyer_moore", base_header))
header_list = csv2.columns.tolist()


df = pd.DataFrame()

algos = ['bp', 'kmp', 'boyer_moore']
labels = ['real_time', '']

length = [64, 128, 256, 512, 1000, 2000]
gc = [0.2, 0.5, 0.8]
entropy = [0.3, 1.1, 1.9]


headers = ['base_name', 'mean', 'min', 'max', 'mode', 'std_dev', 'var', 'range', 'mean_dev', 'q1', 'q2', 'q3', 'iqr', 'label']

print("Header list", header_list)
empty_df = pd.DataFrame(columns=headers, index=[])

print(empty_df.head())

for algo in algos:
    empty_df = pd.DataFrame(columns=headers, index=[])

    for len in length:
        for g in gc:
            for ent in entropy:
                input_base_name = f"synth_{algo}_{len}_{g}_{ent}.csv"
                input_folder_name = f"rowed_{algo}"
                csv = pd.read_csv(os.path.join(input_folder_name, input_base_name))

                mean = csv['real_time'].mean()
                median = csv['real_time'].median()
                minimum = csv['real_time'].min()
                maximum = csv['real_time'].max()
                std_dev = csv['real_time'].std()  
                var = csv['real_time'].var()
                range_val = maximum - minimum
                mean_dev = stats.mean([abs(x - mean) for x in csv['real_time']])
                q1 = csv['real_time'].quantile(0.25)
                q2 = csv['real_time'].quantile(0.50)
                q3 = csv['real_time'].quantile(0.75)
                iqr = q3 - q1

                print("Mean of", input_base_name, "is", mean)
                print("Median of", input_base_name, "is", median)
                print("Max of", input_base_name, "is", maximum)
                print("Min of", input_base_name, "is", minimum)
                print("Std Dev of", input_base_name, "is", std_dev)
                print("Variance of", input_base_name, "is", var)
                print("Range of", input_base_name, "is", range_val)
                print("Mean Deviation of", input_base_name, "is", mean_dev)
                print("Quartile 1 of", input_base_name, "is", q1)
                print("Quartile 2 of", input_base_name, "is", q2)
                print("Quartile 3 of", input_base_name, "is", q3)
                print("Interquartile Range of", input_base_name, "is", iqr)
                print("--------------------------------------------------") 


                new_row_df = pd.DataFrame({
                    'base_name': [input_base_name],
                    'mean': [mean],
                    'min': [minimum],
                    'max': [maximum],
                    'mode': [median],
                    'std_dev': [std_dev],
                    'var': [var],
                    'range': [range_val],
                    'mean_dev': [mean_dev],
                    'q1': [q1],
                    'q2': [q2],
                    'q3': [q3],
                    'iqr': [iqr],
                    'label': ['real_time']
                })
                
                empty_df = pd.concat([empty_df, new_row_df], ignore_index=True)
                    
    empty_df.to_csv(f"desc_rowed_{algo}/desc_rowed_synth_{algo}.csv", index=False)

