import datetime
import uuid
import streamlit as st

st.set_page_config(page_title="AI Agent for Task Allocation", layout="wide")

# Rest of your code

import pandas as pd
import altair as alt
from core_functions import (
    add_individual, update_feedback, auto_extract_skills, summarize_task, classify_task,
    analyze_feedback_sentiment, ai_allocate_task_with_explanation, simulate_task_completion,
    send_notification, get_ai_response, decompose_task, auto_feedback_generator,
    predict_future_tasks, suggest_optimal_shift, generate_team_suggestions,
    update_progress_for_all_tasks, reassign_overdue_tasks, simulate_email_notification,
    schedule_job, submit_proposal
)

# Initialize session state variables if not already present.
if "individuals" not in st.session_state:
    st.session_state.individuals = [
        {"id": "1a2b3c4d", "name": "Alice", "skills": "python, machine learning, flask", 
         "proficiencies": [4.5, 4.0, 3.5], "available": True, "shift": "Morning",
         "tasks_assigned": 0, "tasks_completed": 0, "avg_feedback": 4.2, "predicted_completion": None,
         "current_task": None, "progress": 0},
        {"id": "2b3c4d5e", "name": "Bob", "skills": "javascript, react, nodejs", 
         "proficiencies": [4.0, 3.5, 4.0], "available": True, "shift": "Morning",
         "tasks_assigned": 1, "tasks_completed": 1, "avg_feedback": 3.8, "predicted_completion": None,
         "current_task": None, "progress": 0},
        {"id": "3c4d5e6f", "name": "Charlie", "skills": "java, spring boot", 
         "proficiencies": [3.0, 3.5], "available": False, "shift": "Night",
         "tasks_assigned": 2, "tasks_completed": 2, "avg_feedback": 3.2, "predicted_completion": None,
         "current_task": None, "progress": 0},
        {"id": "4d5e6f7g", "name": "Diana", "skills": "c++, embedded systems", 
         "proficiencies": [4.5, 4.0], "available": True, "shift": "Night",
         "tasks_assigned": 0, "tasks_completed": 0, "avg_feedback": 4.5, "predicted_completion": None,
         "current_task": None, "progress": 0}
    ]
if "feedback" not in st.session_state:
    st.session_state.feedback = {ind["id"]: 0.0 for ind in st.session_state.individuals}
if "match_history" not in st.session_state:
    st.session_state.match_history = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "job_schedule" not in st.session_state:
    st.session_state.job_schedule = []
if "proposals" not in st.session_state:
    st.session_state.proposals = []

# Define the application tabs.
tabs = st.tabs([
    "Task Matching", "Manage Availability", "Manage Individuals", "Match History",
    "Performance Analytics", "Team Suggestions", "Chat with AI Agent", "Task Monitoring",
    "Advanced AI Features", "Job Scheduling & Proposals"
])

