import os
import shutil
import subprocess
import openpyxl
from openpyxl.chart import BarChart, Reference
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.utils.cell import range_boundaries
import pandas as pd

REPO_DIR = "/working_dir/c_da497d1189927669/pmfby_analytics_repo"
DATA_DIR = os.path.join(REPO_DIR, "data")
OUTPUT_DIR = os.path.join(REPO_DIR, "excel")
DELIVERABLE_DIR = "/working_dir/c_da497d1189927669/artifacts/file_generation/ttl=63d/output"
INTERMEDIATE_DIR = "/working_dir/c_da497d1189927669/artifacts/file_generation/ttl=63d/intermediate"

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(DELIVERABLE_DIR, exist_ok=True)
os.makedirs(INTERMEDIATE_DIR, exist_ok=True)

excel_path = os.path.join(OUTPUT_DIR, "PMFBY_Actuarial_BI_Dashboard.xlsx")

df_master = pd.read_csv(os.path.join(DATA_DIR, "pmfby_district_level_master.csv"))
df_dist = pd.read_csv(os.path.join(DATA_DIR, "dim_districts.csv"))
df_crops = pd.read_csv(os.path.join(DATA_DIR, "dim_crops.csv"))
df_seasons = pd.read_csv(os.path.join(DATA_DIR, "dim_seasons.csv"))

df_merged = df_master.merge(df_dist, on="district_id").merge(df_crops, on="crop_id").merge(df_seasons, on="season_id")

PRIMARY_COLOR = "1B365D"       # Deep Navy
SECONDARY_COLOR = "2C5E8A"     # Slate Blue
ALT_ROW_COLOR = "F4F7FA"       # Subtle cool grey
CARD_BG = "EBF1F6"             # Soft card background
BORDER_COLOR = "D9D9D9"        # Clean gridline border
TOTAL_BORDER_COLOR = "1B365D"

header_fill = PatternFill(start_color=PRIMARY_COLOR, end_color=PRIMARY_COLOR, fill_type="solid")
header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
sub_header_fill = PatternFill(start_color=SECONDARY_COLOR, end_color=SECONDARY_COLOR, fill_type="solid")
sub_header_font = Font(name="Calibri", size=10, bold=True, color="FFFFFF")

thin_border = Border(
    left=Side(style="thin", color=BORDER_COLOR),
    right=Side(style="thin", color=BORDER_COLOR),
    top=Side(style="thin", color=BORDER_COLOR),
    bottom=Side(style="thin", color=BORDER_COLOR),
)

total_border = Border(
    top=Side(style="thin", color=TOTAL_BORDER_COLOR),
    bottom=Side(style="double", color=TOTAL_BORDER_COLOR),
    left=Side(style="thin", color=BORDER_COLOR),
    right=Side(style="thin", color=BORDER_COLOR),
)

alt_fill = PatternFill(start_color=ALT_ROW_COLOR, end_color=ALT_ROW_COLOR, fill_type="solid")

def style_range(ws, cell_range, font=None, fill=None, alignment=None, border=None):
    min_col, min_row, max_col, max_row = range_boundaries(cell_range)
    for row in ws.iter_rows(min_row=min_row, max_row=max_row, min_col=min_col, max_col=max_col):
        for cell in row:
            if font: cell.font = font
            if fill: cell.fill = fill
            if alignment: cell.alignment = alignment
            if border: cell.border = border

def autofit_columns(ws, max_cols=15, skip_rows=(1, 2, 3, 4, 5, 6)):
    merged_multi = {cell.coordinate for rng in ws.merged_cells.ranges if rng.min_col != rng.max_col for row in ws[rng.coord] for cell in row}
    for col_idx in range(1, max_cols + 1):
        col_letter = get_column_letter(col_idx)
        max_len = 0
        for row in range(1, ws.max_row + 1):
            if row in skip_rows or f"{col_letter}{row}" in merged_multi:
                continue
            val = ws.cell(row=row, column=col_idx).value
            if val is not None and not str(val).startswith("="):
                max_len = max(max_len, len(str(val)))
        ws.column_dimensions[col_letter].width = min(max(max_len + 4, 12), 38)

wb = openpyxl.Workbook()

# ==============================================================================
# SHEET 1: Executive_Summary
# ==============================================================================
ws1 = wb.active
ws1.title = "Executive_Summary"
ws1.views.sheetView[0].showGridLines = True

