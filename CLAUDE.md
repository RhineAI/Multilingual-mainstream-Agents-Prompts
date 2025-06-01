# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository contains a multilingual collection of AI agent system prompts and tools from major platforms including v0, Cursor, Manus, Same.dev, Lovable, Devin, Replit Agent, Windsurf Agent, VSCode Agent, Dia Browser, and Trae AI. The project includes both original prompts and their translations into multiple languages.

## Architecture

### Directory Structure
- `original/` - Contains the original English prompts and tools
- Language directories (`en-US/`, `zh-CN/`, `pt-BR/`, `ru-RU/`, `it-IT/`, `de-DE/`, `zh-HK/`, `fr-FR/`, `es-ES/`, `ko-KR/`, `ja-JP/`) - Translated versions
- `src/` - Python translation automation scripts

### Translation System
The project uses a custom translation workflow powered by Claude CLI:
- `src/translate.py` - Core translation functions with timing and error handling
- `src/auto.py` - Batch translation automation (incomplete)
- Translation preserves file structure, JSON formatting, and technical terminology
- Supports 11 target languages with locale-specific adaptations

## Common Development Tasks

### Translation Operations

Run single file translation:
```bash
python src/translate.py
```

Translate specific file to target language:
```python
from src.translate import translate_easy
translate_easy("original/Cursor Prompts/Agent Prompt.txt", "zh-CN")
```

### Language Configuration
Supported language codes are defined in `language_directories` list in both translation scripts:
- `pt-BR` - Portuguese (Brazil)
- `ru-RU` - Russian
- `it-IT` - Italian
- `de-DE` - German
- `zh-HK` - Chinese (Hong Kong)
- `fr-FR` - French
- `es-ES` - Spanish
- `ko-KR` - Korean
- `ja-JP` - Japanese
- `zh-CN` - Chinese (Simplified)
- `en-US` - English (United States)

## Translation Workflow

The translation system:
1. Checks if source file exists
2. Deletes target file if it exists (prevents conflicts)
3. Creates target directory structure
4. Uses Claude CLI with specialized translation prompt
5. Records execution time and provides detailed logging
6. Maintains original file structure and formatting

When translating:
- Technical terms, tool names, and JSON keys are preserved
- File structure and indentation are maintained
- Natural language adaptation for target locale
- Professional tone and fluency prioritized