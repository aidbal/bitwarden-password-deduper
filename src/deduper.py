#! /usr/bin/python3

# deduper.py
# Removes duplicates from Bitwarden exported .csv file
# All the credits go to u/5erif

import hashlib
import logging
import sys
from enum import IntEnum
from urllib.parse import urlparse

FILE_ENCODING = "utf8"
CSV_EXTENSION_LENGTH = 4  # .csv
DEDUPED_FILE_SUFFIX = "_deduped.csv"
REMOVED_ENTRIES_FILE_SUFFIX = "_removed_entries.csv"


class CsvFields(IntEnum):
    """
    Field ordinals in Bitwarden CSV
    """
    FOLDER = 0
    FAVORITE = 1
    TYPE = 2
    NAME = 3
    NOTES = 4
    FIELDS = 5
    URI = 6
    USERNAME = 7
    PASSWORD = 8
    TOTP = 9


def main(argv):
    if len(argv) != 1:
        logging.error("Missing input file path")
        sys.exit(1)

    original_fpath = argv[0]
    original_fpath_wo_extension = original_fpath[0: (len(original_fpath) - CSV_EXTENSION_LENGTH)]

    deduped_fpath = original_fpath_wo_extension + DEDUPED_FILE_SUFFIX
    removed_entries_fpath = original_fpath_wo_extension + REMOVED_ENTRIES_FILE_SUFFIX

    unique_entries_hash_set = set()

    read_lines = -1
    written_lines = 0
    previous_line_buffer = ""

    deduped_file = open(deduped_fpath, "w", encoding=FILE_ENCODING)
    removed_entries_file = open(removed_entries_fpath, "w", encoding=FILE_ENCODING)

    for line in open(original_fpath, "r", encoding=FILE_ENCODING):
        read_lines += 1

        if read_lines == 0:
            continue

        parsed_fields = line.split(",")

        if len(parsed_fields) < 10:
            # Add previous line if was split
            line = previous_line_buffer.strip("\n") + line
            previous_line_buffer = line

            parsed_fields = line.split(",")

            if len(parsed_fields) > 9:
                logging.warning(f"Recovered with line {read_lines}:\n{line}")
                previous_line_buffer = ""
            else:
                logging.error(f"Missing fields in line {read_lines}:\n{line}")
                removed_entries_file.write(line)
                continue
        else:
            previous_line_buffer = ""

        if read_lines != 0:  # 0th line is fields header
            domain = urlparse(parsed_fields[CsvFields.URI]).netloc
            if len(domain) > 0:
                parsed_fields[CsvFields.URI] = domain

        token = parsed_fields[CsvFields.URI] + parsed_fields[CsvFields.USERNAME] + parsed_fields[CsvFields.PASSWORD]
        hashValue = hashlib.md5(token.rstrip().encode("utf-8")).hexdigest()

        if hashValue not in unique_entries_hash_set:
            deduped_file.write(line)
            unique_entries_hash_set.add(hashValue)
            written_lines += 1
        else:
            removed_entries_file.write(line)

            logging.warning(f"Skipping duplicate on line {read_lines}:\n"
                            + f"Name: '{parsed_fields[CsvFields.NAME]}', "
                            + f"Uri: '{parsed_fields[CsvFields.URI]}', "
                            + f"Username: '{parsed_fields[CsvFields.USERNAME]}'\n")

    deduped_file.close()
    removed_entries_file.close()

    dup_count = read_lines - written_lines
    logging.info(f"\nOutput file: {deduped_fpath}\n{written_lines} unique entries saved")
    logging.info(f"\n{dup_count} duplicates saved to {removed_entries_fpath}")


if __name__ == "__main__":
    main(sys.argv[1:])
