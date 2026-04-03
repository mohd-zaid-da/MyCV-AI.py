import customtkinter as ctk
from tkinter import filedialog
import pdfplumber
import json, os, hashlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

#APP
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("MyCV AI")
app.geometry("1200x720")

#DB
USER_DB = "users.json"
if not os.path.exists(USER_DB):
    with open(USER_DB, "w") as f:
        json.dump({}, f)

with open(USER_DB, "r") as f:
    
    users = json.load(f)

for u in users:
    if isinstance(users[u], str):
        users[u] = {"password": hashlib.sha256(users[u].encode()).hexdigest()}

def save_users():
    with open(USER_DB, "w") as f:
        json.dump(users, f, indent=4)

#GLOBAL
current_user = None
uploaded_resume_text = ""
dropdown = None
tooltip = None

#SECURITY
def hash_password(p):
    return hashlib.sha256(p.encode()).hexdigest()

#TOOLTIP
def show_tooltip(widget, text):
    global tooltip
    x = widget.winfo_rootx() - app.winfo_rootx() + 30
    y = widget.winfo_rooty() - app.winfo_rooty() + 40
    tooltip = ctk.CTkLabel(app, text=text, fg_color="#333", corner_radius=5)
    tooltip.place(x=x, y=y)

def hide_tooltip():
    global tooltip
    if tooltip:
        tooltip.destroy()
        tooltip = None

