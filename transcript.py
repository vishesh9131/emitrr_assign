DEFAULT="""Physician: Good morning, Ms. Jones. How are you feeling today?
Patient: Good morning, doctor. I'm doing better, but I still have some discomfort now and then.
Physician: I understand you were in a car accident last September. Can you walk me through what happened?
Patient: Yes, it was on September 1st, around 12:30 in the afternoon. I was driving from Cheadle Hulme to Manchester when I had to stop in traffic. Out of nowhere, another car hit me from behind, which pushed my car into the one in front.
Physician: That sounds like a strong impact. Were you wearing your seatbelt?
Patient: Yes, I always do.
Physician: What did you feel immediately after the accident?
Patient: At first, I was just shocked. But then I realized I had hit my head on the steering wheel, and I could feel pain in my neck and back almost right away.
Physician: Did you seek medical attention at that time?
Patient: Yes, I went to Moss Bank Accident and Emergency. They checked me over and said it was a whiplash injury, but they didn't do any X-rays. They just gave me some advice and sent me home.
Physician: How did things progress after that?
Patient: The first four weeks were rough. My neck and back pain were really bad—I had trouble sleeping and had to take painkillers regularly. It started improving after that, but I had to go through ten sessions of physiotherapy to help with the stiffness and discomfort.
Physician: That makes sense. Are you still experiencing pain now?
Patient: It's not constant, but I do get occasional backaches. It's nothing like before, though.
Physician: That's good to hear. Have you noticed any other effects, like anxiety while driving or difficulty concentrating?
Patient: No, nothing like that. I don't feel nervous driving, and I haven't had any emotional issues from the accident.
Physician: And how has this impacted your daily life? Work, hobbies, anything like that?
Patient: I had to take a week off work, but after that, I was back to my usual routine. It hasn't really stopped me from doing anything.
Physician: That's encouraging. Let's go ahead and do a physical examination to check your mobility and any lingering pain.
[Physical Examination Conducted]
Physician: Everything looks good. Your neck and back have a full range of movement, and there's no tenderness or signs of lasting damage. Your muscles and spine seem to be in good condition.
Patient: That's a relief!
Physician: Yes, your recovery so far has been quite positive. Given your progress, I'd expect you to make a full recovery within six months of the accident. There are no signs of long-term damage or degeneration.
Patient: That's great to hear. So, I don't need to worry about this affecting me in the future?
Physician: That's right. I don't foresee any long-term impact on your work or daily life. If anything changes or you experience worsening symptoms, you can always come back for a follow-up. But at this point, you're on track for a full recovery.
Patient: Thank you, doctor. I appreciate it.
Physician: You're very welcome, Ms. Jones. Take care, and don't hesitate to reach out if you need anything."""

CHUNK_A = """Doctor: Good morning, how are you feeling today?
Patient: Not very well, doctor. I've been having chest pain for the past two days.
Doctor: I'm sorry to hear that. Can you describe the pain?
Patient: It's a sharp pain, right in the center of my chest. Sometimes it spreads to my left arm.
Doctor: Does the pain come and go, or is it constant?
Patient: It comes and goes. It's worse when I exert myself.
Doctor: Any shortness of breath or dizziness?
Patient: Yes, I get short of breath when walking up stairs, and I felt dizzy yesterday.
Doctor: Have you had any previous heart problems?
Patient: My father had a heart attack at 60, but I've never had any issues before.
Doctor: I'm going to order an ECG and some blood tests. This could be angina, which is chest pain due to reduced blood flow to the heart.
Patient: Is that serious?
Doctor: It can be, but there are effective treatments. I'm also going to prescribe nitroglycerin tablets for you to take when you feel the chest pain.
Patient: Thank you, doctor.
Doctor: Take it easy for the next few days, and avoid strenuous activity until we get your test results.
"""

CHUNK_B = """Doctor: Good afternoon, what brings you in today?
Patient: Mark Thompson: I've been having stomach pain and constipation for the past four days.
Doctor: I see. Can you describe the pain?
Patient: It's a dull, cramping pain in my lower abdomen. I feel bloated and uncomfortable.
Doctor: How often have you been able to pass stool?
Patient: Only once in the past four days, and it was very hard and difficult to pass.
Doctor: Have you noticed any other symptoms like nausea, vomiting, or blood in the stool?
Patient: No vomiting, but I do feel a bit nauseous. There's no blood.
Doctor: Have you changed your diet recently or been under stress?
Patient: Not really, but I've been eating more fast food and drinking less water.
Doctor: It sounds like you're dealing with constipation, likely due to diet and dehydration. I recommend increasing your fiber intake, drinking plenty of water, and exercising regularly. If needed, I can prescribe a mild laxative.
Patient: How long will it take to improve?
Doctor: If you follow these recommendations, you should feel better within a few days. Let me know if symptoms persist.
Patient: Thank you, doctor.
"""

CHUNK_C = """Doctor: Good morning, what seems to be the problem?
Patient: Priya Sharma: Doctor, I have a persistent cough for the past two weeks.
Doctor: Is it a dry cough, or are you coughing up phlegm?
Patient: It's mostly dry, but sometimes there's a little mucus.
Doctor: Do you have any fever, sore throat, or difficulty breathing?
Patient: No fever, but my throat feels irritated, and I feel tired.
Doctor: Do you have any history of allergies or asthma?
Patient: No, doctor. But I do live in an area with a lot of air pollution.
Doctor: This could be due to allergies or pollution-related irritation. I'll prescribe a cough syrup and an antihistamine. Try to avoid dust and smoke.
Patient: Should I be worried?
Doctor: If symptoms persist beyond another week, we may need to do further tests. For now, take rest and stay hydrated.
Patient: Thank you, doctor.
"""

CHUNK_D = """Doctor: Hello, what brings you here today?
Patient: Have a severe headache and feel very weak since this morning., btw i am Rajesh Kumar
Doctor: I see. Is the headache on one side or all over your head?
Patient: It's all over my head, and I also feel slightly feverish.
Doctor: Have you taken any painkillers?
Patient: I took one paracetamol tablet, but the pain didn't go away.
Doctor: Any nausea, vomiting, or sensitivity to light?
Patient: No vomiting, but I feel dizzy when I stand up.
Doctor: You might be experiencing migraine or dehydration-related headache. I'll prescribe medication and recommend you drink plenty of fluids. If the headache persists, we may need a CT scan.
Patient: Will I be okay?
Doctor: Yes, just follow the medication and rest properly. Avoid loud noises and bright lights for now.
Patient: Thank you, doctor.
"""

CHUNK_E = """Doctor: Good evening, how can I help you?
Patient: Ananya Iyer: Doctor, I've been feeling very fatigued and weak for the past few weeks.
Doctor: Have you been getting enough sleep?
Patient: I sleep about six hours a night, but I wake up feeling exhausted.
Doctor: Any loss of appetite, dizziness, or unusual weight changes?
Patient: I've lost a little weight, and I feel dizzy sometimes.
Doctor: Have you been tested for anemia before?
Patient: No, but my mother had low iron levels before.
Doctor: This could be iron deficiency anemia. I'll recommend a blood test to confirm and prescribe iron supplements.
Patient: Will the supplements help quickly?
Doctor: Yes, but it may take a few weeks to feel fully better. Eating iron-rich foods like spinach and lentils will also help.
Patient: Thank you, doctor.
"""

