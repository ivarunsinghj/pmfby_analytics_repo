# GitHub Publishing & Portfolio Deployment Master Guide
## PMFBY Actuarial & Settlement Analytics (Power BI + Excel BI + SQL)

This guide provides end-to-end instructions for publishing this project to **GitHub**, connecting your data sources across **SQL, Excel, and Power BI**, creating a public portfolio presentation, and showcasing it on **LinkedIn and your Resume**.

---

## 📌 1. Repository Directory Mapping: "What Goes Where"

When uploaded to GitHub, your repository will follow this standardized industry structure:

| Folder / File Path | Contents & Resource Type | Why It Belongs Here & What Recruiters Look For |
| :--- | :--- | :--- |
| `README.md` | Root documentation & architecture | High-level executive overview, problem statement, architecture diagrams, and core findings. |
| `data/pmfby_actuarial.db` | Relational SQLite Database | Demonstrates database design, foreign keys, and normalized schema. |
| `data/*.csv` | Master Fact & Dimension CSVs | Raw data access for viewers without SQLite installed; used for Power Query ingestion. |
| `sql/01_schema_ddl.sql` | Schema DDL & Indexing | Shows database engineering skills (DDL, primary/foreign keys, optimization indexes). |
| `sql/02_data_transformation_etl.sql` | Analytical Views & Feature Engineering | Demonstrates SQL ETL, derived metric calculation, performance bands, and categorization. |
| `sql/03_descriptive_analysis.sql` | Descriptive Analysis Queries | Analytical SQL competence (Window functions, rollups, aggregations, cohort tracking). |
| `sql/04_diagnostic_analysis.sql` | Diagnostic Root-Cause Queries | Advanced SQL (Z-Score calculation, CCE dispute friction, turnaround time percentiles). |
| `sql/05_predictive_prescriptive_modeling.sql` | Prescriptive Actuarial SQL | Algorithmic logic in SQL (Composite scoring, 80:110 Beed Model simulation, queue triage). |
| `power_bi/PMFBY_Actuarial_Analytics_Dashboard.pbit`| Power BI Template File | Complete portable Power BI model (Tables, Relationships, DAX Measures, and Report Layout). |
| `power_bi/dax/*.dax` | Modular DAX Measure Scripts | Readable code version of all DAX measures (KPIs, Diagnostics, What-If Parameters). |
| `power_bi/power_query_m/*.m` | Power Query (M) Scripts | Documented ETL transformation logic for clean data extraction and type conversion. |
| `power_bi/visual_specs/` | Visual Design Specification | Documentation of 4 dashboard pages, color hex tokens, visual fields, and conditional formatting. |
| `power_bi/interactive_preview/index.html`| Interactive Web Dashboard Preview | Web-based mockup enabling visitors to test the dashboard in any browser without Power BI Desktop. |
| `excel/PMFBY_Actuarial_BI_Dashboard.xlsx` | Multi-Tab Excel BI Workbook | Validated Excel BI model with dynamic formulas (`SUMIFS`, `AVERAGEIFS`), KPI cards, and charts. |
| `reports/PMFBY_Comprehensive_Data_Analysis_Report.pdf`| 7-Page Publication PDF Report | Formal executive deliverable showing end-to-end analytical rigor and business communication. |
| `reports/PMFBY_Data_Analysis_Report.md` | Markdown Version of Report | Clean text version viewable directly in GitHub's web interface. |
| `scripts/*.py` | Python Automation & Pipeline Scripts | Reproducible data generation, SQLite pipeline execution, and automated report compilation. |

---

## 💻 2. Step-by-Step Git Commands to Push to GitHub

