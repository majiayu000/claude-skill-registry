# API Integration Skill

```yaml
name: api-integration
version: 1.0.0
category: programming
tags: [api, integration, orcaflex, aqwa, wamit, mock-testing, automation, offshore-software]
created: 2026-01-06
updated: 2026-01-06
author: Claude
description: |
  Expert API integration for offshore engineering software (OrcaFlex, AQWA, WAMIT)
  with mock testing strategies, error handling, and automation workflows. Enables
  development and testing without requiring the actual commercial software licenses.
```

## When to Use This Skill

Use this skill when you need to:
- Integrate with OrcaFlex Python API
- Integrate with ANSYS AQWA or WAMIT
- Create mock APIs for testing without software licenses
- Build automation workflows for marine analysis software
- Develop robust error handling for API calls
- Implement batch processing with external software APIs
- Create abstraction layers over multiple analysis tools

## Core Knowledge Areas

### 1. OrcaFlex API Integration

Working with OrcaFlex Python API:

```python
import os
from pathlib import Path
from typing import Optional, Dict, List, Any
from dataclasses import dataclass
from abc import ABC, abstractmethod

# Mock OrcaFlex API for testing without license
class MockOrcFxAPI:
    """Mock OrcaFlex API for development without license."""

    class Model:
        """Mock OrcaFlex Model class."""

        def __init__(self, file_path: str = None):
            self.file_path = file_path
            self._general_data = {}
            self._objects = []
            self._is_calculated = False

        def SaveData(self, path: str):
            """Mock save data file."""
            print(f"[MOCK] Saving data to: {path}")
            self.file_path = path

        def LoadData(self, path: str):
            """Mock load data file."""
            print(f"[MOCK] Loading data from: {path}")
            self.file_path = path

        def CalculateStatics(self):
            """Mock static calculation."""
            print("[MOCK] Calculating statics...")
            self._is_calculated = True

        def RunSimulation(self):
            """Mock simulation run."""
            print("[MOCK] Running simulation...")
            self._is_calculated = True

        def SaveSimulation(self, path: str):
            """Mock save simulation."""
            print(f"[MOCK] Saving simulation to: {path}")

    @staticmethod
    def otVessel():
        return "Vessel"

    @staticmethod
    def otLine():
        return "Line"

    @staticmethod
    def ot6DBuoy():
        return "6D Buoy"

# Try to import real OrcaFlex API, fall back to mock
try:
    import OrcFxAPI
    USING_MOCK_ORCAFLEX = False
except ImportError:
    OrcFxAPI = MockOrcFxAPI
    USING_MOCK_ORCAFLEX = True
    print("Warning: OrcaFlex not available, using mock API")

@dataclass
class OrcaFlexConfig:
    """Configuration for OrcaFlex analysis."""
    model_file: Path
    output_dir: Path
    simulation_duration: float
    time_step: float
    use_variable_timestep: bool = True
    thread_count: int = 4

class OrcaFlexWrapper:
    """
    Wrapper class for OrcaFlex API with error handling and utilities.

    Example:
        >>> config = OrcaFlexConfig(
        ...     model_file=Path('mooring.dat'),
        ...     output_dir=Path('results'),
        ...     simulation_duration=3600,
        ...     time_step=0.01
        ... )
        >>> wrapper = OrcaFlexWrapper(config)
        >>> wrapper.run_analysis()
    """

    def __init__(self, config: OrcaFlexConfig):
        self.config = config
        self.model: Optional[OrcFxAPI.Model] = None
        self.is_mock = USING_MOCK_ORCAFLEX

    def load_model(self) -> None:
        """Load OrcaFlex model from file."""
        if not self.config.model_file.exists():
            raise FileNotFoundError(f"Model file not found: {self.config.model_file}")

        try:
            self.model = OrcFxAPI.Model(str(self.config.model_file))
            print(f"Loaded model: {self.config.model_file}")
        except Exception as e:
            raise RuntimeError(f"Failed to load model: {e}")

    def configure_simulation(self) -> None:
        """Configure simulation parameters."""
        if self.model is None:
            raise ValueError("Model not loaded")

        if not self.is_mock:
            # Configure real model
            general = self.model.general
            general.ImplicitUseVariableTimeStep = 'Yes' if self.config.use_variable_timestep else 'No'
            general.TargetLogSampleInterval = self.config.time_step
            general.ThreadCount = self.config.thread_count

            # Set simulation stages
            general.StageCount = 2
            general.StageDuration[0] = 100  # Build-up
            general.StageDuration[1] = self.config.simulation_duration
        else:
            print(f"[MOCK] Configured simulation: duration={self.config.simulation_duration}s")

    def run_static_analysis(self) -> bool:
        """
        Run static analysis.

        Returns:
            True if successful, False otherwise
        """
        if self.model is None:
            raise ValueError("Model not loaded")

        try:
            self.model.CalculateStatics()
            print("Static analysis complete")
            return True
        except Exception as e:
            print(f"Static analysis failed: {e}")
            return False

    def run_dynamic_analysis(self, save_results: bool = True) -> Optional[Path]:
        """
        Run dynamic analysis.

        Args:
            save_results: Whether to save simulation results

        Returns:
            Path to saved simulation file if save_results=True, else None
        """
        if self.model is None:
            raise ValueError("Model not loaded")

        try:
            self.model.RunSimulation()
            print("Dynamic analysis complete")

            if save_results:
                self.config.output_dir.mkdir(parents=True, exist_ok=True)
                sim_file = self.config.output_dir / f"{self.config.model_file.stem}.sim"
                self.model.SaveSimulation(str(sim_file))
                print(f"Results saved: {sim_file}")
                return sim_file

            return None

        except Exception as e:
            print(f"Dynamic analysis failed: {e}")
            raise

    def extract_time_series(
        self,
        object_name: str,
        variable_name: str,
        object_extra: str = 'EndA'
    ) -> tuple:
        """
        Extract time series from results.

        Args:
            object_name: Name of object
            variable_name: Variable name
            object_extra: Object extra specification

        Returns:
            Tuple of (time, values) as numpy arrays
        """
        if self.model is None:
            raise ValueError("Model not loaded")

        if self.is_mock:
            # Return mock data
            import numpy as np
            time = np.linspace(0, self.config.simulation_duration, 1000)
            values = np.random.randn(1000) * 100 + 1000  # Mock tension data
            print(f"[MOCK] Extracted time series for {object_name}.{variable_name}")
            return time, values

        # Extract from real model
        import numpy as np
        obj = self.model[object_name]

        # Handle object extra parameter
        if not self.is_mock:
            # Map string to OrcaFlex enum
            if object_extra == 'EndA':
                oe = OrcFxAPI.oeEndA
            elif object_extra == 'EndB':
                oe = OrcFxAPI.oeEndB
            else:
                oe = OrcFxAPI.oeEndA  # Default

            time = np.array(obj.TimeHistory('Time', objectExtra=oe))
            values = np.array(obj.TimeHistory(variable_name, objectExtra=oe))
        else:
            time = np.linspace(0, 3600, 1000)
            values = np.random.randn(1000) * 100 + 1000

        return time, values

    def run_analysis(self) -> Dict[str, Any]:
        """
        Complete analysis workflow.

        Returns:
            Dictionary with analysis results
        """
        # Load model
        self.load_model()

        # Configure
        self.configure_simulation()

        # Run static
        static_success = self.run_static_analysis()
        if not static_success:
            return {'status': 'FAILED', 'stage': 'static'}

        # Run dynamic
        try:
            sim_file = self.run_dynamic_analysis(save_results=True)
            return {
                'status': 'SUCCESS',
                'simulation_file': sim_file,
                'is_mock': self.is_mock
            }
        except Exception as e:
            return {
                'status': 'FAILED',
                'stage': 'dynamic',
                'error': str(e)
            }
```

