# ResumeSkillExtractor

A Python tool for extracting skills, predicting roles, and analyzing experience from resumes (PDFs) using hybrid skill extraction and zero-shot classification.

---

## Features

- Extracts skills using a hybrid method combining rule-based and zero-shot learning.
- Predicts job roles based on resume content with zero-shot classification.
- Extracts years of experience using regex patterns.
- Provides detailed skill and extraction statistics.
- Supports processing PDF resumes.
- Includes a Streamlit UI for uploading resumes and searching relevant jobs via a webscraper (LinkedIn credentials required).

---
## Directories
- `scraper/` contains the cookie retrieval and web scraping of LiknedIn Job posts using Selenium
- `training/` contains a small dataset for natural language inference for tech skills and roles.
- `src/` contains the base (`script.py`), it's the script you need to run and a Streamlit interface (`app.py`)
---

## Installation

1. Clone the repo:
   ```bash
   git clone https://github.com/yourusername/zeroshot-skill-extractor.git
   cd zeroshot-skill-extractor
   ```

2. Make sure you have a HuggingFace Access Token (from your HF account) and that you log in to be able to use the transformers and datasets *(personally, I'm using the `huggingface-cli login` command)*

3. Install dependencies:
    ```bash
        pip install -r requirements.txt
     ```

## Training the NLI for resume skills

#### ATTENTION: This step is required, because in `model_config.py` the `skill_classifier_model` variable is set to this newly generated model directory. If you want to omit this step, just comment out the line in `skill_classifier_model` and enable the one above which is using a HuggingFace model (MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli).

**Training**
```bash
    python3 src/training/train_nli_for_resume_skills.py
```

**Testing**
```bash
    python3 src/training/trainer_test.py
```


## Usage

#### Command-line
```bash
    python3 src/script.py <path-to-pdf>
```
- Processes a hardcoded PDF and outputs skills, role prediction, and other details. Results are saved as JSON in the root directory.

##### Streamlit UI
```bash
    cd src
    streamlit run app.py
```
- Upload a PDF resume.
- Extract skills and roles.
- Search relevant jobs tailored to your skills (requires RapidAPI LinkedIn key in `.env` file or just configure your own and modify `app.py`)

## Others

#### Configuration
Customize model settings in ModelConfig. The extractor loads SpaCy models and zero-shot classifiers accordingly.

#### Updating requirements
I'm using `pipreqs` to get rid of all the fluff dependencies, whenever you install a dependency and wanna update the requirements, run:
```bash
    pipreqs ./src --force --encoding=utf-8 --savepath=requirements.txt
```

## Short demo
[![Watch the demo](https://img.youtube.com/vi/izUvITahOV0/0.jpg)](https://www.youtube.com/watch?v=izUvITahOV0)
