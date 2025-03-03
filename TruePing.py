import socket
import time
import argparse
import signal
import sys

# ANSI escape codes for colors
class Colors:
    PURPLE = '\033[38;5;183m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    RESET = '\033[0m'

latencies = []

def test_latency(host, port, interval, timeout, retries):
    while True:
        start_time = time.time()
        attempt = 0
        while attempt < retries or retries == 0:
            try:
                sock = socket.create_connection((host, port), timeout=timeout)
                sock.close()
                latency = (time.time() - start_time) * 1000  # Convert to milliseconds
                latencies.append(latency)
                print(f"{Colors.GREEN}Latency to {host}:{port} is {latency:.2f} ms{Colors.RESET}")
                break
            except socket.timeout:
                if retries == 0:
                    print(f"{Colors.YELLOW}Connection to {host}:{port} timed out. Retrying in {interval} second(s)...{Colors.RESET}")
                else:
                    print(f"{Colors.YELLOW}Connection to {host}:{port} timed out (attempt {attempt + 1}/{retries}){Colors.RESET}")
            except socket.error as e:
                if retries == 0:
                    print(f"{Colors.RED}Failed to connect to {host}:{port} - {e}. Retrying in {interval} second(s)...{Colors.RESET}")
                else:
                    print(f"{Colors.RED}Failed to connect to {host}:{port} - {e} (attempt {attempt + 1}/{retries}){Colors.RESET}")
            attempt += 1
            time.sleep(interval)  # Ensure the sleep interval is respected even on error
        if retries != 0 and attempt == retries:
            print(f"Maximum number of retries ({retries}) reached. Exiting...")
            break
        time.sleep(interval)

def signal_handler(sig, frame):
    if latencies:
        avg_latency = sum(latencies) / len(latencies)
        min_latency = min(latencies)
        max_latency = max(latencies)
        print(f"\n{Colors.PURPLE}Ping statistics for {host}:{Colors.RESET}")
        print(f"     Packets: Sent = {len(latencies)}, Received = {len(latencies)}, Lost = 0 (0% loss),")
        print(f"{Colors.PURPLE}Approximate round trip times in milli-seconds:{Colors.RESET}")
        print(f"     Minimum = {min_latency:.2f}ms, Maximum = {max_latency:.2f}ms, Average = {avg_latency:.2f}ms")
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    
    parser = argparse.ArgumentParser(description="Continuous non-ICMP based latency tester")
    parser.add_argument("-s", "--site", required=True, help="Target site to test latency")
    parser.add_argument("-p", "--port", type=int, default=80, help="Target port to test latency (default: 80)")
    parser.add_argument("-i", "--interval", type=int, default=1, help="Interval between tests in seconds (default: 1)")
    parser.add_argument("-t", "--timeout", type=int, default=1, help="Connection timeout in seconds (default: 1)")
    parser.add_argument("-r", "--retries", type=int, default=0, help="Number of retries for failed connections (default: 3)")
    args = parser.parse_args()

    host = args.site
    port = args.port
    interval = args.interval
    timeout = args.timeout
    retries = args.retries

    test_latency(host, port, interval, timeout, retries)