ws1.merge_cells("A1:H1")
ws1["A1"] = "PMFBY Actuarial & Settlement BI Dashboard (2019–2024)"
ws1["A1"].font = Font(name="Calibri", size=16, bold=True, color="FFFFFF")
ws1["A1"].alignment = Alignment(horizontal="center", vertical="center")
ws1["A1"].fill = header_fill
ws1.row_dimensions[1].height = 32

ws1.merge_cells("A2:H2")
ws1["A2"] = "Pradhan Mantri Fasal Bima Yojana — Ministry of Agriculture & Farmers Welfare, India | Comprehensive Actuarial Intelligence"
ws1["A2"].font = Font(name="Calibri", size=10, italic=True, color="FFFFFF")
ws1["A2"].alignment = Alignment(horizontal="center", vertical="center")
ws1["A2"].fill = sub_header_fill
ws1.row_dimensions[2].height = 20

kpi_cards = [
    ("A4:B4", "TOTAL ENROLMENTS", "A5:B5", "=SUM('Data_Model_FactTable'!C2:C931)", "A6:B6", "Farmer Applications"),
    ("C4:D4", "GROSS PREMIUM (₹ CR)", "C5:D5", "=SUM('Data_Model_FactTable'!D2:D931)", "C6:D6", "Underwritten Premium"),
    ("E4:F4", "CLAIMS PAID (₹ CR)", "E5:F5", "=SUM('Data_Model_FactTable'!E2:E931)", "E6:F6", "Direct Benefit Transfers"),
    ("G4:H4", "MACRO LOSS COST RATIO", "G5:H5", "=E5/C5", "G6:H6", "Cumulative Burn Rate"),
]

for h_rng, h_txt, v_rng, v_txt, s_rng, s_txt in kpi_cards:
    ws1.merge_cells(h_rng)
    ws1[h_rng.split(":")[0]] = h_txt
    style_range(ws1, h_rng, font=Font(size=9, bold=True, color="FFFFFF"), fill=sub_header_fill, alignment=Alignment(horizontal="center", vertical="center"))
    
    ws1.merge_cells(v_rng)
    ws1[v_rng.split(":")[0]] = v_txt
    v_cell = ws1[v_rng.split(":")[0]]
    if "E5/C5" in v_txt:
        v_cell.number_format = "0.0%"
    else:
        v_cell.number_format = "₹#,##0.00" if "C5" in v_txt or "E5" in v_txt else "#,##0"
    style_range(ws1, v_rng, font=Font(size=14, bold=True, color=PRIMARY_COLOR), fill=PatternFill(start_color=CARD_BG, end_color=CARD_BG, fill_type="solid"), alignment=Alignment(horizontal="center", vertical="center"))
    
    ws1.merge_cells(s_rng)
    ws1[s_rng.split(":")[0]] = s_txt
    style_range(ws1, s_rng, font=Font(size=8.5, italic=True, color="555555"), fill=PatternFill(start_color=CARD_BG, end_color=CARD_BG, fill_type="solid"), alignment=Alignment(horizontal="center", vertical="center"))

ws1.row_dimensions[4].height = 18
ws1.row_dimensions[5].height = 28
ws1.row_dimensions[6].height = 18

ws1.cell(row=8, column=1, value="State-Level PMFBY Actuarial Underwriting & Settlement Summary (2019-2024)").font = Font(size=12, bold=True, color=PRIMARY_COLOR)
ws1.row_dimensions[8].height = 22

headers_s1 = ["State Name", "Districts", "Farmer Enrolments", "Gross Premium (₹ Cr)", "Claims Paid (₹ Cr)", "Net Margin (₹ Cr)", "Loss Cost Ratio (%)", "Avg TAT (Days)"]
for col_idx, h_text in enumerate(headers_s1, start=1):
    c = ws1.cell(row=9, column=col_idx, value=h_text)
    c.fill = header_fill
    c.font = header_font
    c.alignment = Alignment(horizontal="left", vertical="center")
ws1.row_dimensions[9].height = 24

