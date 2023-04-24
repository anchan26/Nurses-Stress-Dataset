# The Nursing Index: A multimodal sensor dataset

### Project Name
This project aims to detect stress level changes using physiological signals, specifically electrodermal activity (EDA), skin temperature, and heart rate. The project uses a sliding window approach to extract features from the physiological signals and applies the cumulative sum (CUSUM) algorithm to detect changes in stress levels.

### Table of Contents
# Getting Started
# Prerequisites
# Usage
# Results

## Getting Started
This project is based on the research paper "A multimodal sensor dataset for continuous stress detection of nurses in a hospital" by Seyedmajid Hosseini, Raju Gottumukkala, Satya Katragadda, Ravi teja Bhupatiraju, Ziad ashkar, Christoph W. Borst, and Kenneth Cochran. 

The dataset used in this project can be found at https://doi.org/10.5061/dryad.5hqbzkh6f.

## Installation
IDLE (Python 3.11), Jupyter Notebook

## Usage

The project consists of four Python scripts that can be used to unzip, combine, merge and label the signals for stress detection. The resulting output is a merged_data_labelled.csv file that can be used to predict nurses' stress levels. The Jupyter Notebook provided in this repository can be used to read the data and perform the stress level prediction.

## Results
Based on the machine learning model results, we were able to predict stress levels accuratelyusing the given features with an accuracy of 1.0 on the test set. This model was built using a Random Forest classifier, and we were able to find the best hyperparameters through grid search.We also identified participant 94 as exhibiting a significantly higher EDA level compared to the other participants, indicating a higher level of stress. Similarly, the analysis of HR data showed that participant 94 had the highest level of stress among all the participants. Furthermore, we implemented a change detection algorithm using the CUSUM method on  physiological signals collected over time. The algorithm computes features such as EDA mean, skin temperature mean, and heart rate, and we can detect changes in these features over time to identify stress-inducing events.