### 2. Abstract API Interface Pattern

Creating abstraction layer for multiple tools:

```python
class MarineAnalysisAPI(ABC):
    """Abstract base class for marine analysis software APIs."""

    @abstractmethod
    def create_model(self, config: dict) -> Any:
        """Create new analysis model."""
        pass

    @abstractmethod
    def load_model(self, file_path: Path) -> Any:
        """Load existing model from file."""
        pass

    @abstractmethod
    def run_static_analysis(self) -> bool:
        """Run static analysis."""
        pass

    @abstractmethod
    def run_dynamic_analysis(self) -> bool:
        """Run dynamic analysis."""
        pass

    @abstractmethod
    def extract_results(self, result_type: str) -> Dict[str, Any]:
        """Extract analysis results."""
        pass

    @abstractmethod
    def cleanup(self) -> None:
        """Cleanup resources."""
        pass

class OrcaFlexAPI(MarineAnalysisAPI):
    """OrcaFlex implementation of MarineAnalysisAPI."""

    def __init__(self):
        self.model = None
        self.is_mock = USING_MOCK_ORCAFLEX

    def create_model(self, config: dict) -> OrcFxAPI.Model:
        """Create new OrcaFlex model."""
        model = OrcFxAPI.Model()

        # Configure based on config dict
        if 'water_depth' in config:
            if not self.is_mock:
                model.environment.WaterDepth = config['water_depth']

        self.model = model
        return model

    def load_model(self, file_path: Path) -> OrcFxAPI.Model:
        """Load OrcaFlex model."""
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        self.model = OrcFxAPI.Model(str(file_path))
        return self.model

    def run_static_analysis(self) -> bool:
        """Run statics."""
        if self.model is None:
            raise ValueError("No model loaded")

        try:
            self.model.CalculateStatics()
            return True
        except Exception as e:
            print(f"Static analysis error: {e}")
            return False

    def run_dynamic_analysis(self) -> bool:
        """Run dynamics."""
        if self.model is None:
            raise ValueError("No model loaded")

        try:
            self.model.RunSimulation()
            return True
        except Exception as e:
            print(f"Dynamic analysis error: {e}")
            return False

    def extract_results(self, result_type: str) -> Dict[str, Any]:
        """Extract results from model."""
        if self.model is None:
            raise ValueError("No model loaded")

        results = {}

        if result_type == 'mooring_tensions':
            # Extract mooring line tensions
            import numpy as np
            for i in range(1, 9):  # Assuming 8 mooring lines
                line_name = f"Mooring_{i}"
                try:
                    if self.is_mock:
                        time = np.linspace(0, 3600, 1000)
                        tension = np.random.randn(1000) * 200 + 1500
                    else:
                        line = self.model[line_name]
                        time = line.TimeHistory('Time')
                        tension = line.TimeHistory('Effective Tension', objectExtra=OrcFxAPI.oeEndA)

                    results[line_name] = {
                        'time': time,
                        'tension': tension,
                        'max': np.max(tension),
                        'mean': np.mean(tension)
                    }
                except:
                    pass  # Line doesn't exist

        return results

    def cleanup(self) -> None:
        """Cleanup OrcaFlex resources."""
        self.model = None

class AQWAMockAPI(MarineAnalysisAPI):
    """
    Mock AQWA API for development.

    Note: Real ANSYS AQWA integration would use ANSYS Workbench scripting or
    ANSYS ACT (Application Customization Toolkit).
    """

    def __init__(self):
        self.project = None
        self.analysis_complete = False

    def create_model(self, config: dict) -> Any:
        """Create new AQWA model (mock)."""
        print("[MOCK AQWA] Creating new model...")
        self.project = {
            'config': config,
            'geometry': None,
            'mesh': None,
            'hydrodynamic_data': None
        }
        return self.project

    def load_model(self, file_path: Path) -> Any:
        """Load AQWA model (mock)."""
        print(f"[MOCK AQWA] Loading model from: {file_path}")
        self.project = {'loaded_from': str(file_path)}
        return self.project

    def run_static_analysis(self) -> bool:
        """Run hydrostatic analysis (mock)."""
        print("[MOCK AQWA] Running hydrostatic analysis...")
        import time
        time.sleep(0.5)  # Simulate computation
        return True

    def run_dynamic_analysis(self) -> bool:
        """Run hydrodynamic analysis (mock)."""
        print("[MOCK AQWA] Running hydrodynamic analysis...")
        import time
        time.sleep(1.0)  # Simulate computation
        self.analysis_complete = True
        return True

    def extract_results(self, result_type: str) -> Dict[str, Any]:
        """Extract AQWA results (mock)."""
        import numpy as np

        if result_type == 'rao':
            # Mock RAO data
            frequencies = np.linspace(0.1, 2.0, 50)
            rao_surge = np.exp(-((frequencies - 0.5)**2) / 0.1) * 2.0
            rao_heave = np.exp(-((frequencies - 0.8)**2) / 0.1) * 1.5

            return {
                'frequencies': frequencies,
                'rao_surge': rao_surge,
                'rao_heave': rao_heave
            }

        elif result_type == 'added_mass':
            # Mock added mass matrix
            return {
                'added_mass': np.random.rand(6, 6) * 1e6,
                'damping': np.random.rand(6, 6) * 1e5
            }

        return {}

    def cleanup(self) -> None:
        """Cleanup AQWA resources (mock)."""
        self.project = None
        self.analysis_complete = False

class APIFactory:
    """Factory for creating marine analysis API instances."""

    @staticmethod
    def create_api(api_type: str) -> MarineAnalysisAPI:
        """
        Create API instance.

        Args:
            api_type: 'orcaflex', 'aqwa', 'wamit', etc.

        Returns:
            API instance

        Example:
            >>> api = APIFactory.create_api('orcaflex')
            >>> api.load_model(Path('model.dat'))
            >>> api.run_dynamic_analysis()
        """
        if api_type.lower() == 'orcaflex':
            return OrcaFlexAPI()
        elif api_type.lower() == 'aqwa':
            return AQWAMockAPI()
        elif api_type.lower() == 'wamit':
            # Would implement WAMIT API here
            raise NotImplementedError("WAMIT API not implemented")
        else:
            raise ValueError(f"Unknown API type: {api_type}")
```