CHUNK_F = """Doctor: Namaste, what seems to be the issue?
Patient: Suresh Patel: I have been feeling a burning sensation while urinating for the past three days.
Doctor: Have you noticed any changes in urine color or odor?
Patient: Yes, it's darker than usual and has a strong smell.
Doctor: Any fever, chills, or lower back pain?
Patient: No fever, but my lower abdomen feels a bit sore.
Doctor: This sounds like a urinary tract infection (UTI). I'll prescribe antibiotics and recommend drinking plenty of water.
Patient: Will I need any tests?
Doctor: If symptoms don't improve in a few days, we may need to do a urine test to rule out kidney infection.
Patient: Thank you, doctor.
"""

CHUNK_G = """Doctor: Hello, what brings you in today?
Patient: Kavita Mehta: Doctor, I have had knee pain for the past few months.
Doctor: Is it worse while walking or sitting?
Patient: It hurts more when I walk or climb stairs.
Doctor: Have you had any injuries to the knee before?
Patient: No injuries, but I do stand for long hours at work.
Doctor: It could be early arthritis or strain from prolonged standing. I'll prescribe pain relief medication and recommend physiotherapy.
Patient: Will I need an X-ray?
Doctor: If the pain persists despite treatment, we might consider an X-ray or MRI.
Patient: Thank you, doctor.
"""

CHUNK_H = """Doctor: How are you feeling today?
Patient: I had a car accident. My neck and back hurt a lot for four weeks.
Doctor: Did you receive treatment?
Patient: Yes, I had ten physiotherapy sessions, and now I only have occasional back pain.
"""

# New edge case chunks

CHUNK_I = """Doctor: How are you feeling today Vishesh?
Patient: I had a car accident. My neck and back hurt a lot for four weeks.
Doctor: Did you receive treatment?
Patient: Yes, I had ten physiotherapy sessions, and now I only have occasional back pain.
"""

CHUNK_J = """Doctor: Good morning, Mr. O'Brien-Smith. How have you been since your last visit?
Patient: The pain in my lower back has improved, but I still feel some discomfort when bending.
Doctor: Have you been doing the exercises I recommended?
Patient: Yes, every morning as you suggested. They seem to be helping.
Doctor: That's good to hear. Let's continue with the current treatment plan for another two weeks.
"""

CHUNK_K = """Doctor: Hello there! What can I help you with today?
Patient: My name is Sarah Johnson, and I've been experiencing severe migraines for the past month.
Doctor: I'm sorry to hear that, Sarah. How often do these migraines occur?
Patient: Almost daily, and they're affecting my ability to work.
Doctor: Let's run some tests to determine the cause. In the meantime, I'll prescribe something for the pain.
"""

CHUNK_L = """Doctor: Good afternoon. Who am I speaking with today?
Patient: I'm David Williams. I've been having trouble sleeping lately.
Doctor: How long has this been going on, David?
Patient: About three weeks now. I can't fall asleep until 3 or 4 in the morning.
Doctor: Are you experiencing any stress or anxiety that might be contributing to this?
Patient: Yes, I've been under a lot of pressure at work lately.
Doctor: I understand. Let's discuss some sleep hygiene techniques and possibly a short-term medication to help.
"""

CHUNK_M = """Doctor: Next patient please. What seems to be the problem?
Patient: Hi doctor, I'm experiencing shortness of breath when exercising.
Doctor: And your name is?
Patient: Oh sorry, I'm Michael Chen.
Doctor: How long have you been experiencing this, Michael?
Patient: For about two weeks now. It never happened before.
Doctor: Let's check your lungs and heart function to see what might be causing this.
"""

CHUNK_N = """Doctor: Good morning, how can I help you today?
Patient: Good morning. My joints have been really painful lately, especially in the morning.
Doctor: I see. And whom do I have the pleasure of speaking with?
Patient: I'm Elizabeth Taylor, but everyone calls me Liz.
Doctor: Thank you, Liz. How long have you been experiencing these joint pains?
Patient: For about six months, but they've gotten worse in the last few weeks.
Doctor: Based on your symptoms, this could be rheumatoid arthritis. Let's run some tests to confirm.
"""

CHUNK_O = """Doctor: Welcome back! How's our patient doing today?
Patient: Much better, thank you. The antibiotics really helped with my sinus infection.
Doctor: Excellent! Remind me of your name again? I see so many patients.
Patient: It's Robert De Niro.
Doctor: Of course, Mr. De Niro. Any remaining symptoms we should address?
Patient: Just a slight headache occasionally, but nothing like before.
Doctor: That should resolve completely in the next few days. Continue the medication until finished.
"""

CHUNK_P = """Doctor: Hello, please come in. What brings you to the clinic today?
Patient: Hello doctor. I've been having these strange heart palpitations.
Doctor: I see. Before we continue, could you state your full name for our records?
Patient: Yes, I'm Maria Garcia-Rodriguez.
Doctor: Thank you, Ms. Garcia-Rodriguez. When did you first notice these palpitations?
Patient: About two weeks ago. They happen randomly throughout the day.
Doctor: Let's get an ECG done today to check your heart rhythm.
"""

# Three challenging medical conversation chunks

CHUNK_Q = """Doctor: Good morning. What brings you in today?
Patient: At first, I thought it was just normal back pain, but it's been getting worse over the past three months. I'm having trouble sleeping because of it.
Doctor: I see. And your name for our records?
Patient: Oh, I'm Dr. Patel, but I'm the patient today, not the doctor. Anil Patel.
Doctor: Thank you, Dr. Patel. Can you describe the pain in more detail?
Patient: It's a sharp, shooting pain that radiates from my lower back down my left leg. Sometimes there's numbness and tingling in my foot.
Doctor: That sounds like it could be sciatica or a herniated disc. Have you had any injuries or do heavy lifting?
Patient: I lift patients occasionally in my practice, but no specific injury I can recall.
Doctor: I'd like to order an MRI to get a better look at what's happening. In the meantime, I'll prescribe a muscle relaxant and anti-inflammatory medication.
Patient: Is this something that might require surgery?
Doctor: It's too early to tell without the imaging, but many cases respond well to physical therapy and medication. Surgery is typically a last resort.
Patient: That's a relief. When should I expect improvement?
Doctor: With proper treatment, you should notice improvement within 2-3 weeks. If the MRI shows a significant herniation, we might need to consider epidural steroid injections.
Patient: Thank you for your help.
Doctor: You're welcome, Dr. Patel. I'll have my staff schedule that MRI as soon as possible.
"""

CHUNK_R = """Doctor: Hello there. How can I help you today?
Patient: I've been experiencing these recurring headaches for about six weeks now. They're quite severe.
Doctor: I'm sorry to hear that. Could you tell me your name please?
Patient: My name is Serious Lee-Wong.
Doctor: Thank you, Mr. Lee-Wong. Can you describe the headaches in more detail?
Patient: They typically start at the back of my head and move forward. The pain is throbbing and sometimes I see flashing lights before they begin. They last for hours, sometimes up to a day.
Doctor: Do you have any nausea, vomiting, or sensitivity to light during these episodes?
Patient: Yes to all three. I often have to lie down in a dark room until they pass.
Doctor: Have you had any changes in vision, balance problems, or confusion during these headaches?
Patient: No confusion or balance issues, but my vision gets blurry during the worst episodes.
Doctor: Based on your symptoms, this sounds like migraine with aura. I'd like to rule out other possibilities though. Have you had any recent head injuries or changes in medication?
Patient: No injuries, and I'm not on any regular medication.
Doctor: I'm going to order a brain MRI to rule out any structural causes, and I'll prescribe a triptan medication to take when you feel a headache coming on. I also want you to start keeping a headache diary to identify potential triggers.
Patient: Is this something I'll have to deal with long-term?
Doctor: Migraines are often chronic, but with proper management, many people can reduce their frequency and severity significantly. We might also consider preventive medications if they're occurring frequently.
Patient: Thank you, doctor. I appreciate your help.
Doctor: You're welcome, Mr. Lee-Wong. We'll get to the bottom of this.
"""

