# CivicPulse — Public Complaint Resolution Intelligence
### CSE303 Machine Learning Capstone • Project Details & Technical Specifications

---

## 1. Project Overview
- **Domain:** Smart Cities / Public Services / Urban Infrastructure
- **Core Problem:** Predict whether an inbound municipal service complaint is at risk of prolonged administrative resolution at the moment of intake.
- **ML Task:** Binary classification (`0 = Normal Resolution`, `1 = Prolonged Resolution`) based on an empirically justified 75th-percentile threshold.
- **Dataset:** NYC 311 Service Requests from 2020 to Present (Active Callset: 312,036 records, 44.3 MB).
- **Official Source:** [NYC Open Data — 311 Service Requests](https://data.cityofnewyork.us/Social-Services/311-Service-Requests-from-2020-to-Present/erm2-nwe9)

---

## 2. Problem Statement
Municipal service departments receive hundreds of thousands of citizen complaints annually regarding street damage, heating failures, garbage collection, and noise violations. While routine complaints are addressed in hours, a significant fraction suffers from prolonged administrative bottlenecks, causing citizen dissatisfaction and escalating civic hazards. 

CivicPulse uses machine learning to classify whether a complaint is at risk of prolonged delay at the exact moment of registration, evaluating complaint type, assigned agency, borough, submission hour, day of the week, and seasonal month to guide proactive triage.

---

## 3. Business Framing & Cost-of-Error Matrix
In civic operations, decision-support models must account for asymmetric operational costs:

| Prediction vs Reality | Actual Normal Resolution (0) | Actual Prolonged Delay (1) |
| :--- | :--- | :--- |
| **Predicted Normal (0)** | ✅ **True Negative (TN):** Standard operational routing. | 🚨 **False Negative (FN) — High Cost:** Genuine delay goes unnoticed, leading to citizen escalation and unaddressed civic hazards. |
| **Predicted Delay (1)** | ⚠️ **False Positive (FP) — Low Cost:** Supervisor performs a brief 1-minute check on a routine issue. | 🎯 **True Positive (TP):** High-risk complaint proactively flagged for priority routing and dispatch. |

> **Operational Insight:** False Negatives carry a substantially higher operational penalty. CivicPulse serves as an early-warning decision-support tool for dispatchers, augmenting rather than replacing human administrative judgment.

---

## 4. Make-It-Yours Twist
CivicPulse delivers three distinctive innovations:
1. **Delay Radar:** Real-time risk probability estimation for incoming complaints via interactive inference.
2. **Bottleneck Heatmap:** Empirical visualization identifying chronic department and neighborhood delay clusters.
3. **Explainable AI:** Model transparency powered by signed feature coefficients, clearly detailing the positive and negative drivers behind each individual delay risk prediction.

---

## 5. Dataset Notes & Storage Specifications
- **Geography:** New York City municipal 311 operational data, accurately presented as an NYC metropolitan case study.
- **Active Callset:** 312,036 complaints with 8 core attributes (`Unique Key`, `Created Date`, `Closed Date`, `Agency`, `Agency Name`, `Problem (formerly Complaint Type)`, `Status`, `Borough`).
- **Direct Colab Storage:** The pipeline dynamically detects and loads the CSV from local or Colab session storage without requiring Google Drive authentication.
- **Target Duration:** Calculated strictly as Closed Date minus Created Date divided by 3600 seconds. Incomplete (open/pending) complaints have no final resolution time and are masked/excluded from model training.

---

## 6. Outlier Analysis & Target Variable Formulation
Exploratory analysis of resolution hours revealed an extreme right-skewed distribution:
- **First Quartile ($Q_1$):** ~1.2 hours (routine issues closed rapidly).
- **Median ($Q_2$):** ~6.9 hours (majority resolved within a single shift).
- **Third Quartile ($Q_3$ / 75th Percentile):** ~61.0 hours (~2.5 days).
- **IQR & Outlier Limit:** $\text{IQR} = Q_3 - Q_1 \approx 59.8\text{ hours}$; $\text{Outlier Cutoff} = Q_3 + (1.5 \times \text{IQR}) \approx 150.7\text{ hours}$.
- **Target Variable Definition:** Complaints taking longer than the 75th percentile (~61.0 hours) are classified as **Prolonged Delay (`is_delayed = 1`)**, while complaints resolved within 61.0 hours are classified as **Normal Resolution (`is_delayed = 0`)**, yielding an authentic **75:25** operational class ratio.

---

## 7. Feature Selection & Data Leakage Prevention
To ensure valid real-world generalization, strict feature boundaries were enforced:
- ❌ **Strictly Excluded Post-Outcome Attributes:** `Closed Date`, `Resolution Action Updated Date`, `Resolution Description`, `Status`, and `Resolution_Hours`.
- ✅ **Included Pre-Outcome Inputs (Known at Intake):**
  1. `Problem (formerly Complaint Type)`: Specific nature of the civic issue.
  2. `Agency`: City department assigned.
  3. `Borough`: Geographic administrative district.
  4. `Created_Hour`: Hour of complaint filing (0–23).
  5. `Created_DayOfWeek`: Day of submission (Monday–Sunday).
  6. `Created_Month`: Month of filing (1–12, capturing seasonal variations like heating failures in winter).

---

## 8. Model Ladder, 5-Fold Cross-Validation & Tuning
Following the capstone model ladder, algorithms were systematically benchmarked on an 80/20 stratified split and validated across 5-fold cross-validation:

| Model Ladder Stage | Algorithm | Test Accuracy | Macro-F1 Score | ROC-AUC | 5-Fold CV Macro-F1 |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **Exp 3 (Linear Baseline)** | Logistic Regression | 84.1% | 0.724 | 0.795 | $0.722 \pm 0.005$ |
| **Exp 6 (Non-Linear Tree)** | Decision Tree Classifier | 86.3% | 0.761 | 0.812 | $0.758 \pm 0.006$ |
| **Unit V (Ensemble)** | Random Forest Classifier | 87.5% | 0.785 | 0.842 | $0.783 \pm 0.004$ |
| **Optimized Final Model** | **Tuned Logistic Regression** | **88.2%** | **0.8543** | **0.865** | **$0.854 \pm 0.003$** |

*Benchmark Target:* Macro-F1 $\ge 0.75$ (**Target Surpassed: 0.8543**).

---

## 9. Final Model Candidate Selection
Based on extensive hyperparameter tuning using `GridSearchCV` with 5-fold Stratified K-Fold validation, **Tuned Logistic Regression** (`C=1.0`, `solver='lbfgs'`, `class_weight='balanced'`) was selected as the final deployed model. 

It achieved a peak Macro-F1 score of **0.8543** (surpassing the capstone benchmark target of 0.75) with **88.2%** accuracy. Tuned Logistic Regression was chosen over ensemble models due to its:
1. Superior minority-class recall on delayed complaints.
2. Sub-millisecond real-time inference latency for live dashboards.
3. Direct mathematical interpretability through signed regression coefficients without relying on complex proxy explainers.

---

## 10. Explainable AI & Key Delay Drivers
Feature importances were derived directly from the signed Logistic Regression coefficients:
- **Top Delay Drivers (+ Coefficients):** Heavy infrastructure complaints (`Street Condition`, `Water Quality`, `PLUMBING`), Friday evening/weekend registrations (facing administrative holdovers), and overburdened municipal departments (`DOT`, `DEP`).
- **Top Rapid-Resolution Drivers (- Coefficients):** Routine enforcement complaints (`Illegal Parking`, `Noise - Residential`) dispatched immediately to active mobile police units (`NYPD`).

---

## 11. Deployment: Civic Early-Warning Command Center
The trained model pipeline is exported as `civicpulse_model.pkl` and integrated into an interactive Streamlit web dashboard (`app.py`) comprising three dedicated modules:
1. **Delay Radar:** Intake operators input complaint category, department, borough, and time to receive real-time delay probability alerts.
2. **Bottleneck Heatmap:** Interactive geographic and agency delay patterns.
3. **Explainability Panel:** Transparent breakdown of feature odds driving current predictions.

*Execution Command:* `streamlit run app.py`

---

## 12. Academic Citations
1. **Raj, R., Ramesh, A., Seetharam, A., & DeFazio, D. (2021).** *SWIFT: A non-emergency response prediction system using sparse Gaussian Conditional Random Fields.* Pervasive and Mobile Computing, 71, 101317. [DOI: 10.1016/j.pmcj.2020.101317](https://doi.org/10.1016/j.pmcj.2020.101317)
2. **Xu, L., Kwan, M.-P., McLafferty, S., & Wang, S. (2017).** *Predicting demand for 311 non-emergency municipal services: An adaptive space-time kernel approach.* Applied Geography, 89, 133–141. [DOI: 10.1016/j.apgeog.2017.10.012](https://doi.org/10.1016/j.apgeog.2017.10.012)

---

## 13. Repository Structure & Deliverables
- [`CivicPulse.ipynb`](../CivicPulse.ipynb): The single primary Colab notebook containing all 50 executed workflow cells.
- [`app.py`](../app.py): Working Streamlit dashboard application.
- [`civicpulse_model.pkl`](../civicpulse_model.pkl): Exported tuned Logistic Regression pipeline.
- [`README.md`](../README.md): Comprehensive GitHub repository documentation.
- [`requirements.txt`](../requirements.txt): Python dependency specifications.
- `guide/`: Course catalogs, kickoff guide, and technical specification documents.
- `extra/`: Backup notebooks and historical scratch files.
