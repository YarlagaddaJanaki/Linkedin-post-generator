import json
from llm_helper import llm
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException


# ---------- CLEAN INVALID UNICODE (emojis, surrogates) ----------
def clean_text(text: str) -> str:
    return text.encode("utf-8", "ignore").decode("utf-8")


def deep_clean(obj):
    """
    Recursively clean strings inside dicts/lists
    to remove invalid unicode surrogate characters.
    """
    if isinstance(obj, str):
        return obj.encode("utf-8", "ignore").decode("utf-8")
    elif isinstance(obj, list):
        return [deep_clean(item) for item in obj]
    elif isinstance(obj, dict):
        return {k: deep_clean(v) for k, v in obj.items()}
    else:
        return obj


# ---------- MAIN PROCESS ----------
def process_posts(raw_file_path, processed_file_path):
    with open(raw_file_path, encoding="utf-8") as file:
        posts = json.load(file)

    enriched_posts = []

    for post in posts:
        cleaned_text = clean_text(post["text"])
        metadata = extract_metadata(cleaned_text)
        enriched_posts.append(post | metadata)

    unified_tags = get_unified_tags(enriched_posts)

    for post in enriched_posts:
        post["tags"] = list(
            {unified_tags.get(tag, tag) for tag in post.get("tags", [])}
        )

    # 🔥 FINAL SAFETY CLEAN BEFORE WRITING
    cleaned_output = deep_clean(enriched_posts)

    with open(processed_file_path, "w", encoding="utf-8") as outfile:
        json.dump(cleaned_output, outfile, indent=4, ensure_ascii=False)


# ---------- METADATA EXTRACTION ----------
def extract_metadata(post):
    parser = JsonOutputParser()

    template = """
You are a JSON API.
Return ONLY valid JSON. No explanations. No markdown.

Schema:
{{
  "line_count": number,
  "language": "English" | "Hinglish",
  "tags": [string, string]
}}

Rules:
- Max 2 tags
- Title Case tags only
- Language must be English or Hinglish

Post:
{post}
"""

    prompt = PromptTemplate(
        template=template,
        input_variables=["post"],
    )

    chain = prompt | llm | parser

    try:
        return chain.invoke({"post": post})
    except OutputParserException as e:
        raise OutputParserException("Metadata JSON parsing failed") from e


# ---------- TAG UNIFICATION ----------
def get_unified_tags(posts_with_metadata):
    unique_tags = set()

    for post in posts_with_metadata:
        unique_tags.update(post.get("tags", []))

    parser = JsonOutputParser()

    template = """
You are a JSON API.

Unify similar tags and return mapping.

Rules:
- Merge similar tags
- Title Case only
- Return ONLY valid JSON

Tags:
{tags}
"""

    prompt = PromptTemplate(
        template=template,
        input_variables=["tags"],
    )

    chain = prompt | llm | parser

    try:
        return chain.invoke({"tags": list(unique_tags)})
    except OutputParserException as e:
        raise OutputParserException("Tag unification failed") from e


# ---------- ENTRY POINT ----------
if __name__ == "__main__":
    process_posts(
        "data/raw_posts.json",
        "data/processed_posts.json"
    )