CHUNK_S = """Doctor: Good afternoon. What seems to be troubling you today?
Patient: I've been having chest discomfort and shortness of breath for the past week.
Doctor: That sounds concerning. Before we continue, may I have your name?
Patient: My name is Angina Pectoris.
Doctor: Thank you, Ms. Pectoris. Can you describe the chest discomfort? Is it pain, pressure, or something else?
Patient: It feels like pressure or squeezing in the center of my chest. It usually happens when I'm walking up stairs or exercising, and goes away when I rest.
Doctor: How long does this discomfort typically last?
Patient: About 5-10 minutes after I stop exerting myself.
Doctor: Do you have any history of heart disease, high blood pressure, diabetes, or high cholesterol?
Patient: My blood pressure has been high at my last few check-ups, and my father had a heart attack at age 55.
Doctor: Given your symptoms and risk factors, I'm concerned about possible coronary artery disease. This pattern of chest discomfort with exertion that resolves with rest is classic for angina pectoris, which is chest pain due to reduced blood flow to the heart muscle.
Patient: That sounds serious. Is that why my parents named me Angina?
Doctor: Your name is quite coincidental given your symptoms. I'd like to perform an ECG right now and then schedule you for a stress test. I'm also going to prescribe nitroglycerin tablets to take if you experience chest discomfort.
Patient: Will I need surgery or something?
Doctor: It's too early to say. If tests confirm coronary artery disease, treatment options range from medication to angioplasty or bypass surgery, depending on the severity. But first, let's confirm the diagnosis.
Patient: Thank you for taking this seriously.
Doctor: Of course, Ms. Pectoris. Heart symptoms always warrant immediate attention. Please make sure to take the nitroglycerin as directed, and if your chest discomfort lasts longer than 15-20 minutes or is accompanied by sweating, nausea, or jaw pain, please go to the emergency room immediately.
"""

CHUNK_T="""Physician: Good morning, Mr. Thompson. I see you've been feeling fatigued and dizzy lately. Can you describe what's been going on?
Patient: Good morning, doctor. Yes, I've been feeling exhausted for months now. Even after a full night's sleep, I wake up tired. I also get dizzy spells, especially when I stand up too fast.
Physician: I see. Have these symptoms been getting worse over time, or have they been about the same?
Patient: I'd say they're slowly getting worse. A few months ago, I was just a little tired, but now I feel like I don't have any energy most of the day.
Physician: Have you noticed any other symptoms? Maybe headaches, blurred vision, palpitations, or weight changes?
Patient: Well… I do get headaches sometimes, but I figured it was just stress. And now that you mention it, I've lost about 5 kilograms in the past two months, but I haven't changed my diet.
Physician: That's something to note. Have you had any fevers, night sweats, or unusual bruising?
Patient: No fever or night sweats. But I did notice a few random bruises on my arms and legs. I assumed I just bumped into things.
Physician: Okay, let's go over your medical history. Do you have any known conditions—diabetes, hypertension, thyroid issues?
Patient: No, none of those. I've always been pretty healthy.
Physician: And any recent illnesses or infections?
Patient: I had a mild flu about two months ago, but nothing serious.
Physician: Do you drink alcohol or smoke?
Patient: I have an occasional drink, maybe once a week. Never smoked.
Physician: That's good. What about your diet—do you get enough iron-rich foods, or have you had any changes in appetite?
Patient: I think I eat fairly well. Though I have been feeling less hungry than usual.
Physician: How about stress levels—anything in your life that could be affecting your sleep or energy?
Patient: Work has been stressful lately, but nothing extreme.
Physician: Understood. Based on your symptoms—fatigue, dizziness, weight loss, and bruising—there are a few possibilities we need to investigate. It could be something as simple as anemia or vitamin deficiencies, but we also need to rule out more serious conditions like diabetes, thyroid issues, or even bone marrow disorders.
Patient: Bone marrow disorders? That sounds serious…
Physician: I don't want to alarm you, but we need to be thorough. Some conditions, like aplastic anemia or leukemia, can cause unexplained fatigue and bruising. But it could also be something far less serious, like low iron levels or chronic fatigue syndrome. That's why we need tests.
Patient: What kind of tests?
Physician: We'll start with a full blood panel, including a complete blood count (CBC), iron levels, vitamin B12, and thyroid function tests. Depending on the results, we may need further testing.
Patient: I see. And what happens if something serious shows up?
Physician: If the blood tests suggest anything concerning, we'll move forward with additional tests like a bone marrow biopsy or imaging scans. But let's not jump ahead. First, we check your blood, and then we go from there.
Patient: Alright, that makes sense.
Physician: I'll have the nurse draw your blood, and we should have results within a few days. Try to take it easy, stay hydrated, and let me know if your symptoms worsen.
Patient: Thanks, doctor. I just hope it's nothing too serious.
Physician: That's completely understandable. We'll figure it out together.
"""
CHUNK_U="""
Physician: Good afternoon. I see you've been experiencing some unusual symptoms. Can you tell me what's been happening?
Patient: Uh… yeah. It's just some random stuff. Nothing serious, probably.
Physician: I understand, but I'd like to get a clear picture. What exactly have you noticed?
Patient: Well… sometimes my muscles twitch. Like, my arms and legs will jerk a little, mostly when I'm sitting still. And lately, my left leg has felt kinda weak.
Physician: I see. When did this start?
Patient: Not sure. A few months ago, maybe? It's hard to say.
Physician: And has it been getting worse?
Patient: Uh… yeah, I guess. The twitches used to be just in my arms, but now they happen all over.
Physician: What about the weakness in your leg? Do you feel it more at certain times, like after walking for a while?
Patient: Sometimes. But other days, it's fine.
Physician: Have you had any other symptoms? Numbness, vision changes, difficulty swallowing?
Patient: No. Well… actually, sometimes I forget words when I'm talking. Like, simple words. But I'm probably just tired.
Physician: That's important to note. Have you noticed any trouble with coordination or balance?
Patient: Maybe? I tripped last week, but that could've been clumsiness.
Physician: Have you had any recent infections, fever, or unusual stress?
Patient: No fever. I mean, work is stressful, but it always is.
Physician: Any family history of neurological diseases?
Patient: Uh… not really.
Physician: Not really? Can you think of any conditions your relatives have had?
Patient: Well, my uncle had something… I don't remember what it was called. Some disease that made him shake a lot. But he was old.
Physician: That's useful information. Have you noticed any changes in your handwriting or fine motor skills?
Patient: Now that you mention it… yeah. Writing feels weird, like my hand doesn't listen to me sometimes.
Physician: Have you seen any other doctors for this?
Patient: Yeah, but they just said it was stress.
Physician: I see. What's your name again?
Patient: Uh… Sam.
Physician: And your last name?
Patient: Sam's fine.
Physician: Alright, Sam. Based on what you're describing—muscle twitching, occasional weakness, memory lapses, and handwriting issues—I'd like to rule out some neurological conditions.
Patient: Like what?
Physician: It could be something as mild as vitamin deficiencies or stress-related muscle spasms. But we also need to consider conditions like ALS, multiple sclerosis (MS), or early-onset Parkinson's disease.
Patient: ALS? That's… serious, right?
Physician: It can be, but it's far too early to jump to conclusions. Many conditions can cause similar symptoms, including things as simple as an electrolyte imbalance or thyroid issues.
Patient: What do we do now?
Physician: I'd like to run a few tests:
	•	Blood tests to check vitamin levels, thyroid function, and markers for autoimmune diseases.
	•	Electromyography (EMG) to examine muscle activity.
	•	MRI scan to check for neurological abnormalities.
Patient: And if the tests show something bad?
Physician: Then we'll figure it out together. The most important thing is getting answers so we can act early if needed.
Patient: …Alright. Let's do the tests.
"""


