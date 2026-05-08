from pathlib import Path
import argparse
import math

import numpy as np
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent
DEFAULT_INPUT = BASE_DIR / "dataset_clean.csv"
DEFAULT_RESULTS = BASE_DIR / "ab_testing_results.csv"
DEFAULT_REPORT = BASE_DIR / "ab_testing_report.md"


def normal_cdf(value):
    return 0.5 * (1.0 + math.erf(value / math.sqrt(2.0)))


def two_proportion_z_test(success_a, total_a, success_b, total_b):
    if min(total_a, total_b) == 0:
        raise ValueError("Setiap variant harus memiliki minimal satu sampel.")

    rate_a = success_a / total_a
    rate_b = success_b / total_b
    pooled_rate = (success_a + success_b) / (total_a + total_b)
    standard_error = math.sqrt(pooled_rate * (1 - pooled_rate) * (1 / total_a + 1 / total_b))

    if standard_error == 0:
        return rate_a, rate_b, 0.0, 1.0

    z_score = (rate_b - rate_a) / standard_error
    p_value = 2 * (1 - normal_cdf(abs(z_score)))
    return rate_a, rate_b, z_score, p_value


def pick_column(df, candidates):
    for candidate in candidates:
        if candidate in df.columns:
            return candidate
    return None


def build_demo_pilot(df, seed=42):
    """Membuat pilot A/B deterministik untuk demo jika data eksperimen nyata belum ada."""
    rng = np.random.default_rng(seed)
    sleep_col = pick_column(df, ["Sleep Duration", "Sleep_Duration_Hours"])
    stress_col = pick_column(df, ["Stress Level", "Mental_Fatigue_Score"])
    disorder_col = pick_column(df, ["Sleep Disorder", "Burnout_Risk"])

    pilot = pd.DataFrame(index=df.index.copy())
    pilot["variant"] = np.where(
        rng.random(len(df)) < 0.5,
        "A_static_education",
        "B_generative_ai",
    )

    if sleep_col:
        sleep_hours = pd.to_numeric(df[sleep_col], errors="coerce").fillna(df[sleep_col].median())
    else:
        sleep_hours = pd.Series(np.repeat(7.0, len(df)), index=df.index)

    if stress_col:
        stress = pd.to_numeric(df[stress_col], errors="coerce")
        stress = stress.fillna(stress.median())
        stress_scaled = (stress - stress.min()) / max(stress.max() - stress.min(), 1)
    else:
        stress_scaled = pd.Series(np.repeat(0.5, len(df)), index=df.index)

    if disorder_col and disorder_col == "Sleep Disorder":
        high_risk = ~df[disorder_col].fillna("Aman").astype(str).str.contains(
            "Aman|None|Normal", case=False, regex=True
        )
    elif disorder_col:
        high_risk = df[disorder_col].fillna("Low").astype(str).str.contains(
            "High|Medium", case=False, regex=True
        )
    else:
        high_risk = sleep_hours < 6

    sleep_deficit = np.clip((7.0 - sleep_hours) / 3.0, 0, 1)
    variant_lift = np.where(pilot["variant"].eq("B_generative_ai"), 0.12, 0.0)

    probability = (
        0.26
        + 0.22 * high_risk.astype(float)
        + 0.18 * sleep_deficit
        + 0.14 * stress_scaled
        + variant_lift
    )
    probability = np.clip(probability, 0.05, 0.95)

    pilot["success"] = rng.binomial(1, probability)
    pilot["metric_name"] = "follow_up_recommendation_click"
    pilot["source"] = "demo_pilot_from_sleep_dataset"
    return pilot


def load_experiment_data(args):
    df = pd.read_csv(args.input)

    if args.group_col and args.outcome_col:
        if args.group_col not in df.columns or args.outcome_col not in df.columns:
            raise ValueError("Kolom group/outcome tidak ditemukan pada input data.")

        experiment = df[[args.group_col, args.outcome_col]].rename(
            columns={args.group_col: "variant", args.outcome_col: "success"}
        )
        experiment["success"] = pd.to_numeric(experiment["success"], errors="coerce").fillna(0)
        experiment["success"] = (experiment["success"] > 0).astype(int)
        experiment["metric_name"] = args.metric_name
        experiment["source"] = "real_experiment_data"
        return experiment

    return build_demo_pilot(df, seed=args.seed)


