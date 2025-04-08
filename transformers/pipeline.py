import pickle
import sys
import os
from sklearn.pipeline import Pipeline
from config import CAT_FEATURES, FEATURE_ENCODER, SCALER_FILE
from transformers import BMICategorizer, BPClassifier, SavedEncoderTransformer, SavedScalerTransformer, FeatureCorrecter



with open(SCALER_FILE, 'rb') as f:
    scaler = pickle.load(f)

with open(FEATURE_ENCODER, 'rb') as f:
    f_encoder = pickle.load(f)


# Define feature groups
#cat_features = ['Gender', 'Occupation', 'BMI Category', 'BP Category']
#num_features = ['Age', 'Sleep Duration', 'Quality of Sleep', 'Physical Activity Level', 'Stress Level', 'Heart Rate', 'Daily Steps']


# Final pipeline
pipeline = Pipeline([
    ('bmi_categorizer', BMICategorizer()),
    ('bp_classifier', BPClassifier()),
    ('feature_correcter', FeatureCorrecter()),
    ('saved_encoder', SavedEncoderTransformer(f_encoder, CAT_FEATURES)),
    ('saved_scaler', SavedScalerTransformer(scaler))
])