import os
import shutil
import sqlite3
import pandas as pd

REPO_DIR = "/working_dir/c_da497d1189927669/pmfby_analytics_repo"
SQL_DIR = os.path.join(REPO_DIR, "sql")
DATA_DIR = os.path.join(REPO_DIR, "data")
TMP_DB = "/tmp/pmfby_actuarial.db"
FINAL_DB = os.path.join(DATA_DIR, "pmfby_actuarial.db")

print("--- Running SQL Analytics Pipeline ---")

# Connect to tmp database
conn = sqlite3.connect(TMP_DB)

# Execute 01_schema_ddl.sql
with open(os.path.join(SQL_DIR, "01_schema_ddl.sql"), "r") as f:
    ddl_sql = f.read()
conn.executescript(ddl_sql)
print("-> 01_schema_ddl.sql executed successfully.")

# Execute 02_data_transformation_etl.sql
with open(os.path.join(SQL_DIR, "02_data_transformation_etl.sql"), "r") as f:
    etl_sql = f.read()
conn.executescript(etl_sql)
print("-> 02_data_transformation_etl.sql executed successfully.")

# Test executing queries from 03, 04, 05
print("\n[Executing Analysis 1: Descriptive & Exploratory Analysis]")
df_macro = pd.read_sql_query("""
SELECT 
    COUNT(DISTINCT state_name) AS states_covered,
    COUNT(DISTINCT district_id) AS districts_covered,
    SUM(total_farmers_enrolled) AS total_farmer_applications,
    ROUND(SUM(gross_premium_inr_crores), 2) AS total_gross_premium_cr,
    ROUND(SUM(claims_paid_inr_crores), 2) AS total_claims_paid_cr,
    ROUND(SUM(claims_paid_inr_crores) / SUM(gross_premium_inr_crores) * 100.0, 2) AS macro_lcr_pct,
    ROUND(AVG(claim_settlement_tat_days), 1) AS avg_tat_days
FROM vw_pmfby_enriched_analytics;
""", conn)
print(df_macro.to_string(index=False))

print("\n[Executing Analysis 2: Diagnostic Analysis - Subsidy Delay Root Cause]")
df_diag = pd.read_sql_query("""
SELECT 
    state_subsidy_status,
    COUNT(record_id) AS total_cases,
    ROUND(AVG(state_subsidy_delay_days), 1) AS avg_subsidy_delay_days,
    ROUND(AVG(claim_settlement_tat_days), 1) AS avg_tat_days,
    ROUND(SUM(claims_paid_inr_crores) / NULLIF(SUM(claims_approved_inr_crores), 0) * 100.0, 2) AS fulfillment_rate_pct
FROM vw_pmfby_enriched_analytics
GROUP BY state_subsidy_status
ORDER BY avg_tat_days DESC;
""", conn)
print(df_diag.to_string(index=False))

print("\n[Executing Analysis 3: Prescriptive Analysis - Beed Model 80:110 Fiscal Simulation]")
df_beed = pd.read_sql_query("""
WITH state_season_financials AS (
    SELECT 
        state_name,
        year,
        season,
        ROUND(SUM(gross_premium_inr_crores), 2) AS total_gross_premium_cr,
        ROUND(SUM(claims_paid_inr_crores), 2) AS total_claims_paid_cr,
        ROUND(SUM(claims_paid_inr_crores) / SUM(gross_premium_inr_crores) * 100.0, 2) AS state_season_lcr_pct
    FROM vw_pmfby_enriched_analytics
    GROUP BY state_name, year, season
),
beed_simulation AS (
    SELECT 
        state_name,
        year,
        season,
        total_gross_premium_cr,
        total_claims_paid_cr,
        state_season_lcr_pct,
        CASE 
            WHEN state_season_lcr_pct < 80.0 THEN 
                ROUND(total_gross_premium_cr * ((80.0 - state_season_lcr_pct) / 100.0), 2)
            ELSE 0.0
        END AS state_clawback_recovery_cr,
        CASE 
            WHEN state_season_lcr_pct > 110.0 THEN 
                ROUND(total_gross_premium_cr * ((state_season_lcr_pct - 110.0) / 100.0), 2)
            ELSE 0.0
        END AS state_excess_liability_cr
    FROM state_season_financials
)
SELECT 
    state_name,
    ROUND(SUM(total_gross_premium_cr), 2) AS gross_premium_cr,
    ROUND(SUM(total_claims_paid_cr), 2) AS claims_paid_cr,
    ROUND(SUM(total_claims_paid_cr) / SUM(total_gross_premium_cr) * 100.0, 2) AS lcr_pct,
    ROUND(SUM(state_clawback_recovery_cr), 2) AS clawback_recovered_cr,
    ROUND(SUM(state_excess_liability_cr), 2) AS excess_liability_cr,
    ROUND(SUM(state_clawback_recovery_cr) - SUM(state_excess_liability_cr), 2) AS net_fiscal_impact_cr
FROM beed_simulation
GROUP BY state_name
ORDER BY net_fiscal_impact_cr DESC;
""", conn)
print(df_beed.to_string(index=False))

conn.commit()
conn.close()

# Update final database in data/
shutil.copy2(TMP_DB, FINAL_DB)
print(f"\nAll SQL scripts executed and synced to {FINAL_DB}!")
