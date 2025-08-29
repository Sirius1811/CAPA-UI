import os
import pickle
import tempfile
from typing import Dict, List, Optional
import datetime as dt

import gspread
import pandas as pd
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials as ServiceAccountCredentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials as OAuthCredentials

# Scopes required for Google Sheets (and ability to create spreadsheets)
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
]

SPREADSHEET_NAME = "CAPA_PORTAL_INDEX"  # spreadsheet name (created if absent)
WORKSHEET_NAME = "CAPA"  # worksheet/tab name

# Column order used in the sheet (keeps consistent)
SHEET_COLUMNS = [
    "DEPARTMENT",
    "AREA_SECTION",
    "DATE_OF_INCIDENT",
    "CAPA_NO",
    "WHAT",
    "WHERE",
    "WHEN",
    "EXTENT",
    "TIME1",
    "TIME2",
    "A",
    "B",
    "C",
    "D",
    "TEAM_NAME",
    "LEADER",
    "MEM1",
    "MEM2",
    "MEM3",
    "MEM4",
    "R1",
    "R2",
    "R3",
    "R4",
    "R5",
    "C1",
    "C2",
    "C3",
    "C4",
    "C5",
    "ACTIONS",
    "TIME_FRAME",
    "RESPONSIBILITY",
    "WHY1",
    "WHY2",
    "WHY3",
    "WHY4",
    "WHY5",
    "M1",
    "M2",
    "M3",
    "M4",
    "M5",
    "CONCLUSION",
    "C_ACTIONS",
    "RES1",
    "T1",
    "D1",
    "P_ACTIONS",
    "RES2",
    "T2",
    "D2",
    "PLAN",
    "O1",
    "O2",
    "O3",
    "O4",
    "O5",
    "OTHERS",
    "TRAINING_DETAILS",
    "DATE_IMPLE",
    "EFFECTIVENESS_EVAL",
    "INITIATOR",
    "REVIEWER",
    "HOD",
]


def _auth_with_service_account(sa_path: str):
    creds = ServiceAccountCredentials.from_service_account_file(sa_path, scopes=SCOPES)
    client = gspread.authorize(creds)
    return client


def _auth_with_oauth(credentials_path: str, token_path: str = "token.pickle"):
    creds = None
    if os.path.exists(token_path):
        with open(token_path, "rb") as f:
            creds = pickle.load(f)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(token_path, "wb") as token:
            pickle.dump(creds, token)
    client = gspread.authorize(creds)
    return client


def init_gspread_client():
    """
    Tries to auth using service_account.json first (recommended for server),
    else falls back to credentials.json + local OAuth flow (interactive).
    """
    cwd = os.getcwd()
    sa_file = os.path.join(cwd, "service_account.json")
    oauth_file = os.path.join(cwd, "credentials.json")

    if os.path.exists(sa_file):
        return _auth_with_service_account(sa_file)
    elif os.path.exists(oauth_file):
        return _auth_with_oauth(oauth_file)
    else:
        raise RuntimeError(
            "No credentials found. Place service_account.json (preferred) or credentials.json in project root."
        )


def _ensure_spreadsheet_and_worksheet(client: gspread.Client):
    # Open spreadsheet if exists; else create
    try:
        sh = client.open(SPREADSHEET_NAME)
    except gspread.SpreadsheetNotFound:
        sh = client.create(SPREADSHEET_NAME)
        # If using service account, you may need to share the sheet with your user email to see it in Drive.
    # Try to open worksheet tab
    try:
        ws = sh.worksheet(WORKSHEET_NAME)
    except gspread.WorksheetNotFound:
        ws = sh.add_worksheet(title=WORKSHEET_NAME, rows="2000", cols=str(len(SHEET_COLUMNS)))
        # Write header row
        ws.append_row(SHEET_COLUMNS)
    return sh, ws


def append_row(data: Dict):
    """
    Insert a row into the Google Sheet. 'data' is a dict with keys matching SHEET_COLUMNS (case-insensitive).
    Missing columns will be left blank. Extra keys are ignored.
    """
    client = init_gspread_client()
    sh, ws = _ensure_spreadsheet_and_worksheet(client)

    # Normalize keys and produce row in correct order
    row = []
    for col in SHEET_COLUMNS:
        v = data.get(col) or data.get(col.lower()) or data.get(col.title()) or ""
        # if it's a datetime, convert to ISO date
        if isinstance(v, (dt.date, dt.datetime)):
            v = v.isoformat()
        row.append(str(v))
    ws.append_row(row)


def _sheet_to_dataframe():
    client = init_gspread_client()
    sh, ws = _ensure_spreadsheet_and_worksheet(client)
    records = ws.get_all_records()
    if not records:
        return pd.DataFrame(columns=SHEET_COLUMNS)
    df = pd.DataFrame(records)
    # Ensure columns exist
    for c in SHEET_COLUMNS:
        if c not in df.columns:
            df[c] = ""
    # Parse date column if present
    try:
        df["DATE_OF_INCIDENT"] = pd.to_datetime(df["DATE_OF_INCIDENT"], errors="coerce")
    except Exception:
        pass
    return df


def get_all_records() -> pd.DataFrame:
    return _sheet_to_dataframe()


def find_by_capa_no(capa_no: str) -> Optional[Dict]:
    df = _sheet_to_dataframe()
    if df.empty:
        return None
    row = df[df["CAPA_NO"].astype(str).str.strip().str.lower() == str(capa_no).strip().lower()]
    if row.empty:
        return None
    # return first match as dict (with original column names)
    return row.iloc[0].to_dict()


def query_records(department: Optional[str] = None, area: Optional[str] = None,
                  start_date: Optional[str] = None, end_date: Optional[str] = None) -> pd.DataFrame:
    df = _sheet_to_dataframe()
    if df.empty:
        return df
    res = df.copy()
    if department:
        res = res[res["DEPARTMENT"].astype(str).str.contains(department, case=False, na=False)]
    if area:
        res = res[res["AREA_SECTION"].astype(str).str.contains(area, case=False, na=False)]
    if start_date:
        sd = pd.to_datetime(start_date, errors="coerce")
        if not pd.isna(sd):
            res = res[res["DATE_OF_INCIDENT"] >= sd]
    if end_date:
        ed = pd.to_datetime(end_date, errors="coerce")
        if not pd.isna(ed):
            # include that day
            res = res[res["DATE_OF_INCIDENT"] <= (ed + pd.Timedelta(days=1))]
    return res
