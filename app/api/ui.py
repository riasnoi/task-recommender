from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(tags=["ui"])


@router.get("/ui", response_class=HTMLResponse)
def ui():
    html = """
    <!doctype html>
    <html>
    <head>
      <meta charset="utf-8" />
      <title>Learning Tasks Recommender UI</title>
      <style>
        body { font-family: Arial, sans-serif; margin: 24px; }
        section { margin-bottom: 24px; padding: 16px; border: 1px solid #ddd; border-radius: 8px; }
        h2 { margin-top: 0; }
        button { padding: 6px 12px; margin-top: 8px; }
        input, textarea { width: 100%; margin-top: 6px; padding: 6px; }
        pre { background: #f6f6f6; padding: 12px; border-radius: 6px; overflow: auto; }
      </style>
    </head>
    <body>
      <h1>Learning Tasks Recommender — быстрый UI</h1>
      <section>
        <h2>Проверка здоровья</h2>
        <button onclick="health()">GET /health</button>
        <pre id="health"></pre>
      </section>
      <section>
        <h2>Задачи</h2>
        <button onclick="loadTasks()">GET /api/v1/tasks</button>
        <pre id="tasks"></pre>
      </section>
      <section>
        <h2>Попытка</h2>
        <label>Task ID <input id="attempt-task" value="task-1"/></label>
        <label>Answer <textarea id="attempt-answer">SELECT 1</textarea></label>
        <label>Lang <input id="attempt-lang" value="sql"/></label>
        <button onclick="submitAttempt()">POST /api/v1/attempts</button>
        <pre id="attempt"></pre>
      </section>
      <section>
        <h2>Рекомендации</h2>
        <button onclick="loadRecs()">GET /api/v1/recommendations</button>
        <pre id="recs"></pre>
      </section>
      <section>
        <h2>План</h2>
        <button onclick="loadPlan()">GET /api/v1/plan/today</button>
        <pre id="plan"></pre>
      </section>
      <script>
        async function health() {
          const r = await fetch('/health');
          document.getElementById('health').textContent = JSON.stringify(await r.json(), null, 2);
        }
        async function loadTasks() {
          const r = await fetch('/api/v1/tasks');
          document.getElementById('tasks').textContent = JSON.stringify(await r.json(), null, 2);
        }
        async function submitAttempt() {
          const payload = {
            taskId: document.getElementById('attempt-task').value,
            answer: document.getElementById('attempt-answer').value,
            answerLang: document.getElementById('attempt-lang').value
          };
          const r = await fetch('/api/v1/attempts', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(payload)});
          document.getElementById('attempt').textContent = JSON.stringify(await r.json(), null, 2);
        }
        async function loadRecs() {
          const r = await fetch('/api/v1/recommendations');
          document.getElementById('recs').textContent = JSON.stringify(await r.json(), null, 2);
        }
        async function loadPlan() {
          const r = await fetch('/api/v1/plan/today');
          document.getElementById('plan').textContent = JSON.stringify(await r.json(), null, 2);
        }
      </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html)