states_list = ["Maharashtra", "Madhya Pradesh", "Rajasthan", "Uttar Pradesh", "Odisha", "Karnataka"]
for idx, st in enumerate(states_list, start=10):
    ws1.cell(row=idx, column=1, value=st)
    ws1.cell(row=idx, column=2, value=6)
    ws1.cell(row=idx, column=3, value=f"=SUMIFS('Data_Model_FactTable'!$C$2:$C$931, 'Data_Model_FactTable'!$A$2:$A$931, A{idx})")
    ws1.cell(row=idx, column=4, value=f"=SUMIFS('Data_Model_FactTable'!$D$2:$D$931, 'Data_Model_FactTable'!$A$2:$A$931, A{idx})")
    ws1.cell(row=idx, column=5, value=f"=SUMIFS('Data_Model_FactTable'!$E$2:$E$931, 'Data_Model_FactTable'!$A$2:$A$931, A{idx})")
    ws1.cell(row=idx, column=6, value=f"=D{idx}-E{idx}")
    ws1.cell(row=idx, column=7, value=f"=E{idx}/D{idx}")
    ws1.cell(row=idx, column=8, value=f"=AVERAGEIFS('Data_Model_FactTable'!$F$2:$F$931, 'Data_Model_FactTable'!$A$2:$A$931, A{idx})")
    
    ws1.row_dimensions[idx].height = 20
    for col_idx in range(1, 9):
        c = ws1.cell(row=idx, column=col_idx)
        c.border = thin_border
        if idx % 2 == 0: c.fill = alt_fill
        c.alignment = Alignment(horizontal="left" if col_idx == 1 else "right", vertical="center")
        if col_idx in (2, 3): c.number_format = "#,##0"
        elif col_idx in (4, 5, 6): c.number_format = "₹#,##0.00"
        elif col_idx == 7: c.number_format = "0.0%"
        elif col_idx == 8: c.number_format = "0.0"

tot_row = 16
ws1.cell(row=tot_row, column=1, value="National Total / Avg").font = Font(name="Calibri", size=11, bold=True)
ws1.cell(row=tot_row, column=2, value="=SUM(B10:B15)")
ws1.cell(row=tot_row, column=3, value="=SUM(C10:C15)")
ws1.cell(row=tot_row, column=4, value="=SUM(D10:D15)")
ws1.cell(row=tot_row, column=5, value="=SUM(E10:E15)")
ws1.cell(row=tot_row, column=6, value="=D16-E16")
ws1.cell(row=tot_row, column=7, value="=E16/D16")
ws1.cell(row=tot_row, column=8, value="=AVERAGE(H10:H15)")

ws1.row_dimensions[tot_row].height = 22
for col_idx in range(1, 9):
    c = ws1.cell(row=tot_row, column=col_idx)
    c.font = Font(name="Calibri", size=11, bold=True)
    c.border = total_border
    c.alignment = Alignment(horizontal="left" if col_idx == 1 else "right", vertical="center")
    if col_idx in (2, 3): c.number_format = "#,##0"
    elif col_idx in (4, 5, 6): c.number_format = "₹#,##0.00"
    elif col_idx == 7: c.number_format = "0.0%"
    elif col_idx == 8: c.number_format = "0.0"

chart1 = BarChart()
chart1.type = "col"
chart1.style = 10
chart1.title = "Gross Premium vs Claims Paid by State (₹ Crores)"
chart1.y_axis.title = "INR Crores"
chart1.x_axis.title = "State"
chart1.width = 17
chart1.height = 10

data_ref = Reference(ws1, min_col=4, min_row=9, max_col=5, max_row=15)
cats_ref = Reference(ws1, min_col=1, min_row=10, max_row=15)
chart1.add_data(data_ref, titles_from_data=True)
chart1.set_categories(cats_ref)
chart1.legend.legendPos = "t"
ws1.add_chart(chart1, "A19")

autofit_columns(ws1, max_cols=8, skip_rows=(1, 2, 4, 5, 6, 8))

# ==============================================================================
# SHEET 2: Descriptive_Analysis
# ==============================================================================
ws2 = wb.create_sheet(title="Descriptive_Analysis")
ws2.views.sheetView[0].showGridLines = True

ws2.merge_cells("A1:G1")
ws2["A1"] = "Descriptive Analysis: Seasonal & Crop Category Actuarial Distribution"
ws2["A1"].font = Font(name="Calibri", size=15, bold=True, color="FFFFFF")
ws2["A1"].alignment = Alignment(horizontal="center", vertical="center")
ws2["A1"].fill = header_fill
ws2.row_dimensions[1].height = 30

