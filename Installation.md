## Installation Requirements

To set up the keylogger, please follow these steps:

### 1. System Requirements

- **Python:** Version 3.12.5 or above is recommended.
- **pip:** Version 24.2 or above is recommended.
- **pynput:** Version 1.7.7 is required.
- **smtplib:** Ensure that the `smtplib` library is available in your Python environment.

### 2. Clone the Repository

Clone the keylogger repository from GitHub using the following command:

    git clone https://github.com/moroii69/jLog.git

Navigate to the cloned directory:

    cd jLog

### 3. Install Required Libraries

Run the following command to install the necessary Python library:

    pip install pynput==1.7.7

For more details on the [pynput library](https://pynput.readthedocs.io/en/latest/) and [smtplib](https://docs.python.org/3/library/smtplib.html), refer to their respective documentation.

### 4. Configure the Script

- Open the `execute_keylogger.pyw` or `execute_keylogger.py` file located in the cloned repository.
- Add your Gmail ID and App Password in the specified fields within the script.

### 5. Run the Keylogger Script

Execute the `execute_keylogger.pyw` or `execute_keylogger.py` file to start the keylogger.

## Additional Setup: Running Keylogger on Startup

To ensure the keylogger starts automatically when the PC boots up, you can use one of the following methods:

### Method 1: Task Scheduler (Windows)

1. Open Task Scheduler from the Start menu.
2. Click on Create Basic Task.
3. Follow the wizard to name your task and provide a description.
4. Choose "When the computer starts" as the trigger.
5. Select "Start a Program" and browse to the location of your `execute_keylogger.pyw` or `execute_keylogger.py` file.
6. Finish the setup by reviewing the settings and clicking Finish.

For more information, check out [how to set up Task Scheduler on Windows](https://docs.microsoft.com/en-us/windows/win32/taskschd/task-scheduler-start-page).

### Method 2: Startup Folder (Windows)

1. Press `Win + R` to open the Run dialog.
2. Type `shell:startup` and press Enter to open the Startup folder.
3. Create a shortcut to your `execute_keylogger.pyw` or `execute_keylogger.py` file in this folder.

### Method 3: Registry Editor (Windows)

1. Press `Win + R` to open the Run dialog.
2. Type `regedit` and press Enter to open the Registry Editor.
3. Navigate to `HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run`.
4. Right-click in the right pane and select New > String Value.
5. Name the new value (e.g., Keylogger) and set the value data to the full path of your `execute_keylogger.pyw` or `execute_keylogger.py` file.
6. Close the Registry Editor. The keylogger will now start automatically with Windows.

For guidance on [using the Windows Registry Editor](https://support.microsoft.com/en-us/help/309427/how-to-use-the-windows-registry-editor) and [managing startup programs](https://support.microsoft.com/en-us/windows/how-to-manage-your-startup-apps-in-windows-10-f1e19f26-45f4-48ea-9d44-ea67d4c2e8a0), refer to the respective documentation.

> **Important:** Ensure you have proper authorization and consent before deploying monitoring software. Follow all applicable laws and regulations regarding privacy and data protection.
