# Interim Data Staging Directory

## Architectural Note: Direct-to-Parquet Streaming

In traditional data processing workflows, intermediate CSV or JSON dumps are written to `data/interim/`.

In this project, processing the 215 monthly CSV files (totaling **9.30 GB**) through an uncompressed intermediate text staging directory would have required an additional **~10 GB of redundant disk storage**, violating the project's **standard student PC footprint constraint**.

### The Solution:
`src/preprocessing.py` implements an optimized chunked streaming pipeline:
1. **Stream:** Ingests monthly CSV chunks directly from `data/raw/` with automatic encoding fallback.
2. **Filter & Clean:** Executes in-memory deduplication, timestamp sorting, and physical range clamping.
3. **Direct Serialization:** Writes directly to columnar Snappy-compressed binary Parquet files under `data/processed/` (`scada_2025_cleaned.parquet`, `scada_2026_cleaned.parquet`, `alarms_cleaned.parquet`).

This reduced total processed storage from ~9.3 GB to **62 MB** with zero intermediate disk waste.