# ---------------------------
# TAB 1: Task Matching with Due Date Priority
# ---------------------------
with tabs[0]:
    st.header("Task Matching")
    st.markdown("""
        **Objective:** Match tasks to individuals based on expertise, availability, and due date priority.
        - Enter a task description.
        - Specify urgency, shift, and due date.
        - View auto-extracted skills and AI-generated summaries.
    """)
    task_description = st.text_area("Enter Task Description", placeholder="Describe the task requirements here...")
    task_category = st.text_input("Enter Task Category (optional)", placeholder="e.g., Web Development, Data Analysis")
    task_urgency = st.selectbox("Task Urgency", ["Low", "Medium", "High"])
    task_shift = st.selectbox("Task Shift", ["Any", "Morning", "Night"])
    due_date_input = st.date_input("Due Date (optional)")
    due_time_input = st.time_input("Due Time (optional)", value=datetime.time(17, 0))
    due_date = datetime.datetime.combine(due_date_input, due_time_input) if due_date_input else None

    if task_description:
        recommended_skills = auto_extract_skills(task_description)
        if recommended_skills:
            st.info(f"Recommended Skills: {', '.join(recommended_skills)}")
        summary = summarize_task(task_description)
        st.write(f"*Task Summary:* {summary}")
        if not task_category.strip():
            predicted_category = classify_task(task_description)
            st.write(f"*Predicted Task Category:* {predicted_category}")
    
    col_manual, col_auto = st.columns(2)
    with col_manual:
        if st.button("Match Task (Manual)"):
            if not task_description.strip():
                st.error("Please enter a valid task description.")
            else:
                available_inds = [ind for ind in st.session_state.individuals 
                                    if ind["available"] and ind["current_task"] is None 
                                    and (task_shift == "Any" or ind["shift"] == task_shift)]
                if not available_inds:
                    st.info("No available individuals found for the specified shift.")
                else:
                    task_embedding = model.encode(task_description)
                    skills_list = [ind["skills"] for ind in available_inds]
                    skill_embeddings = model.encode(skills_list)
                    sim_scores = [cosine_similarity(task_embedding, emb) for emb in skill_embeddings]
                    urgency_weight = {"Low": 0.9, "Medium": 1.0, "High": 1.1}[task_urgency]
                    adjusted_scores = []
                    for ind, score in zip(available_inds, sim_scores):
                        adjustment = st.session_state.feedback.get(ind["id"], 0.0)
                        proficiency_bonus = sum(ind["proficiencies"]) / (len(ind["proficiencies"]) * 10) if ind["proficiencies"] else 0
                        match_bonus = 0.1 * len([skill for skill in auto_extract_skills(task_description) if skill.lower() in ind["skills"].lower()])
                        dd_mult = due_date_multiplier(due_date)
                        final_score = (score + adjustment + proficiency_bonus + match_bonus) * urgency_weight * dd_mult * (1 + calculate_task_complexity(task_description))
                        adjusted_scores.append(final_score)
                    ranked = sorted(zip(available_inds, adjusted_scores), key=lambda x: x[1], reverse=True)
                    st.subheader("Matched Individuals (Manual):")
                    for ind, score in ranked:
                        col1, col2, col3, col4 = st.columns([3, 1, 1, 2])
                        col1.write(f"*Name:* {ind['name']} | *Skills:* {ind['skills']} | *Shift:* {ind['shift']}")
                        col1.write(f"*Score:* {score:.2f}")
                        if col2.button("👍", key=f"like_{ind['id']}"):
                            update_feedback(ind["id"], 0.05)
                            st.success(f"Feedback recorded for {ind['name']} (+)")
                        if col3.button("👎", key=f"dislike_{ind['id']}"):
                            update_feedback(ind["id"], -0.05)
                            st.warning(f"Feedback recorded for {ind['name']} (-)")
                        if col4.button(f"Assign Task to {ind['name']}", key=f"assign_{ind['id']}"):
                            if ind["current_task"] is None:
                                ind["tasks_assigned"] += 1
                                ind["available"] = False
                                predicted_time = simulate_task_completion(ind)
                                ind["predicted_completion"] = predicted_time
                                ind["current_task"] = task_description
                                ind["progress"] = 0
                                st.info(f"Task assigned to {ind['name']}!")
                                email_msg = simulate_email_notification(ind, task_description, predicted_time)
                                st.text_area("Simulated Email Notification", value=email_msg, height=150)
                    st.session_state.match_history.append({
                        "task": task_description,
                        "category": task_category if task_category.strip() else predicted_category,
                        "urgency": task_urgency,
                        "matches": [(ind["id"], score) for ind, score in ranked],
                        "due_date": due_date.strftime("%Y-%m-%d %H:%M") if due_date else "N/A",
                        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
    with col_auto:
        if st.button("Auto Allocate Task"):
            if not task_description.strip():
                st.error("Please enter a valid task description.")
            else:
                candidate, candidate_score, explanation = ai_allocate_task_with_explanation(
                    task_description, task_urgency, task_shift, [], due_date
                )
                if candidate is None:
                    st.info("No available individuals found for auto allocation in the specified shift.")
                else:
                    predicted_time = simulate_task_completion(candidate)
                    candidate["tasks_assigned"] += 1
                    candidate["available"] = False
                    candidate["predicted_completion"] = predicted_time
                    candidate["current_task"] = task_description
                    candidate["progress"] = 0
                    st.success(f"Task auto-allocated to {candidate['name']} with predicted completion in {predicted_time} hrs!")
                    st.balloons()
                    st.markdown("### Allocation Breakdown")
                    st.json(explanation)
                    email_msg = simulate_email_notification(candidate, task_description, predicted_time)
                    st.text_area("Simulated Email Notification", value=email_msg, height=150)
                    st.session_state.match_history.append({
                        "task": task_description,
                        "category": task_category if task_category.strip() else classify_task(task_description),
                        "urgency": task_urgency,
                        "matches": [(candidate["id"], candidate_score)],
                        "predicted_completion": predicted_time,
                        "due_date": due_date.strftime("%Y-%m-%d %H:%M") if due_date else "N/A",
                        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
    
    st.subheader("General Feedback on Matching")
    feedback_text = st.text_area("Provide general feedback on the matching results (optional):", key="general_feedback")
    if st.button("Submit General Feedback"):
        if feedback_text.strip():
            label, score = analyze_feedback_sentiment(feedback_text)
            st.write(f"Feedback Sentiment: {label} with confidence {score:.2f}")
            st.success("General feedback recorded!")
        else:
            st.error("Please enter some feedback before submitting.")

# ---------------------------
# TAB 2: Manage Availability
# ---------------------------
with tabs[1]:
    st.header("Manage Availability")
    st.markdown("**Objective:** Update the availability status for each individual.")
    for ind in st.session_state.individuals:
        col1, col2 = st.columns([3, 1])
        col1.write(f"*Name:* {ind['name']} | *Skills:* {ind['skills']} | *Shift:* {ind['shift']}")
        new_status = col2.checkbox("Available", value=ind["available"], key=f"avail_{ind['id']}")
        ind["available"] = new_status
    st.success("Availability statuses updated.")

# ---------------------------
# TAB 3: Manage Individuals & CSV Export
# ---------------------------
with tabs[2]:
    st.header("Manage Individuals")
    st.markdown("""
        **Objective:** Add, remove, or search for individuals.
        Provide details including name, skills, proficiency levels, and shift.
    """)
    with st.form("add_individual_form"):
        name = st.text_input("Name", placeholder="Enter name")
        skills_input = st.text_input("Enter Skills (comma-separated)", placeholder="e.g., python, flask, sql")
        proficiencies_input = st.text_input("Enter Proficiency Levels (comma-separated, scale 1-5)", placeholder="e.g., 4, 3.5, 5")
        shift = st.selectbox("Select Shift", options=["Morning", "Night"])
        available_input = st.checkbox("Available", value=True)
        submitted = st.form_submit_button("Add Individual")
        if submitted:
            if not name.strip() or not skills_input.strip():
                st.error("Please enter at least a name and one skill.")
            else:
                new_id = add_individual(st.session_state.individuals, name, skills_input, proficiencies_input, available_input, shift)
                st.session_state.feedback[new_id] = 0.0
                st.success(f"Individual '{name}' added with ID: {new_id}")
    
    st.markdown("### Search Individuals")
    search_term = st.text_input("Search by name or skill")
    filtered_inds = st.session_state.individuals
    if search_term:
        filtered_inds = [ind for ind in st.session_state.individuals if search_term.lower() in ind["name"].lower() or search_term.lower() in ind["skills"].lower()]
    st.markdown("### Current Individuals")
    for ind in filtered_inds:
        st.write(f"*Name:* {ind['name']} | *Skills:* {ind['skills']} | *Shift:* {ind['shift']} | *Available:* {ind['available']}")
    
    df_inds = pd.DataFrame(st.session_state.individuals)
    csv_inds = df_inds.to_csv(index=False).encode('utf-8')
    st.download_button("Export Individuals as CSV", data=csv_inds, file_name="individuals.csv", mime="text/csv")

# ---------------------------
# TAB 4: Match History & CSV Export
# ---------------------------
with tabs[3]:
    st.header("Match History")
    st.markdown("**Objective:** Review past task matching events.")
    if st.session_state.match_history:
        for idx, record in enumerate(reversed(st.session_state.match_history), start=1):
            st.markdown(f"*Match {idx}:*")
            st.write(f"Task: {record['task']}")
            st.write(f"Category: {record['category']} | Urgency: {record['urgency']} | Due Date: {record['due_date']} | Timestamp: {record['timestamp']}")
            if "predicted_completion" in record:
                st.write(f"Predicted Completion: {record['predicted_completion']} hrs")
            for match in record['matches']:
                st.write(f"- User ID: {match[0]} | Score: {match[1]:.2f}")
            st.markdown("---")
        df_history = pd.DataFrame(st.session_state.match_history)
        csv_history = df_history.to_csv(index=False).encode('utf-8')
        st.download_button("Export Match History as CSV", data=csv_history, file_name="match_history.csv", mime="text/csv")
    else:
        st.info("No match history available yet.")

# ---------------------------
# TAB 5: Performance Analytics
# ---------------------------
with tabs[4]:
    st.header("Performance Analytics")
    st.markdown("**Objective:** View aggregated performance data and feedback trends.")
    df = pd.DataFrame(st.session_state.individuals)
    if not df.empty:
        df["predicted_completion"] = df["predicted_completion"].fillna("N/A")
        df_display = df[["name", "skills", "shift", "available", "tasks_assigned", "tasks_completed", "avg_feedback", "predicted_completion"]]
        st.dataframe(df_display)
        chart_data = df[["name", "tasks_assigned"]]
        chart = alt.Chart(chart_data).mark_bar().encode(
            x=alt.X("name", sort=None),
            y="tasks_assigned"
        ).properties(title="Tasks Assigned by Individual")
        st.altair_chart(chart, use_container_width=True)
        csv_perf = df_display.to_csv(index=False).encode('utf-8')
        st.download_button("Export Performance Analytics as CSV", data=csv_perf, file_name="performance_analytics.csv", mime="text/csv")
    else:
        st.info("No performance data available yet.")

# ---------------------------
# TAB 6: Team Suggestions & Auto Feedback
# ---------------------------
with tabs[5]:
    st.header("Team Suggestions")
    st.markdown("**Objective:** Get training or improvement suggestions for each team member based on performance.")
    for ind in st.session_state.individuals:
        st.markdown(f"### {ind['name']}")
        suggestions = generate_team_suggestions(ind)
        for suggestion in suggestions:
            st.write(f"- {suggestion}")
        auto_fb = auto_feedback_generator(ind)
        st.markdown("*AI-Generated Feedback:*")
        st.write(auto_fb)
        pred_tasks = predict_future_tasks(ind)
        shift_sugg = suggest_optimal_shift(ind)
        st.write(f"*Predicted Tasks Next Week:* {pred_tasks}")
        st.write(f"*Shift Suggestion:* {shift_sugg}")
        st.markdown("---")

# ---------------------------
# TAB 7: Chat with AI Agent
# ---------------------------
with tabs[6]:
    st.header("Chat with AI Agent")
    st.markdown("**Objective:** Interact with the AI agent. Ask questions or provide feedback.")
    if st.session_state.chat_history:
        for entry in st.session_state.chat_history:
            st.write(f"*You:* {entry['user']}")
            st.write(f"*AI:* {entry['ai']}")
            st.markdown("---")
    user_message = st.text_input("Your message to the AI Agent", key="chat_input")
    if st.button("Send Message"):
        if user_message.strip():
            ai_reply = get_ai_response(user_message)
            st.session_state.chat_history.append({"user": user_message, "ai": ai_reply})
        else:
            st.error("Please enter a message to send.")
            st.error("Please enter a message to send.")

# ---------------------------
# TAB 8: Task Monitoring & Progress Update
# ---------------------------
with tabs[7]:
    st.header("Task Monitoring")
    st.markdown("**Objective:** View active tasks with progress. Update progress or reassign overdue tasks.")
    for ind in st.session_state.individuals:
                if ind["current_task"] is not None and "progress" not in ind:
                   ind["progress"] = 0
    active_tasks = [ind for ind in st.session_state.individuals if ind["current_task"] is not None]
    if active_tasks:
        for ind in active_tasks:
            st.markdown(f"### {ind['name']} ({ind['shift']})")
            st.write(f"*Current Task:* {ind['current_task']}")
            st.write(f"*Predicted Completion:* {ind['predicted_completion']} hrs")
            st.progress(ind["progress"] / 100.0)
            st.markdown("---")
        col_update, col_reassign = st.columns(2)
        with col_update:
            if st.button("Update Task Progress"):
                update_progress_for_all_tasks()
                st.success("Progress updated!")
        with col_reassign:
            if st.button("Reassign Overdue Tasks"):
                reassign_overdue_tasks()
    else:
        st.info("No active tasks at the moment.")

# ---------------------------
# TAB 9: Advanced AI Features (Task Decomposition)
# ---------------------------
with tabs[8]:
    st.header("Advanced AI Features")
    st.markdown("**Objective:** Leverage advanced AI functions for enhanced task management.")
    st.subheader("Task Decomposition")
    complex_task = st.text_area("Enter a complex task to decompose into subtasks", placeholder="E.g., Develop a full-stack e-commerce application with payment integration, user authentication, and admin dashboard.")
    if st.button("Decompose Task"):
        if complex_task.strip():
            subtasks = decompose_task(complex_task)
            st.markdown("*Subtasks Generated:*")
            st.write(subtasks)
        else:
            st.error("Please enter a task description.")

# ---------------------------
# TAB 10: Job Scheduling & Proposals
# ---------------------------
with tabs[9]:
    st.header("Job Scheduling & Proposals")
    st.markdown("**Objective:** Schedule new jobs (with required qualifications and due dates) and allow team members to submit proposals.")
    st.subheader("Schedule a New Job")
    with st.form("schedule_job_form"):
        job_task = st.text_area("Job Task Description", placeholder="Describe the job/task")
        job_urgency = st.selectbox("Job Urgency", ["Low", "Medium", "High"])
        job_shift = st.selectbox("Task Shift", ["Any", "Morning", "Night"])
        quals_input = st.text_input("Required Qualifications (comma-separated)", placeholder="e.g., python, machine learning")
        schedule_time = st.text_input("Scheduled Time (YYYY-MM-DD HH:MM)", placeholder="e.g., 2025-04-03 14:30")
        job_due_date_input = st.date_input("Job Due Date (optional)", key="job_due_date")
        job_due_time_input = st.time_input("Job Due Time (optional)", value=datetime.time(17, 0), key="job_due_time")
        schedule_submitted = st.form_submit_button("Schedule Job")
        if schedule_submitted:
            try:
                scheduled_dt = datetime.datetime.strptime(schedule_time, "%Y-%m-%d %H:%M")
                job_due_date = datetime.datetime.combine(job_due_date_input, job_due_time_input) if job_due_date_input else None
                job = {
                    "job_id": str(uuid.uuid4())[:8],
                    "task_description": job_task,
                    "urgency": job_urgency,
                    "task_shift": job_shift,
                    "required_quals": [q.strip() for q in quals_input.split(",") if q.strip()],
                    "scheduled_time": scheduled_dt,
                    "due_date": job_due_date,
                    "assigned": False
                }
                schedule_job(job)
            except Exception as e:
                st.error(f"Error in scheduling job: {e}")
    
    st.subheader("Submit a Proposal for a Job")
    with st.form("proposal_form"):
        prop_job_id = st.text_input("Job ID", placeholder="Enter the Job ID you are proposing for")
        proposer_name = st.text_input("Your Name", placeholder="Enter your name")
        proposal_text = st.text_area("Proposal Details", placeholder="Why are you the best fit for this job?")
        estimated_time = st.number_input("Estimated Completion Time (hrs)", min_value=0.5, step=0.5)
        prop_submitted = st.form_submit_button("Submit Proposal")
        if prop_submitted:
            if prop_job_id.strip() and proposer_name.strip() and proposal_text.strip():
                submit_proposal(prop_job_id, proposer_name, proposal_text, estimated_time)
            else:
                st.error("Please fill in all proposal details.")
    
    st.subheader("Current Scheduled Jobs")
    if st.session_state.job_schedule:
        for job in st.session_state.job_schedule:
            st.markdown(f"**Job ID:** {job['job_id']}")
            st.write(f"Task: {job['task_description']}")
            st.write(f"Urgency: {job['urgency']} | Shift: {job['task_shift']}")
            st.write(f"Required Qualifications: {', '.join(job['required_quals']) if job['required_quals'] else 'None'}")
            st.write(f"Scheduled Time: {job['scheduled_time'].strftime('%Y-%m-%d %H:%M')}")
            st.write(f"Due Date: {job['due_date'].strftime('%Y-%m-%d %H:%M') if job.get('due_date') else 'N/A'}")
            st.write(f"Assigned: {'Yes' if job.get('assigned') else 'No'}")
            st.markdown("---")
    else:
        st.info("No scheduled jobs yet.")
    
    st.subheader("Current Proposals")
    if st.session_state.proposals:
        for prop in st.session_state.proposals:
            st.markdown(f"**Job ID:** {prop['job_id']} | **Proposer:** {prop['proposer']}")
            st.write(f"Proposal: {prop['proposal_text']}")
            st.write(f"Estimated Time: {prop['estimated_time']} hrs | Submitted at: {prop['timestamp']}")
            st.markdown("---")
    else:
        st.info("No proposals submitted yet.")