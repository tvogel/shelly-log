#!/bin/env python3
from datetime import datetime
import sys
import re

log_pattern = re.compile(r'(\S+) (\d+) (\d+\.\d+) (.*)')
new_sntp_pattern = re.compile(r'New SNTP time: (\d+\.\d+)')

host_states = {}

def process_line(line):
  """
  Process a single log entry and print formatted output.

  This function extracts relevant information from a log entry and prints formatted output
  based on the extracted data. The log entry is expected to have the following format:
  <hostname> <log_id> <sys_time> <log_message>

  The function calculates the boot time of the system by comparing the system time
  with the SNTP time provided in the log entry. It then converts the log time to a
  human-readable format using the calculated boot time.

  This function also detects reboots from dropping log entry ID or dropping system time.

  Args:
    line: A string representing a log entry.

  Returns:
    None
  """
  match = log_pattern.search(line)
  if not match:
    print(line, end='')
    return

  host = match.group(1)
  log_id = int(match.group(2))
  sys_time = float(match.group(3))

  host_state = host_states.setdefault(host, {})

  # If either the log_id or the sys_time drops (significantly), there was a reboot,
  # so reset the boot_time.
  # Small drops may happen when log entries are received out-of-order thanks to UDP.
  if 'log_id' in host_state and log_id < host_state['log_id'] - 10 \
      or 'sys_time' in host_state and sys_time < host_state['sys_time'] - 10:
    del host_state['boot_time']

  sntp_match = new_sntp_pattern.search(line)
  if sntp_match:
    new_time = float(sntp_match.group(1))
    host_state['boot_time'] = new_time - sys_time

  if not 'boot_time' in host_state:
    print(line, end='')
    return

  log_datetime = datetime.fromtimestamp(host_state['boot_time'] + sys_time)
  print(f'{match.group(1)} {match.group(2)} {log_datetime.isoformat()} {match.group(4)}')

  host_state['log_id'] = log_id
  host_state['sys_time'] = sys_time

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

