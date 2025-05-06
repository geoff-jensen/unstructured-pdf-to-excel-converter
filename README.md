# 🩺 Residency Program PDF Parser

This project extracts structured data from a highly unstructured, multi-page residency program PDF. It was designed to meet real client-level requirements and gracefully handle inconsistent formatting, multi-line fields, and missing data.

## 📄 Project Purpose

Residency program directories are often published as poorly structured PDFs that defy traditional scraping tools. This parser transforms those messy blocks of text into a clean, structured CSV file suitable for spreadsheets, databases, or internal review.

## ✅ Output Fields

Each extracted program includes the following columns:

- **Program Number** – 10-digit identifier (e.g., 1402631204)
- **Program Name** – Full name including institution + specialty
- **Program Director Name** – Includes full name + credentials (e.g., MD, DO, PhD)
- **Email Address** – Valid email or `N/A` if not found
- **Preliminary Position** – `"Yes"` or `"No"` indicating whether prelim positions are offered

## 🔍 Parsing Strategy

The PDF is first saved as a `.txt` file to normalize text structure. From there, the parsing flow is:

1. **Split records** using `[10-digit number]` anchors
2. **Extract program name** using multi-line collection logic up to the last occurrence of the word “Program”
3. **Detect and extract** the email address
4. **Extract program director name** from the lines following the email (or phone if email is missing)
5. **Detect presence of “Yes” or “No”** for preliminary position
6. **Flag missing data** gracefully with `"N/A"`

### 🧠 Why This Is Hard

- The source document has **no tables**, just raw text in inconsistent formats
- Fields often **wrap across multiple lines**
- Some entries are **missing** email addresses or phone numbers entirely
- Words like “Program” appear multiple times, making line-bound logic unreliable

### ⚙️ Technologies Used

- Python 3
- Regular expressions (re)
- CSV module for export

## 📊 Sample Output

| Program Number | Program Name                              | Program Director Name     | Email Address                  | Preliminary Position |
|----------------|--------------------------------------------|----------------------------|-------------------------------|-----------------------|
| 1402631204     | Abbott Northwestern Hospital Program        | David M. Tierney, MD       | anwresidency@allina.com       | No                    |
| 1404112358     | Abington Memorial Hospital Program          | Rachel L. Ramirez, MD      | AMH-IMResidents@jefferson.edu | Yes                   |
| 1400511049     | Adventist Health White Memorial Program     | Juan C. Barrio, MD         | VillegS@ah.org                | Yes                   |

> See the full CSV in the [`parsed_programs.csv`](./parsed_programs.csv) output file.

## 🚧 Future Improvements

- Capture multiple degree suffixes with more robust pattern matching
- Add logging for entries with missing data
- Consider UI to let users upload new PDFs and export CSVs on demand

## 👤 Author

Developed by [Your Name], freelance Python developer focused on real-world automation, data extraction, and time-saving solutions.

---

Want to simplify your workflows or extract messy data from a nightmare document? Let’s connect!
