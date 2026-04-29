import streamlit as st
from groq import Groq
import unicodedata
import re
import pandas as pd
from datetime import datetime, date
import sqlite3
import json
import hashlib

# ── Configure ──────────────────────────────────────────────────
client = Groq(api_key="your groq key")

st.set_page_config(page_title="Government Scheme Finder", page_icon="🇮🇳", layout="wide")

# ══════════════════════════════════════════════════════════════
# LANGUAGE TRANSLATIONS
# ══════════════════════════════════════════════════════════════
LANG = {
    "English": {
        "app_title":        "Scheme Finder",
        "app_sub":          "AI-Powered • Free • Instant",
        "nav_find":         "🔍 Find Schemes",
        "nav_chat":         "💬 Chat Mode",
        "nav_compare":      "📊 Compare Schemes",
        "nav_family":       "👨‍👩‍👧 Family Comparison",
        "nav_apps":         "📁 My Applications",
        "nav_deadlines":    "📅 Scheme Deadlines",
        "nav_dashboard":    "📈 Dashboard",
        "your_stats":       "📊 Your Stats",
        "searches":         "🔍 Searches",
        "saved":            "💾 Saved",
        "applications":     "📁 Applications",
        "approved":         "✅ Approved",
        # Find Schemes
        "hero_find_title":  "Government <span>Scheme Finder</span>",
        "hero_find_sub":    "Fill your profile — AI finds every scheme you qualify for instantly.",
        "step1":            "① Personal Info",
        "step2":            "② Financial Info",
        "step3":            "③ AI Analysis",
        "step4":            "④ Results & PDF",
        "personal_info":    "👤 Personal Information",
        "financial_info":   "💼 Professional & Financial",
        "your_name":        "Your Name",
        "name_placeholder": "Enter your full name",
        "age":              "Age",
        "gender":           "Gender",
        "gender_opts":      ["Male", "Female", "Other"],
        "state":            "State",
        "occupation":       "Occupation",
        "annual_income":    "Annual Income (₹)",
        "category":         "Category",
        "category_opts":    ["General", "OBC", "SC", "ST"],
        "family_size":      "Family Size",
        "find_btn":         "🔍 Find My Schemes →",
        "warn_name":        "⚠️ Please enter your name!",
        "step_schemes":     "**Step 1/4** — Finding matching schemes...",
        "step_scores":      "**Step 2/4** — Calculating confidence scores...",
        "step_checklist":   "**Step 3/4** — Generating document checklist...",
        "step_elig":        "**Step 4/4** — Analyzing eligibility breakdown...",
        "found_schemes":    "✅ Found schemes for",
        "top_schemes":      "Top Matched Schemes",
        "confidence":       "Approval Confidence Scores",
        "save_btn":         "💾 Save",
        "already_saved":    "Already saved!",
        "saved_ok":         "✅ Saved!",
        "docs_needed":      "Documents You Will Need",
        "view_checklist":   "📄 View Full Document Checklist",
        "doc_tip":          "💡 **Tip:** Make 2 photocopies of each document. Keep originals safe!",
        "elig_breakdown":   "Eligibility Breakdown",
        "view_elig":        "🔍 View Detailed Eligibility Analysis",
        "download_report":  "Download Your Report",
        "download_pdf":     "📄 Download Full PDF Report",
        "high_chance":      "High Chance",
        "med_chance":       "Medium Chance",
        "low_chance":       "Low Chance",
        # Chat
        "hero_chat_title":  "💬 <span>Chat Mode</span>",
        "hero_chat_sub":    "No form filling needed — just describe yourself naturally!",
        "chat_example":     "💡 Example messages you can send:",
        "chat_ex1":         "\"I am a 28 year old woman farmer from Telangana, OBC category, income 80,000\"",
        "chat_ex2":         "\"నేను 45 సంవత్సరాల రైతుని, తెలంగాణ నుండి\"",
        "chat_ex3":         "\"Main 30 saal ka construction worker hoon, Bihar se, SC category\"",
        "chat_placeholder": "Describe yourself to find schemes...",
        "clear_chat":       "🗑️ Clear Chat",
        # Compare
        "hero_compare_title":"📊 <span>Compare Schemes</span>",
        "hero_compare_sub": "Side-by-side comparison of any 2-3 schemes.",
        "scheme1":          "Scheme 1",
        "scheme2":          "Scheme 2",
        "scheme3":          "Scheme 3 (optional)",
        "compare_btn":      "⚡ Compare Now",
        "compare_warn":     "Please enter at least 2 scheme names!",
        "compare_ready":    "✅ Comparison Ready!",
        "compare_table":    "Scheme Comparison Table",
        "compare_tip":      "💡 Go to **Find Schemes** to check your personal eligibility!",
        # Family
        "hero_fam_title":   "👨‍👩‍👧 <span>Family Comparison</span>",
        "hero_fam_sub":     "Compare schemes for 2 family members — see who qualifies for what!",
        "member1":          "👤 Member 1",
        "member2":          "👤 Member 2",
        "state_both":       "State (both)",
        "compare_fam_btn":  "🔍 Compare Family Members",
        "fam_warn":         "Please enter names for both members!",
        "fam_done":         "✅ Family comparison done!",
        "profile_compare":  "Profile Comparison",
        "ai_analysis":      "AI Scheme Analysis",
        "clear_results":    "🗑️ Clear Results",
        # Applications
        "hero_apps_title":  "📁 <span>My Applications</span>",
        "hero_apps_sub":    "Track every scheme you've applied for — status, notes, reference numbers.",
        "add_app":          "➕ Add New Application",
        "scheme_name":      "Scheme Name",
        "app_date":         "Application Date",
        "status":           "Status",
        "status_opts":      ["Applied", "Pending", "Approved", "Rejected"],
        "ref_num":          "Reference Number (optional)",
        "exp_benefit":      "Expected Benefit (optional)",
        "notes":            "Notes",
        "add_app_btn":      "➕ Add Application",
        "app_warn":         "Please enter the scheme name!",
        "no_apps":          "No applications yet. Add your first one above!",
        "summary":          "Summary",
        "total_apps":       "Total Applications",
        "your_apps":        "Your Applications",
        "update_status":    "Update Status",
        "delete":           "🗑️ Delete",
        # Deadlines
        "hero_dl_title":    "📅 <span>Scheme Deadlines</span>",
        "hero_dl_sub":      "Never miss an application window — color-coded urgency alerts.",
        "your_state":       "Your State",
        "your_occ":         "Your Occupation",
        "check_dl_btn":     "🔔 Check Deadlines",
        "dl_ready":         "✅ Deadline alerts ready!",
        "upcoming_dl":      "Upcoming Deadlines",
        "deadline":         "Deadline",
        "urgency":          "Urgency",
        "benefit":          "Benefit",
        "action":           "Action",
        # Dashboard
        "hero_dash_title":  "📈 <span>Your Dashboard</span>",
        "hero_dash_sub":    "Complete overview of your searches, saved schemes and applications.",
        "saved_schemes":    "Saved Schemes",
        "no_saved":         "No saved schemes yet. Go to **Find Schemes** and click 💾 Save!",
        "recent_searches":  "Recent Searches",
        "no_searches":      "No searches yet.",
        "app_chart":        "Application Status Chart",
        "no_chart":         "No applications tracked yet.",
        "ai_insights":      "AI Insights",
        "gen_insights":     "🔮 Generate Personalized AI Insights",
        "no_insights":      "Go to **Find Schemes** first to get AI insights!",
        "reset":            "Reset",
        "clear_all":        "🗑️ Clear All My Data",
        "cleared":          "All data cleared!",
        "language":         "🌐 Language",
        "auth_title":       "🔐 Login / Register",
        "auth_sub":         "Create an account to save data permanently with SQLite.",
        "login_tab":        "Login",
        "register_tab":     "Register",
        "username":         "Username",
        "password":         "Password",
        "confirm_password": "Confirm Password",
        "login_btn":        "🔓 Login",
        "register_btn":     "📝 Register",
        "logout_btn":       "🚪 Logout",
        "auth_needed":      "Please login to continue.",
        "user_exists":      "Username already exists.",
        "register_ok":      "Registration successful. Please login.",
        "invalid_login":    "Invalid username or password.",
        "pwd_mismatch":     "Passwords do not match.",
        "pwd_short":        "Password must be at least 6 characters.",
        "welcome_user":     "Welcome",
    },
    "తెలుగు": {
        "app_title":        "స్కీమ్ ఫైండర్",
        "app_sub":          "AI ఆధారిత • ఉచితం • తక్షణం",
        "nav_find":         "🔍 స్కీమ్‌లు కనుగొనండి",
        "nav_chat":         "💬 చాట్ మోడ్",
        "nav_compare":      "📊 స్కీమ్‌లు పోల్చండి",
        "nav_family":       "👨‍👩‍👧 కుటుంబ పోలిక",
        "nav_apps":         "📁 నా దరఖాస్తులు",
        "nav_deadlines":    "📅 గడువు తేదీలు",
        "nav_dashboard":    "📈 డాష్‌బోర్డ్",
        "your_stats":       "📊 మీ గణాంకాలు",
        "searches":         "🔍 శోధనలు",
        "saved":            "💾 సేవ్ చేసినవి",
        "applications":     "📁 దరఖాస్తులు",
        "approved":         "✅ ఆమోదించబడినవి",
        "hero_find_title":  "ప్రభుత్వ <span>స్కీమ్ ఫైండర్</span>",
        "hero_find_sub":    "మీ వివరాలు నమోదు చేయండి — AI వెంటనే మీకు అర్హమైన స్కీమ్‌లు కనుగొంటుంది.",
        "step1":            "① వ్యక్తిగత వివరాలు",
        "step2":            "② ఆర్థిక వివరాలు",
        "step3":            "③ AI విశ్లేషణ",
        "step4":            "④ ఫలితాలు & PDF",
        "personal_info":    "👤 వ్యక్తిగత సమాచారం",
        "financial_info":   "💼 వృత్తి & ఆర్థిక వివరాలు",
        "your_name":        "మీ పేరు",
        "name_placeholder": "మీ పూర్తి పేరు నమోదు చేయండి",
        "age":              "వయసు",
        "gender":           "లింగం",
        "gender_opts":      ["పురుషుడు", "స్త్రీ", "ఇతర"],
        "state":            "రాష్ట్రం",
        "occupation":       "వృత్తి",
        "annual_income":    "వార్షిక ఆదాయం (₹)",
        "category":         "వర్గం",
        "category_opts":    ["జనరల్", "OBC", "SC", "ST"],
        "family_size":      "కుటుంబ సభ్యుల సంఖ్య",
        "find_btn":         "🔍 నా స్కీమ్‌లు కనుగొనండి →",
        "warn_name":        "⚠️ దయచేసి మీ పేరు నమోదు చేయండి!",
        "step_schemes":     "**దశ 1/4** — సరిపోలే స్కీమ్‌లు వెతుకుతున్నాం...",
        "step_scores":      "**దశ 2/4** — విశ్వాస స్కోర్లు లెక్కిస్తున్నాం...",
        "step_checklist":   "**దశ 3/4** — పత్రాల జాబితా తయారు చేస్తున్నాం...",
        "step_elig":        "**దశ 4/4** — అర్హత విశ్లేషణ చేస్తున్నాం...",
        "found_schemes":    "✅ స్కీమ్‌లు కనుగొనబడ్డాయి",
        "top_schemes":      "అగ్ర స్కీమ్‌లు",
        "confidence":       "ఆమోద విశ్వాస స్కోర్లు",
        "save_btn":         "💾 సేవ్ చేయి",
        "already_saved":    "ఇప్పటికే సేవ్ చేయబడింది!",
        "saved_ok":         "✅ సేవ్ చేయబడింది!",
        "docs_needed":      "అవసరమైన పత్రాలు",
        "view_checklist":   "📄 పత్రాల జాబితా చూడండి",
        "doc_tip":          "💡 **చిట్కా:** ప్రతి పత్రానికి 2 జిరాక్స్ కాపీలు తీయండి!",
        "elig_breakdown":   "అర్హత వివరాలు",
        "view_elig":        "🔍 అర్హత విశ్లేషణ చూడండి",
        "download_report":  "రిపోర్ట్ డౌన్‌లోడ్ చేయండి",
        "download_pdf":     "📄 PDF రిపోర్ట్ డౌన్‌లోడ్ చేయండి",
        "high_chance":      "అధిక అవకాశం",
        "med_chance":       "మధ్యస్థ అవకాశం",
        "low_chance":       "తక్కువ అవకాశం",
        "hero_chat_title":  "💬 <span>చాట్ మోడ్</span>",
        "hero_chat_sub":    "ఫారం అవసరం లేదు — సహజంగా మాట్లాడండి!",
        "chat_example":     "💡 మీరు ఇలా టైప్ చేయవచ్చు:",
        "chat_ex1":         "\"నేను 28 సంవత్సరాల మహిళా రైతుని, తెలంగాణ నుండి, OBC, ఆదాయం 80,000\"",
        "chat_ex2":         "\"నేను 45 సంవత్సరాల నిర్మాణ కార్మికుడిని, SC వర్గం\"",
        "chat_ex3":         "\"I am a 30 year old student from Telangana\"",
        "chat_placeholder": "మీ గురించి చెప్పండి...",
        "clear_chat":       "🗑️ చాట్ క్లియర్ చేయి",
        "hero_compare_title":"📊 <span>స్కీమ్‌లు పోల్చండి</span>",
        "hero_compare_sub": "ఏదైనా 2-3 స్కీమ్‌లను పక్కపక్కన పోల్చండి.",
        "scheme1":          "స్కీమ్ 1",
        "scheme2":          "స్కీమ్ 2",
        "scheme3":          "స్కీమ్ 3 (ఐచ్ఛికం)",
        "compare_btn":      "⚡ ఇప్పుడే పోల్చండి",
        "compare_warn":     "దయచేసి కనీసం 2 స్కీమ్ పేర్లు నమోదు చేయండి!",
        "compare_ready":    "✅ పోలిక సిద్ధం!",
        "compare_table":    "స్కీమ్ పోలిక పట్టిక",
        "compare_tip":      "💡 మీ వ్యక్తిగత అర్హత తనిఖీకి **స్కీమ్‌లు కనుగొనండి** కి వెళ్ళండి!",
        "hero_fam_title":   "👨‍👩‍👧 <span>కుటుంబ పోలిక</span>",
        "hero_fam_sub":     "2 కుటుంబ సభ్యుల స్కీమ్‌లు పోల్చండి!",
        "member1":          "👤 సభ్యుడు 1",
        "member2":          "👤 సభ్యుడు 2",
        "state_both":       "రాష్ట్రం (ఇద్దరికీ)",
        "compare_fam_btn":  "🔍 కుటుంబ సభ్యులను పోల్చండి",
        "fam_warn":         "దయచేసి ఇద్దరి పేర్లు నమోదు చేయండి!",
        "fam_done":         "✅ కుటుంబ పోలిక పూర్తయింది!",
        "profile_compare":  "ప్రొఫైల్ పోలిక",
        "ai_analysis":      "AI స్కీమ్ విశ్లేషణ",
        "clear_results":    "🗑️ ఫలితాలు తొలగించండి",
        "hero_apps_title":  "📁 <span>నా దరఖాస్తులు</span>",
        "hero_apps_sub":    "మీరు దరఖాస్తు చేసిన ప్రతి స్కీమ్‌ను ట్రాక్ చేయండి.",
        "add_app":          "➕ కొత్త దరఖాస్తు జోడించండి",
        "scheme_name":      "స్కీమ్ పేరు",
        "app_date":         "దరఖాస్తు తేదీ",
        "status":           "స్థితి",
        "status_opts":      ["దరఖాస్తు చేసారు", "పెండింగ్", "ఆమోదించబడింది", "తిరస్కరించబడింది"],
        "ref_num":          "రిఫరెన్స్ నంబర్ (ఐచ్ఛికం)",
        "exp_benefit":      "ఆశించిన లాభం (ఐచ్ఛికం)",
        "notes":            "గమనికలు",
        "add_app_btn":      "➕ దరఖాస్తు జోడించండి",
        "app_warn":         "దయచేసి స్కీమ్ పేరు నమోదు చేయండి!",
        "no_apps":          "ఇంకా దరఖాస్తులు లేవు. పైన మొదటిది జోడించండి!",
        "summary":          "సారాంశం",
        "total_apps":       "మొత్తం దరఖాస్తులు",
        "your_apps":        "మీ దరఖాస్తులు",
        "update_status":    "స్థితి నవీకరించండి",
        "delete":           "🗑️ తొలగించు",
        "hero_dl_title":    "📅 <span>స్కీమ్ గడువు తేదీలు</span>",
        "hero_dl_sub":      "ఏ దరఖాస్తు విండో మిస్ అవ్వకండి — రంగు-కోడెడ్ హెచ్చరికలు.",
        "your_state":       "మీ రాష్ట్రం",
        "your_occ":         "మీ వృత్తి",
        "check_dl_btn":     "🔔 గడువు తేదీలు తనిఖీ చేయండి",
        "dl_ready":         "✅ గడువు హెచ్చరికలు సిద్ధం!",
        "upcoming_dl":      "రాబోయే గడువు తేదీలు",
        "deadline":         "గడువు తేదీ",
        "urgency":          "అత్యవసరత",
        "benefit":          "లాభం",
        "action":           "చర్య",
        "hero_dash_title":  "📈 <span>మీ డాష్‌బోర్డ్</span>",
        "hero_dash_sub":    "మీ శోధనలు, సేవ్ చేసిన స్కీమ్‌లు మరియు దరఖాస్తుల పూర్తి అవలోకనం.",
        "saved_schemes":    "సేవ్ చేసిన స్కీమ్‌లు",
        "no_saved":         "ఇంకా స్కీమ్‌లు సేవ్ చేయలేదు. **స్కీమ్‌లు కనుగొనండి** లో 💾 క్లిక్ చేయండి!",
        "recent_searches":  "ఇటీవలి శోధనలు",
        "no_searches":      "ఇంకా శోధనలు లేవు.",
        "app_chart":        "దరఖాస్తు స్థితి చార్ట్",
        "no_chart":         "ఇంకా దరఖాస్తులు ట్రాక్ చేయలేదు.",
        "ai_insights":      "AI అంతర్దృష్టులు",
        "gen_insights":     "🔮 వ్యక్తిగత AI అంతర్దృష్టులు పొందండి",
        "no_insights":      "AI అంతర్దృష్టులకు ముందు **స్కీమ్‌లు కనుగొనండి** కి వెళ్ళండి!",
        "reset":            "రీసెట్",
        "clear_all":        "🗑️ అన్ని డేటా తొలగించండి",
        "cleared":          "అన్ని డేటా తొలగించబడింది!",
        "language":         "🌐 భాష",
    },
    "हिंदी": {
        "app_title":        "स्कीम फाइंडर",
        "app_sub":          "AI आधारित • मुफ्त • तत्काल",
        "nav_find":         "🔍 स्कीम खोजें",
        "nav_chat":         "💬 चैट मोड",
        "nav_compare":      "📊 स्कीम तुलना",
        "nav_family":       "👨‍👩‍👧 परिवार तुलना",
        "nav_apps":         "📁 मेरे आवेदन",
        "nav_deadlines":    "📅 अंतिम तिथियाँ",
        "nav_dashboard":    "📈 डैशबोर्ड",
        "your_stats":       "📊 आपके आँकड़े",
        "searches":         "🔍 खोजें",
        "saved":            "💾 सहेजे",
        "applications":     "📁 आवेदन",
        "approved":         "✅ स्वीकृत",
        "hero_find_title":  "सरकारी <span>स्कीम फाइंडर</span>",
        "hero_find_sub":    "अपनी जानकारी भरें — AI तुरंत आपकी पात्र स्कीमें ढूंढेगा।",
        "step1":            "① व्यक्तिगत जानकारी",
        "step2":            "② वित्तीय जानकारी",
        "step3":            "③ AI विश्लेषण",
        "step4":            "④ परिणाम और PDF",
        "personal_info":    "👤 व्यक्तिगत जानकारी",
        "financial_info":   "💼 पेशे और वित्तीय विवरण",
        "your_name":        "आपका नाम",
        "name_placeholder": "अपना पूरा नाम दर्ज करें",
        "age":              "आयु",
        "gender":           "लिंग",
        "gender_opts":      ["पुरुष", "महिला", "अन्य"],
        "state":            "राज्य",
        "occupation":       "पेशा",
        "annual_income":    "वार्षिक आय (₹)",
        "category":         "वर्ग",
        "category_opts":    ["सामान्य", "OBC", "SC", "ST"],
        "family_size":      "परिवार के सदस्य",
        "find_btn":         "🔍 मेरी स्कीमें खोजें →",
        "warn_name":        "⚠️ कृपया अपना नाम दर्ज करें!",
        "step_schemes":     "**चरण 1/4** — मिलती-जुलती स्कीमें ढूंढ रहे हैं...",
        "step_scores":      "**चरण 2/4** — विश्वास स्कोर गणना कर रहे हैं...",
        "step_checklist":   "**चरण 3/4** — दस्तावेज़ सूची तैयार कर रहे हैं...",
        "step_elig":        "**चरण 4/4** — पात्रता विश्लेषण कर रहे हैं...",
        "found_schemes":    "✅ स्कीमें मिली",
        "top_schemes":      "शीर्ष मिलान स्कीमें",
        "confidence":       "अनुमोदन विश्वास स्कोर",
        "save_btn":         "💾 सहेजें",
        "already_saved":    "पहले से सहेजा गया!",
        "saved_ok":         "✅ सहेजा गया!",
        "docs_needed":      "आवश्यक दस्तावेज़",
        "view_checklist":   "📄 पूरी दस्तावेज़ सूची देखें",
        "doc_tip":          "💡 **सुझाव:** हर दस्तावेज़ की 2 फोटोकॉपी बनाएं!",
        "elig_breakdown":   "पात्रता विवरण",
        "view_elig":        "🔍 विस्तृत पात्रता विश्लेषण देखें",
        "download_report":  "रिपोर्ट डाउनलोड करें",
        "download_pdf":     "📄 PDF रिपोर्ट डाउनलोड करें",
        "high_chance":      "उच्च संभावना",
        "med_chance":       "मध्यम संभावना",
        "low_chance":       "कम संभावना",
        "hero_chat_title":  "💬 <span>चैट मोड</span>",
        "hero_chat_sub":    "फॉर्म भरने की जरूरत नहीं — बस अपने बारे में बताएं!",
        "chat_example":     "💡 आप इस तरह टाइप कर सकते हैं:",
        "chat_ex1":         "\"मैं 28 साल का किसान हूँ, तेलंगाना से, OBC वर्ग, आय 80,000\"",
        "chat_ex2":         "\"Main 45 saal ka mazdoor hoon, Bihar se, SC category\"",
        "chat_ex3":         "\"I am a 30 year old student from UP\"",
        "chat_placeholder": "अपने बारे में बताएं...",
        "clear_chat":       "🗑️ चैट साफ़ करें",
        "hero_compare_title":"📊 <span>स्कीम तुलना</span>",
        "hero_compare_sub": "किसी भी 2-3 स्कीमों की आमने-सामने तुलना।",
        "scheme1":          "स्कीम 1",
        "scheme2":          "स्कीम 2",
        "scheme3":          "स्कीम 3 (वैकल्पिक)",
        "compare_btn":      "⚡ अभी तुलना करें",
        "compare_warn":     "कृपया कम से कम 2 स्कीम नाम दर्ज करें!",
        "compare_ready":    "✅ तुलना तैयार!",
        "compare_table":    "स्कीम तुलना तालिका",
        "compare_tip":      "💡 अपनी व्यक्तिगत पात्रता जांचने के लिए **स्कीम खोजें** पर जाएं!",
        "hero_fam_title":   "👨‍👩‍👧 <span>परिवार तुलना</span>",
        "hero_fam_sub":     "2 परिवार के सदस्यों की स्कीमें तुलना करें!",
        "member1":          "👤 सदस्य 1",
        "member2":          "👤 सदस्य 2",
        "state_both":       "राज्य (दोनों के लिए)",
        "compare_fam_btn":  "🔍 परिवार के सदस्यों की तुलना करें",
        "fam_warn":         "कृपया दोनों सदस्यों के नाम दर्ज करें!",
        "fam_done":         "✅ परिवार तुलना पूर्ण!",
        "profile_compare":  "प्रोफ़ाइल तुलना",
        "ai_analysis":      "AI स्कीम विश्लेषण",
        "clear_results":    "🗑️ परिणाम साफ़ करें",
        "hero_apps_title":  "📁 <span>मेरे आवेदन</span>",
        "hero_apps_sub":    "हर स्कीम का आवेदन ट्रैक करें — स्थिति, नोट्स, संदर्भ नंबर।",
        "add_app":          "➕ नया आवेदन जोड़ें",
        "scheme_name":      "स्कीम का नाम",
        "app_date":         "आवेदन की तारीख",
        "status":           "स्थिति",
        "status_opts":      ["आवेदन किया", "लंबित", "स्वीकृत", "अस्वीकृत"],
        "ref_num":          "संदर्भ नंबर (वैकल्पिक)",
        "exp_benefit":      "अपेक्षित लाभ (वैकल्पिक)",
        "notes":            "नोट्स",
        "add_app_btn":      "➕ आवेदन जोड़ें",
        "app_warn":         "कृपया स्कीम का नाम दर्ज करें!",
        "no_apps":          "अभी तक कोई आवेदन नहीं। ऊपर पहला जोड़ें!",
        "summary":          "सारांश",
        "total_apps":       "कुल आवेदन",
        "your_apps":        "आपके आवेदन",
        "update_status":    "स्थिति अपडेट करें",
        "delete":           "🗑️ हटाएं",
        "hero_dl_title":    "📅 <span>स्कीम अंतिम तिथियाँ</span>",
        "hero_dl_sub":      "कोई भी आवेदन विंडो मिस न करें — रंग-कोडेड अलर्ट।",
        "your_state":       "आपका राज्य",
        "your_occ":         "आपका पेशा",
        "check_dl_btn":     "🔔 अंतिम तिथियाँ जांचें",
        "dl_ready":         "✅ अंतिम तिथि अलर्ट तैयार!",
        "upcoming_dl":      "आगामी अंतिम तिथियाँ",
        "deadline":         "अंतिम तिथि",
        "urgency":          "तात्कालिकता",
        "benefit":          "लाभ",
        "action":           "कार्रवाई",
        "hero_dash_title":  "📈 <span>आपका डैशबोर्ड</span>",
        "hero_dash_sub":    "आपकी खोजों, सहेजी गई स्कीमों और आवेदनों का पूरा अवलोकन।",
        "saved_schemes":    "सहेजी गई स्कीमें",
        "no_saved":         "अभी तक कोई स्कीम नहीं सहेजी। **स्कीम खोजें** में 💾 क्लिक करें!",
        "recent_searches":  "हालिया खोजें",
        "no_searches":      "अभी तक कोई खोज नहीं।",
        "app_chart":        "आवेदन स्थिति चार्ट",
        "no_chart":         "अभी तक कोई आवेदन ट्रैक नहीं किया।",
        "ai_insights":      "AI अंतर्दृष्टि",
        "gen_insights":     "🔮 व्यक्तिगत AI अंतर्दृष्टि प्राप्त करें",
        "no_insights":      "AI अंतर्दृष्टि के लिए पहले **स्कीम खोजें** पर जाएं!",
        "reset":            "रीसेट",
        "clear_all":        "🗑️ सारा डेटा साफ़ करें",
        "cleared":          "सारा डेटा साफ़ हो गया!",
        "language":         "🌐 भाषा",
    }
}

