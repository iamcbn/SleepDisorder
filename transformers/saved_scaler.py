from sklearn.base import BaseEstimator, TransformerMixin


class SavedScalerTransformer(BaseEstimator, TransformerMixin):
    """
    Uses the saved scaler to scale the entire DataFrame.
    """
    def __init__(self, scaler):
        self.scaler = scaler

    def fit(self, X, y=None):
        self.is_fitted_ = True
        return self

    def transform(self, X):
        X = X.copy()
        # The scaler expects a numpy array, so we convert and then restore DataFrame structure.
        scaled_array = self.scaler.transform(X)
        return scaled_array
        