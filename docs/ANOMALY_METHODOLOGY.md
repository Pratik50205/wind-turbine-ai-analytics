# Abnormal Behavior and Anomaly Detection Methodology

## 1. Philosophical Grounding & Scope
In accordance with engineering rigor and the project specification, **abnormal behavior is defined as statistically and model-significant deviation from expected operational behavior, evaluated within strict operational and environmental context.**

This framework does **NOT** make unsupported assertions of internal mechanical component failure without physical tear-down inspection evidence. Instead, it provides actionable condition-monitoring indicators for operations & maintenance (O&M) teams.

---

## 2. Core Detection Principles

### 2.1 Model-Based Residual Analysis
Expected turbine power generation $P_{pred} = f(v_{wind}, ho, 	heta, \omega, eta)$ is predicted using the trained ensemble model. The prediction residual is formulated as:
$$e(t) = P_{actual}(t) - P_{pred}(t)$$

### 2.2 Thresholding Framework
1. **Underperformance Deficit Boundary:** An instantaneous threshold of **$e(t) \le -250.0$ kW** identifies observations where active power generation is substantially depressed below expectations during productive wind conditions ($v \ge 3.5$ m/s).
2. **Context Masking:**
   - **Curtailment Filter:** If blade pitch angle is elevated ($eta > 15^\circ$) during high winds ($v > 12$ m/s) with low power output, the period is categorized as **`curtailed_operation`** rather than a mechanical anomaly.
   - **Shutdown Filter:** If the turbine error/stop flag is active (`wtc_ScTurSto_timeon > 300s`), the record is categorized as **`shutdown_associated`** and cross-referenced with `tblAlarmLog`.

### 2.3 Temporal Persistence Rule
To prevent false alarms from transient aerodynamic gusts or single-interval SCADA logging jitter:
- **Rule:** A cluster of anomalous timestamps is promoted to an **`abnormal_behavior`** event if and only if the power deficit condition persists for **at least 3 consecutive 10-minute intervals ($\ge 30$ continuous minutes)**.

---

## 3. Operational Classification Taxonomy
| Status Label | Operational Condition | Actionable O&M Interpretation |
| :--- | :--- | :--- |
| `normal` | Residual within standard tolerance ($|e| < 250$ kW) | Standard continuous power generation |
| `elevated_deviation` | Isolated 10-minute deficit point | Transient gust / wake turbulence noise |
| `abnormal_behavior` | Persistent deficit ($\ge 30$ min continuous) | Flagged for review (pitch drift, yaw misalignment, blade icing, or fouling) |
| `curtailed_operation` | Intentional pitch feathering in strong wind | Grid operator curtailment or noise de-rate |
| `shutdown_associated` | Turbine stopped with error/alarm | Alarm-induced outage (see event log) |
