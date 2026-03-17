---
name: pydantic
version: 1.0.0
description: Comprehensive Pydantic data validation skill for customer support tech enablement - covering BaseModel, Field validation, custom validators, FastAPI integration, BaseSettings, serialization, and Pydantic V2 features
author: Customer Support Tech Enablement Team
tags:
  - python
  - validation
  - data-modeling
  - customer-support
  - fastapi
  - backend
  - api
  - type-safety
  - pydantic-v2
  - settings-management
requirements:
  - pydantic>=2.0.0
  - pydantic-settings>=2.0.0
  - email-validator>=2.0.0
  - python-dotenv>=1.0.0
  - fastapi>=0.100.0 (optional, for API integration)
use_cases:
  - Support ticket validation and processing
  - User input sanitization and validation
  - API request/response modeling
  - Configuration management
  - Data curation and quality assurance
  - Database model validation
  - Settings and environment variable handling
  - **create Pydantic model for agent configuration**
  - **validate media metadata with Pydantic**
  - **define brand knowledge schema**
---

# Pydantic Data Validation Skill

## Overview

You are a Pydantic expert specializing in data validation for customer support systems. Your role is to help build robust, type-safe data models that validate support tickets, user data, API requests, and configuration settings using Pydantic V2.

## Core Competencies

### 1. BaseModel Fundamentals

**Purpose**: Create validated data models with automatic type coercion and comprehensive error reporting.

**Key Principles**:
- Define models using Python type hints
- Leverage automatic validation on instantiation
- Use `model_dump()` and `model_dump_json()` for serialization
- Handle `ValidationError` exceptions gracefully
- Implement proper error logging for support operations

**Basic Pattern**:
```python
from pydantic import BaseModel, Field, ValidationError
from datetime import datetime
from typing import Optional, List, Literal, Dict, Any

# TRAE_Extractor-app: Agent Configuration Model
class AgentToolConfig(BaseModel):
    """Configuration for a single agent tool"""
    name: str = Field(..., description="Tool name")
    type: Literal["mcp", "native", "api", "think", "memory", "filesystem"] = Field(
        ...,
        description="Tool type"
    )
    config: Dict[str, Any] = Field(
        default_factory=dict,
        description="Tool-specific configuration"
    )
    command: Optional[str] = Field(None, description="Command for MCP tools")
    args: Optional[List[str]] = Field(None, description="Command arguments")
    env: Optional[Dict[str, str]] = Field(None, description="Environment variables")

class AgentConfig(BaseModel):
    """Configuration for a single agent in Cagent team"""
    name: str = Field(..., min_length=1, max_length=50)
    model: str = Field(..., description="Model reference from models section")
    description: str = Field(..., min_length=10, description="Agent purpose")
    instruction: str = Field(..., min_length=50, description="Agent system prompt")
    toolsets: List[AgentToolConfig] = Field(
        default_factory=list,
        description="List of tool configurations"
    )
    rag: Optional[List[str]] = Field(
        None,
        description="List of RAG knowledge bases to use"
    )
    sub_agents: Optional[List[str]] = Field(
        None,
        description="List of sub-agent names this agent can delegate to"
    )
    add_prompt_files: Optional[List[str]] = Field(
        None,
        description="Additional prompt files to include"
    )

try:
    agent_config = AgentConfig(
        name="captioning",
        model="sonnet",
        description="Generates captions and social media copy",
        instruction="You are a captioning specialist...",
        toolsets=[
            AgentToolConfig(
                type="mcp",
                command="npx",
                args=["-y", "@perplexity-ai/mcp-server"],
                env={"PERPLEXITY_API_KEY": "${PERPLEXITY_API_KEY}"}
            )
        ],
        rag=["brand_guidelines", "platform_specs"]
    )
    print(agent_config.model_dump())
except ValidationError as e:
    # Log validation errors for team review
    for error in e.errors():
        print(f"Field: {error['loc']}, Error: {error['msg']}")
```

**Legacy Support Ticket Example** (for reference):
```python
from pydantic import BaseModel, Field, ValidationError
from datetime import datetime
from typing import Optional

class SupportTicket(BaseModel):
    ticket_id: int
    customer_email: str
    subject: str = Field(min_length=5, max_length=200)
    description: str = Field(min_length=20)
    priority: str = Field(pattern=r'^(low|medium|high|urgent)$')
    created_at: datetime
    assigned_to: Optional[str] = None
    status: str = 'open'

try:
    ticket = SupportTicket(
        ticket_id=12345,
        customer_email='customer@example.com',
        subject='Login Issue',
        description='Cannot access my account after password reset',
        priority='high',
        created_at='2024-01-15T10:30:00'
    )
    print(ticket.model_dump())
except ValidationError as e:
    # Log validation errors for support team review
    for error in e.errors():
        print(f"Field: {error['loc']}, Error: {error['msg']}")
```

### 2. Field Configuration and Constraints

**Purpose**: Apply granular validation rules to individual fields for data quality assurance.

**Common Constraints**:
- **String validation**: `min_length`, `max_length`, `pattern`, `strip_whitespace`
- **Numeric validation**: `gt`, `ge`, `lt`, `le`, `multiple_of`
- **Field metadata**: `title`, `description`, `examples`, `json_schema_extra`
- **Serialization control**: `alias`, `serialization_alias`, `exclude`, `include`

