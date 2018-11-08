"""
Cleanses the data in a .csv file for a sports event. Data from the sport event is stored in a table, and  must conform
to the following rules:

  Column Num.             Data             Max Characters                       Format Rules
 ------------ -------------------------- ---------------- ------------------------------------------------------
            1   Athlete Identifier                      6   whole number
            2   Event Name                             30   letters, digits, space, hyphen & apostrophe
            3   Athlete’s First Name                   30   letters, digits, space, hyphen & apostrophe
            4   Athlete’s Surname                      30   letters, digits, space, hyphen & apostrophe
            5   Country Code                            3   uppercase letters
            6   Place (current or final)                3   whole number or one of three strings (DNS, DNF, PEN)
            7   Score                                   6   whole or floating-point number
            8   Time                                    8   whole or floating-point number
            9   Medal                                   6   Gold, Silver or Bronze
           10   Olympic Record (if set)                 8   whole or floating-point number
           11   World Record (if set)                   8   whole or floating-point number
           12   Track Record (if set)                   8   whole or floating-point number
 ------------ -------------------------- ---------------- ------------------------------------------------------
+ Columns 1 to 5 must have data in every row.
+ If column 6 contains a whole number then there must be a legal value in columns 7 or 8, but not both.
+ If column 9 contains a legal value then column 6 must have an appropriate value (e.g. Gold must be for first place,
    Silver for second place and Bronze for third place).
+ Columns 10 to 12 do not need to correspond to first place in column 6 (e.g. it is possible for an athlete to set a
    world record in a qualifying round and then not win a medal in the  final rounds).
+ The value in columns 10 to 12 does not need to be the same as the value in columns 7 or 8 (e.g. the athlete does worse
    in the final than when setting the record in a qualifying round).
+ If column 11 contains a legal value then it must equal the value in column 10.
"""

__author__ = "Caleb Aitken 45309414"



from assign1_utilities import get_column, replace_column, truncate_string
import re

# declare global constants for data based on rules (see above docstring)
MAX_CHARACTERS_COLUMN_2 = 30
MAX_CHARACTERS_COLUMN_3 = 30
MAX_CHARACTERS_COLUMN_4 = 30
MAX_CHARACTERS_COLUMN_5 = 3
MAX_CHARACTERS_COLUMN_6 = 3
MAX_CHARACTERS_COLUMN_7 = 6
MAX_CHARACTERS_COLUMN_8 = 8
MAX_CHARACTERS_COLUMN_10 = 8
MAX_CHARACTERS_COLUMN_11 = 8
MAX_CHARACTERS_COLUMN_12 = 8
LEGAL_CHARACTERS_COLUMNS_2_3_4 = r'[\s^a-zA-Z0-9À-ú\-\']'
LEGAL_CHARACTERS_COLUMN_5 = r'[A-Z]'
LEGAL_CHARACTERS_COLUMN_6 = r'[0-9DEFNPS]'
LEGAL_CHARACTERS_COLUMNS_7_8_10_11_12 = r'[0-9\.]'
LEGAL_STRINGS_COLUMN_6 = ["", "DNF", "DNS", "PEN"]
LEGAL_STRINGS_COLUMN_9 = ["", "Gold", "Silver", "Bronze"]


def truncate_names_in_row(row):
    """Return the row with columns 2, 3, & 4 truncated

    Parameters
        row (list): list of columns in the row

    Return
        row (list): list of columns in the row now with column 2, 3, & 4 truncated

    Preconditions
        row != None
    """

    row[1] = truncate_string(row[1], MAX_CHARACTERS_COLUMN_2)
    row[2] = truncate_string(row[2], MAX_CHARACTERS_COLUMN_3)
    row[3] = truncate_string(row[3], MAX_CHARACTERS_COLUMN_4)
    return row


def case_correction(row):
    """Return the row with with the correct case for columns 5, 6, & 8

     Parameters
        row (list): list of columns in the row

    Return
        row (list): list of columns in the row now with column 2, 3, & 4 case corrected

    Preconditions
        row != None
    """

    if row[4].isalpha():
        row[4] = row[4].upper()
    if row[5].isalpha():
        row[5] = row[5].upper()
    if row[8].isalpha():
        row[8] = row[8].capitalize()
    return row


def validate_column_length(row):
    """Returns true if any column exceeds its respective character limit

    Parameters
        row (list): list of columns in the row

    Return
        bool: true is any column exceeds its respective character length, false otherwise

    Preconditions
        row != None
    """

    if len(row[1]) > MAX_CHARACTERS_COLUMN_2:
        return True
    elif len(row[2]) > MAX_CHARACTERS_COLUMN_3:
        return True
    elif len(row[3]) > MAX_CHARACTERS_COLUMN_4:
        return True
    elif len(row[4]) > MAX_CHARACTERS_COLUMN_5:
        return True
    elif len(row[5]) > MAX_CHARACTERS_COLUMN_6:
        return True
    elif len(row[6]) > MAX_CHARACTERS_COLUMN_7:
        return True
    elif len(row[7]) > MAX_CHARACTERS_COLUMN_8:
        return True
    elif len(row[9]) > MAX_CHARACTERS_COLUMN_10:
        return True
    elif len(row[10]) > MAX_CHARACTERS_COLUMN_11:
        return True
    elif len(row[11]) > MAX_CHARACTERS_COLUMN_12:
        return True
    else:
        return False


