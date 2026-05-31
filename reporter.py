import json
import os

def load_patterns():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, "risk_patterns.json")
    with open(json_path, "r", encoding="utf-8-sig") as f:
        return json.load(f)

def analyze_contract_risks(pages_data):
    patterns = load_patterns()
    detected_risks = {cat: [] for cat in patterns}
    counters = {"Wysokie": 0, "Średnie": 0, "Niskie": 0}
    seen = set()

    severity_mapping = {
        "Kary umowne": "Wysokie",
        "Jednostronne prawa": "Wysokie",
        "Zgoda i Wypowiedzenie": "Średnie",
        "Ochrona danych i Poufność": "Niskie"
    }

    for page_num, text in pages_data.items():
        sentences = text.split("\n")
        for sentence in sentences:
            sentence_clean = sentence.strip()
            sentence_lower = sentence_clean.lower()

            if len(sentence_clean) < 15:
                continue

            display_text = sentence_clean[:150] + ("…" if len(sentence_clean) > 150 else "")

            for category, markers in patterns.items():
                for marker in markers:
                    if marker in sentence_lower:
                        key = (page_num, sentence_clean[:80], category)
                        if key in seen:
                            break
                        seen.add(key)

                        level = severity_mapping[category]
                        highlighted_text = display_text.replace(marker, f"**{marker}**")

                        detected_risks[category].append({
                            "text": highlighted_text,
                            "page": page_num,
                            "level": level,
                            "marker": marker
                        })
                        counters[level] += 1
                        break

    total_found = sum(len(v) for v in detected_risks.values())
    safety_score = max(100 - (total_found * 5), 20)

    return detected_risks, counters, safety_score