**Customer Support Example**:
```python
from pydantic import BaseModel, Field, EmailStr, HttpUrl
from typing import Annotated
from datetime import datetime

class CustomerProfile(BaseModel):
    # ID fields with constraints
    customer_id: Annotated[int, Field(gt=0, description="Unique customer identifier")]

    # Contact information with validation
    email: EmailStr
    phone: Annotated[str, Field(pattern=r'^\+?1?\d{9,15}$', description="International phone format")]

    # Name fields with length constraints
    first_name: Annotated[str, Field(min_length=1, max_length=50, strip_whitespace=True)]
    last_name: Annotated[str, Field(min_length=1, max_length=50, strip_whitespace=True)]

    # Company information (optional)
    company_name: Optional[Annotated[str, Field(max_length=100)]] = None
    company_website: Optional[HttpUrl] = None

    # Support tier with default
    support_tier: Annotated[str, Field(pattern=r'^(basic|premium|enterprise)$')] = 'basic'

    # Metadata fields
    registration_date: datetime
    last_contact: Optional[datetime] = None
    notes: str = Field(default='', max_length=2000, description="Internal notes")

    # Excluded from serialization (internal use only)
    internal_score: int = Field(default=0, exclude=True)

    model_config = {
        'str_strip_whitespace': True,
        'validate_assignment': True,
        'populate_by_name': True
    }
```

### 3. Custom Field Validators

**Purpose**: Implement business logic validation beyond basic type checking.

**@field_validator Pattern**:
```python
from pydantic import BaseModel, field_validator, ValidationInfo
import re

class SupportTicketSubmission(BaseModel):
    customer_email: str
    subject: str
    description: str
    category: str
    attachments: list[str] = []

    @field_validator('customer_email')
    @classmethod
    def validate_email_domain(cls, v: str) -> str:
        """Validate email format and check against blocked domains"""
        blocked_domains = ['tempmail.com', 'throwaway.email']

        if '@' not in v:
            raise ValueError('Invalid email format')

        domain = v.split('@')[1].lower()
        if domain in blocked_domains:
            raise ValueError(f'Email domain {domain} is not allowed')

        return v.lower()

    @field_validator('subject')
    @classmethod
    def validate_subject(cls, v: str) -> str:
        """Ensure subject is meaningful and not spam"""
        v = v.strip()

        # Check for minimum word count
        words = v.split()
        if len(words) < 2:
            raise ValueError('Subject must contain at least 2 words')

        # Check for spam patterns
        spam_patterns = [r'viagra', r'casino', r'lottery']
        for pattern in spam_patterns:
            if re.search(pattern, v, re.IGNORECASE):
                raise ValueError('Subject contains prohibited content')

        return v

    @field_validator('attachments')
    @classmethod
    def validate_attachments(cls, v: list[str]) -> list[str]:
        """Validate attachment file extensions"""
        allowed_extensions = {'.pdf', '.jpg', '.jpeg', '.png', '.doc', '.docx', '.txt'}

        for filename in v:
            ext = filename[filename.rfind('.'):].lower() if '.' in filename else ''
            if ext not in allowed_extensions:
                raise ValueError(f'File type {ext} not allowed. Allowed: {allowed_extensions}')

        if len(v) > 5:
            raise ValueError('Maximum 5 attachments allowed')

        return v

    @field_validator('category')
    @classmethod
    def validate_category(cls, v: str) -> str:
        """Normalize and validate ticket category"""
        valid_categories = {
            'technical', 'billing', 'account', 'feature_request',
            'bug_report', 'general_inquiry'
        }

        v_normalized = v.lower().replace(' ', '_')
        if v_normalized not in valid_categories:
            raise ValueError(f'Invalid category. Valid options: {valid_categories}')

        return v_normalized
```

### 4. Model-Level Validation

**Purpose**: Validate relationships between multiple fields and perform cross-field validation.

**@model_validator Pattern**:
```python
from pydantic import BaseModel, model_validator, ValidationError
from datetime import datetime, timedelta
from typing import Any, Optional

class TicketSchedule(BaseModel):
    ticket_id: int
    scheduled_start: datetime
    scheduled_end: datetime
    technician_id: Optional[int] = None
    estimated_hours: float
    priority: str

    @model_validator(mode='before')
    @classmethod
    def preprocess_data(cls, data: Any) -> Any:
        """Preprocess and normalize data before field validation"""
        if isinstance(data, dict):
            # Auto-generate estimated hours if not provided
            if 'scheduled_start' in data and 'scheduled_end' in data and 'estimated_hours' not in data:
                start = datetime.fromisoformat(data['scheduled_start'])
                end = datetime.fromisoformat(data['scheduled_end'])
                data['estimated_hours'] = (end - start).total_seconds() / 3600

            # Normalize priority
            if 'priority' in data:
                data['priority'] = data['priority'].lower()

        return data

    @model_validator(mode='after')
    def validate_schedule(self) -> 'TicketSchedule':
        """Validate scheduling logic after all fields are validated"""
        # Ensure end is after start
        if self.scheduled_end <= self.scheduled_start:
            raise ValueError('scheduled_end must be after scheduled_start')

        # Validate duration against priority
        duration = (self.scheduled_end - self.scheduled_start).total_seconds() / 3600

        if self.priority == 'urgent' and duration > 2:
            raise ValueError('Urgent tickets must be scheduled within 2 hours')

        if self.priority == 'low' and duration < 1:
            raise ValueError('Low priority tickets require minimum 1 hour allocation')

        # Ensure estimated hours match duration
        if abs(self.estimated_hours - duration) > 0.1:
            raise ValueError('estimated_hours must match scheduled duration')

        # Validate business hours (9 AM - 6 PM)
        if self.scheduled_start.hour < 9 or self.scheduled_start.hour >= 18:
            raise ValueError('Tickets must be scheduled during business hours (9 AM - 6 PM)')

        return self

class TicketEscalation(BaseModel):
    ticket_id: int
    current_assignee: str
    escalation_level: int
    reason: str
    requested_by: str
    approved_by: Optional[str] = None

    @model_validator(mode='after')
    def validate_escalation_approval(self) -> 'TicketEscalation':
        """Ensure high-level escalations require approval"""
        if self.escalation_level >= 3 and not self.approved_by:
            raise ValueError('Level 3+ escalations require manager approval')

        if self.approved_by == self.requested_by:
            raise ValueError('Approver must be different from requester')

        return self
```

### 5. Nested Models and Complex Structures

**Purpose**: Build hierarchical data models for complex support workflows.