#JOB PROFILES
job_profiles = dict(sorted({
"AI Engineer": ["python","deep learning","nlp","tensorflow","pytorch","computer vision","model tuning","deployment","api","optimization"],
"API Developer": ["api","nodejs","python","django","flask","debugging","testing","security","integration","deployment"],
"AR/VR Developer": ["unity","c#","3d modeling","animation","vr","ar","debugging","ui","interaction","optimization"],
"Android Developer": ["java","kotlin","android studio","xml","firebase","api","debugging","testing","deployment","ui"],
"App Tester": ["testing","qa","automation","debugging","api testing","performance","reporting","tools","manual testing","analysis"],
"Automation Engineer": ["automation","python","selenium","testing","debugging","scripts","tools","ci/cd","performance","analysis"],
"Automation Robotics Engineer": ["robotics","automation","python","control systems","ai","debugging","simulation","electronics","design","testing"],
"Automation Tester": ["selenium","python","testng","automation frameworks","api testing","ci/cd","debugging","scripts","performance","reporting"],

"Backend Developer": ["nodejs","express","django","flask","sql","mongodb","api dev","authentication","debugging","deployment"],
"Big Data Engineer": ["hadoop","spark","scala","python","etl","data pipelines","hive","kafka","debugging","optimization"],
"Bioinformatics Engineer": ["biology","python","data analysis","genomics","statistics","tools","debugging","research","visualization","algorithms"],
"Blockchain Developer": ["solidity","ethereum","web3","smart contracts","cryptography","nodejs","api","debugging","security","testing"],

"C++ Developer": ["c++","dsa","oop","debugging","algorithms","system design","testing","optimization","git","development"],
"Civil Engineer": ["autocad","construction management","structural design","surveying","project planning","materials","site management","safety","cost estimation","analysis"],
"Cloud Architect": ["aws","azure","gcp","architecture","security","networking","deployment","scalability","monitoring","design"],
"Cloud Engineer": ["aws","azure","gcp","linux","networking","storage","deployment","monitoring","security","virtualization"],
"Cloud Security Engineer": ["cloud security","aws","azure","gcp","networking","encryption","compliance","monitoring","debugging","risk"],
"Content Writer": ["writing","seo","research","editing","blogging","storytelling","grammar","content strategy","proofreading","creativity"],
"Cyber Security Analyst": ["network security","siem","incident response","encryption","risk","vulnerability","compliance","forensics","firewall","analysis"],

"Data Analyst": ["python","sql","excel","power bi","tableau","pandas","numpy","statistics","data cleaning","visualization"],
"Data Engineer": ["python","sql","etl","spark","hadoop","data warehousing","pipeline","airflow","debugging","optimization"],
"Data Scientist": ["python","r","machine learning","statistics","pandas","numpy","deep learning","sql","feature engineering","visualization"],
"Data Visualization Engineer": ["tableau","power bi","excel","python","visualization","dashboard","reporting","analysis","design","communication"],
"Database Administrator": ["sql","mysql","oracle","backup","recovery","tuning","security","indexing","query optimization","monitoring"],
"DevOps Engineer": ["docker","kubernetes","aws","linux","ci/cd","terraform","monitoring","networking","security","scripting"],
"Digital Marketer": ["seo","sem","social media","content","analytics","ads","branding","campaigns","strategy","optimization"],

"Electrical Engineer": ["circuit design","matlab","power systems","control systems","electronics","simulation","debugging","wiring","testing","maintenance"],
"Embedded Systems Engineer": ["c","c++","microcontrollers","embedded c","iot","debugging","hardware interfacing","rtos","circuit design","testing"],
"Ethical Hacker": ["penetration testing","kali linux","networking","metasploit","burp suite","web security","exploitation","osint","reporting","scripting"],

"Financial Analyst": ["finance","excel","valuation","analysis","reporting","forecasting","data analysis","models","communication","strategy"],
"Firmware Engineer": ["c","embedded","firmware","debugging","microcontrollers","testing","hardware","rtos","optimization","development"],
"Forensic Analyst": ["cyber forensics","investigation","data recovery","analysis","reporting","security","tools","debugging","networking","compliance"],
"Frontend Developer": ["html","css","javascript","react","redux","bootstrap","ui design","api calls","debugging","optimization"],
"Full Stack Developer": ["html","css","javascript","react","nodejs","mongodb","git","api","deployment","debugging"],

"Game Developer": ["unity","c#","unreal engine","3d modeling","animation","ai logic","debugging","level design","physics","optimization"],
"Game Tester": ["testing","debugging","bug tracking","gameplay","analysis","reporting","tools","qa","automation","performance"],
"GIS Analyst": ["gis","mapping","data analysis","remote sensing","arcgis","qgis","visualization","reporting","tools","analysis"],

"HR Analyst": ["excel","analytics","recruitment","communication","reporting","data analysis","tools","hr systems","planning","strategy"],
"Hardware Engineer": ["hardware","circuits","design","testing","debugging","electronics","tools","analysis","prototyping","maintenance"],

"IT Support Engineer": ["troubleshooting","hardware","networking","windows","linux","support","debugging","ticketing","communication","maintenance"],
"IoT Engineer": ["iot","arduino","raspberry pi","sensors","networking","cloud integration","embedded c","python","debugging","security"],
"Investment Analyst": ["finance","valuation","models","excel","analysis","research","reporting","forecasting","risk","strategy"],
"iOS Developer": ["swift","ios","xcode","ui design","api","debugging","testing","deployment","core data","git"],

"Java Developer": ["java","spring","oop","dsa","debugging","testing","sql","api","git","deployment"],

"Machine Learning Engineer": ["python","numpy","pandas","sklearn","tensorflow","pytorch","mlops","deployment","api","debugging"],
"Mechanical Engineer": ["cad","solidworks","thermodynamics","mechanics","design","simulation","testing","manufacturing","materials","maintenance"],
"Mobile App Developer": ["flutter","react native","java","kotlin","ui design","api integration","debugging","testing","deployment","firebase"],

"Network Engineer": ["networking","ccna","routing","switching","tcp/ip","vpn","firewall","monitoring","troubleshooting","security"],

"Operations Analyst": ["excel","data analysis","sql","reporting","optimization","process","communication","analysis","planning","strategy"],

"Penetration Tester": ["security testing","kali linux","networking","metasploit","burp suite","exploitation","reporting","osint","debugging","analysis"],
"Performance Engineer": ["performance testing","load testing","analysis","debugging","optimization","tools","monitoring","reporting","qa","automation"],
"Product Manager": ["agile","communication","roadmap","analytics","stakeholders","scrum","strategy","planning","prioritization","management"],
"Project Manager": ["scrum","planning","risk management","budgeting","communication","leadership","reporting","stakeholders","timeline","execution"],
"Python Developer": ["python","django","flask","api","debugging","testing","oop","sql","git","deployment"],

"QA Engineer": ["testing","selenium","manual testing","automation","api testing","performance","debugging","test cases","bug tracking","reporting"],

"R&D Engineer": ["research","development","testing","design","analysis","debugging","tools","innovation","prototyping","engineering"],
"Research Engineer": ["research","python","analysis","algorithms","data","experiments","debugging","reporting","tools","innovation"],
"Robotics Engineer": ["robotics","python","control systems","ai","sensor integration","simulation","debugging","automation","electronics","design"],

"SEO Specialist": ["seo","analytics","keyword research","google analytics","content","optimization","link building","reporting","tools","strategy"],
"Security Engineer": ["security","networking","encryption","firewall","monitoring","analysis","debugging","tools","risk","compliance"],
"Site Reliability Engineer": ["linux","monitoring","devops","cloud","scripting","debugging","incident management","automation","ci/cd","networking"],
"Software Engineer": ["java","python","dsa","algorithms","oop","system design","debugging","git","testing","problem solving"],
"Software Tester": ["testing","manual testing","automation","selenium","debugging","reporting","qa","tools","performance","analysis"],
"Solution Architect": ["system design","architecture","api","cloud","security","scalability","debugging","integration","design","planning"],
"Supply Chain Analyst": ["logistics","excel","analysis","planning","forecasting","inventory","optimization","reporting","communication","strategy"],
"System Administrator": ["linux","windows server","networking","scripting","backup","security","user management","monitoring","troubleshooting","virtualization"],
"System Engineer": ["system design","networking","linux","debugging","deployment","monitoring","security","tools","analysis","optimization"],

"Talent Acquisition Specialist": ["recruitment","interviewing","communication","sourcing","hr tools","screening","analysis","planning","strategy","negotiation"],
"Technical Writer": ["documentation","writing","api docs","research","editing","tools","communication","clarity","formatting","review"],
"Telecom Engineer": ["telecom","networking","signal processing","debugging","analysis","tools","communication","design","optimization","testing"],

"UI Designer": ["figma","adobe xd","typography","color theory","wireframing","prototyping","ui kits","design systems","responsive","research"],
"UI Developer": ["html","css","javascript","react","ui design","debugging","api","optimization","responsive","tools"],
"UX Designer": ["user research","wireframing","figma","usability testing","prototyping","journey mapping","persona","interaction design","accessibility","analysis"],

"Web Developer": ["html","css","javascript","react","nodejs","git","api","debugging","responsive design","browser tools"],
"AI Researcher": ["python","deep learning","research","nlp","computer vision","papers","algorithms","experiments","analysis","innovation"],

"Business Analyst": ["excel","sql","communication","requirements","analysis","reporting","stakeholders","process","documentation","strategy"],

"Computer Vision Engineer": ["python","opencv","deep learning","image processing","tensorflow","pytorch","algorithms","debugging","optimization","deployment"],

"Data Architect": ["data modeling","sql","data warehousing","etl","architecture","big data","governance","security","optimization","design"],

"ERP Consultant": ["sap","oracle","erp","business processes","implementation","configuration","support","analysis","training","documentation"],

"Flutter Developer": ["flutter","dart","ui","api integration","firebase","debugging","testing","deployment","responsive","git"],

"Growth Hacker": ["marketing","analytics","seo","experiments","conversion","strategy","data","ads","optimization","tools"],

"Help Desk Technician": ["troubleshooting","support","hardware","software","networking","ticketing","communication","windows","linux","maintenance"],

"Information Security Analyst": ["security","risk","compliance","network security","encryption","siem","monitoring","analysis","incident response","tools"],

"JavaScript Developer": ["javascript","react","nodejs","api","debugging","frontend","backend","git","testing","optimization"],

"Knowledge Engineer": ["ai","knowledge base","ontology","nlp","reasoning","data modeling","semantic web","analysis","tools","development"],

"Linux Administrator": ["linux","shell scripting","networking","security","monitoring","backup","troubleshooting","servers","deployment","maintenance"],

"Marketing Analyst": ["analytics","excel","sql","campaigns","data analysis","reporting","strategy","visualization","tools","optimization"],

"Network Security Engineer": ["networking","firewall","vpn","ids/ips","security","monitoring","encryption","risk","compliance","analysis"],

"Oracle DBA": ["oracle","sql","database","backup","recovery","tuning","performance","security","monitoring","administration"],

"Prompt Engineer": ["ai","llms","prompt design","nlp","testing","optimization","experiments","analysis","tools","deployment"],

"Quantum Computing Engineer": ["quantum computing","python","qiskit","algorithms","research","physics","simulation","math","analysis","innovation"],

"Robotic Process Automation Developer": ["rpa","uipath","automation","scripts","debugging","process","tools","deployment","testing","optimization"],

"Salesforce Developer": ["salesforce","apex","crm","api","integration","debugging","deployment","testing","automation","configuration"],

"Technical Support Engineer": ["troubleshooting","support","networking","software","hardware","debugging","communication","tools","analysis","maintenance"],

"UI Animator": ["animation","after effects","ui","motion design","adobe","prototyping","creativity","design","tools","interaction"],

"VLSI Engineer": ["vlsi","verilog","chip design","simulation","electronics","testing","layout","debugging","tools","analysis"],

"WordPress Developer": ["wordpress","php","themes","plugins","seo","debugging","html","css","deployment","optimization"],

"Xamarin Developer": ["xamarin","c#","mobile apps","ui","api integration","debugging","testing","deployment","cross-platform","tools"],

"YouTube Content Creator": ["video editing","content creation","seo","thumbnail design","script writing","analytics","audience engagement","branding","social media","creativity"],

"Zoologist": ["biology","animal behavior","research","field study","data analysis","ecology","reporting","observation","conservation","documentation"]

}.items()))