# ── CSS ────────────────────────────────────────────────────────
st.markdown("""<style>
    .stApp{background-color:#0A0E1A;color:#CBD5E1;}
    .main{background-color:#0A0E1A;}
    #MainMenu{visibility:hidden;}footer{visibility:hidden;}
    section[data-testid="stSidebar"]{background:linear-gradient(180deg,#0D1528 0%,#0A0E1A 100%);border-right:1px solid #1E2A3A;}
    section[data-testid="stSidebar"] .stRadio label{background:#111827;border:1px solid #1E2A3A;border-radius:8px;padding:10px 14px;margin:4px 0;display:block;transition:all 0.2s;cursor:pointer;color:#CBD5E1 !important;font-size:14px;}
    section[data-testid="stSidebar"] .stRadio label:hover{border-color:#00F5FF;background:#1A2235;color:#00F5FF !important;}
    .hero-banner{background:linear-gradient(135deg,#0D1F3C 0%,#1A0A2E 50%,#0A1A2E 100%);border:1px solid #1E2A3A;border-left:5px solid #00F5FF;border-radius:16px;padding:32px 36px;margin-bottom:24px;position:relative;overflow:hidden;}
    .hero-title{font-size:2.4rem;font-weight:800;color:#FFFFFF;margin:0 0 8px 0;line-height:1.2;}
    .hero-title span{color:#00F5FF;}
    .hero-sub{font-size:1rem;color:#8A9BB5;margin:0 0 20px 0;}
    .hero-tags{display:flex;gap:10px;flex-wrap:wrap;}
    .hero-tag{background:#1A2235;border:1px solid #2D3F5A;border-radius:20px;padding:4px 14px;font-size:12px;color:#00F5FF;font-weight:600;}
    .scheme-card{background:#111827;border:1px solid #1E2A3A;border-left:4px solid #00F5FF;border-radius:12px;padding:20px 24px;margin:12px 0;}
    .scheme-card:hover{border-left-color:#7C3AED;}
    .scheme-card-title{font-size:1.05rem;font-weight:700;color:#FFFFFF;margin-bottom:8px;}
    .scheme-card-body{font-size:0.9rem;color:#8A9BB5;line-height:1.6;}
    .badge{display:inline-block;padding:4px 14px;border-radius:20px;font-size:12px;font-weight:700;}
    .badge-applied{background:#1A2A4A;color:#60A5FA;border:1px solid #3B82F6;}
    .badge-pending{background:#2A2000;color:#FFD60A;border:1px solid #FFD60A;}
    .badge-approved{background:#002A1A;color:#00FF94;border:1px solid #00FF94;}
    .badge-rejected{background:#2A0015;color:#F72585;border:1px solid #F72585;}
    .metric-card{background:#111827;border:1px solid #1E2A3A;border-radius:12px;padding:20px;text-align:center;}
    .metric-card:hover{border-color:#00F5FF;}
    .metric-num{font-size:2.2rem;font-weight:800;color:#00F5FF;}
    .metric-label{font-size:0.85rem;color:#6B7280;margin-top:4px;}
    .section-header{display:flex;align-items:center;gap:10px;margin:28px 0 16px 0;}
    .section-header-line{flex:1;height:1px;background:linear-gradient(90deg,#1E2A3A,transparent);}
    .section-header-text{font-size:1.1rem;font-weight:700;color:#FFFFFF;white-space:nowrap;}
    .score-row{background:#111827;border:1px solid #1E2A3A;border-radius:10px;padding:14px 18px;margin:8px 0;}
    .score-label{font-size:0.9rem;font-weight:600;color:#FFFFFF;margin-bottom:6px;}
    .score-bar-bg{background:#1E2A3A;border-radius:6px;height:8px;width:100%;overflow:hidden;}
    .score-bar-fill{height:8px;border-radius:6px;}
    .score-caption{font-size:0.78rem;color:#6B7280;margin-top:5px;}
    .step-bar{display:flex;gap:0;margin-bottom:28px;background:#111827;border:1px solid #1E2A3A;border-radius:10px;overflow:hidden;}
    .step-item{flex:1;padding:10px 8px;text-align:center;font-size:12px;color:#6B7280;border-right:1px solid #1E2A3A;}
    .step-item:last-child{border-right:none;}
    .step-item.active{background:#1A2235;color:#00F5FF;font-weight:700;}
    .step-item.done{background:#001A12;color:#00FF94;}
    .deadline-card{background:#111827;border:1px solid #1E2A3A;border-radius:12px;padding:18px 22px;margin:10px 0;}
    .deadline-card-title{font-size:1rem;font-weight:700;color:#FFFFFF;margin-bottom:12px;}
    div[data-testid="stExpander"]{background:#111827;border:1px solid #1E2A3A !important;border-radius:10px !important;}
    div[data-testid="stExpander"] div[data-testid="stMarkdown"]{font-size:0.92rem !important;line-height:1.6 !important;}
    .stButton>button{border-radius:8px !important;font-weight:600 !important;}
    .sidebar-logo{text-align:center;padding:10px 0 20px 0;}
    .sidebar-logo-title{font-size:1.1rem;font-weight:800;color:#00F5FF;}
    .sidebar-logo-sub{font-size:0.75rem;color:#6B7280;}
    .sidebar-stat{background:#111827;border:1px solid #1E2A3A;border-radius:8px;padding:8px 12px;margin:4px 0;display:flex;justify-content:space-between;font-size:13px;}
    .sidebar-stat-val{color:#00F5FF;font-weight:700;}
    .lang-badge{background:#1A2235;border:1px solid #00F5FF;border-radius:8px;padding:6px 12px;color:#00F5FF;font-size:13px;font-weight:700;text-align:center;margin-bottom:8px;}
    @keyframes countUp{from{opacity:0;transform:translateY(10px);}to{opacity:1;transform:translateY(0);}}
    .count-anim{animation:countUp 0.5s ease forwards;}
</style>""", unsafe_allow_html=True)