**Pattern**:
```python
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Literal
from enum import Enum

class TicketStatus(str, Enum):
    OPEN = 'open'
    IN_PROGRESS = 'in_progress'
    PENDING_CUSTOMER = 'pending_customer'
    RESOLVED = 'resolved'
    CLOSED = 'closed'

class Comment(BaseModel):
    comment_id: int
    author: str
    content: str = Field(min_length=1, max_length=5000)
    timestamp: datetime
    is_internal: bool = False

class Attachment(BaseModel):
    filename: str
    file_size_bytes: int = Field(gt=0, le=10_000_000)  # Max 10MB
    content_type: str
    uploaded_by: str
    uploaded_at: datetime
    url: str

class Resolution(BaseModel):
    resolved_by: str
    resolution_date: datetime
    resolution_summary: str = Field(min_length=20, max_length=2000)
    root_cause: Optional[str] = None
    preventive_measures: Optional[str] = None
    customer_satisfaction_score: Optional[int] = Field(default=None, ge=1, le=5)

class CustomerInfo(BaseModel):
    customer_id: int
    name: str
    email: str
    phone: Optional[str] = None
    account_type: Literal['free', 'basic', 'premium', 'enterprise']
    registration_date: datetime

class CompleteTicket(BaseModel):
    # Core ticket information
    ticket_id: int
    customer: CustomerInfo

    # Ticket details
    subject: str = Field(min_length=5, max_length=200)
    description: str = Field(min_length=20)
    category: str
    priority: str
    status: TicketStatus

    # Assignment and tracking
    assigned_to: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    # Rich content
    comments: list[Comment] = []
    attachments: list[Attachment] = []

    # Resolution (if resolved/closed)
    resolution: Optional[Resolution] = None

    # Metadata
    tags: list[str] = Field(default_factory=list, max_length=10)
    related_tickets: list[int] = Field(default_factory=list)

    @model_validator(mode='after')
    def validate_ticket_state(self) -> 'CompleteTicket':
        """Ensure ticket state is consistent"""
        if self.status in (TicketStatus.RESOLVED, TicketStatus.CLOSED) and not self.resolution:
            raise ValueError('Resolved/closed tickets must have resolution details')

        if self.status == TicketStatus.IN_PROGRESS and not self.assigned_to:
            raise ValueError('In-progress tickets must be assigned')

        return self

    model_config = {
        'use_enum_values': True,
        'validate_assignment': True,
        'json_schema_extra': {
            'examples': [{
                'ticket_id': 12345,
                'customer': {
                    'customer_id': 6789,
                    'name': 'John Doe',
                    'email': 'john@example.com',
                    'account_type': 'premium',
                    'registration_date': '2023-01-01T00:00:00'
                },
                'subject': 'Unable to access dashboard',
                'description': 'Getting 403 error when trying to access analytics dashboard',
                'category': 'technical',
                'priority': 'high',
                'status': 'in_progress',
                'assigned_to': 'tech_support_1',
                'created_at': '2024-01-15T10:00:00',
                'updated_at': '2024-01-15T11:30:00'
            }]
        }
    }
```

### 6. FastAPI Integration for Request/Response Models

**Purpose**: Create type-safe API endpoints with automatic validation and documentation.

**Pattern**:
```python
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field, ValidationError
from typing import Optional, List
from datetime import datetime

app = FastAPI(title="Support Ticket API")

# Request Models
class TicketCreateRequest(BaseModel):
    customer_email: str
    subject: str = Field(min_length=5, max_length=200)
    description: str = Field(min_length=20, max_length=5000)
    category: str
    priority: str = Field(default='medium', pattern=r'^(low|medium|high|urgent)$')
    attachments: List[str] = Field(default_factory=list, max_length=5)

    model_config = {
        'json_schema_extra': {
            'examples': [{
                'customer_email': 'user@example.com',
                'subject': 'Cannot reset password',
                'description': 'I clicked the reset password link but did not receive an email',
                'category': 'account',
                'priority': 'high',
                'attachments': []
            }]
        }
    }

class TicketUpdateRequest(BaseModel):
    subject: Optional[str] = Field(default=None, min_length=5, max_length=200)
    description: Optional[str] = Field(default=None, min_length=20)
    status: Optional[str] = None
    assigned_to: Optional[str] = None
    priority: Optional[str] = Field(default=None, pattern=r'^(low|medium|high|urgent)$')

# Response Models
class TicketResponse(BaseModel):
    ticket_id: int
    customer_email: str
    subject: str
    description: str
    category: str
    priority: str
    status: str
    assigned_to: Optional[str]
    created_at: datetime
    updated_at: datetime

    model_config = {'from_attributes': True}  # For ORM compatibility

class TicketListResponse(BaseModel):
    tickets: List[TicketResponse]
    total: int
    page: int
    page_size: int

class ErrorResponse(BaseModel):
    error_code: str
    message: str
    details: Optional[dict] = None

# API Endpoints
@app.post(
    "/tickets/",
    response_model=TicketResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"model": ErrorResponse, "description": "Validation error"},
        500: {"model": ErrorResponse, "description": "Server error"}
    }
)
async def create_ticket(ticket: TicketCreateRequest):
    """Create a new support ticket with automatic validation"""
    try:
        # Business logic here
        # ticket_data is automatically validated by Pydantic
        new_ticket = {
            "ticket_id": 12345,
            "customer_email": ticket.customer_email,
            "subject": ticket.subject,
            "description": ticket.description,
            "category": ticket.category,
            "priority": ticket.priority,
            "status": "open",
            "assigned_to": None,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        return TicketResponse(**new_ticket)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error_code": "CREATION_FAILED", "message": str(e)}
        )

@app.get("/tickets/", response_model=TicketListResponse)
async def list_tickets(
    page: int = Field(default=1, ge=1),
    page_size: int = Field(default=20, ge=1, le=100),
    status: Optional[str] = None,
    priority: Optional[str] = None
):
    """List tickets with pagination and filtering"""
    # Query logic here
    tickets = []  # Fetch from database
    return TicketListResponse(
        tickets=tickets,
        total=0,
        page=page,
        page_size=page_size
    )

@app.patch("/tickets/{ticket_id}", response_model=TicketResponse)
async def update_ticket(ticket_id: int, update: TicketUpdateRequest):
    """Update ticket with partial validation"""
    # Only provided fields are validated
    update_data = update.model_dump(exclude_unset=True)
    # Apply updates to database
    # Return updated ticket
    pass
```

