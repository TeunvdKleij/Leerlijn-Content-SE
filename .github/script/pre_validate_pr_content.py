import os

from config import CONTENT_REPORT_PATH


def main():
    if not os.path.exists(CONTENT_REPORT_PATH):
        print(f"Content report file {CONTENT_REPORT_PATH} not found.")
        return

    # Open and read the content report md file
    try:
        with open(CONTENT_REPORT_PATH, "r", encoding="utf-8-sig", errors="ignore") as f:
            content = f.read()
        
        # Print the content of the markdown file
        print(content)
    
    except Exception as e:
        print(f"Error reading content report file: {e}")

if __name__ == "__main__":
    main()