#RESUME
def extract_text(path):
    text = ""
    with pdfplumber.open(path) as pdf:
        for p in pdf.pages:
            text += p.extract_text() or ""
    return text.lower()

def upload_resume():
    global uploaded_resume_text
    file = filedialog.askopenfilename(filetypes=[("PDF","*.pdf")])
    if file:
        uploaded_resume_text = extract_text(file)
        result_box.insert("end", "Resume uploaded\n")

#NEW CHART FUNCTION
def update_chart(score, ats):
    ax.clear()
    ax.set_facecolor("#1C1C1E")

    bars = ax.bar(["Match", "ATS"], [score, ats])

    ax.set_ylim(0,100)
    ax.set_title("Performance", color="white")
    ax.tick_params(colors='white')

    for bar in bars:
        bar.set_color("#007AFF")

    canvas.draw()

def analyze_resume():
    if not uploaded_resume_text:
        result_box.insert("end", "Upload resume first \n")
        return

    job = job_var.get()
    skills = job_profiles[job]

    found = [s for s in skills if s in uploaded_resume_text]
    missing = list(set(skills) - set(found))
    score = int(len(found)/len(skills)*100)

    word_count = len(uploaded_resume_text.split())
    ats_score = int((score*0.6) + min(word_count/500*40, 40))

    # KPI update
    kpi_score.configure(text=f"{score}%")
    kpi_skills.configure(text=f"{len(found)}")
    kpi_ats.configure(text=f"{ats_score}%")

    update_chart(score, ats_score)

    # CLEAN RESULT FORMAT
    result_box.delete("0.0","end")

    result_box.insert("end", "ANALYSIS REPORT\n\n")
    result_box.insert("end", f" Match Score: {score}%\n")
    result_box.insert("end", f" ATS Score: {ats_score}%\n\n")

    result_box.insert("end", " Missing Skills:\n")
    for m in missing:
        result_box.insert("end", f"  • {m}\n")

    result_box.insert("end", "\n💡 Suggestions:\n")
    for m in missing:
        result_box.insert("end", f"  • Add {m}\n")

    if word_count < 300:
        result_box.insert("end", "  • Resume too short\n")