### 3. Mock Testing Strategy

Testing without software licenses:

```python
import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path

class TestOrcaFlexIntegration:
    """Test suite for OrcaFlex integration using mocks."""

    @pytest.fixture
    def mock_orcaflex_model(self):
        """Create mock OrcaFlex model for testing."""
        mock_model = Mock()
        mock_model.general = Mock()
        mock_model.environment = Mock()
        mock_model.CalculateStatics = Mock()
        mock_model.RunSimulation = Mock()
        mock_model.SaveSimulation = Mock()
        return mock_model

    def test_load_model(self, mock_orcaflex_model, tmp_path):
        """Test loading OrcaFlex model."""
        # Create dummy model file
        model_file = tmp_path / "test_model.dat"
        model_file.write_text("dummy model")

        config = OrcaFlexConfig(
            model_file=model_file,
            output_dir=tmp_path / "results",
            simulation_duration=3600,
            time_step=0.1
        )

        wrapper = OrcaFlexWrapper(config)

        with patch('OrcFxAPI.Model', return_value=mock_orcaflex_model):
            wrapper.load_model()
            assert wrapper.model is not None

    def test_run_static_analysis(self, mock_orcaflex_model, tmp_path):
        """Test static analysis execution."""
        config = OrcaFlexConfig(
            model_file=tmp_path / "test.dat",
            output_dir=tmp_path / "results",
            simulation_duration=3600,
            time_step=0.1
        )

        wrapper = OrcaFlexWrapper(config)
        wrapper.model = mock_orcaflex_model

        success = wrapper.run_static_analysis()

        assert success is True
        mock_orcaflex_model.CalculateStatics.assert_called_once()

    def test_run_dynamic_analysis(self, mock_orcaflex_model, tmp_path):
        """Test dynamic analysis execution."""
        config = OrcaFlexConfig(
            model_file=tmp_path / "test.dat",
            output_dir=tmp_path / "results",
            simulation_duration=3600,
            time_step=0.1
        )

        wrapper = OrcaFlexWrapper(config)
        wrapper.model = mock_orcaflex_model

        sim_file = wrapper.run_dynamic_analysis(save_results=True)

        mock_orcaflex_model.RunSimulation.assert_called_once()
        mock_orcaflex_model.SaveSimulation.assert_called_once()
        assert sim_file is not None

    def test_api_factory(self):
        """Test API factory pattern."""
        api = APIFactory.create_api('orcaflex')
        assert isinstance(api, OrcaFlexAPI)

        api_aqwa = APIFactory.create_api('aqwa')
        assert isinstance(api_aqwa, AQWAMockAPI)

        with pytest.raises(ValueError):
            APIFactory.create_api('unknown_api')

    def test_mock_time_series_extraction(self, tmp_path):
        """Test time series extraction with mock."""
        config = OrcaFlexConfig(
            model_file=tmp_path / "test.dat",
            output_dir=tmp_path / "results",
            simulation_duration=3600,
            time_step=0.1
        )

        wrapper = OrcaFlexWrapper(config)
        wrapper.model = Mock()  # Use mock model
        wrapper.is_mock = True

        time, values = wrapper.extract_time_series(
            'Mooring_1',
            'Effective Tension'
        )

        assert len(time) > 0
        assert len(values) > 0
        assert len(time) == len(values)

def test_abstract_api_interface():
    """Test abstract API interface pattern."""

    # Test OrcaFlex API
    api = OrcaFlexAPI()
    model = api.create_model({'water_depth': 1000})
    assert model is not None

    # Test AQWA Mock API
    api_aqwa = AQWAMockAPI()
    project = api_aqwa.create_model({'water_depth': 1000})
    assert project is not None

    success = api_aqwa.run_dynamic_analysis()
    assert success is True

    results = api_aqwa.extract_results('rao')
    assert 'frequencies' in results
    assert 'rao_surge' in results
```

