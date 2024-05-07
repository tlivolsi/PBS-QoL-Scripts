#!/usr/bin/env python3

"""
This script extracts all the nodes used by a PBS job. It uses the qstat command to get the job's 
information and then parses the output to extract the node names. The node names are then printed 
in sorted order.
"""

import subprocess
import re
import argparse

def extract_all_nodes(job_id):
    command = f"qstat -fx {job_id}"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    if stderr:
        print("Error running qstat:")
        print(stderr.decode())
        return

    output = stdout.decode()
    node_list = []
    pattern = re.compile(r'exec_vnode = (.*)', re.DOTALL)
    match = pattern.search(output)
    if match:
        node_entries = match.group(1).replace('\n', '').split('+')
        for entry in node_entries:
            node_name = re.sub(r':.*', '', entry)
            node_name = re.sub(r'\W', '', node_name).strip()
            node_list.append(node_name)

    # Print each unique node name in sorted order
    if node_list:
        for node in sorted(set(node_list)):
            print(node)
    else:
        print("No nodes found in the output.")

def main():
    parser = argparse.ArgumentParser(description='Extract used nodes from a PBS job.')
    parser.add_argument('-j', '--job-id', required=True, help='PBS job ID')
    args = parser.parse_args()

    job_id = args.job_id
    extract_all_nodes(job_id)

if __name__ == '__main__':
    main()