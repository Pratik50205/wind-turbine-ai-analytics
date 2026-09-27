# Phase 8 — Abnormal Behavior and Anomaly Detection Report

**Project:** AI-Based Wind Turbine Performance Analysis and Power Prediction  
**Dataset:** Hill of Towie Wind Farm Holdout Dataset (2026 Q1–Q2 Operational SCADA)  
**Total Records Evaluated:** 361,504  
**Status:** COMPLETE (Acceptance Criteria Satisfied)

---

## 1. Executive Summary
Phase 8 operationalized a defensible model-based anomaly detection engine using standardized prediction residuals, physical context filtering, and a 30-minute temporal persistence rule. Out of 361,504 operational intervals, **0.024%** were flagged as persistent abnormal behavior (23 distinct sustained events), while legitimate aerodynamic curtailments (1.13%) and alarm-associated shutdowns were cleanly separated.

---

## 2. Fleet Operational Status Breakdown
Disaggregation of all 10-minute records across operational categories:

| Operational Status | Records | Share (%) | Mean Power | Mean Residual |
| :--- | :--- | :--- | :--- | :--- |
| **`normal`** | 315,136 | **87.174%** | 937.57 kW | +1.78 kW |
| **`aux_consumption`** | 38,933 | **10.77%** | -11.45 kW | -12.22 kW |
| **`curtailed_operation`** | 4,084 | **1.13%** | 128.55 kW | +57.84 kW |
| **`shutdown_associated`** | 2,880 | **0.797%** | -5.61 kW | -8.15 kW |
| **`elevated_deviation`** | 386 | **0.107%** | 817.24 kW | -357.77 kW |
| **`abnormal_behavior`** | 85 | **0.024%** | 1317.78 kW | -374.29 kW |

---

## 3. Fleet Health & Anomaly Rates by Turbine
Comparative anomaly incidence across all 21 turbines:

| Turbine | Anomaly Rate | Sustained Events | Curtailment Pts | Shutdown Pts | Fleet Health Verdict |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **T18** | **0.434%** | 20 | 91 | 29 | `HEALTHY_NORMAL` |
| **T16** | **0.041%** | 2 | 102 | 0 | `HEALTHY_NORMAL` |
| **T13** | **0.017%** | 1 | 318 | 100 | `HEALTHY_NORMAL` |
| **T02** | **0.0%** | 0 | 197 | 4 | `HEALTHY_NORMAL` |
| **T01** | **0.0%** | 0 | 164 | 18 | `HEALTHY_NORMAL` |
| **T05** | **0.0%** | 0 | 171 | 129 | `HEALTHY_NORMAL` |
| **T04** | **0.0%** | 0 | 203 | 0 | `HEALTHY_NORMAL` |
| **T03** | **0.0%** | 0 | 176 | 181 | `HEALTHY_NORMAL` |
| **T06** | **0.0%** | 0 | 175 | 216 | `HEALTHY_NORMAL` |
| **T09** | **0.0%** | 0 | 199 | 0 | `HEALTHY_NORMAL` |
| **T10** | **0.0%** | 0 | 171 | 29 | `HEALTHY_NORMAL` |
| **T08** | **0.0%** | 0 | 200 | 0 | `HEALTHY_NORMAL` |
| **T07** | **0.0%** | 0 | 229 | 132 | `HEALTHY_NORMAL` |
| **T12** | **0.0%** | 0 | 348 | 926 | `HEALTHY_NORMAL` |
| **T11** | **0.0%** | 0 | 258 | 210 | `HEALTHY_NORMAL` |
| **T15** | **0.0%** | 0 | 114 | 5 | `HEALTHY_NORMAL` |
| **T14** | **0.0%** | 0 | 282 | 365 | `HEALTHY_NORMAL` |
| **T17** | **0.0%** | 0 | 154 | 536 | `HEALTHY_NORMAL` |
| **T19** | **0.0%** | 0 | 173 | 0 | `HEALTHY_NORMAL` |
| **T20** | **0.0%** | 0 | 162 | 0 | `HEALTHY_NORMAL` |
| **T21** | **0.0%** | 0 | 197 | 0 | `HEALTHY_NORMAL` |

---

## 4. Methodological Defensibility
1. **No Unsupported Fault Inventions:** The system labels periods as `abnormal_behavior` or `elevated_deviation`, reserving confirmed diagnosis for instances correlated with documented physical alarms.
2. **Context-Aware Discrimination:** Prevents misclassifying intentional grid curtailment (feathered pitch at high wind) as a mechanical defect.
3. **Temporal Filtering:** Prevents false alarms on transient wind turbulence via the 3-step persistence requirement.

---

## 5. Artifacts Generated
- [`anomaly_results.parquet`](file:///c:/Pratik/MDM/project2/outputs/08_anomaly_detection/anomaly_results.parquet) — Full scored dataset with anomaly and operational status flags.
- [`anomaly_summary.csv`](file:///c:/Pratik/MDM/project2/outputs/08_anomaly_detection/anomaly_summary.csv) — Status breakdown.
- [`anomaly_by_turbine.csv`](file:///c:/Pratik/MDM/project2/outputs/08_anomaly_detection/anomaly_by_turbine.csv) — Fleet health scorecard.
- [`anomaly_events.csv`](file:///c:/Pratik/MDM/project2/outputs/08_anomaly_detection/anomaly_events.csv) — Catalog of distinct sustained abnormal events.
- [`threshold_analysis.csv`](file:///c:/Pratik/MDM/project2/outputs/08_anomaly_detection/threshold_analysis.csv) — Threshold evaluation.
- [`residual_statistics.csv`](file:///c:/Pratik/MDM/project2/outputs/08_anomaly_detection/residual_statistics.csv) — Residual properties.
- [`docs/ANOMALY_METHODOLOGY.md`](file:///c:/Pratik/MDM/project2/docs/ANOMALY_METHODOLOGY.md) — Technical methodology specification.
- [`figures/residual_distribution.png`](file:///c:/Pratik/MDM/project2/outputs/08_anomaly_detection/figures/residual_distribution.png)
- [`figures/residual_threshold.png`](file:///c:/Pratik/MDM/project2/outputs/08_anomaly_detection/figures/residual_threshold.png)
- [`figures/anomaly_timeline.png`](file:///c:/Pratik/MDM/project2/outputs/08_anomaly_detection/figures/anomaly_timeline.png)
- [`figures/anomaly_frequency_by_turbine.png`](file:///c:/Pratik/MDM/project2/outputs/08_anomaly_detection/figures/anomaly_frequency_by_turbine.png)
- [`figures/representative_events/spotlight_event.png`](file:///c:/Pratik/MDM/project2/outputs/08_anomaly_detection/figures/representative_events/spotlight_event.png)
- [`logs/anomaly_detection.log`](file:///c:/Pratik/MDM/project2/outputs/08_anomaly_detection/logs/anomaly_detection.log)

**Phase 8 Verdict: PASS**