### Step 2.1: Create a New GitHub Repository
1. Log in to [GitHub](https://github.com/) and click **New Repository** (or visit `https://github.com/new`).
2. **Repository Name**: `pmfby-actuarial-powerbi-sql-analytics`
3. **Description**: `End-to-End Indian Public Data Analysis: Pradhan Mantri Fasal Bima Yojana (PMFBY) Actuarial Loss Ratios, Settlement Bottlenecks & 80:110 Beed Model using Power BI, Excel BI, and SQL.`
4. Set to **Public**.
5. Leave **Add a README file**, **.gitignore**, and **license** unchecked (since our repository already has complete files).
6. Click **Create repository**.

### Step 2.2: Initialize and Push from Your Local Terminal
Open your terminal inside the project directory:

```bash
# Navigate to the repository root
cd pmfby_analytics_repo

# Initialize git tracking
git init

# Add standard .gitignore to exclude system cache files
cat << 'EOF' > .gitignore
__pycache__/
*.pyc
.DS_Store
recalc_tmp/
EOF

# Stage all files
git add .

# Commit with a professional semantic commit message
git commit -m "feat: complete PMFBY actuarial analytics portfolio with Power BI, Excel BI, SQL pipeline & report"

# Set default branch to main
git branch -M main

# Link to your new GitHub repository (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/pmfby-actuarial-powerbi-sql-analytics.git

# Push all files to GitHub
git push -u origin main
```

---

## 🔗 3. Connecting Excel to SQL & Data Sources

To demonstrate industry-level integration, the Excel workbook can be wired directly to live data:

### Method A: Native Excel Connection to SQLite / PostgreSQL / SQL Server
1. Open Microsoft Excel and go to the **Data** tab on the top ribbon.
2. Click **Get Data** > **From Database** > **From SQL Server Database** (or **From Other Sources** > **From ODBC** for SQLite).
3. If using ODBC for SQLite:
   - Open Windows **ODBC Data Source Administrator (64-bit)**.
   - Add a System DSN pointing to `data/pmfby_actuarial.db`.
   - In Excel, select **From ODBC** > choose your DSN > select table `fact_pmfby_claims_enrolment`.
4. Click **Load To...** > Select **Only Create Connection** and check **Add this data to the Data Model**.
5. Go to **Data** > **Manage Data Model (Power Pivot)** to view the integrated in-memory tabular database.

### Method B: Power Query Live File Connection (Self-Contained)
1. In `PMFBY_Actuarial_BI_Dashboard.xlsx`, the sheet `Data_Model_FactTable` contains the normalized fact records.
2. The summary sheets (`Executive_Summary`, `Descriptive_Analysis`, `Diagnostic_DeepDive`, `Prescriptive_BeedModel`) use dynamic Excel-2007 compatible cross-sheet formulas (`SUMIFS`, `AVERAGEIFS`, `IFERROR`).
3. Whenever raw data in `Data_Model_FactTable` is updated, all KPI cards, margin totals, and embedded charts recalculate automatically across the entire workbook.

---

## 📊 4. How to Open & Configure the Power BI Dashboard

### Method A: Opening the Power BI Template (`.pbit`)
1. Download `PMFBY_Actuarial_Analytics_Dashboard.pbit` from the `power_bi/` directory.
2. Double-click the `.pbit` file to launch **Power BI Desktop**.
3. When prompted, confirm the parameter path or select the source folder pointing to `data/pmfby_district_level_master.csv` (or your SQL connection).
4. Power BI will automatically instantiate the semantic data model, wire all 4 relationships, load all 24 DAX measures from `_Key_Measures`, and render the report canvas!
5. Save the file locally as `PMFBY_Actuarial_Analytics_Dashboard.pbix`.

### Method B: Building from Scratch Using Provided Resources
If you prefer to demonstrate building the model step-by-step in an interview:
1. **Get Data**: Open Power BI Desktop > Click **Get Data** > **Text/CSV** > Select `data/pmfby_district_level_master.csv` and the 4 dimension CSVs.
2. **Apply Power Query (M)**: Open Advanced Editor in Power Query and paste the code from `power_bi/power_query_m/Fact_ClaimsEnrolment.m`.
3. **Model Relationships**: In Model View, connect:
   - `fact[district_id]` → `dim_districts[district_id]` (1:* Single)
   - `fact[crop_id]` → `dim_crops[crop_id]` (1:* Single)
   - `fact[season_id]` → `dim_seasons[season_id]` (1:* Single)
   - `fact[insurer_id]` → `dim_insurers[insurer_id]` (1:* Single)
4. **Load DAX Measures**: Create an empty table `_Key_Measures` and copy-paste the measures from `power_bi/dax/01_kpi_measures.dax`, `02_diagnostic_measures.dax`, and `03_prescriptive_beed_measures.dax`.
5. **Follow Visual Specs**: Recreate the 4 report pages following `power_bi/visual_specs/dashboard_design_specification.md`.

---

## 📦 5. Creating GitHub Releases for Large Deliverable Files

Because `.pbix` or `.xlsx` files can be downloaded directly by hiring managers without cloning git, publish them as a **GitHub Release**:
1. On your GitHub repo page, click **Releases** (on the right sidebar) > **Draft a new release**.
2. **Tag version**: `v1.0.0`
3. **Release title**: `PMFBY Actuarial Analytics v1.0.0 — Production Release`
4. **Description**:
   ```markdown
   ### 🌾 Production Release: PMFBY Actuarial & Settlement Analytics
   - **Full Power BI Template**: `PMFBY_Actuarial_Analytics_Dashboard.pbit`
   - **Interactive Excel BI Model**: `PMFBY_Actuarial_BI_Dashboard.xlsx`
   - **7-Page Formal Analytical PDF Report**: `PMFBY_Comprehensive_Data_Analysis_Report.pdf`
   - **Relational SQLite Database**: `pmfby_actuarial.db`
   ```
5. Drag and drop the `.pbit`, `.xlsx`, and `.pdf` files into the **Attach binaries** box.
6. Click **Publish release**.

---

## 🌐 6. Enabling GitHub Pages for the Interactive Web Preview

To give anyone an instant, clickable web link to test your dashboard right from their browser:
1. In your GitHub repository, click **Settings** > **Pages** (left sidebar).
2. Under **Build and deployment** > **Source**: Select `Deploy from a branch`.
3. Select `main` branch and `/ (root)` folder (or create a `docs` folder with `index.html`).
4. Alternatively, link to `power_bi/interactive_preview/index.html` in your README.

---

## 💼 7. LinkedIn Project Showcase Post Template

Copy and adapt this text when posting about your project on LinkedIn:

```text
🚀 Excited to share my latest end-to-end Data Analytics & BI project: 
"Pradhan Mantri Fasal Bima Yojana (PMFBY): Actuarial Loss-Cost Ratios, Settlement Bottlenecks & Prescriptive Risk Sharing Across Indian States" 🌾📊

In this project, I analyzed 33.68 million farmer applications across 36 agro-climatic districts (Maharashtra, MP, Rajasthan, UP, Odisha, Karnataka) representing ₹25,908 Cr in underwritten premiums to solve key operational bottlenecks in agricultural insurance.

Key Highlights:
1️⃣ Descriptive Analysis: Uncovered a stark structural divergence between Kharif monsoon operations (63.6% Loss Cost Ratio, 158.2 days turnaround time) and irrigated Rabi cycles (47.8% LCR, 117.6 days TAT).
2️⃣ Diagnostic Root-Cause Analysis: Proved that state subsidy disbursal delays are the primary driver of farmer payout latency—settlement TAT spikes 4x from 62.3 days to 245.5 days when state subsidy tranches are deferred, locking ~₹490 Cr in administrative escrow.
3️⃣ Prescriptive Modeling: Simulated the 80:110 "Beed Model" across 6 states over 5 years, revealing that state governments would recover ₹7,644 Cr in surplus clawbacks against ₹490 Cr in catastrophic liabilities, generating a net fiscal gain of ₹7,154 Cr for state exchequers.

🛠️ Tech Stack:
• SQL: Relational Star Schema, Window Functions, Z-Score Anomaly Detection, CTEs
• Power BI: Data Modeling, DAX Measures, Slicers, What-If Parameters, Visual Storytelling
• Excel BI: Live Data Model, Dynamic SUMIFS/AVERAGEIFS, KPI Cards, Embedded Visuals
• Python: Reproducible data engineering pipeline & PDF report compilation

🔗 GitHub Repository: [INSERT YOUR GITHUB URL HERE]
📄 Full 7-Page Analytical Report: [INSERT LINK]

Feedback and thoughts are welcome!

#DataAnalytics #PowerBI #SQL #ExcelBI #BusinessIntelligence #ActuarialScience #DataVisualization #PMFBY #Agritech #PortfolioProject
```

---

## 📝 8. Resume Bullet Points for Your CV

Add these bullet points under your **Projects** section:

- **PMFBY Actuarial & Settlement Analytics (Power BI, Excel BI, SQL, Python)**
  - Engineered an end-to-end data pipeline analyzing 33.68M farmer applications across 36 Indian districts (₹25,908 Cr premium), uncovering an aggregate 57.62% loss-cost ratio and regional latency patterns.
  - Built a relational star schema in SQL utilizing window functions (`OVER PARTITION BY`) to compute Z-score loss-cost anomalies and diagnosed a 4x claim settlement latency spike (62d to 245d) driven by state subsidy disbursal lags.
  - Developed a 4-page interactive Power BI dashboard featuring 24 custom DAX measures, dynamic what-if parameters, and simulated the 80:110 "Beed Model", identifying a potential ₹7,154 Cr net fiscal surplus for state exchequers.
  - Authored a 7-page publication-quality PDF report and designed a companion 5-tab Excel BI workbook with formula validation, KPI metrics, and embedded charts.
