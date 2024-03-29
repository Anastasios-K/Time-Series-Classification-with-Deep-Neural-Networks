import numpy as np
import pandas as pd
from src.interface.interface import Creator
from src.config.load_conifg import Configurator


class LabelCreator(Creator):
    __shifted_col = "Shifted"
    __diff_col = "Diff"

    @classmethod
    def _calc_price_difference(cls, data: pd.DataFrame, config: Configurator) -> pd.DataFrame:
        """
        Shift Close feature by 1.
        Use the shifted and original Close features to calculate the percent difference.
        Add the 2 new features (shifted close and difference) in the given dataset.
        """
        temp_df = data.copy()
        temp_df[cls.__shifted_col] = temp_df[config.dfstructure.close].shift(1)
        temp_df[cls.__diff_col] = (temp_df[config.dfstructure.close] / temp_df[cls.__shifted_col]) - 1
        return temp_df

    @classmethod
    def create_labels(cls, data: pd.DataFrame, config: Configurator) -> (pd.DataFrame, pd.Series):
        """
        Call the _calc_price_difference to get the 2 new features (shifted close and difference).
        Create 3 classes based on the 3 conditions below and put them into the label attribute.
        Also consider a tollerance factor during the creation process.
        Drop the unused features (shifted close and difference).
        Drop the row with Nan values generated because of the shifting action.
        Synchonise the data and labels based on the timestamp.
        """
        # data with difference feature
        data_with_diff = cls._calc_price_difference(
            data=data,
            config=config
        )
        # tollerance factor
        tollerance = config.labeltolerance.tolerance
        # condition 1
        data_with_diff.loc[
            data_with_diff[cls.__diff_col] > tollerance,
            config.dfstructure.labels
        ] = 0
        # condition 2
        data_with_diff.loc[
            data_with_diff[cls.__diff_col] < -tollerance,
            config.dfstructure.labels
        ] = 1
        # condition 3
        data_with_diff.loc[
            (data_with_diff[cls.__diff_col] < tollerance) &
            (data_with_diff[cls.__diff_col] > -tollerance),
            config.dfstructure.labels
        ] = 2
        # drop Nan values and unused features
        data_with_diff.dropna(inplace=True)
        labels = data_with_diff[config.dfstructure.labels]
        data = data_with_diff.drop(
            columns=[
                cls.__diff_col,
                cls.__shifted_col,
                config.dfstructure.labels
            ]
        )

        return data, labels

    @classmethod
    def create_label_weights(cls, train_labels: np.ndarray) -> dict:
        """
        Calculate class weights based on each class population.
        Crucial step when the training data is imbalanced.
        """
        lbs_weights = {}
        # capture the 2nd array dimenssion (the number of columns in pd.DataFrame)
        lbs_amount = len(train_labels.unique())

        for idx in range(lbs_amount):
            weight_dict = {
                idx: (1 / np.count_nonzero(train_labels == idx)) * (len(train_labels)) / lbs_amount
            }
            lbs_weights.update(weight_dict)
        return lbs_weights
