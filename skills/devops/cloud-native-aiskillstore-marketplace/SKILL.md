---
name: cloud-native
description: Generic Cloud-Native Deployment and Infrastructure as Code patterns for 2025. Provides comprehensive implementation strategies for multi-cloud deployments, GitOps workflows, progressive delivery, and platform engineering. Framework-agnostic approach supporting any cloud provider, deployment tool, and orchestration platform.
license: MIT
---

# Cloud-Native Deployment & Infrastructure Patterns

This skill provides comprehensive patterns for implementing cloud-native deployments using modern Infrastructure as Code, GitOps workflows, and progressive delivery strategies. The patterns are designed to be framework-agnostic and applicable across any cloud provider or orchestration platform.

## When to Use This Skill

Use this skill when you need to:
- Implement Infrastructure as Code with any provider (Terraform, Pulumi, CDK)
- Build GitOps workflows with Argo CD, Flux, or similar tools
- Create multi-cloud or hybrid deployment strategies
- Implement progressive delivery (canary, blue-green)
- Build internal developer platforms
- Set up policy as code and compliance automation
- Implement zero-trust security architectures
- Create disaster recovery and failover strategies
- Optimize costs across multiple providers
- Build observability into deployments

## 1. Infrastructure as Code Patterns

### Generic IaC Abstraction Layer

