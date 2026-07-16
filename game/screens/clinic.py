import streamlit as st


def render_clinic(encounter_manager):
    """Render the Healer's Clinic encounter."""

    if not encounter_manager.has_active_encounter():
        encounter_manager.start_encounter(
            encounter_id="clinic_001",
            patient_name="Elias Thornwood",
            chief_complaint="Persistent cough and fever",
        )

    encounter = encounter_manager.get_encounter()

    st.subheader("🏥 Patient Encounter")
    st.write(f"**Patient:** {encounter.patient_name}")
    st.write(f"**Chief Complaint:** {encounter.chief_complaint}")
    st.write(
        f"**Current Stage:** "
        f"{encounter.current_stage.name.replace('_', ' ').title()}"
    )

    st.info(encounter.get_stage_text())

    if encounter.current_stage.name == "INTRODUCTION":

        if st.button("Speak with Patient"):
            encounter_manager.advance()
            st.rerun()

    elif encounter.current_stage.name == "HISTORY":

        st.write("### What would you like to ask first?")

        history_choice = st.radio(
            "Choose one:",
            [
                "How long have you had these symptoms?",
                "Do you have any medication allergies?",
                "Are you taking any medications?",
            ],
            key="history_choice",
        )

        if st.button("Ask Question"):
            st.success(f"You asked: {history_choice}")
            encounter_manager.advance()
            st.rerun()

    elif not encounter.is_complete():

        if st.button("Continue Encounter"):
            encounter_manager.advance()
            st.rerun()

    else:
        st.success("Patient encounter complete! (Rewards coming soon.)")