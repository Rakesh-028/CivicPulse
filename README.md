# 🏛️ CivicPulse — Public Complaint Resolution Intelligence

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/Streamlit-App%20Ready-FF4B4B?logo=streamlit&logoColor=white" alt="Streamlit"/>
  <img src="https://img.shields.io/badge/scikit--learn-1.9+-F7931E?logo=scikit-learn&logoColor=white" alt="scikit-learn"/>
  <img src="https://img.shields.io/badge/License-MIT-22C55E" alt="MIT License"/>
  <img src="https://img.shields.io/badge/Macro--F1-0.8543-6366F1" alt="Macro-F1"/>
</p>

<p align="center">
  <strong>An end-to-end Machine Learning system that predicts whether a NYC 311 service complaint will face prolonged administrative delays — at the exact moment of intake.</strong>
</p>

---

## 📌 Executive Summary

Municipal agencies process hundreds of thousands of citizen complaints every year. While most are resolved quickly, a significant subset gets stuck in administrative bottlenecks — leaving citizens waiting and hazards unaddressed.

**CivicPulse** uses supervised machine learning to flag high-risk complaints **before** they become delayed, giving dispatch supervisors the intelligence to proactively triage workloads and reduce service backlogs.

> Built as a **CSE303 Machine Learning Capstone Project** using real NYC Open Data (311 Service Requests).

---

## 🎯 Problem Statement

**Goal:** Classify whether an inbound 311 service request will face prolonged resolution time — exceeding the operational **75th-percentile threshold of ~61 hours (~2.5 days)** — using **only information available at the moment of complaint registration** (no post-outcome data).

### Cost-of-Error Analysis

| Prediction vs Reality | Normal Resolution (Actual 0) | Prolonged Delay (Actual 1) |
| :--- | :--- | :--- |
| **Predicted Normal (0)** | ✅ True Negative: Standard routing | 🚨 **False Negative (HIGH COST):** Delay missed → citizen escalation, unresolved civic hazard |
| **Predicted Delay (1)** | ⚠️ False Positive (low cost): Brief supervisor check | 🎯 **True Positive:** High-risk complaint flagged for priority dispatch |

> **Key Insight:** False Negatives carry a significantly higher real-world cost. CivicPulse acts as **decision support** — augmenting, not replacing, human judgment.

---

## 📊 Dataset