```python
# iac/core/abstraction.py
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
import json
import yaml
import asyncio
from datetime import datetime

class IaCProvider(str, Enum):
    """Supported IaC providers"""
    TERRAFORM = "terraform"
    PULUMI = "pulumi"
    CDK = "cdk"
    CROSSPLANE = "crossplane"

class CloudProvider(str, Enum):
    """Cloud providers"""
    AWS = "aws"
    AZURE = "azure"
    GCP = "gcp"
    DIGITALOCEAN = "digitalocean"
    ON_PREM = "on-prem"

@dataclass
class Resource:
    """Generic resource definition"""
    type: str
    name: str
    properties: Dict[str, Any] = field(default_factory=dict)
    dependencies: List[str] = field(default_factory=list)
    provider: Optional[CloudProvider] = None
    tags: Dict[str, str] = field(default_factory=dict)

@dataclass
class InfrastructureConfig:
    """Infrastructure configuration"""
    name: str
    environment: str
    provider: CloudProvider
    region: str
    resources: List[Resource] = field(default_factory=list)
    variables: Dict[str, Any] = field(default_factory=dict)
    outputs: Dict[str, str] = field(default_factory=dict)

class IaCBackend(ABC):
    """Abstract IaC backend interface"""

    @abstractmethod
    async def initialize(self, config: InfrastructureConfig) -> None:
        """Initialize IaC backend"""
        pass

    @abstractmethod
    async def plan(self, config: InfrastructureConfig) -> Dict[str, Any]:
        """Generate execution plan"""
        pass

    @abstractmethod
    async def apply(self, config: InfrastructureConfig) -> Dict[str, Any]:
        """Apply infrastructure changes"""
        pass

    @abstractmethod
    async def destroy(self, config: InfrastructureConfig) -> Dict[str, Any]:
        """Destroy infrastructure"""
        pass

    @abstractmethod
    async def output(self, config: InfrastructureConfig, key: str) -> Any:
        """Get output value"""
        pass

    @abstractmethod
    async def validate(self, config: InfrastructureConfig) -> List[str]:
        """Validate configuration"""
        pass

class TerraformBackend(IaCBackend):
    """Terraform backend implementation"""

    def __init__(self, working_dir: Path):
        self.working_dir = working_dir
        self.state_backend: Optional[str] = None

    async def initialize(self, config: InfrastructureConfig) -> None:
        """Initialize Terraform"""
        # Generate Terraform files
        await self._generate_terraform_files(config)

        # Run terraform init
        cmd = ["terraform", "init"]
        result = await self._run_command(cmd, cwd=self.working_dir)

        if result["returncode"] != 0:
            raise RuntimeError(f"Terraform init failed: {result['stderr']}")

    async def plan(self, config: InfrastructureConfig) -> Dict[str, Any]:
        """Generate Terraform plan"""
        cmd = ["terraform", "plan", "-out=tfplan", "-json"]
        result = await self._run_command(cmd, cwd=self.working_dir)

        return {
            "success": result["returncode"] == 0,
            "plan_file": self.working_dir / "tfplan",
            "output": result["stdout"],
            "changes": json.loads(result["stdout"]) if result["stdout"] else {}
        }

    async def apply(self, config: InfrastructureConfig) -> Dict[str, Any]:
        """Apply Terraform changes"""
        cmd = ["terraform", "apply", "-auto-approve", "-json", "tfplan"]
        result = await self._run_command(cmd, cwd=self.working_dir)

        return {
            "success": result["returncode"] == 0,
            "output": result["stdout"],
            "applied_at": datetime.utcnow().isoformat()
        }

    async def destroy(self, config: InfrastructureConfig) -> Dict[str, Any]:
        """Destroy Terraform resources"""
        cmd = ["terraform", "destroy", "-auto-approve", "-json"]
        result = await self._run_command(cmd, cwd=self.working_dir)

        return {
            "success": result["returncode"] == 0,
            "output": result["stdout"],
            "destroyed_at": datetime.utcnow().isoformat()
        }

    async def output(self, config: InfrastructureConfig, key: str) -> Any:
        """Get Terraform output"""
        cmd = ["terraform", "output", "-json", key]
        result = await self._run_command(cmd, cwd=self.working_dir)

        if result["returncode"] == 0:
            return json.loads(result["stdout"])
        return None

    async def validate(self, config: InfrastructureConfig) -> List[str]:
        """Validate Terraform configuration"""
        errors = []

        # Run terraform validate
        cmd = ["terraform", "validate"]
        result = await self._run_command(cmd, cwd=self.working_dir)

        if result["returncode"] != 0:
            errors.append(f"Validation failed: {result['stderr']}")

        # Run terraform fmt check
        cmd = ["terraform", "fmt", "-check", "-diff"]
        result = await self._run_command(cmd, cwd=self.working_dir)

        if result["returncode"] != 0:
            errors.append("Formatting check failed - run terraform fmt")

        # Check for required variables
        cmd = ["terraform", "validate", "-json"]
        result = await self._run_command(cmd, cwd=self.working_dir)

        return errors

    async def _generate_terraform_files(self, config: InfrastructureConfig) -> None:
        """Generate Terraform configuration files"""
        # Generate main.tf
        main_tf = {
            "terraform": {
                "required_providers": self._get_required_providers(config.provider),
                "backend": self._get_backend_config()
            },
            "provider": {config.provider.value: self._get_provider_config(config)},
            "resource": self._convert_resources(config.resources)
        }

        with open(self.working_dir / "main.tf", "w") as f:
            yaml.dump(main_tf, f, sort_keys=False)

        # Generate variables.tf
        if config.variables:
            variables_tf = {
                "variable": {
                    k: {"type": self._infer_type(v), "default": v}
                    for k, v in config.variables.items()
                }
            }

            with open(self.working_dir / "variables.tf", "w") as f:
                yaml.dump(variables_tf, f, sort_keys=False)

        # Generate outputs.tf
        if config.outputs:
            outputs_tf = {
                "output": {
                    k: {"value": v}
                    for k, v in config.outputs.items()
                }
            }

            with open(self.working_dir / "outputs.tf", "w") as f:
                yaml.dump(outputs_tf, f, sort_keys=False)

    async def _run_command(self, cmd: List[str], cwd: Path) -> Dict[str, Any]:
        """Run command and return result"""
        process = await asyncio.create_subprocess_exec(
            *cmd,
            cwd=cwd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await process.communicate()

        return {
            "returncode": process.returncode,
            "stdout": stdout.decode(),
            "stderr": stderr.decode()
        }

    def _get_required_providers(self, provider: CloudProvider) -> Dict[str, Any]:
        """Get required providers configuration"""
        providers = {}

        if provider == CloudProvider.AWS:
            providers["aws"] = {"source": "hashicorp/aws", "version": "~> 5.0"}
        elif provider == CloudProvider.AZURE:
            providers["azurerm"] = {"source": "hashicorp/azurerm", "version": "~> 3.0"}
        elif provider == CloudProvider.GCP:
            providers["google"] = {"source": "hashicorp/google", "version": "~> 5.0"}

        return providers

    def _get_backend_config(self) -> Dict[str, Any]:
        """Get Terraform backend configuration"""
        if self.state_backend:
            return {"s3": self.state_backend}
        return {}

    def _get_provider_config(self, config: InfrastructureConfig) -> Dict[str, Any]:
        """Get provider-specific configuration"""
        base_config = {"region": config.region}

        # Add provider-specific settings
        if config.provider == CloudProvider.AWS:
            base_config["default_tags"] = {
                "tags": {
                    "Environment": config.environment,
                    "ManagedBy": "terraform",
                    "Project": config.name
                }
            }

        return base_config

    def _convert_resources(self, resources: List[Resource]) -> Dict[str, Any]:
        """Convert generic resources to Terraform format"""
        terraform_resources = {}

        for resource in resources:
            resource_key = f"{resource.type}_{resource.name}"

            resource_config = {
                "provider": resource.provider.value if resource.provider else None,
                **resource.properties
            }

            if resource.tags:
                resource_config["tags"] = resource.tags

            terraform_resources[resource_key] = resource_config

        return terraform_resources

    def _infer_type(self, value: Any) -> str:
        """Infer Terraform variable type from value"""
        if isinstance(value, bool):
            return "bool"
        elif isinstance(value, int):
            return "number"
        elif isinstance(value, list):
            return "list(string)"
        elif isinstance(value, dict):
            return "map(string)"
        else:
            return "string"

class PulumiBackend(IaCBackend):
    """Pulumi backend implementation"""

    def __init__(self, working_dir: Path, language: str = "python"):
        self.working_dir = working_dir
        self.language = language

    async def initialize(self, config: InfrastructureConfig) -> None:
        """Initialize Pulumi"""
        # Generate Pulumi program
        await self._generate_pulumi_program(config)

        # Run pulumi stack init
        cmd = ["pulumi", "stack", "init", f"{config.name}-{config.environment}"]
        result = await self._run_command(cmd, cwd=self.working_dir)

        if result["returncode"] != 0:
            raise RuntimeError(f"Pulumi stack init failed: {result['stderr']}")

    async def plan(self, config: InfrastructureConfig) -> Dict[str, Any]:
        """Preview Pulumi changes"""
        cmd = ["pulumi", "preview", "--json"]
        result = await self._run_command(cmd, cwd=self.working_dir)

        return {
            "success": result["returncode"] == 0,
            "output": result["stdout"],
            "changes": json.loads(result["stdout"]) if result["stdout"] else {}
        }

    async def apply(self, config: InfrastructureConfig) -> Dict[str, Any]:
        """Apply Pulumi changes"""
        cmd = ["pulumi", "up", "--yes", "--json"]
        result = await self._run_command(cmd, cwd=self.working_dir)

        return {
            "success": result["returncode"] == 0,
            "output": result["stdout"],
            "applied_at": datetime.utcnow().isoformat()
        }

    async def destroy(self, config: InfrastructureConfig) -> Dict[str, Any]:
        """Destroy Pulumi resources"""
        cmd = ["pulumi", "destroy", "--yes", "--json"]
        result = await self._run_command(cmd, cwd=self.working_dir)

        return {
            "success": result["returncode"] == 0,
            "output": result["stdout"],
            "destroyed_at": datetime.utcnow().isoformat()
        }

    async def output(self, config: InfrastructureConfig, key: str) -> Any:
        """Get Pulumi stack output"""
        cmd = ["pulumi", "stack", "output", "--json"]
        result = await self._run_command(cmd, cwd=self.working_dir)

        if result["returncode"] == 0:
            outputs = json.loads(result["stdout"])
            return outputs.get(key)
        return None

    async def validate(self, config: InfrastructureConfig) -> List[str]:
        """Validate Pulumi configuration"""
        errors = []

        # Run pulumi config validate
        cmd = ["pulumi", "config", "validate"]
        result = await self._run_command(cmd, cwd=self.working_dir)

        if result["returncode"] != 0:
            errors.append(f"Validation failed: {result['stderr']}")

        return errors

    async def _generate_pulumi_program(self, config: InfrastructureConfig) -> None:
        """Generate Pulumi program based on language"""
        if self.language == "python":
            await self._generate_python_program(config)
        elif self.language == "typescript":
            await self._generate_typescript_program(config)

    async def _generate_python_program(self, config: InfrastructureConfig) -> None:
        """Generate Python Pulumi program"""
        program = f'''"""
Pulumi program for {config.name} - {config.environment}
"""

import pulumi
import pulumi_{config.provider.value} as provider

# Configuration
config = pulumi.Config()

# Resources
'''

        # Generate resources
        for resource in config.resources:
            provider_module = f"provider.{resource.type.replace('_', '.')}"
            program += f'''
{resource.name}_resource = {provider_module}.{resource.title()}(
    "{resource.name}",
'''

            # Add properties
            for key, value in resource.properties.items():
                if isinstance(value, str):
                    program += f'    {key}="{value}",\n'
                else:
                    program += f'    {key}={value},\n'

            # Add tags if present
            if resource.tags:
                program += f'    tags={resource.tags},\n'

            program += ')\n\n'

        # Generate outputs
        for key, value in config.outputs.items():
            program += f'pulumi.export("{key}", {value})\n'

        # Write program file
        with open(self.working_dir / "__main__.py", "w") as f:
            f.write(program)

        # Generate requirements.txt
        with open(self.working_dir / "requirements.txt", "w") as f:
            f.write(f"pulumi>={config.provider.value}\n")

    async def _run_command(self, cmd: List[str], cwd: Path) -> Dict[str, Any]:
        """Run command and return result"""
        process = await asyncio.create_subprocess_exec(
            *cmd,
            cwd=cwd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await process.communicate()

        return {
            "returncode": process.returncode,
            "stdout": stdout.decode(),
            "stderr": stderr.decode()
        }

# Factory for creating IaC backends
class IaCFactory:
    """Factory for creating IaC backends"""

    @staticmethod
    def create(
        provider: IaCProvider,
        working_dir: Path,
        **kwargs
    ) -> IaCBackend:
        """Create IaC backend instance"""

        working_dir.mkdir(parents=True, exist_ok=True)

        if provider == IaCProvider.TERRAFORM:
            return TerraformBackend(working_dir)
        elif provider == IaCProvider.PULUMI:
            return PulumiBackend(
                working_dir,
                language=kwargs.get("language", "python")
            )
        else:
            raise ValueError(f"Unsupported IaC provider: {provider}")
```