### 7. BaseSettings for Configuration Management

**Purpose**: Manage application configuration from environment variables with validation.

**Pattern**:
```python
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, PostgresDsn, RedisDsn, EmailStr
from typing import Optional, List

class DatabaseSettings(BaseSettings):
    """Database configuration"""
    host: str = Field(default='localhost', description='Database host')
    port: int = Field(default=5432, ge=1, le=65535)
    username: str
    password: str
    database: str = Field(default='support_db')

    # Computed property for connection string
    @property
    def connection_url(self) -> str:
        return f"postgresql://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"

    model_config = SettingsConfigDict(
        env_prefix='DB_',
        env_file='.env',
        env_file_encoding='utf-8'
    )

class RedisSettings(BaseSettings):
    """Redis cache configuration"""
    url: RedisDsn = Field(default='redis://localhost:6379/0')
    max_connections: int = Field(default=50, ge=1)
    socket_timeout: int = Field(default=5, ge=1)

    model_config = SettingsConfigDict(
        env_prefix='REDIS_',
        env_file='.env'
    )

class EmailSettings(BaseSettings):
    """Email notification configuration"""
    smtp_host: str = Field(default='smtp.gmail.com')
    smtp_port: int = Field(default=587, ge=1, le=65535)
    smtp_username: str
    smtp_password: str
    from_email: EmailStr
    support_email: EmailStr
    use_tls: bool = Field(default=True)

    model_config = SettingsConfigDict(
        env_prefix='EMAIL_',
        env_file='.env'
    )

class SupportSettings(BaseSettings):
    """Support system configuration"""
    max_tickets_per_page: int = Field(default=50, ge=1, le=200)
    max_attachment_size_mb: int = Field(default=10, ge=1, le=100)
    allowed_file_extensions: List[str] = Field(
        default=['.pdf', '.jpg', '.jpeg', '.png', '.doc', '.docx']
    )
    auto_assign_enabled: bool = Field(default=True)
    escalation_hours: int = Field(default=24, ge=1)
    business_hours_start: int = Field(default=9, ge=0, le=23)
    business_hours_end: int = Field(default=18, ge=0, le=23)

    model_config = SettingsConfigDict(
        env_prefix='SUPPORT_',
        env_file='.env'
    )

class ApplicationSettings(BaseSettings):
    """Main application settings"""
    app_name: str = Field(default='Support Ticket System')
    app_version: str = Field(default='1.0.0')
    debug: bool = Field(default=False)
    api_key: str
    secret_key: str
    allowed_origins: List[str] = Field(default=['http://localhost:3000'])

    # Nested settings
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    redis: RedisSettings = Field(default_factory=RedisSettings)
    email: EmailSettings = Field(default_factory=EmailSettings)
    support: SupportSettings = Field(default_factory=SupportSettings)

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        case_sensitive=False,
        extra='ignore'
    )

# Usage
settings = ApplicationSettings()
print(f"Connecting to database at: {settings.database.connection_url}")
print(f"Max tickets per page: {settings.support.max_tickets_per_page}")
```

### 8. Agent Configuration Models

**Purpose**: Validate Cagent team configuration with agent definitions, tool configurations, and RAG settings.

