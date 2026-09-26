# 🩸 BloodBridge

BloodBridge is a knowledge-based application built with Python and Streamlit. It demonstrates blood component compatibility checking using the patient's ABO blood group, Rhesus (Rh) status, and selected component: **Packed Red Cells (PRC)** or **Fresh Frozen Plasma (FFP)**.

The application uses a simple **forward-chaining inference process** to apply the encoded rules and display matching donor profiles.

> **Educational use only:** This application evaluates only the ABO and Rh rules encoded in its source code. Its output does not establish clinical transfusion suitability and must not be used to make clinical decisions.

## Features

- Patient ABO selection: A, B, AB, or O.
- Patient Rh selection: positive or negative.
- Separate compatibility rules for PRC and FFP.
- Input validation before processing.
- Donor profiles displayed as red labels.
- A maximum of four labels per row, with additional wrapping on smaller screens.
- Nonbreaking labels, keeping text such as “AB Negatif” together.
- Component-specific explanations of the applied rules.

The application interface is in **Indonesian**.

## Technology Stack

- **Python** — application logic.
- **Streamlit** — web interface.
- **HTML and CSS** — donor label formatting.

No database, API key, or external dataset is required.

## Repository Structure

```text
.
├── README.md
├── app.py
└── requirements.txt

```

`app.py` contains the complete application, including the knowledge base, inference functions, input validation, and user interface.

## How the System Works

1. The user selects the patient's ABO group, Rh status, and blood component.
2. The application checks that all selections are complete.
3. The inference engine starts with empty donor ABO and Rh conclusions.
4. Applicable rules populate these conclusions.
5. Rule evaluation repeats until no new conclusions are added.
6. The application combines the resulting ABO groups and Rh statuses into donor profiles.

This is a small, fixed rule system. The ABO and Rh conclusions are independent; it is not a general-purpose rule engine.

### Main Code Components

| Component | Purpose |
|---|---|
| `ABO_RULES` | Stores the ABO donor mappings for PRC and FFP. |
| `cek_aturan()` | Applies rules whose conclusions have not yet been populated. |
| `jalankan_forward_chaining()` | Validates facts and repeats rule evaluation until no new conclusions are added. |
| `tampilkan_label()` | Displays donor profiles as nonbreaking red labels. |
| `main()` | Builds the interface and handles input and output. |

## Requirements

- Python with pip available.
- A current version of Streamlit supporting `st.html()`.
- A web browser.

An internet connection is required to download dependencies. After installation, the application can run locally.

## How to Use

1. Select **Golongan Darah Pasien (ABO)**.
2. Select **Status Rhesus (Rh)**.
3. Select **Jenis Komponen Darah**.
4. Click **Verifikasi Kompatibilitas Donor**.
5. Review the donor profiles and the component-specific explanation.

If a field is empty, the application asks the user to complete all selections.

Changing a selection clears the previous result. Click the verification button again to evaluate the updated inputs.

## Validation

During development, Streamlit application checks covered:

- Empty input.
- Partially completed input.
- All **16 input combinations**: four ABO groups, two Rh statuses, and two components.
- Clearing a previously displayed result when an input changes.

These checks assess software behavior against the encoded rules. They do not constitute clinical validation.

Browser-level visual verification was not completed in the development environment. Check the layout in the browser and screen size used for the demonstration.

## Limitations

- Compatibility evaluation is limited to the encoded ABO and Rh rules.
- The application does not assess other blood group antigens, antibody screening, crossmatching, clinical history, or exceptions to the encoded rules.
- Displayed donor profiles represent rule matches, not available donor inventory.
- The application is intended for educational demonstration.

## Troubleshooting

| Problem | Solution |
|---|---|
| `pip` is not recognized | Use the `python.exe -m pip` commands shown above. |
| `py` is not recognized | Check that Python is installed. If `python --version` works, use `python -m venv .venv`. |
| `No module named streamlit` | Install Streamlit using the same virtual environment Python executable used to run the application. |
| Streamlit has no attribute `html` | Upgrade Streamlit in the virtual environment. |
| Port 8502 is already in use | Stop the existing process or use `--server.port 8503`, then open `http://localhost:8503`. |
| File does not exist | Confirm that the terminal is in the folder containing `blood_final.py`. |
| An older interface appears | Confirm the filename being executed and open the exact Local URL printed in the terminal. |

## Live Demo

A public deployment link has not been added yet.

To try the application, follow the local installation instructions above. The `localhost` address is a local development URL, not a publicly accessible demo.
