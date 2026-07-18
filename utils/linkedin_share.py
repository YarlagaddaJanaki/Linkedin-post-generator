import json
import urllib.parse

LINKEDIN_COMPOSE_BASE = "https://www.linkedin.com/feed/?shareActive=true&text="
MAX_URL_TEXT_LENGTH = 1800


def build_linkedin_compose_url(post_text: str) -> str:
    encoded = urllib.parse.quote(post_text, safe="")
    return f"{LINKEDIN_COMPOSE_BASE}{encoded}"


def can_prefill_via_url(post_text: str) -> bool:
    return len(build_linkedin_compose_url(post_text)) <= MAX_URL_TEXT_LENGTH


def copy_to_clipboard_button(label: str, text: str, key: str) -> None:
    import streamlit.components.v1 as components

    components.html(
        f"""
        <button id="{key}" style="
            width: 100%;
            height: 50px;
            font-size: 18px;
            font-weight: bold;
            background: #ffffff;
            color: #0A66C2;
            border: 1px solid #0A66C2;
            border-radius: 8px;
            cursor: pointer;
        ">
            {label}
        </button>
        <script>
            document.getElementById("{key}").addEventListener("click", function() {{
                navigator.clipboard.writeText({json.dumps(text)}).then(function() {{
                    document.getElementById("{key}").innerText = "✅ Copied!";
                    setTimeout(function() {{
                        document.getElementById("{key}").innerText = {json.dumps(label)};
                    }}, 2000);
                }});
            }});
        </script>
        """,
        height=60,
    )
