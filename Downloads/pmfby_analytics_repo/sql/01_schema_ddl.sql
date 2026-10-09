-- ==============================================================================
-- 01_schema_ddl.sql
-- Project: Pradhan Mantri Fasal Bima Yojana (PMFBY) Actuarial & Settlement Analytics
-- Architecture: Relational Star Schema (OLAP / BI Ready)
-- Target RDBMS: SQLite / PostgreSQL / MySQL compliant
-- ==============================================================================

-- 1. Dimension Tables

CREATE TABLE IF NOT EXISTS dim_districts (
    district_id VARCHAR(10) PRIMARY KEY,
    district_name VARCHAR(100) NOT NULL,
    state_name VARCHAR(100) NOT NULL,
    agro_climatic_zone VARCHAR(150) NOT NULL,
    vulnerability_index DECIMAL(4, 2) NOT NULL -- Climate/Drought Vulnerability Score (0.00 to 1.00)
);

CREATE TABLE IF NOT EXISTS dim_crops (
    crop_id VARCHAR(10) PRIMARY KEY,
    crop_name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,              -- Foodgrains, Pulses, Oilseeds, Commercial
    standard_season VARCHAR(20) NOT NULL,       -- Kharif, Rabi
    farmer_premium_rate_pct DECIMAL(4, 2) NOT NULL, -- Statutory subsidized rate (1.5%, 2.0%, 5.0%)
    base_sum_insured_ha DECIMAL(10, 2) NOT NULL -- Normal scale of finance per hectare (INR)
);

CREATE TABLE IF NOT EXISTS dim_seasons (
    season_id VARCHAR(10) PRIMARY KEY,
    year INT NOT NULL,
    season VARCHAR(20) NOT NULL,                -- Kharif, Rabi
    climate_character VARCHAR(200) NOT NULL     -- Notable climatological events / shocks
);

CREATE TABLE IF NOT EXISTS dim_insurers (
    insurer_id VARCHAR(10) PRIMARY KEY,
    insurer_name VARCHAR(150) NOT NULL,
    sector_type VARCHAR(50) NOT NULL            -- Public Sector, Private Sector
);

-- 2. Fact Table

CREATE TABLE IF NOT EXISTS fact_pmfby_claims_enrolment (
    record_id VARCHAR(20) PRIMARY KEY,
    district_id VARCHAR(10) NOT NULL,
    crop_id VARCHAR(10) NOT NULL,
    season_id VARCHAR(10) NOT NULL,
    insurer_id VARCHAR(10) NOT NULL,
    
    -- Farmer Participation Telemetry
    farmer_applications_loanee INT NOT NULL,
    farmer_applications_non_loanee INT NOT NULL,
    total_farmers_enrolled INT NOT NULL,
    small_marginal_farmers INT NOT NULL,
    insured_area_ha DECIMAL(12, 2) NOT NULL,
    sum_insured_inr_crores DECIMAL(12, 2) NOT NULL,
    
    -- Premium Actuarial Structure
    actuarial_premium_rate_pct DECIMAL(5, 2) NOT NULL,
    farmer_premium_rate_pct DECIMAL(4, 2) NOT NULL,
    farmer_premium_inr_crores DECIMAL(12, 2) NOT NULL,
    central_subsidy_inr_crores DECIMAL(12, 2) NOT NULL,
    state_subsidy_inr_crores DECIMAL(12, 2) NOT NULL,
    gross_premium_inr_crores DECIMAL(12, 2) NOT NULL,
    
    -- Administrative Operational Flags
    state_subsidy_status VARCHAR(50) NOT NULL,  -- Settled on Time, Delayed 3-6 Months, Delayed >6 Months
    state_subsidy_delay_days INT NOT NULL,
    
    -- Weather & Crop Cut Experiment (CCE) Yield Telemetry
    rainfall_departure_pct DECIMAL(5, 1) NOT NULL,
    dry_spell_duration_days INT NOT NULL,
    threshold_yield_kg_ha DECIMAL(8, 1) NOT NULL,
    actual_yield_kg_ha DECIMAL(8, 1) NOT NULL,
    yield_shortfall_pct DECIMAL(5, 2) NOT NULL,
    planned_cces INT NOT NULL,
    conducted_cces INT NOT NULL,
    cce_discrepancy_rate_pct DECIMAL(5, 2) NOT NULL,
    
    -- Claims Adjudication & Payout
    claims_reported_inr_crores DECIMAL(12, 2) NOT NULL,
    claims_approved_inr_crores DECIMAL(12, 2) NOT NULL,
    claims_rejected_inr_crores DECIMAL(12, 2) NOT NULL,
    claims_paid_inr_crores DECIMAL(12, 2) NOT NULL,
    claim_settlement_tat_days INT NOT NULL,     -- Harvest to Direct Benefit Transfer (DBT)
    loss_cost_ratio_pct DECIMAL(6, 2) NOT NULL, -- Claims Paid / Gross Premium * 100
    non_loanee_loss_multiplier DECIMAL(4, 2) NOT NULL,
    
    FOREIGN KEY (district_id) REFERENCES dim_districts (district_id),
    FOREIGN KEY (crop_id) REFERENCES dim_crops (crop_id),
    FOREIGN KEY (season_id) REFERENCES dim_seasons (season_id),
    FOREIGN KEY (insurer_id) REFERENCES dim_insurers (insurer_id)
);

-- 3. Optimization Indexes for Analytical Workloads

CREATE INDEX IF NOT EXISTS idx_fact_district ON fact_pmfby_claims_enrolment (district_id);
CREATE INDEX IF NOT EXISTS idx_fact_season ON fact_pmfby_claims_enrolment (season_id);
CREATE INDEX IF NOT EXISTS idx_fact_crop ON fact_pmfby_claims_enrolment (crop_id);
CREATE INDEX IF NOT EXISTS idx_fact_insurer ON fact_pmfby_claims_enrolment (insurer_id);
CREATE INDEX IF NOT EXISTS idx_fact_lcr ON fact_pmfby_claims_enrolment (loss_cost_ratio_pct);
CREATE INDEX IF NOT EXISTS idx_fact_tat ON fact_pmfby_claims_enrolment (claim_settlement_tat_days);
