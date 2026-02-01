
#                                     DISCLAIMER                                       
                                                                                      
  This software is provided for EDUCATIONAL AND RESEARCH PURPOSES ONLY.               
  The author does not condone, encourage, or support the use of this tool for:        
  - Brute-forcing passwords or unauthorized access to systems.                        
  - Performing Denial of Service (DoS) or Distributed Denial of Service (DDoS) attacks. 
   - Any form of illegal cyber activity or disruption of services.                     
                                                                                      
  The user is 100% responsible for their actions. Always ensure you have explicit,     
  written permission before testing the security of any system or network.            
                                                                                      
#

# Requests V1.2 - URL Connectivity & Response Tester

A specialized Python tool designed for developers and security researchers to analyze URL responses and observe how systems handle parameter inputs.

## Features
- Endpoint Discovery: Bulk check paths against a base URL to verify response codes.
- Dynamic Fuzzing: Simulate parameter inputs using presets or local wordlists.
- Smart Filtering: Quickly isolate 200 OK responses from errors.
- Custom Flagging: Define specific text strings to identify failed conditions vs. success.
- UI Highlighting: Successful hits are displayed in Gold Impact Bold.

## Tutorial: Testing the Black Crucible Test Page

This guide explains how to discover the hidden directory and verify credentials on the target site.

### 1. Identify Target Placeholders
Using the browser Inspector on the target site (https://theblackcrucibleofficial.github.io/Test/), we identified the placeholders for the input boxes:
- Username field placeholder: "Username"
- Password field placeholder: "Password"

### 2. Discovering the Account Path
1. Set the **Base URL** in the tool to: `https://theblackcrucibleofficial.github.io/Test/`
2. Click **Run Check** and load your path file (e.g., `paths.txt`).
3. Look for the result: `https://theblackcrucibleofficial.github.io/Test/account/`.
4. Once it shows a green **200 OK**, click that line to open the **Configuration Window**.

### 3. Configuring the Credential Test
In the Configuration Window for the `/account/` path:
1. **BOX 1 (Parameter):** Enter `username` (matching the "Username" placeholder box).
2. **BOX 2 (Parameter):** Enter `Password` (matching the "Password" placeholder box).
3. **Flag / Retry Condition:** Enter `Try again:` into the text box.
   - This tells the tool: "If the response contains 'Try again:', the login attempt failed."

### 4. Running the Test
1. Click **Save**, then click **Test / Fuzz**.
2. The tool will input the username and password into the respective fields based on the site's structure.
3. When the tool sends the correct credentials (`admin` and `password123`), the "Try again:" text will not be found in the response.
4. The tool will then swap the status to **[CORRECT]** in Gold Impact Bold.

## Legal and Ethical Warning
This tool is strictly for educational and authorized testing purposes. The author assumes no liability for misuse.

## Requirements
- Python 3.8+
- httpx library (pip install httpx)
- tkinter
