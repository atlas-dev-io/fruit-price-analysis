from pathlib import Path

import pandas as pd


def export_csv(df: pd.DataFrame, output_path: Path) -> None:
    df.to_csv(output_path, index=False)


def export_summary(summary_text: str, output_path: Path) -> None:
    output_path.write_text(summary_text, encoding="utf-8")

