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

    return response.content


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

    # -------- Resume Context (RAG) -------- #

    if retrieved_context:

        prompt += f"""

IMPORTANT INSTRUCTIONS:

You are writing a LinkedIn post for the owner of the uploaded resume.

Use the resume information below as the PRIMARY source of information.

Do NOT invent projects, skills, achievements, certifications, companies, or experiences that are not present.

If the topic matches the resume, naturally include the relevant projects, technologies, achievements, and skills.

If the topic is "Open To Work", write the post in first person ("I", "my") and mention that I am actively seeking new opportunities. Highlight my skills and projects from the resume and politely request referrals or opportunities.

Resume Information:
------------------------
{retrieved_context}
------------------------

"""

    else:

        prompt += """

IMPORTANT INSTRUCTIONS:

Generate an engaging LinkedIn post based only on the user's topic.

If the topic is "Open To Work", write the post in first person.

Mention that I am actively looking for new opportunities.

Encourage recruiters and professionals to connect with me.

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

        for i, post in enumerate(examples):

            prompt += f"""

Example {i+1}

{post['text']}
"""

            if i == 1:
                break

    return prompt