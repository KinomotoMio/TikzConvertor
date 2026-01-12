"""CLI for TikzConvertor."""

import argparse
from pathlib import Path

from .tikz2svg import tikz2svg
from .svg_utils import svg2png, svg2html

DEFAULT_MODEL = "openrouter/google/gemini-3-pro-preview"


def main():
    parser = argparse.ArgumentParser(description="Convert TikZ to SVG/PNG/HTML")
    parser.add_argument("--mode", required=True,
                        choices=["tikz2svg", "svg2png", "svg2html", "tikz2png", "tikz2html"],
                        help="Conversion mode")
    parser.add_argument("--input", required=True, help="Input file path")
    parser.add_argument("--output", help="Output file path or directory (default: same dir as input)")
    parser.add_argument("--model", default=DEFAULT_MODEL, help=f"LLM model (default: {DEFAULT_MODEL})")
    parser.add_argument("--api", help="API key (required for tikz2* modes)")
    parser.add_argument("--scale", type=int, default=2, help="PNG scale factor (default: 2)")

    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: {input_path} not found")
        return 1

    ext_map = {"tikz2svg": ".svg", "svg2png": ".png", "svg2html": ".html",
               "tikz2png": ".png", "tikz2html": ".html"}
    output_path = Path(args.output) if args.output else None

    # Check API key for tikz modes
    if args.mode.startswith("tikz") and not args.api:
        print("Error: --api required for tikz2* modes")
        return 1

    if input_path.is_dir():
        if args.mode.startswith("tikz"):
            input_files = sorted(
                list(input_path.glob("*.tex")) + list(input_path.glob("*.latex"))
            )
        else:
            input_files = sorted(input_path.glob("*.svg"))

        if not input_files:
            print(f"Error: no input files found in {input_path}")
            return 1

        if output_path and output_path.exists() and not output_path.is_dir():
            print("Error: --output must be a directory when --input is a directory")
            return 1

        output_dir = output_path if output_path else input_path
        output_dir.mkdir(parents=True, exist_ok=True)

        failed = False
        total = len(input_files)
        for idx, file_path in enumerate(input_files, start=1):
            current_output = output_dir / (file_path.stem + ext_map[args.mode])
            print(f"[{idx}/{total}] {file_path} -> {current_output}")
            try:
                content = file_path.read_text(encoding="utf-8")
                if args.mode == "tikz2svg":
                    result = tikz2svg(content, args.model, args.api)
                    current_output.write_text(result, encoding="utf-8")

                elif args.mode == "svg2png":
                    result = svg2png(content, args.scale)
                    current_output.write_bytes(result)

                elif args.mode == "svg2html":
                    result = svg2html(content)
                    current_output.write_text(result, encoding="utf-8")

                elif args.mode == "tikz2png":
                    svg = tikz2svg(content, args.model, args.api)
                    result = svg2png(svg, args.scale)
                    current_output.write_bytes(result)

                elif args.mode == "tikz2html":
                    svg = tikz2svg(content, args.model, args.api)
                    result = svg2html(svg)
                    current_output.write_text(result, encoding="utf-8")

            except Exception as e:
                failed = True
                print(f"Error: {file_path}: {e}")

        return 1 if failed else 0

    content = input_path.read_text(encoding="utf-8")
    output_path = output_path if output_path else input_path.with_suffix(ext_map[args.mode])
    if output_path.exists() and output_path.is_dir():
        output_path = output_path / (input_path.stem + ext_map[args.mode])

    try:
        if args.mode == "tikz2svg":
            result = tikz2svg(content, args.model, args.api)
            output_path.write_text(result, encoding="utf-8")

        elif args.mode == "svg2png":
            result = svg2png(content, args.scale)
            output_path.write_bytes(result)

        elif args.mode == "svg2html":
            result = svg2html(content)
            output_path.write_text(result, encoding="utf-8")

        elif args.mode == "tikz2png":
            svg = tikz2svg(content, args.model, args.api)
            result = svg2png(svg, args.scale)
            output_path.write_bytes(result)

        elif args.mode == "tikz2html":
            svg = tikz2svg(content, args.model, args.api)
            result = svg2html(svg)
            output_path.write_text(result, encoding="utf-8")

        print(f"Output: {output_path}")
        return 0

    except Exception as e:
        print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
