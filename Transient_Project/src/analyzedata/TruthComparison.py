"""Compare observed distributions of event properties
with true distributions

DEPRECATED
"""
import numpy as np
from scipy import stats
from copy import copy


#This tests for if the distributions have consistent shapes
def kolmoSmir(truth, observation):
    """Return the KS statistic for the truth-observed samples"""
    return stats.ks_2samp(truth, observation)