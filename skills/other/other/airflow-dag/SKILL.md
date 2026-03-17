---
name: "airflow-dag"
description: "Create Apache Airflow DAGs for construction data pipelines. Orchestrate ETL, validation, and reporting workflows."
homepage: "https://datadrivenconstruction.io"
metadata: {"openclaw": {"emoji": "⚙️", "os": ["win32"], "homepage": "https://datadrivenconstruction.io", "requires": {"bins": ["python3"]}}}
---
# Apache Airflow DAG for Construction

## Overview
Apache Airflow orchestrates complex data pipelines. This skill creates DAGs for construction ETL processes - from BIM extraction to cost reports.

## Python Implementation

```python
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass
from enum import Enum
import json


class TaskStatus(Enum):
    """Task execution status."""
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class DAGTask:
    """Single task in DAG."""
    task_id: str
    operator: str
    params: Dict[str, Any]
    upstream: List[str]
    downstream: List[str]


@dataclass
class DAGConfig:
    """DAG configuration."""
    dag_id: str
    schedule: str
    start_date: datetime
    catchup: bool
    default_args: Dict[str, Any]
    tags: List[str]


class ConstructionDAGBuilder:
    """Build Airflow DAGs for construction pipelines."""

    # Default DAG arguments
    DEFAULT_ARGS = {
        'owner': 'ddc',
        'depends_on_past': False,
        'email_on_failure': True,
        'email_on_retry': False,
        'retries': 2,
        'retry_delay': timedelta(minutes=5),
        'execution_timeout': timedelta(hours=2)
    }

    def __init__(self, dag_id: str,
                 schedule: str = '@daily',
                 tags: List[str] = None):
        self.dag_id = dag_id
        self.schedule = schedule
        self.tags = tags or ['construction', 'ddc']
        self.tasks: Dict[str, DAGTask] = {}

    def add_bash_task(self, task_id: str,
                      command: str,
                      upstream: List[str] = None) -> str:
        """Add bash command task."""
        self.tasks[task_id] = DAGTask(
            task_id=task_id,
            operator='BashOperator',
            params={'bash_command': command},
            upstream=upstream or [],
            downstream=[]
        )
        self._update_downstream(task_id, upstream)
        return task_id

    def add_python_task(self, task_id: str,
                        python_callable: str,
                        op_kwargs: Dict = None,
                        upstream: List[str] = None) -> str:
        """Add Python callable task."""
        self.tasks[task_id] = DAGTask(
            task_id=task_id,
            operator='PythonOperator',
            params={
                'python_callable': python_callable,
                'op_kwargs': op_kwargs or {}
            },
            upstream=upstream or [],
            downstream=[]
        )
        self._update_downstream(task_id, upstream)
        return task_id

    def add_sensor_task(self, task_id: str,
                        filepath: str,
                        upstream: List[str] = None) -> str:
        """Add file sensor task."""
        self.tasks[task_id] = DAGTask(
            task_id=task_id,
            operator='FileSensor',
            params={
                'filepath': filepath,
                'poke_interval': 300,
                'timeout': 3600
            },
            upstream=upstream or [],
            downstream=[]
        )
        self._update_downstream(task_id, upstream)
        return task_id

    def add_branch_task(self, task_id: str,
                        python_callable: str,
                        upstream: List[str] = None) -> str:
        """Add branching task."""
        self.tasks[task_id] = DAGTask(
            task_id=task_id,
            operator='BranchPythonOperator',
            params={'python_callable': python_callable},
            upstream=upstream or [],
            downstream=[]
        )
        self._update_downstream(task_id, upstream)
        return task_id

    def _update_downstream(self, task_id: str, upstream: List[str]):
        """Update downstream references."""
        if upstream:
            for up_task in upstream:
                if up_task in self.tasks:
                    self.tasks[up_task].downstream.append(task_id)

    def generate_dag_code(self) -> str:
        """Generate Airflow DAG Python code."""

        code = '''
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.sensors.filesystem import FileSensor
from datetime import datetime, timedelta

default_args = {
    'owner': 'ddc',
    'depends_on_past': False,
    'email_on_failure': True,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

'''
        code += f'''
with DAG(
    dag_id='{self.dag_id}',
    default_args=default_args,
    schedule_interval='{self.schedule}',
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags={self.tags}
) as dag:

'''
        # Generate task definitions
        for task_id, task in self.tasks.items():
            code += self._generate_task_code(task)
            code += '\n'

        # Generate dependencies
        code += '\n    # Task dependencies\n'
        for task_id, task in self.tasks.items():
            if task.upstream:
                for upstream in task.upstream:
                    code += f"    {upstream} >> {task_id}\n"

        return code

    def _generate_task_code(self, task: DAGTask) -> str:
        """Generate code for single task."""

        if task.operator == 'BashOperator':
            return f'''    {task.task_id} = BashOperator(
        task_id='{task.task_id}',
        bash_command="{task.params['bash_command']}"
    )'''

        elif task.operator == 'PythonOperator':
            kwargs = json.dumps(task.params.get('op_kwargs', {}))
            return f'''    {task.task_id} = PythonOperator(
        task_id='{task.task_id}',
        python_callable={task.params['python_callable']},
        op_kwargs={kwargs}
    )'''

        elif task.operator == 'FileSensor':
            return f'''    {task.task_id} = FileSensor(
        task_id='{task.task_id}',
        filepath='{task.params["filepath"]}',
        poke_interval={task.params['poke_interval']},
        timeout={task.params['timeout']}
    )'''

        elif task.operator == 'BranchPythonOperator':
            return f'''    {task.task_id} = BranchPythonOperator(
        task_id='{task.task_id}',
        python_callable={task.params['python_callable']}
    )'''

        return ''

    def save_dag(self, output_path: str):
        """Save DAG to file."""
        code = self.generate_dag_code()
        with open(output_path, 'w') as f:
            f.write(code)
        return output_path


class ConstructionPipelineTemplates:
    """Pre-built construction pipeline templates."""

    @staticmethod
    def bim_validation_pipeline(dag_id: str = 'bim_validation') -> ConstructionDAGBuilder:
        """Create BIM validation pipeline."""
        builder = ConstructionDAGBuilder(dag_id, schedule='@daily',
                                         tags=['bim', 'validation'])

        # Wait for file
        builder.add_sensor_task('wait_for_model', '/data/input/*.ifc')

        # Convert to Excel
        builder.add_bash_task(
            'convert_ifc',
            'IfcExporter.exe /data/input/*.ifc bbox',
            upstream=['wait_for_model']
        )

        # Validate data
        builder.add_python_task(
            'validate_data',
            'validate_bim_data',
            {'rules_file': '/config/validation_rules.xlsx'},
            upstream=['convert_ifc']
        )

        # Branch based on validation
        builder.add_branch_task(
            'check_validation',
            'check_validation_result',
            upstream=['validate_data']
        )

        # Success path
        builder.add_python_task(
            'generate_report',
            'generate_validation_report',
            upstream=['check_validation']
        )

        # Failure path
        builder.add_python_task(
            'send_alert',
            'send_validation_alert',
            upstream=['check_validation']
        )

        return builder

    @staticmethod
    def cost_estimation_pipeline(dag_id: str = 'cost_estimation') -> ConstructionDAGBuilder:
        """Create cost estimation pipeline."""
        builder = ConstructionDAGBuilder(dag_id, schedule='@weekly',
                                         tags=['cost', 'estimation'])

        # Extract BIM data
        builder.add_bash_task('extract_bim', 'RvtExporter.exe /data/model.rvt complete bbox')

        # Generate QTO
        builder.add_python_task(
            'generate_qto',
            'generate_quantity_takeoff',
            upstream=['extract_bim']
        )

        # Match with cost database
        builder.add_python_task(
            'match_costs',
            'match_cwicr_costs',
            upstream=['generate_qto']
        )

        # Calculate estimate
        builder.add_python_task(
            'calculate_estimate',
            'calculate_project_estimate',
            upstream=['match_costs']
        )

        # Generate report
        builder.add_python_task(
            'create_report',
            'create_cost_report',
            upstream=['calculate_estimate']
        )

        return builder

    @staticmethod
    def batch_conversion_pipeline(dag_id: str = 'batch_convert') -> ConstructionDAGBuilder:
        """Create batch CAD conversion pipeline."""
        builder = ConstructionDAGBuilder(dag_id, schedule='0 2 * * *',  # 2 AM daily
                                         tags=['conversion', 'batch'])

        # Scan for new files
        builder.add_python_task('scan_files', 'scan_input_folder')

        # Convert Revit files
        builder.add_bash_task(
            'convert_rvt',
            'for %%f in (/data/input/*.rvt) do RvtExporter.exe "%%f" standard',
            upstream=['scan_files']
        )

        # Convert IFC files
        builder.add_bash_task(
            'convert_ifc',
            'for %%f in (/data/input/*.ifc) do IfcExporter.exe "%%f"',
            upstream=['scan_files']
        )

        # Convert DWG files
        builder.add_bash_task(
            'convert_dwg',
            'for %%f in (/data/input/*.dwg) do DwgExporter.exe "%%f"',
            upstream=['scan_files']
        )

        # Consolidate results
        builder.add_python_task(
            'consolidate',
            'consolidate_conversion_results',
            upstream=['convert_rvt', 'convert_ifc', 'convert_dwg']
        )

        # Archive input files
        builder.add_python_task(
            'archive',
            'archive_processed_files',
            upstream=['consolidate']
        )

        return builder
```

## Quick Start

```python
# Create custom pipeline
builder = ConstructionDAGBuilder('my_pipeline', schedule='@daily')

# Add tasks
builder.add_bash_task('convert', 'RvtExporter.exe model.rvt')
builder.add_python_task('analyze', 'analyze_data', upstream=['convert'])
builder.add_python_task('report', 'create_report', upstream=['analyze'])

# Generate DAG code
code = builder.generate_dag_code()
print(code)

# Save to file
builder.save_dag('/airflow/dags/my_pipeline.py')
```

## Pipeline Templates

### 1. BIM Validation
```python
templates = ConstructionPipelineTemplates()
validation_dag = templates.bim_validation_pipeline()
validation_dag.save_dag('/airflow/dags/bim_validation.py')
```

### 2. Cost Estimation
```python
cost_dag = templates.cost_estimation_pipeline()
cost_dag.save_dag('/airflow/dags/cost_estimation.py')
```

### 3. Batch Conversion
```python
batch_dag = templates.batch_conversion_pipeline()
batch_dag.save_dag('/airflow/dags/batch_convert.py')
```

## Resources
- **DDC Book**: Chapter 4.2 - Apache Airflow Orchestration
- **Airflow Docs**: https://airflow.apache.org/docs/
