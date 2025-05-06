import re
import csv

# Read the full text file
with open("test.txt", "r", encoding="utf-8") as f:
    full_text = f.read()

# Split the file into entries using the program number in brackets as anchor
entries = re.split(r"\[(\d{10})\]", full_text)[1:]

# Group program number + content
grouped = list(zip(entries[0::2], entries[1::2]))

parsed_rows = []
for prog_number, content in grouped:
    content = content.strip().replace('\n', ' ')  # Flatten the entry into one string

    # Program Name: Starts at start of content, ends at first occurrence of 'Program'
    prog_name_match = re.search(r"(.*?\bProgram\b)", content)
    program_name = prog_name_match.group(1).strip() if prog_name_match else ""

    # Email
    email_match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-z]{2,}", content)
    email = email_match.group() if email_match else ""

    # Program Director Name: After email, before 'Continued' or similar
    director = ""
    if email:
        post_email = content.split(email)[-1]
        dir_match = re.search(r"([A-Z][a-z]+\s+[A-Z]\.\s+[A-Z][a-zA-Z.\- ]+?,\s*(MD|DO|MBBS|PhD|FACP|FAAP|FRCPC|DSc))", post_email)
        if dir_match:
            director = dir_match.group(1)
        else:
            # fallback: grab text between email and 'Continued'
            dir_fallback = re.search(rf"{re.escape(email)}(.*?)Continued", content)
            if dir_fallback:
                director = dir_fallback.group(1).strip()

    # Preliminary Position
    prelim_match = re.search(r"\b(Yes|No)\b", content)
    prelim = prelim_match.group(1) if prelim_match else ""

    parsed_rows.append([prog_number, program_name, director, email, prelim])

# Write to CSV
with open("parsed_residency_programs.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Program Number", "Program Name", "Program Director", "Email", "Preliminary Position"])
    writer.writerows(parsed_rows)

print(f"✅ Parsed {len(parsed_rows)} entries and wrote to parsed_residency_programs.csv")
