from smb.SMBConnection import SMBConnection
import argparse
import csv
import os

TCP_PORT = 445
EXCEEDED_SIZE = 500 * 1024 * 1024 
CSV_OUTPUT = 'output.csv'

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--username", required=True, help="SMB username")
    parser.add_argument("--password", required=True, help="SMB password")
    parser.add_argument("--ip", required=True, help="IP address of the SMB server")
    parser.add_argument("--machine_name", required=True, help="Client machine name")
    parser.add_argument("--server_name", required=True, help="SMB server name")
    parser.add_argument("--share", required=True, help="Share name on the server")
    return parser.parse_args()


def connect_to_share(args):
    conn = SMBConnection(
        args.username,
        args.password,
        args.machine_name,
        args.server_name,
        domain='',
        use_ntlm_v2=True,
        is_direct_tcp=True
    )
    if conn.connect(args.ip, TCP_PORT):
        print("--- Connected successfully")
        return conn
    else:
        print("Connection failed.")
        return None


def is_folder_empty(conn, share, path):
    files = conn.listPath(share, path)
    real_entries = [f for f in files if f.filename not in ('.', '..')]
    return len(real_entries) == 0


def traverse(conn, share, path, ip, records):
    try:
        entries = conn.listPath(share, path)
    except Exception as e:
        print(f"Error accessing {path}: {e}")
        return

    for entry in entries:
        name = entry.filename
        if name in ('.', '..'):
            continue

        sub_path = os.path.join(path, name)
        column_path = os.path.join(f"\\\\{ip}", share, sub_path)

        if entry.isDirectory:
            if is_folder_empty(conn, share, sub_path):
                records.append([column_path, name, "EMPTY"])
            traverse(conn, share, sub_path, ip, records)
        else:
            if entry.file_size >= EXCEEDED_SIZE:
                records.append([column_path, name, "EXCEEDED"])


def write_csv(records):
    records.sort(key=lambda x: x[2]) 

    header = ["Path", "Name", "Flag"]
    with open(CSV_OUTPUT, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(records)

    print(f"\n--- Results written to {CSV_OUTPUT}")

def print_reslt_csv():
    with open(CSV_OUTPUT, 'r', newline='') as file:
        content = file.read()
        print("\n--- CSV File Content ---")
        print(content)


def main():
    args = parse_arguments()
    records = []

    conn = connect_to_share(args)
    if conn:
        traverse(conn, args.share, "\\", args.ip, records)
        write_csv(records)
        conn.close()
    
    print_reslt_csv()


if __name__ == "__main__":
    main()