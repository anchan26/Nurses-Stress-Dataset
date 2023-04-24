import os
import shutil

MAIN_PATH = 'C:/Users/Akhil/Desktop/Project DSDM/Nurse/'

nurses = ['5C', '6B', '6D', '7A', '7E', '8B', '15', '83', '94', 'BG', 'CE', 'DF', 'E4', 'EG', 'F5']

shutil.unpack_archive(MAIN_PATH + 'StressData.zip', MAIN_PATH + 'StressData')
shutil.unpack_archive(MAIN_PATH + 'StressData/Stress_dataset.zip', MAIN_PATH + 'StressData/Stress_dataset')

stress_data_path = MAIN_PATH + '/StressData/Stress_dataset'


new_list = [(file, sub_file) for file in nurses
            for sub_file in os.listdir(os.path.join(stress_data_path, file))
            ]

def unzip(file, sub_file):
    shutil.unpack_archive(
        os.path.join(stress_data_path, file, sub_file), 
        os.path.join(stress_data_path, file, sub_file[:-4])
    )

counter = 1
for f, n in new_list:
    print(counter, f, n)
    unzip(f, n)
    counter += 1
