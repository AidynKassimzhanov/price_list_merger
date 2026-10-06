# Модуль для экспорта объединенного прайс-листа.

from pathlib import Path
import pandas as pd


def export_dataframe(df: pd.DataFrame, output_path: str | Path) -> None:
    # Сохраняет DataFrame в CSV или Excel в зависимости от расширения.
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    ext = path.suffix.lower()
    if ext == ".xlsx":
        df.to_excel(path, index=False)
    elif ext == ".csv":
        df.to_csv(path, index=False, encoding="utf-8-sig")
    else:
        raise ValueError(f"Неподдерживаемое расширение для сохранения: {ext}")