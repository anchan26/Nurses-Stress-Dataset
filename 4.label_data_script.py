import pandas as pd
from datetime import timedelta, datetime
import numpy as np
import os


def parallel(id):
    new_df = pd.DataFrame(columns=['X', 'Y', 'Z', 'EDA', 'HR', 'TEMP', 'id', 'datetime', 'label'])

    sdf = df[df['id'] == id].copy()
    survey_sdf = survey_df[survey_df['ID'] == id].copy()

    for _, survey_row in survey_sdf.iterrows():
        ssdf = sdf[
            (sdf['datetime'] >= survey_row['Start datetime']) & (sdf['datetime'] <= survey_row['End datetime'])].copy()

        if not ssdf.empty:
            ssdf['label'] = np.repeat(survey_row['Stress level'], len(ssdf.index))
            new_df = pd.concat([new_df, ssdf], ignore_index=True)
        else:
            print(
                f"{survey_row['ID']} is missing label {survey_row['Stress level']} at {survey_row['Start datetime']} to {survey_row['End datetime']}")
    return new_df


# Read Files
print("Reading 1 ...")
PATH = "C:/Users/Akhil/Desktop/Project DSDM/Nurse/StressData/newdata"

df = pd.read_csv(os.path.join(PATH, 'merged_data.csv'), dtype={'id': str})
df['datetime'] = pd.to_datetime(df['datetime'].apply(lambda x: x * (10 ** 9)))

print("Reading 2 ...")
survey_path = 'C:/Users/Akhil/Desktop/Project DSDM/Nurse/StressData/SurveyResults.xlsx'

survey_df = pd.read_excel(survey_path, usecols=['ID', 'Start time', 'End time', 'date', 'Stress level'], dtype={'ID': str})
survey_df['Stress level'].replace('na', np.nan, inplace=True)  # replace missing values
survey_df.dropna(inplace=True)  # drop missing values

survey_df['Start datetime'] = pd.to_datetime(survey_df['date'].map(str) + ' ' + survey_df['Start time'].map(str))
survey_df['End datetime'] = pd.to_datetime(survey_df['date'].map(str) + ' ' + survey_df['End time'].map(str))
survey_df.drop(['Start time', 'End time', 'date'], axis=1, inplace=True)

# Convert SurveyResults.xlsx to GMT-00:00
print("Converting ...")
daylight = pd.to_datetime(datetime(2020, 11, 1, 0, 0))

# Convert time because data collection was performed in Central Standard Time, which is GMT-6 (according to the paper)
# Done in two parts depending on whether daylight savings are on or not
survey_df1 = survey_df[survey_df['End datetime'] <= daylight].copy()
survey_df1['Start datetime'] = survey_df1['Start datetime'].apply(lambda x: x + timedelta(hours=5))
survey_df1['End datetime'] = survey_df1['End datetime'].apply(lambda x: x + timedelta(hours=5))

survey_df2 = survey_df.loc[survey_df['End datetime'] > daylight].copy()
survey_df2['Start datetime'] = survey_df2['Start datetime'].apply(lambda x: x + timedelta(hours=6))
survey_df2['End datetime'] = survey_df2['End datetime'].apply(lambda x: x + timedelta(hours=6))

survey_df = pd.concat([survey_df1, survey_df2], ignore_index=True)
# survey_df = survey_df.loc[survey_df['Stress level'] != 1.0]

survey_df.reset_index(drop=True, inplace=True)

# Label Data
print('Labelling ...')
nurses = df['id'].unique()
results = []
for nurse in nurses:
    results.append(parallel(nurse))

new_df = pd.concat(results, ignore_index=True)

print('Saving ...')
new_df.to_csv(os.path.join(PATH, 'merged_data_labeled.csv'), index=False)
print('Done')


'''
Reading 1 ...
Reading 2 ...
Converting ...
Labelling ...
5C is missing label 1.0 at 2020-04-15 13:00:00 to 2020-04-15 14:00:00
5C is missing label 0.0 at 2020-06-12 07:00:00 to 2020-06-12 08:00:00
6D is missing label 1.0 at 2020-06-03 07:00:00 to 2020-06-03 09:00:00
7A is missing label 2.0 at 2020-07-07 19:16:00 to 2020-07-07 19:27:00
7A is missing label 2.0 at 2020-07-07 19:50:00 to 2020-07-07 20:09:00
7A is missing label 0.0 at 2020-07-07 20:24:00 to 2020-07-07 20:57:00
8B is missing label 2.0 at 2020-07-13 16:59:00 to 2020-07-13 17:05:00
15 is missing label 2.0 at 2020-07-24 19:54:00 to 2020-07-24 20:47:00
15 is missing label 0.0 at 2020-07-17 13:31:00 to 2020-07-17 13:40:00
15 is missing label 2.0 at 2020-07-17 13:59:00 to 2020-07-17 14:19:00
15 is missing label 2.0 at 2020-07-17 15:15:00 to 2020-07-17 15:18:00
15 is missing label 2.0 at 2020-07-17 17:21:00 to 2020-07-17 17:27:00
15 is missing label 2.0 at 2020-07-17 18:49:00 to 2020-07-17 19:16:00
15 is missing label 2.0 at 2020-07-17 20:00:00 to 2020-07-17 20:14:00
83 is missing label 2.0 at 2020-10-28 08:20:00 to 2020-10-28 08:52:00
83 is missing label 0.0 at 2020-10-28 09:44:00 to 2020-10-28 10:05:00
94 is missing label 1.0 at 2020-05-10 13:06:00 to 2020-05-10 13:38:00
94 is missing label 1.0 at 2020-06-24 18:50:00 to 2020-06-24 19:15:00
94 is missing label 0.0 at 2020-07-07 17:26:00 to 2020-07-07 17:33:00
94 is missing label 0.0 at 2020-07-07 19:47:00 to 2020-07-07 19:53:00
BG is missing label 0.0 at 2020-11-05 06:15:00 to 2020-11-05 06:17:00
BG is missing label 2.0 at 2020-12-07 00:58:00 to 2020-12-07 01:15:00
BG is missing label 0.0 at 2020-12-07 01:45:00 to 2020-12-07 02:18:00
E4 is missing label 2.0 at 2020-06-25 23:19:00 to 2020-06-26 00:19:00
E4 is missing label 2.0 at 2020-07-07 12:36:00 to 2020-07-07 12:55:00
E4 is missing label 2.0 at 2020-07-06 12:36:00 to 2020-07-06 12:55:00
E4 is missing label 2.0 at 2020-07-07 17:22:00 to 2020-07-07 19:00:00
EG is missing label 2.0 at 2020-11-08 19:30:00 to 2020-11-08 20:00:00
Saving ...
Done

Process finished with exit code 0
'''
