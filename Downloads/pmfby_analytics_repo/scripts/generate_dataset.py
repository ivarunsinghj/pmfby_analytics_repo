import os
import random
import sqlite3
import numpy as np
import pandas as pd

# Set fixed random seed for reproducible research
np.random.seed(42)
random.seed(42)

REPO_DIR = "/working_dir/c_da497d1189927669/pmfby_analytics_repo"
DATA_DIR = os.path.join(REPO_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

# 1. Dimension Data Definitions
districts_data = [
    # Maharashtra (Western/Central - Dry/Semi-Arid)
    {"district_id": "MH01", "district_name": "Beed", "state_name": "Maharashtra", "agro_climatic_zone": "Western Plateau & Hills", "vulnerability_index": 0.88},
    {"district_id": "MH02", "district_name": "Jalna", "state_name": "Maharashtra", "agro_climatic_zone": "Western Plateau & Hills", "vulnerability_index": 0.82},
    {"district_id": "MH03", "district_name": "Latur", "state_name": "Maharashtra", "agro_climatic_zone": "Western Plateau & Hills", "vulnerability_index": 0.79},
    {"district_id": "MH04", "district_name": "Yavatmal", "state_name": "Maharashtra", "agro_climatic_zone": "Central Plateau & Hills", "vulnerability_index": 0.85},
    {"district_id": "MH05", "district_name": "Solapur", "state_name": "Maharashtra", "agro_climatic_zone": "Western Plateau & Hills", "vulnerability_index": 0.84},
    {"district_id": "MH06", "district_name": "Ahmednagar", "state_name": "Maharashtra", "agro_climatic_zone": "Western Plateau & Hills", "vulnerability_index": 0.75},

    # Madhya Pradesh (Central Heartland)
    {"district_id": "MP01", "district_name": "Ujjain", "state_name": "Madhya Pradesh", "agro_climatic_zone": "Central Plateau & Hills", "vulnerability_index": 0.65},
    {"district_id": "MP02", "district_name": "Sehore", "state_name": "Madhya Pradesh", "agro_climatic_zone": "Central Plateau & Hills", "vulnerability_index": 0.62},
    {"district_id": "MP03", "district_name": "Hoshangabad", "state_name": "Madhya Pradesh", "agro_climatic_zone": "Central Plateau & Hills", "vulnerability_index": 0.45},
    {"district_id": "MP04", "district_name": "Vidisha", "state_name": "Madhya Pradesh", "agro_climatic_zone": "Central Plateau & Hills", "vulnerability_index": 0.68},
    {"district_id": "MP05", "district_name": "Sagar", "state_name": "Madhya Pradesh", "agro_climatic_zone": "Central Plateau & Hills", "vulnerability_index": 0.70},
    {"district_id": "MP06", "district_name": "Dewas", "state_name": "Madhya Pradesh", "agro_climatic_zone": "Central Plateau & Hills", "vulnerability_index": 0.66},

    # Rajasthan (Arid & Semi-Arid West)
    {"district_id": "RJ01", "district_name": "Hanumangarh", "state_name": "Rajasthan", "agro_climatic_zone": "Trans-Gangetic Plains", "vulnerability_index": 0.48},
    {"district_id": "RJ02", "district_name": "Barmer", "state_name": "Rajasthan", "agro_climatic_zone": "Western Dry Region", "vulnerability_index": 0.94},
    {"district_id": "RJ03", "district_name": "Jodhpur", "state_name": "Rajasthan", "agro_climatic_zone": "Western Dry Region", "vulnerability_index": 0.89},
    {"district_id": "RJ04", "district_name": "Kota", "state_name": "Rajasthan", "agro_climatic_zone": "Central Plateau & Hills", "vulnerability_index": 0.52},
    {"district_id": "RJ05", "district_name": "Nagaur", "state_name": "Rajasthan", "agro_climatic_zone": "Western Dry Region", "vulnerability_index": 0.86},
    {"district_id": "RJ06", "district_name": "Alwar", "state_name": "Rajasthan", "agro_climatic_zone": "Trans-Gangetic Plains", "vulnerability_index": 0.58},

    # Uttar Pradesh (Bundelkhand & Gangetic)
    {"district_id": "UP01", "district_name": "Banda", "state_name": "Uttar Pradesh", "agro_climatic_zone": "Central Plateau & Hills (Bundelkhand)", "vulnerability_index": 0.91},
    {"district_id": "UP02", "district_name": "Mahoba", "state_name": "Uttar Pradesh", "agro_climatic_zone": "Central Plateau & Hills (Bundelkhand)", "vulnerability_index": 0.92},
    {"district_id": "UP03", "district_name": "Jhansi", "state_name": "Uttar Pradesh", "agro_climatic_zone": "Central Plateau & Hills (Bundelkhand)", "vulnerability_index": 0.87},
    {"district_id": "UP04", "district_name": "Aligarh", "state_name": "Uttar Pradesh", "agro_climatic_zone": "Upper Gangetic Plains", "vulnerability_index": 0.42},
    {"district_id": "UP05", "district_name": "Barabanki", "state_name": "Uttar Pradesh", "agro_climatic_zone": "Middle Gangetic Plains", "vulnerability_index": 0.50},
    {"district_id": "UP06", "district_name": "Mirzapur", "state_name": "Uttar Pradesh", "agro_climatic_zone": "Middle Gangetic Plains", "vulnerability_index": 0.74},

    # Odisha (East Coast & KBK Region)
    {"district_id": "OD01", "district_name": "Kalahandi", "state_name": "Odisha", "agro_climatic_zone": "Eastern Plateau & Hills", "vulnerability_index": 0.83},
    {"district_id": "OD02", "district_name": "Balangir", "state_name": "Odisha", "agro_climatic_zone": "Eastern Plateau & Hills", "vulnerability_index": 0.85},
    {"district_id": "OD03", "district_name": "Bargarh", "state_name": "Odisha", "agro_climatic_zone": "Eastern Plateau & Hills", "vulnerability_index": 0.55},
    {"district_id": "OD04", "district_name": "Cuttack", "state_name": "Odisha", "agro_climatic_zone": "East Coast Plains & Hills", "vulnerability_index": 0.60},
    {"district_id": "OD05", "district_name": "Puri", "state_name": "Odisha", "agro_climatic_zone": "East Coast Plains & Hills", "vulnerability_index": 0.78},
    {"district_id": "OD06", "district_name": "Koraput", "state_name": "Odisha", "agro_climatic_zone": "Eastern Plateau & Hills", "vulnerability_index": 0.72},

    # Karnataka (Southern Dry Zone)
    {"district_id": "KA01", "district_name": "Kalaburagi", "state_name": "Karnataka", "agro_climatic_zone": "Southern Plateau & Hills", "vulnerability_index": 0.86},
    {"district_id": "KA02", "district_name": "Vijayapura", "state_name": "Karnataka", "agro_climatic_zone": "Southern Plateau & Hills", "vulnerability_index": 0.84},
    {"district_id": "KA03", "district_name": "Belagavi", "state_name": "Karnataka", "agro_climatic_zone": "Southern Plateau & Hills", "vulnerability_index": 0.54},
    {"district_id": "KA04", "district_name": "Haveri", "state_name": "Karnataka", "agro_climatic_zone": "Southern Plateau & Hills", "vulnerability_index": 0.62},
    {"district_id": "KA05", "district_name": "Dharwad", "state_name": "Karnataka", "agro_climatic_zone": "Southern Plateau & Hills", "vulnerability_index": 0.59},
    {"district_id": "KA06", "district_name": "Tumakuru", "state_name": "Karnataka", "agro_climatic_zone": "Southern Plateau & Hills", "vulnerability_index": 0.76},
]
df_districts = pd.DataFrame(districts_data)

crops_data = [
    {"crop_id": "CR01", "crop_name": "Soybean", "category": "Oilseeds", "standard_season": "Kharif", "farmer_premium_rate_pct": 2.0, "base_sum_insured_ha": 42000},
    {"crop_id": "CR02", "crop_name": "Paddy", "category": "Foodgrains (Cereals)", "standard_season": "Kharif", "farmer_premium_rate_pct": 2.0, "base_sum_insured_ha": 55000},
    {"crop_id": "CR03", "crop_name": "Cotton", "category": "Commercial Crops", "standard_season": "Kharif", "farmer_premium_rate_pct": 5.0, "base_sum_insured_ha": 62000},
    {"crop_id": "CR04", "crop_name": "Bajra (Pearl Millet)", "category": "Coarse Cereals", "standard_season": "Kharif", "farmer_premium_rate_pct": 2.0, "base_sum_insured_ha": 28000},
    {"crop_id": "CR05", "crop_name": "Tur (Arhar)", "category": "Pulses", "standard_season": "Kharif", "farmer_premium_rate_pct": 2.0, "base_sum_insured_ha": 38000},
    {"crop_id": "CR06", "crop_name": "Wheat", "category": "Foodgrains (Cereals)", "standard_season": "Rabi", "farmer_premium_rate_pct": 1.5, "base_sum_insured_ha": 58000},
    {"crop_id": "CR07", "crop_name": "Mustard", "category": "Oilseeds", "standard_season": "Rabi", "farmer_premium_rate_pct": 1.5, "base_sum_insured_ha": 36000},
    {"crop_id": "CR08", "crop_name": "Gram (Chickpea)", "category": "Pulses", "standard_season": "Rabi", "farmer_premium_rate_pct": 1.5, "base_sum_insured_ha": 40000},
    {"crop_id": "CR09", "crop_name": "Rabi Jowar (Sorghum)", "category": "Coarse Cereals", "standard_season": "Rabi", "farmer_premium_rate_pct": 1.5, "base_sum_insured_ha": 31000},
    {"crop_id": "CR10", "crop_name": "Groundnut", "category": "Oilseeds", "standard_season": "Kharif", "farmer_premium_rate_pct": 2.0, "base_sum_insured_ha": 45000},
]
df_crops = pd.DataFrame(crops_data)

seasons_data = [
    {"season_id": "2019_K", "year": 2019, "season": "Kharif", "climate_character": "Heavy Monsoon Withdrawal / Localized Floods"},
    {"season_id": "2019_R", "year": 2020, "season": "Rabi", "climate_character": "Normal Winter / Moderate Hail in Central India"},
    {"season_id": "2020_K", "year": 2020, "season": "Kharif", "climate_character": "COVID-19 Disruption / Surplus Monsoon"},
    {"season_id": "2020_R", "year": 2021, "season": "Rabi", "climate_character": "Bumper Harvest / Favorable Temperatures"},
    {"season_id": "2021_K", "year": 2021, "season": "Kharif", "climate_character": "Extended Dry Spells in West / Late Surges"},
    {"season_id": "2021_R", "year": 2022, "season": "Rabi", "climate_character": "Severe March Heatwave (Terminal Heat Shock)"},
    {"season_id": "2022_K", "year": 2022, "season": "Kharif", "climate_character": "Uneven Spatial Rainfall / Eastern Deficit"},
    {"season_id": "2022_R", "year": 2023, "season": "Rabi", "climate_character": "Unseasonal March Rains & Hailstorm"},
    {"season_id": "2023_K", "year": 2023, "season": "Kharif", "climate_character": "Severe El Niño Dry August / Western Drought"},
    {"season_id": "2023_R", "year": 2024, "season": "Rabi", "climate_character": "Warm Winter / Variable Pulse Yields"},
]
df_seasons = pd.DataFrame(seasons_data)

insurers_data = [
    {"insurer_id": "INS01", "insurer_name": "Agriculture Insurance Company of India (AIC)", "sector_type": "Public Sector Undertaking"},
    {"insurer_id": "INS02", "insurer_name": "HDFC ERGO General Insurance", "sector_type": "Private Sector"},
    {"insurer_id": "INS03", "insurer_name": "Bajaj Allianz General Insurance", "sector_type": "Private Sector"},
    {"insurer_id": "INS04", "insurer_name": "ICICI Lombard General Insurance", "sector_type": "Private Sector"},
    {"insurer_id": "INS05", "insurer_name": "SBI General Insurance", "sector_type": "Private Sector (Bank-Promoted)"},
    {"insurer_id": "INS06", "insurer_name": "Reliance General Insurance", "sector_type": "Private Sector"},
]
df_insurers = pd.DataFrame(insurers_data)

# Generate Fact Table records
fact_records = []
record_counter = 1

# District - State tender mapping for insurance companies
# In PMFBY, insurers win clusters of districts via competitive tender for 3 years
state_insurer_map = {
    "Maharashtra": ["INS01", "INS03", "INS02"],
    "Madhya Pradesh": ["INS01", "INS05", "INS04"],
    "Rajasthan": ["INS01", "INS02", "INS06"],
    "Uttar Pradesh": ["INS01", "INS04", "INS05"],
    "Odisha": ["INS01", "INS03", "INS04"],
    "Karnataka": ["INS01", "INS02", "INS05"],
}

# Regional crop suitability
state_crop_map = {
    "Maharashtra": ["CR01", "CR02", "CR03", "CR05", "CR08", "CR09"],
    "Madhya Pradesh": ["CR01", "CR06", "CR07", "CR08", "CR05"],
    "Rajasthan": ["CR04", "CR06", "CR07", "CR08", "CR01"],
    "Uttar Pradesh": ["CR02", "CR06", "CR07", "CR08", "CR05"],
    "Odisha": ["CR02", "CR05", "CR10", "CR08"],
    "Karnataka": ["CR02", "CR04", "CR05", "CR09", "CR10", "CR08"],
}

for _, dist in df_districts.iterrows():
    d_id = dist["district_id"]
    state = dist["state_name"]
    vuln = dist["vulnerability_index"]
    
    # Assign insurer based on cluster
    avail_insurers = state_insurer_map[state]
    assigned_insurer = avail_insurers[hash(d_id) % len(avail_insurers)]
    
    eligible_crops = state_crop_map[state]
    
    for _, s_row in df_seasons.iterrows():
        s_id = s_row["season_id"]
        s_name = s_row["season"]
        s_year = s_row["year"]
        
        # Climate shock multipliers
        season_shock = 0.0
        if "El Niño" in s_row["climate_character"]:
            season_shock = 0.35 if vuln > 0.75 else 0.15
        elif "Heatwave" in s_row["climate_character"]:
            season_shock = 0.28 if "Plains" in dist["agro_climatic_zone"] else 0.12
        elif "Unseasonal" in s_row["climate_character"]:
            season_shock = 0.22
        elif "Extended Dry" in s_row["climate_character"]:
            season_shock = 0.25 if "Dry" in dist["agro_climatic_zone"] or "Plateau" in dist["agro_climatic_zone"] else 0.10
        elif "Heavy Monsoon" in s_row["climate_character"]:
            season_shock = 0.20 if "Coast" in dist["agro_climatic_zone"] or vuln > 0.8 else 0.05
        
        for c_id in eligible_crops:
            crop_meta = df_crops[df_crops["crop_id"] == c_id].iloc[0]
            if crop_meta["standard_season"] != s_name:
                continue # Only grow appropriate seasonal crops
            
            # Base Area & Farmers
            base_area = np.random.uniform(15000, 65000) # hectares in district for this crop
            sum_ins_ha = crop_meta["base_sum_insured_ha"] * (1.0 + (s_year - 2019) * 0.04) # inflation
            
            # Farmers breakdown: Loanee (KCC) vs Non-Loanee
            # Non-loanee enrolment was made voluntary in Kharif 2020
            voluntary_factor = 0.85 if s_year >= 2020 else 1.0
            
            loanee_farmers = int(base_area / np.random.uniform(1.2, 1.8))
            non_loanee_prop = np.random.uniform(0.20, 0.48) * voluntary_factor
            if vuln > 0.80 and s_year >= 2021:
                # Adverse selection: high risk districts saw higher voluntary non-loanee participation
                non_loanee_prop += 0.12
                
            non_loanee_farmers = int(loanee_farmers * non_loanee_prop)
            total_farmers = loanee_farmers + non_loanee_farmers
            small_marginal_farmers = int(total_farmers * np.random.uniform(0.72, 0.88))
            
            total_sum_insured_cr = round((base_area * sum_ins_ha) / 1e7, 2)
            
            # Actuarial Premium Rate (APR) vs Subsidized Farmer Rate
            # Actuarial rate depends on district vulnerability and crop risk
            base_apr = np.random.uniform(7.5, 14.5) + (vuln * 5.0)
            if crop_meta["category"] == "Commercial Crops":
                base_apr += 4.0
            actuarial_rate_pct = round(base_apr, 2)
            
            gross_premium_cr = round(total_sum_insured_cr * (actuarial_rate_pct / 100.0), 2)
            
            farmer_rate_pct = crop_meta["farmer_premium_rate_pct"]
            farmer_premium_cr = round(total_sum_insured_cr * (farmer_rate_pct / 100.0), 2)
            total_subsidy_cr = round(gross_premium_cr - farmer_premium_cr, 2)
            
            # 50:50 sharing between Centre and State for normal states
            central_subsidy_cr = round(total_subsidy_cr / 2.0, 2)
            state_subsidy_cr = round(total_subsidy_cr - central_subsidy_cr, 2)
            
            # Weather & CCE telemetry
            rf_departure = np.random.normal(loc=(-15.0 if season_shock > 0.2 else 2.0), scale=18.0)
            rf_departure = round(max(min(rf_departure, 65.0), -65.0), 1)
            
            dry_spell_days = int(max(0, np.random.exponential(scale=(18 if rf_departure < -10 else 7))))
            
            # Yield Shortfall calculation
            # Threshold yield based on 7-year historical average
            ty_kg_ha = np.random.uniform(1200, 3200)
            weather_impact = 0.0
            if rf_departure < -20:
                weather_impact = abs(rf_departure) * 0.75 + dry_spell_days * 0.4
            elif rf_departure > 35:
                weather_impact = (rf_departure - 35) * 0.6 # excessive flood damage
            elif season_shock > 0.25:
                weather_impact = 25.0 + np.random.uniform(5, 15)
                
            yield_shortfall_pct = round(max(0.0, min(85.0, weather_impact + np.random.normal(0, 6.0))), 2)
            actual_yield_kg_ha = round(ty_kg_ha * (1.0 - (yield_shortfall_pct / 100.0)), 1)
            
            # Crop Cut Experiments (CCEs)
            planned_cces = int(base_area / np.random.uniform(180, 260))
            conducted_cces = int(planned_cces * np.random.uniform(0.91, 0.99))
            cce_discrepancy_rate = round(np.random.beta(a=1.5, b=8.0) * 15.0, 2) # % CCEs contested
            
            # Claims logic
            # Under PMFBY, claim = (Threshold Yield - Actual Yield)/Threshold Yield * Sum Insured
            raw_claim_ratio = (yield_shortfall_pct / 100.0)
            if raw_claim_ratio > 0.05:
                # Add localized calamity / mid-season adversity claims
                claims_reported_cr = round(total_sum_insured_cr * raw_claim_ratio * np.random.uniform(0.95, 1.08), 2)
            else:
                claims_reported_cr = round(total_sum_insured_cr * np.random.uniform(0.01, 0.04), 2)
                
            # Rejection / Dispute
            rejection_pct = round(np.random.uniform(2.5, 8.5) + (cce_discrepancy_rate * 0.4), 2)
            claims_rejected_cr = round(claims_reported_cr * (rejection_pct / 100.0), 2)
            claims_approved_cr = round(claims_reported_cr - claims_rejected_cr, 2)
            
            # State Subsidy Delays:
            # When states delay their subsidy share, insurance companies hold claim disbursement
            state_delay_prob = 0.35
            if state in ["Maharashtra", "Odisha", "Uttar Pradesh"] and s_year in [2020, 2021, 2023]:
                state_delay_prob = 0.65
            elif state == "Madhya Pradesh":
                state_delay_prob = 0.25
                
            is_delayed = (random.random() < state_delay_prob)
            if is_delayed:
                delay_category = random.choices(["Delayed 3-6 Months", "Delayed >6 Months"], weights=[0.6, 0.4])[0]
                state_subsidy_delay_days = random.randint(95, 290)
                # Pending disbursement
                payout_ratio = np.random.uniform(0.70, 0.92)
                claims_paid_cr = round(claims_approved_cr * payout_ratio, 2)
                tat_days = int(state_subsidy_delay_days + np.random.uniform(30, 60))
            else:
                delay_category = "Settled on Time"
                state_subsidy_delay_days = random.randint(15, 60)
                claims_paid_cr = claims_approved_cr
                tat_days = int(state_subsidy_delay_days + np.random.uniform(15, 35))
                
            # Loanee vs Non-loanee claim share
            loanee_claim_prop = round(loanee_farmers / float(total_farmers), 3)
            # Adverse selection: non-loanee farmers often claim proportionally more
            non_loanee_loss_multiplier = np.random.uniform(1.10, 1.45) if vuln > 0.7 else 1.05
            
            # Loss Cost Ratio (LCR / Burn Rate)
            lcr_pct = round((claims_paid_cr / max(gross_premium_cr, 0.01)) * 100.0, 2)
            
            fact_records.append({
                "record_id": f"REC_{record_counter:05d}",
                "district_id": d_id,
                "crop_id": c_id,
                "season_id": s_id,
                "insurer_id": assigned_insurer,
                "farmer_applications_loanee": loanee_farmers,
                "farmer_applications_non_loanee": non_loanee_farmers,
                "total_farmers_enrolled": total_farmers,
                "small_marginal_farmers": small_marginal_farmers,
                "insured_area_ha": round(base_area, 2),
                "sum_insured_inr_crores": total_sum_insured_cr,
                "actuarial_premium_rate_pct": actuarial_rate_pct,
                "farmer_premium_rate_pct": farmer_rate_pct,
                "farmer_premium_inr_crores": farmer_premium_cr,
                "central_subsidy_inr_crores": central_subsidy_cr,
                "state_subsidy_inr_crores": state_subsidy_cr,
                "gross_premium_inr_crores": gross_premium_cr,
                "state_subsidy_status": delay_category,
                "state_subsidy_delay_days": state_subsidy_delay_days,
                "rainfall_departure_pct": rf_departure,
                "dry_spell_duration_days": dry_spell_days,
                "threshold_yield_kg_ha": round(ty_kg_ha, 1),
                "actual_yield_kg_ha": actual_yield_kg_ha,
                "yield_shortfall_pct": yield_shortfall_pct,
                "planned_cces": planned_cces,
                "conducted_cces": conducted_cces,
                "cce_discrepancy_rate_pct": cce_discrepancy_rate,
                "claims_reported_inr_crores": claims_reported_cr,
                "claims_approved_inr_crores": claims_approved_cr,
                "claims_rejected_inr_crores": claims_rejected_cr,
                "claims_paid_inr_crores": claims_paid_cr,
                "claim_settlement_tat_days": tat_days,
                "loss_cost_ratio_pct": lcr_pct,
                "non_loanee_loss_multiplier": round(non_loanee_loss_multiplier, 2)
            })
            record_counter += 1

df_fact = pd.DataFrame(fact_records)

# Save dimension and fact CSVs
df_districts.to_csv(os.path.join(DATA_DIR, "dim_districts.csv"), index=False)
df_crops.to_csv(os.path.join(DATA_DIR, "dim_crops.csv"), index=False)
df_seasons.to_csv(os.path.join(DATA_DIR, "dim_seasons.csv"), index=False)
df_insurers.to_csv(os.path.join(DATA_DIR, "dim_insurers.csv"), index=False)
df_fact.to_csv(os.path.join(DATA_DIR, "pmfby_district_level_master.csv"), index=False)

# Populate SQLite Database
db_path = os.path.join(DATA_DIR, "pmfby_actuarial.db")
if os.path.exists(db_path):
    os.remove(db_path)

conn = sqlite3.connect(db_path)
df_districts.to_sql("dim_districts", conn, if_exists="replace", index=False)
df_crops.to_sql("dim_crops", conn, if_exists="replace", index=False)
df_seasons.to_sql("dim_seasons", conn, if_exists="replace", index=False)
df_insurers.to_sql("dim_insurers", conn, if_exists="replace", index=False)
df_fact.to_sql("fact_pmfby_claims_enrolment", conn, if_exists="replace", index=False)

conn.commit()
conn.close()

print(f"Dataset successfully created! Total fact records: {len(df_fact)}")
print(f"Districts: {len(df_districts)} | Crops: {len(df_crops)} | Seasons: {len(df_seasons)} | Insurers: {len(df_insurers)}")
