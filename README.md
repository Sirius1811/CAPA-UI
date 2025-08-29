# CAPA Portal

This is a Streamlit-based web application for managing Corrective and Preventive Action (CAPA) reports. The app allows users to submit new CAPA forms, store them in a Google Sheet, and generate/download official CAPA PDFs using a Google Docs template.

## Features

- **New CAPA Form:** Fill out and submit CAPA details via a web form.
- **Google Sheets Integration:** All submissions are saved to a Google Sheet for record-keeping.
- **PDF Generation:** Generate official CAPA PDF reports using a Google Docs template and download them.
- **Search & Download:** Search CAPA records by number, department, area, or date range, and download PDFs.

## File Structure

- `app.py` — Main Streamlit application.
- `drive_helper.py` — Handles Google Sheets authentication and data operations.
- `pdf_generator.py` — Generates CAPA PDFs using Google Docs API.
- `requirements.txt` — Python dependencies.

## Setup

1. **Google Cloud Setup**
   - Create a Google Cloud project and enable the Drive and Sheets APIs.
   - Download your `service_account.json` and place it in the project root.

2. **Install Dependencies**
   ```sh
   pip install -r requirements.txt
   ```

3. **Run the App**
   ```sh
   streamlit run app.py
   ```

## Usage

- **New CAPA:** Fill out the form and submit to save to Google Sheets.
- **Search & Download:** Search for CAPA records and download the official PDF.

## Notes

- The Google Docs template ID is set in `pdf_generator.py` as `DOC_TEMPLATE_ID`.
- If you want to use OAuth instead of a service account, place `credentials.json` in the root.

## License

This project is for internal use. Please do not share sensitive credentials.