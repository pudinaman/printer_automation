import os
import pyautogui
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class PDFPrintHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory and event.src_path.lower().endswith('.pdf'):
            print(f"New PDF file created: {event.src_path}")
            wait_for_file(event.src_path)
            print_pdf(event.src_path)

def wait_for_file(file_path, max_attempts=30, sleep_duration=1):
    attempts = 0
    while not os.path.exists(file_path) and attempts < max_attempts:
        attempts += 1
        time.sleep(sleep_duration)
    if attempts == max_attempts:
        print(f"File not found: {file_path}")

def print_pdf(file_path):
    # Use os.startfile to open the file with the default associated application
    os.startfile(file_path)

    # Wait for the PDF viewer to open (adjust sleep duration as needed)
    time.sleep(5)

    # Simulate a keypress to trigger the print operation (adjust coordinates as needed)
    pyautogui.hotkey('ctrl', 'p')

    # Wait for user to give permission to print (adjust sleep duration as needed)
    time.sleep(2)  # Adjust this time based on how long it typically takes to respond to the print dialog

    # Press enter to confirm the print operation
    pyautogui.press('enter')

    # Remove the PDF file after printing
    os.remove(file_path)
    print(f"Deleted: {file_path}")

def watch_for_pdfs(directory):
    event_handler = PDFPrintHandler()
    observer = Observer()
    observer.schedule(event_handler, path=directory, recursive=False)
    observer.start()
    print(f"Watching for PDF files in {directory}. Press Ctrl+C to stop.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    current_directory = os.getcwd()
    watch_for_pdfs(current_directory)
