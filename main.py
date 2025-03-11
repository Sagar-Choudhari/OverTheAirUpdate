import requests
import subprocess

# Replace this with your Google Apps Script Web App URL
APPS_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbyn6h2xvorslCJyiZdnaHEZMZ--Snx2ZBp2dUrzDf2l8kkxhO7BKsIIWkZz8A_m_o36/exec"
# https://script.google.com/a/macros/vasundharasoftware.com/s/AKfycbzGNxaZXM_QzSoNKwgoK7qoPAuHLz33nflpbNkz6tva8uAadQ5RdBm2ncPj6j0Lesko/exec
# https://script.google.com/macros/s/AKfycbyn6h2xvorslCJyiZdnaHEZMZ--Snx2ZBp2dUrzDf2l8kkxhO7BKsIIWkZz8A_m_o36/exec

# Local file paths
UPDATE_DEB_FILE = "/home/pi/update.deb"
SERVICE_NAME = "your_app_service"


def get_latest_file_id():
    """Fetch the latest .deb file ID from Google Apps Script."""
    try:
        response = requests.get(APPS_SCRIPT_URL)
        if response.status_code == 200:
            file_id = response.text.strip()
            print(f"Latest File ID: {file_id}")
            return file_id
        else:
            print("Failed to get file ID:", response.status_code, response.text)
            return None
    except requests.RequestException as e:
        print("Error fetching file ID:", e)
        return None


def download_update(file_id):
    """Download the latest .deb file from Google Drive."""
    url = f"https://drive.google.com/uc?export=download&id={file_id}"
    try:
        subprocess.run(["wget", "-O", UPDATE_DEB_FILE, url], check=True)
        print("Downloaded latest update.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error downloading update: {e}")
        return False


def install_update():
    """Install the new application version."""
    try:
        subprocess.run(["sudo", "systemctl", "stop", SERVICE_NAME], check=True)
        subprocess.run(["sudo", "dpkg", "-r", "your_app_name"], check=True)
        subprocess.run(["sudo", "dpkg", "-i", UPDATE_DEB_FILE], check=True)
        subprocess.run(["sudo", "systemctl", "start", SERVICE_NAME], check=True)
        print("Update installed successfully.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error installing update: {e}")
        return False


def main():
    print("Checking for updates...")

    file_id = get_latest_file_id()
    if file_id:
        if download_update(file_id):
            print("Update downloaded successfully.")
        #     if install_update():
        #         print("Update completed successfully!")
        #     else:
        #         print("Installation failed.")
        # else:
        #     print("Download failed.")
    else:
        print("No new update available.")


if __name__ == "__main__":
    main()
