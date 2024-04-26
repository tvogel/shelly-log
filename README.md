# Shelly Log

This is a Python script that processes log entries and prints formatted output based on the extracted data. It calculates the boot time of the system by comparing the system time with the SNTP time provided in the log entry. The log time is then converted to a human-readable format using the calculated boot time.

Lines before the first known time-stamp are passed through unchanged.

## Prerequisites

- Python 3

## Usage

  ```shell
  python3 shelly_log.py < log_file.txt
  ```

  Replace `log_file.txt` with the path to your log file.

