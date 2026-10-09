// ==============================================================================
// Dim_Crops.m
// ==============================================================================

let
    Source = Csv.Document(File.Contents("data/dim_crops.csv"), [Delimiter=",", Columns=6, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{
        {"crop_id", type text},
        {"crop_name", type text},
        {"category", type text},
        {"standard_season", type text},
        {"farmer_premium_rate_pct", type number},
        {"base_sum_insured_ha", type number}
    })
in
    #"Changed Type"
