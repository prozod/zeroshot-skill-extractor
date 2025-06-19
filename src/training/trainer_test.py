from transformers import pipeline
from sklearn.metrics import precision_recall_fscore_support
from pathlib import Path

model_path = Path(__file__).parent.resolve() / \
    "./skill_extractor_zsl_model"
model_path = model_path.resolve()

# Load your trained or pre-trained NLI model
zsl = pipeline("zero-shot-classification",
               model=model_path,  # or your fine-tuned model
               device=0)

# resume_text = """
# Collaborated with cross-functional teams to deploy containerized microservices using EKS, Terraform, and GitOps workflows.
# Enhanced frontend workflows leveraging Next.js, GraphQL, and Vite. Integrated observability with Datadog and Sentry.
# """
#
# candidate_skills = [
#     "Docker", "Kubernetes", "Terraform", "GitOps", "AWS",
#     "Next.js", "GraphQL", "Vite", "Datadog", "Sentry",
#     "Frontend development", "Observability", "Microservices"
# ]

resume_text = """
    Seasoned engineer with 5+ years building and scaling distributed backend systems. Played a key role in refactoring legacy monoliths into microservice-based architecture using Spring Boot and Docker. Designed REST and GraphQL APIs, integrated with PostgreSQL and Redis, and maintained real-time data pipelines using Kafka and Airflow. Championed CI/CD adoption with GitHub Actions and Terraform for AWS deployments. Collaborated closely with SRE teams on observability stack (Prometheus, Grafana, ELK). Recently led backend modernization effort, introducing gRPC, service mesh patterns, and zero-downtime rollouts. Actively contributed to tech debt reduction and performance tuning across multiple services.
"""
candidate_skills = [
    "Backend development", "Spring Boot", "Docker", "Microservices", "GraphQL",
    "REST APIs", "PostgreSQL", "Redis", "Kafka", "Airflow",
    "CI/CD", "GitHub Actions", "Terraform", "AWS", "Prometheus",
    "Grafana", "ELK stack", "gRPC", "Service Mesh", "Performance Optimization",
    "Software Architecture", "Game Development", "C/C++", "Algorithms", "Computer Architecture", "Assembly (NASM/TASM)", "ChatGPT Professional UAB Graduate", "Godot", "Unity Engine", "Formal Languages & Automata", "DevOps", "Real-time systems", "SRE", "Distributed Systems"
]

# Run inference
results = zsl(resume_text, candidate_skills, multi_label=True)

# Print top matches
print(resume_text + "\n")
for label, score in zip(results['labels'], results['scores']):
    if (score >= 0.85):
        print(f"{label}: {score:.4f}")

print("\n----------- skills that do not match --------- ")
for label, score in zip(results['labels'], results['scores']):
    if (score < 0.85):
        print(f"{label}: {score:.4f}")

model_scores = {
    "Backend development": 0.85,
    "Spring Boot": 0.92,
    "Docker": 0.78,
    "Microservices": 0.80,
    "GraphQL": 0.75,
    "REST APIs": 0.70,
    "PostgreSQL": 0.65,
    "Redis": 0.60,
    "Kafka": 0.55,
    "Airflow": 0.50,
    "CI/CD": 0.68,
    "GitHub Actions": 0.60,
    "Terraform": 0.72,
    "AWS": 0.58,
    "Prometheus": 0.57,
    "Grafana": 0.55,
    "ELK stack": 0.52,
    "gRPC": 0.49,
    "Service Mesh": 0.48,
    "Performance Optimization": 0.45,
    "Software Architecture": 0.44,
    "DevOps": 0.43,
    "Real-time systems": 0.42,
    "SRE": 0.40,
    "Distributed Systems": 0.70
}

# Define your threshold for positive prediction
threshold = 0.6

# Generate binary predictions based on threshold
predicted_skills = [skill for skill,
                    score in model_scores.items() if score >= threshold]

# Prepare binary vectors for sklearn metrics
all_skills = list(set(candidate_skills))  # Union of all candidate skills

y_true = [1 if skill in candidate_skills else 0 for skill in all_skills]
y_pred = [1 if skill in predicted_skills else 0 for skill in all_skills]

precision, recall, f1, _ = precision_recall_fscore_support(
    y_true, y_pred, average='binary')

print(f"Predicted skills (threshold={threshold}):")
print(predicted_skills)
print(f"\nPrecision: {precision:.2f}")
print(f"Recall: {recall:.2f}")
print(f"F1 Score: {f1:.2f}")
