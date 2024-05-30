# Readable Params Extension for Burp Suite

## Description

A Burp Suite extension for automatically encoding URLs, making web application exploitation easier by transforming URL-encoded parameters into a readable format and re-encoding them before sending requests.

## Goal

The goal of this extension is to enhance the readability and usability of URL parameters in Burp Suite's Repeater tool, facilitating easier analysis and exploitation of web applications.

## Installation

### Prerequisites

- Burp Suite
- Jython (for running Python extensions in Burp Suite)

### Steps

1. **Download the Jython Standalone JAR**:
   - [Jython Standalone Download](https://www.jython.org/download)

2. **Configure Jython in Burp Suite**:
   - Go to `Extender` > `Options`.
   - In the `Python Environment` section, click `Select file` and choose the downloaded Jython JAR file.

3. **Add the Extension**:
   - Go to the `Extender` > `Extensions` tab.
   - Click `Add`.
   - Set `Extension Type` to `Python`.
   - Click `Select file` and choose your Python extension file (e.g., `readable_params_extension.py`).

4. **Verify Installation**:
   - Check the `Output` tab for a success message indicating that the extension has loaded.

## Usage

1. Open Burp Suite and go to the Repeater tab.
2. Modify the request as usual. The extension will automatically decode and re-encode URL parameters.
3. Use the modified requests to interact with the web application.

## Contributing

Contributions are welcome! Please fork the repository and submit pull requests with improvements or bug fixes.
