# Pradhan Mantri Fasal Bima Yojana (PMFBY): An Empirical Data Analysis of Actuarial Loss-Cost Ratios, Claim Settlement Bottlenecks, and Prescriptive Risk Sharing Across Indian States (2019–2024)

**Dataset Coverage:** 36 Agro-Climatic Districts across 6 Indian States (MH, MP, RJ, UP, OD, KA) | 10 Seasons (Kharif & Rabi 2019–2024)  
**Analytical Domains:** Descriptive Baseline, Diagnostic Root-Cause & Anomaly Detection, Prescriptive 80:110 Beed Model Simulation  
**Technical Stack:** SQL (Relational Star Schema & Analytics), Excel BI (Data Model & Native Visuals), SQLite Core Engine

---

## 1. Executive Summary & National Portfolio Overview
The Pradhan Mantri Fasal Bima Yojana (PMFBY), instituted by the Ministry of Agriculture & Farmers Welfare (MoA&FW) in 2016, represents one of the largest agricultural risk-transfer mechanisms globally, providing comprehensive social safety nets against non-preventable natural risks for Indian farmers. While the scheme has underwritten hundreds of thousands of crores in crop liability, it operates under structural tensions involving farmer premium affordability, actuarial solvency of general insurers, fiscal sustainability of state subsidy obligations, and timely claim disbursement through Direct Benefit Transfer (DBT).

This empirical investigation examines a high-fidelity longitudinal dataset comprising 930 seasonal district-crop evaluations across 36 agro-climatic districts in six representative agricultural states: Maharashtra, Madhya Pradesh, Rajasthan, Uttar Pradesh, Odisha, and Karnataka. The analysis systematically evaluates 33.68 million farmer applications representing ₹25,908.62 Crores in cumulative gross premiums underwritten between 2019 and 2024. Across the evaluated multi-year horizon, ₹14,928.39 Crores in indemnity claims were disbursed to distressed agricultural households, establishing an aggregate national Loss-Cost Ratio (LCR, or Burn Rate) of 57.62%.

Despite healthy aggregate actuarial solvency, deep structural disparities persist across states, seasons, and farming cohorts. The average settlement Turnaround Time (TAT) stands at 141.2 days from harvest completion, with acute regional bottlenecks exceeding 240 days. Through three distinct analytical paradigms—Descriptive, Diagnostic, and Prescriptive—this study uncovers the foundational drivers of claim delays, detects spatial yield anomalies, and models the fiscal viability of alternative risk-sharing frameworks such as the 80:110 "Beed Model".

---

## 2. Multi-Year State Actuarial Performance & Baseline Metrics
Under the standard PMFBY operational guidelines, farmers contribute a statutory capped premium: 2.0% of Sum Insured for Kharif foodgrains and oilseeds, 1.5% for Rabi crops, and 5.0% for commercial/horticultural crops. The remainder of the Actuarial Premium Rate (APR)—which routinely ranges between 8% and 22% in vulnerable agro-climatic belts—is subsidized on an equal 50:50 basis by the Central Government and the respective State Government.

| State Name | Districts | Farmer Applications | Gross Premium (₹ Cr) | Claims Paid (₹ Cr) | Net Balance (₹ Cr) | LCR (%) | Avg TAT (Days) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Maharashtra** | 6 | 7,842,100 | 5,544.20 | 3,398.03 | +2,146.17 | 61.29% | 178.4 |
| **Uttar Pradesh** | 6 | 5,420,800 | 4,336.17 | 2,823.74 | +1,512.43 | 65.12% | 152.1 |
| **Odisha** | 6 | 4,215,600 | 3,426.38 | 1,966.90 | +1,459.48 | 57.40% | 164.8 |
| **Madhya Pradesh** | 6 | 5,918,400 | 4,083.89 | 2,338.11 | +1,745.78 | 57.25% | 88.5 |
| **Karnataka** | 6 | 5,114,200 | 4,555.80 | 2,455.73 | +2,100.07 | 53.90% | 124.6 |
| **Rajasthan** | 6 | 5,171,200 | 3,962.18 | 1,945.88 | +2,016.30 | 49.11% | 138.9 |
| **National Total / Avg** | **36** | **33,682,300** | **25,908.62** | **14,928.39** | **+10,980.23** | **57.62%** | **141.2** |

---

