QUESTION_GENERATOR_TEMPLATE = """
You are an expert teacher assistant.

Create {number_of_questions} {question_type} practice questions for a {grade_level} {subject} class on the topic: "{topic}".

Difficulty level: {difficulty}
Additional requirements: {additional_requirements}

Please format the response with the following sections:
1. Practice Questions
2. Answer Key
3. Brief Explanation for Each Answer

Keep the language appropriate for {grade_level} students and make sure the questions are accurate, clear, and classroom-ready.
""".strip()