ws2.cell(row=3, column=1, value="1. Kharif (Monsoon) vs Rabi (Winter) Seasonality Performance").font = Font(size=11, bold=True, color=PRIMARY_COLOR)
headers_s2_t1 = ["Season", "Instances", "Gross Premium (₹ Cr)", "Claims Paid (₹ Cr)", "Loss Cost Ratio (%)", "Avg Yield Shortfall (%)", "Avg TAT (Days)"]
for col_idx, h_text in enumerate(headers_s2_t1, start=1):
    c = ws2.cell(row=4, column=col_idx, value=h_text)
    c.fill = sub_header_fill
    c.font = sub_header_font
    c.alignment = Alignment(horizontal="left", vertical="center")
ws2.row_dimensions[4].height = 22

seasons_list = [("Kharif", 540), ("Rabi", 390)]
for idx, (s_name, count_val) in enumerate(seasons_list, start=5):
    ws2.cell(row=idx, column=1, value=s_name)
    ws2.cell(row=idx, column=2, value=count_val)
    ws2.cell(row=idx, column=3, value=f"=SUMIFS('Data_Model_FactTable'!$D$2:$D$931, 'Data_Model_FactTable'!$G$2:$G$931, A{idx})")
    ws2.cell(row=idx, column=4, value=f"=SUMIFS('Data_Model_FactTable'!$E$2:$E$931, 'Data_Model_FactTable'!$G$2:$G$931, A{idx})")
    ws2.cell(row=idx, column=5, value=f"=D{idx}/C{idx}")
    ws2.cell(row=idx, column=6, value=f"=AVERAGEIFS('Data_Model_FactTable'!$L$2:$L$931, 'Data_Model_FactTable'!$G$2:$G$931, A{idx})")
    ws2.cell(row=idx, column=7, value=f"=AVERAGEIFS('Data_Model_FactTable'!$F$2:$F$931, 'Data_Model_FactTable'!$G$2:$G$931, A{idx})")
    
    ws2.row_dimensions[idx].height = 20
    for col_idx in range(1, 8):
        c = ws2.cell(row=idx, column=col_idx)
        c.border = thin_border
        c.alignment = Alignment(horizontal="left" if col_idx == 1 else "right", vertical="center")
        if col_idx == 2: c.number_format = "#,##0"
        elif col_idx in (3, 4): c.number_format = "₹#,##0.00"
        elif col_idx == 5: c.number_format = "0.0%"
        elif col_idx in (6, 7): c.number_format = "0.0"

ws2.cell(row=9, column=1, value="2. Crop Category Actuarial Breakdown").font = Font(size=11, bold=True, color=PRIMARY_COLOR)
headers_s2_t2 = ["Crop Category", "Evaluations", "Gross Premium (₹ Cr)", "Claims Paid (₹ Cr)", "Loss Cost Ratio (%)", "Farmer Statutory Rate (%)", "Est. Actuarial Rate (%)"]
for col_idx, h_text in enumerate(headers_s2_t2, start=1):
    c = ws2.cell(row=10, column=col_idx, value=h_text)
    c.fill = sub_header_fill
    c.font = sub_header_font
    c.alignment = Alignment(horizontal="left", vertical="center")
ws2.row_dimensions[10].height = 22

crop_cats = [
    ("Foodgrains (Cereals)", 300, 2.0, 10.4),
    ("Pulses", 240, 2.0, 11.8),
    ("Oilseeds", 240, 2.0, 12.1),
    ("Commercial Crops", 90, 5.0, 16.5),
    ("Coarse Cereals", 60, 2.0, 9.8),
]
for idx, (cat_name, eval_cnt, f_rate, a_rate) in enumerate(crop_cats, start=11):
    ws2.cell(row=idx, column=1, value=cat_name)
    ws2.cell(row=idx, column=2, value=eval_cnt)
    ws2.cell(row=idx, column=3, value=f"=SUMIFS('Data_Model_FactTable'!$D$2:$D$931, 'Data_Model_FactTable'!$J$2:$J$931, A{idx})")
    ws2.cell(row=idx, column=4, value=f"=SUMIFS('Data_Model_FactTable'!$E$2:$E$931, 'Data_Model_FactTable'!$J$2:$J$931, A{idx})")
    ws2.cell(row=idx, column=5, value=f"=D{idx}/C{idx}")
    ws2.cell(row=idx, column=6, value=f_rate / 100.0)
    ws2.cell(row=idx, column=7, value=a_rate / 100.0)
    
    ws2.row_dimensions[idx].height = 20
    for col_idx in range(1, 8):
        c = ws2.cell(row=idx, column=col_idx)
        c.border = thin_border
        c.alignment = Alignment(horizontal="left" if col_idx == 1 else "right", vertical="center")
        if col_idx == 2: c.number_format = "#,##0"
        elif col_idx in (3, 4): c.number_format = "₹#,##0.00"
        elif col_idx in (5, 6, 7): c.number_format = "0.0%"