# labels for each chunk i generte form gpt HAAHAHA!!!
OUT_CHUNK_A = {
    "Patient_Name": None,
    "Symptoms": ["Chest pain", "Pain spreading to left arm", "Shortness of breath", "Dizziness"],
    "Diagnosis": "Possible angina",
    "Treatment": ["ECG ordered", "Blood tests ordered", "Nitroglycerin tablets prescribed"],
    "Current_Status": "Ongoing chest pain for two days",
    "Prognosis": "Potentially serious but treatable"
}

OUT_CHUNK_B = {
    "Patient_Name": "Mark Thompson",
    "Symptoms": ["Stomach pain", "Constipation", "Bloating", "Nausea"],
    "Diagnosis": "Constipation due to diet and dehydration",
    "Treatment": ["Increase fiber intake", "Drink more water", "Exercise regularly", "Possible laxative"],
    "Current_Status": "Ongoing for four days",
    "Prognosis": "Should improve within a few days with treatment"
}

OUT_CHUNK_C = {
    "Patient_Name": "Priya Sharma",
    "Symptoms": ["Persistent cough", "Throat irritation", "Fatigue", "Occasional mucus"],
    "Diagnosis": "Possible allergies or pollution-related irritation",
    "Treatment": ["Cough syrup", "Antihistamine", "Avoid dust and smoke"],
    "Current_Status": "Ongoing for two weeks",
    "Prognosis": "Should improve with treatment, further tests if persists beyond a week"
}

OUT_CHUNK_D = {
    "Patient_Name": "Rajesh Kumar",
    "Symptoms": ["Severe headache", "Weakness", "Slight fever", "Dizziness"],
    "Diagnosis": "Possible migraine or dehydration-related headache",
    "Treatment": ["Medication prescribed", "Increased fluid intake", "Rest"],
    "Current_Status": "Started this morning",
    "Prognosis": "Should improve with treatment, CT scan if persists"
}

OUT_CHUNK_E = {
    "Patient_Name": "Ananya Iyer",
    "Symptoms": ["Fatigue", "Weakness", "Weight loss", "Dizziness"],
    "Diagnosis": "Possible iron deficiency anemia",
    "Treatment": ["Blood test recommended", "Iron supplements prescribed", "Iron-rich diet"],
    "Current_Status": "Ongoing for a few weeks",
    "Prognosis": "Should improve within a few weeks with treatment"
}

OUT_CHUNK_F = {
    "Patient_Name": "Suresh Patel",
    "Symptoms": ["Burning sensation while urinating", "Dark urine", "Strong urine odor", "Lower abdominal soreness"],
    "Diagnosis": "Urinary tract infection (UTI)",
    "Treatment": ["Antibiotics prescribed", "Increased water intake"],
    "Current_Status": "Ongoing for three days",
    "Prognosis": "Should improve with antibiotics, further tests if no improvement"
}

OUT_CHUNK_G = {
    "Patient_Name": "Kavita Mehta",
    "Symptoms": ["Knee pain", "Pain worse when walking or climbing stairs"],
    "Diagnosis": "Possible early arthritis or strain from prolonged standing",
    "Treatment": ["Pain relief medication", "Physiotherapy recommended"],
    "Current_Status": "Ongoing for a few months",
    "Prognosis": "X-ray or MRI if pain persists despite treatment"
}

OUT_CHUNK_H = {
    "Patient_Name": None,
    "Symptoms": ["Neck pain", "Back pain"],
    "Diagnosis": None,
    "Treatment": ["Physiotherapy (completed ten sessions)"],
    "Current_Status": "Improved, occasional back pain only",
    "Prognosis": None
}

OUT_CHUNK_I = {
    "Patient_Name": "Vishesh",
    "Symptoms": ["Neck pain", "Back pain"],
    "Diagnosis": None,
    "Treatment": ["Physiotherapy (completed ten sessions)"],
    "Current_Status": "Improved, occasional back pain only",
    "Prognosis": None
}

OUT_CHUNK_J = {
    "Patient_Name": "O'Brien-Smith",
    "Symptoms": ["Lower back pain", "Discomfort when bending"],
    "Diagnosis": None,
    "Treatment": ["Exercise regimen", "Continuation of current treatment plan"],
    "Current_Status": "Improving",
    "Prognosis": "Expected continued improvement with treatment"
}

OUT_CHUNK_K = {
    "Patient_Name": "Sarah Johnson",
    "Symptoms": ["Severe migraines"],
    "Diagnosis": "Pending tests",
    "Treatment": ["Tests to be run", "Pain medication prescribed"],
    "Current_Status": "Ongoing for past month, occurring daily",
    "Prognosis": "Affecting ability to work, requires further investigation"
}

OUT_CHUNK_L = {
    "Patient_Name": "David Williams",
    "Symptoms": ["Insomnia", "Difficulty falling asleep"],
    "Diagnosis": "Possible stress-induced insomnia",
    "Treatment": ["Sleep hygiene techniques", "Possible short-term medication"],
    "Current_Status": "Ongoing for three weeks",
    "Prognosis": "Likely related to work pressure"
}

OUT_CHUNK_M = {
    "Patient_Name": "Michael Chen",
    "Symptoms": ["Shortness of breath during exercise"],
    "Diagnosis": "Pending examination",
    "Treatment": ["Lung and heart function tests planned"],
    "Current_Status": "Ongoing for two weeks",
    "Prognosis": "New symptom requiring investigation"
}

OUT_CHUNK_N = {
    "Patient_Name": "Elizabeth Taylor (Liz)",
    "Symptoms": ["Joint pain", "Pain worse in the morning"],
    "Diagnosis": "Possible rheumatoid arthritis",
    "Treatment": ["Tests to confirm diagnosis"],
    "Current_Status": "Ongoing for six months, worsening in recent weeks",
    "Prognosis": "Requires confirmation through testing"
}

OUT_CHUNK_O = {
    "Patient_Name": "Robert De Niro",
    "Symptoms": ["Slight occasional headache", "Previous sinus infection"],
    "Diagnosis": "Recovering sinus infection",
    "Treatment": ["Continue antibiotics until finished"],
    "Current_Status": "Improving, mostly recovered",
    "Prognosis": "Complete resolution expected within days"
}

OUT_CHUNK_P = {
    "Patient_Name": "Maria Garcia-Rodriguez",
    "Symptoms": ["Heart palpitations"],
    "Diagnosis": "Pending ECG",
    "Treatment": ["ECG planned"],
    "Current_Status": "Ongoing for two weeks, occurring randomly throughout the day",
    "Prognosis": "Requires investigation"
}

OUT_CHUNK_Q = {
    "Patient_Name": "Anil Patel",
    "Symptoms": ["Lower back pain", "Sharp shooting pain radiating down left leg", "Numbness and tingling in foot", "Difficulty sleeping"],
    "Diagnosis": "Possible sciatica or herniated disc",
    "Treatment": ["MRI ordered", "Muscle relaxant prescribed", "Anti-inflammatory medication prescribed"],
    "Current_Status": "Worsening over past three months",
    "Prognosis": "Expected improvement within 2-3 weeks with treatment, possible epidural steroid injections if significant herniation"
}

