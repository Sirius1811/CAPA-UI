# pdf_generator.py
from io import BytesIO
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2.service_account import Credentials as ServiceAccountCredentials
import os

# --- Service account setup using service_account.json ---
SCOPES = ["https://www.googleapis.com/auth/documents", "https://www.googleapis.com/auth/drive"]
DOC_TEMPLATE_ID = "159fhtUNIAuMSqY0AiCXy9qhzBqInHqTf"  # your Google Doc template ID

def get_creds():
    sa_file = os.path.join(os.getcwd(), "service_account.json")
    if not os.path.exists(sa_file):
        raise RuntimeError("service_account.json not found in project root")
    creds = ServiceAccountCredentials.from_service_account_file(sa_file, scopes=SCOPES)
    return creds

creds = get_creds()
docs_service = build("docs", "v1", credentials=creds)
drive_service = build("drive", "v3", credentials=creds)


def _tick(val: str) -> str:
    """Return a checkmark if 'YES', else empty string."""
    return "✔" if str(val).strip().upper() == "YES" else ""


def generate_capa_pdf(row: dict) -> bytes:
    """Fill the Google Docs CAPA template with row values and return PDF bytes."""

    copy_title = f"CAPA_{row.get('CAPA_NO', 'TEMP')}"
    body = {"name": copy_title}
    copied_file = drive_service.files().copy(fileId=DOC_TEMPLATE_ID, body=body).execute()
    doc_id = copied_file.get("id")

    replacements = {}
    for k, v in row.items():
        if k in ["A", "B", "C", "D", "M1", "M2", "M3", "M4", "M5", "O1", "O2", "O3", "O4", "O5"]:
            replacements[k] = _tick(v)
        else:
            replacements[k] = str(v) if v else ""

    requests = []
    for key, value in replacements.items():
        requests.append({
            "replaceAllText": {
                "containsText": {"text": f"{{{{{key}}}}}", "matchCase": True},
                "replaceText": value
            }
        })
    docs_service.documents().batchUpdate(documentId=doc_id, body={"requests": requests}).execute()

    request = drive_service.files().export_media(fileId=doc_id, mimeType="application/pdf")
    pdf_buf = BytesIO()
    downloader = MediaIoBaseDownload(pdf_buf, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()

    drive_service.files().delete(fileId=doc_id).execute()

    return pdf_buf.getvalue()
