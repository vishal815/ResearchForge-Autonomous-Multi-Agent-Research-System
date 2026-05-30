from typing import TypedDict, List, Optional


class TodoItem(TypedDict):
    id: int
    task: str
    status: str        # "pending" | "done"
    assigned_to: str   # "search_agent" | "analysis_agent" | "examples_agent"


class ResearchState(TypedDict):
    user_query: str
    todos: List[TodoItem]
    virtual_files: dict
    final_report: Optional[str]
    quality_score: Optional[float]
    retry_count: int
    status_log: List[str]