OUT_CHUNK_R = {
    "Patient_Name": "Serious Lee-Wong",
    "Symptoms": ["Recurring headaches", "Throbbing pain", "Flashing lights", "Nausea", "Vomiting", "Light sensitivity", "Blurry vision"],
    "Diagnosis": "Likely migraine with aura",
    "Treatment": ["Brain MRI ordered", "Triptan medication prescribed", "Headache diary recommended"],
    "Current_Status": "Ongoing for six weeks, lasting hours to a day",
    "Prognosis": "Likely chronic but manageable with proper treatment"
}

OUT_CHUNK_S = {
    "Patient_Name": "Angina Pectoris",
    "Symptoms": ["Chest discomfort", "Pressure/squeezing in chest", "Shortness of breath", "Symptoms occur with exertion, resolve with rest"],
    "Diagnosis": "Possible coronary artery disease/angina pectoris",
    "Treatment": ["ECG planned", "Stress test scheduled", "Nitroglycerin tablets prescribed"],
    "Current_Status": "Ongoing for one week",
    "Prognosis": "Potentially serious, treatment options range from medication to surgery depending on severity"
}

OUT_CHUNK_T = {
    "Patient_Name": "Thompson",
    "Symptoms": ["Fatigue", "Dizziness", "Headaches", "Weight loss", "Unusual bruising", "Decreased appetite"],
    "Diagnosis": "Multiple possibilities including anemia, vitamin deficiencies, diabetes, thyroid issues, or bone marrow disorders",
    "Treatment": ["Full blood panel ordered", "CBC, iron levels, vitamin B12, thyroid function tests"],
    "Current_Status": "Worsening over months",
    "Prognosis": "Depends on test results, could range from simple deficiency to more serious conditions"
}

OUT_CHUNK_U = {
    "Patient_Name": "Sam",
    "Symptoms": ["Muscle twitching", "Muscle weakness in left leg", "Word-finding difficulties", "Coordination issues", "Handwriting changes"],
    "Diagnosis": "Possible neurological condition - differential includes vitamin deficiencies, stress-related muscle spasms, ALS, MS, or early-onset Parkinson's",
    "Treatment": ["Blood tests planned", "EMG recommended", "MRI scan ordered"],
    "Current_Status": "Progressing over a few months",
    "Prognosis": "Depends on test results, early intervention important"
}

# Test chunks for name detection evaluation
TEST_CHUNK_A = """Doctor: Good morning, what brings you in today?
Patient: John Smith: I've been experiencing severe lower back pain for the past week.
Doctor: I see. Can you describe the pain in more detail?
Patient: It's a sharp, stabbing pain that gets worse when I bend over or sit for too long.
Doctor: Have you had any injuries or done any strenuous activities recently?
Patient: I helped my friend move some furniture last weekend. I felt fine that day, but woke up in pain the next morning.
Doctor: That could definitely be the cause. Any numbness or tingling in your legs?
Patient: No, just the pain in my lower back.
Doctor: Based on your description, this sounds like a muscle strain. I'll prescribe some anti-inflammatory medication and recommend rest for a few days.
Patient: How long until I feel better?
Doctor: With proper rest and medication, you should start feeling improvement within 3-5 days.
"""

TEST_CHUNK_B = """Doctor: Hello there, how can I help you today?
Patient: I've been having these terrible migraines, doctor.
Doctor: I'm sorry to hear that. Could you tell me your name first?
Patient: Oh, I'm Jennifer Lopez-Garcia.
Doctor: Thank you, Ms. Lopez-Garcia. How long have you been experiencing these migraines?
Patient: For about three months now, and they're getting more frequent.
Doctor: Do you notice any triggers or warning signs before they start?
Patient: Yes, I often see flashing lights and feel nauseous about an hour before the pain starts.
Doctor: That sounds like migraine with aura. I'll prescribe medication and recommend keeping a headache diary.
"""

TEST_CHUNK_C = """Doctor: Next patient please. What seems to be the problem?
Patient: Doctor, my name is James O'Connor and I've been having chest pains.
Doctor: When did these pains start, Mr. O'Connor?
Patient: About two weeks ago. They come and go, mostly when I'm stressed.
Doctor: Do you have any history of heart problems in your family?
Patient: My father had a heart attack at 50, and my grandfather died from one.
Doctor: Given your symptoms and family history, I'd like to run some tests right away.
Patient: Is it serious?
Doctor: We need to rule out any cardiac issues. Let's not take chances with chest pain.
"""

TEST_CHUNK_D = """Doctor: Good afternoon. Who am I speaking with today?
Patient: Good afternoon. My throat has been really sore for days.
Doctor: I'll help you with that. Could you please state your name for our records?
Patient: My name is Kim Lee-Wong.
Doctor: Thank you, Ms. Lee-Wong. How long has your throat been bothering you?
Patient: About five days now. It hurts to swallow and I've had a low fever.
Doctor: Let me take a look... Yes, your throat is quite inflamed. This appears to be strep throat.
Patient: Is that serious?
Doctor: It's a bacterial infection that requires antibiotics. You should feel better within 48 hours of starting treatment.
"""

TEST_CHUNK_E = """Doctor: Hello, what can I do for you today?
Patient: I've been feeling extremely tired lately, no matter how much I sleep.
Doctor: I understand. Before we continue, may I have your name?
Patient: It's Thomas O'Reilly-Johnson.
Doctor: Thank you, Mr. O'Reilly-Johnson. When did this fatigue begin?
Patient: About a month ago. I used to be very active, but now I can barely get through the day.
Doctor: Have you noticed any other symptoms like weight loss or increased thirst?
Patient: Now that you mention it, I have been drinking a lot more water than usual.
Doctor: I'd like to run some blood tests to check for several conditions, including diabetes and thyroid issues.
"""

TEST_CHUNK_F = """Doctor: Good morning, how are you feeling today?
Patient: Not great, doctor. I've had this persistent cough that won't go away.
Doctor: I see. And your name is?
Patient: Abdul al-Farsi.
Doctor: How long have you been coughing, Mr. al-Farsi?
Patient: For about three weeks now. It's worse at night and early morning.
Doctor: Are you coughing up anything?
Patient: Yes, yellowish phlegm, especially in the morning.
Doctor: This sounds like bronchitis. I'll prescribe antibiotics and recommend plenty of fluids and rest.
"""

TEST_CHUNK_G = """Doctor: Next please. What brings you to the clinic today?
Patient: Hello doctor, I'm experiencing severe joint pain in my hands.
Doctor: I see. Could you tell me your name?
Patient: I'm Mary-Kate Williams.
Doctor: Thank you, Ms. Williams. How long have you had this pain?
Patient: For several months, but it's gotten much worse recently. My fingers are stiff and swollen in the mornings.
Doctor: Based on your symptoms, this could be rheumatoid arthritis. We'll need to run some blood tests to confirm.
Patient: Is there a cure?
Doctor: While there's no cure, we have very effective treatments to manage the symptoms and slow progression.
"""

TEST_CHUNK_H = """Doctor: Good afternoon. What seems to be the problem?
Patient: I've been having dizzy spells for the past week.
Doctor: That must be concerning. Could you state your name please?
Patient: Jean-Claude Van Damme.
Doctor: Thank you, Mr. Van Damme. Can you describe these dizzy spells?
Patient: The room seems to spin, and I feel like I might fall. It lasts for about a minute each time.
Doctor: Have you noticed any hearing changes or ringing in your ears?
Patient: Yes, my right ear feels full, and there's a constant ringing.
Doctor: This sounds like vertigo, possibly due to an inner ear issue. Let's run some tests to determine the exact cause.
"""

