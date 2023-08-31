import os
import threading
from fill_logs import LogsStressTester


def run_async(func: callable) -> threading.Thread:
    thread = threading.Thread(target=func)
    thread.start()
    return thread


def stress_test(num_threads: int = 4):
    cwd = os.getcwd()
    text_directory = os.path.join(cwd, "testlogs")
    threads: list[threading.Thread] = []
    for thread_number in range(1, num_threads + 1):
        fill_directory = os.path.join(cwd, "logs")
        log_stress_tester = LogsStressTester(
            fill_directory,
            text_directory,
            log_name_prefix=f'thread_{thread_number}_log_',
            num_log_writes=1,
            fill_sleep_interval_ms=1*1000,
            time_to_run_seconds=60*5,
        )
        threads.append(run_async(log_stress_tester.fill_logs))

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    num_threads = 8
    stress_test(num_threads)
