import hashlib
import json
import random
from dataclasses import asdict
from datetime import datetime
from uuid import uuid4

from qdrant_client.models import Distance, VectorParams
from sqlalchemy.orm import Session

from app.clients.neo4j_client import get_neo4j_driver
from app.clients.qdrant_client import get_qdrant_client
from app.clients.redis_client import get_redis_client
from app.domain import RecommendationItemModel, RecommendationRunModel
from app.repositories.postgres import PostgresRecommendationRepository, PostgresTaskRepository
from app.schemas import RecommendationItem, RecommendationResponse


class RecommendationService:
    def __init__(self, db: Session) -> None:
        self.repo = PostgresRecommendationRepository(db)
        self.tasks_repo = PostgresTaskRepository(db)
        self.qdrant = get_qdrant_client()
        self.redis = get_redis_client()
        self.neo4j_driver = get_neo4j_driver()
        self.collection_name = "tasks"
        self._ensure_collection()
        self._ensure_graph()

    def _ensure_collection(self) -> None:
        existing = [col.name for col in self.qdrant.get_collections().collections]
        if self.collection_name not in existing:
            self.qdrant.create_collection(self.collection_name, vectors=VectorParams(size=8, distance=Distance.COSINE))

    def _ensure_graph(self) -> None:
        with self.neo4j_driver.session() as session:
            session.run("MERGE (t:Topic {name: $name})", name="sql.basics")
            session.run("MERGE (t:Topic {name: $name})", name="sql.joins")
            session.run("MATCH (a:Topic {name:'sql.basics'}), (b:Topic {name:'sql.joins'}) MERGE (a)-[:PREQ]->(b)")

    def _vector_for_task(self, task_id: str) -> list[float]:
        # Псевдо-эмбеддинг на основе хеша, чтобы было детерминировано
        h = hashlib.sha256(task_id.encode()).digest()
        return [int.from_bytes(h[i:i+2], "little") / 65535.0 for i in range(0, 16, 2)]

    def _upsert_task_vectors(self) -> None:
        tasks = self.tasks_repo.list(topic=None, difficulty=None, tags=None)
        points = []
        for task in tasks:
            points.append({"id": task.id, "vector": self._vector_for_task(task.id), "payload": {"topic": task.topic}})
        if points:
            self.qdrant.upsert(collection_name=self.collection_name, points=points)

    def _score_with_graph(self, topic: str | None) -> float:
        if not topic:
            return 0.0
        with self.neo4j_driver.session() as session:
            res = session.run(
                "MATCH (t:Topic {name:$topic}) OPTIONAL MATCH (p:Topic)-[:PREQ]->(t) RETURN count(p) AS prereq",
                topic=topic,
            )
            record = res.single()
            prereq_count = record["prereq"] if record else 0
        return -0.05 * prereq_count

    def _build_default_run(self) -> RecommendationRunModel:
        self._upsert_task_vectors()
        tasks = self.tasks_repo.list(topic=None, difficulty=None, tags=None)
        items: list[RecommendationItemModel] = []
        for idx, task in enumerate(tasks):
            # Простая попытка векторного ранжирования: случай + штраф/бонус графа
            vec_score = random.random()
            graph_score = self._score_with_graph(task.topic)
            score = round(max(0.0, vec_score + graph_score), 4)
            items.append(RecommendationItemModel(task_id=task.id, rank=idx + 1, score=score, reasons=["seed", f"graph_boost:{graph_score}"]))
        return RecommendationRunModel(run_id=str(uuid4()), user_id="user-1", items=items, created_at=datetime.utcnow())

    def get_recommendations(self) -> RecommendationResponse:
        cached = self.redis.get("recs:user-1")
        if cached:
            data = json.loads(cached)
            return RecommendationResponse(**data)
        run = self.repo.latest_for_user("user-1")
        if not run:
            run = self._build_default_run()
            self.repo.save_run(run)
        response = RecommendationResponse(
            runId=run.run_id,
            items=[RecommendationItem(**asdict(item)) for item in run.items],
        )
        self.redis.setex("recs:user-1", 300, response.json())
        return response

    def recompute(self) -> dict:
        run = self._build_default_run()
        self.repo.save_run(run)
        self.redis.delete("recs:user-1")
        return {"runId": run.run_id, "status": "recomputed"}
