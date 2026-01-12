"""SVG conversion utilities (deterministic, no LLM)."""

from resvg_py import svg_to_bytes


def svg2png(svg_content: str, scale: int = 2) -> bytes:
    """Convert SVG to PNG."""
    return svg_to_bytes(svg_string=svg_content, zoom=scale)


def svg2html(svg_content: str) -> str:
    """Wrap SVG in HTML."""
    return f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>TikZ Figure</title>
    <style>
        body {{ display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; background: #f5f5f5; }}
        .container {{ background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
    </style>
</head>
<body>
    <div class="container">{svg_content}</div>
</body>
</html>'''
