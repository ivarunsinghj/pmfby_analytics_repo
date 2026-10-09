-- ==============================================================================
-- 04_diagnostic_analysis.sql
-- Project: PMFBY Actuarial & Settlement Analytics
-- Type of Analysis 2: Diagnostic & Root-Cause / Spatial Basis Risk Analysis
-- Focus: Identifying Settlement Bottlenecks, CCE Discrepancies, Actuarial Outliers
--        (Z-Score Anomaly Detection), and Adverse Selection Patterns
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- Query 2.1: Root-Cause Decomposition of Claim Settlement Turnaround Time (TAT)
-- Investigating the impact of State Subsidy Disbursal Delays on DBT Latency
-- ------------------------------------------------------------------------------
SELECT 
    state_subsidy_status,
    COUNT(record_id) AS total_cases,
    ROUND(AVG(state_subsidy_delay_days), 1) AS avg_subsidy_delay_days,
    ROUND(AVG(claim_settlement_tat_days), 1) AS avg_claim_settlement_tat_days,
    MIN(claim_settlement_tat_days) AS min_tat_days,
    MAX(claim_settlement_tat_days) AS max_tat_days,
    ROUND(SUM(claims_approved_inr_crores), 2) AS approved_claims_cr,
    ROUND(SUM(claims_paid_inr_crores), 2) AS paid_claims_cr,
    ROUND((SUM(claims_approved_inr_crores) - SUM(claims_paid_inr_crores)), 2) AS pending_claims_disbursal_cr,
    ROUND(SUM(claims_paid_inr_crores) / NULLIF(SUM(claims_approved_inr_crores), 0) * 100.0, 2) AS disbursement_fulfillment_rate_pct
FROM vw_pmfby_enriched_analytics
GROUP BY state_subsidy_status
ORDER BY avg_claim_settlement_tat_days DESC;

-- ------------------------------------------------------------------------------
-- Query 2.2: CCE Discrepancy & Dispute Root Cause on Claim Rejection Rates
-- Assessing whether contested yield cut experiments drive farmer claim rejections
-- ------------------------------------------------------------------------------
SELECT 
    CASE 
        WHEN cce_discrepancy_rate_pct >= 10.0 THEN 'High CCE Dispute (>=10%)'
        WHEN cce_discrepancy_rate_pct >= 5.0 THEN 'Moderate CCE Dispute (5.0-9.9%)'
        ELSE 'Low/Clean CCE Verification (<5.0%)'
    END AS cce_dispute_bracket,
    COUNT(record_id) AS sample_size,
    ROUND(AVG(cce_execution_rate_pct), 2) AS avg_cce_completion_pct,
    ROUND(AVG(cce_discrepancy_rate_pct), 2) AS avg_cce_discrepancy_pct,
    ROUND(AVG(claim_rejection_rate_pct), 2) AS avg_claim_rejection_rate_pct,
    ROUND(SUM(claims_rejected_inr_crores), 2) AS total_rejected_claims_cr,
    ROUND(SUM(claims_reported_inr_crores), 2) AS total_reported_claims_cr
FROM vw_pmfby_enriched_analytics
GROUP BY 
    CASE 
        WHEN cce_discrepancy_rate_pct >= 10.0 THEN 'High CCE Dispute (>=10%)'
        WHEN cce_discrepancy_rate_pct >= 5.0 THEN 'Moderate CCE Dispute (5.0-9.9%)'
        ELSE 'Low/Clean CCE Verification (<5.0%)'
    END
ORDER BY avg_claim_rejection_rate_pct DESC;

