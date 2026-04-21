from flask import Flask, jsonify, request


app = Flask(__name__)

tasks = [
    {"id": 1, "title": "Estudar GitHub Actions", "done": True},
    {"id": 2, "title": "Dockerizar a API", "done": False},
]


@app.get("/")
def home():
    return jsonify(
        {
            "project": "DevOps Study API",
            "message": "API simples criada para praticar fluxo de CI/CD e Docker.",
            "version": "1.0.0",
        }
    )


@app.get("/health")
def health_check():
    return jsonify({"status": "ok"})


@app.get("/tasks")
def list_tasks():
    status = request.args.get("status", "").strip().lower()

    if status == "done":
        filtered_tasks = [task for task in tasks if task["done"] is True]
        return jsonify(filtered_tasks)

    if status == "pending":
        filtered_tasks = [task for task in tasks if task["done"] is False]
        return jsonify(filtered_tasks)

    return jsonify(tasks)


@app.post("/tasks")
def create_task():
    data = request.get_json(silent=True) or {}
    title = (data.get("title") or "").strip()

    if not title:
        return jsonify({"error": "O campo 'title' e obrigatorio."}), 400

    task = {"id": len(tasks) + 1, "title": title, "done": False}
    tasks.append(task)
    return jsonify(task), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
