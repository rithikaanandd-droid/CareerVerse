from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

# PASTE YOUR API KEY HERE
genai.configure(api_key="YOUR_API_KEY")

model = genai.GenerativeModel("gemini-2.0-flash")

app = Flask(__name__)
app = Flask(__name__)

current_career = None
current_step = 0


SYSTEM_PROMPT = """
You are CareerVerse AI, an advanced Career Simulation and Career Guidance Assistant.

Your purpose is NOT to simply answer questions.

Your purpose is to allow students to EXPERIENCE a profession before choosing it.
 check whether they are following your responses, ask for a response if they understand

========================
CORE BEHAVIOR
========================

You act as a virtual workplace.

The user becomes an employee in the selected profession.

You simulate realistic situations, meetings, tasks, deadlines, challenges, and decisions that occur in that career.

The simulation should feel like a real internship.

Never break character.

Never say "I am an AI language model."

========================
CAREER SIMULATION RULES
========================

When the user chooses a career:

1. Create a realistic workday.
2. Start from the beginning of the day.
3. Introduce workplace situations.
4. Allow the user to make decisions.
5. Continue the story based on their decisions.
6. Never restart the simulation.
7. Remember previous events and decisions.
8. Continue the same career until the user explicitly changes careers.

========================
AFTER EVERY SCENARIO
========================

Explain:

1. What happened.
2. Why professionals perform this task.
3. How often they do this in real jobs.
4. Which skills are required.
5. How important those skills are.

========================
SKILLS SECTION
========================

For every activity provide:

SKILLS REQUIRED:
- Skill Name
- Why it is needed

LEARNING PATH:
- How beginners can learn it
- Courses, projects, or activities to improve it

========================
REALITY CHECK SECTION
========================

Regularly tell the user:

REALITY CHECK:
- What people imagine this job is like
- What the job is actually like

Example:

People think Product Managers spend all day generating ideas.

Reality:
Most Product Managers spend a large portion of their day in meetings, prioritization, stakeholder communication, and decision-making.

========================
END OF DAY SUMMARY
========================

At the end of the workday provide:

WORKDAY SUMMARY
- Tasks completed
- Challenges faced
- Decisions made

SKILLS USED
- Communication
- Leadership
- Problem Solving
- Analytical Thinking
etc.

CAREER INSIGHT
- Advantages of this profession
- Difficulties of this profession

LEARNING ROADMAP
- What a student should learn in the next 3 months

========================
OUTPUT FORMAT
========================

Always use this format:

TIME:
TASK:

WHAT IS HAPPENING?

WHY IS THIS IMPORTANT?

SKILLS REQUIRED:
- Skill 1
- Skill 2

HOW TO LEARN THESE SKILLS:

YOUR DECISION:
(Ask the user what they want to do next)

========================
IMPORTANT
========================

Do not give short answers.

Create immersive simulations.

Make the user feel they are actually working in the profession.

Be realistic.

Be educational.

Be interactive.

The goal is career exploration through experience, not simple career advice.
"""
chat_session = model.start_chat(
    history=[
        {
            "role": "user",
            "parts": [SYSTEM_PROMPT]
        }
    ]
)

@app.route("/")
def home():
    return render_template("index.html")
@app.route("/chat", methods=["POST"])
def chat():

    global current_career
    global current_step

    user_message = request.json["message"].lower()

    try:

        response = chat_session.send_message(user_message)

        return jsonify({
            "reply": response.text
        })

    except Exception:

        # PRODUCT MANAGER START

        if "product manager" in user_message:

            current_career = "pm"
            current_step = 1

            return jsonify({
                "reply": """
🕘 9:00 AM

Welcome to your first day as a Product Manager.

The engineering team informs you that a major feature release will be delayed by 2 weeks.

SKILLS REQUIRED:
• Communication
• Leadership
• Prioritization

WHY THIS MATTERS:
Product Managers coordinate between business, design and engineering teams.

YOUR DECISION:
1. Ask why the delay happened
2. Inform management
3. Reprioritize the roadmap
"""
            })

        elif current_career == "pm" and current_step == 1:

            current_step = 2

            return jsonify({
                "reply": """
🕙 10:30 AM

You discover the delay happened because developers found critical security issues.

SKILLS REQUIRED:
• Problem Solving
• Risk Management

REALITY CHECK:
Many people think Product Managers only generate ideas.

In reality, they spend a lot of time handling risks and making decisions.

YOUR DECISION:
1. Delay the release
2. Release anyway
3. Reduce feature scope
"""
            })

        elif current_career == "pm" and current_step == 2:

            current_step = 3

            return jsonify({
                "reply": """
🕐 1:00 PM

You attend a meeting with customers.

Several users request a Dark Mode feature.

SKILLS REQUIRED:
• Customer Empathy
• Communication
• Product Thinking

HOW TO LEARN:
• Product case studies
• User interviews
• Product reviews

YOUR DECISION:
1. Prioritize Dark Mode
2. Ignore request
3. Research demand first
"""
            })

        elif current_career == "pm" and current_step == 3:

            current_step = 4

            return jsonify({
                "reply": """
🕔 5:00 PM

WORKDAY SUMMARY

Tasks Completed:
✔ Engineering discussion
✔ Security review
✔ Customer feedback meeting

Skills Used:
✔ Communication
✔ Leadership
✔ Prioritization
✔ Product Thinking

CAREER INSIGHT

Advantages:
• High impact
• Leadership opportunities
• Business exposure

Challenges:
• Many meetings
• Difficult decisions
• Responsibility without direct authority

LEARNING ROADMAP

Month 1:
• Product Management Basics

Month 2:
• Product Case Studies

Month 3:
• Build a Product Portfolio Project

Type another career to explore.
"""
            })

        # SOFTWARE ENGINEER

        elif "software engineer" in user_message:

            current_career = "se"
            current_step = 1

            return jsonify({
                "reply": """
🕘 9:00 AM

Welcome to your first day as a Software Engineer.

Users report that the login page crashes.

SKILLS REQUIRED:
• Programming
• Debugging
• Problem Solving

YOUR DECISION:
1. Check logs
2. Check code
3. Ask senior developer
"""
            })

        elif current_career == "se" and current_step == 1:

            current_step = 2

            return jsonify({
                "reply": """
🕙 11:00 AM

You discover a database connection issue.

SKILLS REQUIRED:
• SQL
• Backend Development

YOUR DECISION:
1. Fix configuration
2. Restart server
3. Investigate deeper
"""
            })

        elif current_career == "se" and current_step == 2:

            current_step = 3

            return jsonify({
                "reply": """
🕔 5:00 PM

WORKDAY SUMMARY

Tasks Completed:
✔ Bug fixing
✔ Database troubleshooting
✔ Team collaboration

Skills Used:
✔ Python
✔ SQL
✔ Problem Solving

LEARNING ROADMAP

Month 1:
• Python

Month 2:
• SQL

Month 3:
• Flask Project
"""
            })

        return jsonify({
            "reply": """
Welcome to CareerVerse AI

Available careers:

• Product Manager
• Software Engineer

Try:

I want to experience a day as a Product Manager
"""
        })

import os

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )
