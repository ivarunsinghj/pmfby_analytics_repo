// ==============================================================================
// Dim_Districts.m
// Power Query (M) Script for ingesting and transforming District Dimension
// ==============================================================================

let
    Source = Csv.Document(File.Contents("data/dim_districts.csv"), [Delimiter=",", Columns=5, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{
        {"district_id", type text},
        {"district_name", type text},
        {"state_name", type text},
        {"agro_climatic_zone", type text},
        {"vulnerability_index", type number}
    }),
    #"Added Vulnerability Tier" = Table.AddColumn(#"Changed Type", "Vulnerability_Tier", each 
        if [vulnerability_index] >= 0.80 then "High Vulnerability (>=0.80)"
        else if [vulnerability_index] >= 0.60 then "Moderate Vulnerability (0.60-0.79)"
        else "Low Vulnerability (<0.60)", type text
    )
in
    #"Added Vulnerability Tier"
