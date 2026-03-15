# Teacher AI Prompt Generator

## Overview

Teacher AI Prompt Generator is a Streamlit MVP that helps teachers quickly create structured prompts for AI tools such as ChatGPT, Claude, and Gemini. The app provides simple forms for common classroom tasks and generates copy-ready prompts in a clean interface.

## Features

- Generate practice question prompts with answer keys and explanations
- Create quiz-generation prompts for different subjects and grade levels
- Build grading prompts using a rubric and student response
- Generate lesson explanation prompts with different explanation styles
- Write constructive student feedback prompts with adjustable tone
- Download generated prompts as text files

## Project Structure

```text
project/
├── app.py
├── requirements.txt
├── .gitignore
├── README.md
├── data/
│   └── options.py
├── templates/
│   ├── feedback_generator.py
│   ├── grading_generator.py
│   ├── lesson_explainer.py
│   ├── question_generator.py
│   └── quiz_generator.py
└── utils/
    └── prompt_builder.py
```

## Installation

Make sure you are using Python 3.10 or newer.

```bash
pip install -r requirements.txt
```

## Running Locally

Start the Streamlit application with:

```bash
streamlit run app.py
```

The app will open in your browser and run locally.

## Deployment to Streamlit Community Cloud

1. Push this project to a GitHub repository.
2. Go to `https://share.streamlit.io`.
3. Sign in with your GitHub account.
4. Click `Create app`.
5. Select your repository.
6. Select the `main` branch.
7. Set the main file path to `app.py`.
8. Click `Deploy`.

Once deployed, Streamlit Community Cloud will install dependencies from `requirements.txt` and launch the app automatically.
