from dataclasses import dataclass
import numpy as np


@dataclass()
class EEGData:
    ch_names: list
    data_arr: np.NDArray

    def __post_init__(self):
        if len(self.ch_names) != self.data_arr.shape[1]:
            raise ValueError("Length of 'ch_names' and 'data_arr' does not match.")
