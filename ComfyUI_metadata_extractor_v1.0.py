import sys, re, os
from PIL import Image

def read_metadata(file_path):
    """Reads and returns metadata from an image file."""
    try:
        with Image.open(file_path) as img:
            return img.info
    except Exception as e:
        return f"Error reading file {os.path.basename(file_path)}: {e}"

def extract_pattern_from_metadata(metadata, pattern):
    """Extracts a specific pattern from the metadata."""
    match = re.search(pattern, str(metadata), re.DOTALL)
    if match:
        return match.group()
    return "Pattern not found in metadata."

def clean_extracted_string(extracted_string):
    """Cleans the extracted string by removing unnecessary elements and spaces."""
    shortened_string = extracted_string[39:-13]
    return shortened_string.replace(', ', ',')

def save_to_file(content, file_name):
    """Appends the provided content to a text file."""
    try:
        with open(file_name, 'a') as file:
            file.write(content + "\n")
    except Exception as e:
        return f"Error writing to file: {e}"
    return f"Content appended to {file_name}"

def process_files(file_paths):
    """Processes each file and appends results to a common text file."""
    results_file = "results.txt"
    processed_count = 0
    for file_path in file_paths:
        file_name = os.path.basename(file_path)
        metadata = read_metadata(file_path)
        if isinstance(metadata, str):
            print(metadata)
            continue

        pattern = r"lora_clip_strength.+?negative"
        result = extract_pattern_from_metadata(metadata, pattern)

        if result == "Pattern not found in metadata.":
            print(f"{file_name}: {result}")
            continue

        cleaned_result = clean_extracted_string(result)
        save_message = save_to_file(f"{file_name}: {cleaned_result}", results_file)
        print(save_message)
        processed_count += 1

    # Write summary to the file
    summary_message = f"Total files processed: {processed_count}"
    save_to_file(summary_message, results_file)
    print(summary_message)

def main():
    if len(sys.argv) < 2:
        print("No file paths provided.")
        return

    file_paths = sys.argv[1:]
    process_files(file_paths)

if __name__ == "__main__":
    main()