## 3. Empirical Analysis 1: Descriptive & Exploratory Baseline
### Seasonal Polarization: Kharif Monsoon Volatility vs Rabi Relative Stability
A critical characteristic of Indian agriculture is the asymmetric risk profile between the Kharif (Southwest Monsoon) and Rabi (Winter/Post-Monsoon) cropping seasons. Kharif cultivation is predominantly rainfed, exposing smallholders to erratic monsoon onsets, prolonged dry spells, and catastrophic localized flooding. In contrast, Rabi cultivation relies more heavily on tube-well, canal, and residual soil moisture irrigation.

| Cropping Season | Evaluations | Gross Premium (₹ Cr) | Claims Paid (₹ Cr) | Loss Cost Ratio (%) | Avg Yield Shortfall (%) | Avg TAT (Days) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Kharif (Monsoon)** | 540 | 16,112.45 | 10,248.80 | 63.61% | 22.4% | 158.2 |
| **Rabi (Winter)** | 390 | 9,796.17 | 4,679.59 | 47.77% | 14.1% | 117.6 |

### Crop Category Actuarial Distribution
Crop categories display starkly divergent risk profiles. Commercial and cash crops (notably Cotton) exhibit both the highest actuarial rates (averaging 16.5%) and the highest farmer statutory premium contribution (5.0%). Foodgrains (Paddy and Wheat) anchor the portfolio in absolute volume, while Pulses and Oilseeds bear significant production vulnerability.

| Crop Category | Sample Count | Gross Premium (₹ Cr) | Claims Paid (₹ Cr) | LCR (%) | Statutory Rate (%) | Actuarial Rate (%) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Foodgrains (Paddy, Wheat)** | 300 | 9,412.30 | 4,988.52 | 53.00% | 1.5% – 2.0% | 10.4% |
| **Oilseeds (Soybean, Mustard, Groundnut)** | 240 | 7,245.80 | 4,383.71 | 60.50% | 1.5% – 2.0% | 12.1% |
| **Pulses (Gram, Tur/Arhar)** | 240 | 5,118.42 | 3,173.42 | 62.00% | 1.5% – 2.0% | 11.8% |
| **Commercial Crops (Cotton)** | 90 | 2,884.10 | 1,672.78 | 58.00% | 5.0% | 16.5% |
| **Coarse Cereals (Bajra, Jowar)** | 60 | 1,248.00 | 709.96 | 56.89% | 1.5% – 2.0% | 9.8% |

---

## 4. Empirical Analysis 2: Diagnostic & Root-Cause Analysis
### Settlement Latency Root-Cause: The State Subsidy Disbursal Bottleneck
Under scheme guidelines, insurance companies are legally indemnified against paying claims until the corresponding state government releases its requisite 50% premium subsidy installment.

| State Subsidy Status | Total Cases | Avg Subsidy Delay (Days) | Avg Claim TAT (Days) | Min / Max TAT | Fulfillment Rate (%) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Settled on Time** | 523 | 38.0 | 62.3 | 32 / 94 | 100.0% |
| **Delayed 3–6 Months** | 241 | 201.7 | 245.5 | 142 / 315 | 81.7% |
| **Delayed >6 Months** | 166 | 194.0 | 238.1 | 138 / 340 | 80.5% |

### CCE Discrepancy & Dispute Friction in Claim Rejections
In administrative units where CCE discrepancy rates exceeded 10.0%, farmer claim rejections rose to 9.6%—nearly triple the baseline rejection rate of 3.4% observed in clean verification districts.

| CCE Dispute Bracket | Sample Size | Avg CCE Completion (%) | Avg Contested Rate (%) | Claim Rejection Rate (%) |
| :--- | :---: | :---: | :---: | :---: |
| **Clean Verification (<5.0% Contested)** | 702 | 95.8% | 2.1% | 3.4% |
| **Moderate Dispute (5.0%–9.9% Contested)** | 184 | 94.2% | 7.2% | 5.8% |
| **High Dispute (≥10.0% Contested)** | 44 | 91.5% | 12.4% | 9.6% |

---

## 5. Empirical Analysis 3: Predictive & Prescriptive Actuarial Modeling
### Multi-Factor District Actuarial Risk Scoring & Tiering
Composite Actuarial Risk Index (CARI):
`CARI = (Mean Historical LCR × 0.45) + (Mean Yield Shortfall % × 0.30) + (Climate Vulnerability Index × 100 × 0.25)`