-- ------------------------------------------------------------------------------
-- Query 2.3: Actuarial Outlier & Anomaly Detection (Z-Score by Agro-Climatic Zone)
-- Uses SQL Window Functions to compute Zone Mean & Standard Deviation of LCR,
-- and flags statistical outliers where Z-score exceeds +/- 2.0.
-- ------------------------------------------------------------------------------
WITH zone_stats AS (
    SELECT 
        record_id,
        district_name,
        state_name,
        agro_climatic_zone,
        crop_name,
        season_id,
        gross_premium_inr_crores,
        claims_paid_inr_crores,
        loss_cost_ratio_pct,
        yield_shortfall_pct,
        rainfall_departure_pct,
        AVG(loss_cost_ratio_pct) OVER(PARTITION BY agro_climatic_zone) AS zone_avg_lcr,
        -- Population standard deviation approximation in SQLite
        SQRT(AVG(loss_cost_ratio_pct * loss_cost_ratio_pct) OVER(PARTITION BY agro_climatic_zone) - 
             (AVG(loss_cost_ratio_pct) OVER(PARTITION BY agro_climatic_zone) * AVG(loss_cost_ratio_pct) OVER(PARTITION BY agro_climatic_zone))) AS zone_std_lcr
    FROM vw_pmfby_enriched_analytics
),
outlier_classification AS (
    SELECT 
        record_id,
        district_name,
        state_name,
        agro_climatic_zone,
        crop_name,
        season_id,
        gross_premium_inr_crores,
        claims_paid_inr_crores,
        loss_cost_ratio_pct,
        ROUND(zone_avg_lcr, 2) AS zone_mean_lcr,
        ROUND(zone_std_lcr, 2) AS zone_std_lcr,
        ROUND((loss_cost_ratio_pct - zone_avg_lcr) / NULLIF(zone_std_lcr, 0), 2) AS lcr_z_score,
        yield_shortfall_pct,
        rainfall_departure_pct
    FROM zone_stats
)
SELECT 
    record_id,
    district_name,
    state_name,
    crop_name,
    season_id,
    loss_cost_ratio_pct,
    zone_mean_lcr,
    lcr_z_score,
    CASE 
        WHEN lcr_z_score >= 2.0 THEN 'Extreme Deficit Outlier (Z >= 2.0)'
        WHEN lcr_z_score <= -1.5 THEN 'Super-Normal Retention Outlier (Z <= -1.5)'
        ELSE 'Normal Actuarial Variance'
    END AS outlier_diagnosis,
    yield_shortfall_pct,
    rainfall_departure_pct
FROM outlier_classification
WHERE ABS(lcr_z_score) >= 1.5
ORDER BY lcr_z_score DESC
LIMIT 20;

-- ------------------------------------------------------------------------------
-- Query 2.4: Adverse Selection Diagnostics in Voluntary Non-Loanee Farmers
-- Testing whether high vulnerability districts suffer disproportionately higher
-- non-loanee loss ratios compared to mandatory loanee baseline
-- ------------------------------------------------------------------------------
SELECT 
    CASE 
        WHEN vulnerability_index >= 0.80 THEN 'High Vulnerability (Score >= 0.80)'
        WHEN vulnerability_index >= 0.60 THEN 'Moderate Vulnerability (0.60-0.79)'
        ELSE 'Low Vulnerability (< 0.60)'
    END AS vulnerability_tier,
    COUNT(record_id) AS evaluations_count,
    ROUND(AVG(non_loanee_share_pct), 2) AS avg_non_loanee_share_pct,
    ROUND(AVG(non_loanee_loss_multiplier), 2) AS avg_non_loanee_loss_ratio_multiplier,
    ROUND(AVG(yield_shortfall_pct), 2) AS avg_yield_shortfall_pct,
    ROUND(AVG(loss_cost_ratio_pct), 2) AS aggregate_lcr_pct,
    ROUND(SUM(claims_paid_inr_crores) / SUM(gross_premium_inr_crores) * 100.0, 2) AS weighted_lcr_pct
FROM vw_pmfby_enriched_analytics
GROUP BY 
    CASE 
        WHEN vulnerability_index >= 0.80 THEN 'High Vulnerability (Score >= 0.80)'
        WHEN vulnerability_index >= 0.60 THEN 'Moderate Vulnerability (0.60-0.79)'
        ELSE 'Low Vulnerability (< 0.60)'
    END
ORDER BY avg_non_loanee_share_pct DESC;

-- ------------------------------------------------------------------------------
-- Query 2.5: District-Level Turnaround Latency Ranking (Top 10 Most Severely Delayed)
-- Utilizes Window NTILE and DENSE_RANK to identify acute bottleneck geographies
-- ------------------------------------------------------------------------------
SELECT 
    district_name,
    state_name,
    COUNT(record_id) AS recorded_seasons,
    ROUND(AVG(claim_settlement_tat_days), 1) AS avg_settlement_days,
    ROUND(AVG(state_subsidy_delay_days), 1) AS avg_subsidy_delay_days,
    ROUND(AVG(loss_cost_ratio_pct), 2) AS avg_lcr_pct,
    SUM(CASE WHEN state_subsidy_status = 'Delayed >6 Months' THEN 1 ELSE 0 END) AS acute_delay_count,
    DENSE_RANK() OVER (ORDER BY AVG(claim_settlement_tat_days) DESC) AS national_latency_rank
FROM vw_pmfby_enriched_analytics
GROUP BY district_name, state_name
ORDER BY avg_settlement_days DESC
LIMIT 10;
