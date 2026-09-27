# Hill of Towie Wind Farm — Project Data Dictionary

## 1. Overview
This data dictionary defines the canonical schema, engineering units, source tables, and physical validity boundaries for the AI-Based Wind Turbine Performance Analysis and Power Prediction system.

The dataset source is the **Hill of Towie Wind Farm Open Dataset** (RES / Zenodo record 22662930, Version 2.1.0), comprising 21 Siemens SWT-2.3-VS-82 wind turbines (T01 - T21; Station IDs 2304510 - 2304530).

---

## 2. Core Operational Signals

### 2.1 Target Variable (Power Prediction)
| Canonical Name | Source Table | Raw SCADA Column | Engineering Unit | Valid Physical Range | Description |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `active_power` | `tblSCTurGrid` | `wtc_ActPower_mean` | kW | [-50.0, 2450.0] | 10-minute average real electrical power exported to the grid. Rated turbine capacity is 2300 kW. |

### 2.2 Aerodynamic & Environmental Inputs
| Canonical Name | Source Table | Raw SCADA Column | Engineering Unit | Valid Physical Range | Description |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `wind_speed_active` | `tblSCTurbine` | `wtc_AcWindSp_mean` | m/s | [0.0, 35.0] | 10-minute mean wind speed from the active nacelle anemometer. |
| `wind_speed_primary` | `tblSCTurbine` | `wtc_PrWindSp_mean` | m/s | [0.0, 35.0] | 10-minute mean wind speed from the primary anemometer. |
| `wind_direction` | `tblSCTurbine` | `wtc_ActualWindDirection_mean` | degrees (°) | [0.0, 360.0] | 10-minute mean measured wind direction relative to True North. |
| `ambient_temperature` | `tblSCTurTemp` | `wtc_AmbieTmp_mean` | °C | [-30.0, 45.0] | Ambient outside air temperature used for air density calculation. |

### 2.3 Mechanical & Kinematic Signals
| Canonical Name | Source Table | Raw SCADA Column | Engineering Unit | Valid Physical Range | Description |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `generator_rpm` | `tblSCTurbine` | `wtc_GenRpm_mean` | rpm | [0.0, 2000.0] | High-speed generator shaft rotational speed. Synchronous rated ~1500 rpm. |
| `main_shaft_rpm` | `tblSCTurbine` | `wtc_MainSRpm_mean` | rpm | [0.0, 25.0] | Low-speed rotor shaft rotational speed. Nominal ~16 rpm. |
| `pitch_angle_blade_a` | `tblSCTurbine` | `wtc_PitcPosA_mean` | degrees (°) | [-5.0, 95.0] | Aerodynamic blade pitch angle for Blade A. ~0° at peak capture, ~90° feathered. |
| `nacelle_position` | `tblSCTurbine` | `wtc_NacelPos_mean` | degrees (°) | [0.0, 720.0] | Nacelle yaw orientation angle. |

### 2.4 Electrical Signals
| Canonical Name | Source Table | Raw SCADA Column | Engineering Unit | Valid Physical Range | Description |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `current_phase_r` | `tblSCTurGrid` | `wtc_AmpPhR_mean` | A | [0.0, 2500.0] | AC electrical current in Phase R. |
| `voltage_phase_r` | `tblSCTurGrid` | `wtc_VoltPhR_mean` | V | [600.0, 750.0] | AC phase voltage in Phase R. Nominal ~690 V. |
| `power_factor` | `tblSCTurGrid` | `wtc_CosPhi_mean` | unitless | [-1.0, 1.0] | Grid power factor (cos φ). |
| `reactive_power` | `tblSCTurGrid` | `wtc_ReactPwr_mean` | kVar | [-1500.0, 1500.0] | Reactive electrical power. |
| `grid_frequency` | `tblSCTurGrid` | `wtc_GridFreq_mean` | Hz | [47.0, 53.0] | Grid electrical frequency. Nominal UK grid 50.0 Hz. |

### 2.5 Thermal Signals (Condition Monitoring)
| Canonical Name | Source Table | Raw SCADA Column | Engineering Unit | Valid Physical Range | Description |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `nacelle_temp` | `tblSCTurTemp` | `wtc_NacelTmp_mean` | °C | [-20.0, 60.0] | Nacelle interior ambient temperature. |
| `gearbox_oil_temp` | `tblSCTurTemp` | `wtc_GeOilTmp_mean` | °C | [0.0, 95.0] | Gearbox lubrication oil sump temperature. |
| `gen_winding_temp` | `tblSCTurTemp` | `wtc_Gen1U1Tm_mean` | °C | [0.0, 150.0] | Generator stator winding temperature (Phase 1U1). |
| `gen_bearing_temp` | `tblSCTurTemp` | `wtc_GenBeGTm_mean` | °C | [0.0, 110.0] | Generator non-drive end bearing temperature. |

### 2.6 Hydraulic & Mechanical Pressure
| Canonical Name | Source Table | Raw SCADA Column | Engineering Unit | Valid Physical Range | Description |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `gearbox_oil_pressure` | `tblSCTurPress` | `wtc_GearPres_mean` | bar | [0.0, 10.0] | Gearbox lubrication oil pressure. |
| `brake_oil_pressure` | `tblSCTurPress` | `wtc_BrakPres_mean` | bar | [0.0, 250.0] | Mechanical high-speed shaft brake hydraulic pressure. |

### 2.7 Operational Status & Quality Masking
| Canonical Name | Source Table | Raw SCADA Column | Engineering Unit | Description |
| :--- | :--- | :--- | :--- | :--- |
| `time_in_operation` | `tblSCTurFlag` | `wtc_ScInOper_timeon` | seconds | Duration (0 to 600s) turbine operated normally in 10-minute interval. |
| `time_ready_to_operate` | `tblSCTurFlag` | `wtc_ScReToOp_timeon` | seconds | Duration (0 to 600s) turbine was paused/ready to operate. |
| `time_stopped_error` | `tblSCTurFlag` | `wtc_ScTurSto_timeon` | seconds | Duration (0 to 600s) turbine was stopped due to error or trip. |

---

## 3. Metadata Identifiers
- `TimeStamp`: ISO 8601 UTC timestamp of the 10-minute interval end (`YYYY-MM-DD HH:MM:SS`).
- `StationId`: Unique integer turbine identifier (2304510 to 2304530).
- `TurbineName`: Alphanumeric identifier (`T01` to `T21`).
