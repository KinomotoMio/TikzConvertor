"""TikZ to SVG conversion using LLM."""

import re
import litellm

SYSTEM_PROMPT = '''You are a TikZ to SVG converter. Convert LaTeX TikZ code to equivalent SVG code.

## TikZ to SVG Mapping

| TikZ | SVG |
|------|-----|
| node (circle) | <circle> + <text> |
| node (rectangle) | <rect> + <text> |
| \\draw line | <line> or <path> |
| \\draw arrow | <line> + marker-end |
| fill color | fill attribute |
| draw color | stroke attribute |
| thick/thin | stroke-width |
| foreach loop | expand into multiple elements |
| scope with xshift | transform="translate(x,0)" |

## Rules

1. Output ONLY valid SVG code, no explanations
2. Use appropriate viewBox
3. For Chinese text, use font-family="sans-serif"
4. Define arrowhead markers in <defs>
5. TikZ y-axis points up, SVG y-axis points down - flip accordingly
6. TikZ uses cm; multiply by 35 for pixels'''

USER_PROMPT = '''Convert this TikZ code to SVG:

```latex
{tikz_code}
```

Output ONLY the SVG code.'''


def tikz2svg(tikz_code: str, model: str, api_key: str) -> str:
    """Convert TikZ code to SVG using LLM."""
    # Extract tikzpicture if wrapped
    match = re.search(r'(\\begin\{tikzpicture\}.*?\\end\{tikzpicture\})', tikz_code, re.DOTALL)
    if match:
        tikz_code = match.group(1)

    response = litellm.completion(
        model=model,
        api_key=api_key,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": USER_PROMPT.format(tikz_code=tikz_code)},
        ],
        temperature=0.1,
        max_tokens=8192,
    )

    return _extract_svg(response.choices[0].message.content)


def _extract_svg(text: str) -> str:
    """Extract SVG from LLM response."""
    # Try markdown code blocks
    for pattern in [r'```svg\s*(.*?)\s*```', r'```xml\s*(.*?)\s*```', r'```\s*(.*?)\s*```']:
        match = re.search(pattern, text, re.DOTALL)
        if match and '<svg' in match.group(1):
            return match.group(1).strip()

    # Try direct SVG
    match = re.search(r'(<svg[\s\S]*?</svg>)', text)
    if match:
        return match.group(1).strip()

    if text.strip().startswith('<svg'):
        return text.strip()

    raise ValueError("Could not extract SVG from response")