### 4. Error Handling and Retry Logic

Robust error handling for API calls:

```python
import time
from functools import wraps
from typing import Callable, Any, Optional

def retry_on_failure(
    max_retries: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    exceptions: tuple = (Exception,)
) -> Callable:
    """
    Decorator for retrying function calls on failure.

    Args:
        max_retries: Maximum number of retry attempts
        delay: Initial delay between retries [s]
        backoff: Backoff multiplier for delay
        exceptions: Tuple of exceptions to catch

    Example:
        >>> @retry_on_failure(max_retries=3, delay=1.0)
        ... def unstable_api_call():
        ...     # Make API call that might fail
        ...     pass
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            current_delay = delay

            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if attempt == max_retries - 1:
                        # Last attempt failed
                        raise

                    print(f"Attempt {attempt + 1} failed: {e}")
                    print(f"Retrying in {current_delay}s...")
                    time.sleep(current_delay)
                    current_delay *= backoff

            return None

        return wrapper
    return decorator

class RobustAPIWrapper:
    """API wrapper with comprehensive error handling."""

    def __init__(self, api: MarineAnalysisAPI):
        self.api = api
        self.last_error: Optional[Exception] = None

    @retry_on_failure(max_retries=3, delay=2.0)
    def safe_run_static(self) -> bool:
        """Run static analysis with retry logic."""
        try:
            result = self.api.run_static_analysis()
            return result
        except Exception as e:
            self.last_error = e
            print(f"Static analysis error: {e}")
            raise

    @retry_on_failure(max_retries=3, delay=5.0)
    def safe_run_dynamic(self) -> bool:
        """Run dynamic analysis with retry logic."""
        try:
            result = self.api.run_dynamic_analysis()
            return result
        except Exception as e:
            self.last_error = e
            print(f"Dynamic analysis error: {e}")
            raise

    def safe_extract_results(
        self,
        result_type: str,
        fallback_value: Any = None
    ) -> Any:
        """Extract results with error handling."""
        try:
            return self.api.extract_results(result_type)
        except Exception as e:
            self.last_error = e
            print(f"Result extraction error: {e}")
            return fallback_value
```