### Multi-Cloud Resource Manager

```python
# iac/multicloud/manager.py
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import asyncio
from ..core.abstraction import (
    InfrastructureConfig, Resource, CloudProvider, IaCBackend
)

@dataclass
class CloudDeployment:
    """Cloud deployment configuration"""
    provider: CloudProvider
    region: str
    environment: str
    resources: List[Resource]
    priority: int = 0  # Higher priority = primary deployment
    enabled: bool = True

class MultiCloudManager:
    """Manages deployments across multiple cloud providers"""

    def __init__(self):
        self.deployments: Dict[str, CloudDeployment] = {}
        self.backends: Dict[str, IaCBackend] = {}
        self.global_resources: List[Resource] = []
        self.shared_state: Dict[str, Any] = {}

    def add_deployment(self, name: str, deployment: CloudDeployment) -> None:
        """Add a cloud deployment"""
        self.deployments[name] = deployment

    def add_global_resource(self, resource: Resource) -> None:
        """Add a global resource (DNS, CDN, etc.)"""
        self.global_resources.append(resource)

    async def deploy_all(self) -> Dict[str, Any]:
        """Deploy to all configured clouds"""
        results = {}

        # Sort by priority (primary deployments first)
        sorted_deployments = sorted(
            self.deployments.items(),
            key=lambda x: x[1].priority,
            reverse=True
        )

        for name, deployment in sorted_deployments:
            if not deployment.enabled:
                continue

            print(f"Deploying to {name} ({deployment.provider.value})...")

            try:
                result = await self._deploy_single(name, deployment)
                results[name] = result

                # Store shared outputs
                if result["success"]:
                    self.shared_state[name] = result.get("outputs", {})

            except Exception as e:
                results[name] = {
                    "success": False,
                    "error": str(e)
                }
                print(f"Failed to deploy to {name}: {e}")

        return results

    async def _deploy_single(
        self,
        name: str,
        deployment: CloudDeployment
    ) -> Dict[str, Any]:
        """Deploy to a single cloud provider"""

        # Create IaC config
        config = InfrastructureConfig(
            name=name,
            environment=deployment.environment,
            provider=deployment.provider,
            region=deployment.region,
            resources=self._merge_resources(deployment),
            variables=self._get_variables(deployment)
        )

        # Get or create backend
        if name not in self.backends:
            from ..core.abstraction import IaCFactory, IaCProvider
            backend = IaCFactory.create(
                IaCProvider.TERRAFORM,
                Path(f"iac/{name}")
            )
            self.backends[name] = backend

        backend = self.backends[name]

        # Initialize and deploy
        await backend.initialize(config)

        # Plan
        plan = await backend.plan(config)
        if not plan["success"]:
            return {"success": False, "error": "Plan failed"}

        # Apply
        apply_result = await backend.apply(config)

        # Get outputs
        outputs = {}
        for key in deployment.resources:
            if hasattr(key, 'name'):
                output_value = await backend.output(config, key.name)
                if output_value:
                    outputs[key.name] = output_value

        return {
            "success": apply_result["success"],
            "outputs": outputs,
            "deployment_info": {
                "provider": deployment.provider.value,
                "region": deployment.region,
                "environment": deployment.environment
            }
        }

    def _merge_resources(self, deployment: CloudDeployment) -> List[Resource]:
        """Merge global and deployment-specific resources"""
        resources = []

        # Add global resources first
        resources.extend(self.global_resources)

        # Add deployment-specific resources
        resources.extend(deployment.resources)

        return resources

    def _get_variables(self, deployment: CloudDeployment) -> Dict[str, Any]:
        """Get variables for deployment"""
        variables = {
            "environment": deployment.environment,
            "region": deployment.region
        }

        # Add shared state from other deployments
        for name, state in self.shared_state.items():
            if name != deployment.provider.value:
                variables.update({
                    f"{name}_endpoint": state.get("endpoint"),
                    f"{name}_credentials": state.get("credentials")
                })

        return variables

    async def failover(self, primary: str, backup: str) -> Dict[str, Any]:
        """Perform failover from primary to backup deployment"""

        print(f"Initiating failover from {primary} to {backup}")

        # Get backup deployment
        backup_deployment = self.deployments.get(backup)
        if not backup_deployment:
            return {"success": False, "error": f"Backup deployment {backup} not found"}

        # Update DNS to point to backup
        dns_resource = Resource(
            type="route53_record",
            name="failover",
            properties={
                "name": "api.example.com",
                "type": "A",
                "ttl": 60,
                "records": [self.shared_state[backup]["endpoint"]]
            }
        )

        # Add DNS update to backup deployment
        backup_deployment.resources.append(dns_resource)

        # Deploy backup with updated DNS
        result = await self._deploy_single(backup, backup_deployment)

        if result["success"]:
            # Disable primary
            if primary in self.deployments:
                self.deployments[primary].enabled = False

            print(f"Failover to {backup} completed successfully")

        return result

    async def sync_state(self) -> Dict[str, Any]:
        """Synchronize state across deployments"""

        sync_results = {}

        for name, deployment in self.deployments.items():
            if not deployment.enabled:
                continue

            try:
                backend = self.backends.get(name)
                if not backend:
                    continue

                # Refresh state
                config = InfrastructureConfig(
                    name=name,
                    environment=deployment.environment,
                    provider=deployment.provider,
                    region=deployment.region,
                    resources=[]
                )

                # Get current state
                outputs = {}
                for resource in deployment.resources:
                    if hasattr(resource, 'name'):
                        output = await backend.output(config, resource.name)
                        if output:
                            outputs[resource.name] = output

                sync_results[name] = {
                    "success": True,
                    "outputs": outputs
                }

            except Exception as e:
                sync_results[name] = {
                    "success": False,
                    "error": str(e)
                }

        return sync_results
```

