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
finished = pd.read_csv(OUTPUT_CSV)

exercise_list = ', '.join(finished['Exercise'])

import argparse

parser = argparse.ArgumentParser(description = 'Transfer data from output exercises into overall data after completing',
                                 epilog=f'Current exercises: {exercise_list}')
parser.add_argument('-u','--up', help = "Yes/no input for 'up?' column; input in order of exercises (refer to -h) with commas and no spaces")
parser.add_argument('-d', '--date', help = 'Date (YYYY-MM-DD) of exercise completion')
args = parser.parse_args()

if __name__ == '__main__':
    finished['Date'] = pd.to_datetime(args.date, format = '%Y-%m-%d')
    uppies = str(args.up).split(',')
    finished['up?'] = uppies
    df = pd.concat(objs=[df, finished], axis=0, ignore_index=True)
    df.to_csv(DATA, index=False)
    with open(OUTPUT_TXT, 'w') as file:
        print('Finished and recorded', file=file)