### 5. Batch Processing with APIs

Automate multiple analyses:

```python
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict
import pandas as pd

class BatchAnalysisRunner:
    """
    Run batch analyses using marine analysis APIs.

    Example:
        >>> parameter_sets = [
        ...     {'Hs': 5.0, 'Tp': 10.0},
        ...     {'Hs': 7.5, 'Tp': 12.0},
        ...     {'Hs': 10.0, 'Tp': 14.0}
        ... ]
        >>> runner = BatchAnalysisRunner(
        ...     api_type='orcaflex',
        ...     base_model=Path('base.dat')
        ... )
        >>> results = runner.run_batch(parameter_sets)
    """

    def __init__(
        self,
        api_type: str,
        base_model: Path,
        output_dir: Path = Path('batch_results')
    ):
        self.api_type = api_type
        self.base_model = base_model
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def run_single_analysis(
        self,
        run_id: int,
        parameters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Run single analysis with given parameters.

        Args:
            run_id: Unique run identifier
            parameters: Analysis parameters

        Returns:
            Results dictionary
        """
        print(f"Running analysis {run_id} with parameters: {parameters}")

        try:
            # Create API instance
            api = APIFactory.create_api(self.api_type)

            # Load base model
            api.load_model(self.base_model)

            # Apply parameters (implementation depends on API)
            # For OrcaFlex example:
            if self.api_type == 'orcaflex' and not USING_MOCK_ORCAFLEX:
                if 'Hs' in parameters:
                    api.model.environment.WaveHs = parameters['Hs']
                if 'Tp' in parameters:
                    api.model.environment.WaveTp = parameters['Tp']

            # Run analyses
            static_success = api.run_static_analysis()
            if not static_success:
                return {
                    'run_id': run_id,
                    'status': 'FAILED',
                    'stage': 'static',
                    'parameters': parameters
                }

            dynamic_success = api.run_dynamic_analysis()
            if not dynamic_success:
                return {
                    'run_id': run_id,
                    'status': 'FAILED',
                    'stage': 'dynamic',
                    'parameters': parameters
                }

            # Extract results
            results = api.extract_results('mooring_tensions')

            # Cleanup
            api.cleanup()

            return {
                'run_id': run_id,
                'status': 'SUCCESS',
                'parameters': parameters,
                'results': results
            }

        except Exception as e:
            return {
                'run_id': run_id,
                'status': 'FAILED',
                'error': str(e),
                'parameters': parameters
            }

    def run_batch(
        self,
        parameter_sets: List[Dict[str, Any]],
        parallel: bool = False,
        max_workers: int = 4
    ) -> List[Dict[str, Any]]:
        """
        Run batch analyses.

        Args:
            parameter_sets: List of parameter dictionaries
            parallel: Whether to run in parallel
            max_workers: Maximum parallel workers

        Returns:
            List of results dictionaries
        """
        results = []

        if parallel:
            # Run in parallel
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures = {
                    executor.submit(
                        self.run_single_analysis,
                        i + 1,
                        params
                    ): i
                    for i, params in enumerate(parameter_sets)
                }

                for future in as_completed(futures):
                    result = future.result()
                    results.append(result)
        else:
            # Run sequentially
            for i, params in enumerate(parameter_sets):
                result = self.run_single_analysis(i + 1, params)
                results.append(result)

        # Save results summary
        self._save_results_summary(results)

        return results

    def _save_results_summary(self, results: List[Dict[str, Any]]) -> None:
        """Save batch results summary to CSV."""
        summary_data = []

        for result in results:
            row = {
                'run_id': result['run_id'],
                'status': result['status'],
                **result.get('parameters', {})
            }

            # Add result metrics if available
            if 'results' in result:
                # Example: extract max tensions
                for line_name, line_results in result['results'].items():
                    row[f'{line_name}_max'] = line_results.get('max', None)

            summary_data.append(row)

        df = pd.DataFrame(summary_data)
        summary_file = self.output_dir / 'batch_results_summary.csv'
        df.to_csv(summary_file, index=False)
        print(f"Results summary saved: {summary_file}")
```