- **Tier 3: Severe Risk (CARI ≥ 70.0):** Barmer, Beed, Banda, Mahoba. *Prescription:* Mandate Beed Model (80:110), dual-trigger parametric weather indices, state catastrophic reinsurance reserve.
- **Tier 2: Moderate Risk (48.0 ≤ CARI < 70.0):** Ujjain, Latur, Haveri, Balangir. *Prescription:* Standard 50:50 subsidy, semi-automated satellite verification.
- **Tier 1: Low Risk (CARI < 48.0):** Hoshangabad, Aligarh, Bargarh. *Prescription:* Compress actuarial premium loading by 25–35%, reduce government subsidy liability, deploy algorithmic Straight-Through Processing (STP).

### Beed Model (80:110 Cup-and-Cap) Fiscal Simulation

| State Name | Cumulative Premium (₹ Cr) | Cumulative Claims (₹ Cr) | LCR (%) | Clawback Recovered (₹ Cr) | Excess Liability (₹ Cr) | Net Fiscal Gain (₹ Cr) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Rajasthan** | 3,962.18 | 1,945.88 | 49.11% | 1,426.29 | 28.39 | +1,397.90 |
| **Maharashtra** | 5,544.20 | 3,398.03 | 61.29% | 1,725.16 | 339.29 | +1,385.87 |
| **Karnataka** | 4,555.80 | 2,455.73 | 53.90% | 1,313.05 | 0.00 | +1,313.05 |
| **Madhya Pradesh** | 4,083.89 | 2,338.11 | 57.25% | 1,120.88 | 13.60 | +1,107.28 |
| **Uttar Pradesh** | 4,336.17 | 2,823.74 | 65.12% | 1,091.44 | 66.34 | +1,025.10 |
| **Odisha** | 3,426.38 | 1,966.90 | 57.40% | 967.40 | 42.84 | +924.56 |
| **National Total** | **25,908.62** | **14,928.39** | **57.62%** | **7,644.22** | **490.46** | **+7,153.76** |

---

## 6. Strategic Policy Recommendations & Implementation Roadmap
1. **National Escrow Account for State Subsidies:** Mandatory automated escrow mechanism via RBI Public Financial Management System (PFMS), auto-debiting state treasury shares at the commencement of each sowing season.
2. **Digital Crop Cut Verification via YES-TECH & WINDS:** Transition to Yield Estimation System based on Technology (YES-TECH) and Weather Information Network Data Systems (WINDS).
3. **Dynamic Premium Loading Compression for Irrigated Belts:** Separate high-risk rainfed clusters from low-risk canal-fed tracts in tender bidding.
4. **National Adoption of the 80:110 Model with Central Reinsurance:** Scale the Beed Model nationwide, backed by a National Agricultural Reinsurance Pool (NARP).

---

## 7. Technical Repository Architecture & Reproducibility Guide
- `sql/01_schema_ddl.sql`: DDL for star-schema dimension and fact tables.
- `sql/02_data_transformation_etl.sql`: View definitions, calculated KPI columns, and performance bands.
- `sql/03_descriptive_analysis.sql`: Baseline queries, seasonal divergence, and crop category distribution.
- `sql/04_diagnostic_analysis.sql`: Subsidy delay TAT decomposition, CCE dispute correlations, and Z-score outlier detection.
- `sql/05_predictive_prescriptive_modeling.sql`: Composite risk scoring formulas and Beed Model fiscal simulation.
- `excel/PMFBY_Actuarial_BI_Dashboard.xlsx`: 5-sheet interactive Excel BI workbook with KPI cards, dynamic formulas, and native charts.
- `data/pmfby_actuarial.db`: Relational SQLite database.

---

## 8. References & Official Source Documentation
- Ministry of Agriculture & Farmers Welfare, Government of India. [Pradhan Mantri Fasal Bima Yojana (PMFBY) Operational Guidelines](https://pmfby.gov.in/). New Delhi: MoA&FW, 2020.
- Comptroller and Auditor General of India (CAG). [Report on Performance Audit of Agriculture Crop Insurance Schemes](https://cag.gov.in/). Report No. 13 of 2017.
- Reserve Bank of India (RBI). [Report of the Internal Working Group to Review Agricultural Credit](https://rbi.org.in/). Mumbai: RBI, 2019.
- India Meteorological Department (IMD). [State-wise Rainfall Deviation & Drought Monitoring Bulletins (2019–2024)](https://mausam.imd.gov.in/). New Delhi: Ministry of Earth Sciences.
- General Insurance Council of India. [Yearbook of General Insurance Statistics: Crop Insurance Segment](https://www.gicouncil.in/). Mumbai: GIC, 2024.
