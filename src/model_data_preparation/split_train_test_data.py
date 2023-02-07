import pandas as pd
from sklearn.model_selection import train_test_split


class SplitData:
    def __init__(self,
                 data: pd.DataFrame,
                 config
                 ):
        self.config = config
        self.train_set, self.test_set, self.train_labels, self.test_labels = self.__separate_data_n_labels(
            data=data,
            config=config
        )

    @staticmethod
    def __split_into_train_test(data):
        train_set, test_set = train_test_split(
            data,
            train_size=0.8,
            shuffle=False
        )
        return train_set, test_set

    def __separate_data_n_labels(self,
                                 data,
                                 config
                                 ):
        train_set, test_set = self.__split_into_train_test(data=data)

        train_labels = train_set[config.dfstructure.labels]
        test_labels = test_set[config.dfstructure.labels]

        train_set.drop(
            columns=[config.dfstructure.labels],
            inplace=True
        )
        test_set.drop(
            columns=[config.dfstructure.labels],
            inplace=True
        )
        return train_set, test_set, train_labels, test_labels
