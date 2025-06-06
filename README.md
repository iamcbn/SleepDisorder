![Sleep Health and Lifestyle Banner](data/banner_image.png)

[![Streamlit App](https://img.shields.io/badge/Live%20App-Streamlit-ff4b4b?logo=streamlit\&logoColor=red)](https://sleepdisorder-bruno.streamlit.app)
[![Python Version](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/github/license/iamcbn/SleepDisorder)](LICENSE)
<!-- [![Platform](https://img.shields.io/badge/Platform-Streamlit-lightgrey?logo=streamlit)](https://streamlit.io/) -->


  
# Sleep Disorder Prediction

This project explores the prediction of sleep disorders using machine learning techniques. It now includes a multi-page Streamlit web application with dedicated sections for general users (Demo), healthcare professionals (Clinician Portal), and technical audiences (Model Evaluation). Additionally, it still supports command-line interaction via a CLI test script.

---

## Table of Contents

* [Overview](#overview)
* [Key Features](#key-features)
* [App Walkthrough](#app-walkthrough)
* [Project Structure](#project-structure)
* [Installation and Setup](#installation-and-setup)
* [Running the Project](#running-the-project)

  * [Streamlit App](#streamlit-app)
  * [CLI Test Script](#cli-test-script)
* [Deployment](#deployment)
* [Troubleshooting](#troubleshooting)
* [Contributing](#contributing)
* [License](#license)

---

## Overview

This project predicts the likelihood of a sleep disorder—**Sleep Apnoea**, **Insomnia**, or **None**—by processing user data (such as gender, age, BMI, sleep quality, stress level, etc.) through a trained machine learning model.

**Core components include:**

1. **Data Analysis:** Exploratory data analysis (EDA) via Jupyter notebooks.
2. **Model Training:** Training machine learning models with feature engineering and validation.
3. **Prediction Pipeline:** Integrating custom transformers (e.g. BMI categoriser, BP classifier, encoders, scalers) with a trained model.
4. **CLI Interaction:** A command-line test script (`helper/test.py`) for quick terminal-based predictions.
5. **Web App Interface:** A multi-page Streamlit app comprising Home, Demo, Clinician Portal, and Model Evaluation pages.

---

## Key Features

* **Custom Transformers:**

  * **BMICategoriser** — categorises BMI into standard risk groups.
  * **BPClassifier** — classifies blood pressure into clinical categories.

* **Robust Pipeline:**

  * Encodes categorical variables, scales numerical features, and applies custom transformers.
  * Uses a Support Vector Classifier (SVC) with probability calibration to output prediction confidences.

* **Streamlit Web Application:**

  * **Home Page** — overview of the project and contact form.
  * **Demo Page** — public-friendly prediction interface.
  * **Clinician Portal** — doctors verify model predictions, provide corrected diagnoses, and submit feedback.
  * **Model Evaluation Page** — detailed performance metrics, including confusion matrix, classification report, ROC-AUC/PR-AUC plots, log loss, and SHAP summary.

* **Data Collection Loop:**

  * Clinicians can confirm or correct model predictions, and that feedback is appended to a Google Sheet for model improvement.

* **Command-Line Test Script:**

  * Quickly test predictions in the terminal using `helper/test.py`.

---

## App Walkthrough

| Page                 | Description                                                                                                                                 |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| **Home**             | Introduction to the project, developer “About Me” section, and a contact form for general enquiries or feedback.                            |
| **Demo**             | User-friendly interface allowing non-technical users to enter health metrics and receive a sleep disorder prediction with confidence score. |
| **Clinician Portal** | Secure area for healthcare professionals only to:<ul><li> Input the same health metrics as on Demo.</li><li> View model prediction and confidence.</li><li> Confirm if the prediction is correct or indicate the correct diagnosis.</li><li> Provide optional qualitative feedback. |
| **Model Evaluation** | Technical dashboard showing:<ul><li> Macro F1 scores for train/test sets</li><li> Classification report</li><li> Confusion matrix</li><li> Precision-Recall AUC curves per class</li><li> Log Loss metric</li><li> SHAP values summary plot |

---
  

## Project Structure

```
SleepDisorder/
├── .streamlit/
│   └── config.toml                # Theme settings (light/dark)
├── helper/
│   ├── forms.py                   # Streamlit form for clinician feedback + Google Sheets integration
│   ├── test.py                    # CLI test script for terminal predictions
│   └── utils.py                   # UserDataCollector: input validation and conversion
├── pages/
│   ├── home.py                    # Home page: project overview, About Me, contact form
│   ├── demo.py                    # Demo page: public prediction interface
│   ├── doctors.py                 # Clinician Portal page: prediction confirmation and feedback
│   └── evaluation.py              # Model Evaluation page: performance metrics and visualisations
├── data/
│   ├── banner_image.png           # Banner image for Home page
│   ├── data.csv                   # Primary dataset (if needed for reference)
│   ├── notebook.ipynb             # Jupyter notebook for EDA and model training
│   ├── logo.png                   # App logo
│   └── shap_value.png             # SHAP summary plot for Model Evaluation
├── models/
│   ├── model.pkl                  # Trained prediction model (pickle file)
│   ├── feature_encoder.pkl        # Pre-fitted feature encoder (pickle file)
│   ├── target_encoder.pkl         # Pre-fitted target encoder (pickle file)
│   ├── scaler.pkl                 # Pre-fitted scaler (pickle file)
│   └── model_evaluation.pkl       # Serialized performance metrics (pickle file)
├── transformers/
│   ├── bmi_categorizer.py         # BMICategoriser transformer
│   ├── bp_classifier.py           # BPClassifier transformer
│   ├── saved_encoder.py           # SavedEncoderTransformer for categorical features
│   ├── saved_scaler.py            # SavedScalerTransformer for numerical features
│   └── feature_correcter.py       # FeatureCorrecter for cleaning raw inputs
├── app.py                         # Main Streamlit entry point (defines navigation and common UI elements)
├── config.py                      # Central configuration: file paths to images, models, etc.
├── LICENSE                        # MIT License
├── requirements.txt               # Python package requirements
├── .gitignore                     # Files and folders to ignore in Git
└── README.md                      # This documentation file
```

---

## Installation and Setup

1. **Clone the Repository**

   ```bash
   git clone https://github.com/iamcbn/SleepDisorder.git
   cd SleepDisorder
   ```

2. **Create a Virtual Environment**

   > It is highly recommended to use a virtual environment to isolate dependencies.

   **Windows**

   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```

   **macOS/Linux**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Streamlit Secrets (for Google Sheets Integration)**
   If using clinician feedback storage via Google Sheets, create `.streamlit/secrets.toml` with your service account credentials in the following format:

   ```toml
   [connections.gsheets]
   type = "service_account"
   project_id = "your-project-id"
   private_key_id = "YOUR_PRIVATE_KEY_ID"
   private_key = """-----BEGIN PRIVATE KEY-----
   YOUR_PRIVATE_KEY_CONTENT
   -----END PRIVATE KEY-----"""
   client_email = "your-service-account@your-project-id.iam.gserviceaccount.com"
   client_id = "YOUR_CLIENT_ID"
   auth_uri = "https://accounts.google.com/o/oauth2/auth"
   token_uri = "https://oauth2.googleapis.com/token"
   auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
   client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/your-service-account%40your-project-id.iam.gserviceaccount.com"
   ```

---

## Running the Project

### Streamlit App

To launch the multi-page web application, run:

```bash
streamlit run app.py
```

Then open the URL printed in your terminal (e.g. `http://localhost:8501`) in your browser.

---

### CLI Test Script

For quick terminal-based predictions without the web interface:

1. Navigate to the helper folder:

   ```bash
   cd helper
   ```

2. Run the CLI script:

   ```bash
   python test.py
   ```

This will prompt you for the required inputs, run the prediction pipeline, and display the predicted sleep disorder in the terminal.

---

## Deployment

The Streamlit app is hosted on **Streamlit Community Cloud**:

1. Push your repository to GitHub.
2. Sign in to [Streamlit Cloud](https://share.streamlit.io).
3. Create a new app, selecting your GitHub repo and setting `app.py` as the entrypoint.
4. Ensure the following files are present in the GitHub repo for successful deployment:

   - `app.py`
   - `requirements.txt`

🔗 **Live App**: [sleepdisorder-bruno.streamlit.app](https://sleepdisorder-bruno.streamlit.app)

---

## Troubleshooting

* **App crashes on start**
  - Confirm that the paths in `config.py` are correct and match your folder structure.

* **Missing Packages**
  - If you encounter `ModuleNotFoundError`, ensure you’ve run `pip install -r requirements.txt` in your virtual environment.

* **Secret or Google Sheets Errors**
  - Double-check your `.streamlit/secrets.toml` formatting (proper TOML syntax).
  - Make sure the service account email has edit access to the target Google Sheet.

---

## Current Step: Real-World Testing of my model

Training a model is not enough, the model needs to be evaluated with real-world data to understand its performance. Please contact me if you would like to test my model (For clinicians only)

---

## Next Steps: Deploying via API

In the next phase, I plan to make this project accessible by deploying an API. The envisioned steps include:

- **Backend with FastAPI:**  
  Develop a RESTful API that takes JSON input, validates and preprocesses data, runs predictions, and returns results.
    
- **Deployment:**  
  Host the API.

Implementing this API will help you understand and gain hands-on experience with modern deployment practices.

---

## Contributing

Contributions, suggestions, and improvements are welcome! To contribute:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Commit your changes with clear messages.
4. Submit a pull request and describe your modifications or enhancements.

Please adhere to the existing code style and add appropriate tests or documentation where necessary.

---

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for full details.

---

**Made with 💚 by [@iamcbn](https://github.com/iamcbn)**