#AUTH
def login():
    global current_user
    user = entry_username.get()
    pwd = entry_password.get()

    if user in users and users[user]["password"] == hash_password(pwd):
        current_user = user
        open_dashboard()
    else:
        label_msg.configure(text="Invalid credentials", text_color="red")

def signup():
    user = entry_username.get()
    pwd = entry_password.get()

    if not user or not pwd:
        label_msg.configure(text="Fill all fields", text_color="red")
        return

    if user in users:
        label_msg.configure(text="User exists", text_color="red")
        return

    users[user] = {"password": hash_password(pwd)}
    save_users()
    label_msg.configure(text="Account created", text_color="green")

def logout():
    global current_user, dropdown

    # Clear user session
    current_user = None

    # Close dropdown if open
    if dropdown and dropdown.winfo_exists():
        dropdown.destroy()
        dropdown = None

    # Reset UI fields
    entry_username.delete(0, "end")
    entry_password.delete(0, "end")
    label_msg.configure(text="Logged out successfully", text_color="green")

    # Hide dashboard
    dashboard_frame.pack_forget()

    # Show login screen
    login_frame.place(relx=0.5, rely=0.5, anchor="center")

    # Clear results safely
    try:
        result_box.delete("0.0", "end")
    except:
        pass

#DROPDOWN
def toggle_dropdown(event=None):
    global dropdown

    if dropdown and dropdown.winfo_exists():
        dropdown.destroy()
        dropdown = None
        return

    x = profile_icon.winfo_rootx() - app.winfo_rootx()
    y = profile_icon.winfo_rooty() - app.winfo_rooty() + 50

    dropdown = ctk.CTkFrame(app, width=160, corner_radius=10)
    dropdown.place(x=x-100, y=y)

    ctk.CTkLabel(dropdown, text=current_user).pack(pady=5)

    ctk.CTkButton(dropdown,text="Logout",fg_color="#ef4444",hover_color="#dc2626",command=logout).pack(pady=5, padx=10, fill="x")

