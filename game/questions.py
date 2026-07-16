from dataclasses import dataclass
from typing import Optional


@dataclass
class Question:
    id: str
    prompt: str
    correct_answer: str
    explanation: str
    hint: Optional[str] = None


FOUNDATIONS_QUESTIONS = [
    Question(
        id="pk_pd_001",
        prompt=(
            "A patient starts lisinopril for hypertension.\n\n"
            "What is the difference between pharmacokinetics and pharmacodynamics,\n"
            "and which one best explains how lisinopril lowers blood pressure?"
        ),
        correct_answer=(
            "Pharmacokinetics is what the body does to the drug; "
            "pharmacodynamics is what the drug does to the body. "
            "Lisinopril lowering blood pressure is pharmacodynamics."
        ),
        explanation=(
            "Pharmacokinetics describes absorption, distribution, metabolism, and excretion.\n"
            "Pharmacodynamics describes the drug's mechanism and effect on the body.\n"
            "Lisinopril lowers blood pressure through ACE inhibition, which is a pharmacodynamic effect."
        ),
        hint="Think ADME versus drug effect.",
    ),
    Question(
        id="bioavailability_002",
        prompt=(
            "A drug has high bioavailability when administered orally.\n\n"
            "What does 'high bioavailability' mean, and which pharmacokinetic process does it primarily reflect?"
        ),
        correct_answer=(
            "High bioavailability means a large fraction of the oral dose reaches systemic circulation unchanged. "
            "It primarily reflects absorption and first-pass metabolism."
        ),
        explanation=(
            "Bioavailability is the fraction of the administered dose that reaches systemic circulation.\n"
            "Oral bioavailability is affected by absorption and first-pass metabolism."
        ),
        hint="Think: how much of the dose actually gets into the bloodstream?",
    ),
    Question(
        id="half_life_003",
        prompt=(
            "A medication has a half-life of 8 hours.\n\n"
            "What does half-life mean in pharmacokinetics, and why is it clinically important?"
        ),
        correct_answer=(
            "Half-life is the time it takes for the drug concentration in the body to decrease by 50%. "
            "It is important because it helps determine dosing interval, time to steady state, and time to washout."
        ),
        explanation=(
            "Half-life is a key pharmacokinetic parameter.\n"
            "It helps guide how often a drug is given and how long it takes to reach steady state or clear from the body."
        ),
        hint="Think about drug concentration over time.",
    ),
    Question(
        id="antagonist_004",
        prompt=(
            "A drug binds to a receptor and prevents the natural ligand from producing its effect.\n\n"
            "What type of drug interaction is this, and what does it do to the receptor?"
        ),
        correct_answer=(
            "This is receptor antagonism. The drug blocks the receptor and prevents activation by the natural ligand."
        ),
        explanation=(
            "An antagonist binds to a receptor but does not activate it.\n"
            "Instead, it blocks the receptor so the endogenous ligand cannot produce its effect."
        ),
        hint="Think: blocks without activating.",
    ),
    Question(
        id="therapeutic_index_005",
        prompt=(
            "A narrow therapeutic index drug requires close monitoring.\n\n"
            "What does 'narrow therapeutic index' mean, and why does it matter clinically?"
        ),
        correct_answer=(
            "A narrow therapeutic index means there is a small difference between the effective dose and the toxic dose. "
            "It matters because small changes in dose or concentration can cause toxicity or treatment failure."
        ),
        explanation=(
            "Drugs with a narrow therapeutic index need careful monitoring because the safe and effective range is small."
        ),
        hint="Think: safe dose range is small.",
    ),
]