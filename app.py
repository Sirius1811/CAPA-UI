import streamlit as st
import pandas as pd
import datetime as dt

from drive_helper import append_row, query_records, find_by_capa_no
from pdf_generator import generate_capa_pdf   # <-- use your new generator

st.set_page_config(page_title="CAPA Portal (New)", layout="wide")
st.title("CAPA Portal")
st.write("Please fill the CAPA form")

# Simple sidebar navigation
mode = st.sidebar.radio("Mode", ["New CAPA", "Search & Download"])


def now_iso():
    return dt.datetime.now().isoformat(sep=" ", timespec="seconds")


# -------------------- New CAPA Form --------------------
if mode == "New CAPA":
    with st.form("capa_form"):

        # --- Top section (Dept, Area, Date, CAPA No) ---
        st.markdown("### General Information")
        col1, col2 = st.columns(2)

        with col1:
            department = st.text_input("Department")
            date_of_incident = st.date_input("Date of Incident", value=None)
        with col2:
            area_section = st.text_input("Area / Section")
            capa_no = st.text_input("CAPA No (unique)", placeholder="CAPA-2025-001")

        st.markdown("---")

        # --- Problem description + Breakdown ---
        st.markdown("### Problem Description (what/where/when/how extensive?)")

        problem_what = st.text_input("What")
        problem_where = st.text_input("Where")
        problem_when = st.text_input("When")
        problem_extent = st.text_input("Extent")

        st.write("In Case of Breakdown: ")
        col1, col2 = st.columns(2)

        with col1:
            breakdown_from = st.text_input("Duration From (time) - e.g., 10:30")
            breakdown_to = st.text_input("Duration To (time) - e.g., 13:00")
        with col2:
            st.write("Request to Please Tick the duration of breakdown, which is applicable ")
            options = ("≥ 4 Hrs", "2 - 4 Hrs", "1 - 2 Hrs", "≤ 1 Hrs")
            option_to_key_map = {
                "≥ 4 Hrs": "A",
                "2 - 4 Hrs": "B",
                "1 - 2 Hrs": "C",
                "≤ 1 Hrs": "D"
            }
            duration = st.radio(
                "Breakdown Duration", 
                options,
                index = None,
                label_visibility="collapsed" 
            )
            selected_key = option_to_key_map.get(duration)

        st.markdown("### Responsible Team for Corrective/Preventive Actions")
        team_name = st.text_input("Team Name")
        col1, col2, col3 = st.columns(3)

        with col1:
            team_leader = st.text_input("Team Leader")
            member1 = st.text_input("Member 1")
            member2 = st.text_input("Member 2")
            member3 = st.text_input("Member 3")
            member4 = st.text_input("Member 4")
        with col2:
            role1 = st.text_input("Role 1")
            role2 = st.text_input("Role 2")
            role3 = st.text_input("Role 3")
            role4 = st.text_input("Role 4")
            role5 = st.text_input("Role 5")
        with col3:
            contact1 = st.text_input("Contact No. 1")
            contact2 = st.text_input("Contact No. 2")
            contact3 = st.text_input("Contact No. 3")
            contact4 = st.text_input("Contact No. 4")
            contact5 = st.text_input("Contact No. 5")

        st.markdown("### Correction/ Immediate Actions taken")
        immediate_actions = st.text_area("Actions taken", label_visibility="collapsed", height=80)
        immediate_timeframe = st.text_input("Time Frame")
        immediate_responsibility = st.text_input("Responsibility")

        st.markdown("### Root cause analysis - Analysis finding ")

        col1, col2 = st.columns(2)

        with col1:
            why1 = st.text_input("1st Why")
            why2 = st.text_input("2nd Why")
            why3 = st.text_input("3rd Why")
            why4 = st.text_input("4th Why")
            why5 = st.text_input("5th Why")
        with col2:
            st.write("The outcomes of 5 Why Analysis, which “Five (5) M’s” is applicable")
            m1 = st.checkbox("Material (M1)")
            m2 = st.checkbox("Man (M2)")
            m3 = st.checkbox("Machine (M3)")
            m4 = st.checkbox("Measure (M4)")
            m5 = st.checkbox("Method (M5)")

        conclusion = st.text_input("Conclusion(s)")

        st.markdown("---")

        st.markdown("### Recommended Corrective action(s)")
        corrective_actions = st.text_area("Corrective Actions", height=80)
        corrective_resp = st.text_input("Corrective Responsibility")
        corrective_target_date = st.date_input("Target date (Corrective)", value=None)
        corrective_impl_date = st.date_input("Date of implementation (Corrective)", value=None)

        st.markdown("### Recommended Preventive action(s)")
        preventive_actions = st.text_area("Preventive Actions", height=80)
        preventive_resp = st.text_input("Preventive Responsibility")
        preventive_target_date = st.date_input("Target date (Preventive)", value=None)
        preventive_impl_date = st.date_input("Date of implementation (Preventive)", value=None)

        st.markdown("### Detailed Implementation Plan")
        implementation_plan = st.text_area("Plan", label_visibility="collapsed")

        st.markdown("### Modified documents (Please Tick in the applicable document)")
        d1 = st.checkbox("MOC")
        d2 = st.checkbox("SOP / SMP")
        d3 = st.checkbox("Risk and Opportunity Register")
        d4 = st.checkbox("Register of Environmental Aspect Impact and OH & S Risks")
        d5 = st.checkbox("Training Need Identification")
        col1, col2 = st.columns([1, 2]) # Makes the text box column twice as wide

        with col1:
            d6 = st.checkbox("Others (Please Mention)")

        with col2:
            # This text_input is disabled unless the d6 checkbox is ticked
            others_text = st.text_input(
                "Specify Other Documents",
                label_visibility="collapsed",
                placeholder="Specify here..."
            )

        st.markdown("### Training Details (If any)")
        training_details = st.text_area("Training Details", label_visibility="collapsed")

        st.markdown("### Date of Implementation")
        date_of_implementation = st.date_input("Date of Implementation", value=None, label_visibility="collapsed")

        st.markdown("### Effectiveness evaluation of implemented Correction, Corrective Action / Preventive Action")
        effectiveness_evaluation = st.text_area("What is the activity to verify that the corrective actions have been effective (measurement, audit, study, assessment?")

        prepared_by = st.text_input("Prepared By (Name of Initiator)")
        reviewed_by = st.text_input("Reviewed By (Name of Reviewer)")
        approved_by = st.text_input("Approved By (Name of HOD)")

        submitted = st.form_submit_button("Save to Google Sheet")

    if submitted:
        if not capa_no.strip():
            st.error("CAPA No is required.")
        else:
            row = {
                "DEPARTMENT": department,
                "AREA_SECTION": area_section,
                "DATE_OF_INCIDENT": str(date_of_incident),
                "CAPA_NO": capa_no.strip(),
                "WHAT": problem_what,
                "WHERE": problem_where,
                "WHEN": problem_when,
                "EXTENT": problem_extent,
                "TIME1": breakdown_from,
                "TIME2": breakdown_to,
                "A":"YES" if selected_key == "A" else "",
                "B":"YES" if selected_key == "B" else "",
                "C":"YES" if selected_key == "C" else "",
                "D":"YES" if selected_key == "D" else "",
                "TEAM_NAME": team_name,
                "LEADER": team_leader,
                "MEM1": member1,
                "MEM2": member2,
                "MEM3": member3,
                "MEM4": member4,
                "R1": role1,
                "R2": role2,
                "R3": role3,
                "R4": role4,
                "R5": role5,
                "C1": contact1,
                "C2": contact2,
                "C3": contact3,
                "C4": contact4,
                "C5": contact5,
                "ACTIONS": immediate_actions,
                "TIME_FRAME": immediate_timeframe,
                "RESPONSIBILITY": immediate_responsibility,
                "WHY1": why1,
                "WHY2": why2,
                "WHY3": why3,
                "WHY4": why4,
                "WHY5": why5,
                "M1": "YES" if m1 else "",
                "M2": "YES" if m2 else "",
                "M3": "YES" if m3 else "",
                "M4": "YES" if m4 else "",
                "M5": "YES" if m5 else "",
                "CONCLUSION": conclusion,
                "C_ACTIONS": corrective_actions,
                "RES1": corrective_resp,
                "T1": str(corrective_target_date),
                "D1": str(corrective_impl_date),
                "P_ACTIONS": preventive_actions,
                "RES2": preventive_resp,
                "T2": str(preventive_target_date),
                "D2": str(preventive_impl_date),
                "PLAN": implementation_plan,
                "O1": "YES" if d1 else "",
                "O2": "YES" if d2 else "",
                "O3": "YES" if d3 else "",
                "O4": "YES" if d4 else "",
                "O5": "YES" if d5 else "",
                "OTHERS": others_text,
                "TRAINING_DETAILS": training_details,
                "DATE_IMPLE": str(date_of_implementation),
                "EFFECTIVENESS_EVAL": effectiveness_evaluation,
                "INITIATOR": prepared_by,
                "REVIEWER": reviewed_by,
                "HOD": approved_by,
            }
            try:
                append_row(row)
                st.success(f"Saved CAPA {capa_no} to Google Sheet ✅")
            except Exception as e:
                st.error(f"Failed to save to Google Sheet: {e}")