**Pattern**:
```python
from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Optional, List, Literal, Dict, Any
from enum import Enum

class ToolType(str, Enum):
    """Tool type enumeration"""
    MCP = "mcp"
    NATIVE = "native"
    API = "api"
    THINK = "think"
    MEMORY = "memory"
    FILESYSTEM = "filesystem"

class AgentToolConfig(BaseModel):
    """Configuration for a single agent tool"""
    name: str = Field(..., min_length=1, max_length=100, description="Tool name")
    type: ToolType = Field(..., description="Tool type")
    config: Dict[str, Any] = Field(
        default_factory=dict, 
        description="Tool-specific configuration"
    )
    command: Optional[str] = Field(None, max_length=500, description="Command for MCP tools")
    args: Optional[List[str]] = Field(None, max_items=20, description="Command arguments")
    env: Optional[Dict[str, str]] = Field(None, description="Environment variables")
    remote: Optional[Dict[str, str]] = Field(None, description="Remote tool configuration")

    @field_validator('env')
    @classmethod
    def validate_env_vars(cls, v: Optional[Dict[str, str]]) -> Optional[Dict[str, str]]:
        """Validate environment variable format"""
        if v is None:
            return v
        for key, value in v.items():
            if not key.isupper():
                raise ValueError(f'Environment variable key must be uppercase: {key}')
            if '${' in value and not value.endswith('}'):
                raise ValueError(f'Invalid environment variable format: {value}')
        return v

class AgentConfig(BaseModel):
    """Configuration for a single agent in Cagent team"""
    name: str = Field(..., min_length=1, max_length=50, description="Agent name")
    model: str = Field(..., min_length=1, description="Model reference from models section")
    description: str = Field(..., min_length=10, max_length=500, description="Agent purpose")
    instruction: str = Field(..., min_length=50, description="Agent system prompt")
    toolsets: List[AgentToolConfig] = Field(
        default_factory=list,
        description="List of tool configurations"
    )
    rag: Optional[List[str]] = Field(
        None,
        description="List of RAG knowledge bases to use"
    )
    sub_agents: Optional[List[str]] = Field(
        None,
        description="List of sub-agent names this agent can delegate to"
    )
    add_prompt_files: Optional[List[str]] = Field(
        None,
        description="Additional prompt files to include"
    )

    @field_validator('toolsets')
    @classmethod
    def validate_toolsets(cls, v: List[AgentToolConfig]) -> List[AgentToolConfig]:
        """Ensure toolsets are valid"""
        if not v:
            return v
        tool_names = [tool.name for tool in v]
        if len(tool_names) != len(set(tool_names)):
            raise ValueError('Tool names must be unique within an agent')
        return v

    @model_validator(mode='after')
    def validate_agent_consistency(self) -> 'AgentConfig':
        """Ensure agent configuration is consistent"""
        # If RAG is specified, ensure instruction mentions it
        if self.rag and 'rag' not in self.instruction.lower():
            # Warning, not error - agent might handle RAG implicitly
            pass
        return self

class ModelConfig(BaseModel):
    """Model definition for Cagent"""
    provider: str = Field(..., min_length=1, description="LLM provider (anthropic, openai, etc.)")
    model: str = Field(..., min_length=1, description="Model name")
    max_tokens: int = Field(..., gt=0, le=200000, description="Maximum tokens")

class CagentTeamConfig(BaseModel):
    """Complete Cagent team configuration"""
    version: str = Field(..., pattern=r'^\d+\.\d+$', description="Configuration version")
    models: Dict[str, ModelConfig] = Field(
        ...,
        description="Model definitions keyed by model name"
    )
    agents: Dict[str, AgentConfig] = Field(
        ...,
        description="Agent configurations keyed by agent name"
    )
    rag: Optional[Dict[str, Any]] = Field(
        None,
        description="RAG knowledge base configurations"
    )
    metadata: Optional[Dict[str, str]] = Field(
        None,
        description="Team metadata (author, license, version)"
    )

    @model_validator(mode='after')
    def validate_team_consistency(self) -> 'CagentTeamConfig':
        """Ensure team configuration is consistent"""
        # Check that all agent models exist in models section
        for agent_name, agent_config in self.agents.items():
            if agent_config.model not in self.models:
                raise ValueError(
                    f"Agent '{agent_name}' references unknown model: {agent_config.model}. "
                    f"Available models: {list(self.models.keys())}"
                )
        
        # Check that RAG references exist
        if self.rag:
            for agent_name, agent_config in self.agents.items():
                if agent_config.rag:
                    for rag_ref in agent_config.rag:
                        if rag_ref not in self.rag:
                            raise ValueError(
                                f"Agent '{agent_name}' references unknown RAG: {rag_ref}. "
                                f"Available RAGs: {list(self.rag.keys())}"
                            )
        
        return self

# Example usage
try:
    team_config = CagentTeamConfig(
        version="1.0",
        models={
            "sonnet": ModelConfig(
                provider="anthropic",
                model="claude-sonnet-4-5",
                max_tokens=64000
            ),
            "haiku": ModelConfig(
                provider="anthropic",
                model="claude-haiku-4-5",
                max_tokens=32000
            )
        },
        agents={
            "captioning": AgentConfig(
                name="captioning",
                model="sonnet",
                description="Generates captions and social media copy",
                instruction="You are a captioning specialist...",
                toolsets=[
                    AgentToolConfig(
                        type=ToolType.MCP,
                        command="npx",
                        args=["-y", "@perplexity-ai/mcp-server"],
                        env={"PERPLEXITY_API_KEY": "${PERPLEXITY_API_KEY}"}
                    )
                ],
                rag=["brand_guidelines", "platform_specs"]
            ),
            "creative_worker": AgentConfig(
                name="creative_worker",
                model="haiku",
                description="Executes editing plans for images and videos",
                instruction="You are Creative Worker. You execute plans...",
                toolsets=[
                    AgentToolConfig(
                        type=ToolType.MCP,
                        command="npx",
                        args=["-y", "--package", "@cloudinary/asset-management-mcp", "--", "mcp", "start"],
                        env={"CLOUDINARY_URL": "${CLOUDINARY_URL}"}
                    )
                ]
            )
        },
        rag={
            "brand_guidelines": {
                "docs": ["${BRAND_DIR:-./brands/slowfood}/knowledge/guidelines.md"],
                "strategies": [{"type": "chunked-embeddings"}]
            }
        },
        metadata={
            "author": "TRAE Extractor Team",
            "license": "Proprietary",
            "version": "1.0"
        }
    )
    print(f"Team config validated: {team_config.model_dump_json(indent=2)}")
except ValidationError as e:
    print(f"Validation failed: {e.error_count()} errors")
    for error in e.errors():
        print(f"  {error['loc']}: {error['msg']}")
```

### 9. Media Validation

**Purpose**: Validate media metadata, EXIF data, and post scheduling information for TRAE_Extractor-app.