TEST_CHUNK_I = """Doctor: Hello, how can I help you today?
Patient: Doctor, I've been having trouble sleeping for weeks now.
Doctor: I'm sorry to hear that. What's your name?
Patient: D'Angelo Washington.
Doctor: Mr. Washington, can you tell me more about your sleep issues?
Patient: I lie awake for hours before falling asleep, and then wake up multiple times during the night.
Doctor: Have there been any recent changes or stressors in your life?
Patient: I started a new job with irregular hours about a month ago.
Doctor: Your insomnia is likely related to your disrupted sleep schedule. Let's discuss some sleep hygiene techniques and possibly a short-term sleep aid.
"""

TEST_CHUNK_J = """Doctor: Good morning, who do I have the pleasure of seeing today?
Patient: Good morning. I'm experiencing numbness in my right hand.
Doctor: I see. And your name is?
Patient: Sarah O'Malley-Jenkins.
Doctor: Thank you, Ms. O'Malley-Jenkins. How long have you had this numbness?
Patient: About two weeks. It's mainly in my thumb and first two fingers.
Doctor: That distribution suggests carpal tunnel syndrome. Do you do repetitive hand movements at work?
Patient: Yes, I'm a computer programmer. I type all day.
Doctor: Let's do some tests to confirm, but we'll likely need to discuss ergonomic changes and possibly a wrist brace.
"""

# Corresponding output chunks
TEST_OUT_CHUNK_A = {
    "Patient_Name": "John Smith",
    "Symptoms": ["Severe lower back pain", "Pain worse when bending or sitting"],
    "Diagnosis": "Muscle strain",
    "Treatment": ["Anti-inflammatory medication", "Rest"],
    "Current_Status": "Ongoing for one week",
    "Prognosis": "Expected improvement within 3-5 days with treatment"
}

TEST_OUT_CHUNK_B = {
    "Patient_Name": "Jennifer Lopez-Garcia",
    "Symptoms": ["Migraines", "Flashing lights", "Nausea"],
    "Diagnosis": "Migraine with aura",
    "Treatment": ["Medication prescribed", "Headache diary recommended"],
    "Current_Status": "Ongoing for three months, increasing in frequency",
    "Prognosis": "Manageable with proper treatment"
}

TEST_OUT_CHUNK_C = {
    "Patient_Name": "James O'Connor",
    "Symptoms": ["Chest pains", "Pain associated with stress"],
    "Diagnosis": "Pending tests",
    "Treatment": ["Tests ordered"],
    "Current_Status": "Ongoing for two weeks, intermittent",
    "Prognosis": "Requires investigation due to family history"
}

TEST_OUT_CHUNK_D = {
    "Patient_Name": "Kim Lee-Wong",
    "Symptoms": ["Sore throat", "Pain when swallowing", "Low fever"],
    "Diagnosis": "Strep throat",
    "Treatment": ["Antibiotics prescribed"],
    "Current_Status": "Ongoing for five days",
    "Prognosis": "Expected improvement within 48 hours of treatment"
}

TEST_OUT_CHUNK_E = {
    "Patient_Name": "Thomas O'Reilly-Johnson",
    "Symptoms": ["Extreme fatigue", "Increased thirst"],
    "Diagnosis": "Pending blood tests",
    "Treatment": ["Blood tests ordered"],
    "Current_Status": "Ongoing for one month",
    "Prognosis": "Depends on test results"
}

TEST_OUT_CHUNK_F = {
    "Patient_Name": "Abdul al-Farsi",
    "Symptoms": ["Persistent cough", "Worse at night and morning", "Yellow phlegm"],
    "Diagnosis": "Bronchitis",
    "Treatment": ["Antibiotics prescribed", "Increased fluid intake", "Rest"],
    "Current_Status": "Ongoing for three weeks",
    "Prognosis": "Expected improvement with treatment"
}

TEST_OUT_CHUNK_G = {
    "Patient_Name": "Mary-Kate Williams",
    "Symptoms": ["Severe joint pain in hands", "Morning stiffness", "Swollen fingers"],
    "Diagnosis": "Possible rheumatoid arthritis",
    "Treatment": ["Blood tests ordered"],
    "Current_Status": "Ongoing for several months, worsening",
    "Prognosis": "Manageable with treatment if confirmed"
}

TEST_OUT_CHUNK_H = {
    "Patient_Name": "Jean-Claude Van Damme",
    "Symptoms": ["Dizzy spells", "Room spinning sensation", "Ear fullness", "Ringing in ears"],
    "Diagnosis": "Possible vertigo due to inner ear issue",
    "Treatment": ["Tests ordered"],
    "Current_Status": "Ongoing for one week",
    "Prognosis": "Depends on underlying cause"
}

TEST_OUT_CHUNK_I = {
    "Patient_Name": "D'Angelo Washington",
    "Symptoms": ["Insomnia", "Difficulty falling asleep", "Multiple night awakenings"],
    "Diagnosis": "Insomnia related to disrupted sleep schedule",
    "Treatment": ["Sleep hygiene techniques", "Possible short-term sleep aid"],
    "Current_Status": "Ongoing for weeks",
    "Prognosis": "Likely to improve with regular sleep schedule"
}

TEST_OUT_CHUNK_J = {
    "Patient_Name": "Sarah O'Malley-Jenkins",
    "Symptoms": ["Numbness in right hand", "Affects thumb and first two fingers"],
    "Diagnosis": "Possible carpal tunnel syndrome",
    "Treatment": ["Tests to confirm", "Ergonomic changes recommended", "Possible wrist brace"],
    "Current_Status": "Ongoing for two weeks",
    "Prognosis": "Manageable with proper ergonomics and treatment"
}

# Additional complex medical conversations with challenging name detection scenarios

CHUNK_V = """
Physician: Good morning. What brings you in today?
Patient: I've been having these terrible headaches for about three weeks now.
Physician: I'm sorry to hear that. Can you describe the headaches?
Patient: They're mostly on one side, and sometimes I see flashing lights before they start.
Physician: That sounds like it could be migraines. Have you had migraines before?
Patient: No, this is new for me. I'm worried because my mother had a brain aneurysm.
Physician: I understand your concern. Let's get some information first. Your name?
Patient: Oh, I'm just J.D.
Physician: Is that your full name or initials?
Patient: Just call me J.D. That's what everyone calls me.
Physician: I need your legal name for our records.
Patient: Fine. John Dorian. But I prefer J.D.
Physician: Thank you, Mr. Dorian. I'll note your preference for J.D. in your chart. Now, have you tried any medications for these headaches?
Patient: Just over-the-counter stuff. Doesn't really help much.
Physician: I'd like to order an MRI to rule out any structural issues, given your family history. I'll also prescribe a triptan medication specifically for migraines.
Patient: Will the MRI show if I have what my mother had?
Physician: Yes, it would detect an aneurysm if present. But let's not jump to conclusions. Migraines are much more common.
Patient: Okay. I'm just worried, you know?
Physician: That's completely understandable, J.D. We'll get to the bottom of this.
"""

OUT_CHUNK_V = {
    "Patient_Name": "John Dorian (J.D.)",
    "Symptoms": ["Headaches on one side", "Flashing lights", "Headaches lasting three weeks"],
    "Diagnosis": "Possible migraines",
    "Treatment": ["MRI ordered", "Triptan medication prescribed"],
    "Current_Status": "Ongoing for three weeks, not responding to OTC medication",
    "Prognosis": "Requires investigation due to family history of aneurysm"
}

