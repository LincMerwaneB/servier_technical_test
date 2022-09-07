""" This module import csv and json files inside a dataframe """
from os import listdir
from os.path import isfile, join
from pathlib import Path
import warnings
import pandas as pd
import numpy as np


# init data files path
path_files = Path(Path(__file__).parents[1], 'data')

# column header for publication files
columns_name_publication = ['id', 'title', 'date', 'journal']

# column header for drugs files
columns_name_drugs = ['atccode', 'drug']


def get_files_from_dir(path=path_files):
    """Gets a list of all files in the directory

    If the argument `path` isn't passed in, the default path_files is used.

    Parameters
    ----------
    path : str, optional
        Path to a directory (default is path)

    Returns
    -------
    list
        a list of files in the directory
    path object
        a path to join a directory

    Raises
    ------
    ValueError
        No file in the directory.
    """

    list_files = [f for f in listdir(path) if isfile(join(path, f))]

    if len(list_files) == 0:
        raise ValueError('No files to process')
    return list_files, path


def get_path_file_from_dir(path=path_files):
    """Gets a list of path to all csv and json files in the directory

    If the argument `path` isn't passed in, the default path_files is used.

    Parameters
    ----------
    path : str, optional
        Path to a directory (default is path)

    Returns
    -------
    list
        list of paths to csv files that contain drugs name
    list
        list of paths to csv files in the directory
    list
        list of paths to json files in the directory

    Raises
    ------
    ValueError
        No files with drugs data.
        No files with journal data.
    """

    drugs = []
    files_csv = []
    files_json = []

    # gets files
    list_files, path = get_files_from_dir(path)
    for name_file in list_files:
        file = Path(path, name_file)
        # gets paths to files that contain drugs
        if name_file.split('.')[0].find('drugs') != -1 and name_file.split('.')[-1] == 'csv':
            drugs.append(file)
        # I separate files according to file type to simplify import via pandas
        elif name_file.split('.')[-1] == 'csv':
            files_csv.append(file)
        elif name_file.split('.')[-1] == 'json':
            files_json.append(file)

    # checking for empty files
    if len(drugs) == 0:
        raise ValueError('No files with drugs data')
    if len(files_csv) == 0 and len(files_json) == 0:
        raise ValueError('No files with journal data')
    print('==> Files ready to import')
    return drugs, files_csv, files_json


def import_list_file(list_file, extension):
    """Import csv and json files from path list inside a dataframe.

    Parameters
    ----------
    list_file : list of path
    extension : type of list ( csv or json )

    Returns
    -------
    dataframe
        a dataframe with the concat of file
    None
        None
    """

    list_df_concat = []
    for file in list_file:
        try:
            if extension == 'csv':
                # adding a source column that contains the origin of the publications
                df_file = pd.read_csv(file,
                                      names=columns_name_publication,
                                      skiprows=1,
                                      parse_dates=['date'],
                                      encoding='utf8').assign(source=file.stem)
            elif extension == 'json':
                df_file = pd.read_json(file,
                                       convert_dates='date',
                                       encoding='utf8').assign(source=file.stem)
            list_df_concat.append(df_file)
        except Exception as error_import:
            print(type(error_import), error_import, file)
    if len(list_df_concat) == 0:
        return None
    return pd.concat(list_df_concat, ignore_index=True)


def import_dir_to_dataframe(path=path_files):
    """Import csv and json files from the specified directory and load them inside a dataframe

    If the argument `path` isn't passed in, the default path_files is used.

    Parameters
    ----------
    path : str, optional
        Path to a directory (default is path)

    Returns
    -------
    dataframe
        a dataframe that contains drugs
    dataframe
        a dataframe that contains publication

    Raises
    ------
    ValueError
        No drugs header.
        Missing data.

    """

    drugs, files_csv, files_json = get_path_file_from_dir(path)
    # show files ready to be imported
    print('Filename :\n'
          '\tdrug_file : {}\n\tcsv : {}\n\tjson : {}'.format(drugs, files_csv, files_json))

    # loading the drug list into a dataframe
    df_drugs = pd.concat((pd.read_csv(f,
                                      names=columns_name_drugs,
                                      skiprows=1) for f in drugs))
    # drug column check
    if 'drug' not in list(df_drugs.columns):
        raise ValueError("Files {} does not contain a column with the header 'drug'".format(drugs))

    if len(files_csv) != 0 and len(files_json) != 0:
        df_csv = import_list_file(files_csv, 'csv')
        df_json = import_list_file(files_json, 'json')
        # concatenation of the 2 previous dataframes in order to handle only one object
        df_journal = pd.concat([df_csv, df_json], ignore_index=True)

    elif len(files_csv) != 0 and len(files_json) == 0:
        df_journal = import_list_file(files_csv, 'csv')

    elif len(files_csv) == 0 and len(files_json) != 0:
        df_journal = import_list_file(files_json, 'json')

    # test to verify that the fields have been populated
    if len(df_journal['title']) == 0 or len(df_journal['journal']) == 0 or len(df_drugs['drug']) == 0:
        raise ValueError('Missing data\ndrug : {}, title : {}, journal : {}'.format(len(df_drugs['drug']), 
                                                                                    len(df_journal['title']), 
                                                                                    len(df_journal['journal'])))
    df_drugs, df_journal = data_cleaning(df_drugs, df_journal)
    return df_drugs, df_journal


