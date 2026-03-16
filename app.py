import streamlit.components.v1 as components
import streamlit as st

from data.options import (
    DIFFICULTY_LEVELS,
    EXPLANATION_STYLES,
    GRADE_LEVELS,
    QUESTION_TYPES,
    SUBJECTS,
    TOOLS,
    TONES,
)
from templates.feedback_generator import FEEDBACK_TEMPLATE
from templates.grading_generator import GRADING_TEMPLATE
from templates.lesson_explainer import LESSON_EXPLAINER_TEMPLATE
from templates.question_generator import QUESTION_GENERATOR_TEMPLATE
from templates.quiz_generator import QUIZ_GENERATOR_TEMPLATE
from utils.prompt_library import delete_prompt, get_prompt_list, load_prompt_library, save_prompt_to_library
from utils.prompt_builder import build_prompt


st.set_page_config(
    page_title="Teacher AI Prompt Generator",
    page_icon=":memo:",
    layout="wide",
)


def apply_app_styles() -> None:
    """Apply lightweight styling to give the app a more polished product feel."""
    st.markdown(
        """
        <style>
        .stApp {
            background: linear-gradient(180deg, #f6f8fb 0%, #ffffff 22%);
        }
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            max-width: 1200px;
        }
        [data-testid="stSidebar"] {
            background: #f7f9fc;
            border-right: 1px solid rgba(15, 23, 42, 0.08);
        }
        .app-panel {
            background: #ffffff;
            border: 1px solid rgba(15, 23, 42, 0.08);
            border-radius: 18px;
            padding: 1.25rem 1.25rem 1rem 1.25rem;
            box-shadow: 0 10px 30px rgba(15, 23, 42, 0.05);
            margin-bottom: 1rem;
        }
        .section-label {
            font-size: 0.82rem;
            font-weight: 700;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            color: #3b5ccc;
            margin-bottom: 0.35rem;
        }
        .hero-card {
            background: linear-gradient(135deg, #ffffff 0%, #eef4ff 100%);
            border: 1px solid rgba(59, 92, 204, 0.12);
            border-radius: 22px;
            padding: 1.4rem 1.5rem 1.1rem 1.5rem;
            box-shadow: 0 14px 36px rgba(15, 23, 42, 0.06);
            margin-bottom: 1rem;
        }
        .hero-title {
            font-size: 2rem;
            font-weight: 700;
            color: #0f172a;
            margin-bottom: 0.2rem;
        }
        .hero-subtitle {
            font-size: 1rem;
            color: #334155;
            margin-bottom: 0.7rem;
        }
        .helper-text {
            color: #475569;
            font-size: 0.95rem;
            line-height: 1.5;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_section_shell(label: str, title: str, caption: str | None = None) -> None:
    """Render a section heading with consistent visual hierarchy."""
    st.markdown(f'<div class="section-label">{label}</div>', unsafe_allow_html=True)
    st.subheader(title)
    if caption:
        st.caption(caption)


def render_header() -> None:
    """Render the polished top-of-page product header."""
    st.markdown(
        """
        <div class="hero-card">
          <div class="hero-title">AI Education Prompt Generator</div>
          <div class="hero-subtitle">Create high-quality teaching prompts in seconds.</div>
          <div class="helper-text">
            This tool helps teachers quickly generate classroom-ready prompts for AI tools like ChatGPT, Claude, and Gemini.
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_output(prompt: str, filename: str) -> None:
    """Display the generated prompt and its follow-up actions in clear sections."""
    with st.container():
        render_section_shell(
            "Generated Prompt",
            "Generated Prompt",
            "Review, save, and reuse this prompt in your preferred AI tool.",
        )
        prompt_title = st.text_input("Prompt title", key="prompt_title_input", placeholder="Example: Algebra Quiz")
        st.text_area(
            "Prompt content",
            value=prompt,
            height=320,
            disabled=True,
            label_visibility="collapsed",
        )

    with st.container():
        render_section_shell(
            "Actions",
            "Prompt Actions",
            "Save the prompt, copy it, or send it directly to an AI assistant.",
        )

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Save Prompt", use_container_width=True):
                current_prompt = st.session_state.get("current_prompt_data", {}).copy()
                current_prompt["title"] = prompt_title.strip()
                if not prompt_title.strip():
                    st.warning("Enter a prompt title before saving.")
                elif save_prompt_to_library(current_prompt):
                    st.success(f'Saved "{prompt_title.strip()}" to the Prompt Library.')
                else:
                    st.warning("A prompt with that title already exists. Choose a different title.")

        with col2:
            render_copy_button(prompt)

        st.markdown("---")
        st.markdown("**Send to AI**")

        col3, col4, col5 = st.columns(3)
        with col3:
            st.link_button("Open ChatGPT", "https://chat.openai.com", use_container_width=True)
        with col4:
            st.link_button("Open in Claude", "https://claude.ai", use_container_width=True)
        with col5:
            st.link_button("Open in Gemini", "https://gemini.google.com", use_container_width=True)

        st.markdown("---")
        st.download_button(
            label="Download Prompt",
            data=prompt,
            file_name=filename,
            mime="text/plain",
            use_container_width=True,
        )


def render_copy_button(prompt: str) -> None:
    """Render a small browser-side copy button for the current prompt."""
    escaped_prompt = prompt.replace("\\", "\\\\").replace("`", "\\`").replace("${", "\\${")
    components.html(
        f"""
        <div style="display: grid;">
          <button
            onclick="navigator.clipboard.writeText(`{escaped_prompt}`)"
            style="
              width: 100%;
              padding: 0.5rem 0.75rem;
              border-radius: 0.5rem;
              border: 1px solid rgba(49, 51, 63, 0.2);
              background: white;
              cursor: pointer;
              font-size: 0.95rem;
              font-weight: 600;
            "
          >
            Copy Prompt
          </button>
        </div>
        """,
        height=44,
    )


def set_current_prompt(prompt_data: dict[str, str], filename: str) -> None:
    """Store the active prompt in session state for reuse across the app."""
    st.session_state["current_prompt_data"] = prompt_data
    st.session_state["current_prompt_filename"] = filename
    st.session_state["prompt_title_input"] = prompt_data.get("title", "")


def render_prompt_library() -> None:
    """Render the sidebar prompt library with load and delete controls."""
    with st.sidebar:
        st.header("Prompt Library")
        st.caption("Save and reuse your generated prompts.")
        st.markdown("---")
        prompt_titles = get_prompt_list()

        if not prompt_titles:
            st.caption("No saved prompts yet.")
            return

        selected_title = st.selectbox("Saved Prompts", prompt_titles, key="library_selected_title")
        selected_prompt = next(
            (item for item in load_prompt_library() if item.get("title") == selected_title),
            None,
        )

        if not selected_prompt:
            st.caption("Select a saved prompt to preview it.")
            return

        st.markdown(f"**{selected_prompt['title']}**")
        st.caption(
            " | ".join(
                value
                for value in [
                    selected_prompt.get("subject", ""),
                    selected_prompt.get("grade", ""),
                    selected_prompt.get("difficulty", ""),
                ]
                if value
            )
        )
        st.text_area(
            "Prompt Content",
            selected_prompt.get("prompt", ""),
            height=180,
            disabled=True,
        )

        load_col, delete_col = st.columns(2)
        with load_col:
            if st.button("Load Prompt", use_container_width=True):
                set_current_prompt(selected_prompt, "saved_prompt.txt")
                st.success(f'Loaded "{selected_prompt["title"]}".')

        with delete_col:
            if st.button("Delete Prompt", use_container_width=True):
                if delete_prompt(selected_prompt["title"]):
                    if st.session_state.get("current_prompt_data", {}).get("title") == selected_prompt["title"]:
                        st.session_state.pop("current_prompt_data", None)
                        st.session_state.pop("current_prompt_filename", None)
                        st.session_state["prompt_title_input"] = ""
                    st.success(f'Deleted "{selected_prompt["title"]}".')
                    st.rerun()


def practice_questions_tool() -> None:
    with st.container():
        render_section_shell(
            "Teaching Task Setup",
            "Generate Practice Questions",
            "Create a classroom-ready prompt for practice questions, answer keys, and explanations.",
        )

        with st.form("practice_questions_form"):
            left_col, right_col = st.columns(2)
            with left_col:
                subject = st.selectbox("Subject", SUBJECTS)
                grade_level = st.selectbox("Grade level", GRADE_LEVELS, key="practice_grade")
                question_type = st.selectbox("Question type", QUESTION_TYPES)
            with right_col:
                difficulty = st.selectbox("Difficulty", DIFFICULTY_LEVELS, key="practice_difficulty")
                number_of_questions = st.slider("Number of questions", min_value=1, max_value=20, value=5)
                topic = st.text_input("Topic")
            additional_requirements = st.text_area(
                "Additional instructions",
                placeholder="Include standards, vocabulary, examples, or formatting requirements.",
            )
            submitted = st.form_submit_button("Generate Prompt", use_container_width=True)

    if submitted:
        prompt = build_prompt(
            QUESTION_GENERATOR_TEMPLATE,
            subject=subject,
            grade_level=grade_level,
            topic=topic.strip() or "the selected topic",
            question_type=question_type,
            number_of_questions=number_of_questions,
            difficulty=difficulty,
            additional_requirements=additional_requirements.strip() or "No additional requirements.",
        )
        set_current_prompt(
            {
                "title": "",
                "subject": subject,
                "grade": grade_level,
                "difficulty": difficulty,
                "question_type": question_type,
                "prompt": prompt,
            },
            "practice_questions_prompt.txt",
        )


def create_quiz_tool() -> None:
    with st.container():
        render_section_shell(
            "Teaching Task Setup",
            "Create Quiz",
            "Generate a quiz-writing prompt with answer key instructions.",
        )

        with st.form("quiz_form"):
            left_col, right_col = st.columns(2)
            with left_col:
                subject = st.selectbox("Subject", SUBJECTS, key="quiz_subject")
                grade_level = st.selectbox("Grade level", GRADE_LEVELS, key="quiz_grade")
                topic = st.text_input("Topic", key="quiz_topic")
            with right_col:
                difficulty = st.selectbox("Difficulty", DIFFICULTY_LEVELS, key="quiz_difficulty")
                quiz_length = st.slider("Quiz length", min_value=3, max_value=25, value=10)
                question_types = st.multiselect(
                    "Question types",
                    QUESTION_TYPES,
                    default=[QUESTION_TYPES[0]],
                )
            submitted = st.form_submit_button("Generate Prompt", use_container_width=True)

    if submitted:
        selected_question_types = ", ".join(question_types) if question_types else "multiple choice"
        prompt = build_prompt(
            QUIZ_GENERATOR_TEMPLATE,
            subject=subject,
            grade_level=grade_level,
            topic=topic.strip() or "the selected topic",
            quiz_length=quiz_length,
            question_types=selected_question_types,
            difficulty=difficulty,
        )
        set_current_prompt(
            {
                "title": "",
                "subject": subject,
                "grade": grade_level,
                "difficulty": difficulty,
                "question_type": selected_question_types,
                "prompt": prompt,
            },
            "quiz_prompt.txt",
        )


def grade_student_answers_tool() -> None:
    with st.container():
        render_section_shell(
            "Teaching Task Setup",
            "Grade Student Answers",
            "Build a grading prompt that requests a score, strengths, improvements, and feedback.",
        )

        with st.form("grading_form"):
            left_col, right_col = st.columns(2)
            with left_col:
                subject = st.selectbox("Subject", SUBJECTS, key="grading_subject")
                grade_level = st.selectbox("Grade level", GRADE_LEVELS, key="grading_grade")
                assignment_topic = st.text_input("Assignment topic")
            with right_col:
                rubric = st.text_area("Rubric", placeholder="Paste the grading rubric or criteria.", height=140)
            student_answer = st.text_area(
                "Student answer",
                height=200,
                placeholder="Paste the student's response here.",
            )
            submitted = st.form_submit_button("Generate Prompt", use_container_width=True)

    if submitted:
        prompt = build_prompt(
            GRADING_TEMPLATE,
            subject=subject,
            grade_level=grade_level,
            assignment_topic=assignment_topic.strip() or "the selected assignment topic",
            rubric=rubric.strip() or "No rubric provided.",
            student_answer=student_answer.strip() or "No student answer provided.",
        )
        set_current_prompt(
            {
                "title": "",
                "subject": subject,
                "grade": grade_level,
                "difficulty": "",
                "question_type": "",
                "prompt": prompt,
            },
            "grading_prompt.txt",
        )


def lesson_explanation_tool() -> None:
    with st.container():
        render_section_shell(
            "Teaching Task Setup",
            "Generate Lesson Explanation",
            "Create a prompt for a clear explanation tailored to the selected grade level.",
        )

        with st.form("lesson_form"):
            left_col, right_col = st.columns(2)
            with left_col:
                subject = st.selectbox("Subject", SUBJECTS, key="lesson_subject")
                grade_level = st.selectbox("Grade level", GRADE_LEVELS, key="lesson_grade")
            with right_col:
                explanation_style = st.selectbox("Explanation style", EXPLANATION_STYLES)
                topic = st.text_input("Topic", key="lesson_topic")
            submitted = st.form_submit_button("Generate Prompt", use_container_width=True)

    if submitted:
        prompt = build_prompt(
            LESSON_EXPLAINER_TEMPLATE,
            subject=subject,
            grade_level=grade_level,
            topic=topic.strip() or "the selected topic",
            explanation_style=explanation_style,
        )
        set_current_prompt(
            {
                "title": "",
                "subject": subject,
                "grade": grade_level,
                "difficulty": explanation_style,
                "question_type": "",
                "prompt": prompt,
            },
            "lesson_explanation_prompt.txt",
        )


def student_feedback_tool() -> None:
    with st.container():
        render_section_shell(
            "Teaching Task Setup",
            "Write Student Feedback",
            "Generate a prompt for constructive, personalized student feedback.",
        )

        with st.form("feedback_form"):
            left_col, right_col = st.columns(2)
            with left_col:
                student_name = st.text_input("Student name")
                subject = st.selectbox("Subject", SUBJECTS, key="feedback_subject")
                tone = st.selectbox("Tone", TONES)
            with right_col:
                performance_summary = st.text_area(
                    "Performance summary",
                    placeholder="Summarize the student's recent performance.",
                    height=140,
                )
            strengths = st.text_area("Strengths", placeholder="List the student's strengths.")
            weaknesses = st.text_area("Growth areas", placeholder="List the student's growth areas.")
            submitted = st.form_submit_button("Generate Prompt", use_container_width=True)

    if submitted:
        prompt = build_prompt(
            FEEDBACK_TEMPLATE,
            student_name=student_name.strip() or "the student",
            subject=subject,
            performance_summary=performance_summary.strip() or "No performance summary provided.",
            strengths=strengths.strip() or "No strengths provided.",
            weaknesses=weaknesses.strip() or "No weaknesses provided.",
            tone=tone,
        )
        set_current_prompt(
            {
                "title": "",
                "subject": subject,
                "grade": "",
                "difficulty": tone,
                "question_type": "",
                "prompt": prompt,
            },
            "student_feedback_prompt.txt",
        )


TOOL_RENDERERS = {
    TOOLS[0]: practice_questions_tool,
    TOOLS[1]: create_quiz_tool,
    TOOLS[2]: grade_student_answers_tool,
    TOOLS[3]: lesson_explanation_tool,
    TOOLS[4]: student_feedback_tool,
}


def main() -> None:
    if "current_prompt_data" not in st.session_state:
        st.session_state["current_prompt_data"] = {}
    if "current_prompt_filename" not in st.session_state:
        st.session_state["current_prompt_filename"] = "generated_prompt.txt"
    if "prompt_title_input" not in st.session_state:
        st.session_state["prompt_title_input"] = ""

    apply_app_styles()

    render_header()

    with st.sidebar:
        st.markdown("### Workspace")
        st.caption("Choose the type of teaching prompt you want to create.")
        selected_tool = st.radio("Choose a tool", TOOLS, label_visibility="collapsed")

    render_prompt_library()
    TOOL_RENDERERS[selected_tool]()

    current_prompt = st.session_state.get("current_prompt_data", {})
    if current_prompt.get("prompt"):
        st.markdown("---")
        render_output(
            current_prompt["prompt"],
            st.session_state.get("current_prompt_filename", "generated_prompt.txt"),
        )


if __name__ == "__main__":
    main()