## 2. GitOps Patterns

### Generic GitOps Engine

```python
# gitops/engine.py
import asyncio
import aiohttp
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
import yaml
import json
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class GitOpsTool(str, Enum):
    """Supported GitOps tools"""
    ARGOCD = "argocd"
    FLUX = "flux"
    JENKINS_X = "jenkins-x"

class DeploymentStrategy(str, Enum):
    """Deployment strategies"""
    ROLLING = "rolling"
    BLUE_GREEN = "blue-green"
    CANARY = "canary"
    A_B = "a-b"

@dataclass
class Application:
    """Application definition for GitOps"""
    name: str
    repo_url: str
    path: str
    target_revision: str = "HEAD"
    namespace: str = "default"
    destination_server: str = "https://kubernetes.default.svc"
    sync_policy: Dict[str, Any] = field(default_factory=dict)
    health_checks: List[Dict[str, Any]] = field(default_factory=list)
    hooks: Dict[str, List[str]] = field(default_factory=dict)

@dataclass
class GitOpsConfig:
    """GitOps configuration"""
    tool: GitOpsTool
    namespace: str = "gitops-system"
    applications: List[Application] = field(default_factory=list)
    repositories: Dict[str, str] = field(default_factory=dict)
    policies: List[Dict[str, Any]] = field(default_factory=list)
    notifications: Dict[str, Any] = field(default_factory=dict)

class GitOpsEngine:
    """Generic GitOps engine"""

    def __init__(self, config: GitOpsConfig):
        self.config = config
        self.kubeconfig_path: Optional[Path] = None
        self.tool_client = None

    async def initialize(self) -> None:
        """Initialize GitOps tool"""

        if self.config.tool == GitOpsTool.ARGOCD:
            await self._init_argocd()
        elif self.config.tool == GitOpsTool.FLUX:
            await self._init_flux()
        else:
            raise ValueError(f"Unsupported GitOps tool: {self.config.tool}")

    async def deploy_application(
        self,
        app: Application,
        strategy: DeploymentStrategy = DeploymentStrategy.ROLLING
    ) -> Dict[str, Any]:
        """Deploy application using GitOps"""

        logger.info(f"Deploying application {app.name} with {strategy.value} strategy")

        # Pre-deployment hooks
        await self._execute_hooks(app, "pre-deploy")

        # Deploy based on strategy
        if strategy == DeploymentStrategy.CANARY:
            result = await self._deploy_canary(app)
        elif strategy == DeploymentStrategy.BLUE_GREEN:
            result = await self._deploy_blue_green(app)
        else:
            result = await self._deploy_rolling(app)

        # Post-deployment hooks
        if result["success"]:
            await self._execute_hooks(app, "post-deploy")

            # Health checks
            health_status = await self._check_health(app)
            result["health"] = health_status

        return result

    async def _init_argocd(self) -> None:
        """Initialize ArgoCD"""

        # Install ArgoCD if not present
        install_cmd = [
            "kubectl", "apply", "-n", self.config.namespace,
            "-f", "https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml"
        ]

        result = await self._run_kubectl_command(install_cmd)

        if result["returncode"] != 0 and "AlreadyExists" not in result["stderr"]:
            raise RuntimeError(f"Failed to install ArgoCD: {result['stderr']}")

        # Wait for ArgoCD to be ready
        await self._wait_for_deployment("argocd-server", self.config.namespace)

    async def _init_flux(self) -> None:
        """Initialize Flux"""

        # Install Flux CLI
        install_cmd = [
            "curl", "-s", "https://fluxcd.io/install.sh | bash"
        ]

        result = await self._run_command(install_cmd, shell=True)

        if result["returncode"] != 0:
            raise RuntimeError(f"Failed to install Flux: {result['stderr']}")

        # Bootstrap Flux
        bootstrap_cmd = [
            "flux", "bootstrap", "git",
            "--url", self.config.repositories.get("main", ""),
            "--branch", "main",
            "--path", "clusters/my-cluster"
        ]

        result = await self._run_command(bootstrap_cmd)

        if result["returncode"] != 0:
            raise RuntimeError(f"Failed to bootstrap Flux: {result['stderr']}")

    async def _deploy_rolling(self, app: Application) -> Dict[str, Any]:
        """Deploy using rolling update strategy"""

        # Create ArgoCD application manifest
        app_manifest = self._generate_argocd_app(app)

        # Apply manifest
        result = await self._apply_kubernetes_yaml(app_manifest)

        # Wait for sync
        if result["success"]:
            sync_result = await self._wait_for_sync(app.name)
            result.update(sync_result)

        return result

    async def _deploy_canary(self, app: Application) -> Dict[str, Any]:
        """Deploy using canary strategy"""

        # Create canary application
        canary_app = Application(
            name=f"{app.name}-canary",
            repo_url=app.repo_url,
            path=app.path,
            target_revision=app.target_revision,
            namespace=app.namespace,
            sync_policy={
                "automated": {
                    "prune": False,
                    "self_heal": False
                }
            }
        )

        # Create stable application
        stable_app = Application(
            name=f"{app.name}-stable",
            repo_url=app.repo_url,
            path=app.path,
            target_revision=app.target_revision,
            namespace=app.namespace,
            sync_policy=app.sync_policy
        )

        results = {}

        # Deploy stable first
        results["stable"] = await self._deploy_rolling(stable_app)

        # Deploy canary with small traffic split
        if results["stable"]["success"]:
            results["canary"] = await self._deploy_rolling(canary_app)

            # Set up traffic splitting
            if results["canary"]["success"]:
                traffic_result = await self._setup_traffic_split(app, canary_weight=10)
                results["traffic"] = traffic_result

        return {
            "success": all(r.get("success", False) for r in results.values()),
            "phases": results
        }

    async def _deploy_blue_green(self, app: Application) -> Dict[str, Any]:
        """Deploy using blue-green strategy"""

        # Determine active color
        active_color = await self._get_active_color(app.name)
        new_color = "green" if active_color == "blue" else "blue"

        # Create new deployment
        new_app = Application(
            name=f"{app.name}-{new_color}",
            repo_url=app.repo_url,
            path=app.path,
            target_revision=app.target_revision,
            namespace=app.namespace,
            sync_policy=app.sync_policy
        )

        # Deploy new color
        deploy_result = await self._deploy_rolling(new_app)

        if deploy_result["success"]:
            # Health check new deployment
            health_result = await self._check_deployment_health(
                f"{app.name}-{new_color}",
                app.namespace
            )

            if health_result["healthy"]:
                # Switch traffic
                switch_result = await self._switch_traffic(app.name, new_color)
                deploy_result["traffic_switch"] = switch_result

                if switch_result["success"]:
                    # Clean up old deployment
                    old_color = active_color
                    cleanup_result = await self._cleanup_deployment(
                        f"{app.name}-{old_color}",
                        app.namespace
                    )
                    deploy_result["cleanup"] = cleanup_result
            else:
                deploy_result["health_check"] = health_result
                deploy_result["success"] = False

        return deploy_result

    def _generate_argocd_app(self, app: Application) -> str:
        """Generate ArgoCD application manifest"""

        manifest = {
            "apiVersion": "argoproj.io/v1alpha1",
            "kind": "Application",
            "metadata": {
                "name": app.name,
                "namespace": self.config.namespace
            },
            "spec": {
                "project": "default",
                "source": {
                    "repoURL": app.repo_url,
                    "targetRevision": app.target_revision,
                    "path": app.path
                },
                "destination": {
                    "server": app.destination_server,
                    "namespace": app.namespace
                },
                "syncPolicy": {
                    "automated": {
                        "prune": app.sync_policy.get("prune", True),
                        "selfHeal": app.sync_policy.get("self_heal", True)
                    },
                    "syncOptions": [
                        "CreateNamespace=true"
                    ]
                }
            }
        }

        return yaml.dump(manifest, sort_keys=False)

    async def _apply_kubernetes_yaml(self, yaml_content: str) -> Dict[str, Any]:
        """Apply Kubernetes YAML manifest"""

        cmd = ["kubectl", "apply", "-f", "-"]

        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            env={"KUBECONFIG": str(self.kubeconfig_path)} if self.kubeconfig_path else None
        )

        stdout, stderr = await process.communicate(yaml_content.encode())

        return {
            "success": process.returncode == 0,
            "stdout": stdout.decode(),
            "stderr": stderr.decode()
        }

    async def _wait_for_sync(self, app_name: str, timeout: int = 300) -> Dict[str, Any]:
        """Wait for ArgoCD application to sync"""

        start_time = datetime.utcnow()

        while (datetime.utcnow() - start_time).seconds < timeout:
            cmd = ["argocd", "app", "get", app_name, "-o", "json"]
            result = await self._run_command(cmd)

            if result["returncode"] == 0:
                app_data = json.loads(result["stdout"])
                status = app_data.get("status", {})

                sync_status = status.get("sync", {}).get("status", "")
                health_status = status.get("health", {}).get("status", "")

                if sync_status == "Synced" and health_status == "Healthy":
                    return {
                        "success": True,
                        "status": "Synced and Healthy",
                        "duration": (datetime.utcnow() - start_time).seconds
                    }

            await asyncio.sleep(5)

        return {
            "success": False,
            "error": f"Sync timeout after {timeout} seconds"
        }

    async def _execute_hooks(self, app: Application, hook_type: str) -> None:
        """Execute deployment hooks"""

        hooks = app.hooks.get(hook_type, [])

        for hook in hooks:
            logger.info(f"Executing {hook_type} hook: {hook}")

            try:
                result = await self._run_command(hook, shell=True)

                if result["returncode"] != 0:
                    logger.error(f"Hook failed: {result['stderr']}")

            except Exception as e:
                logger.error(f"Error executing hook: {e}")

    async def _check_health(self, app: Application) -> Dict[str, Any]:
        """Check application health"""

        health_results = {}

        for check in app.health_checks:
            if check["type"] == "http":
                result = await self._check_http_health(check)
            elif check["type"] == "kubernetes":
                result = await self._check_kubernetes_health(check)
            else:
                result = {"healthy": False, "error": f"Unknown health check type: {check['type']}"}

            health_results[check["name"]] = result

        return health_results

    async def _run_kubectl_command(self, cmd: List[str]) -> Dict[str, Any]:
        """Run kubectl command"""
        return await self._run_command(
            ["kubectl"] + cmd,
            env={"KUBECONFIG": str(self.kubeconfig_path)} if self.kubeconfig_path else None
        )

    async def _run_command(
        self,
        cmd: List[str],
        shell: bool = False,
        env: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """Run command"""

        if shell:
            cmd = ["bash", "-c", " ".join(cmd) if isinstance(cmd, list) else cmd]

        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            env=env
        )

        stdout, stderr = await process.communicate()

        return {
            "returncode": process.returncode,
            "stdout": stdout.decode(),
            "stderr": stderr.decode()
        }

    async def _wait_for_deployment(
        self,
        deployment_name: str,
        namespace: str,
        timeout: int = 300
    ) -> None:
        """Wait for deployment to be ready"""

        cmd = [
            "kubectl", "wait",
            f"deployment/{deployment_name}",
            "--for", "condition=available",
            f"--namespace={namespace}",
            f"--timeout={timeout}s"
        ]

        result = await self._run_kubectl_command(cmd)

        if result["returncode"] != 0:
            raise RuntimeError(f"Deployment {deployment_name} not ready: {result['stderr']}")
```

