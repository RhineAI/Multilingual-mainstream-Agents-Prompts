
import os
import sys
import time
from datetime import datetime

language_directories = [
    ('pt-BR', 'Portuguese (Brazil)'),
    ('ru-RU', 'Russian'),
    ('it-IT', 'Italian'),
    ('de-DE', 'German'),
    ('zh-HK', 'Chinese (Hong Kong)'),
    ('fr-FR', 'French'),
    ('es-ES', 'Spanish'),
    ('ko-KR', 'Korean'),
    ('ja-JP', 'Japanese'),
    ('zh-CN', 'Chinese (Simplified)'),
    ('en-US', 'English (United States)'),
]


def get_language_name(language):
    for lang, name in language_directories:
        if lang == language:
            return name
    return language


def translate(from_file, to_file, from_language, to_language):
    # Check if input file exists
    if not os.path.exists(from_file):
        print(f"Error: Input file '{from_file}' does not exist.")
        return False
    
    # Delete target file if it exists
    if os.path.exists(to_file):
        try:
            os.remove(to_file)
            print(f"Deleted existing target file: {to_file}")
        except OSError as e:
            print(f"Error deleting existing file '{to_file}': {e}")
            return False
    
    # Create output directory if it doesn't exist
    output_dir = os.path.dirname(to_file)
    if output_dir and not os.path.exists(output_dir):
        try:
            os.makedirs(output_dir, exist_ok=True)
            print(f"Created directory: {output_dir}")
        except OSError as e:
            print(f"Error creating directory '{output_dir}': {e}")
            return False
    
    from_language_name = get_language_name(from_language)
    to_language_name = get_language_name(to_language)
    
    # Record start time
    start_time = time.time()
    start_datetime = datetime.now()
    print(f"\n\nTranslation started at: {start_datetime.strftime('%Y-%m-%d %H:%M:%S')}")

    prompt = f"""
You are a helpful assistant that translates text from {from_language_name} to {to_language_name}.
    
Translate file "{from_file}" to "{to_file}".

Analyze the file to identify parts that need translation, such as JSON keys, placeholder markers, proper nouns, tool names, and similar elements that should not be translated. Everything else should be translated, including descriptive text or other natural language content within JSON files.
When translating, strictly follow the original order without skipping any content, and maintain the exact structure of the original file, including markdown formatting, JSON structure, and indentation.
Translate to the target language in a natural manner that conforms to the speaking habits of the corresponding language region. Use professional language while ensuring smooth and fluent sentences."""

    command = f"claude --dangerously-skip-permissions -p '{prompt}'"
    print(f"\nExecuting: {command}\n")
    
    try:
        result = os.system(command)
    except Exception as e:
        end_time = time.time()
        end_datetime = datetime.now()
        duration = end_time - start_time
        print(f"Translation ended at: {end_datetime.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Total duration: {duration:.2f} seconds")
        print(f"Error executing translation command: {e}")
        return False
    
    # Record end time and calculate duration
    end_time = time.time()
    end_datetime = datetime.now()
    duration = end_time - start_time
    
    print(f"\n\nTranslation ended at: {end_datetime.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Total duration: {duration:.2f} seconds")
    print()
    
    if result == 0:
        print(f"Translation completed successfully: {from_file} -> {to_file}")
        return True
    else:
        print(f"Translation failed with exit code: {result}")
        return False


def translate_easy(file, language):
    file_parts = file.split('/')
    
    source_language = 'en-US'  # Default to English
    relative_path = file
    
    if len(file_parts) > 0:
        first_part = file_parts[0]
        for lang_code, _ in language_directories:
            if first_part == lang_code:
                source_language = lang_code
                relative_path = '/'.join(file_parts[1:])
                break

        if first_part == 'original':
            relative_path = '/'.join(file_parts[1:])
    
    target_file = f"{language}/{relative_path}"
    
    return translate(file, target_file, source_language, language)


if __name__ == "__main__":
    translate_easy("en-US/Cursor Prompts/Chat Prompt.txt", "zh-CN")
    # translate("original/test.txt", "zh-CN/test.txt", "en-US", "zh-CN")

