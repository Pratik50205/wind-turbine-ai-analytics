# Data Card: Hill of Towie Wind Farm Open SCADA Dataset

## Dataset Description
- **Facility:** Hill of Towie Wind Farm, Moray, Scotland.
- **Operator/Source:** Open SCADA Dataset for Hill of Towie.
- **Turbine Model:** Siemens SWT-2.3-VS-82 (21 turbines, Station IDs `2304510`–`2304530`).
- **Nominal Power:** 2.3 MW per turbine (48.3 MW farm total).
- **Rotor Diameter:** 82 m (Swept Area: 5281 m²).
- **Sampling Interval:** 10-minute continuous SCADA averages.
- **Time Coverage:** January 1, 2025 to April 30, 2026 (16 months).
- **Raw Volume:** 215 CSV files totaling 9.30 GB.

## Cleaned Data Files
- `data/processed/scada_2025_cleaned.parquet` (1,059,460 rows, 42.1 MB)
- `data/processed/scada_2026_cleaned.parquet` (361,504 rows, 14.8 MB)
- `data/processed/alarms_cleaned.parquet` (512,117 events, 5.4 MB)

## Quality Scorecard
- **Data Quality Index (DQI):** 99.8 / 100
- **Timestamp Completeness:** 100%
- **Physical Range Adherence:** 99.98%
