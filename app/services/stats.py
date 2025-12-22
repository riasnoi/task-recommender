from typing import List

from sqlalchemy.orm import Session

from app.repositories.postgres import PostgresTopicProgressRepository
from app.schemas import Overview, TopicStat


class StatsService:
    def __init__(self, db: Session) -> None:
        self.repo = PostgresTopicProgressRepository(db)

    def overview(self) -> Overview:
        topics = self.repo.list_for_user("user-1")
        mastery_avg = sum(t.mastery for t in topics) / len(topics) if topics else 0.0
        streak = int(mastery_avg * 10)
        return Overview(progress=mastery_avg, streak=streak)

    def topics(self) -> List[TopicStat]:
        topics = self.repo.list_for_user("user-1")
        if not topics:
            topics = []
        return [TopicStat(topic=t.topic, mastery=t.mastery) for t in topics]