# ── Session State ──────────────────────────────────────────────
defaults = {
    "chat_history":[], "saved_schemes":[], "application_track":[],
    "last_result":None, "last_profile":{}, "last_score_text":"",
    "last_checklist":"", "last_elig_text":"", "last_deadline_result":None,
    "family_compare_snapshot":None, "compare_schemes":[], "search_history":[],
    "lang":"English", "is_authenticated":False, "current_user_id":None, "current_username":"",
}
for k,v in defaults.items():
    if k not in st.session_state: st.session_state[k] = v

# ── Helpers ────────────────────────────────────────────────────
def T(key): return LANG[st.session_state.lang].get(key, LANG["English"].get(key,""))

def clean_text(text):
    text = unicodedata.normalize("NFKD", text).encode("ascii","ignore").decode("ascii")
    return re.sub(r'[^\x20-\x7E]','',text).strip()

def normalize_llm(text):
    if not text: return text
    return "\n".join(re.sub(r"^#{1,6}\s+","",l) for l in text.splitlines())

def _save_cb(sname, score, profile_name, save_idx):
    sname=(sname or "").strip()
    if sname in [s["name"].strip() for s in st.session_state.saved_schemes]:
        st.session_state.save_notice_pair=(save_idx, T("already_saved")); return
    st.session_state.saved_schemes.append({"name":sname,"profile":profile_name,"score":score,"saved":datetime.now().strftime("%d %b %Y")})
    st.session_state.save_notice_pair=(save_idx, T("saved_ok"))

