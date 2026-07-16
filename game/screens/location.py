import streamlit as st


def render_location(selected):
    """Render a generic Foundations Village location."""

    st.info(
        f"You found the {selected.name}. "
        "This location will soon hold its own quests and secrets."
    )

    descriptions = {
        "Library": (
            "Ancient books whisper of pharmacology, calculations, "
            "and clinical reasoning."
        ),
        "Apothecary": (
            "Shelves of tinctures and tonics line the walls. "
            "Preparation and precision matter here."
        ),
        "Village Square": (
            "The heart of Foundations Village. "
            "Travelers gather here before continuing their journey."
        ),
    }

    if selected.name in descriptions:
        st.write(descriptions[selected.name])