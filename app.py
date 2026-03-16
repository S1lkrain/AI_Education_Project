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


def render_output(prompt: str, filename: str) -> None:
    """Display the generated prompt and offer a text download."""
    st.subheader("Generated Prompt")
    st.code(prompt, language="text")
    prompt_title = st.text_input("Prompt title", key="prompt_title_input", placeholder="Example: Algebra Quiz")

    save_col, copy_col, chatgpt_col = st.columns(3)
    with save_col:
        if st.button("Save Prompt", use_container_width=True):
            current_prompt = st.session_state.get("current_prompt_data", {}).copy()
            current_prompt["title"] = prompt_title.strip()
            if not prompt_title.strip():
                st.warning("Enter a prompt title before saving.")
            elif save_prompt_to_library(current_prompt):
                st.success(f'Saved "{prompt_title.strip()}" to the Prompt Library.')
            else:
                st.warning("A prompt with that title already exists. Choose a different title.")

    with copy_col:
        render_copy_button(prompt)

    with chatgpt_col:
        st.link_button("Open ChatGPT", "https://chat.openai.com", use_container_width=True)

    st.markdown("**Send to AI**")
    claude_col, gemini_col = st.columns(2)
    with claude_col:
        st.link_button("Open in Claude", "https://claude.ai", use_container_width=True)
    with gemini_col:
        st.link_button("Open in Gemini", "https://gemini.google.com", use_container_width=True)

    st.download_button(
        label="Download Prompt",
        data=prompt,
        file_name=filename,
        mime="text/plain",
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
              padding: 0.45rem 0.75rem;
              border-radius: 0.5rem;
              border: 1px solid rgba(49, 51, 63, 0.2);
              background: white;
              cursor: pointer;
              font-size: 0.95rem;
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
        st.divider()
        st.header("Prompt Library")
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
    st.header("Generate Practice Questions")
    st.write("Create a classroom-ready prompt for practice questions, answer keys, and explanations.")

    with st.form("practice_questions_form"):
        subject = st.selectbox("Subject", SUBJECTS)
        grade_level = st.selectbox("Grade level", GRADE_LEVELS, key="practice_grade")
        topic = st.text_input("Topic")
        question_type = st.selectbox("Question type", QUESTION_TYPES)
        number_of_questions = st.slider("Number of questions", min_value=1, max_value=20, value=5)
        difficulty = st.selectbox("Difficulty", DIFFICULTY_LEVELS, key="practice_difficulty")
        additional_requirements = st.text_area("Additional requirements", placeholder="Include vocabulary, standards, examples, or formatting needs.")
        submitted = st.form_submit_button("Generate Prompt")

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
    st.header("Create Quiz")
    st.write("Generate a quiz-writing prompt with answer key instructions.")

    with st.form("quiz_form"):
        subject = st.selectbox("Subject", SUBJECTS, key="quiz_subject")
        grade_level = st.selectbox("Grade level", GRADE_LEVELS, key="quiz_grade")
        topic = st.text_input("Topic", key="quiz_topic")
        quiz_length = st.slider("Quiz length", min_value=3, max_value=25, value=10)
        question_types = st.multiselect(
            "Question types",
            QUESTION_TYPES,
            default=[QUESTION_TYPES[0]],
        )
        difficulty = st.selectbox("Difficulty", DIFFICULTY_LEVELS, key="quiz_difficulty")
        submitted = st.form_submit_button("Generate Prompt")

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
    st.header("Grade Student Answers")
    st.write("Build a grading prompt that requests a score, strengths, improvements, and feedback.")

    with st.form("grading_form"):
        subject = st.selectbox("Subject", SUBJECTS, key="grading_subject")
        grade_level = st.selectbox("Grade level", GRADE_LEVELS, key="grading_grade")
        assignment_topic = st.text_input("Assignment topic")
        rubric = st.text_area("Rubric", placeholder="Paste the grading rubric or criteria.")
        student_answer = st.text_area("Student answer", height=200, placeholder="Paste the student's response here.")
        submitted = st.form_submit_button("Generate Prompt")

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
    st.header("Generate Lesson Explanation")
    st.write("Create a prompt for a clear explanation tailored to the selected grade level.")

    with st.form("lesson_form"):
        subject = st.selectbox("Subject", SUBJECTS, key="lesson_subject")
        grade_level = st.selectbox("Grade level", GRADE_LEVELS, key="lesson_grade")
        topic = st.text_input("Topic", key="lesson_topic")
        explanation_style = st.selectbox("Explanation style", EXPLANATION_STYLES)
        submitted = st.form_submit_button("Generate Prompt")

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
    st.header("Write Student Feedback")
    st.write("Generate a prompt for constructive, personalized student feedback.")

    with st.form("feedback_form"):
        student_name = st.text_input("Student name")
        subject = st.selectbox("Subject", SUBJECTS, key="feedback_subject")
        performance_summary = st.text_area("Performance summary", placeholder="Summarize the student's recent performance.")
        strengths = st.text_area("Strengths", placeholder="List the student's strengths.")
        weaknesses = st.text_area("Weaknesses", placeholder="List the student's growth areas.")
        tone = st.selectbox("Tone", TONES)
        submitted = st.form_submit_button("Generate Prompt")

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

    st.title("Teacher AI Prompt Generator")
    st.caption("A simple Streamlit app for creating structured prompts teachers can paste into AI tools.")

    with st.sidebar:
        st.header("Tools")
        selected_tool = st.radio("Choose a tool", TOOLS, label_visibility="collapsed")

    render_prompt_library()
    TOOL_RENDERERS[selected_tool]()

    current_prompt = st.session_state.get("current_prompt_data", {})
    if current_prompt.get("prompt"):
        render_output(
            current_prompt["prompt"],
            st.session_state.get("current_prompt_filename", "generated_prompt.txt"),
        )


if __name__ == "__main__":
    main()
