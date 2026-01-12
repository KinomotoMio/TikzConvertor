# TikzConvertor

[English](#english) | [中文](#中文)

---

## English

### What is this?

**TikzConvertor** converts LaTeX TikZ code to SVG/PNG/HTML **without installing LaTeX**.

Perfect for:
- You have TikZ figures but don't want to install a 3GB+ LaTeX distribution
- You need to batch convert TikZ to web-friendly formats
- You want editable SVG output instead of rasterized images

### How it works

```
TikZ ──(LLM)──> SVG ──(resvg)──> PNG
                  └──(wrap)───> HTML
```

- **tikz2svg**: Uses LLM to understand TikZ and generate equivalent SVG
- **svg2png/svg2html**: Deterministic conversion, no LLM needed

### Installation

```bash
# Clone
git clone https://github.com/patchescamerababy/TikzConvertor.git
cd TikzConvertor

# Install (requires uv)
uv sync
```

### Usage

```bash
# TikZ → SVG (requires API key)
uv run tikzconv --mode tikz2svg --input figure.tex --api <your-api-key>

# SVG → PNG (no API needed)
uv run tikzconv --mode svg2png --input figure.svg

# SVG → HTML (no API needed)
uv run tikzconv --mode svg2html --input figure.svg

# TikZ → PNG directly
uv run tikzconv --mode tikz2png --input figure.tex --api <your-api-key>

# TikZ → HTML directly
uv run tikzconv --mode tikz2html --input figure.tex --api <your-api-key>

# Use different model
uv run tikzconv --mode tikz2svg --input figure.tex --api <key> --model openrouter/openai/gpt-4o
```

### Options

| Option | Description |
|--------|-------------|
| `--mode` | `tikz2svg`, `svg2png`, `svg2html`, `tikz2png`, `tikz2html` |
| `--input` | Input file path |
| `--output` | Output file path (default: same directory) |
| `--model` | LLM model (default: `openrouter/google/gemini-3-pro-preview`) |
| `--api` | API key (required for tikz* modes) |
| `--scale` | PNG scale factor (default: 2) |

### Supported Models

Any model supported by [LiteLLM](https://docs.litellm.ai/docs/providers):

```
openrouter/google/gemini-3-pro-preview  (default)
openrouter/anthropic/claude-sonnet-4
openrouter/openai/gpt-4o
openai/gpt-4o
anthropic/claude-sonnet-4
ollama/llama3
```

---

## 中文

### 这是什么？

**TikzConvertor** 可以将 LaTeX TikZ 代码转换为 SVG/PNG/HTML，**无需安装 LaTeX**。

适用场景：
- 有 TikZ 图但不想安装 3GB+ 的 LaTeX 发行版
- 需要批量将 TikZ 转换为网页友好格式
- 想要可编辑的 SVG 而不是栅格图像

### 工作原理

```
TikZ ──(LLM)──> SVG ──(resvg)──> PNG
                  └──(wrap)───> HTML
```

- **tikz2svg**: 使用 LLM 理解 TikZ 并生成等价的 SVG
- **svg2png/svg2html**: 确定性转换，无需 LLM

### 安装

```bash
# 克隆
git clone https://github.com/patchescamerababy/TikzConvertor.git
cd TikzConvertor

# 安装 (需要 uv)
uv sync
```

### 使用方法

```bash
# TikZ → SVG (需要 API key)
uv run tikzconv --mode tikz2svg --input figure.tex --api <your-api-key>

# SVG → PNG (无需 API)
uv run tikzconv --mode svg2png --input figure.svg

# SVG → HTML (无需 API)
uv run tikzconv --mode svg2html --input figure.svg

# TikZ → PNG 直接转换
uv run tikzconv --mode tikz2png --input figure.tex --api <your-api-key>

# TikZ → HTML 直接转换
uv run tikzconv --mode tikz2html --input figure.tex --api <your-api-key>

# 使用其他模型
uv run tikzconv --mode tikz2svg --input figure.tex --api <key> --model openrouter/openai/gpt-4o
```

### 参数说明

| 参数 | 说明 |
|------|------|
| `--mode` | `tikz2svg`, `svg2png`, `svg2html`, `tikz2png`, `tikz2html` |
| `--input` | 输入文件路径 |
| `--output` | 输出文件路径（默认：同目录） |
| `--model` | LLM 模型（默认：`openrouter/google/gemini-3-pro-preview`） |
| `--api` | API 密钥（tikz* 模式必需） |
| `--scale` | PNG 缩放倍数（默认：2） |

### 支持的模型

支持 [LiteLLM](https://docs.litellm.ai/docs/providers) 的所有模型：

```
openrouter/google/gemini-3-pro-preview  (默认)
openrouter/anthropic/claude-sonnet-4
openrouter/openai/gpt-4o
openai/gpt-4o
anthropic/claude-sonnet-4
ollama/llama3
```

---

## License

MIT
