import streamlit as st

from game.questions import FOUNDATIONS_QUESTIONS
from game.save_manager import save_player


def render_sidebar(player, question_bank, chapter_mastery_count):
    """Render the application's sidebar."""

    with st.sidebar:
        st.header("⚕️ Apprentice Pharmacist")

        player.name = st.text_input("Name", value=player.name)

        st.divider()

        st.selectbox(
            "Mode",
            ["Study Mode", "Exam Mode"],
            key="game_mode",
            help="Study Mode gives hints and coaching. Exam Mode behaves like a test.",
        )

        st.write(f"**Level:** {player.level}")
        st.write(f"**XP:** {player.xp}")
        st.write(f"**Gold:** {player.gold}")
        st.write(f"**Confidence:** {player.clinical_confidence}")
        st.write(f"**Region:** {player.region}")

        st.divider()

        mastered_count = chapter_mastery_count(question_bank)
        chapter_complete = mastered_count == len(FOUNDATIONS_QUESTIONS)

        st.session_state.chapter_mastered = chapter_complete

        st.write("### Chapter Mastery")

        mastery_status = (
            "✅ Mastered"
            if chapter_complete
            else "🟡 In Progress"
        )

        st.write(mastery_status)

        st.progress(
            mastered_count / max(len(FOUNDATIONS_QUESTIONS), 1)
        )

        st.caption(
            f"Mastered {mastered_count} / {len(FOUNDATIONS_QUESTIONS)} challenges"
        )

        if player.badges:
            st.write("### Badges")

            for badge in player.badges:
                st.write(f"🏅 {badge}")

        st.divider()

        if st.button("💾 Save Progress"):
            save_player(player)
            st.success("Progress saved!")