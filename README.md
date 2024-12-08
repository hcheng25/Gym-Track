# "Gym Track"
This is a set of simple Python scripts I wrote primarily to automate my personal process of deciding what exercises I do when I go to the gym as well as practice some Python.

**Disclaimer:** I am not an expert, and my code simply picks exercises according to my personal methodology which I'll describe below.

## Function
The intended function of these scripts is to use information from a spreadsheet provided by the user to determine which exercises have not been done for the longest period of time, then relay the desired number of exercises to a text file. The spreadsheets and scripts process and output information about the weights used, sets, and reps for each exercise during each session. There is additionally a column in the input spreadsheet to indicate to the script if the difficulty should be increased via weights and/or reps the next time the exercise is called.

Difficulty is increased by increasing reps by a set value up to a maximumn number, at which point raising the difficulty again will reset the reps to a minimum value and increase the weight by a set increment.

## `.env` Setup
The scripts utilize variables set in a `.env` file. The following variables should be set by the user:
- DATA = path to a `.csv` file containing past workout data
- CONFIG = path to a `.csv` containing parameters to determine script behavior
- OUTPUT_TXT = path to a `.txt` output file
- OUTPUT_CSV = path to a `.csv` output file
- PER_DAY = number determining the desired number of exercises generated per session

### DATA
The DATA `.csv` file should contain the following columns:
- `Date`: Date that an exercise entry was performed
- `Exercise`: Name of the exercise performed - ensure names are consistently used (case-sensitivity, typos, etc.)
- `weight`: Amount of weight used
- `sets`: Number of sets in exercise session
- `reps`: Number of reps per set in exercise session
- `up?`: Variable indicating if the difficulty should be increased next time the same exercise is called
    - `'yes'` if user wants the next session to be more difficult
    - `'no'` if user wants the next session to be the same difficulty (weight, sets, reps all unchangedd)

### CONFIG
The DATA `.csv` file should contain the following columns:
- `exercises`: All exercise names as they appear on the `DATA` spreadsheet
- `weight_inc`: How much the weight for an exercise will increase when `up?` is set to `yes` and weight is increased
- `rep_inc`: How many reps more will be assigned for an exercise when `up?` is set to `yes` and reps are increased
- `min_rep`: The number that reps will be reset to when increasing weight
- `max_rep`: The maximum number of reps at which increasing difficulting will increase weight and reset reps to `min_rep` value

Each value can be set individually for each exercise using this spreadsheet.

### OUTPUT_TXT and OUTPUT_CSV
Both these paths simply point to the desired output location. When running the scripts, files should be created if they do not already exist and will be updated as appropriate. If the user does not follow the generated list of exercises, the output `.csv` file can be manually edited to ensure that the correct new data is added to the complete DATA spreadsheet when running `finish.py`.

**Note from me:** I find that copypasting the entire `.txt` file into a Google Tasks list is an easy way to create a checklist for working out using this output.

## `generate.py`
Running this script will create a list of exercises along with the respective stats for performing the exercises during the user's next workout. Running `generate.py` multiple times without running `finish.py` should output the same list of exercises each time, so there should be no adverse effects to running `generate.py` multiple times in a row.

## `finish.py`
Running this script along with the necessary `-u` and `-d` options will fill in the `up?` column based on the user's preferences and the `date` column, then add those entries to the overall spreadsheet so that the newly completed session can be taken into account upon next exercise generation.

### `-d`
The date should be input in the `%Y-%m-%d` format. For example, December 7, 2024 would be input as 2024-12-07.

### `-u`
Information on whether the user would like to up the difficult of an exercise next time it is generated should be entered in the form of yes or no. There must be one entry for each exercise, and the entries must be entered in the same order that the exercises are listed in the OUTPUT_CSV file. Separate entries using a comma and no space.

### `-h`
Using the `-h` option should display a description of the function along with a list of the exercises in the order they appear in the OUTPUT_CSV file. This can be used as a reference when entering the `-u` entries.

### Example usage
On November 12, 2024, I generated a list of six exercises named Exercise 1 through Exercise 6. After doing the exercises that day, I want to increase the difficulty of Exercise 2 and Exercise 4 the next time they are given to me. I would run the `finish.py` script as shown below:

`python3 finish.py -d 2024-11-12 -u no,yes,no,yes,no,no`