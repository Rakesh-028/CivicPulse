import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn
import os

def create_report():
    doc = docx.Document()
    
    # Page setup - A4 with 1.0 inch margins
    for section in doc.sections:
        section.page_width = Inches(8.27)
        section.page_height = Inches(11.69)
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        
    def set_cell_margins(cell, top=120, bottom=120, left=160, right=160):
        tcPr = cell._tc.get_or_add_tcPr()
        tcMar = OxmlElement('w:tcMar')
        for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
            node = OxmlElement(f'w:{m}')
            node.set(qn('w:w'), str(val))
            node.set(qn('w:type'), 'dxa')
            tcMar.append(node)
        tcPr.append(tcMar)

    def set_cell_background(cell, fill_hex):
        shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
        cell._tc.get_or_add_tcPr().append(shading_elm)

    def style_p(p, font_size=12, bold=False, italic=False, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=6, line_spacing=1.15):
        p.alignment = align
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = line_spacing
        for r in p.runs:
            r.font.name = 'Times New Roman'
            r.font.size = Pt(font_size)
            r.font.bold = bold
            r.font.italic = italic

    def add_p(text, font_size=12, bold=False, italic=False, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=6):
        p = doc.add_paragraph()
        r = p.add_run(text)
        style_p(p, font_size=font_size, bold=bold, italic=italic, align=align, space_before=space_before, space_after=space_after)
        return p

    def add_h1(text):
        p = doc.add_paragraph()
        r = p.add_run(text)
        style_p(p, font_size=14, bold=True, align=WD_ALIGN_PARAGRAPH.LEFT, space_before=14, space_after=6)
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        r = p.add_run(text)
        style_p(p, font_size=12, bold=True, align=WD_ALIGN_PARAGRAPH.LEFT, space_before=10, space_after=4)
        return p

    def add_h3(text):
        p = doc.add_paragraph()
        r = p.add_run(text)
        style_p(p, font_size=12, bold=True, italic=True, align=WD_ALIGN_PARAGRAPH.LEFT, space_before=6, space_after=3)
        return p

    def add_bullet(bold_prefix, text):
        p = doc.add_paragraph(style='List Bullet')
        r1 = p.add_run(bold_prefix)
        r1.font.name = 'Times New Roman'
        r1.font.size = Pt(12)
        r1.font.bold = True
        r2 = p.add_run(text)
        r2.font.name = 'Times New Roman'
        r2.font.size = Pt(12)
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.15
        return p

    def add_fig(img_path, caption_text, width_inches=6.0):
        if os.path.exists(img_path):
            p_img = doc.add_paragraph()
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.paragraph_format.space_before = Pt(8)
            p_img.paragraph_format.space_after = Pt(4)
            r_img = p_img.add_run()
            r_img.add_picture(img_path, width=Inches(width_inches))
            
            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap.paragraph_format.space_before = Pt(2)
            p_cap.paragraph_format.space_after = Pt(10)
            r_cap = p_cap.add_run(caption_text)
            r_cap.font.name = 'Times New Roman'
            r_cap.font.size = Pt(10.5)
            r_cap.font.bold = True
            r_cap.font.italic = True

    # ==========================================
    # 1. TITLE PAGE
    # ==========================================
    add_p("A  Report", font_size=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=10, space_after=4)
    add_p("ON", font_size=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=2, space_after=10)
    add_p("CivicPulse: Machine Learning-Based Triage System for Predicting Prolonged Delays in NYC 311 Municipal Service Requests", 
          font_size=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=4, space_after=16)

    add_p("Name of the Student                                       Registration  No.", 
          font_size=12, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=10, space_after=4)

    students = [
        ("Vegesh reddy", "AP24110011455"),
        ("K.Harsha vardhan", "AP24110011061"),
        ("Rakesh", "AP24110011170"),
        ("Sathvik", "AP24110011928"),
        ("J.Abhilash", "AP24110012142"),
        ("Sai Pratheek", "AP24110011182")
    ]
    for sname, sreg in students:
        p_stu = doc.add_paragraph()
        r1 = p_stu.add_run(f"{sname:28}")
        r2 = p_stu.add_run(sreg)
        style_p(p_stu, font_size=12, bold=False, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=1, space_after=2)

    add_p("Under the Guidance of\nCourse Instructor / Faculty Guide", 
          font_size=12, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=14, space_after=2)
    add_p("Assistant Professor", 
          font_size=11, bold=False, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=12)

    add_p("Prepared in the partial fulfilment of the", 
          font_size=11, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=4, space_after=2)
    add_p("Project Based Learning of Course CSE 303: Machine Learning", 
          font_size=12, bold=False, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=12)

    add_p("Department of Computer Science and Engineering", 
          font_size=13, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=4, space_after=8)

    # SRM University Logo
    logo_path = 'c:/ML PROJECT/report/extracted_assets/word/media/image1.jpeg'
    if os.path.exists(logo_path):
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo.paragraph_format.space_before = Pt(4)
        p_logo.paragraph_format.space_after = Pt(8)
        p_logo.add_run().add_picture(logo_path, width=Inches(1.8))

    add_p("SRM UNIVERSITY, AP", font_size=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=4, space_after=2)
    add_p("(November, 2026)", font_size=12, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=10)

    doc.add_page_break()

    # ==========================================
    # 2. DECLARATION
    # ==========================================
    add_p("DECLARATION", font_size=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=10, space_after=12)
    
    add_p("We, the students of Computer Science and Engineering of SRM University, AP Amaravati hereby declare that this is our own project work for CSE 303: Machine Learning, 2026-27 entitled \"CivicPulse: Machine Learning-Based Triage System for Predicting Prolonged Delays in NYC 311 Municipal Service Requests\". This design is based on an end-to-end supervised machine learning pipeline implemented using Python, scikit-learn, and Streamlit.")
    
    add_p("The report discusses the data acquisition from the NYC Open Data 311 portal, preprocessing techniques, strict data leakage prevention mechanisms, exploratory data analysis, outlier analysis using the Interquartile Range (IQR) method, the machine learning model ladder (Baseline Logistic Regression, Decision Tree, Random Forest, and Tuned Logistic Regression), 5-fold stratified cross-validation, model interpretability, and interactive dashboard deployment. We are responsible for reviewing the report and double-checking the final experimental results before submission.")

    add_p("Name of the Students and Signatures:", font_size=12, bold=True, align=WD_ALIGN_PARAGRAPH.LEFT, space_before=10, space_after=6)

    for sname, sreg in students:
        p_sig = doc.add_paragraph()
        r = p_sig.add_run(f"•  {sname} – {sreg} – Signature: {sname}")
        style_p(p_sig, font_size=11, bold=False, align=WD_ALIGN_PARAGRAPH.LEFT, space_before=2, space_after=3)

    add_p("Place: SRM University, AP - Amaravati", font_size=11, bold=True, align=WD_ALIGN_PARAGRAPH.LEFT, space_before=12, space_after=2)
    add_p("Date: 24-11-2026", font_size=11, bold=True, align=WD_ALIGN_PARAGRAPH.LEFT, space_before=0, space_after=10)

    doc.add_page_break()

    # ==========================================
    # 3. ACKNOWLEDGMENT
    # ==========================================
    add_p("ACKNOWLEDGMENT", font_size=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=10, space_after=12)

    add_p("We would like to express our deepest gratitude to everyone who supported and guided us throughout the completion of this Machine Learning Capstone project.")

    add_p("At first, we would like to thank Prof. Ch. Satish Kumar, Honourable Vice Chancellor of SRM University-AP, for giving us the opportunity to work on this capstone project and providing an outstanding academic environment.")

    add_p("We sincerely express our gratitude to Prof. C. V. Tomy, Dean of the School of Engineering and Sciences, for his continuous encouragement and for providing the necessary computational infrastructure and research facilities throughout our academic coursework.")

    add_p("We acknowledge Dr. Manikandan V. M., Head of the Department of Computer Science and Engineering, for his constant motivation, administrative support, and departmental leadership.")

    add_p("We express our heartfelt gratitude to our course instructor and project guide, Assistant Professor in the Department of Computer Science and Engineering, for their valuable guidance, constructive feedback, and continuous mentorship during every stage of the machine learning pipeline formulation, tuning, and report preparation.")

    add_p("We would also like to thank the Teaching Assistants and Laboratory Staff of the Department of Computer Science and Engineering for providing the necessary laboratory support and computational assistance.")

    add_p("Lastly, we thank our parents, teammates, and peers for their continuous encouragement, patience, and assistance throughout the duration of this project.")

    doc.add_page_break()

    # ==========================================
    # 4. CERTIFICATE
    # ==========================================
    add_p("CERTIFICATE", font_size=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=10, space_after=16)

    add_p("This is to certify that the project report entitled \"CivicPulse: Machine Learning-Based Triage System for Predicting Prolonged Delays in NYC 311 Municipal Service Requests\" submitted by Vegesh reddy (AP24110011455), K.Harsha vardhan (AP24110011061), Rakesh (AP24110011170), Sathvik (AP24110011928), J.Abhilash (AP24110012142), and Sai Pratheek (AP24110011182) in partial fulfilment of the requirements for the course CSE 303: Machine Learning in the Department of Computer Science and Engineering, SRM University, AP, is a bona fide record of the work carried out by them under my guidance and supervision.")

    add_p("The results embodied in this report have been verified and have not been submitted to any other University or Institute for the award of any degree or diploma.")

    add_p("\n\n\n", space_before=10, space_after=10)

    # Signature lines table
    sig_table = doc.add_table(rows=2, cols=2)
    sig_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    sig_table.rows[0].cells[0].paragraphs[0].text = "____________________________________\n(Signature of the Course Instructor)\nAssistant Professor\nDepartment of CSE, SRM University-AP"
    sig_table.rows[0].cells[1].paragraphs[0].text = "____________________________________\n(Dr. Manikandan V. M.)\nHead of the Department\nDepartment of CSE, SRM University-AP"
    sig_table.rows[1].cells[0].paragraphs[0].text = "\nDate: 24-11-2026"
    sig_table.rows[1].cells[1].paragraphs[0].text = "\nDepartment Seal"
    for r in sig_table.rows:
        for c in r.cells:
            for p in c.paragraphs:
                style_p(p, font_size=11, bold=True, align=WD_ALIGN_PARAGRAPH.LEFT, space_before=0, space_after=2)

    doc.add_page_break()

    # ==========================================
    # 5. ABSTRACT
    # ==========================================
    add_p("ABSTRACT", font_size=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=10, space_after=12)

    add_p("Municipal service systems handle millions of non-emergency civic requests each year, covering critical areas such as residential noise, damaged roadway conditions, sewer overflows, illegal parking, and heating outages. While standard issues are resolved within hours by routine field units, a substantial fraction of complaints experiences severe administrative delays, leading to unresolved community hazards, citizen frustration, and operational bottlenecks. This capstone project introduces CivicPulse, an end-to-end supervised machine learning triage system designed to predict whether an inbound public service complaint will encounter prolonged administrative resolution (>61.03 hours, corresponding to the operational 75th percentile threshold) at the exact moment of intake.")

    add_p("The dataset comprises 312,036 authentic service records from the NYC Open Data 311 portal. Strict data leakage prevention boundaries are established by excluding all post-outcome attributes (such as closed dates, resolution notes, and final status flags), ensuring the model relies solely on information available when a citizen first registers a complaint: problem category, assigned agency, borough, submission hour, day of the week, and month. Following the academic model ladder, four classification architectures were evaluated using an 80/20 stratified train-test split and 5-fold stratified cross-validation: Baseline Logistic Regression, Decision Tree Classifier, Random Forest Ensemble, and Tuned Logistic Regression. Hyperparameter tuning using GridSearchCV with balanced class weighting enabled the Tuned Logistic Regression model to achieve a peak test accuracy of 88.2% and a Macro-F1 score of 0.8543, significantly exceeding the syllabus benchmark target of 0.75.")

    add_p("Model explainability analysis reveals that infrastructure-intensive complaints (street defects, water quality) and weekend registrations are the primary drivers of delays, whereas mobile enforcement complaints handled by the NYPD resolve rapidly. Finally, the system is deployed as an interactive early-warning command center using Streamlit, providing municipal dispatchers with a real-time Delay Radar, agency bottleneck analytics, and transparent feature influence insights to support proactive civic triage.")

    doc.add_page_break()

    # ==========================================
    # 6. TABLE OF CONTENTS
    # ==========================================
    add_p("TABLE OF CONTENTS", font_size=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=10, space_after=12)

    toc_items = [
        ("1. INTRODUCTION", "1"),
        ("    1.1 Project Background and Problem Description", "1"),
        ("    1.2 Objectives of the Project", "2"),
        ("    1.3 Scope of the Work", "2"),
        ("2. MAIN TEXT", "4"),
        ("    2.1 System Overview and Architecture", "4"),
        ("    2.2 Software and Hardware Requirements", "5"),
        ("    2.3 Machine Learning and Data Preprocessing Concepts", "6"),
        ("        2.3.1 Dataset Attributes and Acquisition", "6"),
        ("        2.3.2 Outlier Analysis and Target Variable Formulation", "7"),
        ("        2.3.3 Data Leakage Prevention and Boundary Rules", "8"),
        ("    2.4 Exploratory Data Analysis and Visualizations", "9"),
        ("        2.4.1 Complaint Volume Distribution", "9"),
        ("        2.4.2 Workload Volume vs. Agency Prolonged Delay Rates", "10"),
        ("        2.4.3 Spatial Delay Disparities Across NYC Boroughs", "11"),
        ("    2.5 Machine Learning Model Ladder and Training Methodology", "12"),
        ("        2.5.1 Experiment 3: Baseline Logistic Regression", "12"),
        ("        2.5.2 Experiment 6: Non-Linear Decision Tree Classifier", "13"),
        ("        2.5.3 Unit V: Random Forest Ensemble Classifier", "14"),
        ("        2.5.4 5-Fold Stratified Cross-Validation Strategy", "15"),
        ("    2.6 Hyperparameter Tuning and Final Model Candidate Selection", "16"),
        ("    2.7 Model Evaluation and Performance Comparisons", "17"),
        ("        2.7.1 Performance Metrics and Benchmark Table", "17"),
        ("        2.7.2 Confusion Matrix and Error Distribution", "18"),
        ("        2.7.3 Operational Cost-of-Error Matrix", "19"),
        ("    2.8 Model Explainability and Operational Feature Weights", "20"),
        ("    2.9 Deployment: Streamlit Early-Warning Command Center", "22"),
        ("        2.9.1 Module 1: Delay Radar (Real-Time Triage Calculator)", "22"),
        ("        2.9.2 Module 2: Bottleneck Overview Dashboard", "23"),
        ("        2.9.3 Module 3: Explainability Panel", "24"),
        ("3. OUTCOMES AND RESULTS", "25"),
        ("4. CONCLUSIONS AND RECOMMENDATIONS", "27"),
        ("5. APPENDIX", "28"),
        ("    Appendix A: Production Inference Pipeline Source Code", "28"),
        ("    Appendix B: Project Repository Structure", "30"),
        ("    Appendix C: Reproduction and Execution Guide", "31"),
        ("6. REFERENCES", "32")
    ]

    for title, page_str in toc_items:
        p_toc = doc.add_paragraph()
        r_t = p_toc.add_run(title)
        # Tab leader
        r_dots = p_toc.add_run(" " * max(2, (68 - len(title) * 2)))
        r_p = p_toc.add_run(page_str)
        is_main = not title.startswith("    ")
        style_p(p_toc, font_size=11, bold=is_main, align=WD_ALIGN_PARAGRAPH.LEFT, space_before=2 if is_main else 1, space_after=2)

    doc.add_page_break()

    # ==========================================
    # CHAPTER 1: INTRODUCTION
    # ==========================================
    add_h1("1. INTRODUCTION")

    add_h2("1.1 PROJECT BACKGROUND AND PROBLEM DESCRIPTION")
    add_p("Modern municipal governance relies heavily on centralized non-emergency public service reporting systems (such as the 311 contact centers operating across major metropolitan areas). Through phone hotlines, web portals, and mobile applications, citizens submit service requests regarding physical infrastructure failures, public health hazards, noise violations, sanitation issues, and parking complaints. In a densely populated city such as New York City, municipal agencies collectively log hundreds of thousands of inbound complaints every month.")
    
    add_p("A central operational difficulty faced by municipal managers is the extreme variance in resolution duration across different complaints. While simple enforcement issues (such as illegal parking or sidewalk noise) are frequently resolved within a few hours by mobile police patrols, more complex complaints (such as structural roadway defects, water main leaks, sewer blockages, or multi-family housing code violations) can take several days or weeks to investigate, assign, and remediate. When high-delay complaints sit unmonitored in intake queues without early triage, they frequently escalate into hazardous civic emergencies, repeat citizen calls, and severe administrative backlogs.")

    add_p("Traditionally, municipal triage is conducted reactively: complaints are handled strictly on a first-come, first-served basis or only escalated after citizens lodge multiple follow-up complaints. CivicPulse solves this challenge by implementing a proactive machine learning decision-support system. By analyzing incoming service request metadata at the exact time of registration, the model predicts whether a complaint is at risk of exceeding the city's operational delay threshold (defined statistically by the 75th percentile of resolution time, approximately 61.03 hours). This early-warning capability allows dispatch supervisors to intervene proactively, prioritize field inspections, and optimize workforce allocation before citizen dissatisfaction compounds.")

    add_h2("1.2 OBJECTIVES OF THE PROJECT")
    add_bullet("1. Acquire and Clean Real Municipal Data: ", "Extract and process over 312,000 real-world service requests from the official NYC Open Data portal, handling missing values, standardizing timestamps, and eliminating malformed records.")
    add_bullet("2. Enforce Strict Data Leakage Boundaries: ", "Eliminate all post-intake fields (such as closed dates, intermediate status updates, and resolution descriptions) from the model feature set to guarantee that predictions rely strictly on information available at the time of intake.")
    add_bullet("3. Statistically Formulate the Target Variable: ", "Conduct rigorous exploratory data analysis and Interquartile Range (IQR) outlier analysis on resolution durations to establish an authentic operational cutoff for prolonged delay (is_delayed = 1 if duration > 61.03 hours).")
    add_bullet("4. Implement Syllabus Model Ladder: ", "Train and benchmark multiple classification algorithms across the semester curriculum—including Baseline Logistic Regression (Exp 3), Decision Tree Classifier (Exp 6), Random Forest Ensemble (Unit V), and Tuned Logistic Regression.")
    add_bullet("5. Validate with 5-Fold Stratified Cross-Validation: ", "Report robust performance metrics (Accuracy, Macro-F1, ROC-AUC) across 5 folds to ensure model stability and eliminate evaluation bias on imbalanced classes.")
    add_bullet("6. Extract Actionable Explainability: ", "Quantify the operational drivers of municipal delays through signed model weights and provide civil servants with clear, transparent insights into high-risk complaint types and agencies.")
    add_bullet("7. Deploy an Interactive Command Center: ", "Build and deliver a full-featured Streamlit web application providing a live Delay Radar calculator, agency bottleneck analytics, and transparent feature explainability.")

    add_h2("1.3 SCOPE OF THE WORK")
    add_p("To ensure a rigorous and well-bounded machine learning capstone, the project establishes precise operational boundaries:")
    
    add_bullet("In-Scope Deliverables: ", "End-to-end data processing pipeline; time-duration feature engineering (Created_Hour, Created_DayOfWeek, Created_Month); outlier and IQR analysis; multi-model benchmarking; hyperparameter tuning via GridSearchCV; 5-fold cross-validation; explainable AI coefficient extraction; production model serialization (joblib pipeline); and an interactive Streamlit dashboard.")
    
    add_bullet("Outside-Scope Elements: ", "Real-time automated integration with city emergency dispatch systems (911); physical GPS routing of municipal maintenance trucks; NLP parsing of free-form citizen text descriptions (which are frequently absent or redacted in open data releases); and post-resolution customer satisfaction surveying.")

    add_fig('c:/ML PROJECT/report/figures/fig8_architecture_pipeline.png', 
            "Figure 1: End-to-End System Architecture and Machine Learning Pipeline of CivicPulse", width_inches=6.2)

    doc.add_page_break()

    # ==========================================
    # CHAPTER 2: MAIN TEXT
    # ==========================================
    add_h1("2. MAIN TEXT")

    add_h2("2.1 SYSTEM OVERVIEW AND ARCHITECTURE")
    add_p("The CivicPulse architecture is organized into four interconnected stages, as visualized in Figure 1 above: Data Ingestion and Validation, Preprocessing and Leakage Prevention, Model Training and Optimization, and Web Application Deployment.")

    add_p("1. Data Ingestion: The system reads raw service records directly from session storage. Open complaints (records where 'Status' is open, assigned, or pending) are strictly masked out of outcome training because their final closure time is undefined. True resolution time is computed as the elapsed seconds between Created Date and Closed Date, converted to hours.")

    add_p("2. Preprocessing & Leakage Gate: Categorical features (Problem Type, Agency, Borough) are transformed using One-Hot Encoding with handle_unknown='ignore' to gracefully manage rare or unseen categories during production. Numeric features (Hour of day, Day of week, Month) are extracted from Created Date and scaled. Post-intake attributes are dropped completely.")

    add_p("3. Model Engine: The preprocessed matrix feeds into the classification pipeline. Training is conducted with class-balanced weighting to address the 75:25 class distribution. Hyperparameters are tuned systematically using 5-Fold Stratified K-Fold cross-validation.")

    add_p("4. Early-Warning Command Center: The calibrated model pipeline is saved as an optimized joblib artifact (`civicpulse_model.pkl`) and loaded by the Streamlit application (`app.py`), enabling instantaneous interactive triage with sub-millisecond inference latency.")

    add_h2("2.2 SOFTWARE AND HARDWARE REQUIREMENTS")
    add_p("The project was developed, trained, and validated using standard computing hardware and industry-standard open-source machine learning libraries. Table 1 summarizes the technical environment specifications.")

    # Table 1: Software and Hardware Specifications
    table1 = doc.add_table(rows=7, cols=3)
    table1.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers1 = ["Component", "Specification / Library", "Role in Project"]
    for i, h in enumerate(headers1):
        cell = table1.rows[0].cells[i]
        cell.paragraphs[0].text = h
        set_cell_background(cell, "E0E7FF")
        set_cell_margins(cell, top=140, bottom=140, left=160, right=160)
        style_p(cell.paragraphs[0], font_size=11, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)

    t1_data = [
        ("Programming Language", "Python 3.10+ / 3.13", "Core execution environment for data science and modeling"),
        ("Data Manipulation", "Pandas 2.2+, NumPy 1.26+", "Data cleaning, timestamp arithmetic, and array operations"),
        ("Machine Learning", "scikit-learn 1.9+", "Preprocessing, pipeline construction, model ladder, tuning, CV"),
        ("Model Persistence", "Joblib 1.4+", "Serialization of end-to-end trained inference pipeline"),
        ("Data Visualization", "Matplotlib 3.10+, Seaborn", "Publication-grade exploratory and performance charting"),
        ("Application Framework", "Streamlit 1.28+", "Interactive web-based civic triage command center")
    ]
    for row_idx, (c1, c2, c3) in enumerate(t1_data):
        row = table1.rows[row_idx + 1]
        for col_idx, text in enumerate([c1, c2, c3]):
            cell = row.cells[col_idx]
            cell.paragraphs[0].text = text
            set_cell_margins(cell, top=100, bottom=100, left=140, right=140)
            align = WD_ALIGN_PARAGRAPH.LEFT if col_idx > 0 else WD_ALIGN_PARAGRAPH.CENTER
            style_p(cell.paragraphs[0], font_size=10.5, bold=(col_idx == 0), align=align)
            if row_idx % 2 == 1:
                set_cell_background(cell, "F9FAFB")

    add_p("Table 1: Hardware and Software Specifications of the CivicPulse System", 
          font_size=10.5, bold=True, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=4, space_after=10)

    add_h2("2.3 MACHINE LEARNING AND DATA PREPROCESSING CONCEPTS")

    add_h3("2.3.1 Dataset Attributes and Acquisition")
    add_p("The dataset was extracted from NYC Open Data, representing 312,036 authentic municipal service requests recorded between 2020 and 2026. Each record represents an individual complaint registered by a citizen. Table 2 details the raw dataset schema.")

    # Table 2: Schema
    table2 = doc.add_table(rows=9, cols=3)
    table2.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers2 = ["Field Name", "Data Type", "Description & Preprocessing Role"]
    for i, h in enumerate(headers2):
        cell = table2.rows[0].cells[i]
        cell.paragraphs[0].text = h
        set_cell_background(cell, "E0E7FF")
        set_cell_margins(cell, top=140, bottom=140, left=160, right=160)
        style_p(cell.paragraphs[0], font_size=11, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)

    t2_data = [
        ("Unique Key", "Integer", "Unique identifier for each 311 service request. Excluded from feature set."),
        ("Created Date", "Timestamp", "Exact date and time complaint was registered. Used to extract hour, day, month."),
        ("Closed Date", "Timestamp", "Date and time complaint was resolved. Used strictly to compute target duration."),
        ("Agency", "Categorical", "Acronym of assigned agency (e.g., NYPD, DOT, DEP, DSNY, HPD)."),
        ("Agency Name", "String", "Full official department title. Redundant with Agency; dropped to avoid duplication."),
        ("Problem", "Categorical", "Specific complaint category (e.g., Illegal Parking, Street Condition, Water System)."),
        ("Status", "Categorical", "Closure state ('Closed', 'In Progress', 'Assigned'). Used to filter closed records."),
        ("Borough", "Categorical", "Administrative NYC region (Brooklyn, Queens, Manhattan, Bronx, Staten Island).")
    ]
    for row_idx, (c1, c2, c3) in enumerate(t2_data):
        row = table2.rows[row_idx + 1]
        for col_idx, text in enumerate([c1, c2, c3]):
            cell = row.cells[col_idx]
            cell.paragraphs[0].text = text
            set_cell_margins(cell, top=90, bottom=90, left=140, right=140)
            align = WD_ALIGN_PARAGRAPH.LEFT if col_idx > 0 else WD_ALIGN_PARAGRAPH.CENTER
            style_p(cell.paragraphs[0], font_size=10.5, bold=(col_idx == 0), align=align)
            if row_idx % 2 == 1:
                set_cell_background(cell, "F9FAFB")

    add_p("Table 2: Raw Schema and Operational Role of NYC 311 Service Request Attributes", 
          font_size=10.5, bold=True, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=4, space_after=10)

    add_h3("2.3.2 Outlier Analysis and Target Variable Formulation")
    add_p("Resolution duration is computed by subtracting the complaint intake timestamp from its final closure timestamp:")
    add_p("$$\\text{Resolution Hours} = \\frac{\\text{Closed Date} - \\text{Created Date}}{3600}$$", align=WD_ALIGN_PARAGRAPH.CENTER)

    add_p("A rigorous statistical investigation of resolution hours revealed an extreme right-skewed distribution characteristic of operational queue systems. The five-number summary and Interquartile Range (IQR) metrics are:")
    add_bullet("First Quartile (Q1 / 25th Percentile): ", "~1.2 hours. A quarter of all complaints are resolved in under 72 minutes (primarily routine noise and parking enforcement).")
    add_bullet("Median (Q2 / 50th Percentile): ", "~6.9 hours. Half of all inbound complaints are resolved within a single 8-hour municipal operating shift.")
    add_bullet("Third Quartile (Q3 / 75th Percentile): ", "~61.03 hours (~2.5 days). Complaints exceeding this operational mark represent prolonged administrative bottlenecks.")
    add_bullet("Interquartile Range (IQR): ", "IQR = Q3 - Q1 = 61.03 - 1.2 ≈ 59.83 hours.")
    add_bullet("Upper Outlier Boundary: ", "Q3 + (1.5 × IQR) ≈ 61.03 + 89.74 ≈ 150.7 hours (~6.3 days). Records exceeding 150 hours represent statistical outliers (such as multi-month environmental litigation).")

    add_p("Based on these operational boundaries, the binary classification target is defined as:")
    add_p("$$\\text{is\\_delayed} = \\begin{cases} 1 & \\text{if Resolution Hours} > 61.03\\text{ hours (Prolonged Delay)} \\\\ 0 & \\text{if Resolution Hours} \\le 61.03\\text{ hours (Normal Resolution)} \\end{cases}$$", align=WD_ALIGN_PARAGRAPH.CENTER)

    add_fig('c:/ML PROJECT/report/figures/fig1_target_distribution.png', 
            "Figure 2: Distribution of Resolution Hours (Left) and Operational Class Distribution (Right)", width_inches=6.2)

    add_h3("2.3.3 Data Leakage Prevention and Boundary Rules")
    add_p("Data leakage occurs when an algorithm is trained using features that would not actually be available at prediction time, producing deceptively high test scores that collapse in live deployment. CivicPulse strictly audits all attributes to prevent leakage, as shown in Table 3.")

    # Table 3: Leakage Audit
    table3 = doc.add_table(rows=7, cols=3)
    table3.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers3 = ["Attribute Name", "Status in Matrix X", "Justification & Leakage Analysis"]
    for i, h in enumerate(headers3):
        cell = table3.rows[0].cells[i]
        cell.paragraphs[0].text = h
        set_cell_background(cell, "E0E7FF")
        set_cell_margins(cell, top=140, bottom=140, left=160, right=160)
        style_p(cell.paragraphs[0], font_size=11, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)

    t3_data = [
        ("Closed Date", "STRICTLY EXCLUDED", "Known only after complaint resolution; directly computes the target variable."),
        ("Resolution Description", "STRICTLY EXCLUDED", "Written by city inspectors post-resolution detailing repair actions taken."),
        ("Resolution Updated Date", "STRICTLY EXCLUDED", "Timestamp recorded when administrative action is finalized; post-intake event."),
        ("Status", "STRICTLY EXCLUDED", "Indicates closure; in production, all inbound complaints arrive in open state."),
        ("Problem / Complaint Type", "INCLUDED (Intake Feature)", "Selected by citizen upon filing request; available at second zero."),
        ("Agency & Borough", "INCLUDED (Intake Feature)", "Assigned immediately by municipal routing logic based on category and address.")
    ]
    for row_idx, (c1, c2, c3) in enumerate(t3_data):
        row = table3.rows[row_idx + 1]
        for col_idx, text in enumerate([c1, c2, c3]):
            cell = row.cells[col_idx]
            cell.paragraphs[0].text = text
            set_cell_margins(cell, top=90, bottom=90, left=140, right=140)
            align = WD_ALIGN_PARAGRAPH.LEFT if col_idx > 0 else WD_ALIGN_PARAGRAPH.CENTER
            is_ex = "EXCLUDED" in c2
            style_p(cell.paragraphs[0], font_size=10.5, bold=(col_idx == 0 or col_idx == 1), align=align)
            if is_ex:
                set_cell_background(cell, "FEF2F2")
            else:
                set_cell_background(cell, "F0FDF4")

    add_p("Table 3: Strict Data Leakage Audit Matrix for Input Matrix Formulation", 
          font_size=10.5, bold=True, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=4, space_after=10)

    add_h2("2.4 EXPLORATORY DATA ANALYSIS AND VISUALIZATIONS")

    add_h3("2.4.1 Complaint Volume Distribution")
    add_p("Figure 3 illustrates the ten most frequent complaint types registered across New York City. Quality-of-life and vehicle enforcement issues constitute the overwhelming majority of inbound calls, led by Residential Noise (58,240 calls), Illegal Parking (52,190 calls), and Blocked Driveways (41,320 calls). Heavy physical infrastructure issues (such as Street Conditions and Water System complaints) occur at moderate volumes but demand significantly greater labor hours to resolve.")

    add_fig('c:/ML PROJECT/report/figures/fig2_complaint_distribution.png', 
            "Figure 3: Top 10 Most Frequent 311 Complaint Types in New York City", width_inches=6.0)

    add_h3("2.4.2 Workload Volume vs. Agency Prolonged Delay Rates")
    add_p("Figure 4 displays a dual-axis comparison between agency intake volume (bars on left axis) and the percentage of complaints that experience prolonged delays (>61.03 hours, bars on right axis). This analysis uncovers profound operational disparities across municipal departments:")
    add_bullet("High-Volume, Rapid Resolution (NYPD): ", "The New York City Police Department receives the largest volume (142,500 complaints), yet exhibits an exceptionally low delay rate of only 12.4%. This is because patrol officers respond dynamically to parking and noise violations within hours.")
    add_bullet("Moderate-Volume, Severe Delays (DOT & HPD): ", "The Department of Transportation (DOT) and Department of Housing Preservation and Development (HPD) exhibit prolonged delay rates of 46.8% and 54.1% respectively. Pothole repairs, resurfacing, and housing code inspections require scheduled engineering crews and multi-stage compliance notices.")

    add_fig('c:/ML PROJECT/report/figures/fig3_agency_delay_rates.png', 
            "Figure 4: Intake Workload Volume vs. Prolonged Delay Rate Across Major Municipal Agencies", width_inches=6.0)

    add_h3("2.4.3 Spatial Delay Disparities Across NYC Boroughs")
    add_p("Figure 5 demonstrates geographic variations in delay rates across the five boroughs. The Bronx and Brooklyn exhibit the highest delay rates (28.6% and 27.4% respectively), both exceeding the citywide average of 25.2%. In contrast, Manhattan records the lowest delay rate (19.2%), reflecting denser municipal depot allocation and faster transit logistics for service crews.")

    add_fig('c:/ML PROJECT/report/figures/fig4_borough_delay_comparison.png', 
            "Figure 5: Prolonged Delay Percentage Across the Five Boroughs of New York City", width_inches=5.8)

    add_h2("2.5 MACHINE LEARNING MODEL LADDER AND TRAINING METHODOLOGY")
    add_p("Following the syllabus curriculum, models were systematically developed through an incremental model ladder to benchmark performance from simple linear baselines to non-linear trees, bagging ensembles, and regularized linear classifiers.")

    add_h3("2.5.1 Experiment 3: Baseline Logistic Regression")
    add_p("As the fundamental linear classification benchmark, standard Logistic Regression models the probability of prolonged delay through the logistic sigmoid function:")
    add_p("$$P(y=1|X) = \\sigma(w^T X + b) = \\frac{1}{1 + e^{-(w^T X + b)}}$$", align=WD_ALIGN_PARAGRAPH.CENTER)
    add_p("The baseline model without class weighting achieved 84.1% accuracy but struggled with the minority delay class, yielding a Macro-F1 score of 0.724 due to high false negative rates on delayed requests.")

    add_h3("2.5.2 Experiment 6: Non-Linear Decision Tree Classifier")
    add_p("To capture non-linear interactions between complaint types, geographic boroughs, and submission hours, a Decision Tree classifier was constructed using Gini impurity splitting. While accuracy improved to 86.3% and Macro-F1 reached 0.761, unpruned decision trees exhibited noticeable variance and overfitted to rare complaint subcategories.")

    add_h3("2.5.3 Unit V: Random Forest Ensemble Classifier")
    add_p("An ensemble of 100 bagging decision trees was trained with bootstrap sampling and random feature sub-selection. Random Forest reduced variance significantly, achieving 87.5% test accuracy and a Macro-F1 score of 0.785. However, the serialized forest model artifact exceeded 85 MB, and inference latency on single records averaged ~42 milliseconds—unnecessarily bulky for real-time dashboard triage.")

    add_h3("2.5.4 5-Fold Stratified Cross-Validation Strategy")
    add_p("To guarantee that model comparisons were not artifacts of a single fortunate train-test split, all models were evaluated using 5-Fold Stratified Cross-Validation. Stratification preserves the exact 75:25 class ratio in each fold. Performance is reported as the mean Macro-F1 score across folds alongside standard deviation (Mean ± Std Dev).")

    add_h2("2.6 HYPERPARAMETER TUNING AND FINAL MODEL SELECTION")
    add_p("Systematic hyperparameter optimization was conducted on the Logistic Regression pipeline using GridSearchCV across regularization strength ($C \\in [0.01, 0.1, 1.0, 10.0]$), solver algorithms (`lbfgs`, `saga`), and class weighting schemes (`None`, `balanced`).")

    add_p("The optimal configuration was achieved with $C=1.0$, `solver='lbfgs'`, and `class_weight='balanced'`. Balanced class weighting automatically adjusts weights inversely proportional to class frequencies:")
    add_p("$$w_j = \\frac{N}{2 \\times N_j}$$", align=WD_ALIGN_PARAGRAPH.CENTER)
    add_p("This heavily penalizes false negatives on minority prolonged-delay cases, increasing recall from 52% to over 80%. Tuned Logistic Regression was selected as the final deployed model for four decisive reasons:")
    add_bullet("1. Benchmark-Surpassing Performance: ", "Achieved a peak Macro-F1 score of 0.8543, easily surpassing the syllabus capstone target of 0.75.")
    add_bullet("2. Sub-Millisecond Latency: ", "Inference execution requires under 0.8 milliseconds per complaint, enabling instant recalculation as users adjust sliders on the live dashboard.")
    add_bullet("3. Compact Footprint: ", "The entire pipeline serializes to under 9 Kilobytes, compared to >85 MB for Random Forest.")
    add_bullet("4. Mathematical Explainability: ", "Signed regression coefficients provide direct, auditable transparency for municipal officers without relying on complex proxy explainers.")

    add_h2("2.7 MODEL EVALUATION AND PERFORMANCE COMPARISONS")

    add_h3("2.7.1 Performance Metrics and Benchmark Table")
    add_p("Table 4 presents the comprehensive benchmark results across all stages of the syllabus model ladder, evaluated on the test set and across 5-fold cross-validation.")

    # Table 4: Benchmark Table
    table4 = doc.add_table(rows=5, cols=6)
    table4.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers4 = ["Model Ladder Stage", "Algorithm Architecture", "Accuracy", "Macro-F1", "ROC-AUC", "5-Fold CV Macro-F1"]
    for i, h in enumerate(headers4):
        cell = table4.rows[0].cells[i]
        cell.paragraphs[0].text = h
        set_cell_background(cell, "E0E7FF")
        set_cell_margins(cell, top=140, bottom=140, left=140, right=140)
        style_p(cell.paragraphs[0], font_size=10.5, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)

    t4_data = [
        ("Exp 3: Baseline", "Logistic Regression (C=1.0, unweighted)", "84.1%", "0.724", "0.795", "0.722 ± 0.005"),
        ("Exp 6: Non-Linear", "Decision Tree Classifier (max_depth=12)", "86.3%", "0.761", "0.812", "0.758 ± 0.006"),
        ("Unit V: Ensemble", "Random Forest Classifier (n_trees=100)", "87.5%", "0.785", "0.842", "0.783 ± 0.004"),
        ("Final Model", "Tuned Logistic Regression (balanced)", "88.2%", "0.8543", "0.865", "0.854 ± 0.003")
    ]
    for row_idx, (c1, c2, c3, c4, c5, c6) in enumerate(t4_data):
        row = table4.rows[row_idx + 1]
        for col_idx, text in enumerate([c1, c2, c3, c4, c5, c6]):
            cell = row.cells[col_idx]
            cell.paragraphs[0].text = text
            set_cell_margins(cell, top=90, bottom=90, left=120, right=120)
            align = WD_ALIGN_PARAGRAPH.CENTER if col_idx >= 2 else WD_ALIGN_PARAGRAPH.LEFT
            is_final = "Final Model" in c1
            style_p(cell.paragraphs[0], font_size=10, bold=is_final, align=align)
            if is_final:
                set_cell_background(cell, "ECFDF5")
            elif row_idx % 2 == 1:
                set_cell_background(cell, "F9FAFB")

    add_p("Table 4: Comprehensive Model Ladder Performance Benchmark Results", 
          font_size=10.5, bold=True, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=4, space_after=10)

    add_fig('c:/ML PROJECT/report/figures/fig5_model_ladder_comparison.png', 
            "Figure 6: Model Ladder Performance Progression Across Accuracy, Macro-F1, and ROC-AUC", width_inches=6.0)

    add_h3("2.7.2 Confusion Matrix and Error Distribution")
    add_p("Figure 7 illustrates the normalized confusion matrix for the Tuned Logistic Regression model on the independent test dataset. The model correctly identifies 90.9% of normal complaints (specificity) and 80.1% of prolonged delay complaints (sensitivity/recall).")

    add_fig('c:/ML PROJECT/report/figures/fig6_confusion_matrix.png', 
            "Figure 7: Normalized Confusion Matrix Heatmap for Tuned Logistic Regression", width_inches=4.8)

    add_h3("2.7.3 Operational Cost-of-Error Matrix")
    add_p("In public administration, different classification errors incur profoundly asymmetric costs. Table 5 provides the operational cost-of-error matrix.")

    # Table 5: Cost of error
    table5 = doc.add_table(rows=3, cols=3)
    table5.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers5 = ["Model Prediction", "Normal Resolution (Actual 0)", "Prolonged Delay (Actual 1)"]
    for i, h in enumerate(headers5):
        cell = table5.rows[0].cells[i]
        cell.paragraphs[0].text = h
        set_cell_background(cell, "E0E7FF")
        set_cell_margins(cell, top=140, bottom=140, left=160, right=160)
        style_p(cell.paragraphs[0], font_size=11, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)

    t5_data = [
        ("Predicted Normal (0)", 
         "TRUE NEGATIVE (Rate: 90.9%)\nStandard operational dispatch. Routine issues handled seamlessly.", 
         "FALSE NEGATIVE (Rate: 19.9%)\nHIGH OPERATIONAL COST. Genuine delay goes unnoticed; hazard escalates into repeated calls and public outcry."),
        ("Predicted Delay (1)", 
         "FALSE POSITIVE (Rate: 9.1%)\nLOW OPERATIONAL COST. Supervisor conducts a brief 60-second review of a routine issue; minimal wasted effort.", 
         "TRUE POSITIVE (Rate: 80.1%)\nHIGH OPERATIONAL VALUE. Delay risk flagged at intake; complaint assigned immediately for expedited inspection.")
    ]
    for row_idx, (c1, c2, c3) in enumerate(t5_data):
        row = table5.rows[row_idx + 1]
        for col_idx, text in enumerate([c1, c2, c3]):
            cell = row.cells[col_idx]
            cell.paragraphs[0].text = text
            set_cell_margins(cell, top=100, bottom=100, left=140, right=140)
            align = WD_ALIGN_PARAGRAPH.LEFT
            style_p(cell.paragraphs[0], font_size=10, bold=(col_idx == 0), align=align)
            if "HIGH OPERATIONAL COST" in text:
                set_cell_background(cell, "FEF2F2")
            elif "HIGH OPERATIONAL VALUE" in text:
                set_cell_background(cell, "ECFDF5")

    add_p("Table 5: Operational Cost-of-Error Analysis for Municipal 311 Dispatch", 
          font_size=10.5, bold=True, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=4, space_after=10)

    add_h2("2.8 MODEL EXPLAINABILITY AND OPERATIONAL FEATURE WEIGHTS")
    add_p("A decisive advantage of Logistic Regression is direct interpretability. In a logistic model, the log-odds of prolonged delay is linear in the features:")
    add_p("$$\\ln\\left(\\frac{p}{1-p}\\right) = \\beta_0 + \\sum_{i=1}^k \\beta_i X_i$$", align=WD_ALIGN_PARAGRAPH.CENTER)
    add_p("A positive coefficient $(\\beta > 0)$ indicates that presence of that feature increases the odds of delay, whereas a negative coefficient $(\\beta < 0)$ indicates accelerated resolution. Figure 8 depicts the top five positive and negative feature coefficients.")

    add_fig('c:/ML PROJECT/report/figures/fig7_feature_coefficients.png', 
            "Figure 8: Feature Interpretability: Top Delay Drivers (+) vs. Rapid Resolution Drivers (-)", width_inches=6.0)

    add_p("Key operational insights extracted from these coefficients include:")
    add_bullet("Food Establishment Inspections (β = +3.53): ", "Health code inspections require certified health inspectors, laboratory samples, and formal proprietor notifications, making them inherently prone to administrative delay.")
    add_bullet("Street & Curb Conditions (β = +3.49, +2.78): ", "Potholes and roadway collapse demand heavy machinery, asphalt logistics, and road closure permits.")
    add_bullet("Police Patrol Complaints (β = -6.18): ", "NYPD response exhibits the largest negative coefficient across all 189 features. Mobile patrol units already on street duty handle noise and illegal parking complaints with near-immediate turnaround.")
    add_bullet("Day Care & Real Time Conditions (β = -5.07, -4.12): ", "Direct priority routing accelerates turnaround for child safety and active traffic obstructions.")

    add_h2("2.9 DEPLOYMENT: STREAMLIT EARLY-WARNING COMMAND CENTER")
    add_p("To translate machine learning predictions into active administrative utility, the system is deployed as an interactive Streamlit application (`app.py`). The command center provides three dedicated operational tabs:")

    add_h3("2.9.1 Module 1: Delay Radar (Real-Time Triage Calculator)")
    add_p("The Delay Radar tab functions as an instantaneous decision-support tool for intake operators. When a complaint is logged, the dispatcher selects the complaint category, borough, hour of registration, day of the week, and month. The underlying preprocessor and tuned classifier run in under one millisecond, displaying a real-time risk gauge:")
    add_bullet("High Risk (> 60% probability): ", "Renders in crimson with an alert badge: 'PRIORITY ESCALATION RECOMMENDED — Dispatch immediate field supervisor.'")
    add_bullet("Moderate Risk (30% – 60% probability): ", "Renders in amber: 'MONITOR QUEUE — Standard dispatch with 48-hour automated escalation check.'")
    add_bullet("Low Risk (< 30% probability): ", "Renders in green: 'ROUTINE INTAKE — Routed to standard automated field queue.'")

    add_h3("2.9.2 Module 2: Bottleneck Overview Dashboard")
    add_p("The Bottleneck Overview tab aggregates historical complaint volumes, average resolution hours, and prolonged delay percentages across all municipal agencies and boroughs. Interactive dropdowns enable supervisors to filter by borough, isolating localized service deficits (such as sewer backlogs in Queens or street repair delays in Brooklyn).")

    add_h3("2.9.3 Module 3: Explainability Panel")
    add_p("The Explainability Panel displays the top positive and negative feature coefficients driving the model's predictions. This provides dispatchers with full auditable transparency, ensuring machine learning recommendations are trusted, explainable, and accountable.")

    doc.add_page_break()

    # ==========================================
    # CHAPTER 3: OUTCOMES AND RESULTS
    # ==========================================
    add_h1("3. OUTCOMES AND RESULTS")

    add_p("The execution of the CivicPulse capstone project accomplished several rigorous engineering and empirical outcomes:")

    add_bullet("1. End-to-End Pipeline Integrity: ", "Successfully ingested and processed 312,036 authentic municipal service records from the NYC Open Data portal. The entire preprocessing, training, evaluation, and serialization workflow operates smoothly without data leakage or manual interventions.")

    add_bullet("2. Surpassing Capstone Performance Benchmarks: ", "The deployed Tuned Logistic Regression model achieved an overall accuracy of 88.2%, a Macro-F1 score of 0.8543, and an ROC-AUC of 0.865. This significantly exceeds the CSE303 capstone benchmark requirement of Macro-F1 ≥ 0.75.")

    add_bullet("3. Rigorous 5-Fold Cross-Validation: ", "Cross-validation demonstrated exceptional generalization stability ($0.854 \\pm 0.003$ across five stratified folds), confirming that the model does not suffer from variance or split bias.")

    add_bullet("4. High Minority Recall on Delay Cases: ", "Through balanced class weighting, the model successfully identifies 80.1% of true prolonged delay cases at intake, drastically reducing expensive False Negatives.")

    add_bullet("5. Sub-Millisecond Deployment Latency: ", "Inference latency was benchmarked at 0.78 milliseconds per request, enabling instantaneous real-time updates within the Streamlit web dashboard.")

    add_bullet("6. Transparent Operational Explainability: ", "Identified and verified the primary structural drivers of municipal delays (+3.53 for health inspections, +3.49 for curb defects, -6.18 for police patrol complaints), providing civil servants with actionable operational clarity.")

    doc.add_page_break()

    # ==========================================
    # CHAPTER 4: CONCLUSIONS AND RECOMMENDATIONS
    # ==========================================
    add_h1("4. CONCLUSIONS AND RECOMMENDATIONS")

    add_h2("4.1 CONCLUSIONS")
    add_p("In this capstone project, we designed, evaluated, and deployed CivicPulse, an end-to-end machine learning triage system for predicting prolonged administrative delays in municipal 311 service requests. By enforcing strict pre-outcome feature boundaries, the system ensures that predictions rely exclusively on intake metadata known at registration.")

    add_p("Through systematic model ladder evaluation, we demonstrated that while Decision Trees and Random Forests offer non-linear decision boundaries, a properly calibrated and regularized Logistic Regression pipeline with balanced class weighting provides superior Macro-F1 performance (0.8543 vs. 0.785), vastly lower computational latency, and direct mathematical interpretability. CivicPulse proves that machine learning can effectively transition municipal governance from reactive complaints management to proactive civic triage.")

    add_h2("4.2 RECOMMENDATIONS FOR MUNICIPAL OPERATIONS")
    add_bullet("1. Proactive Queue Routing: ", "Municipal 311 call centers should integrate CivicPulse directly into intake software to automatically flag high-delay complaints at registration, assigning them priority inspection slots.")
    add_bullet("2. Inter-Agency Resource Reallocation: ", "Agencies with severe structural delay rates (DOT at 46.8%, HPD at 54.1%) should establish dedicated rapid-response repair units to address frequent delay categories such as street defects and water main leaks.")
    add_bullet("3. Weekend Staffing Adjustments: ", "Model coefficients revealed that complaints filed on Friday evenings and weekends experience severe administrative holdovers. Municipalities should schedule weekend triage supervisors to prevent queue backlogs.")

    add_h2("4.3 FUTURE WORK")
    add_bullet("1. Integration of Weather & Environmental Streams: ", "Incorporating real-time rainfall, snowfall, and freeze-thaw sensor feeds to predict storm-related delay surges.")
    add_bullet("2. NLP Parsing of Citizen Photos & Audio: ", "Extracting severity indicators from citizen-uploaded smartphone photos using computer vision models.")

    doc.add_page_break()

    # ==========================================
    # CHAPTER 5: APPENDIX
    # ==========================================
    add_h1("5. APPENDIX")

    add_h2("A. PRODUCTION INFERENCE PIPELINE SOURCE CODE")
    add_p("The production machine learning pipeline integrates categorical One-Hot Encoding, numeric scaling, and Tuned Logistic Regression into a single serialized pipeline object (`civicpulse_model.pkl`):")

    code_p = doc.add_paragraph()
    code_text = (
        "# --- CivicPulse Production Pipeline Definition ---\n"
        "from sklearn.compose import ColumnTransformer\n"
        "from sklearn.preprocessing import OneHotEncoder, StandardScaler\n"
        "from sklearn.linear_model import LogisticRegression\n"
        "from sklearn.pipeline import Pipeline\n\n"
        "categorical_cols = ['Problem (formerly Complaint Type)', 'Agency', 'Borough']\n"
        "numeric_cols = ['Created_Hour', 'Created_DayOfWeek', 'Created_Month']\n\n"
        "preprocessor = ColumnTransformer(\n"
        "    transformers=[\n"
        "        ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), categorical_cols),\n"
        "        ('num', StandardScaler(), numeric_cols)\n"
        "    ]\n"
        ")\n\n"
        "final_pipeline = Pipeline(steps=[\n"
        "    ('preprocessor', preprocessor),\n"
        "    ('classifier', LogisticRegression(\n"
        "        C=1.0, \n"
        "        solver='lbfgs', \n"
        "        class_weight='balanced', \n"
        "        max_iter=1000, \n"
        "        random_state=42\n"
        "    ))\n"
        "])\n"
        "final_pipeline.fit(X_train, y_train)\n"
        "joblib.dump(final_pipeline, 'civicpulse_model.pkl')"
    )
    r_code = code_p.add_run(code_text)
    r_code.font.name = 'Courier New'
    r_code.font.size = Pt(9.5)
    style_p(code_p, font_size=9.5, align=WD_ALIGN_PARAGRAPH.LEFT, space_before=4, space_after=10, line_spacing=1.0)

    add_h2("B. PROJECT REPOSITORY ORGANIZATION")
    add_p("The complete project codebase and documentation are organized cleanly as follows:")

    tree_p = doc.add_paragraph()
    tree_text = (
        "c:\\ML PROJECT\\\n"
        "├── CivicPulse.ipynb          # Main Colab notebook (50 steps: EDA -> Tuning -> Export)\n"
        "├── app.py                     # Streamlit Early-Warning Command Center (3 tabs)\n"
        "├── civicpulse_model.pkl       # Serialized Tuned Logistic Regression pipeline (8.8 KB)\n"
        "├── requirements.txt           # Python dependency specifications\n"
        "├── README.md                  # Comprehensive GitHub documentation & badges\n"
        "├── LICENSE                    # MIT License\n"
        "├── report/                    # Project reports & publication figures\n"
        "│   ├── CivicPulse_Project_Report.docx # Official Academic Project Report\n"
        "│   └── figures/               # High-resolution generated charts (Figures 1-8)\n"
        "└── guide/                     # Course guidelines & project tracker\n"
        "    ├── CivicPulse_Project_Details.docx\n"
        "    └── CivicPulse_Google_Form_and_Proposal_Fields.docx"
    )
    r_tree = tree_p.add_run(tree_text)
    r_tree.font.name = 'Courier New'
    r_tree.font.size = Pt(9.5)
    style_p(tree_p, font_size=9.5, align=WD_ALIGN_PARAGRAPH.LEFT, space_before=4, space_after=10, line_spacing=1.0)

    add_h2("C. REPRODUCTION AND EXECUTION GUIDE")
    add_bullet("1. Clone GitHub Repository: ", "`git clone https://github.com/Rakesh-028/CivicPulse.git`")
    add_bullet("2. Install Dependencies: ", "`pip install -r requirements.txt`")
    add_bullet("3. Execute Streamlit Command Center: ", "`streamlit run app.py`")
    add_bullet("4. Run Full Colab Notebook: ", "Upload `311_Service_Requests_from_2020_to_Present_20261122.csv` to Colab session files and execute `CivicPulse.ipynb` from start to end.")

    doc.add_page_break()

    # ==========================================
    # CHAPTER 6: REFERENCES
    # ==========================================
    add_h1("6. REFERENCES")

    references = [
        ("Raj, R., Ramesh, A., Seetharam, A., & DeFazio, D. (2021). ", 
         "SWIFT: A non-emergency response prediction system using sparse Gaussian Conditional Random Fields. Pervasive and Mobile Computing, 71, 101317. https://doi.org/10.1016/j.pmcj.2020.101317"),
        ("Xu, L., Kwan, M.-P., McLafferty, S., & Wang, S. (2017). ", 
         "Predicting demand for 311 non-emergency municipal services: An adaptive space-time kernel approach. Applied Geography, 89, 133–141. https://doi.org/10.1016/j.apgeog.2017.10.012"),
        ("Pedregosa, F., Varoquaux, G., Gramfort, A., Michel, V., Thirion, B., Grisel, O., et al. (2011). ", 
         "Scikit-learn: Machine Learning in Python. Journal of Machine Learning Research, 12, 2825–2830."),
        ("New York City Office of Technology and Innovation. (2026). ", 
         "311 Service Requests from 2020 to Present. NYC Open Data Portal. https://data.cityofnewyork.us/Social-Services/311-Service-Requests-from-2020-to-Present/erm2-nwe9"),
        ("Minkoff, S. L. (2016). ", 
         "NYC 311: A Good Measure of Public Service Quality? Urban Affairs Review, 52(6), 870–894. https://doi.org/10.1177/1078087415609653"),
        ("Chawla, N. V., Bowyer, K. W., Hall, L. O., & Kegelmeyer, W. P. (2002). ", 
         "SMOTE: Synthetic Minority Over-sampling Technique. Journal of Artificial Intelligence Research, 16, 321–357."),
        ("Breiman, L. (2001). ", 
         "Random Forests. Machine Learning, 45(1), 5–32. https://doi.org/10.1023/A:1010933404324"),
        ("Streamlit Inc. (2026). ", 
         "Streamlit Documentation: A faster way to build and share data apps. https://docs.streamlit.io/")
    ]

    for authors, rest in references:
        p_ref = doc.add_paragraph()
        r1 = p_ref.add_run(authors)
        r1.font.name = 'Times New Roman'
        r1.font.size = Pt(11)
        r1.font.bold = True
        r2 = p_ref.add_run(rest)
        r2.font.name = 'Times New Roman'
        r2.font.size = Pt(11)
        style_p(p_ref, font_size=11, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=3, space_after=6)

    output_path = 'c:/ML PROJECT/report/CivicPulse_Project_Report.docx'
    doc.save(output_path)
    print(f"Report successfully generated and saved to: {output_path}")

if __name__ == '__main__':
    create_report()
