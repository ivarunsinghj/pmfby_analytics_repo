-- ==============================================================================
-- 03_descriptive_analysis.sql
-- Project: PMFBY Actuarial & Settlement Analytics
-- Type of Analysis 1: Descriptive & Exploratory Data Analysis (EDA)
-- Focus: Multi-Year Macro Baseline, Seasonal Variations, Crop Breakdown, and
--        Farmer Participation Demographics (Loanee vs Non-Loanee)
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- Query 1.1: Macro National Baseline KPIs (Aggregated across 2019-2024)
-- ------------------------------------------------------------------------------
SELECT 
    COUNT(DISTINCT state_name) AS states_covered,
    COUNT(DISTINCT district_id) AS districts_covered,
    SUM(total_farmers_enrolled) AS total_farmer_applications,
    SUM(small_marginal_farmers) AS total_small_marginal_farmers,
    ROUND(SUM(insured_area_ha) / 1e6, 2) AS total_insured_area_million_ha,
    ROUND(SUM(sum_insured_inr_crores), 2) AS total_sum_insured_crores,
    ROUND(SUM(gross_premium_inr_crores), 2) AS total_gross_premium_crores,
    ROUND(SUM(farmer_premium_inr_crores), 2) AS total_farmer_share_crores,
    ROUND(SUM(central_subsidy_inr_crores + state_subsidy_inr_crores), 2) AS total_govt_subsidy_crores,
    ROUND(SUM(claims_paid_inr_crores), 2) AS total_claims_paid_crores,
    ROUND(SUM(claims_paid_inr_crores) / SUM(gross_premium_inr_crores) * 100.0, 2) AS macro_loss_cost_ratio_pct,
    ROUND(AVG(claim_settlement_tat_days), 1) AS avg_turnaround_time_days
FROM vw_pmfby_enriched_analytics;

-- ------------------------------------------------------------------------------
-- Query 1.2: Multi-Year State-Level Performance & Underwriting Margin Summary
-- ------------------------------------------------------------------------------
SELECT 
    state_name,
    COUNT(record_id) AS total_evaluations,
    SUM(total_farmers_enrolled) AS total_farmers,
    ROUND(SUM(sum_insured_inr_crores), 2) AS sum_insured_cr,
    ROUND(SUM(gross_premium_inr_crores), 2) AS gross_premium_cr,
    ROUND(SUM(claims_paid_inr_crores), 2) AS claims_paid_cr,
    ROUND(SUM(gross_premium_inr_crores) - SUM(claims_paid_inr_crores), 2) AS net_underwriting_balance_cr,
    ROUND(SUM(claims_paid_inr_crores) / SUM(gross_premium_inr_crores) * 100.0, 2) AS aggregate_lcr_pct,
    ROUND(AVG(claim_settlement_tat_days), 1) AS avg_tat_days,
    ROUND(AVG(vulnerability_index), 2) AS avg_vulnerability_score
FROM vw_pmfby_enriched_analytics
GROUP BY state_name
ORDER BY aggregate_lcr_pct DESC;

-- ------------------------------------------------------------------------------
-- Query 1.3: Seasonality Breakdown - Kharif (Monsoon) vs Rabi (Winter)
-- ------------------------------------------------------------------------------
SELECT 
    season,
    COUNT(record_id) AS crop_district_instances,
    SUM(total_farmers_enrolled) AS total_farmers,
    ROUND(SUM(insured_area_ha) / 1e6, 2) AS area_million_ha,
    ROUND(SUM(gross_premium_inr_crores), 2) AS gross_premium_cr,
    ROUND(SUM(claims_paid_inr_crores), 2) AS claims_paid_cr,
    ROUND(SUM(claims_paid_inr_crores) / SUM(gross_premium_inr_crores) * 100.0, 2) AS season_lcr_pct,
    ROUND(AVG(yield_shortfall_pct), 2) AS avg_yield_shortfall_pct,
    ROUND(AVG(claim_settlement_tat_days), 1) AS avg_settlement_tat_days
FROM vw_pmfby_enriched_analytics
GROUP BY season
ORDER BY season_lcr_pct DESC;

-- ------------------------------------------------------------------------------
-- Query 1.4: Crop Category Actuarial Distribution
-- ------------------------------------------------------------------------------
SELECT 
    crop_category,
    COUNT(DISTINCT crop_name) AS crop_types_count,
    ROUND(SUM(insured_area_ha), 2) AS insured_area_ha,
    ROUND(SUM(gross_premium_inr_crores), 2) AS gross_premium_cr,
    ROUND(SUM(farmer_premium_inr_crores), 2) AS farmer_premium_cr,
    ROUND(SUM(claims_paid_inr_crores), 2) AS claims_paid_cr,
    ROUND(SUM(claims_paid_inr_crores) / SUM(gross_premium_inr_crores) * 100.0, 2) AS category_lcr_pct,
    ROUND(AVG(actuarial_premium_rate_pct), 2) AS avg_actuarial_rate_pct,
    ROUND(AVG(farmer_premium_rate_pct), 2) AS avg_statutory_farmer_rate_pct
FROM vw_pmfby_enriched_analytics
GROUP BY crop_category
ORDER BY gross_premium_cr DESC;

-- ------------------------------------------------------------------------------
-- Query 1.5: Temporal Evolution of Non-Loanee Farmer Participation (Post-2020 Policy Shift)
-- ------------------------------------------------------------------------------
SELECT 
    year,
    season,
    SUM(farmer_applications_loanee) AS loanee_farmers,
    SUM(farmer_applications_non_loanee) AS non_loanee_farmers,
    ROUND(CAST(SUM(farmer_applications_non_loanee) AS FLOAT) / SUM(total_farmers_enrolled) * 100.0, 2) AS non_loanee_participation_share_pct,
    ROUND(AVG(non_loanee_loss_multiplier), 2) AS avg_non_loanee_loss_multiplier
FROM vw_pmfby_enriched_analytics
GROUP BY year, season
ORDER BY year, season;