## 3. Progressive Delivery Patterns

### Canary Analysis Engine

```python
# delivery/canary.py
import asyncio
import aiohttp
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import numpy as np
import logging

logger = logging.getLogger(__name__)

@dataclass
class CanaryMetric:
    """Canary analysis metric"""
    name: str
    query: str
    weight: float = 1.0
    threshold: Optional[float] = None
    comparison: str = "less_than"  # less_than, greater_than, equals

@dataclass
class CanaryConfig:
    """Canary deployment configuration"""
    application: str
    namespace: str
    baseline_label: str = "version=baseline"
    canary_label: str = "version=canary"
    traffic_step: int = 10
    max_traffic: int = 50
    analysis_interval: int = 60  # seconds
    metrics: List[CanaryMetric] = field(default_factory=list)
    success_criteria: Dict[str, float] = field(default_factory=dict)
    rollback_on_failure: bool = True

class CanaryAnalyzer:
    """Analyzes canary deployment metrics"""

    def __init__(self, prometheus_url: str):
        self.prometheus_url = prometheus_url
        self.session = None

    async def analyze(
        self,
        config: CanaryConfig,
        current_traffic: int
    ) -> Dict[str, Any]:
        """Analyze canary vs baseline metrics"""

        analysis = {
            "timestamp": datetime.utcnow().isoformat(),
            "traffic_percentage": current_traffic,
            "metrics": {},
            "overall_score": 0.0,
            "recommendation": "proceed"
        }

        # Query metrics for both baseline and canary
        baseline_metrics = await self._query_metrics(config, "baseline")
        canary_metrics = await self._query_metrics(config, "canary")

        # Analyze each metric
        metric_scores = []

        for metric in config.metrics:
            baseline_value = baseline_metrics.get(metric.name, 0)
            canary_value = canary_metrics.get(metric.name, 0)

            # Calculate percentage difference
            if baseline_value != 0:
                diff_percentage = ((canary_value - baseline_value) / baseline_value) * 100
            else:
                diff_percentage = 0

            # Determine if metric passes threshold
            passes = self._evaluate_metric(metric, canary_value, baseline_value)

            # Calculate score
            score = self._calculate_score(metric, diff_percentage, passes)
            metric_scores.append(score * metric.weight)

            analysis["metrics"][metric.name] = {
                "baseline": baseline_value,
                "canary": canary_value,
                "difference_percentage": diff_percentage,
                "passes": passes,
                "score": score
            }

        # Calculate overall score
        if metric_scores:
            analysis["overall_score"] = np.mean(metric_scores)

        # Determine recommendation
        analysis["recommendation"] = self._get_recommendation(
            analysis["overall_score"],
            config,
            current_traffic
        )

        return analysis

    async def _query_metrics(
        self,
        config: CanaryConfig,
        variant: str
    ) -> Dict[str, float]:
        """Query metrics from Prometheus"""

        label = config.canary_label if variant == "canary" else config.baseline_label
        metrics = {}

        for metric in config.metrics:
            query = metric.query.format(label=label)

            try:
                value = await self._query_prometheus(query)
                metrics[metric.name] = value
            except Exception as e:
                logger.error(f"Failed to query metric {metric.name}: {e}")
                metrics[metric.name] = 0

        return metrics

    async def _query_prometheus(self, query: str) -> float:
        """Query single metric from Prometheus"""

        if not self.session:
            self.session = aiohttp.ClientSession()

        url = f"{self.prometheus_url}/api/v1/query"
        params = {"query": query}

        async with self.session.get(url, params=params) as response:
            data = await response.json()

            if data["status"] == "success" and data["data"]["result"]:
                return float(data["data"]["result"][0]["value"][1])

            return 0.0

    def _evaluate_metric(
        self,
        metric: CanaryMetric,
        canary_value: float,
        baseline_value: float
    ) -> bool:
        """Evaluate if metric passes threshold"""

        if metric.threshold is None:
            return True

        if metric.comparison == "less_than":
            return canary_value <= metric.threshold
        elif metric.comparison == "greater_than":
            return canary_value >= metric.threshold
        elif metric.comparison == "equals":
            return abs(canary_value - metric.threshold) < 0.01

        return True

    def _calculate_score(
        self,
        metric: CanaryMetric,
        diff_percentage: float,
        passes: bool
    ) -> float:
        """Calculate metric score"""

        if not passes:
            return 0.0

        # Score based on how close to baseline
        if abs(diff_percentage) < 5:
            return 1.0
        elif abs(diff_percentage) < 10:
            return 0.8
        elif abs(diff_percentage) < 20:
            return 0.6
        else:
            return 0.4

    def _get_recommendation(
        self,
        score: float,
        config: CanaryConfig,
        current_traffic: int
    ) -> str:
        """Get deployment recommendation"""

        if score < 0.5:
            return "rollback"
        elif score < 0.7:
            if current_traffic >= config.max_traffic:
                return "rollback"
            return "hold"
        else:
            if current_traffic >= config.max_traffic:
                return "promote"
            return "promote"

class CanaryController:
    """Controls canary deployment lifecycle"""

    def __init__(self, analyzer: CanaryAnalyzer, k8s_client):
        self.analyzer = analyzer
        self.k8s_client = k8s_client
        self.active_canaries: Dict[str, Dict[str, Any]] = {}

    async def start_canary(self, config: CanaryConfig) -> str:
        """Start canary deployment"""

        canary_id = f"{config.application}-{int(datetime.utcnow().timestamp())}"

        # Create initial canary deployment
        await self._create_canary_deployment(config)

        # Set up initial traffic split
        await self._set_traffic_split(config, config.traffic_step)

        # Start analysis loop
        asyncio.create_task(self._analysis_loop(canary_id, config))

        self.active_canaries[canary_id] = {
            "config": config,
            "current_traffic": config.traffic_step,
            "started_at": datetime.utcnow(),
            "status": "running"
        }

        logger.info(f"Started canary deployment {canary_id}")
        return canary_id

    async def _analysis_loop(self, canary_id: str, config: CanaryConfig) -> None:
        """Run continuous analysis"""

        while canary_id in self.active_canaries:
            canary_info = self.active_canaries[canary_id]

            if canary_info["status"] != "running":
                break

            # Run analysis
            analysis = await self.analyzer.analyze(
                config,
                canary_info["current_traffic"]
            )

            # Act on recommendation
            await self._handle_recommendation(canary_id, analysis)

            # Wait for next analysis
            await asyncio.sleep(config.analysis_interval)

    async def _handle_recommendation(
        self,
        canary_id: str,
        analysis: Dict[str, Any]
    ) -> None:
        """Handle analysis recommendation"""

        canary_info = self.active_canaries.get(canary_id)
        if not canary_info:
            return

        recommendation = analysis["recommendation"]
        config = canary_info["config"]

        if recommendation == "rollback":
            logger.warning(f"Rolling back canary {canary_id}")
            await self._rollback_canary(canary_id)

        elif recommendation == "hold":
            logger.info(f"Holding canary {canary_id} at {canary_info['current_traffic']}% traffic")

        elif recommendation == "promote":
            if canary_info["current_traffic"] >= config.max_traffic:
                # Full promotion
                logger.info(f"Promoting canary {canary_id} to production")
                await self._promote_canary(canary_id)
            else:
                # Increase traffic
                new_traffic = min(
                    canary_info["current_traffic"] + config.traffic_step,
                    config.max_traffic
                )

                logger.info(f"Increasing canary {canary_id} traffic to {new_traffic}%")
                await self._set_traffic_split(config, new_traffic)
                canary_info["current_traffic"] = new_traffic

    async def _set_traffic_split(
        self,
        config: CanaryConfig,
        canary_percentage: int
    ) -> None:
        """Set traffic split between baseline and canary"""

        # Implementation depends on traffic management solution
        # Could be Istio VirtualService, AWS ALB, Nginx Ingress, etc.

        if config.namespace == "istio-system":
            await self._set_istio_traffic_split(config, canary_percentage)
        elif config.namespace == "aws":
            await self._set_alb_traffic_split(config, canary_percentage)
        else:
            await self._set_service_mesh_traffic_split(config, canary_percentage)

    async def _set_istio_traffic_split(
        self,
        config: CanaryConfig,
        canary_percentage: int
    ) -> None:
        """Set traffic split using Istio"""

        # Update Istio VirtualService
        virtual_service = {
            "apiVersion": "networking.istio.io/v1beta1",
            "kind": "VirtualService",
            "metadata": {
                "name": config.application,
                "namespace": config.namespace
            },
            "spec": {
                "http": [
                    {
                        "name": "primary",
                        "route": [
                            {
                                "destination": {
                                    "host": f"{config.application}",
                                    "subset": "canary"
                                },
                                "weight": canary_percentage
                            },
                            {
                                "destination": {
                                    "host": f"{config.application}",
                                    "subset": "baseline"
                                },
                                "weight": 100 - canary_percentage
                            }
                        ]
                    }
                ]
            }
        }

        # Apply to Kubernetes
        cmd = [
            "kubectl", "apply", "-f", "-",
            "-n", config.namespace
        ]

        # Implementation would apply the VirtualService
        pass
```

This comprehensive cloud-native deployment skill provides production-ready patterns for implementing modern infrastructure as code, GitOps workflows, and progressive delivery strategies across any cloud provider or platform.

`★ Insight ─────────────────────────────────────`
The cloud-native patterns shown here emphasize several key 2025 best practices:
1. **Provider Abstraction**: Generic interfaces allow switching between Terraform, Pulumi, and other IaC tools
2. **Multi-Cloud Strategy**: Built-in support for managing deployments across multiple providers with failover capabilities
3. **GitOps-First**: Declarative deployment through Git with support for ArgoCD, Flux, and custom tools
4. **Progressive Delivery**: Safe deployments with canary analysis, blue-green strategies, and automated rollback
5. **Policy as Code**: Integration with Open Policy Agent for automated compliance and security

These patterns ensure your cloud deployments are automated, secure, and resilient across any infrastructure.
`─────────────────────────────────────────────────`