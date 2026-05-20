---
slug: "workflow-automation"
display_name: "Workflow Automation"
description: "Automate construction data workflows. Build ETL pipelines and DAG workflows for recurring tasks."
---

# Workflow Automation

## Business Case

### Problem Statement
Data workflow challenges:
- Manual repetitive tasks
- Data inconsistency between systems
- Error-prone manual processes
- Lack of audit trails

### Solution
Automated workflow system for construction data pipelines with task dependencies, scheduling, and monitoring.

## Technical Implementation

```python
import pandas as pd
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import json


class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    SKIPPED = "skipped"


class TriggerType(Enum):
    MANUAL = "manual"
    SCHEDULED = "scheduled"
    EVENT = "event"
    DEPENDENCY = "dependency"


class ScheduleInterval(Enum):
    HOURLY = "hourly"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"


@dataclass
class WorkflowTask:
    task_id: str
    name: str
    task_type: str  # extract, transform, load, notify, validate
    config: Dict[str, Any] = field(default_factory=dict)
    dependencies: List[str] = field(default_factory=list)
    retries: int = 3
    timeout_minutes: int = 30


@dataclass
class TaskExecution:
    task_id: str
    status: TaskStatus
    start_time: datetime
    end_time: Optional[datetime] = None
    output: Any = None
    error: str = ""
    attempt: int = 1


@dataclass
class Workflow:
    workflow_id: str
    name: str
    description: str
    tasks: List[WorkflowTask] = field(default_factory=list)
    trigger_type: TriggerType = TriggerType.MANUAL
    schedule: Optional[ScheduleInterval] = None


class WorkflowAutomation:
    """Automate construction data workflows and ETL pipelines."""

    def __init__(self, project_name: str):
        self.project_name = project_name
        self.workflows: Dict[str, Workflow] = {}
        self.executions: Dict[str, List[TaskExecution]] = {}
        self.task_handlers: Dict[str, Callable] = {}
        self._register_default_handlers()

    def _register_default_handlers(self):
        """Register default task handlers."""

        self.task_handlers['extract_csv'] = self._extract_csv
        self.task_handlers['extract_excel'] = self._extract_excel
        self.task_handlers['transform_filter'] = self._transform_filter
        self.task_handlers['transform_aggregate'] = self._transform_aggregate
        self.task_handlers['transform_join'] = self._transform_join
        self.task_handlers['load_csv'] = self._load_csv
        self.task_handlers['validate_schema'] = self._validate_schema
        self.task_handlers['notify_email'] = self._notify_email

    def register_handler(self, task_type: str, handler: Callable):
        """Register custom task handler."""
        self.task_handlers[task_type] = handler

    def create_workflow(self, workflow_id: str, name: str,
                        description: str = "") -> Workflow:
        """Create new workflow."""

        workflow = Workflow(
            workflow_id=workflow_id,
            name=name,
            description=description
        )
        self.workflows[workflow_id] = workflow
        self.executions[workflow_id] = []
        return workflow

    def add_task(self, workflow_id: str, task: WorkflowTask):
        """Add task to workflow."""

        if workflow_id in self.workflows:
            self.workflows[workflow_id].tasks.append(task)

    def set_schedule(self, workflow_id: str, interval: ScheduleInterval):
        """Set workflow schedule."""

        if workflow_id in self.workflows:
            self.workflows[workflow_id].trigger_type = TriggerType.SCHEDULED
            self.workflows[workflow_id].schedule = interval

    def get_execution_order(self, workflow_id: str) -> List[str]:
        """Get task execution order based on dependencies (topological sort)."""

        if workflow_id not in self.workflows:
            return []

        workflow = self.workflows[workflow_id]
        tasks = {t.task_id: t for t in workflow.tasks}

        # Build dependency graph
        in_degree = {t.task_id: 0 for t in workflow.tasks}
        graph = {t.task_id: [] for t in workflow.tasks}

        for task in workflow.tasks:
            for dep in task.dependencies:
                if dep in graph:
                    graph[dep].append(task.task_id)
                    in_degree[task.task_id] += 1

        # Topological sort
        queue = [t for t in in_degree if in_degree[t] == 0]
        order = []

        while queue:
            task_id = queue.pop(0)
            order.append(task_id)

            for dependent in graph[task_id]:
                in_degree[dependent] -= 1
                if in_degree[dependent] == 0:
                    queue.append(dependent)

        return order

    def execute_workflow(self, workflow_id: str,
                         context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute workflow."""

        if workflow_id not in self.workflows:
            return {'error': f'Workflow {workflow_id} not found'}

        workflow = self.workflows[workflow_id]
        context = context or {}
        execution_results = []
        task_outputs = {}

        execution_order = self.get_execution_order(workflow_id)
        start_time = datetime.now()

        for task_id in execution_order:
            task = next(t for t in workflow.tasks if t.task_id == task_id)

            # Check dependencies
            deps_success = all(
                task_outputs.get(dep, {}).get('status') == TaskStatus.SUCCESS
                for dep in task.dependencies
            )

            if not deps_success:
                execution = TaskExecution(
                    task_id=task_id,
                    status=TaskStatus.SKIPPED,
                    start_time=datetime.now(),
                    end_time=datetime.now(),
                    error="Dependencies not met"
                )
            else:
                execution = self._execute_task(task, context, task_outputs)

            task_outputs[task_id] = {
                'status': execution.status,
                'output': execution.output
            }
            execution_results.append(execution)
            self.executions[workflow_id].append(execution)

        end_time = datetime.now()
        success_count = sum(1 for e in execution_results if e.status == TaskStatus.SUCCESS)

        return {
            'workflow_id': workflow_id,
            'workflow_name': workflow.name,
            'start_time': start_time.isoformat(),
            'end_time': end_time.isoformat(),
            'duration_seconds': (end_time - start_time).total_seconds(),
            'total_tasks': len(execution_results),
            'successful_tasks': success_count,
            'failed_tasks': sum(1 for e in execution_results if e.status == TaskStatus.FAILED),
            'skipped_tasks': sum(1 for e in execution_results if e.status == TaskStatus.SKIPPED),
            'overall_status': 'success' if success_count == len(execution_results) else 'failed',
            'task_results': [
                {
                    'task_id': e.task_id,
                    'status': e.status.value,
                    'error': e.error
                }
                for e in execution_results
            ]
        }

    def _execute_task(self, task: WorkflowTask, context: Dict[str, Any],
                      task_outputs: Dict[str, Any]) -> TaskExecution:
        """Execute single task."""

        execution = TaskExecution(
            task_id=task.task_id,
            status=TaskStatus.RUNNING,
            start_time=datetime.now()
        )

        handler = self.task_handlers.get(task.task_type)

        if not handler:
            execution.status = TaskStatus.FAILED
            execution.error = f"No handler for task type: {task.task_type}"
            execution.end_time = datetime.now()
            return execution

        # Merge context with task config
        task_config = {**task.config, 'context': context, 'task_outputs': task_outputs}

        for attempt in range(1, task.retries + 1):
            try:
                execution.attempt = attempt
                result = handler(task_config)
                execution.output = result
                execution.status = TaskStatus.SUCCESS
                break
            except Exception as e:
                execution.error = str(e)
                if attempt == task.retries:
                    execution.status = TaskStatus.FAILED

        execution.end_time = datetime.now()
        return execution

    # Default task handlers
    def _extract_csv(self, config: Dict[str, Any]) -> pd.DataFrame:
        """Extract data from CSV."""
        path = config.get('path')
        if path:
            return pd.read_csv(path)
        return pd.DataFrame()

    def _extract_excel(self, config: Dict[str, Any]) -> pd.DataFrame:
        """Extract data from Excel."""
        path = config.get('path')
        sheet = config.get('sheet', 0)
        if path:
            return pd.read_excel(path, sheet_name=sheet)
        return pd.DataFrame()

    def _transform_filter(self, config: Dict[str, Any]) -> pd.DataFrame:
        """Filter DataFrame."""
        task_outputs = config.get('task_outputs', {})
        source_task = config.get('source_task')
        column = config.get('column')
        operator = config.get('operator', '==')
        value = config.get('value')

        df = task_outputs.get(source_task, {}).get('output', pd.DataFrame())

        if df.empty or column not in df.columns:
            return df

        if operator == '==':
            return df[df[column] == value]
        elif operator == '!=':
            return df[df[column] != value]
        elif operator == '>':
            return df[df[column] > value]
        elif operator == '<':
            return df[df[column] < value]

        return df

    def _transform_aggregate(self, config: Dict[str, Any]) -> pd.DataFrame:
        """Aggregate DataFrame."""
        task_outputs = config.get('task_outputs', {})
        source_task = config.get('source_task')
        group_by = config.get('group_by', [])
        aggregations = config.get('aggregations', {})

        df = task_outputs.get(source_task, {}).get('output', pd.DataFrame())

        if df.empty:
            return df

        return df.groupby(group_by).agg(aggregations).reset_index()

    def _transform_join(self, config: Dict[str, Any]) -> pd.DataFrame:
        """Join DataFrames."""
        task_outputs = config.get('task_outputs', {})
        left_task = config.get('left_task')
        right_task = config.get('right_task')
        left_on = config.get('left_on')
        right_on = config.get('right_on')
        how = config.get('how', 'left')

        left_df = task_outputs.get(left_task, {}).get('output', pd.DataFrame())
        right_df = task_outputs.get(right_task, {}).get('output', pd.DataFrame())

        return pd.merge(left_df, right_df, left_on=left_on, right_on=right_on, how=how)

    def _load_csv(self, config: Dict[str, Any]) -> str:
        """Load data to CSV."""
        task_outputs = config.get('task_outputs', {})
        source_task = config.get('source_task')
        path = config.get('path')

        df = task_outputs.get(source_task, {}).get('output', pd.DataFrame())

        if not df.empty and path:
            df.to_csv(path, index=False)
            return path

        return ""

    def _validate_schema(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Validate DataFrame schema."""
        task_outputs = config.get('task_outputs', {})
        source_task = config.get('source_task')
        required_columns = config.get('required_columns', [])

        df = task_outputs.get(source_task, {}).get('output', pd.DataFrame())

        missing = [c for c in required_columns if c not in df.columns]

        return {
            'valid': len(missing) == 0,
            'missing_columns': missing,
            'actual_columns': list(df.columns)
        }

    def _notify_email(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Simulate email notification."""
        return {
            'sent': True,
            'to': config.get('to'),
            'subject': config.get('subject'),
            'timestamp': datetime.now().isoformat()
        }

    def export_workflow_definition(self, workflow_id: str) -> Dict[str, Any]:
        """Export workflow definition as JSON."""

        if workflow_id not in self.workflows:
            return {}

        workflow = self.workflows[workflow_id]

        return {
            'workflow_id': workflow.workflow_id,
            'name': workflow.name,
            'description': workflow.description,
            'trigger_type': workflow.trigger_type.value,
            'schedule': workflow.schedule.value if workflow.schedule else None,
            'tasks': [
                {
                    'task_id': t.task_id,
                    'name': t.name,
                    'task_type': t.task_type,
                    'config': t.config,
                    'dependencies': t.dependencies,
                    'retries': t.retries,
                    'timeout_minutes': t.timeout_minutes
                }
                for t in workflow.tasks
            ]
        }

    def generate_airflow_dag(self, workflow_id: str) -> str:
        """Generate Airflow DAG code for workflow."""

        if workflow_id not in self.workflows:
            return ""

        workflow = self.workflows[workflow_id]

        dag_code = f'''
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

default_args = {{
    'owner': 'construction_team',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}}

dag = DAG(
    '{workflow.workflow_id}',
    default_args=default_args,
    description='{workflow.description}',
    schedule_interval='@{workflow.schedule.value if workflow.schedule else "daily"}',
    catchup=False
)

'''

        for task in workflow.tasks:
            dag_code += f'''
def {task.task_id}_func(**kwargs):
    # Task: {task.name}
    # Type: {task.task_type}
    pass

{task.task_id} = PythonOperator(
    task_id='{task.task_id}',
    python_callable={task.task_id}_func,
    dag=dag
)

'''

        # Add dependencies
        for task in workflow.tasks:
            for dep in task.dependencies:
                dag_code += f"{dep} >> {task.task_id}\n"

        return dag_code

    def get_execution_history(self, workflow_id: str) -> List[Dict[str, Any]]:
        """Get workflow execution history."""

        return [
            {
                'task_id': e.task_id,
                'status': e.status.value,
                'start_time': e.start_time.isoformat(),
                'end_time': e.end_time.isoformat() if e.end_time else None,
                'attempt': e.attempt,
                'error': e.error
            }
            for e in self.executions.get(workflow_id, [])
        ]
```

