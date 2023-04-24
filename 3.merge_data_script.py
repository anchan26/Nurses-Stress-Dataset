""" Creates a single data frame that has all the info from all the nurses.
Missing values in the time series have been filled by upsampling where needed. """

import pandas as pd
import os


def read_signal(signal):
    df = pd.read_csv(os.path.join(COMBINED_DATA_PATH, f"combined_{signal}.csv"), dtype={'id': str})
    return df


def merge(id):
    print(f"Processing {id}")
    df = pd.DataFrame(columns=columns)

    acc_id = acc[acc['id'] == id]  # this was already downsampled in '2.combine_data_script.py'
    eda_id = eda[eda['id'] == id].drop(['id'], axis=1)
    hr_id = hr[hr['id'] == id].drop(['id'], axis=1)
    temp_id = temp[temp['id'] == id].drop(['id'], axis=1)

    df = acc_id.merge(eda_id, on='datetime', how='outer')
    df = df.merge(temp_id, on='datetime', how='outer')
    df = df.merge(hr_id, on='datetime', how='outer')

    df.fillna(method='ffill', inplace=True)
    df.fillna(method='bfill', inplace=True)

    return df


COMBINED_DATA_PATH = "C:/Users/Akhil/Desktop/Project DSDM/Nurse/StressData/processed_data2"
SAVE_PATH = "C:/Users/Akhil/Desktop/Project DSDM/Nurse/StressData/newdata"

if COMBINED_DATA_PATH != SAVE_PATH:
    os.mkdir(SAVE_PATH)

print("Reading data ...")

acc, eda, hr, temp = None, None, None, None

signals = ['acc', 'eda', 'hr', 'temp']


acc = read_signal('acc')
eda = read_signal('eda')
hr = read_signal('hr')
temp = read_signal('temp')

# Merge data
print('Merging Data ...')
nurses = eda['id'].unique()
columns = ['X', 'Y', 'Z', 'EDA', 'HR', 'TEMP', 'id', 'datetime']

results = []
for nurse in nurses:
    results.append(merge(nurse))
new_df = pd.concat(results, ignore_index=True)

print("Saving data ...")
new_df.to_csv(os.path.join(SAVE_PATH, "merged_data.csv"), index=False)
