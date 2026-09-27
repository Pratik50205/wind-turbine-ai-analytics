# Phase 2 — Data Preprocessing and Quality Engine Report

**Project:** AI-Based Wind Turbine Performance Analysis and Power Prediction  
**Dataset:** Hill of Towie Wind Farm (21 Siemens SWT-2.3-VS-82 Turbines)  
**Status:** COMPLETE (Acceptance Criteria Satisfied)

---

## 1. Executive Summary
Phase 2 implemented and executed an end-to-end data cleaning, physical validation, and transformation pipeline across all 16 months of operational SCADA data (2025 full year + 2026 Q1–Q2). Raw tables were harmonized, cross-table joined on composite keys (`TimeStamp`, `StationId`), validated against strict physical boundaries, and converted into high-performance Parquet format with 0% data fabrication.

### Key Preprocessing Milestones:
- **Raw Records Ingested:** 1,421,276
- **Duplicates Removed:** 272 (0.0191%)
- **Physically Impossible Outliers Filtered:** 0 (0.0%)
- **Clean Analytical Records Retained:** **1,420,964** (**99.98% retention rate**)
- **Data Quality Index (DQI):** **99.98 / 100 (EXCELLENT)**

---

## 2. Pipeline Traceability & Retention
Every transformation is fully tracked and recorded in [`row_counts_before_after.csv`](file:///c:/Pratik/MDM/project2/outputs/02_data_preprocessing/row_counts_before_after.csv):

| Pipeline Stage | Rows Before | Rows After | Rows Removed | Pct Removed | Reason |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **1. Raw Ingestion** | 1,421,276 | 1,421,276 | 0 | 0.0% | Multi-table inner join across SCADA tables |
| **2. Duplicate Deduping** | 1,421,276 | 1,421,004 | 272 | 0.0191% | Exact timestamp duplicate elimination |
| **3. Physical Validation** | 1,421,004 | 1,421,004 | 0 | 0.0% | Out-of-bounds power, wind speed, or RPM |
| **4. Target Completeness** | 1,421,004 | 1,420,964 | 40 | 0.0028% | Residual unrecoverable target/wind NaNs |
| **Final Retained** | — | **1,420,964** | — | **99.98%** | Clean analytical dataset ready for modeling |

---

## 3. Physical Boundary & Outlier Handling
The pipeline distinguishes between legitimate extreme operational events and unphysical sensor faults:

1. **Auxiliary Parasitic Consumption (276,956 records):**
   - Active power values between -50.0 kW and 0.0 kW represent real electricity imported by turbines to power heaters, yaw drives, and electronics during calm wind. These are **preserved** and flagged via `is_aux_consumption=1`.
2. **Aerodynamic Curtailment / De-rating (12,872 records):**
   - High wind speeds (>12 m/s) with feathered blade pitch (>15°) and low power (<500 kW) represent real curtailment events. These are **preserved** and flagged via `is_curtailed=1`, ensuring the anomaly detection engine can distinguish curtailment from mechanical faults.
3. **Shutdown Events (19,162 records):**
   - Periods where `wtc_ScTurSto_timeon > 300s` are correlated with `tblAlarmLog` and flagged via `is_stopped=1`.

---

## 4. Processed Data Artifacts
Cleaned datasets have been exported to [`data/processed/`](file:///c:/Pratik/MDM/project2/data/processed/):
- **`scada_2025_cleaned.parquet`**: 1,059,460 rows, 35 columns (full annual baseline).
- **`scada_2026_cleaned.parquet`**: 361,504 rows, 35 columns (holdout test set).
- **`alarms_cleaned.parquet`**: 512,117 event records with alarm descriptions, stopping status, and duration.
- **`cleaned_sample.csv`**: 10,000-row representative CSV for rapid inspection.

---

## 5. Data Quality Scorecard
| Metric | Score | Benchmark | Status | Detail |
| :--- | :--- | :--- | :--- | :--- |
| **Data Completeness** | 100.0% | >= 95.0% | EXCELLENT | Residual missingness < 0.1% |
| **Physical Validity** | 100.0% | >= 99.0% | EXCELLENT | 0 unphysical spikes in clean data |
| **Temporal Consistency** | 99.85% | >= 98.0% | EXCELLENT | 10-min grid verified across all 21 turbines |
| **Retention Rate** | 99.98% | >= 95.0% | PASS | Over 99% of raw records cleanly preserved |
| **Overall DQI** | **99.98 / 100** | >= 90.0 | **EXCELLENT** | Production-grade foundation |

---

## 6. Diagnostic Visualizations Generated
- [`figures/missingness_before.png`](file:///c:/Pratik/MDM/project2/outputs/02_data_preprocessing/figures/missingness_before.png)
- [`figures/missingness_after.png`](file:///c:/Pratik/MDM/project2/outputs/02_data_preprocessing/figures/missingness_after.png)
- [`figures/distributions_before.png`](file:///c:/Pratik/MDM/project2/outputs/02_data_preprocessing/figures/distributions_before.png)
- [`figures/distributions_after.png`](file:///c:/Pratik/MDM/project2/outputs/02_data_preprocessing/figures/distributions_after.png)
- [`figures/cleaning_impact.png`](file:///c:/Pratik/MDM/project2/outputs/02_data_preprocessing/figures/cleaning_impact.png)

**Phase 2 Verdict: PASS**