def data_cleaning(df_drugs, df_journal):
    """ Clean the dataframe by deleting byte char and add id columns

    Parameters
    ----------
    df_drugs : dataframe
    df_journal : dataframe

    Returns
    -------
    dataframe
        a dataframe that contains drugs
    dataframe
        a dataframe that contains publication

    Raises
    ------
    TypeError
        New id attribution failed

    Warning
    ------
    Warn
        Missing value deleted
    ValueError
        Missing data.
    """

    # check to make sure that the drugs are in capital letters
    df_drugs['drug'] = df_drugs['drug'].str.upper()

    # check unicity
    df_drugs = df_drugs.drop_duplicates()
    df_journal = df_journal.drop_duplicates()

    # cleaning dataframe
    df_journal['title'] = df_journal['title'].replace('  ', '')
    # add id if precdent is a row_number
    for i, row in df_journal.iterrows():
        if row['id'] == '' or row['id'] == np.NaN:
            df_journal.at[i, 'id'] = np.NaN
            df_id = df_journal['id'].dropna().loc[df_journal['source'] == row['source']]
            try:
                max_id = df_id.astype('int').max()
                df_journal.at[i, 'id'] = max_id + 1
            except TypeError as argument:
                print("New id attribution failed\n", argument)
        if isinstance(row['journal'], str):
            df_journal.at[i, 'journal'] = row['journal'].replace('\\xc3\\x28', '')
            # check other value
            if df_journal.at[i, 'journal'].find('\\') != -1:
                warnings.warn('Clean journal data :\n\tid : {}, journal : {}, source : {} '.format(row['id'], 
                                                                                                   row['journal'], 
                                                                                                   row['source']))
        if isinstance(row['title'], str):
            df_journal.at[i, 'title'] = row['title'].replace('\\xc3\\xb1', '')
            if df_journal.at[i, 'title'].find('\\') != -1:
                warnings.warn('Clean title data :\n\tid : {}, title : {}, source : {} '.format(row['id'], 
                                                                                               row['title'], 
                                                                                               row['source']))
        if row['title'] == '':
            df_journal.at[i, 'title'] = np.NaN

    # fusion row with same title and same date
    df_journal = df_journal.groupby(['title', 'date']).first().reset_index()

    # delete null value
    if df_drugs['drug'].isnull().any() is True:
        warnings.warn('Missing drug row deleted')
        df_drugs.dropna(subset=['drug'], how='any', inplace=True)
    if df_journal['title'].isnull().any() is True:
        warnings.warn("Missing title deleted")
        df_journal.dropna(subset=['title'], how='any', inplace=True)
    if df_journal['journal'].isnull().any() is True:
        warnings.warn("Missing journal")
        # i leave the journal empty because if the title is filled it can useful
        df_journal['journal'].fillna('Empty', inplace=True)
    if df_journal['id'].isnull().any() is True:
        warnings.warn("Missing id")

    # create new id for journal
    cols_journal = columns_name_publication
    cols_journal.append('source')
    df_journal = df_journal[cols_journal]
    df_journal['id_source'] = df_journal[['source']].groupby(['source']).cumcount()+1
    distinct_journal = df_journal[['journal']].drop_duplicates()
    distinct_journal['id_journal'] = distinct_journal['journal'].rank()
    df_journal = df_journal.merge(distinct_journal, left_on='journal', right_on='journal')
    # test to verify that the fields have been populated
    if len(df_journal['title']) == 0 or len(df_journal['journal']) == 0 or len(df_drugs['drug']) == 0:
        raise ValueError('Missing data\ndrug : {}, title : {}, journal : {}'.format(len(df_drugs['drug']),
                                                                                    len(df_journal['title']), 
                                                                                    len(df_journal['journal'])))

    return df_drugs, df_journal
