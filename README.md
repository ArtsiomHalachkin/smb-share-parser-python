# SMB Share Scanner

A Python script to connect to an SMB share, traverse its directories, and generate a CSV report of empty folders and files exceeding 500MB.

## Requirements

- Python 3.6+
- [pysmb](https://pysmb.readthedocs.io/en/latest/)

## Installation

1. Clone this repository
3. Create and Activate a Virtual Environment

**Windows:**
```sh
python -m venv venv
venv\Scripts\activate
```

**Linux/macOS:**
```sh
python -m venv venv
source venv/bin/activate
```

Then install dependencies:

```sh
pip install -r requirements.txt
```

## Usage

Run the script from the command line with the required arguments:

```sh
python main.py --username <USERNAME> --password <PASSWORD> --ip <SMB_SERVER_IP> --machine_name <CLIENT_MACHINE_NAME> --server_name <SMB_SERVER_NAME> --share <SHARE_NAME>
```

After execution, results will be saved to `output.csv` and printed to the console.

## Arguments

- `--username` (required): SMB username.
- `--password` (required): SMB password.
- `--ip` (required): IP address of the SMB server.
- `--machine_name` (required): Client machine name.
- `--server_name` (required): SMB server name.
- `--share` (required): Share name on the server.
