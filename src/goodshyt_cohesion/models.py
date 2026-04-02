from pydantic import BaseModel, Field

class Worker(BaseModel):
    worker_id: str = Field(min_length=1)
    skills: list[str]
    capacity: int = Field(ge=1)

class WorkItem(BaseModel):
    task_id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    required_skill: str = Field(min_length=1)
    effort: int = Field(ge=1)
    dependencies: list[str] = []

class AssignmentRequest(BaseModel):
    workers: list[Worker]
    tasks: list[WorkItem]

class Assignment(BaseModel):
    task_id: str
    worker_id: str | None = None
    status: str
    reason: str = ""
