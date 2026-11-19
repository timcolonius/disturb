"""Site content for the DISTURB website.

Edit this file to change the Home page text, then run `make site` (or
`make serve` to preview). Team, Publications and Positions come from the
Google Sheet instead (see sheet_data.py). Text fields may contain simple HTML
(<em>, <sup>, <a href=...>).
"""

PROJECT   = "DISTURB"
TAGLINE   = "Digital Simulation Twins for Turbulence"
MOTTO     = "See turbulence fully. Predict it. Control it."
GRANT     = "ERC Synergy Grant"
PERIOD    = "2027–2033"
GA        = "101307825"
SITES     = "Institut Pprime (CNRS) · Caltech · Sapienza"
CONTACT_EMAIL = ""   # e.g. a project mailbox; left blank → contact via PI pages

EU_DISCLAIMER = (
    "Funded by the European Union (ERC, DISTURB, 101307825). Views and opinions "
    "expressed are however those of the author(s) only and do not necessarily "
    "reflect those of the European Union or the European Research Council "
    "Executive Agency. Neither the European Union nor the granting authority "
    "can be held responsible for them."
)

HERO_TITLE = "A cyber-physical laboratory for turbulence"
HERO_TEXT = (
    "Experiments, simulations and models exchanging self-correcting information "
    "about the same flow, through a hierarchy of interacting digital twins, for "
    "a more complete and less uncertain observation of turbulence."
)

KEY_FIGURES = [
    ("€9.9 M", "ERC funding"),
    ("72", "months"),
    ("9", "PhD students"),
    ("8", "post-docs"),
    ("3", "engineers"),
]

CHALLENGE_TEXT = (
    "From aircraft and fusion reactors to blood flow and climate, turbulence "
    "limits what we can predict, optimise and control. Its vast range of "
    "interacting scales, its stochastic behaviour and its chaotic sensitivity "
    "put it beyond the reach of experiment, simulation or modelling taken "
    "separately."
)
CHALLENGES = [
    ("Enormous dimensionality", "The scale range grows as Re<sup>3/4</sup> along each of the three spatial dimensions."),
    ("Nonlinearity", "Triadic interactions couple every scale to every other."),
    ("Stochastic behaviour", "Only statistics repeat; every realisation is different."),
    ("Chaotic sensitivity", "Tiny uncertainties grow until forecasts part from reality."),
]

PILLARS = [
    dict(name="Experiment", style="solid", image="exp.jpg",
         text="Field measurement is the norm: time-resolved and tomographic PIV, "
              "particle tracking velocimetry, schlieren imaging, kilo-channel "
              "pressure-sensing arrays.",
         limits=[("Uncertainty", "the smallest scales stay out of reach; noise is always present."),
                 ("Coverage", "no simultaneous, time-resolved measurement of all variables in a volume."),
                 ("Latency", "transfer and processing delay analysis.")]),
    dict(name="Simulation", style="dashed", image="sim.jpg",
         text="DNS and LES on GPU-accelerated supercomputers are narrowing the "
              "Reynolds-number gap with real applications.",
         limits=[("Uncertainty", "initial and boundary conditions are never fully known."),
                 ("Scalability", "memory-bound on GPUs; DNS remains slow and offline."),
                 ("Data deluge", "petabytes of data, most of it never used.")]),
    dict(name="Modelling", style="dotted", image="model.jpg",
         text="Data assimilation transformed weather prediction; reduced-order "
              "models make it fast enough to forecast.",
         limits=[("Forecast latency", "real time puts a severe ceiling on model fidelity."),
                 ("Perfect-model assumption", "unrealistic for high-Reynolds-number turbulence."),
                 ("Untested at scale", "mostly demonstrated on simplified flows.")]),
]

SYNERGY_TEXT = (
    "State-of-the-art data assimilation couples the pillars so that each "
    "corrects the others: measurement sparsity and noise are compensated by "
    "numerical precision, computational simplifications are corrected by "
    "experimental data, and model deficiencies are constrained by both."
)
TWINS = [
    ("DT1", "Fidelity", "high-resolution, offline",
     "Exascale simulation synchronised with high-resolution measurements: "
     "reconstructs what experiments cannot measure and what simulations cannot know."),
    ("DT2", "Agility", "reduced-order, offline",
     "Reduced-order twins distilled from DT1: reveal mechanisms, quantify "
     "uncertainty and the trade-off between cost and fidelity."),
    ("DT3", "Action", "on the fly",
     "A real-time twin synchronised with the experiment: tracks the flow, "
     "forecasts rare events and regime changes, and drives reactive control."),
]

FLOWS = [
    ("Turbulent jet", "amplifier", "jet.jpg",
     "Re ~10<sup>6</sup>, subsonic to supersonic, dynamics and sound: wave packets, "
     "loud events, screech mode switching."),
    ("Open cavity", "oscillator", "cavity.jpg",
     "Re 10<sup>3</sup>–10<sup>5</sup>: Rossiter tones, mode coupling, broadband–tonal intermittency."),
    ("Airfoil", "both, with pitch &amp; plunge", "airfoil.jpg",
     "Re 10<sup>3</sup>–4×10<sup>5</sup>: separation, fluid–structure interaction, flapping control."),
]

QUESTIONS = [
    "How does turbulence structure emerge and organise under changing conditions?",
    "When and why do flows switch regime, and can these transitions be forecast?",
    "How can this understanding drive effective, low-latency control?",
]

PHASES = [("Foundation", "M1–24"), ("Integration", "M22–48"), ("Capability", "M49–72")]
WORK_PACKAGES = [
    ("WP1", "Experiments", "Pprime"),
    ("WP2", "Simulation", "Sapienza"),
    ("WP3", "Reduced-order modelling &amp; data assimilation", "Caltech"),
    ("WP4", "Synergy", "all sites"),
    ("WP5", "Coordination", "all sites"),
]
OUTPUTS_TEXT = "Open databases, software and an open workshop in the final year."

# ── Team ─────────────────────────────────────────────────────────────────────
# photo: filename in docs/images/ (optional). url: personal/institutional page.
TEAM = [
    dict(pillar="Experiment", site="CNRS – Institut Pprime, Poitiers",
         url="https://www.pprime.fr/",
         pi=dict(name="Peter Jordan", role="Corresponding PI", url="", photo=""),
         members=["Laurent David", "Ludovic Chatellier", "Jacques Borée",
                  "Vincent Jaunet", "Eduardo Martini", "Damien Eysseric", "Anton Lebedev"]),
    dict(pillar="Simulation", site="Sapienza Università di Roma",
         url="https://www.uniroma1.it/",
         pi=dict(name="Sergio Pirozzoli", role="PI", url="", photo=""),
         members=["Matteo Bernardini"]),
    dict(pillar="Modelling", site="California Institute of Technology",
         url="https://www.caltech.edu/",
         pi=dict(name="Tim Colonius", role="PI", url="https://colonius.caltech.edu", photo=""),
         members=["Andrew Stuart (Caltech)", "Jane Bae (Caltech)", "Aaron Towne (University of Michigan)"]),
]

# ── Openings ─────────────────────────────────────────────────────────────────
OPENINGS_TEXT = (
    "DISTURB will recruit 9 PhD students, 8 post-doctoral researchers and 3 "
    "engineers across Poitiers, Rome and Pasadena. Positions will be advertised "
    "here as they open."
)

# Team, Publications and Positions listings come from the Google Sheet
# (see sheet_data.py). TEAM above is only a fallback if the sheet is unreachable.