## Complete Examples

### Example 1: Multi-Tool Integration Workflow

```python
from pathlib import Path
import numpy as np

def multi_tool_analysis_workflow(
    geometry_file: Path,
    analysis_config: dict,
    output_dir: Path
) -> dict:
    """
    Complete workflow using multiple marine analysis tools.

    Workflow:
    1. Generate hydrodynamic database with AQWA
    2. Import into OrcaFlex for dynamic analysis
    3. Extract and post-process results

    Example:
        >>> config = {
        ...     'water_depth': 1200,
        ...     'wave_height': 8.0,
        ...     'wave_period': 13.0,
        ...     'current_speed': 1.0
        ... }
        >>> results = multi_tool_analysis_workflow(
        ...     geometry_file=Path('vessel.igs'),
        ...     analysis_config=config,
        ...     output_dir=Path('integrated_analysis')
        ... )
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    print("="*70)
    print("MULTI-TOOL ANALYSIS WORKFLOW")
    print("="*70)

    # Step 1: AQWA Hydrodynamic Analysis
    print("\n[Step 1/3] Running AQWA hydrodynamic analysis...")

    aqwa_api = APIFactory.create_api('aqwa')

    # Create AQWA model
    aqwa_config = {
        'geometry': geometry_file,
        'water_depth': analysis_config['water_depth'],
        'frequency_range': (0.1, 2.0),
        'n_frequencies': 50
    }

    aqwa_api.create_model(aqwa_config)

    # Run hydrodynamic analysis
    aqwa_api.run_dynamic_analysis()

    # Extract RAOs and hydrodynamic coefficients
    rao_data = aqwa_api.extract_results('rao')
    hydro_coeffs = aqwa_api.extract_results('added_mass')

    print("AQWA analysis complete")
    print(f"  RAO frequencies: {len(rao_data['frequencies'])}")

    # Step 2: Create OrcaFlex Model with AQWA Data
    print("\n[Step 2/3] Creating OrcaFlex model...")

    orcaflex_api = APIFactory.create_api('orcaflex')

    # Create model
    orcaflex_config = {
        'water_depth': analysis_config['water_depth'],
        'wave_height': analysis_config['wave_height'],
        'wave_period': analysis_config['wave_period'],
        'current_speed': analysis_config['current_speed']
    }

    orcaflex_api.create_model(orcaflex_config)

    # In real implementation, would import AQWA hydrodynamic database
    # For mock, we proceed with standard analysis

    # Run OrcaFlex analysis
    print("\n[Step 3/3] Running OrcaFlex dynamic analysis...")

    robust_wrapper = RobustAPIWrapper(orcaflex_api)

    static_success = robust_wrapper.safe_run_static()
    if not static_success:
        return {'status': 'FAILED', 'stage': 'static'}

    dynamic_success = robust_wrapper.safe_run_dynamic()
    if not dynamic_success:
        return {'status': 'FAILED', 'stage': 'dynamic'}

    # Extract results
    mooring_results = robust_wrapper.safe_extract_results(
        'mooring_tensions',
        fallback_value={}
    )

    print("\nOrcaFlex analysis complete")

    # Cleanup
    aqwa_api.cleanup()
    orcaflex_api.cleanup()

    # Combine results
    final_results = {
        'status': 'SUCCESS',
        'aqwa_results': {
            'rao': rao_data,
            'hydrodynamic_coefficients': hydro_coeffs
        },
        'orcaflex_results': {
            'mooring_tensions': mooring_results
        }
    }

    print("\n" + "="*70)
    print("WORKFLOW COMPLETE")
    print("="*70)

    return final_results

# Run workflow
geometry_file = Path('fpso_geometry.igs')
config = {
    'water_depth': 1200,
    'wave_height': 8.0,
    'wave_period': 13.0,
    'current_speed': 1.0
}

workflow_results = multi_tool_analysis_workflow(
    geometry_file=geometry_file,
    analysis_config=config,
    output_dir=Path('integrated_analysis_results')
)

print(f"\nFinal status: {workflow_results['status']}")
```