CHUNK_W = """
Physician: Hello there. How can I help you today?
Patient: I've been having chest pain and shortness of breath.
Physician: That's concerning. How long has this been happening?
Patient: About a week. It's worse when I exert myself.
Physician: Do you have any history of heart problems?
Patient: No, but my father had a heart attack at 50.
Physician: I see. And you are?
Patient: van der Woodsen.
Physician: Your first name?
Patient: Serena.
Physician: Thank you, Ms. van der Woodsen. Is there any pain radiation to your jaw or left arm?
Patient: Sometimes to my left arm, yes.
Physician: Given your symptoms and family history, I'd like to do an ECG right away and some blood tests. We need to rule out a cardiac issue.
Patient: Is it serious?
Physician: It could be, which is why we need to investigate promptly. I'm also going to prescribe nitroglycerin tablets to take if you experience chest pain.
Patient: Okay, that sounds scary.
Physician: Try not to worry too much, Ms. van der Woodsen. We'll get answers soon. If your chest pain becomes severe or lasts more than 15 minutes, please go to the emergency room immediately.
"""

OUT_CHUNK_W = {
    "Patient_Name": "Serena van der Woodsen",
    "Symptoms": ["Chest pain", "Shortness of breath", "Pain radiation to left arm", "Symptoms worse with exertion"],
    "Diagnosis": "Possible cardiac issue",
    "Treatment": ["ECG ordered", "Blood tests ordered", "Nitroglycerin tablets prescribed"],
    "Current_Status": "Ongoing for one week",
    "Prognosis": "Potentially serious, requires immediate investigation"
}

CHUNK_X = """
Physician: Good afternoon. What seems to be the problem?
Patient: I've been feeling really tired lately, and I've lost weight without trying.
Physician: How long has this been going on?
Patient: About two months. I've lost almost 10 kilograms.
Physician: That's significant. Any other symptoms?
Patient: I'm thirsty all the time, and I'm urinating frequently, especially at night.
Physician: I see. Before we continue, could I get your name please?
Patient: It's O'Malley-Smith. First name George.
Physician: Thank you, Mr. O'Malley-Smith. Have you been monitoring your blood sugar levels?
Patient: No, should I be?
Physician: The symptoms you're describing are classic for diabetes. I'd like to check your blood sugar right now and order some additional tests.
Patient: Diabetes? Really? No one in my family has that.
Physician: It can develop without family history. Let's not jump to conclusions until we have the test results, but we should investigate this possibility.
Patient: What would treatment involve if it is diabetes?
Physician: It depends on the type and severity, but it could include dietary changes, exercise, and possibly medication or insulin. The good news is that diabetes can be managed effectively.
Patient: I see. Well, let's find out then.
"""

OUT_CHUNK_X = {
    "Patient_Name": "George O'Malley-Smith",
    "Symptoms": ["Fatigue", "Unintentional weight loss (10kg)", "Excessive thirst", "Frequent urination", "Nocturia"],
    "Diagnosis": "Possible diabetes mellitus",
    "Treatment": ["Blood glucose test", "Additional laboratory tests ordered"],
    "Current_Status": "Ongoing for two months, progressive weight loss",
    "Prognosis": "Likely manageable with proper treatment if confirmed"
}

CHUNK_Y = """
Physician: Hello, how are you feeling today?
Patient: Not great. I've been having joint pain in my hands and feet.
Physician: I'm sorry to hear that. When did this start?
Patient: About six months ago, but it's gotten worse recently. The joints are swollen and stiff, especially in the morning.
Physician: Are you experiencing fatigue as well?
Patient: Yes, I'm exhausted all the time.
Physician: I'll need to run some tests. Could you tell me your name?
Patient: Dr. Torres.
Physician: Your first name as well, please?
Patient: Callie. Dr. Callie Torres. I'm an orthopedic surgeon at Seattle Grace.
Physician: I see, Dr. Torres. As a medical professional, you probably have some thoughts about your symptoms?
Patient: I'm concerned about rheumatoid arthritis. The symmetric joint involvement, morning stiffness, fatigue... it fits.
Physician: I agree that's a possibility. I'd like to order rheumatoid factor, anti-CCP antibodies, ESR, and CRP tests. We should also get X-rays of your hands and feet.
Patient: I'd appreciate that. It's affecting my ability to perform surgeries.
Physician: I understand how concerning that must be. If it is RA, there are effective treatments available now that can help prevent joint damage and maintain function.
Patient: Thank you. I just need to know what I'm dealing with.
"""

OUT_CHUNK_Y = {
    "Patient_Name": "Dr. Callie Torres",
    "Symptoms": ["Joint pain in hands and feet", "Joint swelling", "Morning stiffness", "Fatigue", "Symmetric joint involvement"],
    "Diagnosis": "Possible rheumatoid arthritis",
    "Treatment": ["Rheumatoid factor test", "Anti-CCP antibodies test", "ESR and CRP tests", "X-rays of hands and feet"],
    "Current_Status": "Ongoing for six months, worsening, affecting work ability",
    "Prognosis": "Potentially manageable with early intervention"
}

CHUNK_Z = """
Physician: Good morning. What can I do for you today?
Patient: I've been having trouble sleeping. I lie awake for hours, and when I do sleep, I wake up frequently.
Physician: How long have you been experiencing these sleep issues?
Patient: About three months. It started after I lost my job.
Physician: I see. Are you experiencing any other symptoms like low mood or anxiety?
Patient: Yes, I feel down most of the time, and I've lost interest in things I used to enjoy.
Physician: I understand. Could you tell me your name?
Patient: McSteamy. Mark McSteamy.
Physician: Is that spelled M-c-S-t-e-a-m-y?
Patient: Actually, it's M-c-S-t-e-a-m-y. Scottish heritage.
Physician: Thank you, Mr. McSteamy. Based on what you've described, you may be experiencing depression, which can significantly affect sleep.
Patient: I figured it might be something like that.
Physician: I'd like to do a depression screening assessment and discuss treatment options, which might include therapy, medication, or both.
Patient: I'm open to therapy, but I'm hesitant about medication.
Physician: That's completely understandable. We can start with therapy and see how you respond. Cognitive-behavioral therapy is particularly effective for both depression and insomnia.
Patient: That sounds good. I just want to feel like myself again.
Physician: We'll work on that together, Mr. McSteamy. Recovery is definitely possible.
"""

OUT_CHUNK_Z = {
    "Patient_Name": "Mark McSteamy",
    "Symptoms": ["Insomnia", "Frequent waking", "Low mood", "Anhedonia"],
    "Diagnosis": "Possible depression with insomnia",
    "Treatment": ["Depression screening assessment", "Cognitive-behavioral therapy recommended"],
    "Current_Status": "Ongoing for three months, following job loss",
    "Prognosis": "Good potential for recovery with appropriate treatment"
}

CHUNK_AA = """
Physician: Good afternoon. What brings you in today?
Patient: I've been experiencing recurring abdominal pain and diarrhea.
Physician: I'm sorry to hear that. How long has this been going on?
Patient: On and off for about a year, but it's been worse the past month.
Physician: Do you notice any particular foods that trigger these symptoms?
Patient: Dairy products definitely make it worse. Sometimes wheat too.
Physician: I see. And your name is?
Patient: My name is Grey-Shepherd.
Physician: And your first name?
Patient: Meredith.
Physician: Thank you, Ms. Grey-Shepherd. Based on your symptoms, we should consider conditions like irritable bowel syndrome or possibly celiac disease.
Patient: My mother had ulcerative colitis. Could it be that?
Physician: That's important information. Given your family history, we should definitely rule that out as well. I'd like to order some blood tests and possibly refer you for a colonoscopy.
Patient: Is there anything I can do in the meantime?
Physician: I'd recommend keeping a food diary to identify triggers, and you might want to try eliminating dairy and wheat temporarily to see if that helps.
Patient: Okay, I can do that.
Physician: Great. We'll get to the bottom of this, Ms. Grey-Shepherd.
"""

