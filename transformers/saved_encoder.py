from sklearn.base import BaseEstimator, TransformerMixin
cat_features = ['Gender', 'Occupation', 'BMI Category', 'BP Category']

class SavedEncoderTransformer(BaseEstimator, TransformerMixin):
    """
    Applies the saved encoder to specified categorical columns.
    """
    def __init__(self, encoders, cat_features):
        self.encoders = encoders
        self.cat_features = cat_features

    def fit(self, X, y=None):
        self.is_fitted_ = True
        return self

    def transform(self, X):
        X = X.copy()
        for col in self.cat_features:
            if col in X.columns:
                # Transform and override the column with encoded values.
                X[col] = self.encoders[col].transform(X[[col]])
        return X
