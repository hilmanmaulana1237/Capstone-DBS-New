# MindTrack A/B Testing Report

## Experiment
- Variant A: `A_static_education`
- Variant B: `B_generative_ai`
- Metric: `follow_up_recommendation_click`
- Source: `demo_pilot_from_sleep_dataset`
- Note: Demo mode: outcome dibuat deterministik dari dataset untuk menunjukkan pipeline A/B Testing.

## Result
- Sample A: 189 users, success 81 (42.86%)
- Sample B: 185 users, success 96 (51.89%)
- Absolute lift: 9.03%
- Relative lift: 21.08%
- Z-score: 1.7496
- P-value: 0.0802
- Alpha: 0.05
- Decision: **Belum signifikan secara statistik**

## Interpretation
Variant B dianggap lebih baik jika conversion rate lebih tinggi dan p-value < alpha.
Untuk data produksi, jalankan script ini dengan `--group-col` dan `--outcome-col` dari event tracking aplikasi.