OUT_CHUNK_AA = {
    "Patient_Name": "Meredith Grey-Shepherd",
    "Symptoms": ["Recurring abdominal pain", "Diarrhea", "Symptoms worsen with dairy and wheat consumption"],
    "Diagnosis": "Possible IBS, celiac disease, or inflammatory bowel disease",
    "Treatment": ["Blood tests ordered", "Possible colonoscopy referral", "Food diary recommended", "Trial elimination diet suggested"],
    "Current_Status": "Ongoing for a year, worsening in past month",
    "Prognosis": "Likely manageable with proper diagnosis and treatment"
}

CHUNK_AB = """
Physician: Hello there. What seems to be the problem today?
Patient: I've been having these dizzy spells. Sometimes the room feels like it's spinning.
Physician: How often do these episodes occur?
Patient: A few times a week. They last for about a minute each time.
Physician: Is there anything that seems to trigger them?
Patient: They often happen when I turn my head quickly or get up from bed.
Physician: I see. Could I have your name please?
Patient: Just put down "House."
Physician: I need your full name for our records.
Patient: Gregory House, M.D. But I prefer to go by House.
Physician: Thank you, Dr. House. Your symptoms sound consistent with benign paroxysmal positional vertigo, or BPPV.
Patient: I suspected as much. Otoliths in the semicircular canals?
Physician: Exactly. I'd like to perform the Dix-Hallpike maneuver to confirm, and if positive, we can try the Epley maneuver right away to reposition the crystals.
Patient: Fine, but I've already tried the Epley maneuver on myself. Didn't help.
Physician: It can be difficult to perform correctly on yourself. Let's try it here, and I can also prescribe an anti-vertigo medication for symptomatic relief.
Patient: Whatever. Let's just get this over with.
"""

OUT_CHUNK_AB = {
    "Patient_Name": "Gregory House, M.D.",
    "Symptoms": ["Dizzy spells", "Vertigo", "Room spinning sensation", "Symptoms triggered by head movement and positional changes"],
    "Diagnosis": "Likely benign paroxysmal positional vertigo (BPPV)",
    "Treatment": ["Dix-Hallpike maneuver for diagnosis", "Epley maneuver", "Anti-vertigo medication"],
    "Current_Status": "Occurring multiple times weekly, lasting about a minute each episode",
    "Prognosis": "Generally good with proper treatment"
}

CHUNK_AC = """
Physician: Good morning. How can I help you today?
Patient: I've been having a persistent cough for over a month now.
Physician: Is it a dry cough or are you coughing up anything?
Patient: It's mostly dry, but sometimes I cough up a small amount of clear mucus.
Physician: Any other symptoms like fever, chest pain, or shortness of breath?
Patient: No fever, but I do get short of breath more easily than usual.
Physician: I see. And your name is?
Patient: de la Cruz.
Physician: Your first name as well, please?
Patient: Cristina de la Cruz.
Physician: Thank you, Ms. de la Cruz. Do you smoke or have you ever smoked?
Patient: I quit about five years ago. I smoked for ten years before that.
Physician: Given your history and symptoms, I'd like to order a chest X-ray and pulmonary function tests. This could be chronic bronchitis, asthma, or another respiratory condition.
Patient: Could it be something more serious?
Physician: We need to rule out more serious conditions, but let's not jump to conclusions before we have the test results.
Patient: Okay. How soon can we do these tests?
Physician: We can schedule the chest X-ray for today, and the pulmonary function tests within the week.
Patient: Thank you, doctor.
"""

OUT_CHUNK_AC = {
    "Patient_Name": "Cristina de la Cruz",
    "Symptoms": ["Persistent cough for over a month", "Occasional clear mucus", "Shortness of breath with exertion"],
    "Diagnosis": "Possible chronic bronchitis, asthma, or other respiratory condition",
    "Treatment": ["Chest X-ray ordered", "Pulmonary function tests ordered"],
    "Current_Status": "Ongoing for over a month",
    "Prognosis": "Requires investigation, likely manageable with proper treatment"
}

CHUNK_AD = """
Physician: Good afternoon. What brings you in today?
Patient: I've been having these strange episodes where I lose awareness for a few seconds.
Physician: Can you describe what happens during these episodes?
Patient: I just kind of blank out. People tell me I stare and sometimes my eyelids flutter.
Physician: How long do these episodes last, and how often do they occur?
Patient: Maybe 10-15 seconds each time. They happen a few times a week now.
Physician: Have you ever lost consciousness completely or had convulsions?
Patient: No, nothing like that.
Physician: I see. Could you tell me your name?
Patient: It's St. Patrick.
Physician: Your full name, please?
Patient: Izzie St. Patrick. That's I-Z-Z-I-E.
Physician: Thank you, Ms. St. Patrick. Based on your description, these episodes sound like they could be absence seizures.
Patient: Seizures? But I thought seizures meant falling down and shaking?
Physician: That's one type of seizure, but there are many different kinds. Absence seizures are brief episodes exactly like what you're describing.
Patient: Is this serious?
Physician: It's something we need to address. I'd like to refer you for an EEG to record your brain activity, and possibly an MRI to rule out any structural causes.
Patient: Will I need medication?
Physician: If the diagnosis is confirmed, then yes, anti-seizure medication is typically very effective for controlling absence seizures.
Patient: I see. Thank you for explaining.
"""

OUT_CHUNK_AD = {
    "Patient_Name": "Izzie St. Patrick",
    "Symptoms": ["Brief loss of awareness", "Staring episodes", "Eyelid fluttering", "Episodes lasting 10-15 seconds"],
    "Diagnosis": "Possible absence seizures",
    "Treatment": ["EEG referral", "Possible MRI", "Potential anti-seizure medication"],
    "Current_Status": "Occurring multiple times weekly",
    "Prognosis": "Typically controllable with appropriate medication"
}

CHUNK_AE = """
Physician: Hello. What can I do for you today?
Patient: I've been having trouble with my memory. I keep forgetting things.
Physician: What kinds of things are you forgetting?
Patient: Recent conversations, where I put things, appointments. Last week I left the stove on all day.
Physician: How long have you noticed these memory problems?
Patient: They've been getting worse over the past year or so.
Physician: I see. And your name is?
Patient: I'm... um... just a moment... I'm sorry, this is embarrassing.
Physician: Take your time.
Patient: Al. Al Z. Heimer. That's my name.
Physician: Mr. Heimer, is there someone who came with you today who can help provide some additional information?
Patient: My daughter is in the waiting room.
Physician: With your permission, I'd like to speak with her as well. Memory issues can have many causes, from stress and medication side effects to neurological conditions.
Patient: Yes, please talk to her. She's been very worried about me.
Physician: I'd like to perform a cognitive assessment today and then order some tests, including blood work and possibly brain imaging.
Patient: Will this get better, doctor?
Physician: That depends on the cause. Some memory issues are reversible, while others can be managed with proper treatment. We'll take this one step at a time.
Patient: Thank you. I'm scared about what's happening to me.
Physician: I understand, Mr. Heimer. We'll work through this together.
"""

OUT_CHUNK_AE = {
    "Patient_Name": "Al Z. Heimer",
    "Symptoms": ["Progressive memory loss", "Forgetting conversations", "Misplacing items", "Forgetting appointments", "Safety concerns (left stove on)"],
    "Diagnosis": "Possible cognitive impairment, multiple potential causes",
    "Treatment": ["Cognitive assessment", "Blood tests ordered", "Possible brain imaging"],
    "Current_Status": "Progressive worsening over approximately one year",
    "Prognosis": "Depends on underlying cause, requires thorough investigation"
}