def summarize_ab_test(experiment, alpha=0.05):
    variants = sorted(experiment["variant"].dropna().unique())
    if len(variants) != 2:
        raise ValueError("A/B test membutuhkan tepat dua variant.")

    variant_a, variant_b = variants
    group_a = experiment[experiment["variant"] == variant_a]
    group_b = experiment[experiment["variant"] == variant_b]

    success_a = int(group_a["success"].sum())
    success_b = int(group_b["success"].sum())
    total_a = len(group_a)
    total_b = len(group_b)
    rate_a, rate_b, z_score, p_value = two_proportion_z_test(
        success_a,
        total_a,
        success_b,
        total_b,
    )

    lift = rate_b - rate_a
    relative_lift = lift / rate_a if rate_a else float("inf")
    decision = (
        "Signifikan secara statistik"
        if p_value < alpha
        else "Belum signifikan secara statistik"
    )

    return {
        "variant_a": variant_a,
        "variant_b": variant_b,
        "success_a": success_a,
        "success_b": success_b,
        "total_a": total_a,
        "total_b": total_b,
        "rate_a": rate_a,
        "rate_b": rate_b,
        "absolute_lift": lift,
        "relative_lift": relative_lift,
        "z_score": z_score,
        "p_value": p_value,
        "alpha": alpha,
        "decision": decision,
    }


def write_report(summary, experiment, report_path):
    source = experiment["source"].iloc[0]
    metric = experiment["metric_name"].iloc[0]
    mode_note = (
        "Data eksperimen nyata."
        if source == "real_experiment_data"
        else "Demo mode: outcome dibuat deterministik dari dataset untuk menunjukkan pipeline A/B Testing."
    )

    content = f"""# MindTrack A/B Testing Report

## Experiment
- Variant A: `{summary['variant_a']}`
- Variant B: `{summary['variant_b']}`
- Metric: `{metric}`
- Source: `{source}`
- Note: {mode_note}

## Result
- Sample A: {summary['total_a']} users, success {summary['success_a']} ({summary['rate_a']:.2%})
- Sample B: {summary['total_b']} users, success {summary['success_b']} ({summary['rate_b']:.2%})
- Absolute lift: {summary['absolute_lift']:.2%}
- Relative lift: {summary['relative_lift']:.2%}
- Z-score: {summary['z_score']:.4f}
- P-value: {summary['p_value']:.4f}
- Alpha: {summary['alpha']}
- Decision: **{summary['decision']}**

## Interpretation
Variant B dianggap lebih baik jika conversion rate lebih tinggi dan p-value < alpha.
Untuk data produksi, jalankan script ini dengan `--group-col` dan `--outcome-col` dari event tracking aplikasi.
"""
    report_path.write_text(content, encoding="utf-8")


def parse_args():
    parser = argparse.ArgumentParser(description="MindTrack A/B Testing utility.")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--group-col", default=None)
    parser.add_argument("--outcome-col", default=None)
    parser.add_argument("--metric-name", default="follow_up_recommendation_click")
    parser.add_argument("--alpha", type=float, default=0.05)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--results", type=Path, default=DEFAULT_RESULTS)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    return parser.parse_args()


def main():
    args = parse_args()
    experiment = load_experiment_data(args)
    summary = summarize_ab_test(experiment, alpha=args.alpha)

    experiment.to_csv(args.results, index=False)
    write_report(summary, experiment, args.report)

    print("MindTrack A/B Testing selesai.")
    print(f"Variant A rate: {summary['rate_a']:.2%}")
    print(f"Variant B rate: {summary['rate_b']:.2%}")
    print(f"P-value: {summary['p_value']:.4f}")
    print(f"Decision: {summary['decision']}")
    print(f"Results: {args.results}")
    print(f"Report: {args.report}")


if __name__ == "__main__":
    main()
