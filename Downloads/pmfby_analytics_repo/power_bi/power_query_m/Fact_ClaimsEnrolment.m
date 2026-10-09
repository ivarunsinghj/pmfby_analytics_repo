// ==============================================================================
// Fact_ClaimsEnrolment.m
// Power Query (M) Script for ingesting and transforming PMFBY Fact Table
// Source: SQL Server / PostgreSQL / SQLite / Local CSV
// ==============================================================================

let
    // Source definition: In Power BI Desktop, connect to SQL or CSV
    // Example for SQL: Sql.Database("localhost", "pmfby_warehouse", [Query="SELECT * FROM fact_pmfby_claims_enrolment"])
    Source = Csv.Document(File.Contents("data/pmfby_district_level_master.csv"), [Delimiter=",", Columns=31, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{
        {"record_id", type text},
        {"district_id", type text},
        {"crop_id", type text},
        {"season_id", type text},
        {"insurer_id", type text},
        {"farmer_applications_loanee", Int64.Type},
        {"farmer_applications_non_loanee", Int64.Type},
        {"total_farmers_enrolled", Int64.Type},
        {"small_marginal_farmers", Int64.Type},
        {"insured_area_ha", type number},
        {"sum_insured_inr_crores", type number},
        {"actuarial_premium_rate_pct", type number},
        {"farmer_premium_rate_pct", type number},
        {"farmer_premium_inr_crores", type number},
        {"central_subsidy_inr_crores", type number},
        {"state_subsidy_inr_crores", type number},
        {"gross_premium_inr_crores", type number},
        {"state_subsidy_status", type text},
        {"state_subsidy_delay_days", Int64.Type},
        {"rainfall_departure_pct", type number},
        {"dry_spell_duration_days", Int64.Type},
        {"threshold_yield_kg_ha", type number},
        {"actual_yield_kg_ha", type number},
        {"yield_shortfall_pct", type number},
        {"planned_cces", Int64.Type},
        {"conducted_cces", Int64.Type},
        {"cce_discrepancy_rate_pct", type number},
        {"claims_reported_inr_crores", type number},
        {"claims_approved_inr_crores", type number},
        {"claims_rejected_inr_crores", type number},
        {"claims_paid_inr_crores", type number},
        {"claim_settlement_tat_days", Int64.Type},
        {"loss_cost_ratio_pct", type number},
        {"non_loanee_loss_multiplier", type number}
    }),
    
    // Add Derived Operational Buckets
    #"Added TAT Category" = Table.AddColumn(#"Changed Type", "TAT_Category", each 
        if [claim_settlement_tat_days] <= 60 then "Fast Track (<=60 Days)"
        else if [claim_settlement_tat_days] <= 120 then "Standard (61-120 Days)"
        else if [claim_settlement_tat_days] <= 180 then "Delayed (121-180 Days)"
        else "Severe Latency (>180 Days)", type text
    ),
    
    #"Added LCR Performance Band" = Table.AddColumn(#"Added TAT Category", "Underwriting_Performance_Band", each 
        if [loss_cost_ratio_pct] > 150.0 then "Severe Underwriting Loss (>150%)"
        else if [loss_cost_ratio_pct] > 100.0 then "Deficit (100%-150%)"
        else if [loss_cost_ratio_pct] >= 60.0 then "Balanced Commercial (60%-100%)"
        else "Super-Normal Surplus (<60%)", type text
    )
in
    #"Added LCR Performance Band"
