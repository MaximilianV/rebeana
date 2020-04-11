import numpy as np
from typing import List, Dict
from utils.Configuration import Configuration


class CorrelationResult:
    pearson: np.ndarray
    spearman: np.ndarray
    normality: np.ndarray


    def __init__(self, inputs_len, outputs_len):
        self.pearson = np.full((inputs_len, outputs_len), np.nan, np.int8)
        self.spearman = np.full((inputs_len, outputs_len), np.nan, np.int8)
        self.normality = np.full((1, inputs_len + outputs_len), np.nan, np.int8)

    def add_pearson(self, value, input, output):
        self.pearson[input][output] = value[0]

    def add_spearman(self, value, input, output):
        self.spearman[input][output] = value

    def add_correlation(self, pearson, spearman, input, output):
        self.add_pearson(pearson, input, output)
        self.add_spearman(spearman, input, output)

    def add_normality(self, value, metric):
        self.pearson[metric] = value
