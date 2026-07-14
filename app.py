import streamlit as st

from game.player import Player
from game.save_manager import load_player, save_player

st.set_page_config(
    page_title="NAPLEX Quest",
    page_icon="⚕️",
    layout="wide"
)

if "player" not in st.session_state:
    st.session_state.player = load_player()

player: Player = st.session_state.player

st.title("⚕️ NAPLEX Quest")
st.subheader("An Educational RPG for NAPLEX Mastery")

st.write(
    """
Welcome to **NAPLEX Quest**!

This is the beginning of your journey through the Kingdom of **Pharmacia**.

Your mission is to recover the lost **Book of Therapeutics**, master every region of pharmacy,
and ultimately become the **Guardian Pharmacist of Pharmacia**.

🚧 Version 0.1 is under development.
"""
)

with st.sidebar:
    st.header("Player Profile")
    player.name = st.text_input("Name", value=player.name)
    st.write(f"**Level:** {player.level}")
    st.write(f"**XP:** {player.xp}")
    st.write(f"**Gold:** {player.gold}")
    st.write(f"**Clinical Confidence:** {player.clinical_confidence}")
    st.write(f"**Region:** {player.region}")
    st.write(f"**Badges:** {', '.join(player.badges) if player.badges else 'None'}")

    if st.button("Save Progress"):
        save_player(player)
        st.success("Progress saved!")

if st.button("Begin Your Adventure"):
    player.region = "Foundations Village"
    save_player(player)
    st.success("Welcome, Apprentice Pharmacist! Your journey begins in Foundations Village...")