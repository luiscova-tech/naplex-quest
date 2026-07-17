import re
import streamlit as st

from game.screens.sidebar import render_sidebar

from game.player import Player
from game.save_manager import load_player, save_player
from game.dialogue import INTRO_DIALOGUE
from game.regions import FOUNDATIONS_VILLAGE
from game.questions import FOUNDATIONS_QUESTIONS
from game.question_engine import QuestionBank
from game.village import FOUNDATIONS_LOCATIONS
from game.encounter_manager import EncounterManager
from game.screens.intro import render_intro
from game.screens.clinic import render_clinic
from game.screens.location import render_location

from game.screens.grand_pharmacist import (
    render_exam_question_header,
    render_grand_pharmacist_header,
    render_study_question_header,
)
st.set_page_config(
    page_title="NAPLEX Quest",
    page_icon="⚕️",
    layout="wide"
)

# ---------- Session State ----------

if "player" not in st.session_state:
    st.session_state.player = load_player()

if "dialogue_index" not in st.session_state:
    st.session_state.dialogue_index = 0

if "in_foundations_village" not in st.session_state:
    st.session_state.in_foundations_village = False

if "game_mode" not in st.session_state:
    st.session_state.game_mode = "Study Mode"

if "selected_location" not in st.session_state:
    st.session_state.selected_location = "Village Square"

if "awaiting_feedback" not in st.session_state:
    st.session_state.awaiting_feedback = False

if "question_outcome" not in st.session_state:
    st.session_state.question_outcome = None  # "correct" or "incorrect"

if "last_feedback" not in st.session_state:
    st.session_state.last_feedback = ""

if "chapter_mastered" not in st.session_state:
    st.session_state.chapter_mastered = False

if "current_question_id" not in st.session_state:
    st.session_state.current_question_id = None

if "question_bank" not in st.session_state:
    st.session_state.question_bank = QuestionBank(questions=FOUNDATIONS_QUESTIONS)

if "encounter_manager" not in st.session_state:
    st.session_state.encounter_manager = EncounterManager()

player: Player = st.session_state.player
question_bank: QuestionBank = st.session_state.question_bank
encounter_manager: EncounterManager = st.session_state.encounter_manager


# ---------- Helpers ----------

def normalize_text(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9\s]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text


def grade_study_answer(user_answer: str) -> bool:
    normalized = normalize_text(user_answer)

    has_pk = "pharmacokinetics" in normalized or "pk" in normalized or "adme" in normalized
    has_pd = "pharmacodynamics" in normalized or "pd" in normalized or "mechanism" in normalized
    has_body_drug = "body does to the drug" in normalized or "what the body does to the drug" in normalized
    has_drug_body = "drug does to the body" in normalized or "what the drug does to the body" in normalized
    has_lisinopril_pd = "lisinopril" in normalized and ("pharmacodynamics" in normalized or "pd" in normalized)

    return has_pk and has_pd and has_body_drug and has_drug_body and has_lisinopril_pd


def get_location(name: str):
    for location in FOUNDATIONS_LOCATIONS:
        if location.name == name:
            return location
    return None


def get_question_by_id(question_id: str):
    for q in FOUNDATIONS_QUESTIONS:
        if q.id == question_id:
            return q
    return None


def choose_next_question(bank: QuestionBank):
    """
    Priority:
    1) Unseen questions
    2) Questions answered incorrectly
    3) Least-correct review questions
    """
    if not bank.questions:
        return None

    stats_map = {q.id: bank._get_stats(q.id) for q in bank.questions}  # intentional internal access

    unseen = [q for q in bank.questions if stats_map[q.id].times_seen == 0]
    if unseen:
        return unseen[0]

    incorrect = [q for q in bank.questions if stats_map[q.id].times_incorrect > 0 and stats_map[q.id].times_correct == 0]
    if incorrect:
        return sorted(
            incorrect,
            key=lambda q: (-stats_map[q.id].times_incorrect, stats_map[q.id].times_seen)
        )[0]

    # Review weakest first
    return sorted(
        bank.questions,
        key=lambda q: (stats_map[q.id].times_correct - stats_map[q.id].times_incorrect, stats_map[q.id].times_seen)
    )[0]


def chapter_mastery_count(bank: QuestionBank) -> int:
    return sum(1 for q in bank.questions if bank._get_stats(q.id).times_correct > 0)


# ---------- Exam Mode Data ----------