# -------------------- Search & Download --------------------
else:
    st.header("Search & Download CAPA PDF")

    col1, col2, col3 = st.columns(3)
    with col1:
        search_capa = st.text_input("CAPA No")
    with col2:
        search_department = st.text_input("Department")
    with col3:
        search_area = st.text_input("Area / Section")

    col4, col5 = st.columns(2)
    with col4:
        start_date = st.date_input("Start Date", value=None)
    with col5:
        end_date = st.date_input("End Date", value=None)

    if st.button("Search"):
        try:
            df = query_records(
                department=search_department,
                area=search_area,
                start_date=(str(start_date) if start_date else None),
                end_date=(str(end_date) if end_date else None),
            )
            if search_capa:
                df = df[df["CAPA_NO"].astype(str).str.contains(search_capa, case=False, na=False)]
            if df.empty:
                st.info("No results.")
            else:
                st.write(f"Found {len(df)} records")
                df_display = df[["CAPA_NO", "DEPARTMENT", "AREA_SECTION", "DATE_OF_INCIDENT"]].copy()
                df_display["DATE_OF_INCIDENT"] = pd.to_datetime(
                    df_display["DATE_OF_INCIDENT"], errors="coerce"
                ).dt.date
                st.dataframe(df_display)

                for _, r in df.iterrows():
                    st.markdown("---")
                    st.write(
                        f"**CAPA:** {r['CAPA_NO']} — Department: {r['DEPARTMENT']} — Area: {r['AREA_SECTION']} — Incident: {r['DATE_OF_INCIDENT']}"
                    )

                    record = find_by_capa_no(r["CAPA_NO"])
                    if not record:
                        st.error("Could not read this CAPA row.")
                        continue

                    pdf_bytes = generate_capa_pdf(record)

                    st.download_button(
                        label=f"📥 Download PDF — {r['CAPA_NO']}",
                        data=pdf_bytes,
                        file_name=f"{r['CAPA_NO']}.pdf",
                        mime="application/pdf",
                        key=f"download_{r['CAPA_NO']}"
                    )

        except Exception as e:
            st.error(f"Search failed: {e}")
