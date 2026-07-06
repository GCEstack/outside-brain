import re


STOP_WORDS = {
    "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "by", "from", "as", "is", "was", "are", "this", "that",
    "it", "its", "i", "you", "we", "they", "he", "she", "my", "your",
}


def tokenize(text: str) -> set[str]:
    words = re.findall(r"[a-zA-Z0-9]+", text.lower())
    return {w for w in words if w not in STOP_WORDS and len(w) > 1}


def build_keywords(project_name: str, project_summary: str, domains: list[str]) -> set[str]:
    keywords: set[str] = set()
    keywords.update(tokenize(project_name))
    keywords.update(tokenize(project_summary))
    for domain in domains:
        keywords.update(tokenize(domain))
    return keywords