EXAM_QUESTION_CHOICES = {
    "pk_pd_001": {
        "correct": "B",
        "choices": {
            "A": "Pharmacokinetics is what the drug does to the body; pharmacodynamics is what the body does to the drug.",
            "B": "Pharmacokinetics is what the body does to the drug; pharmacodynamics is what the drug does to the body.",
            "C": "Pharmacokinetics and pharmacodynamics mean the same thing.",
            "D": "Pharmacokinetics is only metabolism; pharmacodynamics is only absorption.",
        },
    },
    "bioavailability_002": {
        "correct": "A",
        "choices": {
            "A": "A large fraction of the oral dose reaches systemic circulation unchanged; it reflects absorption and first-pass metabolism.",
            "B": "The drug is eliminated completely by the kidneys.",
            "C": "The drug has a very short half-life.",
            "D": "The drug binds strongly to plasma proteins.",
        },
    },
    "half_life_003": {
        "correct": "C",
        "choices": {
            "A": "The time it takes for the drug to be completely removed from the body.",
            "B": "The time it takes for the drug concentration to double.",
            "C": "The time it takes for the drug concentration to decrease by 50%.",
            "D": "The time it takes for the drug to reach peak effect.",
        },
    },
    "antagonist_004": {
        "correct": "D",
        "choices": {
            "A": "Agonism; the drug activates the receptor and increases the response.",
            "B": "Partial agonism; the drug activates the receptor weakly.",
            "C": "Inverse agonism; the drug increases receptor activity.",
            "D": "Antagonism; the drug blocks the receptor without activating it.",
        },
    },
    "therapeutic_index_005": {
        "correct": "B",
        "choices": {
            "A": "The drug is only available by injection.",
            "B": "There is a small difference between the effective dose and toxic dose.",
            "C": "The drug works only in the liver.",
            "D": "The drug cannot be monitored.",
        },
    },
}

render_sidebar(
    player=player,
    question_bank=question_bank,
    chapter_mastery_count=chapter_mastery_count,
)

# ---------- Main ----------

st.title("⚕️ NAPLEX Quest")
st.caption("Recover the lost Book of Therapeutics and restore knowledge to the Kingdom of Pharmacia.")

if not st.session_state.in_foundations_village:
    render_intro(player)