autofit_columns(ws2, max_cols=8, skip_rows=(1, 3, 9))

# ==============================================================================
# SHEET 3: Diagnostic_DeepDive
# ==============================================================================
ws3 = wb.create_sheet(title="Diagnostic_DeepDive")
ws3.views.sheetView[0].showGridLines = True

ws3.merge_cells("A1:G1")
ws3["A1"] = "Diagnostic Deep-Dive: Settlement Bottlenecks & Spatial Basis Risk"
ws3["A1"].font = Font(name="Calibri", size=15, bold=True, color="FFFFFF")
ws3["A1"].alignment = Alignment(horizontal="center", vertical="center")
ws3["A1"].fill = header_fill
ws3.row_dimensions[1].height = 30

ws3.cell(row=3, column=1, value="1. Root-Cause: State Subsidy Disbursal Delay vs Claim Turnaround Time (TAT)").font = Font(size=11, bold=True, color=PRIMARY_COLOR)
headers_s3_t1 = ["Subsidy Disbursal Status", "Instances", "Avg Subsidy Delay (Days)", "Avg Claim Settlement TAT (Days)", "Fulfillment Rate (%)"]
for col_idx, h_text in enumerate(headers_s3_t1, start=1):
    c = ws3.cell(row=4, column=col_idx, value=h_text)
    c.fill = sub_header_fill
    c.font = sub_header_font
    c.alignment = Alignment(horizontal="left", vertical="center")
ws3.row_dimensions[4].height = 22

delay_cats = [
    ("Settled on Time", 523, 38.0, 62.3, 100.0),
    ("Delayed 3-6 Months", 241, 201.7, 245.5, 81.7),
    ("Delayed >6 Months", 166, 194.0, 238.1, 80.5),
]
for idx, (status, inst, sub_del, tat, fulf) in enumerate(delay_cats, start=5):
    ws3.cell(row=idx, column=1, value=status)
    ws3.cell(row=idx, column=2, value=inst)
    ws3.cell(row=idx, column=3, value=sub_del)
    ws3.cell(row=idx, column=4, value=tat)
    ws3.cell(row=idx, column=5, value=fulf / 100.0)
    
    ws3.row_dimensions[idx].height = 20
    for col_idx in range(1, 6):
        c = ws3.cell(row=idx, column=col_idx)
        c.border = thin_border
        c.alignment = Alignment(horizontal="left" if col_idx == 1 else "right", vertical="center")
        if col_idx == 2: c.number_format = "#,##0"
        elif col_idx in (3, 4): c.number_format = "0.0"
        elif col_idx == 5: c.number_format = "0.0%"

ws3.cell(row=10, column=1, value="2. Crop Cut Experiment (CCE) Discrepancy Impact on Farmer Claim Rejections").font = Font(size=11, bold=True, color=PRIMARY_COLOR)
headers_s3_t2 = ["CCE Verification Bracket", "Evaluations", "Avg CCE Completion (%)", "Avg CCE Discrepancy (%)", "Farmer Claim Rejection Rate (%)"]
for col_idx, h_text in enumerate(headers_s3_t2, start=1):
    c = ws3.cell(row=11, column=col_idx, value=h_text)
    c.fill = sub_header_fill
    c.font = sub_header_font
    c.alignment = Alignment(horizontal="left", vertical="center")
ws3.row_dimensions[11].height = 22

cce_brackets = [
    ("Low / Clean CCE Verification (<5.0%)", 702, 95.8, 2.1, 3.4),
    ("Moderate CCE Dispute (5.0-9.9%)", 184, 94.2, 7.2, 5.8),
    ("High CCE Dispute (>=10.0%)", 44, 91.5, 12.4, 9.6),
]
for idx, (brk, evals, c_comp, c_disc, c_rej) in enumerate(cce_brackets, start=12):
    ws3.cell(row=idx, column=1, value=brk)
    ws3.cell(row=idx, column=2, value=evals)
    ws3.cell(row=idx, column=3, value=c_comp / 100.0)
    ws3.cell(row=idx, column=4, value=c_disc / 100.0)
    ws3.cell(row=idx, column=5, value=c_rej / 100.0)
    
    ws3.row_dimensions[idx].height = 20
    for col_idx in range(1, 6):
        c = ws3.cell(row=idx, column=col_idx)
        c.border = thin_border
        c.alignment = Alignment(horizontal="left" if col_idx == 1 else "right", vertical="center")
        if col_idx == 2: c.number_format = "#,##0"
        elif col_idx in (3, 4, 5): c.number_format = "0.0%"

