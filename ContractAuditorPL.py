import streamlit as st
import matplotlib.pyplot as plt
from pdf_reader import extract_text_by_pages
from analyzer import extract_legal_entities
from reporter import analyze_contract_risks

st.set_page_config(page_title="Contract Auditor PL", layout="wide")

st.sidebar.title("📁 Contract Auditor")
st.sidebar.info("Aplikacja dedykowana do analizy polskich umów prawnych.")
st.sidebar.write("---")
st.sidebar.write("Wzorce ryzyk: **42 (Polskie prawo)**")
st.sidebar.write("Silnik NLP: **RegEx / Rule-based Parsing**")

st.title("Analiza umowy")
st.write("Wgraj plik PDF — aplikacja wykryje klauzule ryzyka i wygeneruje raport")

uploaded_file = st.file_uploader("", type="pdf", label_visibility="collapsed")

if uploaded_file is not None:
    file_bytes = uploaded_file.getvalue()
    
    pages_data = extract_text_by_pages(file_bytes)
    full_text = " ".join(pages_data.values())
    
    strony, daty = extract_legal_entities(full_text)
    
    st.sidebar.subheader("👤 Podmioty umowy (RegEx)")
    if strony:
        for strona in strony:
            st.sidebar.success(f"Strona: {strona}")
    else:
        st.sidebar.warning("Nie wykryto podmiotów")
        
    if daty:
        st.sidebar.write(f"⏱ Wykryte daty: {', '.join(daty)}")
        
    detected_risks, counters, safety_score = analyze_contract_risks(pages_data)
    
    st.write("---")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"<div style='border:1px solid #ddd; padding:15px; border-radius:8px; background-color:#fff5f5;'>Ryzyka wysokie<br><h1 style='color:#e74c3c; margin:0;'>{counters['Wysokie']}</h1></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div style='border:1px solid #ddd; padding:15px; border-radius:8px; background-color:#fffaf0;'>Ryzyka średnie<br><h1 style='color:#f39c12; margin:0;'>{counters['Średnie']}</h1></div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div style='border:1px solid #ddd; padding:15px; border-radius:8px; background-color:#f0f8ff;'>Ryzyka niskie<br><h1 style='color:#3498db; margin:0;'>{counters['Niskie']}</h1></div>", unsafe_allow_html=True)
    with col4:
        st.markdown(f"<div style='border:1px solid #ddd; padding:15px; border-radius:8px; background-color:#f5fff5;'>Safety Score<br><h1 style='color:#2ecc71; margin:0;'>{safety_score}%</h1></div>", unsafe_allow_html=True)

    st.write("---")
    
    st.subheader("Rozkład ryzyk według kategorii")
    categories = list(detected_risks.keys())
    counts = [len(detected_risks[cat]) for cat in categories]
    
    fig, ax = plt.subplots(figsize=(10, 2.5))
    colors = ['#e74c3c', '#e67e22', '#f1c40f', '#3498db']
    bars = ax.barh(categories, counts, color=colors, height=0.4)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.xaxis.set_visible(False)
    
    for bar in bars:
        width = bar.get_width()
        ax.text(width + 0.1, bar.get_y() + bar.get_height()/2, f'{int(width)}', va='center', ha='left', fontweight='bold')
        
    st.pyplot(fig)
    st.write("---")
    
    st.subheader("Wykryte klauzule ryzyka")
    
    any_risk = False
    for category, entries in detected_risks.items():
        for entry in entries:
            any_risk = True
            badge_color = "#e74c3c" if entry["level"] == "Wysokie" else "#f39c12" if entry["level"] == "Średnie" else "#3498db"
            
            st.markdown(f"""
            <div style="border-left: 5px solid {badge_color}; background-color: #fafafa; padding: 15px; margin-bottom: 12px; border-radius: 4px;">
                <span style="background-color: {badge_color}; color: white; padding: 2px 6px; border-radius: 3px; font-size: 11px; font-weight: bold;">{entry['level']}</span>
                <strong style="margin-left: 10px; color:#2c3e50;">Klauzula z grupy: {category}</strong>
                <p style="font-style: italic; margin-top: 8px; color: #333; line-height:1.5;">"{entry['text']}"</p>
                <small style="color: #777;">🎯 Wykryty znacznik: <u>{entry['marker']}</u> &nbsp;|&nbsp; 📄 <b>Lokalizacja: Strona {entry['page']}</b></small>
            </div>
            """, unsafe_allow_html=True)
            
    if not any_risk:
        st.info("Nie wykryto żadnych klauzul ryzyka w dokumencie.")
            
        st.write("---")
    
    report_text = f"RAPORT Z AUDYTU UMOWY\n"
    report_text += f"=====================\n\n"
    report_text += f"Bezpieczenstwo dokumentu (Safety Score): {safety_score}%\n"
    report_text += f"Wykryte ryzyka wysokie: {counters['Wysokie']}\n"
    report_text += f"Wykryte ryzyka srednie: {counters['Średnie']}\n"
    report_text += f"Wykryte ryzyka niskie: {counters['Niskie']}\n\n"
    report_text += f"SZCZEGOLY ANALIZY KLAUZUL:\n"
    report_text += f"--------------------------\n"
    
    for category, entries in detected_risks.items():
        for entry in entries:
            clean_txt = entry['text'].replace('**', '')
            report_text += f"[{entry['level']}] Grupa: {category} | Strona: {entry['page']}\n"
            report_text += f"Tresc: \"{clean_txt}\"\n"
            report_text += f"Znacznik: {entry['marker']}\n\n"

    st.download_button(
        label="📄 Pobierz raport z audytu",
        data=report_text,
        file_name="Raport_Audyt_Umowy.txt",
        mime="text/plain"
    )

else:
    st.info("Proszę wgrać plik umowy w formacie PDF, aby rozpocząć analizę.")