def validate_column_format(row):
    """Returns true if any column (excluding column 9) contains an illegal character

    Parameters
        row (list): list of columns in the row

    Return
        bool: true if an illegal character is found, false otherwise

    Preconditions
        row != None
    """

    if not re.sub(LEGAL_CHARACTERS_COLUMNS_2_3_4, '', row[1]) == '':
        return True
    elif not re.sub(LEGAL_CHARACTERS_COLUMNS_2_3_4, '', row[2]) == '':
        return True
    elif not re.sub(LEGAL_CHARACTERS_COLUMNS_2_3_4, '', row[3]) == '':
        return True
    elif not re.sub(LEGAL_CHARACTERS_COLUMN_5, '', row[4]) == '':
        return True
    elif not re.sub(LEGAL_CHARACTERS_COLUMN_6, '', row[5]) == '':
        return True
    elif not re.sub(LEGAL_CHARACTERS_COLUMNS_7_8_10_11_12, '', row[6]) == '':
        return True
    elif not re.sub(LEGAL_CHARACTERS_COLUMNS_7_8_10_11_12, '', row[7]) == '':
        return True
    elif not re.sub(LEGAL_CHARACTERS_COLUMNS_7_8_10_11_12, '', row[9]) == '':
        return True
    elif not re.sub(LEGAL_CHARACTERS_COLUMNS_7_8_10_11_12, '', row[10]) == '':
        return True
    elif not re.sub(LEGAL_CHARACTERS_COLUMNS_7_8_10_11_12, '', row[11]) == '':
        return True
    else:
        return False


def validate_column_strings(row):
    """Returns true if column 6 or 9 contain an illegal string

    Parameters
        row (list): list of columns in the row

    Return
        bool: true if an illegal string is found, false otherwise

    Preconditions
        row != None
    """
    if row[5].isalpha() and row[5] not in LEGAL_STRINGS_COLUMN_6:
        return True
    elif row[8] not in LEGAL_STRINGS_COLUMN_9:
        return True
    else:
        return False


def validate_row_logic(row):
    """Returns true if any row-wide rules are broken (ie, columns 1 to 5 must contain data)

    Parameters
        row (list): list of columns in the row

    Return
        bool: true if any rules are broken, false otherwise

    Preconditions
        row != None
    """
    # columns 1 to 5 must contain data (note column 1 is removed regardless)
    if row[1] == "":
        return True
    elif row[2] == "":
        return True
    elif row[3] == "":
        return True
    elif row[4] == "":
        return True

    # if column 6 contains a whole number then there must be a legal value in columns 7 or 8, but not both
    if row[5].isdigit() and not row[6] and not row[7]:
        return True
    elif row[6] and row[7]:
        return True

    # if column 9 contains a legal value then column 6 must have an appropriate value (e.g. Gold must be for first
    #   place, Silver for second place and Bronze for third place)
    if row[5] == "1" and not row[8] == "Gold":
        return True
    elif row[5] == "2" and not row[8] == "Silver":
        return True
    elif row[5] == "3" and not row[8] == "Bronze":
        return True

    # if column 11 contains a legal value then it must equal the value in column 10
    if row[10] != "" and row[10] != row[9]:
        return True

    return False


def main():
    """Main functionality of program."""
    with open("athlete_data.csv", "r") as raw_data_file, \
            open("athlete_data_clean.csv", "w") as clean_data_file:
        for row in raw_data_file:
            corrupt = False

            # clean data; make it more manageable
            row_to_process = row.split(',')  # converts the row_to_process from a string to a list
            row_to_process[11] = row_to_process[11].rstrip('\n')  # removes newline from final column
            row_to_process = truncate_names_in_row(row_to_process)  # truncates columns 2, 3, & 4
            row_to_process = case_correction(row_to_process)  # corrects the case of strings in th row

            # check for corruption, set corrupt to true if any errors are found
            if validate_column_length(row_to_process):  # true if any column exceeds its character limit
                corrupt = True
            elif validate_column_format(row_to_process):  # true if any column contains illegal characters
                corrupt = True
            elif validate_column_strings(row_to_process):  # true if column 6 or 9 contain an illegal string
                corrupt = True
            elif validate_row_logic(row_to_process):  # true if the row contains fallacies
                corrupt = True

            # remove the first column from row_to_process and the original row
            row = row.split(',')  # converts the row from a string to a list
            row = row[1:len(row)]  # removes athlete id from row (first column)
            row_to_process = row_to_process[1:len(row_to_process)]  # removes athlete id from row_to_process (1st col.)

            # revert row and row_to_process to data type string
            row_to_process = ','.join(row_to_process)
            row = ','.join(row)

            # Save the row data to the cleaned data file
            if not corrupt:
                clean_data_file.write(row_to_process + '\n')
            else:
                clean_data_file.write(row + ",CORRUPT" + '\n')


# Call the main() function if this module is executed
if __name__ == "__main__":
    main()
