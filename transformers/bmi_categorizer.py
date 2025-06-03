from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd

class BMICategorizer(BaseEstimator, TransformerMixin):
    """
    Calculates BMI Category based on gender-specific criteria.
    """
    def fit(self, X, y=None):
        self.is_fitted_ = True
        return self

    def transform(self, X):
        
        X = X.copy()
        
        # Ensure 'weight', 'height', and 'Gender' columns exist in the data
        if 'Weight' in X.columns and 'Height' in X.columns and 'Gender' in X.columns:
            # Calculate BMI
            X['BMI'] = X['Weight'] / (X['Height'] ** 2)
            
            def categorize(row):
                bmi = row['BMI']
                gender = str(row['Gender']).lower() if isinstance(row['Gender'], str) else None
                if gender == 'male':
                    if bmi <= 25: 
                        return 'Normal Weight'
                    elif bmi <= 30: 
                        return 'Overweight'
                    else: 
                        return 'Obese'
                    
                elif gender == 'female':
                    if bmi <= 24: 
                        return 'Normal Weight'
                    elif bmi <= 39: 
                        return 'Overweight'
                    else: 
                        return 'Obese'

                else:
                    return 'Unknown'  # If gender is not recognized
                
            # Apply categorization logic
            X['BMI Category'] = X.apply(categorize, axis=1)
            
            # Drop the 'weight', 'height', and 'BMI' columns as they are no longer needed
            X.drop(columns=['Weight', 'Height', 'BMI'], inplace=True)
        else:
            raise ValueError("DataFrame must contain 'Weight', 'Height', and 'Gender' columns.")
        
        return X
