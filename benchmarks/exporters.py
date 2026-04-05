"""Export benchmark runs to CSV and JSON."""

import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from benchmarks.runner import BenchmarkRunRecord, BenchmarkSummaryRecord


def export_benchmark_results(
    run_records: list[BenchmarkRunRecord],
    summary_records: list[BenchmarkSummaryRecord],
    metadata: dict[str, object],
    *,
    output_root: str | Path = "results",
) -> Path:
    """Write benchmark runs, summaries, and metadata to a timestamped directory."""
    root = Path(output_root)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    output_dir = root / f"{metadata['suite_name']}-{timestamp}"
    output_dir.mkdir(parents=True, exist_ok=False)

    runs_frame = pd.DataFrame([record.to_row() for record in run_records])
    summary_frame = pd.DataFrame([record.to_row() for record in summary_records])

    runs_frame.to_csv(output_dir / "runs.csv", index=False)
    summary_frame.to_csv(output_dir / "summary.csv", index=False)

    metadata_payload = dict(metadata)
    metadata_payload["exported_at_utc"] = timestamp
    with (output_dir / "metadata.json").open("w", encoding="utf-8") as file_obj:
        json.dump(metadata_payload, file_obj, indent=2, sort_keys=True)

    return output_dir
