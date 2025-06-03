"""
This is a test script to test the components together
"""

import pickle
import sys
import os
import warnings
from utils import UserDataCollector

# Setting directory to be parent root directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from transformers import BMICategorizer, pipeline, BPClassifier, SavedEncoderTransformer, SavedScalerTransformer, FeatureCorrecter
from config import MODEL_FILE, FEATURE_ENCODER, TARGET_ENCODER


def load_model_and_encoders():
    """Fetches the neccessary files and load them"""
    with open(MODEL_FILE, 'rb') as f:
        model = pickle.load(f)

    with open(TARGET_ENCODER, 'rb') as f:
        t_encoder = pickle.load(f)

    with open(FEATURE_ENCODER, 'rb') as f:
        f_encoder = pickle.load(f)

    return model, t_encoder, f_encoder


def main():
    model, t_encoder, _ = load_model_and_encoders()

    collector = UserDataCollector()
    collector.collect_input()
    data = collector.get_data()

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=FutureWarning)
        trans_data = pipeline.transform(data)

    pred = model.predict(trans_data)
    result = t_encoder.inverse_transform(pred)[0]
    print("ðŸ§  Sleep disorder prediction: ", result)


if __name__ == "__main__":
    main()
