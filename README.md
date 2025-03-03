# TruePing

TruePing is a continuous non-ICMP based latency tester written in Python. It measures the latency to a specified host and port by attempting to create a TCP connection repeatedly at a specified interval. The script also handles retries and provides colored console output for better readability.

This project was developed to help troubleshoot connectivity issues where ICMP packets are dropped/tailed during periods of high bandwidth utilization (or when bandwidth has been severely degraded)

## Features

- Measures latency to a specified host and port using TCP connections.
- Supports configurable intervals between tests.
- Handles connection timeouts and retries.
- Provides colored console output for better readability.
- Gracefully exits and provides statistics on average, minimum, and maximum latency.

## Requirements

- Python 3.x

## Installation

To install TruePing, just clone the repository (no required dependancies!):

```bash
git clone https://github.com/tylxr59/TruePing.git
cd TruePing
pip install -r requirements.txt
```

## Usage

To run TruePing, use the following command:

```bash
python TruePing.py --site example.com
```

You can specify additional options as needed:

```bash
python TruePing.py --site example.com --port 80 --interval 1 --timeout 1 --retries 3
```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request or reach out via Discord (@tylxr59)

## License

This project is licensed under the MIT License.