**Pattern**:
```python
from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Optional, List, Tuple
from datetime import datetime
from enum import Enum

class MediaType(str, Enum):
    """Media file types"""
    IMAGE = "image"
    VIDEO = "video"

class EXIFData(BaseModel):
    """EXIF metadata from photos"""
    camera_make: Optional[str] = Field(None, max_length=50, description="Camera manufacturer")
    camera_model: Optional[str] = Field(None, max_length=50, description="Camera model")
    date_taken: Optional[datetime] = Field(None, description="When photo was taken")
    gps_coordinates: Optional[Tuple[float, float]] = Field(None, description="GPS coordinates (lat, lon)")
    iso: Optional[int] = Field(None, ge=100, le=6400, description="ISO sensitivity")
    aperture: Optional[float] = Field(None, ge=1.0, le=32.0, description="Aperture f-stop")
    shutter_speed: Optional[str] = Field(None, max_length=20, description="Shutter speed")
    focal_length: Optional[int] = Field(None, ge=1, le=1000, description="Focal length in mm")

    @field_validator('gps_coordinates')
    @classmethod
    def validate_gps(cls, v: Optional[Tuple[float, float]]) -> Optional[Tuple[float, float]]:
        """Validate GPS coordinates"""
        if v is None:
            return v
        lat, lon = v
        if not (-90 <= lat <= 90):
            raise ValueError(f'Latitude must be between -90 and 90: {lat}')
        if not (-180 <= lon <= 180):
            raise ValueError(f'Longitude must be between -180 and 180: {lon}')
        return v

class MediaMetadata(BaseModel):
    """Metadata for extracted media files"""
    filename: str = Field(..., pattern=r'^[\w\-\.]+\.(jpg|png|mp4|mov|jpeg)$', description="Filename with extension")
    file_size_bytes: int = Field(..., gt=0, le=5_000_000_000, description="File size in bytes (max 5GB)")
    media_type: MediaType = Field(..., description="Type of media")
    exif_data: Optional[EXIFData] = Field(None, description="EXIF metadata")
    tags: List[str] = Field(
        default_factory=list,
        max_length=20,
        description="User-defined tags"
    )
    album: Optional[str] = Field(None, max_length=100, description="Source album name")
    date_imported: datetime = Field(default_factory=datetime.utcnow, description="When media was imported")
    cloudinary_public_id: Optional[str] = Field(None, max_length=200, description="Cloudinary public ID")
    cloudinary_url: Optional[str] = Field(None, regex=r'^https://res\.cloudinary\.com/.*', description="Cloudinary URL")

    @field_validator('filename')
    @classmethod
    def validate_filename(cls, v: str) -> str:
        """Ensure filename has valid extension"""
        valid_extensions = ['.jpg', '.jpeg', '.png', '.mp4', '.mov']
        if not any(v.lower().endswith(ext) for ext in valid_extensions):
            raise ValueError(f'Invalid file extension. Must be one of: {valid_extensions}')
        return v

class MediaExtractionResult(BaseModel):
    """Result of media extraction operation"""
    album: str = Field(..., min_length=1, max_length=100, description="Source album name")
    export_path: str = Field(..., min_length=1, description="Export directory")
    media_count: int = Field(..., ge=0, description="Number of files extracted")
    media_files: List[MediaMetadata] = Field(..., description="Extracted media metadata")
    extraction_time: float = Field(..., gt=0, le=3600, description="Extraction duration in seconds")
    success: bool = Field(..., description="Whether extraction succeeded")

    @model_validator(mode='after')
    def validate_extraction_consistency(self) -> 'MediaExtractionResult':
        """Ensure extraction result is consistent"""
        if self.success and self.media_count == 0:
            raise ValueError('Successful extraction must have at least one media file')
        if not self.success and self.media_count > 0:
            raise ValueError('Failed extraction should not have media files')
        if self.media_count != len(self.media_files):
            raise ValueError('media_count must match length of media_files list')
        return self

class SocialPlatform(str, Enum):
    """Supported social media platforms"""
    INSTAGRAM = "instagram"
    FACEBOOK = "facebook"
    LINKEDIN = "linkedin"
    TWITTER = "twitter"
    TIKTOK = "tiktok"

class PostStatus(str, Enum):
    """Post scheduling status"""
    PENDING = "pending"
    SCHEDULED = "scheduled"
    PUBLISHED = "published"
    FAILED = "failed"
    CANCELLED = "cancelled"

class ScheduledPost(BaseModel):
    """Scheduled social media post"""
    post_id: Optional[str] = Field(None, max_length=100, description="Post ID from platform")
    media_id: str = Field(..., min_length=1, max_length=200, description="Cloudinary public ID or media file ID")
    caption: str = Field(..., min_length=10, max_length=2200, description="Post caption")
    platforms: List[SocialPlatform] = Field(..., min_items=1, max_items=5, description="Target platforms")
    scheduled_at: datetime = Field(..., description="Scheduled publish time")
    hashtags: List[str] = Field(
        default_factory=list,
        max_length=30,
        description="Hashtags to include"
    )
    status: PostStatus = Field(default=PostStatus.PENDING, description="Post status")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="When post was created")
    published_at: Optional[datetime] = Field(None, description="When post was published")
    error_message: Optional[str] = Field(None, max_length=1000, description="Error if publishing failed")

    @field_validator('scheduled_at')
    @classmethod
    def validate_scheduled_time(cls, v: datetime) -> datetime:
        """Ensure scheduled time is in future"""
        if v <= datetime.utcnow():
            raise ValueError('Scheduled time must be in future')
        return v

    @model_validator(mode='after')
    def validate_post_state(self) -> 'ScheduledPost':
        """Ensure post state is consistent"""
        if self.status == PostStatus.PUBLISHED and not self.published_at:
            raise ValueError('Published posts must have published_at timestamp')
        if self.status == PostStatus.FAILED and not self.error_message:
            raise ValueError('Failed posts must have error_message')
        return self

class CaptionVariation(BaseModel):
    """Caption variation for different platforms"""
    platform: SocialPlatform = Field(..., description="Target platform")
    caption: str = Field(..., min_length=10, max_length=2200, description="Caption text")
    hashtags: List[str] = Field(default_factory=list, max_length=30, description="Platform-specific hashtags")
    character_limit: Optional[int] = Field(None, ge=1, le=5000, description="Platform character limit")

class CaptionGenerationResult(BaseModel):
    """Result of caption generation by agent"""
    media_id: str = Field(..., min_length=1, description="Media file ID")
    variations: List[CaptionVariation] = Field(..., min_items=1, description="Caption variations per platform")
    suggested_hashtags: List[str] = Field(default_factory=list, max_length=30, description="Suggested hashtags")
    tone_analysis: Optional[Dict[str, str]] = Field(None, description="Tone analysis results")
    generation_time: float = Field(..., gt=0, le=300, description="Generation time in seconds")

# Example usage
try:
    # Validate media metadata
    media = MediaMetadata(
        filename="sunset-beach.jpg",
        file_size_bytes=2048576,
        media_type=MediaType.IMAGE,
        exif_data=EXIFData(
            camera_make="Apple",
            camera_model="iPhone 15 Pro",
            date_taken=datetime(2024, 7, 15, 18, 30, 0),
            iso=100,
            aperture=2.8
        ),
        tags=["sunset", "beach", "summer"],
        album="Summer 2024"
    )
    print(f"Media validated: {media.filename}")

    # Validate scheduled post
    scheduled_post = ScheduledPost(
        media_id="cloudinary/summer-beach-abc123",
        caption="Beautiful sunset at the beach. The colors of nature never disappoint! 🌅 #sunset #beach #nature",
        platforms=[SocialPlatform.INSTAGRAM, SocialPlatform.FACEBOOK],
        scheduled_at=datetime(2024, 8, 1, 18, 0, 0),
        hashtags=["#sunset", "#beach", "#nature", "#summer"]
    )
    print(f"Post scheduled for: {scheduled_post.scheduled_at}")

except ValidationError as e:
    print(f"Validation failed: {e.error_count()} errors")
    for error in e.errors():
        print(f"  {error['loc']}: {error['msg']}")
```


