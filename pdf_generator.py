from io import BytesIO
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import json
import os

# --- OAuth setup using credentials.json (same as drive_helper.py) ---
SCOPES = ["https://www.googleapis.com/auth/documents", "https://www.googleapis.com/auth/drive"]
DOC_TEMPLATE_ID = "1qGFGK9NOkISKbGWYqg3U0w5jqNOmVeSCnS97SJJawG0"  # your Google Doc template ID

def get_creds():
    creds = None
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)
    return creds

creds = get_creds()
docs_service = build("docs", "v1", credentials=creds)
drive_service = build("drive", "v3", credentials=creds)


def _tick(val: str) -> str:
    """Return a checkmark if 'YES', else empty string."""
    return "✔" if str(val).strip().upper() == "YES" else ""


def generate_capa_pdf(row: dict) -> bytes:
    """
    Fill the Google Docs CAPA template with row values and return PDF bytes.
    """

    # --- 1. Copy the template temporarily ---
    copy_title = f"CAPA_{row.get('CAPA_NO', 'TEMP')}"
    body = {"name": copy_title}
    copied_file = drive_service.files().copy(fileId=DOC_TEMPLATE_ID, body=body).execute()
    doc_id = copied_file.get("id")

    # --- 2. Build replacements dict ---
    replacements = {}
    for k, v in row.items():
        if k in ["A", "B", "C", "D", "M1", "M2", "M3", "M4", "M5", "O1", "O2", "O3", "O4", "O5"]:
            replacements[k] = _tick(v)
        else:
            replacements[k] = str(v) if v else ""

    # --- 3. Replace placeholders in copied Doc (one by one) ---
    for key, value in replacements.items():
        request = {
            "replaceAllText": {
                "containsText": {"text": f"{{{{{key}}}}}", "matchCase": True},
                "replaceText": value
            }
        }
        try:
            docs_service.documents().batchUpdate(
                documentId=doc_id,
                body={"requests": [request]}
            ).execute()
        except Exception as e:
            print(f"⚠️ Failed to replace {key} with '{value}': {e}")

    # --- 4. Export the updated Doc as PDF ---
    request = drive_service.files().export_media(fileId=doc_id, mimeType="application/pdf")
    pdf_buf = BytesIO()
    downloader = MediaIoBaseDownload(pdf_buf, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()

    # --- 5. Delete the temporary doc so Drive doesn’t fill up ---
    drive_service.files().delete(fileId=doc_id).execute()

    return pdf_buf.getvalue()
