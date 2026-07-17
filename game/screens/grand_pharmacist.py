import streamlit as st


def render_grand_pharmacist_header(chapter_mastered: bool):
    """Render the quest introduction and chapter status."""

    if chapter_mastered:
        st.markdown(
            """
            ### ✨ The First Chapter Has Been Restored

            The floating page glows bright gold and returns to the **Book of Therapeutics**.

            The Grand Pharmacist smiles.

            > "Excellent. Pharmacia remembers."
            """
        )

        st.info(
            "The chapter is complete. More regions and quests will unlock as the game expands."
        )

    else:
        st.markdown(
            """
            ### Quest Log

            **Quest 1: Restore the First Lost Chapter**

            A villager reports that the Shadow Alchemist has clouded the meaning of
            *pharmacokinetics* and *pharmacodynamics*.

            Your task is to restore the chapter by answering the Grand Pharmacist's challenge.
            """
        )

        st.subheader("Your First Quest")

        st.write(
            "A glowing page from the Book of Therapeutics floats before you. "
            "Answer carefully to restore its light."
        )


def render_study_question_header():
    """Render the Study Mode section heading."""
    st.markdown("### Challenge of the Grand Pharmacist")


def render_exam_question_header():
    """Render the Exam Mode section heading."""
    st.write("### Exam Challenge")
    st.write("Choose the best answer. No hints. No coaching until after grading.")