### 8. Serialization and Deserialization

**Purpose**: Control how models are converted to/from dictionaries, JSON, and other formats.

**Pattern**:
```python
from pydantic import BaseModel, Field, field_serializer, computed_field
from datetime import datetime
from typing import Optional

class TicketExport(BaseModel):
    ticket_id: int
    customer_email: str
    subject: str
    created_at: datetime
    status: str
    priority: str
    assigned_to: Optional[str] = None
    internal_notes: str = Field(default='', exclude=True)

    @field_serializer('customer_email')
    def mask_email(self, email: str) -> str:
        """Mask email for privacy in exports"""
        if '@' in email:
            local, domain = email.split('@')
            masked = local[:2] + '***' + local[-1:] if len(local) > 3 else '***'
            return f"{masked}@{domain}"
        return email

    @field_serializer('created_at')
    def format_datetime(self, dt: datetime) -> str:
        """Format datetime for export"""
        return dt.strftime('%Y-%m-%d %H:%M:%S')

    @computed_field
    @property
    def days_open(self) -> int:
        """Calculate days since ticket creation"""
        return (datetime.now() - self.created_at).days

# Serialization modes
ticket = TicketExport(
    ticket_id=123,
    customer_email='john.doe@example.com',
    subject='Login issue',
    created_at=datetime.now(),
    status='open',
    priority='high',
    internal_notes='Customer called twice'
)

# Standard serialization
print(ticket.model_dump())
# {'ticket_id': 123, 'customer_email': 'jo***e@example.com', ...}

# Include all fields (even excluded)
print(ticket.model_dump(mode='python', exclude_none=False))

# Serialize to JSON
json_str = ticket.model_dump_json(indent=2)
print(json_str)

# Exclude specific fields
print(ticket.model_dump(exclude={'internal_notes', 'assigned_to'}))

# Include only specific fields
print(ticket.model_dump(include={'ticket_id', 'subject', 'status'}))
```

### 9. Advanced Validation Techniques

**Purpose**: Implement sophisticated validation logic for complex business requirements.

**Pattern**:
```python
from pydantic import BaseModel, field_validator, model_validator
from typing import Any, Optional
import re

class TicketPrioritization(BaseModel):
    customer_tier: str
    issue_category: str
    response_time_hours: int
    business_impact: str
    affected_users: int = Field(ge=1)

    @field_validator('customer_tier')
    @classmethod
    def validate_tier(cls, v: str) -> str:
        valid_tiers = {'free', 'basic', 'premium', 'enterprise'}
        v = v.lower()
        if v not in valid_tiers:
            raise ValueError(f'Invalid tier. Must be one of: {valid_tiers}')
        return v

    @model_validator(mode='after')
    def calculate_priority(self) -> 'TicketPrioritization':
        """Auto-calculate priority based on multiple factors"""
        priority_score = 0

        # Customer tier weights
        tier_weights = {'enterprise': 40, 'premium': 30, 'basic': 20, 'free': 10}
        priority_score += tier_weights.get(self.customer_tier, 10)

        # Business impact weights
        impact_weights = {'critical': 30, 'high': 20, 'medium': 10, 'low': 5}
        priority_score += impact_weights.get(self.business_impact.lower(), 5)

        # Affected users factor
        if self.affected_users > 100:
            priority_score += 20
        elif self.affected_users > 10:
            priority_score += 10

        # Response time urgency
        if self.response_time_hours <= 2:
            priority_score += 10

        # Store computed priority (you'd add this field to the model)
        # self.computed_priority = 'urgent' if priority_score >= 80 else ...

        return self

class SecureTicketData(BaseModel):
    """Model with PII validation and sanitization"""
    customer_name: str
    email: str
    phone: Optional[str] = None
    credit_card_last4: Optional[str] = None
    ssn_last4: Optional[str] = None

    @field_validator('credit_card_last4')
    @classmethod
    def validate_cc_last4(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        if not re.match(r'^\d{4}$', v):
            raise ValueError('Credit card last 4 must be exactly 4 digits')
        return v

    @field_validator('phone')
    @classmethod
    def sanitize_phone(cls, v: Optional[str]) -> Optional[str]:
        """Remove all non-digit characters from phone"""
        if v is None:
            return v
        digits_only = re.sub(r'\D', '', v)
        if len(digits_only) < 10:
            raise ValueError('Phone number must have at least 10 digits')
        return digits_only

    @model_validator(mode='after')
    def validate_pii_consistency(self) -> 'SecureTicketData':
        """Ensure PII fields are consistent"""
        # If SSN is provided, credit card should also be provided for identity verification
        if self.ssn_last4 and not self.credit_card_last4:
            raise ValueError('Credit card verification required when SSN is provided')
        return self
```

### 10. Performance Optimization with Pydantic V2

**Purpose**: Optimize validation performance for high-throughput support systems.

**Key Strategies**:

1. **Use TypeAdapter for bulk validation**:
```python
from pydantic import TypeAdapter
from typing import List

# Define adapter once, reuse for validation
ticket_list_adapter = TypeAdapter(List[SupportTicket])

# Fast bulk validation
tickets_data = [...]  # List of dictionaries
validated_tickets = ticket_list_adapter.validate_python(tickets_data)
```

