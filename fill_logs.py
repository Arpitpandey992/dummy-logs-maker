import os
import random
import sys
import time


class LogsStressTester:

    def __init__(
        self,
        fill_directory: str,
        text_directory: str,
        log_name_prefix: str = "my_log_",
        num_log_writes: int = 20,
        fill_sleep_interval_ms: int = 1000,
        time_to_run_seconds: int = 60,
        max_log_size_mb: int = 30
    ) -> None:
        self.fill_directory = fill_directory
        self.text_directory = text_directory
        self.log_name_prefix = log_name_prefix
        self.num_log_writes = num_log_writes
        self.fill_sleep_interval_ms = fill_sleep_interval_ms
        self.seconds_to_run = time_to_run_seconds
        self.max_log_size_bytes = max_log_size_mb * 1024 * 1024

        if not os.path.exists(self.fill_directory):
            os.makedirs(self.fill_directory)

    def fill_logs(self):
        """
        1. fill `num_log_writes` files with a random log file text every `fill_sleep_interval` milliseconds.
        2. create new log file and rename old to <name>_<timestamp>.log when size exceeds max_log_size_kb (kiloBytes)
        """
        for current_second in range(1, self.seconds_to_run + 1):
            for log_file_index in range(1, self.num_log_writes + 1):
                self._write_log_file(log_file_index, self._get_random_text_from_text_directory())
            print(f"filled {self.num_log_writes} logs")
            time.sleep(self.fill_sleep_interval_ms / 1000)

    def _write_log_file(self, index: int, text_to_append: str):
        log_file_path = os.path.join(self.fill_directory, f"{self.log_name_prefix}{index}.log")
        if os.path.exists(log_file_path):
            text_size_bytes = sys.getsizeof(text_to_append)
            log_size_bytes = os.path.getsize(log_file_path)
            if text_size_bytes + log_size_bytes > self.max_log_size_bytes:
                self._rotate_log_file(log_file_path)  # rename the current log file
        with open(log_file_path, 'a') as f:
            f.write(text_to_append + '\n')

    def _rotate_log_file(self, log_file_path: str):
        """adds a suffix to log file and returns the new path"""
        filepath_without_extension, extension = os.path.splitext(log_file_path)
        new_log_file_path = filepath_without_extension + "_" + self._get_current_timestamp() + extension
        print(f"rotated {os.path.basename(log_file_path)}, renamed to {os.path.basename(new_log_file_path)}")
        os.rename(log_file_path, new_log_file_path)

    def _get_current_timestamp(self) -> str:
        return time.strftime("%Y%m8%d%H%M%S")

    def _get_random_text_from_text_directory(self) -> str:
        logs = [os.path.join(self.text_directory, log) for log in os.listdir(self.text_directory) if log.lower().endswith("log")]
        if not logs:
            raise Exception(f'no logs present in {self.text_directory}')
        random_log = random.choice(logs)
        with open(random_log, 'r') as f:
            return f.read()
