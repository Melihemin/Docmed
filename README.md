# Team Name: AI’m Fine 


Our Trello Link: https://trello.com/invite/b/685aa4443a00e4e2ff9b8756/ATTIf4340459b7dd4851d03b223950619c8b97BEF699/yzta-bootcamp

## Demo Video

https://github.com/user-attachments/assets/8de424cd-50ff-46a5-8e86-580e83a113d5


https://youtu.be/mF2d6E-SeuQ

# Docmed – AI-Powered Medical Decision Assistant

Docmed is a smart health assistant system. It helps patients explain their symptoms, supports doctors in making decisions, and gives medical students a place to learn from real cases. The system has four main modules:

- Patient Module – Writing Symptoms
- Doctor Module – Managing Cases
- Education Module – Medical Learning
- Report Module – Full Medical Reports

---

## Patient Module – Writing Symptoms

Patients can write their symptoms in their own words. They don’t need to use medical language. The system:

- Understands and changes these words into medical terms.
- Analyzes the situation and gives an urgency level:
  - Green: Low risk
  - Yellow: Medium risk
  - Red: High risk
- Creates a short summary of the case.
- Sends this summary to the doctor automatically.

---

## Doctor Module – Managing Cases

Doctors see a full list of patients, including:

- National ID number
- Time of visit
- Medical department
- Urgency level (Green, Yellow, Red)

For each patient, doctors can:

- View AI-generated suggestions:
  - 3 possible diseases (with percentage chances)
  - Recommended medicines
  - Recovery suggestions
- Read patient symptoms and AI analysis together
- Write their own notes
- Use the report section to create a full medical report (explained below)

---

## Education Module – Medical Learning

This module is for medical students and doctors in training. Users can:

- Choose cases by urgency (Green, Yellow, Red)
- See:
  - Patient symptoms
  - Suggested diseases and chances
  - Recommended treatments
  - Recovery advice
- Check the doctor's final decision, notes, and full report
- Learn from real examples and improve decision skills

---

## Report Module – Full Medical Reports

The system creates a detailed medical report for each case. Reports include:

### AI-Powered Pre-Diagnosis
- Based on symptoms, the system shows if it may be:
  - Common cold
  - Flu
  - Sinus infection
- Each suggestion has a percentage chance

### Clinical Diagnosis
- The doctor gives the final diagnosis

### Treatment Plan and Suggestions
- Suggested medicines
- Daily care advice (rest, hydration, etc.)

### Natural Support
- Herbal and vitamin recommendations
- Foods and drinks that support recovery

### Things to Avoid
- Physical overwork
- Alcohol, smoking
- Processed and sugary foods

### Recovery Timeline and Guidance
- Estimated healing time
- What to do to recover faster
- What to do if symptoms get worse after 3–4 days

### Patient Info and References
- Patient’s ID
- Report ID and date

---

## Why Use Docmed?

- Easy to write symptoms in natural language
- Fast AI support for doctors
- Real cases for medical education
- Complete and organized reports
- Modular system, easy to grow and improve

