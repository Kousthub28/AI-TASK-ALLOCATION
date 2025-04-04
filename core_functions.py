import datetime
import uuid

def add_individual(individuals, name, skills, proficiencies, available, shift):
    new_id = str(uuid.uuid4())[:8]
    new_individual = {
        "id": new_id,
        "name": name,
        "skills": skills,
        "proficiencies": [float(x) for x in proficiencies.split(",")],
        "available": available,
        "shift": shift,
        "tasks_assigned": 0,
        "tasks_completed": 0,
        "avg_feedback": 0.0,
        "predicted_completion": None,
        "current_task": None,
        "progress": 0
    }
    individuals.append(new_individual)
    return new_id

def update_feedback(individual_id, feedback_delta):
    for ind in st.session_state.individuals:
        if ind["id"] == individual_id:
            ind["avg_feedback"] += feedback_delta

def auto_extract_skills(task_description):
    # Dummy function to simulate skill extraction
    return ["python", "machine learning"]

def summarize_task(task_description):
    # Dummy function to simulate task summarization
    return "This is a summary of the task."

def classify_task(task_description):
    # Dummy function to simulate task classification
    return "Web Development"

def analyze_feedback_sentiment(feedback_text):
    # Dummy function to simulate feedback sentiment analysis
    return "Positive", 0.95

def ai_allocate_task_with_explanation(task_description, task_urgency, task_shift, candidates, due_date):
    # Dummy function to simulate AI task allocation
    return None, 0.0, {}

def simulate_task_completion(individual):
    # Dummy function to simulate task completion time prediction
    return 5.0

def simulate_email_notification(individual, task_description, predicted_time):
    # Dummy function to simulate email notification
    return f"Task '{task_description}' assigned to {individual['name']}. Predicted completion time: {predicted_time} hrs."

def generate_team_suggestions(individual):
    # Dummy function to simulate team suggestions generation
    return ["Improve Python skills", "Learn Docker"]

def auto_feedback_generator(individual):
    # Dummy function to simulate auto feedback generation
    return "Great job on the last task!"

def predict_future_tasks(individual):
    # Dummy function to simulate future task prediction
    return ["Task 1", "Task 2"]

def suggest_optimal_shift(individual):
    # Dummy function to simulate shift suggestion
    return "Morning"

def update_progress_for_all_tasks():
    # Dummy function to simulate task progress update
    pass

def reassign_overdue_tasks():
    # Dummy function to simulate task reassignment
    pass

def decompose_task(complex_task):
    # Dummy function to simulate task decomposition
    return ["Subtask 1", "Subtask 2"]

def schedule_job(job):
    # Dummy function to simulate job scheduling
    if "job_schedule" not in st.session_state:
        st.session_state.job_schedule = []
    st.session_state.job_schedule.append(job)

def submit_proposal(job_id, proposer_name, proposal_text, estimated_time):
    # Dummy function to simulate proposal submission
    if "proposals" not in st.session_state:
        st.session_state.proposals = []
    proposal = {
        "job_id": job_id,
        "proposer": proposer_name,
        "proposal_text": proposal_text,
        "estimated_time": estimated_time,
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    st.session_state.proposals.append(proposal)

def get_ai_response(user_message):
    # Dummy function to simulate AI response
    return "This is an AI response to your message."

def send_notification(user_id, message):
    # Dummy function to simulate sending a notification
    print(f"Notification sent to {user_id}: {message}")