autofit_columns(ws3, max_cols=6, skip_rows=(1, 3, 10))

# ==============================================================================
# SHEET 4: Prescriptive_BeedModel
# ==============================================================================
ws4 = wb.create_sheet(title="Prescriptive_BeedModel")
ws4.views.sheetView[0].showGridLines = True

ws4.merge_cells("A1:G1")
ws4["A1"] = "Prescriptive Modeling: Beed Model (80:110) Fiscal Simulation"
ws4["A1"].font = Font(name="Calibri", size=15, bold=True, color="FFFFFF")
ws4["A1"].alignment = Alignment(horizontal="center", vertical="center")
ws4["A1"].fill = header_fill
ws4.row_dimensions[1].height = 30

ws4.cell(row=3, column=1, value="State Budgetary Impact Simulation under the 80:110 Cup-and-Cap Actuarial Model").font = Font(size=11, bold=True, color=PRIMARY_COLOR)
headers_s4 = ["State Name", "Cumulative Premium (₹ Cr)", "Cumulative Claims (₹ Cr)", "LCR (%)", "Clawback Recovered (₹ Cr)", "Excess Liability (₹ Cr)", "Net Fiscal Impact (₹ Cr)"]
for col_idx, h_text in enumerate(headers_s4, start=1):
    c = ws4.cell(row=4, column=col_idx, value=h_text)
    c.fill = sub_header_fill
    c.font = sub_header_font
    c.alignment = Alignment(horizontal="left", vertical="center")
ws4.row_dimensions[4].height = 22

beed_data = [
    ("Rajasthan", 3962.18, 1945.88, 49.1, 1426.29, 28.39, 1397.90),
    ("Maharashtra", 5544.20, 3398.03, 61.3, 1725.16, 339.29, 1385.87),
    ("Karnataka", 4555.80, 2455.73, 53.9, 1313.05, 0.00, 1313.05),
    ("Madhya Pradesh", 4083.89, 2338.11, 57.3, 1120.88, 13.60, 1107.28),
    ("Uttar Pradesh", 4336.17, 2823.74, 65.1, 1091.44, 66.34, 1025.10),
    ("Odisha", 3426.38, 1966.90, 57.4, 967.40, 42.84, 924.56),
]

for idx, (st, prem, clm, lcr, claw, liab, net_f) in enumerate(beed_data, start=5):
    ws4.cell(row=idx, column=1, value=st)
    ws4.cell(row=idx, column=2, value=prem)
    ws4.cell(row=idx, column=3, value=clm)
    ws4.cell(row=idx, column=4, value=lcr / 100.0)
    ws4.cell(row=idx, column=5, value=claw)
    ws4.cell(row=idx, column=6, value=liab)
    ws4.cell(row=idx, column=7, value=f"=E{idx}-F{idx}")
    
    ws4.row_dimensions[idx].height = 20
    for col_idx in range(1, 8):
        c = ws4.cell(row=idx, column=col_idx)
        c.border = thin_border
        if idx % 2 == 0: c.fill = alt_fill
        c.alignment = Alignment(horizontal="left" if col_idx == 1 else "right", vertical="center")
        if col_idx in (2, 3, 5, 6, 7): c.number_format = "₹#,##0.00"
        elif col_idx == 4: c.number_format = "0.0%"

tot_beed = 11
ws4.cell(row=tot_beed, column=1, value="National Cumulative").font = Font(name="Calibri", size=11, bold=True)
ws4.cell(row=tot_beed, column=2, value="=SUM(B5:B10)")
ws4.cell(row=tot_beed, column=3, value="=SUM(C5:C10)")
ws4.cell(row=tot_beed, column=4, value="=C11/B11")
ws4.cell(row=tot_beed, column=5, value="=SUM(E5:E10)")
ws4.cell(row=tot_beed, column=6, value="=SUM(F5:F10)")
ws4.cell(row=tot_beed, column=7, value="=E11-F11")

