# CAPA Portal

A Streamlit web application for managing Corrective and Preventive Action (CAPA) reports. It integrates with Google Sheets for data storage and Google Docs for PDF report generation.

---

## Features

- **Submit CAPA Forms:** Fill out and submit CAPA forms via a web interface.
- **Google Sheets Integration:** All submissions are stored in a Google Sheet.
- **PDF Generation:** Generate official CAPA PDF reports using a Google Docs template.
- **Search & Download:** Search CAPA records and download PDFs.

---

## File Structure

- `app.py` — Main Streamlit app.
- `drive_helper.py` — Google Sheets authentication and data operations.
- `pdf_generator.py` — Google Docs template filling and PDF generation.
- `requirements.txt` — Python dependencies.
- `service_account.json` or `credentials.json` — Google API credentials (not included).

---

## Setup

1. **Google Cloud Setup**
   - Enable Google Sheets and Google Drive APIs.
   - Download `service_account.json` or `credentials.json` and place in the project root.
   - Share your Google Sheet and Doc template with the service account email.

2. **Install dependencies**
   ```sh
   pip install -r requirements.txt
   ```

3. **Run the app**
   ```sh
   streamlit run app.py
   ```

---

## Usage

- Use the sidebar to select "New CAPA" or "Search & Download".
- Fill out the form and submit to save to Google Sheets.
- Search for records and download CAPA PDFs.

---

## Notes

- The Google Docs template ID is set in `pdf_generator.py` as `DOC_TEMPLATE_ID`.
- Sheet and worksheet names are set in `drive_helper.py`.
- Credentials files are required for Google API access.

---

## License

For internal use only. Do not share credentials
