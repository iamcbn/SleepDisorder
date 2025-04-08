from sklearn.base import BaseEstimator, TransformerMixin


class FeatureCorrecter(BaseEstimator, TransformerMixin):
    """
    This transformer rearranges the columns to match that of the model.
    It also capitalises Occupation column
    """
    def fit(self, X, y=None):
        self.is_fitted_ = True
        return self

    def transform(self, X):
        X = X.copy()
        expected_order = ['Gender', 'Age', 'Occupation', 'Sleep Duration',
                          'Quality of Sleep', 'Physical Activity Level', 'Stress Level',
                          'BMI Category', 'Heart Rate', 'Daily Steps', 'BP Category']
        X = X.reindex(columns=expected_order)

        if 'Occupation' in X.columns:
            X['Occupation'] = X['Occupation'].str.title()
        return X