# Corrective and Preventive Action (CAPA) Portal

A web-based application for managing Corrective and Preventive Action (CAPA) reports, built with Streamlit and integrated with Google Sheets and Google Docs APIs. This portal streamlines CAPA documentation, storage, and reporting for your organization.

---

## Overview

The CAPA Portal enables users to:
- **Submit new CAPA forms** via a user-friendly web interface.
- **Store CAPA records** securely in a Google Sheet for easy access and tracking.
- **Generate official CAPA PDF reports** using a Google Docs template, filled dynamically with your data.
- **Search and download CAPA records** by CAPA number, department, area, or date range.

---

## Features

- **Intuitive Form Submission:** Capture all required CAPA details, including incident info, root cause analysis, corrective/preventive actions, team members, and more.
- **Google Sheets Integration:** All submissions are automatically appended to a designated Google Sheet for centralized record-keeping.
- **Automated PDF Generation:** Instantly create downloadable CAPA reports in PDF format using a Google Docs template.
- **Advanced Search:** Filter CAPA records by number, department, area, or incident date range, and download PDFs for selected records.
- **Secure Authentication:** Uses Google service account credentials for seamless, secure API access.

---

## File Structure

- `app.py` — Main Streamlit application (user interface and workflow).
- `drive_helper.py` — Handles Google Sheets authentication, data storage, and querying.
- `pdf_generator.py` — Fills Google Docs template and generates CAPA PDFs.
- `requirements.txt` — Python dependencies.

---

## Setup Instructions

### 1. Google Cloud Setup

- Create a Google Cloud project.
- Enable the **Google Drive API** and **Google Sheets API**.
- Create a service account and download the `service_account.json` file.
- Share your target Google Sheet and Google Doc template with the service account email.

### 2. Google Docs Template

- Create a Google Docs template for CAPA reports.
- Insert placeholders in the format `{{FIELD_NAME}}` (e.g., `{{CAPA_NO}}`, `{{DEPARTMENT}}`) matching the column names in your sheet.
- Set the template ID in `pdf_generator.py` (`DOC_TEMPLATE_ID`).

### 3. Install Dependencies

```sh
pip install -r requirements.txt
```

### 4. Run the Application

```sh
streamlit run app.py
```

---

## Usage

### New CAPA

- Select **New CAPA** in the sidebar.
- Fill out the form with all required details.
- Click **Save to Google Sheet** to submit.

### Search & Download

- Select **Search & Download** in the sidebar.
- Enter search criteria (CAPA No, Department, Area, Date Range).
- Click **Search** to view matching records.
- Download CAPA PDFs for any record.

---

## Configuration & Customization

- **Google Sheet Name:** Set in `drive_helper.py` (`SPREADSHEET_NAME`).
- **Worksheet Name:** Set in `drive_helper.py` (`WORKSHEET_NAME`).
- **Sheet Columns:** Adjust `SHEET_COLUMNS` in `drive_helper.py` to match your data requirements.
- **Google Docs Template ID:** Set in `pdf_generator.py` (`DOC_TEMPLATE_ID`).

---

## Troubleshooting

- **Authentication Errors:** Ensure `service_account.json` is present in the project root and shared with your Google Sheet/Doc.
- **API Quotas:** Make sure your Google Cloud project has sufficient quota for Drive and Sheets API usage.
- **PDF Generation Issues:** Verify that your template placeholders match the keys in your CAPA data.

---

## Security

- Keep your `service_account.json` file secure and **do not share** it publicly.
- This project is intended for internal organizational use.

---

## License

This project is for internal use only. Do not distribute sensitive credentials or proprietary templates.

---

## Contact

For support or customization, contact your IT administrator or
