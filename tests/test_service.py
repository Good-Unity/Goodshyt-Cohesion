from goodshyt_cohesion.models import AssignmentRequest, WorkItem, Worker
from goodshyt_cohesion.service import CohesionService


def test_assigns_by_skill_and_capacity() -> None:
    service = CohesionService()
    result = service.assign(AssignmentRequest(
        workers=[Worker(worker_id="a", skills=["ops"], capacity=3)],
        tasks=[WorkItem(task_id="t1", title="Ops Task", required_skill="ops", effort=2)],
    ))
    assert result[0].status == "assigned"
    assert result[0].worker_id == "a"


def test_blocks_on_unmet_dependency() -> None:
    service = CohesionService()
    result = service.assign(AssignmentRequest(
        workers=[Worker(worker_id="a", skills=["ops"], capacity=5)],
        tasks=[WorkItem(task_id="t2", title="Serve", required_skill="ops", effort=2, dependencies=["setup"])],
    ))
    assert result[0].status == "blocked"