2. **Leverage strict mode for performance**:
```python
from pydantic import BaseModel, ConfigDict

class FastTicket(BaseModel):
    model_config = ConfigDict(strict=True)  # No type coercion

    ticket_id: int  # Must be int, won't coerce from string
    priority: str
```

3. **Use discriminated unions for polymorphic data**:
```python
from typing import Literal, Union
from pydantic import Field, BaseModel

class EmailTicket(BaseModel):
    ticket_type: Literal['email'] = 'email'
    customer_email: str
    subject: str

class PhoneTicket(BaseModel):
    ticket_type: Literal['phone'] = 'phone'
    phone_number: str
    call_duration: int

class ChatTicket(BaseModel):
    ticket_type: Literal['chat'] = 'chat'
    chat_session_id: str

# Fast dispatch based on discriminator field
TicketUnion = Union[EmailTicket, PhoneTicket, ChatTicket]

class TicketProcessor(BaseModel):
    ticket: TicketUnion = Field(discriminator='ticket_type')
```

4. **Reuse models and avoid dynamic creation**:
```python
# Good: Define once, reuse
class TicketModel(BaseModel):
    ticket_id: int
    subject: str

# Avoid: Dynamic model creation in loops
for data in ticket_data:
    # Don't create models dynamically
    pass
```

## Error Handling Best Practices

### Comprehensive Validation Error Handling

```python
from pydantic import ValidationError
import logging

logger = logging.getLogger(__name__)

def process_ticket_submission(data: dict) -> Optional[SupportTicket]:
    """Process ticket with comprehensive error handling"""
    try:
        ticket = SupportTicket(**data)
        logger.info(f"Ticket {ticket.ticket_id} validated successfully")
        return ticket

    except ValidationError as e:
        # Log detailed validation errors
        logger.error(f"Validation failed for ticket submission: {e.error_count()} errors")

        for error in e.errors():
            field = '.'.join(str(loc) for loc in error['loc'])
            error_type = error['type']
            message = error['msg']

            logger.error(f"Field '{field}': {message} (type: {error_type})")

        # Return user-friendly error response
        return None

    except Exception as e:
        logger.exception(f"Unexpected error processing ticket: {str(e)}")
        return None
```

## Testing Pydantic Models

### Unit Test Pattern

```python
import pytest
from pydantic import ValidationError

def test_support_ticket_validation():
    """Test ticket validation logic"""
    # Valid ticket
    valid_data = {
        'ticket_id': 123,
        'customer_email': 'test@example.com',
        'subject': 'Test Issue',
        'description': 'This is a test ticket with enough description',
        'priority': 'medium',
        'created_at': '2024-01-15T10:00:00'
    }
    ticket = SupportTicket(**valid_data)
    assert ticket.ticket_id == 123
    assert ticket.priority == 'medium'

    # Invalid priority
    with pytest.raises(ValidationError) as exc_info:
        SupportTicket(**{**valid_data, 'priority': 'invalid'})

    errors = exc_info.value.errors()
    assert any(e['loc'] == ('priority',) for e in errors)

    # Missing required field
    with pytest.raises(ValidationError):
        incomplete_data = {k: v for k, v in valid_data.items() if k != 'subject'}
        SupportTicket(**incomplete_data)
```

## Guidelines for Customer Support Context

1. **Always validate user input**: Never trust data from support forms, API calls, or external systems
2. **Provide helpful error messages**: Users should understand what's wrong and how to fix it
3. **Log validation failures**: Track patterns in validation errors to improve forms and documentation
4. **Use appropriate field constraints**: Balance security with usability
5. **Implement business rule validation**: Beyond types, validate business logic
6. **Handle PII carefully**: Mask or encrypt sensitive data, exclude from logs
7. **Version your models**: Use model versioning for API compatibility
8. **Test edge cases**: Include tests for boundary conditions and unusual inputs
9. **Document models thoroughly**: Use Field descriptions and JSON schema examples
10. **Monitor validation performance**: Track validation times for high-volume operations

## Common Patterns and Anti-Patterns

### Pattern: Request/Response Separation
```python
# Good: Separate models for requests and responses
class TicketCreateRequest(BaseModel):
    subject: str
    description: str

class TicketResponse(BaseModel):
    ticket_id: int
    subject: str
    description: str
    created_at: datetime

# Avoid: Using same model for input and output
```

### Pattern: Default Factory for Mutable Defaults
```python
# Good: Use default_factory
class Ticket(BaseModel):
    tags: list[str] = Field(default_factory=list)

# Avoid: Mutable default
class BadTicket(BaseModel):
    tags: list[str] = []  # Shared across instances!
```

### Pattern: Computed Fields
```python
# Good: Use computed_field for derived values
from pydantic import computed_field

class Ticket(BaseModel):
    created_at: datetime

    @computed_field
    @property
    def age_days(self) -> int:
        return (datetime.now() - self.created_at).days
```

## Skill Application Checklist

When using this skill, ensure you:

- [ ] Define clear, typed models with appropriate constraints
- [ ] Implement custom validators for business logic
- [ ] Handle ValidationError exceptions gracefully
- [ ] Use appropriate serialization for different contexts (API, database, logs)
- [ ] Configure models appropriately (frozen, validate_assignment, etc.)
- [ ] Write comprehensive tests for validation logic
- [ ] Document models with descriptions and examples
- [ ] Use BaseSettings for configuration management
- [ ] Optimize performance for high-volume operations
- [ ] Follow security best practices for PII and sensitive data

## References and Resources

- Pydantic V2 Documentation: https://docs.pydantic.dev/latest/
- Pydantic Settings: https://docs.pydantic.dev/latest/concepts/pydantic_settings/
- FastAPI Integration: https://fastapi.tiangolo.com/tutorial/body/
- Migration Guide (V1 to V2): https://docs.pydantic.dev/latest/migration/
- Performance Tips: https://docs.pydantic.dev/latest/concepts/performance/
