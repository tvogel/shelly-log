#!/bin/env python3
from datetime import datetime
import sys
import re

log_pattern = re.compile(r'(\S+) (\d+) (\d+\.\d+) (.*)')
new_sntp_pattern = re.compile(r'New SNTP time: (\d+\.\d+)')

boot_time = {}

def process_line(line):
  """
  Process a single log entry and print formatted output.

  This function extracts relevant information from a log entry and prints formatted output
  based on the extracted data. The log entry is expected to have the following format:
  <hostname> <log_id> <sys_time> <log_message>

  The function calculates the boot time of the system by comparing the system time
  with the SNTP time provided in the log entry. It then converts the log time to a
  human-readable format using the calculated boot time.

  Args:
    line: A string representing a log entry.

  Returns:
    None
  """
  global boot_time
  match = log_pattern.search(line)
  if not match:
    print(line, end='')
    return
  host = match.group(1)
  sys_time = float(match.group(3))
  sntp_match = new_sntp_pattern.search(line)
  if sntp_match:
    new_time = float(sntp_match.group(1))
    boot_time[host] = new_time - sys_time
  if not host in boot_time:
    print(line, end='')
    return
  log_datetime = datetime.fromtimestamp(boot_time[host] + sys_time)
  print(f'{match.group(1)} {match.group(2)} {log_datetime.isoformat()} {match.group(4)}')

def process_log():
  """
  Process log entries and print formatted output.

  This function reads log entries from standard input and processes them using the
  process_line function. The function reads log entries until the end of input is reached.

  Args:
    None

  Returns:
    None
  """
  for line in sys.stdin:
    process_line(line)

if __name__ == '__main__':
  process_log()

