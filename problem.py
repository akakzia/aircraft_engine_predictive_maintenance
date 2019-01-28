from __future__ import division, print_function
import os
import datetime

import warnings
import numpy as np
import pandas as pd
from sklearn.model_selection import KFold
from sklearn.metrics import log_loss, recall_score, precision_score

import rampwf as rw
from rampwf.score_types.base import BaseScoreType
from rampwf.score_types.classifier_base import ClassifierBaseScoreType
from rampwf.workflows.feature_extractor import FeatureExtractor
from rampwf.workflows.classifier import Classifier


problem_title = 'Predictive maintenance for aircraft engines'





# -----------------------------------------------------------------------------
# Training / testing data reader
# -----------------------------------------------------------------------------


def _read_data(path, type_):

    fname1 = '{}_FD001.txt'.format(type_)
    fname2 = '{}_FD003.txt'.format(type_)

    fp1 = os.path.join(path, 'data', fname1)
    fp2 = os.path.join(path, 'data', fname2)

    df1 = pd.read_csv(fp1, sep=' ', header=None)
    df2 = pd.read_csv(fp2, sep=' ', header=None)

    #Merging data
    df2[0] = df2[0] + df1[0].max()
    frames = [df1, df2]
    data = pd.concat(frames)
    data.reset_index(level=0, inplace=True)
    data.drop(['index'], axis=1, inplace=True)

    data.drop([26, 27], axis=1, inplace=True)
    column_name = ['ID', 'Cycle', 'op_set_1', 'op_set_2', 'op_set_3', 's1', 's2', 's3', 's4', 's5', 's6', 's7', 's8',
                   's9',
                   's10', 's11', 's12', 's13', 's14', 's15', 's16', 's17', 's18', 's19', 's20', 's21']
    data.columns = column_name

    ## TTF calculation

    failure_cycle = pd.DataFrame(data.groupby('ID')['Cycle'].max())
    failure_cycle.reset_index(level=0, inplace=True)
    failure_cycle.columns = ['ID', 'ttf']

    data_merged = pd.merge(data, failure_cycle, on='ID')
    data_merged['ttf'] = data_merged['ttf'] - data_merged['Cycle']

    ## labeling data
    data_merged['ttf'] = data_merged['ttf'].apply(lambda x: 0 if x <= 10 else 1 if x <= 30 else 2 if x <= 100 else 3)
    y = data_merged[['ID', 'ttf']].set_index('ID')['ttf']

    # for the "quick-test" mode, use less data
    test = os.getenv('RAMP_TEST_MODE', 0)
    if test:
        N_small = 5000
        data = data[:N_small]
        y = y[:N_small]

    return data, y


def get_train_data(path='.'):
    return _read_data(path, 'train')


def get_test_data(path='.'):
    return _read_data(path, 'test')
