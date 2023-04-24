

import os
import pandas as pd

DATA_PATH = "C:/Users/Akhil/Desktop/Project DSDM/Nurse/StressData/Stress_dataset"
SAVE_PATH = "C:/Users/Akhil/Desktop/Project DSDM/Nurse/StressData/processed_data2"
os.mkdir(SAVE_PATH)

final_columns = {
    'ACC': ['id', 'X', 'Y', 'Z', 'datetime'],
    'EDA': ['id', 'EDA', 'datetime'],
    'HR': ['id', 'HR', 'datetime'],
    'TEMP': ['id', 'TEMP', 'datetime'],
}

names = {
    'ACC.csv': ['X', 'Y', 'Z'],
    'EDA.csv': ['EDA'],
    'HR.csv': ['HR'],
    'TEMP.csv': ['TEMP'],
}

desired_signals = ['ACC.csv', 'EDA.csv', 'HR.csv', 'TEMP.csv']

acc = pd.DataFrame(columns=final_columns['ACC'])
eda = pd.DataFrame(columns=final_columns['EDA'])
hr = pd.DataFrame(columns=final_columns['HR'])
temp = pd.DataFrame(columns=final_columns['TEMP'])


def process_df(df, file):
    start_timestamp = df.iloc[0, 0]
    sample_rate = df.iloc[1, 0]
    new_df = pd.DataFrame(df.iloc[2:].values, columns=df.columns)  # skip first two rows
    new_df['id'] = file[-2:]
    new_df['datetime'] = [(start_timestamp + i/sample_rate) for i in range(len(new_df))]
    if sample_rate > 4:  # Done by Ana to avoid a ridiculously large ACC file
        # Downsample to 4 Hz
        ds_factor = int(sample_rate / 4)
        new_df = new_df.iloc[::ds_factor, :]
    return new_df

nurses = ['5C', '6B', '6D', '7A', '7E', '8B', '15', '83', '94', 'BG', 'CE', 'DF', 'E4', 'EG', 'F5']

for nurse in nurses:
    print(f'Processing nurse {nurse}')
    for sub_file in os.listdir(os.path.join(DATA_PATH, nurse)):
        if not sub_file.endswith(".zip"):
            for signal in os.listdir(os.path.join(DATA_PATH, nurse, sub_file)):
                if signal in desired_signals:
                    df = pd.read_csv(os.path.join(DATA_PATH, nurse, sub_file, signal), names=names[signal], header=None)
                    if not df.empty:
                        if signal == 'ACC.csv':
                            acc = pd.concat([acc, process_df(df, nurse)])
                        if signal == 'EDA.csv':
                            eda = pd.concat([eda, process_df(df, nurse)])
                        if signal == 'HR.csv':
                            hr = pd.concat([hr, process_df(df, nurse)])
                        if signal == 'TEMP.csv':
                            temp = pd.concat([temp, process_df(df, nurse)])


print('Saving Data ...')
acc.to_csv(os.path.join(SAVE_PATH, 'combined_acc.csv'), index=False)
eda.to_csv(os.path.join(SAVE_PATH, 'combined_eda.csv'), index=False)
hr.to_csv(os.path.join(SAVE_PATH, 'combined_hr.csv'), index=False)
temp.to_csv(os.path.join(SAVE_PATH, 'combined_temp.csv'), index=False)
