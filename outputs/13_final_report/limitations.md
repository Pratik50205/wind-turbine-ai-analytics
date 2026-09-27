# System Limitations & Engineering Constraints

1. **10-Minute Averaged SCADA Sampling:**
   High-frequency aerodynamic turbulence, gust impacts, and transient sub-second grid fluctuations are smoothed by 10-minute aggregation.
2. **Barometric Pressure Absence:**
   Direct barometric air pressure measurements were not available in `tblSCTurGrid`; air density was estimated using a temperature-dependent sea-level standard atmosphere proxy.
3. **Terrain & Wake Dynamics:**
   Turbine-to-turbine wake interactions vary dynamically with wind direction across the ridge, which is modeled statistically rather than via computationally intensive 3D computational fluid dynamics (CFD).
4. **Safety Control Scope:**
   The ML models are intended for offline and near-real-time supervisory monitoring and maintenance prioritization. They are not certified for closed-loop safety shutdown actuators.
