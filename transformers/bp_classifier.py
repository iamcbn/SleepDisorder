from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd

class BPClassifier(BaseEstimator, TransformerMixin):
    """
    Classifies blood pressure into categories.
    """
    def fit(self, X, y=None):
        self.is_fitted_ = True
        return self

    def transform(self, X):
        X = X.copy()

        # Ensure that 'Blood Pressure' exists in the DataFrame
        if 'Blood Pressure' in X.columns:
            # Handle missing or invalid values in 'Blood Pressure'
            def split_bp(bp_value):
                try:
                    systolic, diastolic = bp_value.split('/')
                    return int(systolic), int(diastolic)
                except (ValueError, AttributeError):
                    return None, None  # Handle invalid format

            X[['Systolic BP', 'Diastolic BP']] = X['Blood Pressure'].apply(lambda x: pd.Series(split_bp(x)))
            X.drop(columns=['Blood Pressure'], inplace=True)

        # Check if 'Systolic BP' and 'Diastolic BP' are available and classify BP
        if 'Systolic BP' in X.columns and 'Diastolic BP' in X.columns:
            # Use element-wise comparison for proper row-wise checking
            X['BP Category'] = X.apply(
                lambda row: self.classify_bp(row['Systolic BP'], row['Diastolic BP']), axis=1)

            # Drop the 'Systolic BP' and 'Diastolic BP' columns as they're no longer needed
            X.drop(columns=['Systolic BP', 'Diastolic BP'], inplace=True)

        return X

    def classify_bp(self, systolic, diastolic):
        if systolic is None or diastolic is None:
            return 'Unknown'  # If values are invalid
        elif systolic < 90 or diastolic < 60:
            return 'Low'
        elif 90 <= systolic < 120 and 60 <= diastolic < 80:
            return 'Normal'
        elif 120 <= systolic < 130 and diastolic < 80:
            return 'Elevated'
        elif (130 <= systolic <= 139) or (80 <= diastolic <= 89):
            return 'High BP (Stage 1)'
        elif systolic >= 140 or diastolic >= 90:
            return 'High BP (Stage 2)'
        else:
            return 'Unknown'