import ftplib
import os
import time
from termcolor import colored

def display_welcome_message():
    message = colored("Welcome by lothbrok9", "magenta")
    for char in message:
        print(char, end='', flush=True)
        time.sleep(0.1)
    print("\n")

class FTPClient:
    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password
        try:
            self.ftp = ftplib.FTP(self.host)
            self.ftp.login(user=self.username, passwd=self.password)
            print(f"Connected to {self.host}")
        except ftplib.all_errors as e:
            print(f"Failed to connect: {e}")
            exit(1)

    def list_files(self):
        try:
            files = self.ftp.nlst()
            for file in files:
                print(file)
        except ftplib.all_errors as e:
            print(f"Failed to list files: {e}")

    def download_file(self, remote_file, local_file):
        try:
            with open(local_file, 'wb') as f:
                self.ftp.retrbinary(f"RETR {remote_file}", f.write)
            print(f"Downloaded {remote_file} to {local_file}")
        except ftplib.all_errors as e:
            print(f"Failed to download file: {e}")

    def upload_file(self, local_file, remote_file):
        try:
            with open(local_file, 'rb') as f:
                self.ftp.storbinary(f"STOR {remote_file}", f)
            print(f"Uploaded {local_file} to {remote_file}")
        except ftplib.all_errors as e:
            print(f"Failed to upload file: {e}")

    def view_file(self, remote_file):
        try:
            lines = []
            self.ftp.retrlines(f"RETR {remote_file}", lines.append)
            for line in lines:
                print(line)
        except ftplib.all_errors as e:
            print(f"Failed to view file: {e}")

    def close(self):
        try:
            self.ftp.quit()
            print("Connection closed")
        except ftplib.all_errors as e:
            print(f"Failed to close connection: {e}")

if __name__ == "__main__":
    display_welcome_message()
    
    host = input("Enter FTP host: ")
    username = input("Enter username: ")
    password = input("Enter password: ")

    ftp_client = FTPClient(host, username, password)

    while True:
        print("\nOptions:")
        print("1. List files")
        print("2. Download file")
        print("3. Upload file")
        print("4. View file")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            ftp_client.list_files()
        elif choice == '2':
            remote_file = input("Enter the name of the file to download: ")
            local_file = input("Enter the local path to save the file: ")
            ftp_client.download_file(remote_file, local_file)
        elif choice == '3':
            local_file = input("Enter the local file path to upload: ")
            remote_file = input("Enter the remote file name: ")
            ftp_client.upload_file(local_file, remote_file)
        elif choice == '4':
            remote_file = input("Enter the name of the file to view: ")
            ftp_client.view_file(remote_file)
        elif choice == '5':
            ftp_client.close()
            break
        else:
            print("Invalid choice, please try again.")