else:
    st.header("🏰 Foundations Village")
    st.write(FOUNDATIONS_VILLAGE.description)
    st.success(f"You are now with {FOUNDATIONS_VILLAGE.guardian}.")

    st.markdown("### Explore Foundations Village")

    col1, col2 = st.columns(2)

    for i, location in enumerate(FOUNDATIONS_LOCATIONS):
        target_col = col1 if i % 2 == 0 else col2
        with target_col:
            if st.button(
                f"{location.icon} {location.name}",
                key=f"loc_{location.name}",
                use_container_width=True
            ):
                st.session_state.selected_location = location.name
                st.rerun()

    selected = get_location(st.session_state.selected_location)

    if selected:
        st.divider()
        st.subheader(f"{selected.icon} {selected.name}")
        st.write(selected.description)

        if selected.name == "Grand Pharmacist":
            
                if st.session_state.current_question_id is None:
                    next_q = choose_next_question(question_bank)
                    if next_q is not None:
                        st.session_state.current_question_id = next_q.id

                q = get_question_by_id(st.session_state.current_question_id)

                if q is None:
                    st.success("You have restored every challenge in this chapter.")
                    st.session_state.chapter_mastered = True
                    save_player(player)
                    st.rerun()

                render_study_question_header()

                if st.session_state.game_mode == "Study Mode":
                    st.write(q.prompt)

                    if q.hint:
                        with st.expander("Need a hint?"):
                            st.write(q.hint)

                    if not st.session_state.awaiting_feedback:
                        user_answer = st.text_area("Your answer", key=f"study_answer_{q.id}")

                        if st.button("Submit Answer"):
                            is_correct = grade_study_answer(user_answer)
                            question_bank.record_result(q.id, is_correct)

                            if is_correct:
                                player.add_xp(25)
                                player.add_gold(5)
                                player.complete_quest(q.id)
                                save_player(player)

                                st.session_state.last_feedback = (
                                    "✅ **The chapter begins to glow.**\n\n"
                                    "A warm light rises from the page and the Grand Pharmacist nods.\n\n"
                                    f"**Teaching:** {q.explanation}\n\n"
                                    "**Key takeaway:** PK = what the body does to the drug; "
                                    "PD = what the drug does to the body."
                                )
                                st.session_state.question_outcome = "correct"
                                st.session_state.awaiting_feedback = True
                                st.success("The lost knowledge returns to the Book of Therapeutics!")
                                st.rerun()
                            else:
                                player.adjust_confidence(-5)
                                save_player(player)

                                st.session_state.last_feedback = (
                                    "❌ **The Shadow Alchemist resists.**\n\n"
                                    f"**Correct answer:** {q.correct_answer}\n\n"
                                    f"**Teaching:** {q.explanation}\n\n"
                                    "**Hint:** Think ADME versus drug effect."
                                )
                                st.session_state.question_outcome = "incorrect"
                                st.session_state.awaiting_feedback = True
                                st.error("The chapter remains dim. Review the explanation below.")
                                st.rerun()

                    else:
                        st.markdown(st.session_state.last_feedback)

                        if st.session_state.question_outcome == "correct":
                            if st.button("Continue to the Next Challenge"):
                                st.session_state.awaiting_feedback = False
                                st.session_state.question_outcome = None
                                st.session_state.last_feedback = ""
                                st.session_state.current_question_id = None

                                mastered_count = chapter_mastery_count(question_bank)
                                if mastered_count == len(FOUNDATIONS_QUESTIONS):
                                    st.session_state.chapter_mastered = True
                                    player.add_xp(25)
                                    player.add_gold(10)
                                    save_player(player)

                                st.rerun()
                        else:
                            if st.button("Try Again"):
                                st.session_state.awaiting_feedback = False
                                st.session_state.question_outcome = None
                                st.session_state.last_feedback = ""
                                st.rerun()

                else:
                    render_exam_question_header()

                    options = EXAM_QUESTION_CHOICES[q.id]["choices"]
                    correct_letter = EXAM_QUESTION_CHOICES[q.id]["correct"]

                    st.write(q.prompt)

                    selected_choice = st.radio(
                        "Answer choices",
                        list(options.keys()),
                        format_func=lambda k: f"{k}. {options[k]}",
                        horizontal=False,
                        key=f"exam_choice_{q.id}"
                    )

                    if not st.session_state.awaiting_feedback:
                        if st.button("Submit Exam Answer"):
                            is_correct = selected_choice == correct_letter
                            question_bank.record_result(q.id, is_correct)

                            if is_correct:
                                player.add_xp(25)
                                player.add_gold(5)
                                player.complete_quest(q.id)
                                save_player(player)

                                st.session_state.last_feedback = (
                                    "✅ **Correct.**\n\n"
                                    f"**Teaching:** {q.explanation}\n\n"
                                    "**Key takeaway:** PK = what the body does to the drug; "
                                    "PD = what the drug does to the body."
                                )
                                st.session_state.question_outcome = "correct"
                                st.session_state.awaiting_feedback = True
                                st.success("Correct! The chapter has been restored.")
                                st.rerun()
                            else:
                                player.adjust_confidence(-5)
                                save_player(player)

                                st.session_state.last_feedback = (
                                    "❌ **Incorrect.**\n\n"
                                    f"**Correct answer:** {correct_letter}. {options[correct_letter]}\n\n"
                                    f"**Teaching:** {q.explanation}"
                                )
                                st.session_state.question_outcome = "incorrect"
                                st.session_state.awaiting_feedback = True
                                st.error("Incorrect. Review the explanation below.")
                                st.rerun()

                    else:
                        st.markdown(st.session_state.last_feedback)

                        if st.session_state.question_outcome == "correct":
                            if st.button("Continue to the Next Challenge"):
                                st.session_state.awaiting_feedback = False
                                st.session_state.question_outcome = None
                                st.session_state.last_feedback = ""
                                st.session_state.current_question_id = None

                                mastered_count = chapter_mastery_count(question_bank)
                                if mastered_count == len(FOUNDATIONS_QUESTIONS):
                                    st.session_state.chapter_mastered = True
                                    player.add_xp(25)
                                    player.add_gold(10)
                                    save_player(player)

                                st.rerun()
                        else:
                            if st.button("Try Again"):
                                st.session_state.awaiting_feedback = False
                                st.session_state.question_outcome = None
                                st.session_state.last_feedback = ""
                                st.rerun()

        elif selected.name == "Healer's Clinic":
            render_clinic(encounter_manager)

        else:
            render_location(selected)

            if selected.name == "Library":
                st.write("Ancient books whisper of pharmacology, calculations, and clinical reasoning.")
            elif selected.name == "Apothecary":
                st.write("Shelves of tinctures and tonics line the walls. Preparation and precision matter here.")
            elif selected.name == "Village Square":
                st.write("The heart of Foundations Village. Travelers gather here before continuing their journey.")
    else:
        st.info("Choose a location in Foundations Village to explore the realm.")