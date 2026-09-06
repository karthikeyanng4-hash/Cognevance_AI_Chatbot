import json
import os
import re
import pickle

# ============================================================
# LOAD PERSONAL DATA FROM JSON
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "personal_data.json")

def load_data():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading personal_data.json: {e}")
        return {}

# Load on startup
data = load_data()


# ============================================================
# LOAD NLP ML MODEL & VECTORIZER (OPTIONAL FALLBACK)
# ============================================================

model = None
vectorizer = None

MODEL_FILE = os.path.join(BASE_DIR, "chatbot_model.pkl")
VECT_FILE = os.path.join(BASE_DIR, "vectorizer.pkl")

if os.path.exists(MODEL_FILE) and os.path.exists(VECT_FILE):
    try:
        with open(MODEL_FILE, "rb") as f:
            model = pickle.load(f)
        with open(VECT_FILE, "rb") as f:
            vectorizer = pickle.load(f)
    except Exception as e:
        print(f"Notice: ML model could not be loaded: {e}")


# ============================================================
# HELPER FUNCTIONS - ROBUST TOKEN / WORD BOUNDARY MATCHING
# ============================================================

def clean(text):
    if not text:
        return ""
    # Lowercase and normalize whitespace
    text = text.lower().strip()
    return re.sub(r"\s+", " ", text)


def has_word(text, words):
    """
    Checks if any word in `words` appears as a complete word (using regex \b word boundary).
    Prevents false positive collisions like 'hi' in 'his' or 'age' in 'percentage'.
    """
    if isinstance(words, str):
        words = [words]
    pattern = r"\b(" + "|".join(re.escape(w) for w in words) + r")\b"
    return bool(re.search(pattern, text, re.IGNORECASE))


def has_phrase(text, phrases):
    """
    Checks if any phrase in `phrases` appears in `text` with word boundaries.
    """
    if isinstance(phrases, str):
        phrases = [phrases]
    for p in phrases:
        pattern = r"\b" + re.escape(p).replace(r"\ ", r"\s+") + r"\b"
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False


# ============================================================
# FORMATTED RESPONSE BUILDERS
# ============================================================

def get_skills_text(personal_data):
    skills_data = personal_data.get("skills", {})
    prog = ", ".join(skills_data.get("programming_languages", []))
    tech = ", ".join(skills_data.get("technical_skills", []))
    tools = ", ".join(skills_data.get("tools", []))

    return f"""💻 Programming Languages:
{prog}

⚙️ Technical Skills:
{tech}

🛠️ Tools & Technologies:
{tools}"""


def get_subject_marks(personal_data, subject):
    subject = subject.lower().strip()

    aliases = {
        "maths": "mathematics",
        "math": "mathematics",
        "social": "social science",
        "cs": "computer science"
    }
    subject = aliases.get(subject, subject)

    edu = personal_data.get("education", {})
    results = []

    for standard in ["10th", "11th", "12th"]:
        std_data = edu.get(standard, {})
        marks = std_data.get("marks", {})

        if subject in marks:
            mark = marks[subject]
            # Skip 0 or unrecorded marks
            if mark != 0:
                results.append(f"📚 {standard}: {mark}")

    if results:
        return f"📊 Karthikeyan's {subject.title()} Marks:\n\n" + "\n".join(results)

    return None


def get_standard_summary(personal_data, standard):
    edu = personal_data.get("education", {})
    std_data = edu.get(standard, {})
    school = std_data.get("school", "The TVS School")
    pct = std_data.get("percentage", "")
    group = std_data.get("group", "")
    marks = std_data.get("marks", {})

    lines = [f"🏫 {standard.upper()} Standard:"]
    if school:
        lines.append(f"School: {school}")
    if group:
        lines.append(f"Group: {group}")
    if pct:
        lines.append(f"Percentage: {pct}")

    valid_marks = [f"• {k.title()}: {v}" for k, v in marks.items() if v != 0]
    if valid_marks:
        lines.append("\nMarks:")
        lines.extend(valid_marks)
    elif standard == "11th":
        lines.append("\nKarthikeyan completed his 11th standard in the Computer Science stream with an overall score of 92.00%.")

    return "\n".join(lines)


def get_project_link(personal_data, project_key):
    projects = personal_data.get("projects", {})
    proj = projects.get(project_key, {})
    name = proj.get("name", "Project")
    link = proj.get("link") or personal_data.get("profiles", {}).get("github", "https://github.com/karthikeyanng4-hash")
    return f"""🚀 {name}\n\n🔗 Link:\n{link}"""


def get_project_text(personal_data, project_key):
    projects = personal_data.get("projects", {})
    proj = projects.get(project_key)
    if not proj:
        return None

    name = proj.get("name", "")
    desc = proj.get("description", "")
    link = proj.get("link", "")
    if not link:
        link = personal_data.get("profiles", {}).get("github", "https://github.com/karthikeyanng4-hash")

    link_str = f"\n\n🔗 Link:\n{link}" if link else ""
    return f"""🚀 {name}

{desc}{link_str}"""