#LOGIN UI
login_frame = ctk.CTkFrame(app,corner_radius=30,
    fg_color="#1a1a1a" #glass dark feel
)

login_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.35, relheight=0.55)

#L-TITLE
ctk.CTkLabel(login_frame,text="MyCV AI",font=("Helvetica", 32, "bold")).pack(pady=(30, 10))

#L-SUBTITLE
ctk.CTkLabel(login_frame,text="Login to continue",text_color="gray").pack(pady=(0, 20))

#L-INPUTS
entry_username = ctk.CTkEntry(login_frame,placeholder_text="Username",height=40,corner_radius=15)
entry_username.pack(pady=10, padx=40, fill="x")

entry_password = ctk.CTkEntry(login_frame,placeholder_text="Password",show="*",height=40,corner_radius=15)
entry_password.pack(pady=10, padx=40, fill="x")

#L-MESSAGE
label_msg = ctk.CTkLabel(login_frame, text="")
label_msg.pack(pady=5)

#LOGIN BUTTON
ctk.CTkButton(login_frame,text="Login",height=45,corner_radius=20,command=login).pack(pady=(20, 10), padx=40, fill="x")

# ---------------- SIGNUP BUTTON ----------------
ctk.CTkButton(login_frame,text="Create Account",height=45,corner_radius=20,fg_color="#2563eb",     # modern blue
hover_color="#1e40af",command=signup).pack(pady=10, padx=40, fill="x")

# ---------------- FOOTER ----------------
ctk.CTkLabel(login_frame,text="© 2026 MyCV AI",text_color="gray").pack(side="bottom", pady=15)


# ---------------- DASHBOARD ----------------
dashboard_frame = ctk.CTkFrame(app)

header = ctk.CTkFrame(dashboard_frame)
header.pack(fill="x")

logout_icon = ctk.CTkButton(header, text="logout", width=40, command=logout)
logout_icon.pack(side="right", padx=10, pady=10)

logout_icon.bind("<Enter>", lambda e: show_tooltip(logout_icon, "Logout"))
logout_icon.bind("<Leave>", lambda e: hide_tooltip())

profile_icon = ctk.CTkLabel(header, text="", width=40, height=40, corner_radius=20, fg_color="#007AFF")
profile_icon.pack(side="right", padx=10)
profile_icon.bind("<Button-1>", toggle_dropdown)

# KPI CARDS
def create_kpi(parent, title, value):
    box = ctk.CTkFrame(parent, corner_radius=15)
    box.pack(side="left", expand=True, fill="x", padx=10)

    ctk.CTkLabel(box, text=title, text_color="#A1A1AA").pack(pady=(10,0))
    label = ctk.CTkLabel(box, text=value, font=("Helvetica", 24, "bold"))
    label.pack(pady=10)

    return label

kpi_frame = ctk.CTkFrame(dashboard_frame, fg_color="transparent")
kpi_frame.pack(fill="x", padx=40, pady=20)

kpi_score = create_kpi(kpi_frame, "Match Score", "0%")
kpi_skills = create_kpi(kpi_frame, "Skills Match", "0")
kpi_ats = create_kpi(kpi_frame, "ATS Score", "0%")

# CENTER CONTROLS
center_frame = ctk.CTkFrame(dashboard_frame, fg_color="transparent")
center_frame.pack()

job_var = ctk.StringVar(value=list(job_profiles.keys())[0])
ctk.CTkOptionMenu(center_frame, values=list(job_profiles.keys()), variable=job_var).pack(pady=10)

ctk.CTkButton(center_frame, text="Upload Resume", command=upload_resume).pack(pady=5)
ctk.CTkButton(center_frame, text="Analyze", command=analyze_resume).pack(pady=5)

# Chart
fig = plt.Figure(figsize=(5,3), facecolor="#1C1C1E")
ax = fig.add_subplot(111)
ax.set_facecolor("#1C1C1E")

canvas = FigureCanvasTkAgg(fig, master=dashboard_frame)
canvas.get_tk_widget().pack(pady=20)

# Result
result_box = ctk.CTkTextbox(dashboard_frame, height=150)
result_box.pack(fill="x", padx=20, pady=10)

#OPEN
def open_dashboard():
    login_frame.place_forget()
    dashboard_frame.pack(fill="both", expand=True)
    profile_icon.configure(text=current_user[0].upper())

app.mainloop()
