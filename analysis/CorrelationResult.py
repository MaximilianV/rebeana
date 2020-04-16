import numpy as np
from typing import List, Dict


class CorrelationResult:
    pearson: np.ndarray
    pearson_p: np.ndarray
    spearman: np.ndarray
    spearman_p: np.ndarray
    normality: np.ndarray


    def __init__(self, inputs_len, outputs_len):
        self.pearson = np.full((inputs_len, outputs_len), np.nan, np.float32)
        self.pearson_p = np.full((inputs_len, outputs_len), np.nan, np.float32)
        self.spearman = np.full((inputs_len, outputs_len), np.nan, np.float32)
        self.spearman_p = np.full((inputs_len, outputs_len), np.nan, np.float32)
        self.normality = np.full((1, inputs_len + outputs_len), np.nan, np.float32)

    def add_pearson(self, value, input, output):
        self.pearson[input][output] = value[0]
        self.pearson_p[input][output] = value[1]

    def add_spearman(self, value, input, output):
        self.spearman[input][output] = value[0]
        self.spearman_p[input][output] = value[1]

    def add_correlation(self, input, output, pearson=np.nan, spearman=np.nan):
        self.add_pearson(pearson, input, output)
        self.add_spearman(spearman, input, output)

    def add_normality(self, value, metric):
        self.pearson[metric] = value