| Property | Value |
| :--- | :--- |
| **Source** | [NYC Open Data — 311 Service Requests (2020–Present)](https://data.cityofnewyork.us/Social-Services/311-Service-Requests-from-2020-to-Present/erm2-nwe9) |
| **Records** | 312,036 complaints |
| **File Size** | ~44.3 MB (CSV) |
| **Columns Used** | 8 |

**Active Columns:** `Unique Key`, `Created Date`, `Closed Date`, `Agency`, `Agency Name`, `Problem (formerly Complaint Type)`, `Status`, `Borough`

> ⚠️ **The dataset CSV is not included in this repository** (exceeds GitHub size limits). To run the notebook, download the CSV from NYC Open Data and upload it directly to your Colab session storage. The notebook auto-detects any `311_Service_Requests*.csv` file — no Google Drive connection required.

---

## 📐 Target Variable & Formulation

**Step 1 — Compute Resolution Duration:**

$$\text{Resolution Hours} = \frac{\text{Closed Date} - \text{Created Date}}{3600}$$

Records with negative durations (data entry errors) and open/pending complaints are strictly excluded.

**Step 2 — IQR Boundary Analysis (Outlier-Robust Threshold Selection):**

| Percentile | Value |
| :--- | :--- |
| Q1 (25th) | ~1.2 hours |
| Q2 / Median (50th) | ~6.9 hours |
| Q3 (75th) ← **Decision Threshold** | **~61.0 hours** |
| IQR | ~59.8 hours |
| Outlier Boundary (Q3 + 1.5×IQR) | ~150.7 hours |

**Step 3 — Binary Classification:**

$$\text{is\_delayed} = \begin{cases} 1 & \text{if Resolution Hours} > 61.03\text{ hrs} \\ 0 & \text{if Resolution Hours} \le 61.03\text{ hrs} \end{cases}$$

**Class Distribution:** ~75% Normal Resolution (`0`) vs. ~25% Prolonged Delay (`1`)

---

## 🛡️ Data Leakage Prevention

All post-outcome information is strictly excluded from the input matrix $X$ to guarantee real-world generalization.

| Feature Type | Fields |
| :--- | :--- |
| ❌ **Excluded (post-outcome)** | `Closed Date`, `Resolution Action Updated Date`, `Resolution Description`, `Status`, `Resolution_Hours` |
| ✅ **Included (known at intake)** | `Problem`, `Agency`, `Borough`, `Created_Hour`, `Created_DayOfWeek`, `Created_Month` |

---

## 🔬 Model Ladder & Results

All models trained on an **80/20 stratified train-test split** with **5-Fold Stratified Cross-Validation**:

| Stage | Algorithm | Test Accuracy | Macro-F1 | ROC-AUC | 5-Fold CV F1 |
| :--- | :--- | :---: | :---: | :---: | :---: |
| Baseline (Exp 3) | Logistic Regression | 84.1% | 0.724 | 0.795 | 0.722 ± 0.005 |
| Non-Linear (Exp 6) | Decision Tree | 86.3% | 0.761 | 0.812 | 0.758 ± 0.006 |
| Ensemble (Unit V) | Random Forest | 87.5% | 0.785 | 0.842 | 0.783 ± 0.004 |
| **Final Model** | **Tuned Logistic Regression** | **88.2%** | **0.8543** | **0.865** | **0.854 ± 0.003** |

🏆 **Benchmark Target:** Macro-F1 ≥ 0.75 — **Surpassed at 0.8543**

### Why Tuned Logistic Regression?

After `GridSearchCV` tuning (`C=1.0`, `solver='lbfgs'`, `class_weight='balanced'`):

1. **Best Macro-F1 (0.8543)** — balanced class weights penalize missed delay cases
2. **Sub-millisecond inference** — suitable for real-time dispatch dashboards
3. **Transparent explainability** — model weights ($\beta$ coefficients) give actionable insights without black-box approximations
4. **Stable generalization** — minimal CV variance (±0.003)

---

## 🔍 Explainability — Top Feature Weights

| Direction | Feature | Coefficient | Insight |
| :--- | :--- | :---: | :--- |
| 🟢 Rapid Resolution | NYPD (Agency) | −6.18 | Active field patrols resolve enforcement complaints instantly |
| 🔴 Delay Driver | Food Establishment (Problem) | +3.53 | Requires multi-step inspection workflows |
| 🔴 Delay Driver | Street Condition (Problem) | +3.49 | Infrastructure repair involves cross-agency coordination |

---

## 🌟 Streamlit Dashboard — Civic Early-Warning Command Center

The deployment app (`app.py`) provides three modules:

| Tab | Name | Description |
| :--- | :--- | :--- |
| 🎯 Tab 1 | **Delay Radar** | Live calculator — enter complaint type, agency, borough & time for immediate delay probability |
| 📊 Tab 2 | **Bottleneck Overview** | Visual analysis of agency response bottlenecks across all NYC boroughs |
| 🔍 Tab 3 | **Explainability Panel** | Transparent review of model feature weights |

### Launch Locally

```bash
git clone https://github.com/Rakesh-028/CivicPulse.git
cd CivicPulse
pip install -r requirements.txt
streamlit run app.py
```

Open your browser at `http://localhost:8501`

---

## 📂 Project Structure

```
CivicPulse/
├── CivicPulse.ipynb              # ⭐ Main Colab notebook (50 steps: EDA → Model → Export)
├── app.py                        # Streamlit Early-Warning Command Center
├── civicpulse_model.pkl          # Saved Tuned Logistic Regression pipeline
├── requirements.txt              # Python dependencies
├── LICENSE                       # MIT License
├── README.md                     # This file
└── guide/                        # Course guidelines & full project documentation
    ├── CivicPulse_Project_Details.docx
    └── CivicPulse_Google_Form_and_Proposal_Fields.docx
```

> `extra/` and the dataset CSV are excluded via `.gitignore`.

---

## ⚙️ How to Run the Notebook (Google Colab)

1. Open `CivicPulse.ipynb` in [Google Colab](https://colab.research.google.com/)
2. Download the dataset from [NYC Open Data](https://data.cityofnewyork.us/Social-Services/311-Service-Requests-from-2020-to-Present/erm2-nwe9)
3. Upload the CSV directly to Colab's session storage (the Files panel on the left)
4. Run all cells — the notebook auto-detects `311_Service_Requests*.csv` without needing Google Drive

---

## 🛠️ Tech Stack

| Layer | Technology |
| :--- | :--- |
| Language | Python 3.10+ |
| Data Processing | Pandas, NumPy |
| Machine Learning | scikit-learn 1.9+ |
| Visualization | Matplotlib, Seaborn |
| Web App | Streamlit |
| Model Persistence | Joblib |
| Notebook | Google Colab |

---

## 📚 Academic Citations

1. **Raj, R., Ramesh, A., Seetharam, A., & DeFazio, D. (2021).** *SWIFT: A non-emergency response prediction system using sparse Gaussian Conditional Random Fields.* Pervasive and Mobile Computing, 71, 101317. [DOI: 10.1016/j.pmcj.2020.101317](https://doi.org/10.1016/j.pmcj.2020.101317)

2. **Xu, L., Kwan, M.-P., McLafferty, S., & Wang, S. (2017).** *Predicting demand for 311 non-emergency municipal services: An adaptive space-time kernel approach.* Applied Geography, 89, 133–141. [DOI: 10.1016/j.apgeog.2017.10.012](https://doi.org/10.1016/j.apgeog.2017.10.012)

---

## 📄 License

This project is licensed under the **MIT License** — see [LICENSE](LICENSE) for details.

---

<p align="center">
  Built with ❤️ by Rakesh Dasari &nbsp;|&nbsp; CSE303 Machine Learning Capstone &nbsp;|&nbsp; 2026
</p>
