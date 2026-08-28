from urllib import response

from httpx import post

from few_shots import FewShotPosts
from prompts.prompt_templates import LINKEDIN_PROMPT
from services.llm_service import LLMService

few_shot = FewShotPosts()
llm_service = LLMService()


def get_length_str(length):
    if length == "Short":
        return "1 to 5 lines"
    elif length == "Medium":
        return "6 to 10 lines"
    else:
        return "11 to 15 lines"


def generate_post(
    length,
    language,
    tag,
    audience,
    tone,
    emoji,
    cta,
    model_name,
    retrieved_context=""
):

    # Normalize common job-search topics
    job_topics = [
    "job searching",
    "job search",
    "looking for job",
    "looking for a job",
    "looking for opportunities",
    "looking for opportunity",
    "open to work",
    "open to opportunities",
    "career opportunity",
    "career opportunities",
    "new opportunity",
    "new opportunities",
    "seeking job",
    "seeking opportunities",
    "hiring",
    "job"
]

    if tag.lower().strip() in job_topics:
        tag = "Open To Work"

    prompt = get_prompt(
        length,
        language,
        tag,
        audience,
        tone,
        emoji,
        cta,
        retrieved_context
    )

    llm = llm_service.get_llm(model_name)

    response = llm.invoke(prompt)

    post = response.content.strip()

    if "</think>" in post:
        post = post.split("</think>", 1)[1].strip()

    return post


def get_prompt(
    length,
    language,
    tag,
    audience,
    tone,
    emoji,
    cta,
    retrieved_context=""
):

    length_str = get_length_str(length)

    prompt = LINKEDIN_PROMPT.format(
        topic=tag,
        audience=audience,
        tone=tone,
        length=length_str,
        language=language,
        emoji=emoji,
        cta="Yes" if cta else "No"
    )

    # -------- RAG Context -------- #

    if retrieved_context:

        prompt += f"""

IMPORTANT:

You are writing a LinkedIn post using information from the
uploaded document.

Use the uploaded document information as the PRIMARY source
of factual information.

Do NOT invent projects, skills, achievements, certifications,
companies, experiences, names, dates, or other facts that are
not present in the uploaded document.

If the topic matches information in the uploaded document,
naturally include the relevant details.

If the topic is "Open To Work", write the post in first person
using "I" and "my". Highlight relevant skills and projects from
the uploaded document.

Uploaded Document Information:
------------------------
{retrieved_context}
------------------------
"""

    else:

        prompt += """

Generate an engaging LinkedIn post based only on the user's topic.

Do not invent specific achievements, certifications, companies,
or experiences that were not provided by the user.

If the topic is "Open To Work", write in first person and mention
that I am actively looking for opportunities.

End with relevant hashtags.
"""

    # -------- Few-shot Examples -------- #

    examples = few_shot.get_filtered_posts(
        length,
        language,
        tag
    )

    if len(examples) > 0:

        prompt += "\n\nWriting Style Examples:\n"

        for i, example in enumerate(examples):

            prompt += f"""

Example {i + 1}:

{example['text']}
"""

            if i == 1:
                break

    # -------- FINAL OUTPUT RULES -------- #

    prompt += """

FINAL OUTPUT RULES:

Return ONLY the final LinkedIn post.

Do NOT include reasoning, thinking process, analysis, planning,
explanations, drafts, or constraint checks.

Do NOT include <think> or </think> tags.

Do NOT repeat or explain the prompt instructions.

Do NOT say "Here is your LinkedIn post".

Start directly with the final LinkedIn post.

Your entire response must contain only the text that should be
published on LinkedIn.
"""

    return prompt