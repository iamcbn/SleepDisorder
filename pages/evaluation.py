import matplotlib.pyplot as plt
import streamlit as st
import seaborn as sns
import pickle 
import pandas as pd
import numpy as np


from sklearn.metrics import (
    average_precision_score,
    precision_recall_curve,
    log_loss
)
from sklearn.preprocessing import label_binarize


# Setting the path to root __dir__
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# from config import MODEL_EVAL

# Load the evaluation metrics and model pickle files
with open('models/model_evaluation.pkl', 'rb') as f:
    full_metrics = pickle.load(f)

with open('models/model.pkl', 'rb') as f:
    model = pickle.load(f)


# Extracting test and train metrics
evaluation_metrics = full_metrics['test_metrics']
train_metrics = full_metrics['train_metrics']

# Extracting test metrics
report = evaluation_metrics['classification_report']
matrix= evaluation_metrics['confusion_matrix']
class_names = evaluation_metrics['class_names']


# ----- Extracting values needed for ROC-AUC, Log Loss and PR AUC --------
y_true= evaluation_metrics["y_test"]
X_test= evaluation_metrics["X_test"]
y_pred_proba = model.predict_proba(X_test) # For log loss, roc auc
y_true_bin = label_binarize(y_true, classes=range(3)) # Label binarisation for One-vs-Rest evaluation



# Function to display confusion matrix
def plot_confusion_matrix(matrix, class_names):
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(matrix, annot=True, fmt="d", cmap="Blues", xticklabels=class_names, yticklabels=class_names, cbar=False, ax=ax)
    ax.set_xlabel('Predicted')
    ax.set_ylabel('True')
    ax.set_title('Confusion Matrix')
    st.pyplot(fig)

# Function to display classification report as a table
def display_classification_report(report):
    df = pd.DataFrame(report).transpose()
    st.dataframe(df)

@st.cache_resource
def compute_auc_pr_summary():
    summary_data = []
    fig_dict = {}

    for i, cls in enumerate(class_names):
        precision, recall, _ = precision_recall_curve(y_true_bin[:, i], y_pred_proba[:, i])
        pr_auc = average_precision_score(y_true_bin[:, i], y_pred_proba[:, i])
        summary_data.append((cls, pr_auc))

        # Plot
        fig, ax = plt.subplots()
        ax.plot(recall, precision, label=f'PR AUC = {pr_auc:.2f}')
        ax.set_xlabel("Recall")
        ax.set_ylabel("Precision")
        ax.set_title(f"Precision-Recall Curve – {cls}")
        ax.legend(loc='lower left')
        fig_dict[cls] = fig

    return summary_data, fig_dict


def auc_pr():
    summary_data, pr_figures = compute_auc_pr_summary()

    # Summary section
    st.subheader("Precision-Recall AUC Summary")
    for cls, auc_score in summary_data:
        st.markdown(f"- **{cls}**: PR AUC = `{auc_score:.4f}`")
    for cls in class_names:
        st.pyplot(pr_figures[cls])

text = """
This page offers a transparent overview of the modelling process behind the **Sleep Disorder Classifier**. It contains key insights into my thought process, model selection (SVC with `probability=True`), and hyperparameters used. I’ve also included evaluation metrics that reflect how the model performs across the three sleep disorder categories: **None**, **Sleep Apnea**, and **Insomnia**.

To ensure a robust evaluation, I relied on a combination of:

- **Confusion Matrix** – for class-wise prediction breakdown
- **Macro F1-Score** – to summarise performance for each class independently
- **ROC AUC (OvR)** and **AUC-PR** – to evaluate probabilistic discrimination ability per class
- **Log Loss** – to quantify how confident the model was in its predictions
- **SHAP Summary** - to understand the roles of each feature to each class. Take it as your feature importance.

These metrics were chosen to provide a complete picture of classification performance from both deterministic and probabilistic standpoints.

Additional context such as:

- The features used
- Data preprocessing techniques (e.g., scaling, encoding)
- Model assumptions and limitations

...are essential to fully grasp the model’s behaviour and should be reviewed alongside the evaluation.



**For a deeper understanding**, please refer to my:

* `README.md` for a project overview
* Model training notebook for end-to-end development details

*Your feedback is encouraged – this is an avenue for me to learn and grow.*
"""


# ----- STREAMLIT AP -------
st.toast("Welcome Technical Viewers")
st.title("Model Evaluation")

st.subheader("Technical Summary")
st.caption(text)


# Show F1 Score
with st.expander("F1 Scores"):
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Test Macro F1Score", round(evaluation_metrics['f1_score'],3))
    with col2:
        st.metric("Train Macro F1-Score", round(train_metrics['f1_score'], 3))
    st.caption(" *I understand the numbers look perfect—I thought so too. However, if you compare the test results with the training results, you'll notice that the training F1 score is lower than the test score. What do you make of this? Please leave your feedback via the `Contact Me` form.*")

# Show Classification Report
with st.expander("Classification Report"):
    display_classification_report(report)

# Show Confusion Matrix
with st.expander("Confusion Matrix"):
    plot_confusion_matrix(matrix, class_names)

# Show SHAP Values Plot
with st.expander("SHAP Values Summary"):
    st.image('data/shap_value.png')


# --- ROC AUC ---
with st.expander("Precision-Recall AUC (PR AUC)"):
    auc_pr()
        

# --- Log Loss ---
with st.expander(" Log Loss (Cross-Entropy)"):
    loss = log_loss(y_true, y_pred_proba)
    st.metric("Log Loss", f"{loss:.3f}")


# # Allow users to download the classification report and other details as a CSV or text file
# st.subheader("Download Evaluation Metrics")
# metrics_df = pd.DataFrame(evaluation_metrics['classification_report']).transpose()
# metrics_df.to_csv("classification_report.csv")
# st.download_button("Download Classification Report", "classification_report.csv", "classification_report.csv")