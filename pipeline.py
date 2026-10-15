
import argparse
import logging
import sys

from src import (
    create_cleaning_report,
    load_data,
    process_data,
    save_data,
    setup_logging,
    validate_dataframe,
    validate_input,
)

logger = logging.getLogger(__name__)


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Data Processing Pipeline"
    )
    parser.add_argument("--input", "-i", required=True)
    parser.add_argument("--config", required=True)
    parser.add_argument("--output", "-o", required=True)
    parser.add_argument("--verbose", "-v", action="store_true")
    return parser.parse_args()


def main():
    args = parse_arguments()
    setup_logging(args.verbose)

    if not validate_input(args.input):
        sys.exit(1)

    if not validate_input(args.config):
        sys.exit(1)

    try:
        data = load_data(args.input)
        config = load_data(args.config)
    except (ValueError, OSError) as error:
        logger.error(error)
        sys.exit(1)

    try:
        settings = config["validation"]
        before = len(data)

        validated_data = validate_dataframe(
            data,
            settings["required_columns"],
            settings["numeric_columns"]
        )

        logger.info(
            f"Validation complete: {before} -> "
            f"{len(validated_data)} rows"
        )
    except (ValueError, KeyError) as error:
        logger.error(error)
        sys.exit(1)

    original_data = validated_data.copy()

    try:
        cleaned_data = process_data(validated_data, config)
    except (ValueError, KeyError) as error:
        logger.error(error)
        sys.exit(1)

    logger.info(
        f"Processing complete: {len(original_data)} -> "
        f"{len(cleaned_data)} rows"
    )

    report = create_cleaning_report(
        original_data, cleaned_data
    )

    try:
        output_path = save_data(cleaned_data, args.output)
    except OSError as error:
        logger.error(error)
        sys.exit(1)

    logger.info(f"Saved cleaned data to {output_path}")

    print("\nCleaning report:")
    print(report)


if __name__ == "__main__":
    main()