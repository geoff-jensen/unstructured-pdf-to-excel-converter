import re
import csv

# Load the plain text file
with open("test.txt", "r", encoding="utf-8") as f:
    full_text = f.read()

# Split into entries based on [10-digit number]
entries = re.split(r"\[(\d{10})\]", full_text)
paired_entries = [(entries[i], entries[i + 1]) for i in range(1, len(entries) - 1, 2)]

parsed_data = []

for program_number, block in paired_entries:
    lines = block.strip().splitlines()

    # ----- Program Name -----
    program_name_lines = []
    for line in lines:
        program_name_lines.append(line.strip())
        if "Program" in line:
            break

    program_name = " ".join(line.strip() for line in program_name_lines)
    program_name = re.sub(r"\s+", " ", program_name).strip()

    # ----- Email -----
    email_match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-z]{2,}", block)
    email = email_match.group() if email_match else ""

    # ----- Director Name -----
    director = ""
    if email:
        after_email = False
        collected = []
        for line in lines:
            if email in line:
                after_email = True
                continue
            if after_email:
                if any(word in line for word in ["Continued", "Initial", "Provisional"]):
                    break
                collected.append(line.strip())
        director = " ".join(collected).strip()
    else:
        # Fallback: collect after "Ph:" if no email
        after_phone = False
        collected = []
        for line in lines:
            if "Ph:" in line:
                after_phone = True
                continue
            if after_phone:
                if any(word in line for word in ["Continued", "Initial", "Provisional"]):
                    break
                collected.append(line.strip())
        director = " ".join(collected).strip()

    # ----- Preliminary Position -----
    prelim_match = re.search(r"\b(Yes|No)\b", block)
    prelim = prelim_match.group() if prelim_match else ""

    # ----- Flag if missing both email and phone -----
    phone_missing = not any("Ph:" in line for line in lines)
    flagged = "Missing email & phone" if not email and phone_missing else ""

    parsed_data.append([
        program_number,
        program_name,
        director,
        email if email else "N/A",
        prelim,
        flagged
    ])

# ----- Write to CSV -----
with open("parsed_programs.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([
        "Program Number",
        "Program Name",
        "Program Director Name",
        "Email Address",
        "Preliminary Position",
        "Flag"
    ])
    writer.writerows(parsed_data)

print("CSV file 'parsed_programs.csv' created successfully.")