> Docmed helps patients explain, doctors decide, and students learn — all in one smart system.
![WhatsApp Image 2025-08-03 at 15 44 59](https://github.com/user-attachments/assets/fb07ddc0-75f4-4a24-8d3f-5e8ed7d2fe31)


## Fine-Tuning the AI Model for Medical Reporting
The core of Docmed's intelligence lies in a fine-tuned Gemini model. A general-purpose AI model is powerful, but to understand the nuances of patient symptoms and convert them into structured medical reports, it needs specialized training.

  - 1. The Goal: Teaching the AI to be a Medical Scribe
Our goal is to teach the model a single, critical task: take a patient's informal, everyday language description of their symptoms (input_text) and transform it into a standardized, professional, and data-rich HTML report (output_text) that a doctor can immediately use.

  - 2. Preparing the Training Data
The model learns from examples. We created a dataset in the JSON Lines (.jsonl) format, where each line is a complete training example.

input_text: A string containing patient information, complaints, and other details, written in a semi-structured format.

output_text: The corresponding, perfectly formatted HTML report the model is expected to produce.

Example data (gemini_model/train_data.jsonl):

```json

{"input_text": "HASTA BİLGİLERİ: Adı Soyadı: Ayşe Yılmaz, T.C. Kimlik No: 12345678901... --- ŞİKAYETLER: Şiddetli baş ağrısı ve ateş... --- DOKTOR: Dr. Elif Solmaz...", "output_text": "<!DOCTYPE html><html lang='tr'><head>...</head><body>...</body></html>"}
{"input_text": "HASTA BİLGİLERİ: Adı Soyadı: Mehmet Kaya, T.C. Kimlik No: 98765432109... --- ŞİKAYETLER: Kuru öksürük, boğaz ağrısı... --- DOKTOR: Dr. Ahmet Çetin...", "output_text": "<!DOCTYPE html><html lang='tr'><head>...</head><body>...</body></html>"}

```

  - 3. Running the Fine-Tuning Process
We use a sophisticated Python script (advanced_finetune.py) to manage the training process. This script handles everything from uploading the data to launching and monitoring the training job on Google's infrastructure.

How to run it:
```bash

python advanced_finetune.py \
    --data_file "data/egitim_verisi.jsonl" \
    --model_id "docmed-report-generator-v1" \
    --display_name "Docmed Report Generator v1" \
    --epochs 15

```

  - 4. Monitoring Model Performance
During training, we track the model's "loss" value across each "epoch" (a full pass through the training data). A lower loss value means a more accurate model. The graph below illustrates an ideal training session, showing that the model gets progressively better at its task without simply memorizing the data.

Training Loss (Blue): The model's error on the data it's learning from. Its consistent decrease is a good sign.

Validation Loss (Green): The model's error on new, unseen data. Its decrease shows the model is genuinely learning and can generalize.

<img width="1600" height="1025" alt="unnamed" src="https://github.com/user-attachments/assets/9b9aa0ea-1eea-4d97-87cd-9e267e86e333" />
<img width="512" height="512" alt="unnamed" src="https://github.com/user-attachments/assets/ac464d27-5bae-4ea9-9424-79ac0fa153cc" />
<img width="1044" height="549" alt="image" src="https://github.com/user-attachments/assets/ee30a9ea-9002-422e-9617-be120effe4f2" />


## Team Members


|       | Collaborators             | Roles           | Socials                                                                                         | GitHub                                                                                           |
|-------|----------------------------|------------------|------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------|
| <img src="https://lh3.googleusercontent.com/a/ACg8ocJ4CyEWbr63AMTA-ioGNBeAEC-46ppEm7d7O32ce5RYKwVK4j8SqA=s432-c-no" width="100" height="100"> | Melih Emin Kılıçoğlu | Product Owner & Developer    | [<img src="https://raw.githubusercontent.com/Melihemin/GeVmini/main/assets/profile_image/linkedin.png" width="100" height="100">](https://www.linkedin.com/in/melihemin/) | [<img src="https://raw.githubusercontent.com/Melihemin/GeVmini/main/assets/profile_image/github.png" width="100" height="100">](https://github.com/Melihemin) |
| <img src="https://github.com/Melihemin/OptiMend-AI/blob/main/team_information/iclal_aca.jpg" width="100" height="100"> | İclal Aca | Developer & Scrum Master   | [<img src="https://raw.githubusercontent.com/Melihemin/GeVmini/main/assets/profile_image/linkedin.png" width="100" height="100">](https://www.linkedin.com/in/iclal-aca/	) | [<img src="https://raw.githubusercontent.com/Melihemin/GeVmini/main/assets/profile_image/github.png" width="100" height="100">](https://github.com/iclalaca) |
| <img src="https://github.com/Melihemin/OptiMend-AI/blob/main/team_information/hatice_sanli.jpg" width="100" height="100"> | Hatice Şanlı  | Developer & Scrum Master | [<img src="https://raw.githubusercontent.com/Melihemin/GeVmini/main/assets/profile_image/linkedin.png" width="100" height="100">](https://github.com/Melihemin/OptiMend-AI/blob/main/team_information/hatice_sanli.jpg) | [<img src="https://raw.githubusercontent.com/Melihemin/GeVmini/main/assets/profile_image/github.png" width="100" height="100">](https://www.linkedin.com/in/hatice-%C5%9Fanl%C4%B1-539066266/) |
| <img src="https://github.com/Melihemin/OptiMend-AI/blob/main/team_information/nergiz_alici.jpg" width="100" height="100"> | Nergiz Alıcı  | Developer & Scrum Master| [<img src="https://raw.githubusercontent.com/Melihemin/GeVmini/main/assets/profile_image/linkedin.png" width="100" height="100">](https://www.linkedin.com/in/nergiz-al%C4%B1ci/) | [<img src="https://raw.githubusercontent.com/Melihemin/GeVmini/main/assets/profile_image/github.png" width="100" height="100">](https://github.com/nergizal) |


  
# SPRINT 1 

### Sprint Notes

•	The project vision was clarified as an AI-powered triage and patient assessment solution aimed at reducing emergency room overcrowding.  
•	Design research was conducted using Figma, Canva, and analyses of healthcare-specific UI/UX patterns.  
•	The foundational infrastructure for task tracking (Trello), daily team communication (WhatsApp), and weekly meetings (Google Meet) was established.  
•	Initial AI experiments were launched for NLP-based sentence processing and prompt design, and preliminary outputs were achieved.  
•	For patients: the first versions of the symptom entry screens and user flow were prepared; for medical students and educators: initial versions of rare case analysis and evaluation screens were developed.  

### Estimated score to be completed within the sprint

100 points  

### Score completion logic

The project was planned as 3 sprints and it was anticipated to reach a total of approximately 300 points of work. Priority tasks such as basic system components such as patient interface, symptom processing, and artificial intelligence-based first output production were planned in  
Tasks were evaluated in the range of 5–13 points according to their difficulty level and organized in lists such as “Tasks”, “Frontend Backlogs”, “File Goals” on the Trello board.

### Daily Scrum

Daily Scrum meetings were conducted in writing via the WhatsApp group due to time constraints. The team shared important decisions and developments here instantly. Weekly online meetings were held via Google Meet, task sharing, design reviews and AI trials were conducted in coordination.

Chat History Links: https://github.com/Melihemin/OptiMend-AI/tree/main/Daily%20Scrum

### Sprint Board

![](https://github.com/Melihemin/OptiMend-AI/blob/main/Daily%20Scrum/WhatsApp%20Image%202025-07-07%20at%2022.00.10_17b2890c.jpg)


Tasks: Main work items (symptom input, AI output, recommendation system, etc.)  
File Goals: Model goals, technical task descriptions  
Frontend Backlogs: UI tasks separated by user types  
Required Documents: Design templates, meeting notes, training content  
1. Sprint – 3. Sprint: Areas where tasks will be distributed based on sprint  
 

### Sprint 1 – Completed Tasks

•	The project idea was solidified based on the goal of reducing emergency room congestion through an AI-powered triage and patient evaluation system.  
•	Design research was conducted, including analysis of existing medical interfaces using tools like Figma, Canva, and healthcare-related UI/UX patterns.  
•	Project management infrastructure was set up, with Trello used for task tracking, a WhatsApp group for daily communication, and Google Meet scheduled for team meetings.  
•	Initial experimentation with the AI model began, focusing on NLP-based sentence processing, prompt design trials, and testing early outputs of the model.  
•	The patient interface was designed, including screens for symptom input and user flow, enabling patients to describe their condition in natural language.  
•	The educator interface was also initiated, starting with the layout and logic for rare case analysis and student response functionality.  

### Sprint Review

•	Idea validation  
•	UI and user scenario creation  
•	First versions of patient and trainer screens  
•	Testing sample scenarios for model tests  
•	Clarification of project team processes  

**Notes:**  
Doctor panel and database integration were transferred to Sprint 2.  
Prompt tests were planned but not fully implemented.  

### Sprint Retrospective

**What's Going Well:**  
•	Team communication was successful (WhatsApp + Google Meet)  
•	Design and idea generation was very efficient  
•	Tasks were well organized via Trello  

**Improvement Required:**  
•	AI side tests should be measured with more concrete metrics  
•	Frontend tasks should be divided into smaller steps  

## Tool Used

Trello	Task tracking and sprint planning  
Figma	UI design and wireframe prototyping  
Canva	Visual research and layout inspiration  
WhatsApp	Daily team communication  
Google Meet	Weekly team meetings and discussion sessions  
Python + NLP	AI model experimentation and symptom processing  

## User Stories

### Patient Stories

•	As a patient, I want to enter my symptoms in my own words so that the system can understand me easily.  
•	As a patient, I want to receive an AI-generated report that tells me how urgent my condition is.  
•	As a patient, I want my report to be sent directly to a doctor so that I can get help without delays.  

### Doctor Stories

•	As a doctor, I want to see a list of incoming patient reports so I can prioritize my workflow.  
•	As a doctor, I want to view the patient’s AI-generated report in detail so I can make an informed decision.  
•	As a doctor, I want to add my own notes and diagnosis to each case and mark their treatment status.  

### Student & Educator Stories

•	As a medical student, I want to analyze rare cases and submit my own diagnosis so I can practice clinical thinking.  
•	As an educator, I want to see how students evaluate rare cases so I can track their learning progress  
•	As a student, I want to receive AI feedback on my answers so I can understand my mistakes and improve.  

## Product Backlogs

### Patient Module

•	Design and develop the login/registration page  
•	Create personal information entry form  
•	Implement symptom input interface (free-text area)  
•	Build AI processing pipeline for symptom interpretation  
•	Generate triage report (green/yellow/red classification)  
•	Enable doctor report submission button  

### Doctor Module

•	Create doctor login page  
•	Develop patient report list dashboard  
•	Display patient name, triage color, and submission time  
•	Implement detailed report view  
•	Add editable doctor notes section  
•	Build "Referred / On Hold / Treated" action buttons  
•	Add search & filter functionality (by color or date)  

### Student & Educator Module

•	Build rare case listing page  
•	Add “View Case” and “Submit Diagnosis” UI  
•	Connect student input to AI for automated evaluation  
•	Create AI-based scoring/feedback system  
•	Develop educator dashboard to monitor student performance  

### AI & Backend

•	Train NLP model for converting layman symptom input into medical terms  
•	Design prompt structures for AI diagnosis and triage output  
•	Integrate AI model into frontend via API  
•	Set up database to store patients, reports, and student responses  
•	Conduct prompt testing and optimization (30–40 prompt variants)  

# SPRINT 2 

### Sprint Notes

•	The patient page was updated to improve user flow and interface clarity.

•	Page routing and navigation logic was implemented to enable smooth transitions between patient, doctor, and student interfaces.

•	FastAPI was successfully integrated for backend communication and API handling.

• A comparative analysis of AI models was conducted to evaluate performance and suitability for symptom interpretation.

•	Personalized interface enhancements were implemented based on user type (patient, doctor, student).

•	Initial work has begun on the database setup, including planning of data structure and schema design.

•	A team member, Hatice, left the project. İclal took over organizational coordination responsibilities and now serves as the Scrum Master.

### Sprint Board

<img width="1144" height="802" alt="Ekran Resmi 2025-07-20 17 37 25" src="https://github.com/user-attachments/assets/409dc094-fec3-49e7-9733-1bdcc99a8b27" />


• Patient page design improvements

• Page routing and navigation logic implemented

• FastAPI backend integration

• Research and comparison of AI model candidates

• Personalized user experience enhancements in UI


### Sprint Review

•	FastAPI integration enabled real-time interaction between the frontend and backend.

•	UI modifications allowed better role-based personalization.

•	Page routing logic was tested and confirmed to work correctly across modules.

•	AI model comparisons informed the final selection to be implemented in the next sprint.

•	The updated team structure increased clarity in responsibilities and planning.

### Estimated score to be completed within the sprint

100 points

### Score Completion Logic

Although task points were not explicitly labeled on the Trello board, the estimated workload for this sprint was evaluated to be around 100 points based on the scope and difficulty of the completed tasks. The estimation was made using general effort and time spent on each task such as FastAPI integration, UI improvements, and routing logic. Tasks were organized via Trello lists including “Tasks”, “Frontend Backlogs”, and “File Goals”.


### App Screenshots

<img width="1512" height="811" alt="Ekran Resmi 2025-07-20 18 02 46" src="https://github.com/user-attachments/assets/ed81caf1-23a6-4a6b-b057-21355e1ed073" />
<img width="1512" height="805" alt="Ekran Resmi 2025-07-20 18 03 04" src="https://github.com/user-attachments/assets/e4d37b07-7bcb-4dcf-b84d-842b80ac9f26" />
<img width="1512" height="856" alt="Ekran Resmi 2025-07-20 17 54 33" src="https://github.com/user-attachments/assets/bd82abad-cb13-40b5-a93d-93efd8cf91fe" />
<img width="1512" height="856" alt="Ekran Resmi 2025-07-20 17 56 00" src="https://github.com/user-attachments/assets/ada30c38-8d1e-47c3-9ac2-2abdcfacfe98" />





### Daily Scrum

Daily Scrum meetings were conducted in writing via the WhatsApp group due to time constraints. The team shared important decisions and developments here instantly. Weekly online meetings were held via Google Meet, task sharing, design reviews and AI trials were conducted in coordination.

Chat History Link: https://github.com/Melihemin/OptiMend-AI/tree/main/Daily%20Scrum

### Sprint Retrospective

**What's Going Well:**

•	Clear division of tasks and increased productivity with FastAPI integration

•	Smooth redistribution of responsibilities after the team change

•	Interface and routing improvements enhanced overall user experience

**Needs Improvement:**

•	Model integration needs to be prioritized and finalized in Sprint 3

•	Database structure and testing still pending

## Tools Used

Trello	Task tracking and sprint planning
WhatsApp	Daily team communication
Google Meet	Team meetings
FastAPI	Backend API development and integration
Google Docs	Meeting notes 

### Ready for Sprint 3

•	Finalize AI model integration

•	Implement database and begin storing patient data

•	Conduct system-wide testing and error handling

•	Continue frontend feature development and UI refinements

# SPRINT 3

## Sprint Notes
The AI model was fully integrated and rigorously tested with real-life patient symptom scenarios.
Prompt testing and refinement improved the AI’s ability to provide accurate, medically coherent responses.
Backend performance optimizations and error handling were implemented for a smoother experience.
The web project UI was finalized with detailed project information pages (purpose, workflow, user roles).
A modern system architecture diagram was created and digitized for clarity and documentation.
Doctor interface gained triage-based filtering (green, yellow, red prioritization).
Student module prototype was added, showcasing rare cases for medical education.
Database integration is now complete, with real patient data being stored and retrieved.
Technical documentation and handover materials were completed to ensure long-term maintainability.

## Sprint Board – Completed Tasks

•	AI model integration and testing

•	Prompt improvements and accuracy tuning

•	Backend performance and bug fixes

•	Web UI completion and responsive design

•	Digital system architecture diagram

•	Student (Education) module prototype

•	Doctor triage-based filtering

•	Database activation and testing

•	Completion of technical documentation

![PHOTO-2025-07-31-00-53-37](https://github.com/user-attachments/assets/0daff16f-70e0-40f6-b302-b0b4e3330fb3)
![PHOTO-2025-07-31-00-50-12](https://github.com/user-attachments/assets/d23315eb-c06e-4b26-b65e-6da5c349e719)
![PHOTO-2025-07-31-00-52-06](https://github.com/user-attachments/assets/5c283076-85c9-4105-966c-16ac373f147c)
![PHOTO-2025-07-31-00-52-17](https://github.com/user-attachments/assets/cf00b64d-91f9-4ebc-9ea9-97fd67bf24b1)


## Sprint Review

•	AI model performance improved through extensive testing and prompt refinement.

•	Web platform now includes finalized user interfaces and project details for all roles (Patient, Doctor, Student).

•	Digital system architecture flowchart serves as a central reference for all future documentation.

•	Educational features for medical students (rare case library) were successfully introduced.

•	The system is stable and ready for demonstration or deployment.

## Sprint Score – Points System

•	Each sprint was estimated at 100 points based on task scope and complexity.

•	Sprint 1 (100 pts), Sprint 2 (100 pts), and Sprint 3 (100 pts) have all been fully completed, bringing the total to 300 points.

•	This points system was used to measure workload and ensure balanced progress across all phases.

•	Sprint 3 focused on finalizing AI integration, UI polish, and documentation, accounting for its 100-point allocation.

## App & System Visuals

•	AI test outputs

•	Doctor interface with triage filtering

•	Rare case section (Student module)

•	Finalized web project pages with descriptions

•	Digital system architecture diagram

<img width="1512" height="858" alt="Ekran Resmi 2025-07-31 19 33 17" src="https://github.com/user-attachments/assets/3e43b667-a379-4eaa-afcb-301e3239ddcf" />
<img width="1512" height="858" alt="Ekran Resmi 2025-07-31 19 33 25" src="https://github.com/user-attachments/assets/deea0b36-e439-4f37-aa74-4187785854b7" />
<img width="1512" height="858" alt="Ekran Resmi 2025-07-31 19 33 31" src="https://github.com/user-attachments/assets/d4aee585-71f9-4adb-96d3-eb76ad660578" />
<img width="1512" height="858" alt="Ekran Resmi 2025-07-31 19 33 38" src="https://github.com/user-attachments/assets/eff5ec5d-bcb0-4ea0-b710-bb909f5c0f62" />
<img width="1512" height="858" alt="Ekran Resmi 2025-07-31 19 33 44" src="https://github.com/user-attachments/assets/5ca52e02-9aab-40d2-b275-e55caed1300c" />
<img width="1512" height="858" alt="Ekran Resmi 2025-07-31 19 33 52" src="https://github.com/user-attachments/assets/1a3c6e03-5e2c-48a9-aafd-16bb8b904885" />
<img width="1503" height="790" alt="Ekran Resmi 2025-07-31 20 50 59" src="https://github.com/user-attachments/assets/87ea340b-7fda-4033-bc48-3bf6e333beb1" />
<img width="1503" height="790" alt="Ekran Resmi 2025-07-31 20 51 09" src="https://github.com/user-attachments/assets/9f6236cf-bacc-444a-825a-19a39d381fb5" />
<img width="1503" height="790" alt="Ekran Resmi 2025-07-31 20 51 20" src="https://github.com/user-attachments/assets/e31ece2c-9e38-44ce-ac26-5edd3b32f9e3" />
<img width="1503" height="790" alt="Ekran Resmi 2025-07-31 20 51 34" src="https://github.com/user-attachments/assets/7ffd640d-e2bf-4069-ab40-fe8600398a5d" />
<img width="1503" height="790" alt="Ekran Resmi 2025-07-31 20 51 41" src="https://github.com/user-attachments/assets/99c0e275-7080-42f9-8082-8634d8b2c631" />
<img width="1503" height="790" alt="Ekran Resmi 2025-07-31 20 52 15" src="https://github.com/user-attachments/assets/a6c13b45-1e92-40d6-9b5e-dad726850729" />
 
## Daily Scrum

Daily updates were shared via WhatsApp, while weekly Google Meet sessions were conducted for reviews and planning.
AI testing and system improvements were frequently discussed during these meetings.

Chat History Links: https://github.com/Melihemin/Docmed/tree/main/Daily%20Scrum


## Sprint Retrospective – Final Reflections

•	Sprint 3 marked the successful conclusion of the DiagnoAI development journey. During this final phase, the team effectively brought together all core components into a stable, testable, and user-friendly system. The AI model’s performance was significantly improved through well-structured prompt testing and iterative refinement, which enhanced the accuracy and reliability of symptom-to-report translation.

•	On the frontend, thoughtful UI design updates, clear project explanations, and responsive layouts ensured a smoother experience for patients, doctors, and students alike. The introduction of the rare case library in the student module extended the project's value into medical education. On the backend, performance improvements and complete database integration laid the foundation for scalability and long-term maintainability.

•	The digitized system architecture diagram now offers a comprehensive visual reference of the entire platform, supporting documentation, onboarding, and presentations.
Team communication remained strong through WhatsApp updates and weekly Google Meet meetings. Despite remote collaboration, alignment on goals and deliverables was maintained throughout the sprint.

•	In summary, Sprint 3 delivered on all intended objectives, reaching the full 100-point target. Across all three sprints, 300 out of 300 points were completed, marking the project as functionally complete and deployment-ready.

## Areas for Future Work

•	Expand content for the Student module

•	Add advanced error tracking and analytics

•	Plan for multilingual support and more real-world testing

## Tools Used

During the project, various tools were used to streamline communication, development, and documentation. 

•	Trello was utilized for task management and sprint tracking, allowing the team to plan and monitor progress effectively. 

•	Daily communication and quick updates were maintained through WhatsApp, while Google Meet facilitated weekly online team meetings.

•	For backend and AI service development, FastAPI was used, and GitHub served as the platform for version control and collaboration. 

•	Project notes and team decisions were organized using Google Docs.

•	Designs and system flow diagrams were created using Figma and Draw.io, which helped visualize UI elements and architecture. 

•	For data storage and queries, SQLite was employed depending on the testing and deployment needs
