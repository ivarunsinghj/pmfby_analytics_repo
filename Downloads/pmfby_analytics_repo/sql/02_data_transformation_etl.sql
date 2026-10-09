-- ==============================================================================
-- 02_data_transformation_etl.sql
-- Project: PMFBY Actuarial & Settlement Analytics
-- Purpose: Analytical Views, Feature Engineering & Data Normalization
-- ==============================================================================

DROP VIEW IF EXISTS vw_pmfby_enriched_analytics;

CREATE VIEW vw_pmfby_enriched_analytics AS
SELECT 
    f.record_id,
    
    -- District & Geographic Attributes
    d.district_id,
    d.district_name,
    d.state_name,
    d.agro_climatic_zone,
    d.vulnerability_index,
    
    -- Crop Attributes
    c.crop_id,
    c.crop_name,
    c.category AS crop_category,
    c.standard_season,
    c.farmer_premium_rate_pct,
    
    -- Temporal Attributes
    s.season_id,
    s.year,
    s.season,
    s.climate_character,
    
    -- Insurer Attributes
    i.insurer_id,
    i.insurer_name,
    i.sector_type AS insurer_sector,
    
    -- Volume & Enrolment Metrics
    f.farmer_applications_loanee,
    f.farmer_applications_non_loanee,
    f.total_farmers_enrolled,
    f.small_marginal_farmers,
    ROUND(CAST(f.small_marginal_farmers AS FLOAT) / NULLIF(f.total_farmers_enrolled, 0) * 100.0, 2) AS smallholder_share_pct,
    ROUND(CAST(f.farmer_applications_non_loanee AS FLOAT) / NULLIF(f.total_farmers_enrolled, 0) * 100.0, 2) AS non_loanee_share_pct,
    f.insured_area_ha,
    f.sum_insured_inr_crores,
    ROUND(f.sum_insured_inr_crores * 1e7 / NULLIF(f.insured_area_ha, 0), 2) AS sum_insured_per_ha_inr,
    
    -- Financials & Subsidies
    f.actuarial_premium_rate_pct,
    f.farmer_premium_inr_crores,
    f.central_subsidy_inr_crores,
    f.state_subsidy_inr_crores,
    f.gross_premium_inr_crores,
    ROUND((f.central_subsidy_inr_crores + f.state_subsidy_inr_crores) / NULLIF(f.gross_premium_inr_crores, 0) * 100.0, 2) AS govt_subsidy_share_pct,
    
    -- Operational Turnaround & Subsidy Delay
    f.state_subsidy_status,
    f.state_subsidy_delay_days,
    f.claim_settlement_tat_days,
    CASE 
        WHEN f.claim_settlement_tat_days <= 60 THEN 'Fast Track (<=60 Days)'
        WHEN f.claim_settlement_tat_days <= 120 THEN 'Standard (61-120 Days)'
        WHEN f.claim_settlement_tat_days <= 180 THEN 'Delayed (121-180 Days)'
        ELSE 'Severe Latency (>180 Days)'
    END AS tat_category,
    
    -- Yield & Weather Telemetry
    f.rainfall_departure_pct,
    f.dry_spell_duration_days,
    f.threshold_yield_kg_ha,
    f.actual_yield_kg_ha,
    f.yield_shortfall_pct,
    f.planned_cces,
    f.conducted_cces,
    ROUND(CAST(f.conducted_cces AS FLOAT) / NULLIF(f.planned_cces, 0) * 100.0, 2) AS cce_execution_rate_pct,
    f.cce_discrepancy_rate_pct,
    
    -- Claims & Actuarial Performance
    f.claims_reported_inr_crores,
    f.claims_approved_inr_crores,
    f.claims_rejected_inr_crores,
    ROUND(f.claims_rejected_inr_crores / NULLIF(f.claims_reported_inr_crores, 0) * 100.0, 2) AS claim_rejection_rate_pct,
    f.claims_paid_inr_crores,
    f.loss_cost_ratio_pct,
    CASE 
        WHEN f.loss_cost_ratio_pct > 150.0 THEN 'Severe Underwriting Loss (>150%)'
        WHEN f.loss_cost_ratio_pct > 100.0 THEN 'Deficit (100%-150%)'
        WHEN f.loss_cost_ratio_pct >= 60.0 THEN 'Balanced Commercial (60%-100%)'
        ELSE 'Super-Normal Surplus (<60%)'
    END AS underwriting_performance_band,
    ROUND(f.gross_premium_inr_crores - f.claims_paid_inr_crores, 2) AS insurer_underwriting_margin_cr,
    f.non_loanee_loss_multiplier

FROM fact_pmfby_claims_enrolment f
JOIN dim_districts d ON f.district_id = d.district_id
JOIN dim_crops c ON f.crop_id = c.crop_id
JOIN dim_seasons s ON f.season_id = s.season_id
JOIN dim_insurers i ON f.insurer_id = i.insurer_id;
