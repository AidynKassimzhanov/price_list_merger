# Главный модуль запуска CLI для price-list-merger.
import pandas as pd
import argparse
from pathlib import Path

from price_list_merger.io import load_price_list
from price_list_merger.mapping import load_mapping_config, apply_column_mapping
from price_list_merger.cleaning import clean_dataframe
from price_list_merger.validation import validate_dataframe
from price_list_merger.merger import merge_price_lists
from price_list_merger.exporter import export_dataframe


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Консольная программа для объединения и очистки прайс-листов."
    )
    parser.add_argument(
        "--files",
        nargs="+",
        required=True,
        help="Пути к прайс-листам (например: data/supplier_a.xlsx data/supplier_b.csv)",
    )
    parser.add_argument(
        "--config",
        default="config/mapping.json",
        help="Путь к конфигурационному файлу сопоставления колонок",
    )
    parser.add_argument(
        "--output",
        default="output/merged_price_list.xlsx",
        help="Путь для сохранения итогового файла (.xlsx или .csv)",
    )

    args = parser.parse_args()
    
    # 1. Загружаем конфиг маппинга
    config = load_mapping_config(args.config)

    cleaned_dfs = []
    invalid_dfs = []
    total_invalid = 0

    print("Начинаем обработку прайс-листов...")

    for file_path in args.files:
        path = Path(file_path)
        # Имя поставщика берем из имени файла без расширения (например, supplier_a)
        supplier_name = path.stem
        print(f"Обработка файла: {file_path} (Поставщик: {supplier_name})")

        # 2. Чтение
        raw_df = load_price_list(path)

        # 3. Маппинг колонок
        mapped_df = apply_column_mapping(raw_df, supplier_name, config)

        # 4. Очистка типов
        cleaned_df = clean_dataframe(mapped_df)

        # 5. Валидация
        valid_df, invalid_df = validate_dataframe(cleaned_df)
        total_invalid += len(invalid_df)

        if not invalid_df.empty:
            rejected_df = invalid_df.copy()
            rejected_df["supplier"] = supplier_name
            rejected_df["source_file"] = str(path)
            invalid_dfs.append(rejected_df)

        print(f"   └─ Валидных строк: {len(valid_df)}, отбраковано: {len(invalid_df)}")

        cleaned_dfs.append(valid_df)

    # 6. Объединение и дедупликация
    final_df = merge_price_lists(cleaned_dfs, strategy="min_price")

    # 7. Сохранение
    export_dataframe(final_df, args.output)

    if invalid_dfs:
        output_path = Path(args.output)
        rejected_path = output_path.with_name(
            f"{output_path.stem}_rejected{output_path.suffix}"
        )
        rejected_df = pd.concat(invalid_dfs, ignore_index=True)
        export_dataframe(rejected_df, rejected_path)
        print(f"Файл с отбракованными строками сохранен: {rejected_path}")

    print("\n Обработка завершена!")
    print(f" Итоговых позиций в объединенном прайсе: {len(final_df)}")
    print(f"  Всего отбраковано позиций: {total_invalid}")
    print(f" Результат сохранен в: {args.output}")


if __name__ == "__main__":
    main()