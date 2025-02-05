import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

DATA = os.getenv('DATA')
CONFIG = os.getenv('CONFIG')
OUTPUT_TXT = os.getenv('OUTPUT_TXT')
OUTPUT_CSV = os.getenv('OUTPUT_CSV')
per_day = int(os.getenv('PER_DAY'))

config = pd.read_csv(CONFIG)
df = pd.read_csv(DATA)

import argparse

parser = argparse.ArgumentParser(description = 'Generate a list of exercises with weight, sets, and reps, based on the per_day and config set in .env')
args = parser.parse_args()

if __name__ == '__main__':
    # 1. find most recent entry for each exercise
    recent = []
    for i in range(len(config['exercises'])):
        current = df[df['Exercise']==config.loc[i, 'exercises']]
        recent.append(current['Date'].idxmax())
    recent = df.loc[recent]
    recent = recent.sort_values(by='Date').reset_index(drop=True).loc[range(per_day)] # 2. order those entries by date, 3. select the six oldest entries i.e. the six exercises that have been done the longest time ago
    recent = recent.sort_values(by='Exercise', ignore_index=True)

    # 4. increase reps/weights where `up?` is `yes` based on config
    for i in range(len(recent['up?'])):
        current_exercise = recent.loc[i, 'Exercise']
        ref_index = int(config.loc[config['exercises']==current_exercise].index[0])
        if recent.loc[i, 'up?']=='yes':
            recent.loc[i, 'weight'] += config.loc[ref_index,'weight_inc']

    # 5. empty `Date` and `up?` columns
    recent['Date'] = None
    recent['up?'] = None

    # 6. export to csv output
    recent.to_csv(OUTPUT_CSV, index=False)

    # 7. output to txt output
    with open(OUTPUT_TXT, 'w') as file:
        for i in range(len(recent['Exercise'])):
            exercise = recent.loc[i, 'Exercise']
            weight = recent.loc[i, 'weight']
            print(f'{exercise} {weight} lb', file=file)