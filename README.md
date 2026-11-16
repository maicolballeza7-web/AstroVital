# AstroVital

**Astronaut Self-Health Monitoring System** for the NASA Space Apps challenge:
**Create Health Monitoring Software for Astronauts on Space Missions**.

AstroVital is a self-assessment prototype designed for long-duration space missions. It helps users track health indicators, observe personal changes, and receive preventive guidance through the following workflow:

**MONITOR → ANALYZE → UNDERSTAND → ACT**

> AstroVital is an educational tool that uses both simulated data and user-entered records. It does not provide medical diagnoses, prescribe treatments, or authorize critical activities such as an EVA (Extravehicular Activity).

## Features

- Tracking of heart rate, blood pressure, temperature, glucose levels, sleep, stress, physical activity, and mood.
- Data validation and detection of missing indicators.
- Local storage of user assessments in CSV format.
- Separation between user history and simulated data.
- Establishment of a personal baseline after at least three saved assessments.
- Transparent comparison against the individual’s own average.
- Insights regarding recent deviations and trends.
- "Human Health Map" featuring five categories of indicators.
- Independent charts for different types of metrics.
- Experimental "Mission Readiness" indicator (not intended for medical authorization).

## Structure

```text
SPACE APP/
├── app.py
├── modules/
│   ├── __init__.py
│   ├── assessment.py
│   ├── baseline.py
│   ├── insights.py
│   └── persistence.py
├── data/
│   └── .gitkeep
├── requirements.txt
├── README.md
└── .gitignore
```

## Running Locally

Requires Python 3.11 or higher. ### Windows PowerShell

```powershell
git clone <REPOSITORY_URL>
cd "SPACE APP"
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

The application will typically be available at
`http://localhost:8501`.

### Running without activating the environment

```powershell
.\.venv\Scripts\streamlit.exe run app.py
```

## Deploying to Streamlit Community Cloud

1. Create a public repository on GitHub.
2. Upload `app.py`, `modules/`, `data/.gitkeep`, `requirements.txt`,
`README.md`, and `.gitignore`.
3. Go to [share.streamlit.io](https://share.streamlit.io/).
4. Select the repository, the branch, and the `app.py` file.
5. Click **Deploy**.

No secrets or environment variables need to be configured for this MVP.

### Cloud Persistence

Assessments are saved in `data/assessments.csv`. In Streamlit Community Cloud,
local container storage should not be considered permanent: a restart or
redeploy may erase these records. A production-ready version would require a
database or persistent storage.

## Data and Reliability

- Data generated using NumPy is labeled as **simulated**.
- Data submitted via the form is labeled as **user**.
- Synthetic data is not presented as actual measurements from astronauts.
- Establishing a baseline requires a minimum of three user assessments.
- Current rules are based on prototype heuristics, not universal clinical
criteria.
- The Readiness Score is experimental and does not determine fitness for EVA.
- 
## Use of Artificial Intelligence
AI coding assistants were used to accelerate boilerplate code generation and documentation. The system architecture, medical logic, validation rules, and project design were developed by the author.

The current version does not integrate external datasets from the NASA Human
Research Program, Human Research Roadmap, OSDR, or GeneLab. This limitation is intentional: scientific results are not attributed to sources that have not yet been verified or integrated.

## Verification before publishing

```powershell
python -m py_compile app.py modules\assessment.py modules\baseline.py modules\insights.py modules\persistence.py
streamlit run app.py
```

Verify the following manually:

- That an assessment can be saved.
- That `data/assessments.csv` appears locally.
- That missing indicators are clearly displayed.
- That the baseline indicates when it is not yet reliable.
- That the charts render correctly without mixing units.