def safe_write(pdf, text, height=7):
    words=text.split(); line=""
    for word in words:
        if len(line)+len(word)+1<=90: line+=(" " if line else "")+word
        else: pdf.cell(0,height,line,ln=True); line=word
    if line: pdf.cell(0,height,line,ln=True)

def ask_groq(prompt, max_tokens=1500):
    r=client.chat.completions.create(model="llama-3.3-70b-versatile",
        messages=[{"role":"user","content":prompt}],max_tokens=max_tokens)
    return r.choices[0].message.content

def get_db():
    return sqlite3.connect("scheme_finder.db", check_same_thread=False)

def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS user_state (
            user_id INTEGER PRIMARY KEY,
            state_json TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """)
    conn.commit()
    conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def register_user(username, password):
    conn = get_db()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO users(username, password_hash, created_at) VALUES (?, ?, ?)",
            (username.strip(), hash_password(password), datetime.now().isoformat()),
        )
        conn.commit()
        return True, None
    except sqlite3.IntegrityError:
        return False, "exists"
    finally:
        conn.close()

def login_user(username, password):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, username FROM users WHERE username=? AND password_hash=?",
        (username.strip(), hash_password(password)),
    )
    row = cur.fetchone()
    conn.close()
    return row

def _serialize_state():
    return {
        "chat_history": st.session_state.chat_history,
        "saved_schemes": st.session_state.saved_schemes,
        "application_track": st.session_state.application_track,
        "last_result": st.session_state.last_result,
        "last_profile": st.session_state.last_profile,
        "last_score_text": st.session_state.last_score_text,
        "last_checklist": st.session_state.last_checklist,
        "last_elig_text": st.session_state.last_elig_text,
        "last_deadline_result": st.session_state.last_deadline_result,
        "family_compare_snapshot": st.session_state.family_compare_snapshot,
        "compare_schemes": st.session_state.compare_schemes,
        "search_history": st.session_state.search_history,
        "lang": st.session_state.lang,
    }

def save_user_state():
    if not st.session_state.is_authenticated or not st.session_state.current_user_id:
        return
    state_json = json.dumps(_serialize_state(), ensure_ascii=False)
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO user_state (user_id, state_json, updated_at)
        VALUES (?, ?, ?)
        ON CONFLICT(user_id) DO UPDATE SET
            state_json=excluded.state_json,
            updated_at=excluded.updated_at
    """, (st.session_state.current_user_id, state_json, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def load_user_state(user_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT state_json FROM user_state WHERE user_id=?", (user_id,))
    row = cur.fetchone()
    conn.close()
    if not row:
        return
    try:
        data = json.loads(row[0])
    except json.JSONDecodeError:
        return
    for k in [
        "chat_history","saved_schemes","application_track","last_result","last_profile",
        "last_score_text","last_checklist","last_elig_text","last_deadline_result",
        "family_compare_snapshot","compare_schemes","search_history","lang"
    ]:
        if k in data:
            st.session_state[k] = data[k]

def reset_user_session_data():
    st.session_state.chat_history = []
    st.session_state.saved_schemes = []
    st.session_state.application_track = []
    st.session_state.last_result = None
    st.session_state.last_profile = {}
    st.session_state.last_score_text = ""
    st.session_state.last_checklist = ""
    st.session_state.last_elig_text = ""
    st.session_state.last_deadline_result = None
    st.session_state.family_compare_snapshot = None
    st.session_state.compare_schemes = []
    st.session_state.search_history = []

init_db()

if not st.session_state.is_authenticated:
    st.markdown(f"""<div class="hero-banner">
        <div class="hero-title">{T('auth_title')}</div>
        <div class="hero-sub">{T('auth_sub')}</div>
    </div>""", unsafe_allow_html=True)

    tab_login, tab_register = st.tabs([T("login_tab"), T("register_tab")])

    with tab_login:
        lu = st.text_input(T("username"), key="login_username")
        lp = st.text_input(T("password"), type="password", key="login_password")
        if st.button(T("login_btn"), use_container_width=True):
            row = login_user(lu, lp)
            if not row:
                st.error(T("invalid_login"))
            else:
                st.session_state.is_authenticated = True
                st.session_state.current_user_id = row[0]
                st.session_state.current_username = row[1]
                reset_user_session_data()
                load_user_state(row[0])
                st.rerun()

    with tab_register:
        ru = st.text_input(T("username"), key="register_username")
        rp = st.text_input(T("password"), type="password", key="register_password")
        rcp = st.text_input(T("confirm_password"), type="password", key="register_confirm")
        if st.button(T("register_btn"), use_container_width=True):
            if rp != rcp:
                st.error(T("pwd_mismatch"))
            elif len(rp) < 6:
                st.error(T("pwd_short"))
            else:
                ok, err = register_user(ru, rp)
                if ok:
                    st.success(T("register_ok"))
                elif err == "exists":
                    st.error(T("user_exists"))

    st.info(T("auth_needed"))
    st.stop()

def build_profile(p):
    return (f"Name:{p.get('name')},Age:{p.get('age')},Gender:{p.get('gender')},"
            f"State:{p.get('state')},Occupation:{p.get('occupation')},"
            f"Income:Rs.{p.get('income')},Category:{p.get('category')},FamilySize:{p.get('family_size')}")

def sec_hdr(text, icon=""):
    st.markdown(f'<div class="section-header"><span class="section-header-text">{icon} {text}</span><div class="section-header-line"></div></div>',unsafe_allow_html=True)

def score_bar_html(name, score, reason, color):
    st.markdown(f'<div class="score-row"><div class="score-label">{name}</div><div class="score-bar-bg"><div class="score-bar-fill" style="width:{score}%;background:{color};"></div></div><div class="score-caption">{score}% — {reason}</div></div>',unsafe_allow_html=True)

def status_badge(status):
    cls={"Applied":"badge-applied","Pending":"badge-pending","Approved":"badge-approved","Rejected":"badge-rejected"}.get(status,"badge-applied")
    return f'<span class="badge {cls}">{status}</span>'

_OCC = [
    "Farmer","Agricultural Labourer","Fisherman","Shepherd / Animal Husbandry",
    "Dairy Farmer","Plantation Worker","Forest Worker","Daily Wage Worker",
    "Construction Worker","Brick Kiln Worker","Mine / Factory Worker",
    "Domestic Worker / Maid","Sanitation Worker","MGNREGA Worker",
    "Street Vendor / Small Trader","Shop Owner","Business Owner",
    "Auto / Cab / Truck Driver","Mechanic / Electrician / Plumber",
    "Weaver / Artisan / Craftsman","Potter / Cobbler / Blacksmith","Barber / Tailor",
    "Self Employed / Freelancer","Gig Worker (Swiggy/Zomato/Ola)",
    "Content Creator / YouTuber","Salaried Employee (Private)","Government Employee",
    "Doctor / Healthcare Worker","Nurse / Paramedic","Teacher / Professor",
    "Engineer / IT Professional","Lawyer / Advocate","Chartered Accountant",
    "Architect / Designer","Journalist / Media","School Student","College Student",
    "Vocational / ITI Student","Unemployed / Job Seeker","Intern / Apprentice",
    "Retired / Pensioner","Differently Abled / Disabled","Widow / Single Parent",
    "Senior Citizen","Ex-Serviceman / Army Veteran","Transgender","Homemaker",
    "NRI / Overseas Worker","Other",
]

# ── SIDEBAR ────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""<div class="sidebar-logo">
        <div style="font-size:2rem;">🇮🇳</div>
        <div class="sidebar-logo-title">{T('app_title')}</div>
        <div class="sidebar-logo-sub">{T('app_sub')}</div>
    </div>""", unsafe_allow_html=True)

    # Language Selector
    lang_choice = st.selectbox(T("language"), ["English","తెలుగు","हिंदी"],
        index=["English","తెలుగు","हिंदी"].index(st.session_state.lang))
    if lang_choice != st.session_state.lang:
        st.session_state.lang = lang_choice
        st.rerun()

    # Show current language badge
    flags = {"English":"🇬🇧 English","తెలుగు":"🔵 తెలుగు","हिंदी":"🟠 हिंदी"}
    st.markdown(f'<div class="lang-badge">{flags[st.session_state.lang]}</div>', unsafe_allow_html=True)
    st.markdown("---")

    nav_options = [T("nav_find"),T("nav_chat"),T("nav_compare"),T("nav_family"),
                   T("nav_apps"),T("nav_deadlines"),T("nav_dashboard")]
    page = st.radio("Navigate", nav_options, label_visibility="collapsed")

    st.markdown("---")
    st.markdown(f"**{T('your_stats')}**")
    for label, val in [
        (T("searches"),    len(st.session_state.search_history)),
        (T("saved"),       len(st.session_state.saved_schemes)),
        (T("applications"),len(st.session_state.application_track)),
        (T("approved"),    sum(1 for a in st.session_state.application_track if a["status"] in ["Approved","ఆమోదించబడింది","స్వీకృత"])),
    ]:
        st.markdown(f'<div class="sidebar-stat"><span>{label}</span><span class="sidebar-stat-val">{val}</span></div>',unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(f"**{T('welcome_user')}, {st.session_state.current_username}**")
    if st.button(T("logout_btn"), use_container_width=True):
        save_user_state()
        st.session_state.is_authenticated = False
        st.session_state.current_user_id = None
        st.session_state.current_username = ""
        reset_user_session_data()
        st.rerun()

    st.markdown("---")
    st.caption("Built with Python · Streamlit · Groq AI")

# ── Map page key ───────────────────────────────────────────────
page_key = {
    T("nav_find"):"find", T("nav_chat"):"chat", T("nav_compare"):"compare",
    T("nav_family"):"family", T("nav_apps"):"apps",
    T("nav_deadlines"):"deadlines", T("nav_dashboard"):"dashboard"
}.get(page,"find")

# ══════════════════════════════════════════════════════════════
# PAGE 1 — FIND SCHEMES
# ══════════════════════════════════════════════════════════════
if page_key == "find":
    st.markdown(f"""<div class="hero-banner">
        <div class="hero-title">{T('hero_find_title')}</div>
        <div class="hero-sub">{T('hero_find_sub')}</div>
        <div class="hero-tags">
            <span class="hero-tag">🤖 AI Powered</span>
            <span class="hero-tag">📊 {T('confidence')}</span>
            <span class="hero-tag">📋 {T('docs_needed')}</span>
            <span class="hero-tag">📄 PDF</span>
        </div>
    </div>""", unsafe_allow_html=True)

    st.markdown(f"""<div class="step-bar">
        <div class="step-item active">{T('step1')}</div>
        <div class="step-item active">{T('step2')}</div>
        <div class="step-item">{T('step3')}</div>
        <div class="step-item">{T('step4')}</div>
    </div>""", unsafe_allow_html=True)

    with st.form("user_form"):
        col1,col2 = st.columns(2)
        with col1:
            st.markdown(f"**{T('personal_info')}**")
            name   = st.text_input(T("your_name"), placeholder=T("name_placeholder"))
            age    = st.number_input(T("age"), min_value=1, max_value=100, value=25)
            gender = st.selectbox(T("gender"), T("gender_opts"))
            state  = st.selectbox(T("state"), [
                "Andhra Pradesh","Arunachal Pradesh","Assam","Bihar","Chhattisgarh",
                "Goa","Gujarat","Haryana","Himachal Pradesh","Jharkhand","Karnataka",
                "Kerala","Madhya Pradesh","Maharashtra","Manipur","Meghalaya","Mizoram",
                "Nagaland","Odisha","Punjab","Rajasthan","Sikkim","Tamil Nadu","Telangana",
                "Tripura","Uttar Pradesh","Uttarakhand","West Bengal","Delhi",
                "Jammu and Kashmir","Ladakh","Puducherry","Other"
            ])
        with col2:
            st.markdown(f"**{T('financial_info')}**")
            occupation  = st.selectbox(T("occupation"), _OCC)
            income      = st.number_input(T("annual_income"), min_value=0, value=100000, step=10000)
            category    = st.selectbox(T("category"), T("category_opts"))
            family_size = st.number_input(T("family_size"), min_value=1, max_value=20, value=4)
        submitted = st.form_submit_button(T("find_btn"), use_container_width=True)

    if submitted:
        if not name:
            st.warning(T("warn_name"))
        else:
            # Normalize category back to English for AI
            cat_map = {"జనరల్":"General","OBC":"OBC","SC":"SC","ST":"ST",
                       "సామాన్య":"General","सामान्य":"General"}
            cat_en = cat_map.get(category, category)
            gen_map = {"పురుషుడు":"Male","స్త్రీ":"Female","ఇతర":"Other",
                       "पुरुष":"Male","महिला":"Female","अन्य":"Other"}
            gen_en = gen_map.get(gender, gender)

            profile = dict(name=name,age=age,gender=gen_en,state=state,
                           occupation=occupation,income=income,
                           category=cat_en,family_size=family_size)
            st.session_state.last_profile = profile
            st.session_state.search_history.append({"time":datetime.now().strftime("%d %b %Y, %I:%M %p"),"profile":profile})

            prog = st.progress(0)
            stat = st.empty()
            lang_instruction = f"Respond in {'Telugu' if st.session_state.lang=='తెలుగు' else 'Hindi' if st.session_state.lang=='हिंदी' else 'English'}."

            stat.markdown(f"🤖 {T('step_schemes')}")
            prog.progress(10)
            st.session_state.last_result = ask_groq(f"""
                Indian government scheme advisor. Profile:{build_profile(profile)}
                Start exactly with: "Hello {name}, this is your govt scheme finder."
                Then list schemes immediately after that intro (do not use any other greeting line).
                List top 5 relevant schemes. For each: Name, Benefit, Eligibility, How to Apply.
                Format with emojis. Focus on Central and {state} schemes. {lang_instruction}
            """)

            stat.markdown(f"📊 {T('step_scores')}")
            prog.progress(40)
            st.session_state.last_score_text = ask_groq(f"""
                Profile:{build_profile(profile)}
                Give approval confidence scores. ONLY use:
                SCHEME: <name>
                SCORE: <0-100>
                REASON: <one line in English>
                ---
            """)

            stat.markdown(f"📋 {T('step_checklist')}")
            prog.progress(70)
            st.session_state.last_checklist = ask_groq(f"""
                Document checklist for:{build_profile(profile)}
                Sections: Identity, Address, Income, Occupation, Other.
                Format: ☐ Document — why — where to get. {lang_instruction}
            """)

            stat.markdown(f"🎯 {T('step_elig')}")
            prog.progress(90)
            st.session_state.last_elig_text = normalize_llm(ask_groq(f"""
                Profile:{build_profile(profile)}
                For each top 5 scheme:
                SCHEME: <name>
                MEETS: <criteria met>
                WATCH OUT: <verify>
                RISK: <disqualifiers>
                ---
                No markdown headings. {lang_instruction}
            """))
            prog.progress(100)
            stat.empty(); prog.empty()

    if st.session_state.last_result and st.session_state.last_profile:
        snp = st.session_state.pop("save_notice_pair", None)
        result=st.session_state.last_result; profile=st.session_state.last_profile
        name=profile["name"]; state=profile["state"]; occupation=profile["occupation"]
        income=profile["income"]; category=profile["category"]
        score_text=st.session_state.last_score_text or ""
        checklist=st.session_state.last_checklist or ""
        elig_text=st.session_state.last_elig_text or ""

        st.success(f"{T('found_schemes')} **{name}**!")
        st.markdown(f"""<div class="step-bar">
            <div class="step-item done">{T('step1')} ✓</div>
            <div class="step-item done">{T('step2')} ✓</div>
            <div class="step-item done">{T('step3')} ✓</div>
            <div class="step-item active">{T('step4')}</div>
        </div>""", unsafe_allow_html=True)

        sec_hdr(T("top_schemes"),"🏆")
        lines=result.split("\n"); current=[]; cards=[]
        for line in lines:
            if line.strip().startswith("###") or (line.strip() and line.strip()[0].isdigit() and "." in line.strip()[:3]):
                if current: cards.append("\n".join(current))
                current=[line]
            else: current.append(line)
        if current: cards.append("\n".join(current))
        if len(cards)>1:
            for card in cards:
                card=card.strip()
                if not card: continue
                lns=card.split("\n")
                title=lns[0].replace("###","").replace("**","").strip()
                body="\n".join(lns[1:]).strip()
                st.markdown(f'<div class="scheme-card"><div class="scheme-card-title">🏛️ {title}</div><div class="scheme-card-body">{body}</div></div>',unsafe_allow_html=True)
        else:
            st.markdown(result)

        sec_hdr(T("confidence"),"📊")
        scheme_names=[]
        for sidx, block in enumerate(score_text.strip().split("---")):
            block=block.strip()
            if not block: continue
            sm=re.search(r"SCHEME:\s*(.+)",block)
            sc=re.search(r"SCORE:\s*(\d+)",block)
            rm=re.search(r"REASON:\s*(.+)",block)
            if sm and sc:
                sname=sm.group(1).strip(); score=int(sc.group(1).strip())
                reason=rm.group(1).strip() if rm else ""
                scheme_names.append(sname)
                color="#00FF94" if score>=75 else "#FFD60A" if score>=50 else "#F72585"
                emoji="🟢" if score>=75 else "🟡" if score>=50 else "🔴"
                label=T("high_chance") if score>=75 else T("med_chance") if score>=50 else T("low_chance")
                c1,c2=st.columns([5,1])
                with c1: score_bar_html(f"{emoji} {sname}",score,f"{score}% — {label} | {reason}",color)
                with c2:
                    st.markdown("<br>",unsafe_allow_html=True)
                    st.button(T("save_btn"),key=f"sv_{sidx}",on_click=_save_cb,
                              kwargs={"sname":sname,"score":score,"profile_name":name,"save_idx":sidx})
                    if snp and snp[0]==sidx: st.success(snp[1])
        if scheme_names: st.session_state.compare_schemes=scheme_names

        sec_hdr(T("docs_needed"),"📋")
        with st.expander(T("view_checklist"),expanded=True): st.markdown(checklist)
        st.info(T("doc_tip"))

        sec_hdr(T("elig_breakdown"),"🎯")
        with st.expander(T("view_elig"),expanded=False): st.markdown(elig_text)

        sec_hdr(T("download_report"),"📄")
        from fpdf import FPDF
        pdf=FPDF(); pdf.add_page(); pdf.set_margins(15,15,15); pdf.set_auto_page_break(auto=True,margin=15)
        pdf.set_fill_color(33,97,140); pdf.rect(0,0,210,32,'F')
        pdf.set_text_color(255,255,255); pdf.set_font("Arial","B",16); pdf.set_xy(0,7)
        pdf.cell(210,10,"Government Scheme Finder - India",ln=True,align="C")
        pdf.set_font("Arial",size=9)
        pdf.cell(210,8,clean_text(f"{name} | {occupation} | {state} | Rs.{income} | {category}"),ln=True,align="C")
        pdf.ln(12); pdf.set_text_color(0,0,0)
        for line in result.split("\n"):
            cl=clean_text(line)
            if not cl: pdf.ln(2); continue
            if cl.startswith("###"):
                pdf.ln(3); pdf.set_fill_color(220,235,255); pdf.set_font("Arial","B",11)
                pdf.set_x(15); pdf.cell(0,9,"  "+cl.replace("###","").replace("**","").strip()[:85],ln=True,fill=True)
                pdf.set_font("Arial",size=10)
            elif "**" in cl:
                pdf.set_font("Arial","B",10); pdf.set_text_color(33,97,140)
                safe_write(pdf,cl.replace("**","")); pdf.set_text_color(0,0,0); pdf.set_font("Arial",size=10)
            elif cl.startswith("-"):
                pdf.set_x(20); safe_write(pdf,"* "+cl[1:].strip())
            else: safe_write(pdf,cl)
        pdf.set_y(-18); pdf.set_font("Arial","I",8); pdf.set_text_color(150,150,150)
        pdf.cell(0,10,"Generated by Government Scheme Finder | For informational purposes only",align="C")
        st.download_button(T("download_pdf"),data=bytes(pdf.output()),
                           file_name=f"schemes_{name}.pdf",mime="application/pdf",use_container_width=True)

# ══════════════════════════════════════════════════════════════
# PAGE 2 — CHAT MODE
# ══════════════════════════════════════════════════════════════
elif page_key=="chat":
    st.markdown(f"""<div class="hero-banner">
        <div class="hero-title">{T('hero_chat_title')}</div>
        <div class="hero-sub">{T('hero_chat_sub')}</div>
        <div class="hero-tags"><span class="hero-tag">🗣️ Natural Language</span><span class="hero-tag">🌐 Telugu & Hindi OK</span></div>
    </div>""",unsafe_allow_html=True)
    st.markdown(f"""<div class="scheme-card">
        <div class="scheme-card-title">{T('chat_example')}</div>
        <div class="scheme-card-body">{T('chat_ex1')}<br>{T('chat_ex2')}<br>{T('chat_ex3')}</div>
    </div>""",unsafe_allow_html=True)
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])
    user_input=st.chat_input(T("chat_placeholder"))
    if user_input:
        st.session_state.chat_history.append({"role":"user","content":user_input})
        with st.chat_message("user"): st.markdown(user_input)
        with st.chat_message("assistant"):
            with st.spinner("..."):
                lang_instruction=f"Respond in {'Telugu' if st.session_state.lang=='తెలుగు' else 'Hindi' if st.session_state.lang=='हिंदी' else 'English'}."
                reply=ask_groq(f"""Indian government scheme advisor. User said: "{user_input}"
                Extract profile, find top 5 schemes. For each: Name, Benefit, Eligibility, How to Apply.
                If not enough info ask follow-up. Use emojis. {lang_instruction}""")
                st.markdown(reply)
                st.session_state.chat_history.append({"role":"assistant","content":reply})
    if st.session_state.chat_history:
        if st.button(T("clear_chat"),use_container_width=True):
            st.session_state.chat_history=[]; st.rerun()

# ══════════════════════════════════════════════════════════════
# PAGE 3 — COMPARE SCHEMES
# ══════════════════════════════════════════════════════════════
elif page_key=="compare":
    st.markdown(f"""<div class="hero-banner">
        <div class="hero-title">{T('hero_compare_title')}</div>
        <div class="hero-sub">{T('hero_compare_sub')}</div>
        <div class="hero-tags"><span class="hero-tag">⚡ Instant Table</span><span class="hero-tag">🏆 AI Recommendation</span></div>
    </div>""",unsafe_allow_html=True)
    s1=st.text_input(T("scheme1"),placeholder="e.g. PM Kisan Samman Nidhi")
    s2=st.text_input(T("scheme2"),placeholder="e.g. Rythu Bandhu")
    s3=st.text_input(T("scheme3"),placeholder="e.g. PM Awas Yojana")
    if st.button(T("compare_btn"),use_container_width=True):
        schemes=[s for s in [s1,s2,s3] if s.strip()]
        if len(schemes)<2: st.warning(T("compare_warn"))
        else:
            lang_instruction=f"Respond in {'Telugu' if st.session_state.lang=='తెలుగు' else 'Hindi' if st.session_state.lang=='हिंदी' else 'English'}."
            with st.spinner("..."):
                comparison=ask_groq(f"""Compare Indian government schemes: {', '.join(schemes)}
                Detailed comparison table: Benefit, Eligibility, Documents, How to Apply, Time, Central/State, Website, Best For.
                After table give recommendation. {lang_instruction}""")
            st.success(T("compare_ready"))
            sec_hdr(T("compare_table"),"📊")
            st.markdown(comparison)
            st.info(T("compare_tip"))

# ══════════════════════════════════════════════════════════════
# PAGE 4 — FAMILY COMPARISON
# ══════════════════════════════════════════════════════════════
elif page_key=="family":
    st.markdown(f"""<div class="hero-banner">
        <div class="hero-title">{T('hero_fam_title')}</div>
        <div class="hero-sub">{T('hero_fam_sub')}</div>
        <div class="hero-tags"><span class="hero-tag">👤 2 Profiles</span><span class="hero-tag">🔄 Overlap Analysis</span><span class="hero-tag">💰 Total Estimate</span></div>
    </div>""",unsafe_allow_html=True)
    c1,c2=st.columns(2)
    with c1:
        st.markdown(f'<div class="scheme-card"><div class="scheme-card-title">{T("member1")}</div></div>',unsafe_allow_html=True)
        m1n=st.text_input("Name",key="m1n"); m1a=st.number_input("Age",min_value=1,max_value=100,value=50,key="m1a")
        m1g=st.selectbox("Gender",["Male","Female","Other"],key="m1g"); m1o=st.selectbox("Occupation",_OCC,key="m1o")
        m1i=st.number_input("Income (₹)",min_value=0,value=80000,step=5000,key="m1i"); m1c=st.selectbox("Category",["General","OBC","SC","ST"],key="m1c")
    with c2:
        st.markdown(f'<div class="scheme-card"><div class="scheme-card-title">{T("member2")}</div></div>',unsafe_allow_html=True)
        m2n=st.text_input("Name",key="m2n"); m2a=st.number_input("Age",min_value=1,max_value=100,value=22,key="m2a")
        m2g=st.selectbox("Gender",["Male","Female","Other"],key="m2g"); m2o=st.selectbox("Occupation",_OCC,key="m2o")
        m2i=st.number_input("Income (₹)",min_value=0,value=0,step=5000,key="m2i"); m2c=st.selectbox("Category",["General","OBC","SC","ST"],key="m2c")
    sf=st.selectbox(T("state_both"),["Telangana","Andhra Pradesh","Maharashtra","Karnataka","Tamil Nadu","Uttar Pradesh","Bihar","Other"])
    if st.button(T("compare_fam_btn"),use_container_width=True):
        if not m1n or not m2n: st.warning(T("fam_warn"))
        else:
            lang_instruction=f"Respond in {'Telugu' if st.session_state.lang=='తెలుగు' else 'Hindi' if st.session_state.lang=='हिंदी' else 'English'}."
            with st.spinner("..."):
                fr=ask_groq(f"""Compare government schemes for two family members.
                {m1n}: Age {m1a},{m1g},{m1o},Rs.{m1i},{m1c},State:{sf}
                {m2n}: Age {m2a},{m2g},{m2o},Rs.{m2i},{m2c},State:{sf}
                Format: Comparison table | Only {m1n} | Only {m2n} | Both | Summary. {lang_instruction}""")
            st.session_state.family_compare_snapshot={"result":fr,"m1_name":m1n,"m1_age":m1a,"m1_gender":m1g,"m1_occ":m1o,"m1_income":m1i,"m1_cat":m1c,"m2_name":m2n,"m2_age":m2a,"m2_gender":m2g,"m2_occ":m2o,"m2_income":m2i,"m2_cat":m2c,"state_f":sf}
            st.success(T("fam_done"))
    snap=st.session_state.family_compare_snapshot
    if snap:
        sec_hdr(T("profile_compare"),"📋")
        df=pd.DataFrame({"Field":["Age","Gender","Occupation","Income (₹)","Category","State"],
            snap["m1_name"]:[snap["m1_age"],snap["m1_gender"],snap["m1_occ"],snap["m1_income"],snap["m1_cat"],snap["state_f"]],
            snap["m2_name"]:[snap["m2_age"],snap["m2_gender"],snap["m2_occ"],snap["m2_income"],snap["m2_cat"],snap["state_f"]]})
        st.dataframe(df,hide_index=True,use_container_width=True)
        sec_hdr(T("ai_analysis"),"📊"); st.markdown(snap["result"])
        if st.button(T("clear_results")): st.session_state.family_compare_snapshot=None; st.rerun()

# ══════════════════════════════════════════════════════════════
# PAGE 5 — MY APPLICATIONS
# ══════════════════════════════════════════════════════════════
elif page_key=="apps":
    st.markdown(f"""<div class="hero-banner">
        <div class="hero-title">{T('hero_apps_title')}</div>
        <div class="hero-sub">{T('hero_apps_sub')}</div>
        <div class="hero-tags"><span class="hero-tag">🔵 Applied</span><span class="hero-tag">🟡 Pending</span><span class="hero-tag">🟢 Approved</span><span class="hero-tag">🔴 Rejected</span></div>
    </div>""",unsafe_allow_html=True)
    with st.expander(T("add_app"),expanded=len(st.session_state.application_track)==0):
        ac1,ac2=st.columns(2)
        with ac1:
            as_=st.text_input(T("scheme_name")); ad=st.date_input(T("app_date"),value=date.today())
            ast=st.selectbox(T("status"),["Applied","Pending","Approved","Rejected"])
        with ac2:
            ar=st.text_input(T("ref_num")); aa=st.text_input(T("exp_benefit"),placeholder="e.g. Rs.6000/year")
            an=st.text_area(T("notes"),height=80)
        if st.button(T("add_app_btn"),use_container_width=True):
            if not as_: st.warning(T("app_warn"))
            else:
                st.session_state.application_track.append({"scheme":as_,"date":str(ad),"status":ast,"ref":ar,"amount":aa,"notes":an})
                st.success(f"✅ {as_}"); st.rerun()
    if not st.session_state.application_track:
        st.info(T("no_apps"))
    else:
        statuses=[a["status"] for a in st.session_state.application_track]
        sec_hdr(T("summary"),"📊")
        mc1,mc2,mc3,mc4=st.columns(4)
        with mc1: st.markdown(f'<div class="metric-card"><div class="metric-num count-anim">{len(statuses)}</div><div class="metric-label">{T("total_apps")}</div></div>',unsafe_allow_html=True)
        with mc2: st.markdown(f'<div class="metric-card"><div class="metric-num count-anim" style="color:#00FF94">{statuses.count("Approved")}</div><div class="metric-label">✅ {T("approved")}</div></div>',unsafe_allow_html=True)
        with mc3: st.markdown(f'<div class="metric-card"><div class="metric-num count-anim" style="color:#FFD60A">{statuses.count("Pending")}</div><div class="metric-label">⏳ Pending</div></div>',unsafe_allow_html=True)
        with mc4: st.markdown(f'<div class="metric-card"><div class="metric-num count-anim" style="color:#60A5FA">{statuses.count("Applied")}</div><div class="metric-label">📝 Applied</div></div>',unsafe_allow_html=True)
        sec_hdr(T("your_apps"),"📋")
        for i,app in enumerate(st.session_state.application_track):
            badge=status_badge(app["status"])
            with st.expander(f"🏛️ {app['scheme']} — {app['date']}"):
                st.markdown(f"**{T('status')}:** {badge}",unsafe_allow_html=True)
                cc1,cc2=st.columns(2)
                with cc1:
                    st.markdown(f"**{T('app_date')}:** {app['date']}")
                    if app["ref"]: st.markdown(f"**{T('ref_num')}:** `{app['ref']}`")
                with cc2:
                    if app["amount"]: st.markdown(f"**{T('exp_benefit')}:** {app['amount']}")
                    if app["notes"]: st.markdown(f"**{T('notes')}:** {app['notes']}")
                ca,cb=st.columns(2)
                with ca:
                    ns=st.selectbox(T("update_status"),["Applied","Pending","Approved","Rejected"],
                                    index=["Applied","Pending","Approved","Rejected"].index(app["status"]),key=f"st_{i}")
                    if ns!=app["status"]: st.session_state.application_track[i]["status"]=ns; st.rerun()
                with cb:
                    st.markdown("<br>",unsafe_allow_html=True)
                    if st.button(T("delete"),key=f"dl_{i}",use_container_width=True):
                        st.session_state.application_track.pop(i); st.rerun()

# ══════════════════════════════════════════════════════════════
# PAGE 6 — DEADLINES
# ══════════════════════════════════════════════════════════════
elif page_key=="deadlines":
    st.markdown(f"""<div class="hero-banner">
        <div class="hero-title">{T('hero_dl_title')}</div>
        <div class="hero-sub">{T('hero_dl_sub')}</div>
        <div class="hero-tags"><span class="hero-tag">🔴 High</span><span class="hero-tag">🟡 Medium</span><span class="hero-tag">🟢 Low / Ongoing</span></div>
    </div>""",unsafe_allow_html=True)
    dc1,dc2=st.columns(2)
    with dc1:
        dl_state=st.selectbox(T("your_state"),["Telangana","Andhra Pradesh","Maharashtra","Karnataka","Tamil Nadu","Uttar Pradesh","Bihar","Rajasthan","Delhi","Gujarat","Other"])
        dl_occ=st.selectbox(T("your_occ"),["Farmer","Student","Daily Wage Worker","Business Owner","Salaried Employee","Unemployed","Other"])
    with dc2:
        dl_cat=st.selectbox(T("category"),["General","OBC","SC","ST"])
        dl_age=st.number_input(T("age"),min_value=1,max_value=100,value=25)
    if st.button(T("check_dl_btn"),use_container_width=True):
        schemes=[]
        if dl_occ=="Farmer":
            schemes+=[
                {"name":"PM Kisan Samman Nidhi","deadline":"April 30, 2026","urgency":"High","action":"Register at pmkisan.gov.in with Aadhaar and bank details","benefit":"Rs.6,000/year"},
                {"name":"Rythu Bandhu (Telangana)","deadline":"May 2026","urgency":"High","action":"Visit nearest agriculture office with land records","benefit":"Rs.10,000/acre/year"},
                {"name":"PM Fasal Bima Yojana","deadline":"July 31, 2026","urgency":"Medium","action":"Apply via bank or CSC before Kharif season","benefit":"Crop insurance"},
                {"name":"Kisan Credit Card","deadline":"Ongoing","urgency":"Low","action":"Apply at any nationalized bank with land documents","benefit":"Up to Rs.3 lakh credit"},
            ]
        if dl_occ=="Student":
            schemes+=[
                {"name":"National Scholarship Portal","deadline":"Oct 31, 2026","urgency":"Medium","action":"Apply at scholarships.gov.in","benefit":"Rs.10,000–75,000/year"},
                {"name":"Post Matric Scholarship","deadline":"Nov 2026","urgency":"Medium","action":"Apply through state portal with caste certificate","benefit":"Full tuition + allowance"},
            ]
        if dl_cat in ["SC","ST"]:
            schemes+=[{"name":"Dr. Ambedkar Post Matric Scholarship","deadline":"Dec 2026","urgency":"Low","action":"Apply via state social welfare department","benefit":"Full scholarship"}]
        schemes+=[
            {"name":"Ayushman Bharat PM-JAY","deadline":"Ongoing","urgency":"Low","action":"Check eligibility at pmjay.gov.in with Aadhaar","benefit":"Rs.5 lakh health cover/family/year"},
            {"name":"PM Awas Yojana","deadline":"March 31, 2026","urgency":"High","action":"Apply at pmaymis.gov.in or nearest CSC","benefit":"Rs.1.5 lakh housing subsidy"},
            {"name":"PM Jan Dhan Yojana","deadline":"Ongoing","urgency":"Low","action":"Open account at any bank with Aadhaar + photo","benefit":"Free bank account + Rs.10,000 OD"},
        ]
        st.session_state.last_deadline_result=schemes
    if st.session_state.last_deadline_result:
        st.success(T("dl_ready"))
        sec_hdr(T("upcoming_dl"),"📅")
        for scheme in st.session_state.last_deadline_result:
            uc={"High":"🔴","Medium":"🟡","Low":"🟢"}.get(scheme["urgency"],"⚪")
            bc={"High":"#F72585","Medium":"#FFD60A","Low":"#00FF94"}.get(scheme["urgency"],"#00F5FF")
            st.markdown(f"""<div class="deadline-card" style="border-left:4px solid {bc};">
                <div class="deadline-card-title">{uc} {scheme['name']}</div>
                <div style="display:flex;gap:20px;flex-wrap:wrap;margin-bottom:10px;">
                    <span style="font-size:0.85rem;color:#8A9BB5;">📅 {T('deadline')}: <strong style="color:#fff">{scheme['deadline']}</strong></span>
                    <span style="font-size:0.85rem;color:#8A9BB5;">⚡ {T('urgency')}: <strong style="color:#fff">{scheme['urgency']}</strong></span>
                    <span style="font-size:0.85rem;color:#8A9BB5;">💰 {T('benefit')}: <strong style="color:#fff">{scheme['benefit']}</strong></span>
                </div>
                <div style="background:#1A2235;border-radius:8px;padding:10px 14px;font-size:0.88rem;color:#CBD5E1;">
                    👉 <strong>{T('action')}:</strong> {scheme['action']}
                </div>
            </div>""",unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# PAGE 7 — DASHBOARD
# ══════════════════════════════════════════════════════════════
elif page_key=="dashboard":
    st.markdown(f"""<div class="hero-banner">
        <div class="hero-title">{T('hero_dash_title')}</div>
        <div class="hero-sub">{T('hero_dash_sub')}</div>
        <div class="hero-tags"><span class="hero-tag">🕒 History</span><span class="hero-tag">💾 Saved</span><span class="hero-tag">📊 Charts</span><span class="hero-tag">🤖 AI Insights</span></div>
    </div>""",unsafe_allow_html=True)
    approved=sum(1 for a in st.session_state.application_track if a["status"]=="Approved")
    dc1,dc2,dc3,dc4=st.columns(4)
    with dc1: st.markdown(f'<div class="metric-card"><div class="metric-num count-anim">{len(st.session_state.search_history)}</div><div class="metric-label">🔍 {T("searches")}</div></div>',unsafe_allow_html=True)
    with dc2: st.markdown(f'<div class="metric-card"><div class="metric-num count-anim" style="color:#7C3AED">{len(st.session_state.saved_schemes)}</div><div class="metric-label">💾 {T("saved")}</div></div>',unsafe_allow_html=True)
    with dc3: st.markdown(f'<div class="metric-card"><div class="metric-num count-anim" style="color:#FFD60A">{len(st.session_state.application_track)}</div><div class="metric-label">📁 {T("applications")}</div></div>',unsafe_allow_html=True)
    with dc4: st.markdown(f'<div class="metric-card"><div class="metric-num count-anim" style="color:#00FF94">{approved}</div><div class="metric-label">{T("approved")}</div></div>',unsafe_allow_html=True)

    sec_hdr(T("saved_schemes"),"💾")
    if not st.session_state.saved_schemes: st.info(T("no_saved"))
    else:
        for i,scheme in enumerate(st.session_state.saved_schemes):
            sc1,sc2,sc3,sc4,sc5=st.columns([3,1.5,1,1.5,1])
            sc1.markdown(f"**🏛️ {scheme['name']}**"); sc2.markdown(f"👤 {scheme.get('profile','—')}")
            sc3.markdown(f"📊 {scheme.get('score','—')}%"); sc4.markdown(f"📅 {scheme.get('saved','—')}")
            if sc5.button("🗑️",key=f"rm_{i}"): st.session_state.saved_schemes.pop(i); st.rerun()

    sec_hdr(T("recent_searches"),"🕒")
    if not st.session_state.search_history: st.info(T("no_searches"))
    else:
        for s in reversed(st.session_state.search_history[-8:]):
            p=s["profile"]
            st.markdown(f'<div class="scheme-card" style="padding:12px 18px;margin:6px 0;"><span style="color:#6B7280;font-size:0.8rem;">{s["time"]}</span><br><strong>{p.get("name","?")}</strong> — {p.get("age","?")} yrs, {p.get("occupation","?")}, {p.get("state","?")}, Rs.{p.get("income","?")}/yr</div>',unsafe_allow_html=True)

    sec_hdr(T("app_chart"),"📊")
    if not st.session_state.application_track: st.info(T("no_chart"))
    else:
        sc={}
        for app in st.session_state.application_track: sc[app["status"]]=sc.get(app["status"],0)+1
        st.bar_chart(pd.DataFrame(list(sc.items()),columns=["Status","Count"]).set_index("Status"))

    sec_hdr(T("ai_insights"),"🤖")
    if st.session_state.last_profile:
        if st.button(T("gen_insights"),use_container_width=True):
            lang_instruction=f"Respond in {'Telugu' if st.session_state.lang=='తెలుగు' else 'Hindi' if st.session_state.lang=='हिंदी' else 'English'}."
            with st.spinner("..."):
                ins=ask_groq(f"""Profile:{build_profile(st.session_state.last_profile)}
                Applications:{[a['scheme'] for a in st.session_state.application_track]}
                Give: 1.Best scheme types 2.Approval tips 3.Missing schemes 4.State/occupation tips 5.Total annual benefit estimate.
                Be specific and encouraging. {lang_instruction}""")
                st.markdown(f'<div class="scheme-card"><div class="scheme-card-body">{ins}</div></div>',unsafe_allow_html=True)
    else: st.info(T("no_insights"))

    sec_hdr(T("reset"),"⚠️")
    if st.button(T("clear_all"),use_container_width=True):
        for k in ["saved_schemes","application_track","search_history","chat_history"]:
            st.session_state[k]=[]
        for k in ["last_result","last_profile","family_compare_snapshot","last_deadline_result"]:
            st.session_state[k]=None if "profile" in k or "snapshot" in k or "deadline" in k or "result" in k else {}
        for k in ["last_score_text","last_checklist","last_elig_text"]:
            st.session_state[k]=""
        st.success(T("cleared")); st.rerun()

save_user_state()
