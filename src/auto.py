import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from translate import translate

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


def translate_directory(from_dir, to_language):
    """
    Translate all files from a source directory to a target language.
    
    Args:
        from_dir (str): Source directory path (e.g., "original", "en-US")
        to_language (str): Target language code (e.g., "zh-CN", "pt-BR")
    
    Returns:
        dict: Summary of translation results
    """
    if not os.path.exists(from_dir):
        print(f"Error: Source directory '{from_dir}' does not exist.")
        return {"success": 0, "failed": 0, "errors": [f"Source directory '{from_dir}' does not exist."]}
    
    # Determine source language from directory path
    dir_parts = from_dir.split('/')
    source_language = 'en-US'  # Default to English
    relative_base = from_dir
    
    if len(dir_parts) > 0:
        first_part = dir_parts[0]
        for lang_code, _ in language_directories:
            if first_part == lang_code:
                source_language = lang_code
                relative_base = '/'.join(dir_parts[1:]) if len(dir_parts) > 1 else ''
                break
        
        if first_part == 'original':
            relative_base = '/'.join(dir_parts[1:]) if len(dir_parts) > 1 else ''
    
    success_count = 0
    failed_count = 0
    skipped_count = 0
    errors = []
    
    print(f"Starting batch translation from '{from_dir}' to '{to_language}'")
    print(f"Source language detected: {source_language}")
    print(f"Target language: {to_language}")
    print("-" * 60)
    
    # Collect all files to translate
    files_to_translate = []
    
    # Walk through all files in the source directory
    for root, dirs, files in os.walk(from_dir):
        for file in files:
            source_file = os.path.join(root, file)
            
            # Calculate relative path from the base directory
            rel_path = os.path.relpath(source_file, from_dir)
            if relative_base:
                target_file = os.path.join(to_language, relative_base, rel_path)
            else:
                target_file = os.path.join(to_language, rel_path)
            
            # Skip if target file already exists
            if os.path.exists(target_file):
                skipped_count += 1
                print(f"⏭ Skipping: {file} (target file already exists)")
                continue
            
            files_to_translate.append((source_file, target_file, source_language, to_language, file))
    
    # Translate files using multithreading
    max_workers = min(len(files_to_translate), 64)  # Limit to 64 concurrent threads
    
    def translate_file(args):
        source_file, target_file, source_lang, target_lang, filename = args
        try:
            print(f"\nTranslating: {source_file} -> {target_file}")
            result = translate(source_file, target_file, source_lang, target_lang)
            if result:
                return ("success", filename, None)
            else:
                return ("failed", filename, f"Translation failed for {filename}")
        except Exception as e:
            return ("failed", filename, f"Exception in {filename}: {str(e)}")
    
    if files_to_translate:
        print(f"\nStarting multithreaded translation with {max_workers} workers...")
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_file = {executor.submit(translate_file, args): args[4] for args in files_to_translate}
            
            for future in as_completed(future_to_file):
                filename = future_to_file[future]
                try:
                    status, file, error_msg = future.result()
                    if status == "success":
                        success_count += 1
                        print(f"✓ Success: {file}")
                    else:
                        failed_count += 1
                        print(f"✗ Failed: {file}")
                        if error_msg:
                            errors.append(error_msg)
                except Exception as e:
                    failed_count += 1
                    error_msg = f"✗ Exception processing {filename}: {str(e)}"
                    print(error_msg)
                    errors.append(error_msg)
    
    print("\n" + "=" * 60)
    print("BATCH TRANSLATION SUMMARY")
    print("=" * 60)
    print(f"Total files found: {success_count + failed_count + skipped_count}")
    print(f"Successful translations: {success_count}")
    print(f"Failed translations: {failed_count}")
    print(f"Skipped files (already exist): {skipped_count}")
    
    if errors:
        print(f"\nErrors encountered:")
        for error in errors:
            print(f"  - {error}")
    
    return {
        "success": success_count,
        "failed": failed_count,
        "skipped": skipped_count,
        "errors": errors
    }


def main():
    for lang_code, _ in language_directories:
        if lang_code == 'en-US':
            continue
        print(f"Translating en-US to {lang_code}\n")
        translate_directory("en-US", lang_code)
        print(f"Finished translating en-US to {lang_code}\n\n\n")


if __name__ == "__main__":
    # main()
    translate_directory("en-US", "ja-JP")
