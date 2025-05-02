import re

def parse_entry(entry):
    entry = entry.replace("¾", "@")
    lines = entry.splitlines()

    # -------- Program Number --------
    program_number = ""
    match = re.match(r"\d{10}", lines[0].strip())
    if match:
        program_number = match.group()

    # -------- Program Name --------
    name_lines = []
    for line in lines[1:]:
        if re.search(r"\d{5}", line):  # if it looks like an address, stop
            break
        if "Ph:" in line or "Fax:" in line:
            break
        if "@" in line or "Email" in line:
            break
        name_lines.append(line.strip())
    program_name = " ".join(name_lines).strip()

    # -------- Email Address --------
    email = ""
    email_match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-z]{2,}", entry)
    if email_match:
        email = email_match.group()

    # -------- Program Director --------
    # The director appears below the email and above the "Accreditation Status"
    director = ""
    found_email = False
    for i, line in enumerate(lines):
        if email and email in line:
            found_email = True
            continue
        if found_email:
            if re.search(r"(MD|DO|MBBS|PhD|FACP|FAAP|FRCPC|DSc)", line):
                director = line.strip()
                break

    # -------- Preliminary Position --------
    prelim = ""
    for line in reversed(lines):
        match = re.search(r"\b(Yes|No)\b", line)
        if match:
            prelim = match.group()
            break

    return [program_number, program_name, director, email, prelim]
