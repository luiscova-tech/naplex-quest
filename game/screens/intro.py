import streamlit as st

from game.dialogue import INTRO_DIALOGUE
from game.regions import FOUNDATIONS_VILLAGE
from game.save_manager import save_player


def render_intro(player):
    """Render the introduction and prologue."""

    st.markdown(
        """
        ### Prologue

        The **Book of Therapeutics** has been shattered.

        Across the Kingdom of **Pharmacia**, knowledge is fading and the Shadow Alchemist grows stronger.
        Only an Apprentice Pharmacist can restore the lost chapters and bring balance back to the realm.
        """
    )

    current = INTRO_DIALOGUE[st.session_state.dialogue_index]

    st.subheader(current.speaker)
    st.write(current.text)

    col1, col2 = st.columns(2)

    with col1:
        if st.session_state.dialogue_index > 0:
            if st.button("⬅ Previous"):
                st.session_state.dialogue_index -= 1
                st.rerun()

    with col2:
        if st.session_state.dialogue_index < len(INTRO_DIALOGUE) - 1:
            if st.button("Next ➜"):
                st.session_state.dialogue_index += 1
                st.rerun()
        else:
            if st.button("🚪 Enter Foundations Village"):
                player.region = FOUNDATIONS_VILLAGE.name
                st.session_state.in_foundations_village = True
                st.session_state.selected_location = "Village Square"
                save_player(player)
                st.rerun()