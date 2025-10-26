import subprocess
import requests
import csv
import hashlib
import yaml
import io
import hmac
import tkinter as tk


PATCHES_CSV = 'supported_patches.csv'


def parse_patches_list():
    fields = []     # Column Names
    rows = []
    with open(PATCHES_CSV, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        fields = next()
        for row in spamreader:
            print(', '.join(row))


def download_patch_delta(url : str, filename : str, sha256hash : str, outfile_location='./'):
    outfile = f"{outfile_location}{filename}"
    print(f"Attempting to dowload file from URL {url} ...")
    print(f"Saving content to {outfile}")
    # Files are downloaded in streaming form
    with requests.get(url, stream=True) as response:
        with open(outfile, mode="wb") as file:
            for chunk in response.iter_content(chunk_size=10 * 1024):
                file.write(chunk)
    output_hash = calculate_file_hash(outfile)
    print(f"Downloaded file SHA256 HASH")
    print("-------------------------------------------------------------")
    print(output_hash)
    print("-------------------------------------------------------------")
    if (output_hash != sha256hash):
        print("ERROR: SHA256 HASH for downloaded file does not match expected value.")
        print(f"Expected Value (SHA256): {sha256hash}")
        # TODO Add error handlig and exceptions
    else:
        print("Success")

def download_config_file(url : str):
    # TODO Oneshot download for .csv etc
    pass


def calculate_file_hash(path : str) -> str:
    """
    Calculate sha256 hash over the content of a file specified by a path
    """
    hexdigest = ''
    with open(path, "rb") as f:
        digest = hashlib.file_digest(f, "sha256")
        hexdigest = digest.hexdigest()
    return hexdigest

download_patch_delta("http://riders.schafsbreiten.org/patches/Vanilla_to_SRF101.xdelta")
XDELTA_ARGS_LIST = ['./xdelta3', '-v', '-d', '-s', 'SonicRiders.iso', './Patches/patch.xdelta', 'SRF.iso']
#XDELTA_ARGS_LIST = ['./xdelta3', ' ']

pret = subprocess.run(XDELTA_ARGS_LIST, stdout=subprocess.PIPE)
output = pret.stdout.decode()
#print(f"xdelta3: {output}")



window = tk.Tk()
window.title("Hello World")


# Start the event loop.
window.mainloop()