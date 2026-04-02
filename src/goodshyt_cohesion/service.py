from .models import Assignment, AssignmentRequest, Worker

class CohesionService:
    def assign(self, payload: AssignmentRequest) -> list[Assignment]:
        capacities = {worker.worker_id: worker.capacity for worker in payload.workers}
        worker_index = {worker.worker_id: worker for worker in payload.workers}
        completed: set[str] = set()
        assignments: list[Assignment] = []

        for task in payload.tasks:
            unmet = [dep for dep in task.dependencies if dep not in completed]
            if unmet:
                assignments.append(Assignment(task_id=task.task_id, status="blocked", reason=f"unmet dependencies: {', '.join(unmet)}"))
                continue
            candidate = self._find_worker(task.required_skill, task.effort, payload.workers, capacities)
            if candidate is None:
                assignments.append(Assignment(task_id=task.task_id, status="unassigned", reason="no available worker with matching skill/capacity"))
                continue
            capacities[candidate.worker_id] -= task.effort
            assignments.append(Assignment(task_id=task.task_id, worker_id=candidate.worker_id, status="assigned"))
            completed.add(task.task_id)
        return assignments

    def _find_worker(self, skill: str, effort: int, workers: list[Worker], capacities: dict[str, int]) -> Worker | None:
        eligible = [worker for worker in workers if skill in worker.skills and capacities[worker.worker_id] >= effort]
        if not eligible:
            return None
        return sorted(eligible, key=lambda worker: capacities[worker.worker_id], reverse=True)[0]
