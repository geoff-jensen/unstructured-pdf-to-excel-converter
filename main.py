import re
import pdfplumber
from utils import parse_entry



with pdfplumber.open("PDF_TO_EXTRACT.pdf") as pdf:
    full_text = ""
    for page in pdf.pages:
        full_text += page.extract_text() + "\n"

print(full_text[:2000])
with open("output_preview.txt", "w", encoding="utf-8") as f:
    f.write(full_text[:2000])


# # Find just the program numbers (10 digits anywhere in the text)
# matches = re.findall(r"\d{10}", full_text)
# print(f"🔍 Found {len(matches)} 10-digit sequences. First few:")
# print(matches[:10])

# # Just break at each 10-digit number
# pattern = r"(\d{10}.*?)(?=\d{10}|$)"
# entries = re.findall(pattern, full_text, flags=re.DOTALL)

# print(f"✅ Found {len(entries)} program-like blocks.")
# for i in range(min(3, len(entries))):
#     print(f"\n--- Entry {i} ---\n{entries[i][:500]}")

# # for i in range(3):
# #     print(f"\n--- Parsed Entry {i} ---")
# #     print(parse_entry(entries[i]))