## Quick Start

```python
# Create workflow automation
automation = WorkflowAutomation("Office Building A")

# Create ETL workflow
workflow = automation.create_workflow(
    "daily_cost_etl",
    "Daily Cost Data ETL",
    "Extract cost data, transform, and load to reporting database"
)

# Add tasks
automation.add_task("daily_cost_etl", WorkflowTask(
    task_id="extract_costs",
    name="Extract Cost Data",
    task_type="extract_csv",
    config={"path": "costs.csv"}
))

automation.add_task("daily_cost_etl", WorkflowTask(
    task_id="aggregate_costs",
    name="Aggregate by Category",
    task_type="transform_aggregate",
    config={
        "source_task": "extract_costs",
        "group_by": ["category"],
        "aggregations": {"amount": "sum"}
    },
    dependencies=["extract_costs"]
))

automation.add_task("daily_cost_etl", WorkflowTask(
    task_id="load_report",
    name="Save Report",
    task_type="load_csv",
    config={
        "source_task": "aggregate_costs",
        "path": "cost_report.csv"
    },
    dependencies=["aggregate_costs"]
))

# Execute workflow
result = automation.execute_workflow("daily_cost_etl")
print(f"Status: {result['overall_status']}")
print(f"Successful: {result['successful_tasks']}/{result['total_tasks']}")
```

## Common Use Cases

### 1. Schedule Workflow
```python
automation.set_schedule("daily_cost_etl", ScheduleInterval.DAILY)
```

### 2. Generate Airflow DAG
```python
dag_code = automation.generate_airflow_dag("daily_cost_etl")
with open("daily_cost_dag.py", "w") as f:
    f.write(dag_code)
```

### 3. Export Definition
```python
definition = automation.export_workflow_definition("daily_cost_etl")
with open("workflow.json", "w") as f:
    json.dump(definition, f, indent=2)
```

## Resources
- **DDC Book**: Chapter 4.2 - ETL and Process Automation
- **Apache Airflow**: https://airflow.apache.org/
- **Website**: https://datadrivenconstruction.io
