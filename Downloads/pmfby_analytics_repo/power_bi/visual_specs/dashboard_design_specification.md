# Power BI Dashboard Visual Design & Implementation Specification

## 🎨 Global Design Tokens & Theme Specification
- **Canvas Aspect Ratio**: 16:9 widescreen (1280 × 720 px)
- **Primary Color Palette**:
  - Primary Corporate Navy: `#1B365D`
  - Slate Accent / Secondary: `#2C5E8A`
  - Harvest Ochre / Highlight: `#D99B26`
  - Neutral Background Canvas: `#F8FAFC`
  - Card & Container Fill: `#FFFFFF`
  - Subtle Gridline / Border: `#E2E8F0`
- **Semantic Status Palette**:
  - Surplus / On-Time (`LCR < 80%`, `TAT ≤ 60d`): `#10B981` (Emerald)
  - Commercial Balanced (`80% ≤ LCR ≤ 110%`): `#3B82F6` (Blue)
  - Severe Deficit / Outlier (`LCR > 110%`, `TAT > 180d`): `#EF4444` (Ruby/Crimson)
- **Typography**:
  - Headings & KPI Figures: `Segoe UI Semibold` / `Segoe UI Bold`
  - Data Labels & Tables: `Segoe UI Regular`, 9pt–10pt

---

## 📑 Page-by-Page Visual Architecture

### Page 1: Executive Summary & Macro Portfolio Overview
**Objective**: High-level executive cockpit for MoA&FW leadership and State Agriculture Ministers.

| Visual Name | Visual Type | Data Fields (Axes / Values / Tooltips) | Formatting & Interaction Rules |
| :--- | :--- | :--- | :--- |
| **Top Filter Banner** | Slicer Bar | `dim_seasons[year]`, `dim_seasons[season]`, `dim_districts[state_name]` | Horizontal dropdown tiles, multi-select with search |
| **KPI Card 1** | Card / New KPI | `[Total Farmer Applications]` | Subtitle: "33.68M Applications across 36 Districts" |
| **KPI Card 2** | Card / New KPI | `[Total Gross Premium (₹ Cr)]` | Formatted as `₹#,##0.00 Cr`, Accent color `#1B365D` |
| **KPI Card 3** | Card / New KPI | `[Total Claims Paid (₹ Cr)]` | Subtitle: "Direct Benefit Transfer (DBT) Disbursed" |
| **KPI Card 4** | Card / New KPI | `[Macro Loss Cost Ratio (LCR) %]` | Target conditional color: Green if `<60%`, Red if `>100%` |
| **State Comparison Chart** | Clustered Column Chart | **X-Axis**: `dim_districts[state_name]`<br>**Y-Axis**: `[Total Gross Premium (₹ Cr)]`, `[Total Claims Paid (₹ Cr)]` | Data labels on; custom tooltips showing LCR % and Avg TAT |
| **State Underwriting Matrix** | Matrix Table | **Rows**: `state_name` > `district_name`<br>**Values**: Premium, Claims, LCR %, Avg TAT, Net Margin | In-cell data bars for LCR %, conditional heatmap on TAT |

---

### Page 2: Descriptive Analysis — Seasonal & Crop Category Distribution
**Objective**: Uncover spatial and seasonal asymmetries between monsoon-dependent rainfed crops and irrigated winter crops.

| Visual Name | Visual Type | Data Fields | Formatting & Interaction Rules |
| :--- | :--- | :--- | :--- |
| **Seasonality Comparison** | 100% Stacked Bar | **Y-Axis**: `season` (Kharif vs Rabi)<br>**X-Axis**: Premium share & Claim share | Clear two-tone contrast showing Kharif's 68.7% claim dominance |
| **Crop Category Risk Matrix** | Matrix / Treemap | **Category**: `dim_crops[category]` > `crop_name`<br>**Values**: `[Total Gross Premium]`, `[Actuarial Rate %]`, `[LCR %]` | Highlights Commercial Cotton (16.5% APR) vs Foodgrains |
| **Non-Loanee Transition Trend**| Area Chart | **X-Axis**: `year` + `season`<br>**Y-Axis**: `[Loanee Applications]`, `[Non-Loanee Applications]` | Reference line at Kharif 2020 (Policy shift making non-loanee voluntary) |
| **Yield Shortfall vs Claims** | Scatter Chart | **X-Axis**: `[Weighted Yield Shortfall %]`<br>**Y-Axis**: `[Claims Paid (₹ Cr)]`<br>**Size**: `[Insured Area Ha]` | Bubble size indicates district acreage footprint |

---

### Page 3: Diagnostic Deep Dive — Settlement Bottlenecks & Spatial Basis Risk
**Objective**: Root-cause diagnostic dashboard isolating operational delays and contested crop cutting data.

| Visual Name | Visual Type | Data Fields | Formatting & Interaction Rules |
| :--- | :--- | :--- | :--- |
| **Subsidy Delay vs Settlement TAT**| Clustered Bar Chart | **Y-Axis**: `state_subsidy_status`<br>**X-Axis**: `[Average Settlement TAT (Days)]`, `[Average State Subsidy Delay (Days)]` | Proves 4x latency spike when state subsidies are deferred |
| **CCE Dispute Friction Matrix**| Funnel / Column | **Categories**: Clean (<5%), Moderate (5-9.9%), High (≥10%)<br>**Values**: `[Claim Rejection Rate %]`, `[Total Claims Rejected (₹ Cr)]` | Demonstrates rejection jump from 3.4% to 9.6% under disputes |
| **Agro-Climatic Anomaly Table**| Table with Alerts | `district_name`, `agro_climatic_zone`, `[District LCR Z-Score]`, `[Underwriting Anomaly Status]` | Filtered for $|Z| \ge 1.5$. Red icon for severe deficit, green for surplus |
| **Fulfillment Funnel** | Gauge / KPI Ribbon | Approved Claims vs Paid Claims by State | Visualizes ₹490+ Cr held in administrative escrow |

---

### Page 4: Prescriptive Modeling — 80:110 Beed Model Fiscal Simulation
**Objective**: Interactive policy decision tool for state finance secretaries to evaluate alternative risk-pooling architectures.

| Visual Name | Visual Type | Data Fields | Formatting & Interaction Rules |
| :--- | :--- | :--- | :--- |
| **What-If Parameter Sliders** | Numeric Range Slicers | `Cup Threshold %` (60% to 90%, step 5%)<br>`Cap Threshold %` (100% to 130%, step 5%) | Live DAX recalculation across all visuals |
| **State Fiscal Balance Waterfall**| Waterfall Chart | **Category**: `state_name`<br>**Values**: `[Beed Net State Fiscal Impact (₹ Cr)]` | Shows cumulative ₹7,153.76 Cr net surplus across states |
| **District Actuarial Tiering Map**| Shape Map / Scatter | **Legend**: `[Actuarial Risk Tier]` (Tier 1, Tier 2, Tier 3)<br>**Values**: `[Composite Actuarial Risk Index (CARI)]` | Red/Amber/Green classification for automated policy assignment |
| **DBT Queue Triage Funnel** | Donut / Funnel Chart | **Category**: Prescriptive Queue (Pipeline A STP, Pipeline B Satellite, Pipeline C Forensic) | Quantifies claims eligible for 21-day fast-track settlement |
