import re
import csv

# Load the text content
with open("test.txt", "r", encoding="utf-8") as f:
    text = f.read()

# Split entries by bracketed 10-digit number
entries = re.split(r"(?=\[\d{10}\])", text)

# Prepare output
output = []
for entry in entries:
    if not entry.strip():
        continue

    # Program Number
    program_number_match = re.search(r"\[(\d{10})\]", entry)
    program_number = program_number_match.group(1) if program_number_match else ""

    # Program Name (first line after bracket containing "Program")
    lines = entry.splitlines()
    program_name = ""
    for line in lines:
        if "Program" in line:
            program_name = line.strip()
            break

    # Email (anything ending in @domain)
    email_match = re.search(r"[\w\.-]+@[\w\.-]+\.\w+", entry)
    email = email_match.group() if email_match else ""

    # Program Director Name (after email until "Continued")
    director = ""
    if email:
        after_email = entry.split(email, 1)[-1]
        director_match = re.search(r"\n([A-Z][a-zA-Z.\- ]+,\s?(MD|DO|MBBS|PhD|FACP|FRCPC|FAAP))", after_email)
        if director_match:
            director = director_match.group(1).strip()

    # Preliminary Position
    prelim_match = re.search(r"\b(Yes|No)\b", entry, re.IGNORECASE)
    prelim = prelim_match.group().capitalize() if prelim_match else ""

    output.append([program_number, program_name, director, email, prelim])

# Write to CSV
with open("parsed_programs.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Program Number", "Program Name", "Program Director Name", "Email Address", "Preliminary Position"])
    writer.writerows(output)
