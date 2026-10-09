-- ==============================================================================
-- 05_predictive_prescriptive_modeling.sql
-- Project: PMFBY Actuarial & Settlement Analytics
-- Type of Analysis 3: Predictive & Prescriptive / Actuarial Optimization Modeling
-- Focus: 1. District Actuarial Risk Scoring & Tiering
--        2. Beed Model (80:110 Cup-and-Cap) State Fiscal Liability Simulation
--        3. Prescriptive Queue Optimization for Automated Claim Clearance
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- Model 3.1: Multi-Factor Actuarial Risk Scoring & Dynamic Underwriting Tiering
-- Predicts future volatility and assigns dynamic risk pricing recommendations
-- ------------------------------------------------------------------------------
WITH district_risk_profiles AS (
    SELECT 
        district_id,
        district_name,
        state_name,
        agro_climatic_zone,
        vulnerability_index,
        COUNT(record_id) AS historical_seasons_observed,
        ROUND(AVG(loss_cost_ratio_pct), 2) AS mean_historical_lcr,
        ROUND(AVG(yield_shortfall_pct), 2) AS mean_yield_shortfall,
        ROUND(AVG(cce_discrepancy_rate_pct), 2) AS mean_cce_discrepancy,
        ROUND(SUM(gross_premium_inr_crores), 2) AS total_gross_premium_cr,
        ROUND(SUM(claims_paid_inr_crores), 2) AS total_claims_paid_cr
    FROM vw_pmfby_enriched_analytics
    GROUP BY district_id, district_name, state_name, agro_climatic_zone, vulnerability_index
),
composite_scoring AS (
    SELECT 
        district_id,
        district_name,
        state_name,
        agro_climatic_zone,
        mean_historical_lcr,
        mean_yield_shortfall,
        vulnerability_index,
        -- Weighted Risk Index formula (0 to 100)
        ROUND(
            (mean_historical_lcr * 0.45) + 
            (mean_yield_shortfall * 0.30) + 
            (vulnerability_index * 100 * 0.25), 
            2
        ) AS composite_actuarial_risk_score
    FROM district_risk_profiles
)
SELECT 
    district_id,
    district_name,
    state_name,
    agro_climatic_zone,
    mean_historical_lcr,
    mean_yield_shortfall,
    vulnerability_index,
    composite_actuarial_risk_score,
    CASE 
        WHEN composite_actuarial_risk_score >= 70.0 THEN 'Tier 3: Severe Risk (Reinsurance / High Reserve)'
        WHEN composite_actuarial_risk_score >= 48.0 THEN 'Tier 2: Moderate Risk (Standard Underwriting Pool)'
        ELSE 'Tier 1: Low Risk (Surplus Generating / Rate Concession)'
    END AS prescriptive_underwriting_tier,
    CASE 
        WHEN composite_actuarial_risk_score >= 70.0 THEN 'Mandate Beed Model (80:110) + Parametric Weather Triggers'
        WHEN composite_actuarial_risk_score >= 48.0 THEN 'Standard 50:50 Subsidy + Semi-Automated CCE Verification'
        ELSE 'Fast-Track Automated Settlement + Reduce State Subsidy Loading'
    END AS strategic_policy_prescription
FROM composite_scoring
ORDER BY composite_actuarial_risk_score DESC;

-- ------------------------------------------------------------------------------
-- Model 3.2: Beed Model (80:110 Cup-and-Cap) State Fiscal Liability Simulation
-- Simulates the financial balance if the Beed Model was applied across all states:
-- Rule 1: If LCR < 80%, Insurer refunds (80 - LCR)% of Gross Premium to State (Clawback).
-- Rule 2: If 80% <= LCR <= 110%, Insurer operates within commercial bounds (Zero Liability).
-- Rule 3: If LCR > 110%, State Government reimburses Insurer (LCR - 110)% of Gross Premium.
-- ------------------------------------------------------------------------------
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
    COUNT(*) AS seasons_evaluated,
    ROUND(SUM(total_gross_premium_cr), 2) AS cumulative_gross_premium_cr,
    ROUND(SUM(total_claims_paid_cr), 2) AS cumulative_claims_paid_cr,
    ROUND(SUM(total_claims_paid_cr) / SUM(total_gross_premium_cr) * 100.0, 2) AS cumulative_lcr_pct,
    ROUND(SUM(state_clawback_recovery_cr), 2) AS total_beed_clawback_recovered_cr,
    ROUND(SUM(state_excess_liability_cr), 2) AS total_state_excess_liability_incurred_cr,
    ROUND(SUM(state_clawback_recovery_cr) - SUM(state_excess_liability_cr), 2) AS net_state_budgetary_impact_cr,
    CASE 
        WHEN SUM(state_clawback_recovery_cr) - SUM(state_excess_liability_cr) > 0 
        THEN 'Net Fiscal Surplus (Favorable for State Adoption)'
        ELSE 'Net Fiscal Deficit (Requires Central Backstop Fund)'
    END AS beed_model_fiscal_verdict
FROM beed_simulation
GROUP BY state_name
ORDER BY net_state_budgetary_impact_cr DESC;

-- ------------------------------------------------------------------------------
-- Model 3.3: Prescriptive Claim Settlement Queue Optimization Engine
-- Classifies individual claim batches into execution pipelines to reduce TAT
-- ------------------------------------------------------------------------------
SELECT 
    record_id,
    district_name,
    state_name,
    crop_name,
    season_id,
    cce_discrepancy_rate_pct,
    yield_shortfall_pct,
    claim_settlement_tat_days,
    claims_approved_inr_crores,
    CASE 
        -- Pipeline A: Straight-Through Processing (Zero Dispute + High Verifiability)
        WHEN cce_discrepancy_rate_pct < 4.0 AND yield_shortfall_pct >= 10.0 
        THEN 'Pipeline A: Automated Direct DBT (SLA: <= 21 Days)'
        
        -- Pipeline B: Moderate Verification (Low yield shortfall or slight dispute)
        WHEN cce_discrepancy_rate_pct BETWEEN 4.0 AND 8.0 
        THEN 'Pipeline B: Remote Sensing Verification (SLA: <= 45 Days)'
        
        -- Pipeline C: High Dispute / Forensic Audit Required
        ELSE 'Pipeline C: Joint Committee Forensic Audit (SLA: <= 90 Days)'
    END AS prescriptive_execution_queue,
    CASE 
        WHEN cce_discrepancy_rate_pct < 4.0 AND yield_shortfall_pct >= 10.0 
        THEN 'Bypass manual insurer review; release 80% ad-hoc DBT upon CCE upload'
        WHEN cce_discrepancy_rate_pct BETWEEN 4.0 AND 8.0 
        THEN 'Cross-reference NDVI satellite vegetation index with crop cut data'
        ELSE 'Conduct physical inspection and tripartite district committee review'
    END AS operational_directive
FROM vw_pmfby_enriched_analytics
ORDER BY cce_discrepancy_rate_pct ASC, yield_shortfall_pct DESC
LIMIT 25;