## Best Practices

### 1. API Availability Checking

```python
def check_api_availability(api_type: str) -> tuple[bool, str]:
    """
    Check if API is available and return status.

    Args:
        api_type: Type of API to check

    Returns:
        Tuple of (is_available, message)

    Example:
        >>> available, msg = check_api_availability('orcaflex')
        >>> if available:
        ...     print("OrcaFlex API is ready")
        >>> else:
        ...     print(f"Using mock: {msg}")
    """
    if api_type == 'orcaflex':
        try:
            import OrcFxAPI
            return True, "OrcaFlex API available"
        except ImportError:
            return False, "OrcaFlex not installed, using mock API"

    elif api_type == 'aqwa':
        # AQWA typically accessed via ANSYS Workbench
        # Check if ANSYS is available
        return False, "AQWA integration via ANSYS Workbench (mock mode)"

    else:
        return False, f"Unknown API type: {api_type}"
```

### 2. Configuration Management

```python
import yaml
from dataclasses import dataclass, asdict

@dataclass
class APIConfiguration:
    """Configuration for API integration."""
    api_type: str
    model_file: Optional[Path]
    output_dir: Path
    simulation_settings: dict
    retry_settings: dict

    def save_to_yaml(self, file_path: Path) -> None:
        """Save configuration to YAML file."""
        with open(file_path, 'w') as f:
            yaml.dump(asdict(self), f, default_flow_style=False)

    @classmethod
    def load_from_yaml(cls, file_path: Path) -> 'APIConfiguration':
        """Load configuration from YAML file."""
        with open(file_path) as f:
            data = yaml.safe_load(f)
        # Convert Path strings back to Path objects
        if 'model_file' in data and data['model_file']:
            data['model_file'] = Path(data['model_file'])
        data['output_dir'] = Path(data['output_dir'])
        return cls(**data)
```

