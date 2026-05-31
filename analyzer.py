import re

def extract_legal_entities(full_text):
    strony = set()
    daty = set()

    date_patterns = [
        r'\b\d{2}[\.\-]\d{2}[\.\-]\d{4}\b',
        r'\b(\d{4})\s*r\.?\b'
    ]
    for pattern in date_patterns:
        found_dates = re.findall(pattern, full_text)
        for d in found_dates:
            val = d if isinstance(d, str) else d[0]
            daty.add(val.strip())

    company_pattern = r'\b[A-Za-zŻŹĆĄŚĘŁÓŃżźćąśęłón0-9\s\.\-]{3,30}(?:Sp\.\s*z\s*o\.\s*o\.|S\.A\.|S\.C\.)'
    companies = re.findall(company_pattern, full_text)
    for c in companies:
        strony.add(c.strip())

    names_pattern = r'(?:pomiędzy|a\s+firmą|a\s+panem|a\s+panią)\s+([A-ZŻŹĆĄŚĘŁÓŃ][a-zżźćąśęłón]+\s+[A-ZŻŹĆĄŚĘŁÓŃ][a-zżźćąśęłón]+)'
    names = re.findall(names_pattern, full_text)
    for n in names:
        strony.add(n.strip())

    return list(strony)[:4], list(daty)[:3]
