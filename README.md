# Requests V1.2 - URL Connectivity & Response Tester

A specialized Python tool designed for developers and security researchers to analyze URL responses, test endpoint availability, and observe how systems handle different parameter inputs.

## Features
- **Endpoint Discovery:** Bulk check paths against a base URL to verify response codes.
- **Dynamic Fuzzing:** Simulate parameter inputs using presets (Strong, Alphanum, etc.) or local wordlists.
- **Smart Filtering:** Quickly isolate "OK" (200) responses from errors.
- **Custom Flagging:** Define specific text strings to identify failed conditions vs. successful hits.
- **UI Highlighting:** Successful hits are displayed in **Gold Impact Bold** for easy visibility.

## Legal & Ethical Warning
This tool is strictly for **educational and authorized testing purposes**. It is designed to help users understand how web requests work and how to secure their own code. 

**Prohibited Actions:**
- Do not use this tool to brute force credentials on websites you do not own.
- Do not use this tool to flood or overwhelm servers (DoS/DDoS).
- Do not use this tool for any activity that violates local or international laws.

The author assumes no liability for misuse of this tool.

## Getting Started
1. **Base URL:** Enter the target domain (e.g., `https://example.com`).
2. **Load Paths:** Import a `.txt` file containing the paths you wish to check.
3. **Configure:** Click on an "OK" result to open the Config Window for specific parameter testing.
4. **Run Fuzz:** Set your retry conditions and start the test.

## Requirements
- Python 3.8+
- `httpx` library (`pip install httpx`)
- `tkinter` (usually included with Python)