### 3. Logging and Monitoring

```python
import logging
from datetime import datetime

def setup_api_logging(
    log_dir: Path,
    api_type: str
) -> logging.Logger:
    """
    Setup logging for API operations.

    Args:
        log_dir: Directory for log files
        api_type: Type of API

    Returns:
        Configured logger
    """
    log_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_file = log_dir / f"{api_type}_api_{timestamp}.log"

    logger = logging.getLogger(f"{api_type}_api")
    logger.setLevel(logging.DEBUG)

    # File handler
    fh = logging.FileHandler(log_file)
    fh.setLevel(logging.DEBUG)

    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger
```

## Resources

### OrcaFlex API

- **Documentation**: OrcFxAPI Python documentation (in OrcaFlex installation)
- **Examples**: OrcaFlex → Examples → Python folder
- **Support**: support@orcina.com

### ANSYS AQWA

- **ANSYS ACT**: Application Customization Toolkit for scripting
- **PyAnsys**: https://github.com/pyansys
- **Documentation**: ANSYS Help → AQWA → Programmer's Guide

### Testing

- **pytest**: https://docs.pytest.org/
- **unittest.mock**: https://docs.python.org/3/library/unittest.mock.html
- **Mock Testing Best Practices**: Various online resources

### Python API Design

- **PEP 8**: Python style guide
- **Design Patterns**: Gang of Four patterns
- **Abstract Base Classes**: Python ABC module documentation

---

**Use this skill for:** Expert API integration with marine analysis software, mock testing strategies, and automation workflows with robust error handling.
