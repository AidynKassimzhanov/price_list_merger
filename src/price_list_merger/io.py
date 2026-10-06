from pathlib import Path
import pandas as pd


def load_price_list(file_path: Path) -> pd.DataFrame:
    """Загружает прайс-лист из файла CSV или XLSX в pandas DataFrame.

    :param file_path: Путь к файлу прайс-листа.
    :return: DataFrame с загруженными данными.
    :raises FileNotFoundError: Если файл не найден.
    :raises ValueError: Если формат файла не поддерживается или не удалось прочитать CSV.
    """
    if not isinstance(file_path, Path):
        file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"Файл не найден: {file_path}")

    extension = file_path.suffix.lower()

    if extension in [".xlsx", ".xls"]:
        return pd.read_excel(file_path)

    if extension == ".csv":
        encodings = ["utf-8-sig", "utf-8", "cp1251"]
        separators = [";", ","]

        for encoding in encodings:
            for sep in separators:
                try:
                    df = pd.read_csv(file_path, sep=sep, encoding=encoding)
                    if len(df.columns) > 1:
                        return df
                except (UnicodeDecodeError, pd.errors.ParserError):
                    continue
                
        for encoding in encodings:
            try:
                return pd.read_csv(file_path, encoding=encoding)
            except UnicodeDecodeError:
                    continue

        raise ValueError(f"Не удалось прочитать CSV-файл {file_path}. Проверьте кодировку и разделители.")                                

    raise ValueError(f"Неподдерживаемый формат файла: '{extension}'. Допустимы только .csv, .xlsx, .xls")
            