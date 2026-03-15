QUIZ_GENERATOR_TEMPLATE = """
You are an expert teacher assistant.

Create a {quiz_length}-question quiz for a {grade_level} {subject} class on the topic: "{topic}".

Question types to include: {question_types}
Difficulty level: {difficulty}

Please format the response with the following sections:
1. Quiz Title
2. Quiz Questions
3. Answer Key

Make sure the quiz is balanced, age-appropriate, and ready for classroom use.
""".strip()