ws4.row_dimensions[tot_beed].height = 22
for col_idx in range(1, 8):
    c = ws4.cell(row=tot_beed, column=col_idx)
    c.font = Font(name="Calibri", size=11, bold=True)
    c.border = total_border
    c.alignment = Alignment(horizontal="left" if col_idx == 1 else "right", vertical="center")
    if col_idx in (2, 3, 5, 6, 7): c.number_format = "₹#,##0.00"
    elif col_idx == 4: c.number_format = "0.0%"

autofit_columns(ws4, max_cols=7, skip_rows=(1, 3))

# ==============================================================================
# SHEET 5: Data_Model_FactTable
# ==============================================================================
ws5 = wb.create_sheet(title="Data_Model_FactTable")
ws5.views.sheetView[0].showGridLines = True

fact_headers = [
    "State", "District", "Total_Farmers", "Gross_Premium_Cr", "Claims_Paid_Cr",
    "TAT_Days", "Season", "Year", "Crop", "Category", "Subsidy_Status",
    "Yield_Shortfall_Pct", "Loss_Cost_Ratio_Pct"
]

for col_idx, h_text in enumerate(fact_headers, start=1):
    c = ws5.cell(row=1, column=col_idx, value=h_text)
    c.fill = header_fill
    c.font = header_font
    c.alignment = Alignment(horizontal="left", vertical="center")
ws5.row_dimensions[1].height = 24
ws5.freeze_panes = "A2"

for idx, r in df_merged.iterrows():
    row_num = idx + 2
    ws5.cell(row=row_num, column=1, value=r["state_name"])
    ws5.cell(row=row_num, column=2, value=r["district_name"])
    ws5.cell(row=row_num, column=3, value=int(r["total_farmers_enrolled"]))
    ws5.cell(row=row_num, column=4, value=float(r["gross_premium_inr_crores"]))
    ws5.cell(row=row_num, column=5, value=float(r["claims_paid_inr_crores"]))
    ws5.cell(row=row_num, column=6, value=int(r["claim_settlement_tat_days"]))
    ws5.cell(row=row_num, column=7, value=r["season"])
    ws5.cell(row=row_num, column=8, value=int(r["year"]))
    ws5.cell(row=row_num, column=9, value=r["crop_name"])
    ws5.cell(row=row_num, column=10, value=r["category"])
    ws5.cell(row=row_num, column=11, value=r["state_subsidy_status"])
    ws5.cell(row=row_num, column=12, value=float(r["yield_shortfall_pct"]) / 100.0)
    ws5.cell(row=row_num, column=13, value=float(r["loss_cost_ratio_pct"]) / 100.0)
    
    for col_idx in range(1, 14):
        c = ws5.cell(row=row_num, column=col_idx)
        c.border = thin_border
        if row_num % 2 == 0: c.fill = alt_fill
        c.alignment = Alignment(horizontal="left" if col_idx in (1, 2, 7, 9, 10, 11) else "right", vertical="center")
        if col_idx == 3: c.number_format = "#,##0"
        elif col_idx in (4, 5): c.number_format = "0.00"
        elif col_idx in (6, 8): c.number_format = "0"
        elif col_idx in (12, 13): c.number_format = "0.0%"

autofit_columns(ws5, max_cols=13, skip_rows=(1,))

# Save workbook
wb.save(excel_path)

# Recalculate formulas via headless LibreOffice
recalc_dir = os.path.join(INTERMEDIATE_DIR, "recalc_tmp")
os.makedirs(recalc_dir, exist_ok=True)
subprocess.run(
    ["libreoffice", "--headless", "--calc", "--convert-to", "xlsx", "--outdir", recalc_dir, excel_path],
    check=True
)
shutil.move(os.path.join(recalc_dir, os.path.basename(excel_path)), excel_path)
shutil.rmtree(recalc_dir, ignore_errors=True)

deliverable_excel = os.path.join(DELIVERABLE_DIR, "PMFBY_Actuarial_BI_Dashboard.xlsx")
shutil.copy2(excel_path, deliverable_excel)

val_res = subprocess.run(
    ["python3", "skills/excel-processing/scripts/validate_excel.py", deliverable_excel],
    capture_output=True, text=True
)
print("=== Validation Result ===")
print(val_res.stdout)
