![Sleep Health and Lifestyle Banner](data/banner_image.png)
# Sleep Disorder Prediction Project

This project explores the prediction of sleep disorders using machine learning techniques. It includes data analysis, model training, building a prediction pipeline with custom transformers, and a CLI test script for interaction. In the future, we will deploy the model via an API.

---

## Table of Contents

- [Overview](#overview)
- [Project Workflow](#project-workflow)
  - [Data Analysis](#data-analysis)
  - [Model Training](#model-training)
  - [Prediction Pipeline](#prediction-pipeline)
- [Project Structure](#project-structure)
- [Installation and Setup](#installation-and-setup)
- [Running the Project](#running-the-project)
  - [Running the CLI Test Script](#running-the-cli-test-script)
- [Next Steps: Deploying via API](#next-steps-deploying-via-api)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

This project predicts the likelihood of a sleep disorder by processing user data (such as gender, age, BMI, sleep quality, stress level, etc.) using a machine learning model. The workflow consists of:

1. **Data Analysis:** Exploratory data analysis (EDA) via Jupyter notebooks.
2. **Model Training:** Training machine learning models with robust feature engineering and validation.
3. **Prediction Pipeline:** Integrating custom transformers (e.g., BMI categorizer, blood pressure classifier, encoders, scalers) with a trained model.
4. **CLI Testing:** Interacting with the pipeline through a CLI test script (`app/test.py`).
5. **Next Steps:** Planning to deploy the model via an API using FastAPI and optionally a frontend via Streamlit.

---

## Project Workflow

### Data Analysis

- **Exploratory Data Analysis (EDA):**  
  Jupyter notebooks in `data/notebook.ipynb` were used to visualize and understand the relationships between variables such as sleep duration, BMI, and stress levels.
- **Data Cleaning and Feature Engineering:**  
  Data inconsistencies, such as unit mismatches (e.g., converting height from centimeters to meters), were corrected and additional features were derived to enhance model performance.

### Model Training

- **Model Selection and Training:**  
  Several models were trained and evaluated to predict sleep disorders. Hyperparameter tuning and cross-validation ensured robust performance.
- **Custom Transformers:**  
  Custom transformers, like `BMICategorizer` and `BPClassifier`, were built to preprocess the data according to domain-specific criteria.
- **Persisting the Model:**  
  The best-performing model, along with pre-fitted encoders/scalers, was serialized using `pickle` and saved in the `models/` directory.

### Prediction Pipeline

- **Pipeline Assembly:**  
  A prediction pipeline was built using scikit-learn’s `Pipeline` class. It includes the custom transformers and the trained model.
- **CLI Interaction:**  
  The pipeline was tested using a CLI test script (`app/test.py`). This script uses the `UserDataCollector` class (from `app/utils.py`) to gather user input, transform it, and output a prediction.

---

## Project Structure

```
SleepDisorder/
├── app/
│   ├── __init__.py               # (Optional) Package marker for app directory
│   ├── test.py                   # CLI test script to interact with the model
│   ├── utils.py                  # Contains UserDataCollector for data input
├── data/
│   ├── banner_image.png          # Image
│   ├── data.csv                  # Primary dataset
│   └── notebooks.ipynb           # Jupyter notebooks for EDA and model training
├── models/                       # Trained models and serialized objects
│   ├── model.pkl                 # Trained prediction model
│   ├── feature_encoder.pkl       # Pre-fitted feature encoder
│   └── target_encoder.pkl        # Pre-fitted target encoder
│   ├── scaler.pkl                # Pre-fitted scaler
├── transformers/                 # Custom transformers for data preprocessing
│   ├── __init__.py               # Exports transformer classes (BMICategorizer, etc.)
│   ├── bmi_categorizer.py        # Contains BMICategorizer class
│   ├── bp_classifier.py          # Contains BPClassifier class
│   ├── saved_encoder.py          # Contains SavedEncoderTransformer class
│   ├── saved_scaler.py           # Contains SavedScalerTransformer class
│   └── feature_correcter.py      # Contains FeatureCorrecter class
├── config.py                     # Central configuration file defining paths, etc.
└── LICENSE                       # MIT License
├── README.md                     # This documentation file
├── requirements.txt              # Python package requirements
```

---

## Installation and Setup

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/iamcbn/SleepDisorder.git
   cd SleepDisorder
   ```

2. **Create a Virtual Environment (Recommended):**

   **On Windows:**
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```

   **On macOS/Linux:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

---

## Running the Project

### Running the CLI Test Script

The test script located at `app/test.py` interacts with your model. It collects user input, processes the data through your prediction pipeline, and outputs the sleep disorder prediction.

1. **Navigate to the `app` Directory:**

   ```bash
   cd app
   ```

2. **Run the Test Script:**

   ```bash
   python test.py
   ```

   This will prompt you for the necessary inputs, process them through the pipeline, and print out the prediction result.

---

## Next Steps: Deploying via API

In the next phase, we plan to make this project publicly accessible by deploying an API. The envisioned steps include:

- **Backend with FastAPI:**  
  Develop a RESTful API that takes JSON input, validates and preprocesses data, runs predictions, and returns results.
  
- **Optional Frontend with Streamlit:**  
  Build an interactive web interface for users to input data and view predictions.
  
- **Deployment:**  
  Host the API and/or web app on platforms such as Render, Railway, or Hugging Face Spaces.

Implementing this API will help you understand and gain hands-on experience with modern deployment practices.

---

## Troubleshooting

- **Module or Path Issues:**  
  Ensure that the paths defined in `config.py` align with your project structure and that the virtual environment is active.
  
- **Input Data Errors:**  
  Verify that inputs conform to the expected ranges (e.g., height in meters between 0.5 and 2.5) as enforced by the `UserDataCollector`.
  
- **Dependency Issues:**  
  If a module is not found, double-check the `requirements.txt` and confirm all necessary packages are installed.

---

## Contributing

Contributions, suggestions, and improvements are welcome! Please fork the repository, make your changes, and submit a pull request with clear descriptions of your modifications or bug fixes.

---

## License

This project is licensed under the [MIT License](LICENSE).

---


### Instructions to Use the README

1. **Copy and paste** the entire text above into a file named `README.md` in your project root.
2. **Update URLs** (e.g., `https://github.com/iamcbn/SleepDisorder.git`) and any project-specific details as necessary.
3. **Commit and push** your README along with your other project files.