# ============================================================
# MAIN CHATBOT RESPONSE FUNCTION
# ============================================================

def get_response(user_message, password=None, context=None):
    # Reload personal data to always ensure freshness
    personal_data = load_data() or data

    if context is None:
        context = {}

    def finish(resp):
        return resp

    message = clean(user_message)
    if not message:
        return "Please ask a question about Karthikeyan!"

    # --------------------------------------------------------
    # 1. GIRLFRIEND - SENSITIVE / PASSWORD PROTECTED
    # --------------------------------------------------------
    if (
        has_word(message, ["girlfriend", "gf"])
        or has_phrase(message, ["gf name", "his gf", "who is his gf", "girlfriend name"])
    ):
        gf_info = personal_data.get("girlfriend", {})
        correct_password = str(gf_info.get("password", "12102005"))
        gf_name = gf_info.get("name", "Ishuwarya T N")

        if password == correct_password:
            return f"""❤️ Karthikeyan's girlfriend's name is {gf_name}."""
        else:
            return """😂 Lol! He doesn't have a girlfriend!"""

    # --------------------------------------------------------
    # 2. ELDER BROTHER (HIGH PRIORITY)
    # --------------------------------------------------------
    # Matches: "does he have an elder brother", "does he have and elder brother",
    # "does he have elder brother", "any elder brother", "elder brother", "older brother"
    family = personal_data.get("family", {})
    younger_brother = family.get("younger_brother", "N. G. Abishek Kumar")

    is_elder_brother_query = (
        has_phrase(message, [
            "elder brother",
            "older brother",
            "big brother",
            "elder bro",
            "older bro",
            "and elder brother",
            "an elder brother"
        ])
        or (has_word(message, ["elder", "older", "big"]) and has_word(message, ["brother", "bro"]))
    )

    if is_elder_brother_query:
        return f"""❌ No, Karthikeyan does not have an elder brother.

👦 He has only one younger brother, and his name is {younger_brother}."""

    # --------------------------------------------------------
    # 3. YOUNGER BROTHER
    # --------------------------------------------------------
    is_younger_brother_query = (
        has_phrase(message, [
            "younger brother",
            "little brother",
            "younger bro",
            "little bro"
        ])
        or (has_word(message, ["younger", "little"]) and has_word(message, ["brother", "bro"]))
    )

    if is_younger_brother_query:
        return f"""✅ Yes, Karthikeyan has one younger brother.

👦 His name is {younger_brother}."""

    # --------------------------------------------------------
    # 4. SISTER
    # --------------------------------------------------------
    if has_word(message, ["sister", "sisters", "sis"]):
        return f"""❌ No, Karthikeyan does not have a sister.

👦 He has only one younger brother named {younger_brother}."""

    # --------------------------------------------------------
    # 5. GENERAL BROTHER / SIBLINGS
    # --------------------------------------------------------
    if has_word(message, ["brother", "brothers", "bro", "siblings", "sibling"]):
        return f"""👦 Karthikeyan has only one younger brother.

His name is {younger_brother}."""

    # --------------------------------------------------------
    # 6. FATHER
    # --------------------------------------------------------
    if (
        has_word(message, ["father", "dad", "appa"])
        or has_phrase(message, ["father name", "father's name", "dad name", "dad's name", "who is his father"])
    ):
        father = family.get("father", "N. K. Ganesh Babu")
        return f"""👨 Karthikeyan's father is {father}."""

    # --------------------------------------------------------
    # 7. MOTHER
    # --------------------------------------------------------
    if (
        has_word(message, ["mother", "mom", "amma", "mummy"])
        or has_phrase(message, ["mother name", "mother's name", "mom name", "mom's name", "who is his mother"])
    ):
        mother = family.get("mother", "N. G. Vijayalakshmi")
        return f"""👩 Karthikeyan's mother is {mother}."""

    # --------------------------------------------------------
    # 8. FAMILY MEMBERS / FAMILY OVERVIEW
    # --------------------------------------------------------
    if (
        has_word(message, ["family", "parents"])
        or has_phrase(message, ["family members", "how many family members", "family details", "tell me about family"])
    ):
        total_members = family.get("family_members", 4)
        father = family.get("father", "N. K. Ganesh Babu")
        mother = family.get("mother", "N. G. Vijayalakshmi")
        return f"""👨‍👩‍👦 Karthikeyan's family has {total_members} members:

• Karthikeyan
• Father: {father}
• Mother: {mother}
• Younger Brother: {younger_brother}"""

    # --------------------------------------------------------
    # 9. UNIQUE / POLYDACTYLY
    # --------------------------------------------------------
    if (
        has_word(message, ["unique", "polydactyly"])
        or has_phrase(message, ["special thing", "something special", "six toes", "6 toes", "extra toe", "toes on his foot"])
    ):
        unique_fact = personal_data.get("unique", "Karthikeyan has polydactyly and has six toes on his left foot.")
        return f"""✨ {unique_fact}"""

    # --------------------------------------------------------
    # 10. FULL NAME / REAL NAME / PREFERRED NAME / HIS NAME
    # --------------------------------------------------------
    is_name_query = (
        has_phrase(message, [
            "full name",
            "real name",
            "preferred name",
            "what is his name",
            "what is your name",
            "what's his name",
            "tell me his name",
            "tell his name",
            "his name",
            "karthikeyan name",
            "karthikeyan's name",
            "candidate name"
        ])
        or message == "name"
    )

    if is_name_query:
        full_name = personal_data.get("full_name", "Nattamai Ganesh Babu Karthikeyan")
        pref_name = personal_data.get("preferred_name", "Karthikeyan N G")
        return f"""👤 Full Name: {full_name}

⭐ Preferred Name: {pref_name}"""

    # --------------------------------------------------------
    # 11. WHO IS KARTHIKEYAN / ABOUT HIM
    # --------------------------------------------------------
    is_about_karthikeyan = (
        has_phrase(message, [
            "who is karthikeyan",
            "about karthikeyan",
            "tell me about karthikeyan",
            "who is he",
            "about him",
            "tell me about him",
            "describe karthikeyan",
            "introduce karthikeyan",
            "give me information about karthikeyan",
            "what do you know about karthikeyan"
        ])
    )

    if is_about_karthikeyan:
        about = personal_data.get("about", "")
        return f"""ℹ️ About Karthikeyan:

{about}

He enjoys building practical technology projects and continuously improving his programming and software development skills."""

    # --------------------------------------------------------
    # 12. DATE OF BIRTH / BIRTHDAY
    # --------------------------------------------------------
    if (
        has_phrase(message, ["date of birth", "birth date", "when was he born", "born date"])
        or has_word(message, ["dob", "birthday", "born"])
    ):
        dob = personal_data.get("date_of_birth", "21 August 2007")
        return f"""🎂 Karthikeyan was born on {dob}."""

    # --------------------------------------------------------
    # 13. CITY / HOMETOWN / LIVING
    # --------------------------------------------------------
    if (
        has_word(message, ["city", "hometown", "native"])
        or has_phrase(message, [
            "where is he living",
            "where does he live",
            "living place",
            "from where",
            "where is he from",
            "where is karthikeyan from"
        ])
    ):
        city = personal_data.get("city", "Madurai")
        return f"""📍 Karthikeyan is from {city}."""

    # --------------------------------------------------------
    # 14. CGPA
    # --------------------------------------------------------
    if has_word(message, ["cgpa", "gpa"]):
        cgpa = personal_data.get("education", {}).get("cgpa", "9.22")
        return f"""📊 Karthikeyan's CGPA is {cgpa} (up to Second Semester)."""

    # --------------------------------------------------------
    # 15. STANDALONE STANDARD (10th, 11th, 12th)
    # --------------------------------------------------------
    if message in ["10th", "10", "tenth", "10th std", "10th standard", "tenth standard", "about 10th"]:
        return finish(get_standard_summary(personal_data, "10th"))

    if message in ["11th", "11", "eleventh", "11th std", "11th standard", "eleventh standard", "about 11th"]:
        return finish(get_standard_summary(personal_data, "11th"))

    if message in ["12th", "12", "twelfth", "12th std", "12th standard", "twelfth standard", "about 12th"]:
        return finish(get_standard_summary(personal_data, "12th"))

    # --------------------------------------------------------
    # 16. SPECIFIC SUBJECT MARKS
    # (Checked BEFORE overall marks so specific questions are accurate)
    # --------------------------------------------------------
    # Check subjects by specificity: compound subjects first!
    ordered_subjects = [
        ("computer science", ["computer science", "cs"]),
        ("social science", ["social science", "social"]),
        ("mathematics", ["mathematics", "maths", "math"]),
        ("physics", ["physics"]),
        ("chemistry", ["chemistry"]),
        ("science", ["science"]),  # Checked after computer/social science
        ("tamil", ["tamil"]),
        ("english", ["english"])
    ]

    detected_subject = None
    for subj_key, triggers in ordered_subjects:
        for trig in triggers:
            # If short trigger like 'cs', match as standalone word
            if len(trig) <= 3:
                if has_word(message, trig):
                    detected_subject = subj_key
                    break
            else:
                if trig in message:
                    detected_subject = subj_key
                    break
        if detected_subject:
            break

    if detected_subject:
        # Check standard
        edu = personal_data.get("education", {})
        if re.search(r"\b(10th|10|tenth)\b", message):
            marks_10 = edu.get("10th", {}).get("marks", {})
            if detected_subject in marks_10:
                return finish(f"""📚 In 10th standard, Karthikeyan scored {marks_10[detected_subject]} in {detected_subject.title()}.""")
            else:
                return finish(f"""📚 {detected_subject.title()} was not in Karthikeyan's 10th standard curriculum.""")

        if re.search(r"\b(11th|11|eleventh)\b", message):
            marks_11 = edu.get("11th", {}).get("marks", {})
            val = marks_11.get(detected_subject, 0)
            if val != 0:
                return finish(f"""📚 In 11th standard, Karthikeyan scored {val} in {detected_subject.title()}.""")
            else:
                pct = edu.get("11th", {}).get("percentage", "92.00%")
                return finish(f"""📊 In 11th standard, Karthikeyan was in the Computer Science stream with an overall percentage of {pct} at The TVS School.\n\nIndividual subject mark for {detected_subject.title()} is not separately recorded.""")

        if re.search(r"\b(12th|12|twelfth)\b", message):
            marks_12 = edu.get("12th", {}).get("marks", {})
            if detected_subject in marks_12:
                return finish(f"""📚 In 12th standard, Karthikeyan scored {marks_12[detected_subject]} in {detected_subject.title()}.""")
            else:
                return finish(f"""📚 {detected_subject.title()} was not in Karthikeyan's 12th standard curriculum.""")

        # Subject marks across all standards
        res = get_subject_marks(personal_data, detected_subject)
        if res:
            return finish(res)

    # --------------------------------------------------------
    # 17. STANDARD PERCENTAGE / MARKS (10th, 11th, 12th)
    # --------------------------------------------------------
    is_percentage_or_mark = (
        has_word(message, ["percentage", "percent", "%", "score", "scores"])
        or has_phrase(message, ["marks", "mark", "percentage"])
    )

    edu = personal_data.get("education", {})

    if is_percentage_or_mark:
        is_pct_only = has_word(message, ["percentage", "percent", "%"]) and not has_word(message, ["mark", "marks", "score", "scores"])

        if re.search(r"\b(10th|10|tenth)\b", message):
            if is_pct_only:
                pct = edu.get("10th", {}).get("percentage", "92.2%")
                return finish(f"""📊 Karthikeyan scored {pct} in 10th standard.""")
            else:
                marks_10 = edu.get("10th", {}).get("marks", {})
                pct = edu.get("10th", {}).get("percentage", "92.2%")
                marks_lines = "\n".join([f"• {k.title()}: {v}" for k, v in marks_10.items()])
                return finish(f"""📊 Karthikeyan's 10th Standard Marks:\n\n{marks_lines}\n\n🏆 Overall Percentage: {pct} (Zion Good Shepherd's Matric Higher Secondary School)""")

        if re.search(r"\b(11th|11|eleventh)\b", message):
            if is_pct_only:
                pct = edu.get("11th", {}).get("percentage", "92.00%")
                return finish(f"""📊 Karthikeyan scored {pct} in 11th standard.""")
            else:
                marks_11 = edu.get("11th", {}).get("marks", {})
                pct = edu.get("11th", {}).get("percentage", "92.00%")
                marks_lines = "\n".join([f"• {k.title()}: {v}" for k, v in marks_11.items() if v != 0])
                return finish(f"""📊 Karthikeyan's 11th Standard Marks:\n\n{marks_lines}\n\n🏆 Overall Percentage: {pct} (The TVS School)""")

        if re.search(r"\b(12th|12|twelfth)\b", message):
            if is_pct_only:
                pct = edu.get("12th", {}).get("percentage", "90.17%")
                return finish(f"""📊 Karthikeyan scored {pct} in 12th standard.""")
            else:
                marks_12 = edu.get("12th", {}).get("marks", {})
                pct = edu.get("12th", {}).get("percentage", "90.17%")
                marks_lines = "\n".join([f"• {k.title()}: {v}" for k, v in marks_12.items()])
                return finish(f"""📊 Karthikeyan's 12th Standard Marks:\n\n{marks_lines}\n\n🏆 Overall Percentage: {pct} (The TVS School)""")

    # --------------------------------------------------------
    # 18. AGE (CRITICAL FIX: uses has_word so it never collides with 'percentage')
    # --------------------------------------------------------
    if (
        not is_percentage_or_mark
        and (has_word(message, ["age"]) or has_phrase(message, ["how old", "what is his age", "how old is he"]))
    ):
        age = personal_data.get("age", 19)
        return finish(f"""🎉 Karthikeyan is {age} years old.""")

    # --------------------------------------------------------
    # 19. SCHOOLS (10th, 11th, 12th)
    # --------------------------------------------------------
    is_school_query = (
        has_word(message, ["school", "studied", "completed", "schooling"])
        or has_phrase(message, ["which school", "what school", "school name"])
    )

    if is_school_query:
        if re.search(r"\b(10th|10|tenth)\b", message):
            sch = edu.get("10th", {}).get("school", "")
            return finish(f"""🏫 Karthikeyan completed his 10th standard at:\n\n{sch}""")

        if re.search(r"\b(11th|11|eleventh)\b", message):
            sch = edu.get("11th", {}).get("school", "")
            return finish(f"""🏫 Karthikeyan completed his 11th standard at:\n\n{sch}""")

        if re.search(r"\b(12th|12|twelfth)\b", message):
            sch = edu.get("12th", {}).get("school", "")
            return finish(f"""🏫 Karthikeyan completed his 12th standard at:\n\n{sch}""")

    # --------------------------------------------------------
    # 20. SCHOOL GROUP / STREAM
    # --------------------------------------------------------
    if has_word(message, ["group", "stream"]) or has_phrase(message, ["what group", "which group"]):
        return finish("""📚 Karthikeyan took the Computer Science group in both 11th and 12th standard.""")

    # --------------------------------------------------------
    # 21. CURRENT YEAR / STUDYING STATUS / GRADUATION
    # --------------------------------------------------------
    if has_phrase(message, ["current year", "college year", "which year", "year of studying"]):
        yr = edu.get("current_year", "Second Year")
        return finish(f"""🎓 Karthikeyan is currently in {yr} of college.""")

    if (
        has_word(message, ["graduate", "graduation"])
        or has_phrase(message, ["when will he complete college", "graduation year", "pass out", "passout", "finish college"])
    ):
        grad = edu.get("graduation_year", 2029)
        return finish(f"""🎓 Karthikeyan will likely graduate in {grad}.""")

    if has_phrase(message, ["is he studying", "currently studying", "studying now", "is karthikeyan studying", "is he a student"]):
        col = edu.get("college", "Coimbatore Institute of Engineering and Technology")
        dept = edu.get("department", "Computer Science and Engineering (Cyber Security)")
        yr = edu.get("current_year", "Second Year")
        grad = edu.get("graduation_year", 2029)
        return finish(f"""Yes! ✅\n\nKarthikeyan is currently studying {dept} at {col}.\n\nHe is in {yr} and will likely graduate in {grad}.""")

    # --------------------------------------------------------
    # 22. COLLEGE & DEPARTMENT
    # --------------------------------------------------------
    if has_word(message, ["college", "university", "institute", "campus"]):
        col = edu.get("college", "Coimbatore Institute of Engineering and Technology")
        return finish(f"""🎓 Karthikeyan studies at:\n\n{col}""")

    if has_word(message, ["department", "course", "branch", "degree"]):
        dept = edu.get("department", "Computer Science and Engineering (Cyber Security)")
        return finish(f"""💻 Karthikeyan is studying:\n\n{dept}""")

    # --------------------------------------------------------
    # 23. OVERALL EDUCATION
    # --------------------------------------------------------
    if (
        message == "education"
        or has_phrase(message, ["his education", "educational qualification", "education details", "tell me his education"])
    ):
        return finish(f"""🎓 Karthikeyan's Education\n\n🏫 10th Standard:\nSchool: {edu.get('10th', {}).get('school')}\nPercentage: {edu.get('10th', {}).get('percentage')}\n\n🏫 11th Standard:\nSchool: {edu.get('11th', {}).get('school')}\nPercentage: {edu.get('11th', {}).get('percentage')}\nGroup: {edu.get('11th', {}).get('group')}\n\n🏫 12th Standard:\nSchool: {edu.get('12th', {}).get('school')}\nPercentage: {edu.get('12th', {}).get('percentage')}\nGroup: {edu.get('12th', {}).get('group')}\n\n🎓 College:\n{edu.get('college')}\nDepartment: {edu.get('department')}\nCurrent Year: {edu.get('current_year')}\nCGPA: {edu.get('cgpa')} (up to Second Semester)""")

    # --------------------------------------------------------
    # 24. SKILLS
    # --------------------------------------------------------
    if has_phrase(message, ["programming languages", "coding languages", "what languages", "which languages"]):
        skills_data = personal_data.get("skills", {})
        langs = ", ".join(skills_data.get("programming_languages", []))
        return finish(f"""💻 Programming Languages Karthikeyan knows:\n\n{langs}""")

    if has_word(message, ["tools"]) or has_phrase(message, ["what tools", "tools used", "technologies used"]):
        skills_data = personal_data.get("skills", {})
        tools = ", ".join(skills_data.get("tools", []))
        return finish(f"""🛠️ Tools & Technologies Karthikeyan uses:\n\n{tools}""")

    if has_word(message, ["skills", "abilities", "skillset"]):
        return finish(get_skills_text(personal_data))

    # --------------------------------------------------------
    # 25. PROJECT LINKS & CONTEXTUAL FOLLOW-UPS (Checked BEFORE general projects)
    # --------------------------------------------------------
    is_link_query = (
        has_word(message, ["link", "links", "url", "repo", "repository", "github"])
        or has_phrase(message, ["give me the link", "show link", "project link", "link of", "where is the link"])
    )

    is_above_project_query = (
        has_phrase(message, [
            "above project", "this project", "that project", "the project",
            "of above project", "give me the link of the above project",
            "give me the link of above project", "link of the above project",
            "link of this project", "link of above project", "give me the link"
        ])
        or message in ["link", "project link", "give me the link", "link of project", "the link"]
    )

    if is_link_query:
        # 1. Specifically AI Movie Recommendation
        if has_phrase(message, ["movie", "ai movie", "movie recommendation"]):
            context["last_project"] = "movie_recommendation"
            return finish(get_project_link(personal_data, "movie_recommendation"))

        # 2. Specifically Government Scheme Navigator
        if has_phrase(message, ["government scheme", "scheme navigator", "hackathon"]):
            context["last_project"] = "government_scheme_navigator"
            return finish(get_project_link(personal_data, "government_scheme_navigator"))

        # 3. Specifically Hangman Game
        if has_phrase(message, ["hangman", "hangman game"]):
            context["last_project"] = "hangman"
            return finish(get_project_link(personal_data, "hangman"))

        # 4. Contextual "above project" follow-up
        if is_above_project_query:
            last_proj = context.get("last_project")
            if last_proj in ["movie_recommendation", "government_scheme_navigator", "hangman"]:
                return finish(get_project_link(personal_data, last_proj))
            return finish("""🚀 Karthikeyan's Project Links:

• Government Scheme Navigator:
  https://github.com/karthikeyanng4-hash/Hackproject.git

• AI Movie Recommendation System:
  https://github.com/karthikeyanng4-hash

• Hangman Game:
  https://hangman-game-q7e3nzsfl-karthikeyanng4-hashs-projects.vercel.app""")

    # --------------------------------------------------------
    # 26. ANOTHER PROJECT / NEXT PROJECT
    # --------------------------------------------------------
    if (
        has_phrase(message, ["another project", "next project", "other project", "more projects", "different project", "next one", "another one"])
        or message in ["another", "next"]
    ):
        last_proj = context.get("last_project")
        cycle = {
            "government_scheme_navigator": "movie_recommendation",
            "movie_recommendation": "hangman",
            "hangman": "government_scheme_navigator"
        }
        next_proj = cycle.get(last_proj, "movie_recommendation")
        context["last_project"] = next_proj
        return finish(get_project_text(personal_data, next_proj))

    # --------------------------------------------------------
    # 27. INDIVIDUAL PROJECTS (Checked BEFORE general project list)
    # --------------------------------------------------------
    if has_phrase(message, ["government scheme navigator", "government scheme", "scheme navigator", "hackathon project"]):
        context["last_project"] = "government_scheme_navigator"
        return finish(get_project_text(personal_data, "government_scheme_navigator"))

    if has_phrase(message, ["movie recommendation", "ai movie", "movie project", "give me the project of the ai movie project"]):
        context["last_project"] = "movie_recommendation"
        return finish(get_project_text(personal_data, "movie_recommendation"))

    if has_phrase(message, ["hangman", "hangman game", "game project"]):
        context["last_project"] = "hangman"
        return finish(get_project_text(personal_data, "hangman"))

    # --------------------------------------------------------
    # 28. PROJECTS OVERVIEW / LIST
    # --------------------------------------------------------
    is_projects_overview = (
        message in ["projects", "project", "list projects", "all projects"]
        or has_phrase(message, [
            "his projects", "projects he has done", "what projects", "what are the projects",
            "show me projects", "list projects", "tell me his projects", "completed projects",
            "what projects did he do", "what projects has he completed", "tell me about projects"
        ])
    )

    if is_projects_overview:
        return finish("""🚀 Karthikeyan has completed these projects:

• Government Scheme Navigator (AI-powered hackathon project)
• AI Movie Recommendation System (Machine learning project)
• Hangman Game (Interactive word guessing game)

Ask me about any specific project for details and links!""")

    # --------------------------------------------------------
    # 26. CAREER GOAL / AMBITION
    # --------------------------------------------------------
    if (
        has_word(message, ["career", "ambition", "aim"])
        or has_phrase(message, ["career goal", "future goal", "what does he want to become", "future plan", "dream job"])
    ):
        career = personal_data.get("career_goal", "")
        return f"""🎯 Career Goal:

{career}

He is dedicated to solving real-world challenges through innovative and scalable AI solutions."""

    # --------------------------------------------------------
    # 27. HOBBIES
    # --------------------------------------------------------
    if has_word(message, ["hobbies", "hobby"]) or has_phrase(message, ["free time", "for fun", "leisure", "what does he do"]):
        hobbies = personal_data.get("hobbies", [])
        items = "\n".join(f"• {h}" for h in hobbies)
        return f"""🎨 Karthikeyan enjoys:\n\n{items}"""

    # --------------------------------------------------------
    # 28. INTERESTS
    # --------------------------------------------------------
    if has_word(message, ["interests", "interest", "passion"]) or has_phrase(message, ["what does he like", "what is he interested in", "areas of interest"]):
        interests = personal_data.get("interests", [])
        items = "\n".join(f"• {i}" for i in interests)
        return f"""💡 Karthikeyan is interested in:\n\n{items}"""

    # --------------------------------------------------------
    # 29. PROFILES (LinkedIn, LeetCode, GitHub)
    # --------------------------------------------------------
    profiles = personal_data.get("profiles", {})

    if has_word(message, ["linkedin"]):
        return f"""🔗 Karthikeyan's LinkedIn Profile:\n\n{profiles.get('linkedin', '')}"""

    if has_word(message, ["leetcode"]):
        return f"""🔗 Karthikeyan's LeetCode Profile:\n\n{profiles.get('leetcode', '')}"""

    if has_word(message, ["github"]):
        return f"""🔗 Karthikeyan's GitHub Profile:\n\n{profiles.get('github', '')}"""

    if has_word(message, ["profiles", "socials", "links"]) or has_phrase(message, ["social media", "profile links"]):
        return f"""🔗 Karthikeyan's Profiles:

• LinkedIn: {profiles.get('linkedin', '')}
• GitHub: {profiles.get('github', '')}
• LeetCode: {profiles.get('leetcode', '')}"""

    # --------------------------------------------------------
    # 30. IDENTITY / ABOUT THE BOT
    # --------------------------------------------------------
    if has_phrase(message, ["who are you", "what are you", "about you", "yourself", "introduce yourself", "what is this chatbot", "who is this"]):
        return """🤖 I am Karthikeyan's Personal AI Assistant.

I can answer questions about:
🎓 Education & CGPA
💻 Skills & Tech Stack
🚀 Projects & GitHub Links
🎯 Career Goals
🎨 Hobbies & Interests
👨‍👩‍👦 Family
✨ Unique Facts & Traits
🔗 Professional Profiles"""

    # --------------------------------------------------------
    # 31. GREETINGS (CRITICAL FIX: uses has_word to prevent collision with 'his', 'which', 'him')
    # --------------------------------------------------------
    if (
        has_word(message, ["hello", "hi", "hey", "greetings", "sup", "hola"])
        or has_phrase(message, ["good morning", "good afternoon", "good evening", "hey there", "hi there", "hello chatbot"])
    ):
        return """Hello! 👋

I am Karthikeyan's Personal AI Assistant 🤖

Ask me anything about Karthikeyan!"""

    # --------------------------------------------------------
    # 32. HELP
    # --------------------------------------------------------
    if has_word(message, ["help"]) or has_phrase(message, ["what can i ask", "what questions", "how can you help"]):
        return """💡 You can ask me questions like:

• "Who is Karthikeyan?"
• "Does he have an elder brother?"
• "What are his skills?"
• "What projects has he built?"
• "Which college does he study in?"
• "What is his CGPA?"
• "What is his 10th and 12th percentage?"
• "Tell me about his family."
• "Show his LinkedIn / GitHub profile."
• "What is something unique about him?"
"""

    # --------------------------------------------------------
    # 33. COURTESY / THANKS
    # --------------------------------------------------------
    if has_word(message, ["thanks", "thank", "thx"]) or has_phrase(message, ["thank you", "thanks a lot", "thank you so much"]):
        return """You're welcome! 😊

I'm always happy to help you learn more about Karthikeyan! 🤖"""

    # --------------------------------------------------------
    # 34. GOODBYE
    # --------------------------------------------------------
    if has_word(message, ["bye", "goodbye", "cya"]) or has_phrase(message, ["see you", "see you later", "take care", "have a good day"]):
        return """Goodbye! 👋

Have a great day! 😊"""

    # --------------------------------------------------------
    # 35. NLP ML INTENT CLASSIFICATION FALLBACK
    # --------------------------------------------------------
    if model and vectorizer:
        try:
            x = vectorizer.transform([message])
            probabilities = model.predict_proba(x)[0]
            max_prob = max(probabilities)
            predicted_tag = model.classes_[probabilities.argmax()]

            if max_prob >= 0.30:
                intent_responses = {
                    "greeting": """Hello! 👋\n\nI am Karthikeyan's Personal AI Assistant 🤖\n\nAsk me anything about Karthikeyan!""",
                    "goodbye": """Goodbye! 👋\n\nHave a great day! 😊""",
                    "thanks": """You're welcome! 😊\n\nI'm always happy to help you learn more about Karthikeyan! 🤖""",
                    "help": """💡 You can ask me about Karthikeyan's education, skills, projects, career, family, hobbies, CGPA, or profiles!""",
                    "identity": """🤖 I am Karthikeyan's Personal AI Assistant. Ask me anything about Karthikeyan!""",
                    "about_me": f"""ℹ️ About Karthikeyan:\n\n{personal_data.get('about', '')}""",
                    "full_name": f"""👤 Full Name: {personal_data.get('full_name')}\n\n⭐ Preferred Name: {personal_data.get('preferred_name')}""",
                    "age": f"""🎉 Karthikeyan is {personal_data.get('age', 19)} years old.""",
                    "birthday": f"""🎂 Karthikeyan was born on {personal_data.get('date_of_birth', '21 August 2007')}.""",
                    "city": f"""📍 Karthikeyan is from {personal_data.get('city', 'Madurai')}.""",
                    "college": f"""🎓 Karthikeyan studies at:\n\n{personal_data.get('education', {}).get('college')}""",
                    "department": f"""💻 Karthikeyan is studying:\n\n{personal_data.get('education', {}).get('department')}""",
                    "college_year": f"""🎓 Karthikeyan is currently in {personal_data.get('education', {}).get('current_year')} of college.""",
                    "graduation": f"""🎓 Karthikeyan will likely graduate in {personal_data.get('education', {}).get('graduation_year')}.""",
                    "10th_education": f"""🏫 Karthikeyan completed his 10th standard at:\n\n{personal_data.get('education', {}).get('10th', {}).get('school')}""",
                    "10th_marks": f"""📊 Karthikeyan scored {personal_data.get('education', {}).get('10th', {}).get('percentage')} in 10th standard.""",
                    "11th_education": f"""🏫 Karthikeyan completed his 11th standard at:\n\n{personal_data.get('education', {}).get('11th', {}).get('school')}""",
                    "11th_marks": f"""📊 Karthikeyan scored {personal_data.get('education', {}).get('11th', {}).get('percentage')} in 11th standard.""",
                    "12th_education": f"""🏫 Karthikeyan completed his 12th standard at:\n\n{personal_data.get('education', {}).get('12th', {}).get('school')}""",
                    "12th_marks": f"""📊 Karthikeyan scored {personal_data.get('education', {}).get('12th', {}).get('percentage')} in 12th standard.""",
                    "programming_languages": f"""💻 Programming Languages:\n{', '.join(personal_data.get('skills', {}).get('programming_languages', []))}""",
                    "technical_skills": get_skills_text(personal_data),
                    "tools": f"""🛠️ Tools & Technologies:\n{', '.join(personal_data.get('skills', {}).get('tools', []))}""",
                    "projects": """🚀 Karthikeyan has completed: Government Scheme Navigator, AI Movie Recommendation System, and Hangman Game.""",
                    "government_scheme_project": get_project_text(personal_data, "government_scheme_navigator"),
                    "movie_recommendation_project": get_project_text(personal_data, "movie_recommendation"),
                    "hangman_project": get_project_text(personal_data, "hangman"),
                    "career_goal": f"""🎯 Career Goal:\n\n{personal_data.get('career_goal')}""",
                    "interests": f"""💡 Karthikeyan is interested in: {', '.join(personal_data.get('interests', []))}.""",
                    "hobbies": f"""🎨 Karthikeyan's hobbies: {', '.join(personal_data.get('hobbies', []))}.""",
                    "family": f"""👨‍👩‍👦 Karthikeyan's family has 4 members: Karthikeyan, Father ({family.get('father')}), Mother ({family.get('mother')}), and Younger Brother ({younger_brother}).""",
                    "father": f"""👨 Karthikeyan's father is {family.get('father')}.""",
                    "mother": f"""👩 Karthikeyan's mother is {family.get('mother')}.""",
                    "elder_brother": f"""❌ No, Karthikeyan does not have an elder brother.\n\n👦 He has only one younger brother, and his name is {younger_brother}.""",
                    "younger_brother": f"""✅ Yes, Karthikeyan has one younger brother named {younger_brother}.""",
                    "brother": f"""👦 Karthikeyan has only one younger brother named {younger_brother}.""",
                    "sister": f"""❌ No, Karthikeyan does not have a sister.\n\n👦 He has only one younger brother named {younger_brother}.""",
                    "linkedin": f"""🔗 Karthikeyan's LinkedIn Profile:\n{profiles.get('linkedin')}""",
                    "github": f"""🔗 Karthikeyan's GitHub Profile:\n{profiles.get('github')}""",
                    "leetcode": f"""🔗 Karthikeyan's LeetCode Profile:\n{profiles.get('leetcode')}"""
                }

                if predicted_tag in intent_responses:
                    return intent_responses[predicted_tag]
        except Exception:
            pass

    # --------------------------------------------------------
    # 36. DEFAULT FALLBACK
    # --------------------------------------------------------
    return """Sorry 😅 I don't understand that question yet.

Try asking me about Karthikeyan's:
• Education & 10th / 12th marks & percentage
• Skills & programming languages
• Projects (Government Scheme Navigator, Movie Recommendation, Hangman)
• Career goal & ambition
• College, department, and CGPA
• Family members
• LinkedIn, GitHub, or LeetCode profiles
• Unique traits 
"""