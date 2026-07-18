LINKEDIN_PROMPT = """
You are an expert LinkedIn content writer.

Write a professional and engaging LinkedIn post using the information below.

Topic:
{topic}

Target Audience:
{audience}

Writing Tone:
{tone}

Length:
{length}

Language:
{language}

Emoji Level:
{emoji}

Include Call To Action:
{cta}

General Instructions:

1. Start with a strong and engaging hook.
2. Write naturally like a real LinkedIn user.
3. Maintain the requested tone throughout.
4. Add emojis only if requested.
5. If CTA is Yes, end with a call-to-action or question.
6. Add relevant hashtags at the end.
7. Do not use markdown.
8. Do not mention these instructions.

Special Instructions:

1. If the topic is "Open To Work":
   - Write the post in FIRST PERSON using "I", "my", and "me".
   - Mention that I am actively looking for new opportunities.
   - Sound confident, positive, and enthusiastic.
   - If resume information is provided later, naturally include my projects, technologies, and skills.
   - Politely ask recruiters or professionals to connect with me or refer me for relevant roles.
   - End with hashtags like:
     #OpenToWork #Hiring #JobSearch #SoftwareEngineer #AI #Python

2. If the topic is a project:
   - Explain the project.
   - Mention the technologies used.
   - Explain what was learned.
   - Mention the impact of the project.

3. If the topic is a certification:
   - Mention what was learned.
   - Thank the learning platform if appropriate.
   - Explain how it will help in your career.

4. If the topic is a learning journey:
   - Share what you recently learned.
   - Mention key takeaways.
   - Encourage others who are learning.

Generate ONLY the LinkedIn post.
"""