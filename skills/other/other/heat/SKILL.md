---
name: openstack-heat
description: "OpenStack Heat orchestration service skill. Use when working with HOT templates, stack lifecycle management, auto-scaling groups, nested stacks, resource type registry, template validation, or infrastructure-as-code patterns within OpenStack. Covers deployment via Kolla-Ansible, template authoring, stack operations, and troubleshooting common orchestration failures."
user-invocable: true
allowed-tools: Read Grep Glob
metadata:
  extensions:
    gsd-skill-creator:
      version: 1
      createdAt: "2026-02-23"
      triggers:
        intents:
          - "heat"
          - "orchestration"
          - "HOT template"
          - "stack"
          - "auto-scaling"
          - "nested stack"
          - "template"
          - "infrastructure as code"
        contexts:
          - "deploying openstack orchestration"
          - "writing heat templates"
          - "troubleshooting stacks"
          - "managing infrastructure as code"
---

# OpenStack Heat -- Orchestration Service

## Introduction

Heat is OpenStack's native orchestration engine. It implements infrastructure-as-code through HOT (Heat Orchestration Template) files -- YAML documents that declaratively describe cloud resources and their relationships. Heat creates, updates, and deletes collections of resources (called "stacks") as atomic units, handling dependency ordering, rollback on failure, and lifecycle management automatically.

Heat is to OpenStack what CloudFormation is to AWS and Deployment Manager is to GCP. The critical difference: HOT templates are portable across any OpenStack deployment, and Heat's resource type registry is extensible -- operators can register custom resource types without modifying the core service. For users familiar with Terraform, Heat serves a similar role but is integrated directly into the OpenStack control plane, meaning it has native access to all OpenStack APIs without external provider configuration.

The stack lifecycle follows a state machine: CREATE_IN_PROGRESS, CREATE_COMPLETE, CREATE_FAILED, UPDATE_IN_PROGRESS, UPDATE_COMPLETE, UPDATE_FAILED, DELETE_IN_PROGRESS, DELETE_COMPLETE, DELETE_FAILED. Each state transition is atomic -- either all resources in a stack reach the target state or the stack rolls back to the previous known-good state.

## Deploy

Heat deployment via Kolla-Ansible requires enabling the service in `globals.yml`:

```yaml
# /etc/kolla/globals.yml
enable_heat: "yes"
```

After deployment, Heat runs as two containers: `heat_api` (handles REST API requests) and `heat_engine` (processes stack operations, manages resource lifecycle). Some deployments also include `heat_api_cfn` for CloudFormation API compatibility.

**Verification commands:**

```bash
# Verify Heat containers are running
docker ps --filter name=heat

# Verify service registration in Keystone catalog
openstack service list | grep orchestration

# Verify Heat API is responsive
openstack orchestration service list

# Check engine status
openstack orchestration service list --format json
```

The orchestration service should appear with type `orchestration` in the service catalog. The engine should report status `up` with a recent `updated_at` timestamp. If the engine shows `down`, check the heat_engine container logs: `docker logs heat_engine`.

## Configure

### Template Format (HOT)

HOT templates are YAML documents with four top-level sections:

```yaml
heat_template_version: wallaby    # OpenStack release name or date (2021-04-16)

description: >
  Human-readable description of what this template creates.

parameters:
  instance_name:
    type: string
    default: my-server
    description: Name for the Nova instance
    constraints:
      - length: { min: 1, max: 64 }
  image_id:
    type: string
    description: Glance image ID to use
  flavor:
    type: string
    default: m1.small

resources:
  my_network:
    type: OS::Neutron::Net
    properties:
      name: template-network

  my_subnet:
    type: OS::Neutron::Subnet
    properties:
      network_id: { get_resource: my_network }
      cidr: 10.0.1.0/24
      dns_nameservers: [8.8.8.8]

  my_server:
    type: OS::Nova::Server
    properties:
      name: { get_param: instance_name }
      image: { get_param: image_id }
      flavor: { get_param: flavor }
      networks:
        - network: { get_resource: my_network }

outputs:
  server_ip:
    description: IP address of the created instance
    value: { get_attr: [my_server, first_address] }
```

### Core Resource Types

| Resource Type | Service | Purpose |
|--------------|---------|---------|
| `OS::Nova::Server` | Nova | Compute instances |
| `OS::Neutron::Net` | Neutron | Virtual networks |
| `OS::Neutron::Subnet` | Neutron | Subnets with CIDR blocks |
| `OS::Neutron::Router` | Neutron | Virtual routers |
| `OS::Neutron::FloatingIP` | Neutron | Floating IP allocation |
| `OS::Neutron::SecurityGroup` | Neutron | Security group rules |
| `OS::Cinder::Volume` | Cinder | Block storage volumes |
| `OS::Cinder::VolumeAttachment` | Cinder | Volume-to-instance attachment |
| `OS::Glance::Image` | Glance | Image registration |
| `OS::Swift::Container` | Swift | Object storage containers |
| `OS::Keystone::Project` | Keystone | Project creation |
| `OS::Heat::AutoScalingGroup` | Heat | Auto-scaling groups |
| `OS::Heat::ScalingPolicy` | Heat | Scaling policies |
| `OS::Heat::SoftwareConfig` | Heat | Software configuration scripts |
| `OS::Heat::SoftwareDeployment` | Heat | Software deployment execution |
| `OS::Heat::WaitCondition` | Heat | Wait for external signals |

### Intrinsic Functions

| Function | Purpose | Example |
|----------|---------|---------|
| `get_resource` | Reference another resource in the template | `{ get_resource: my_network }` |
| `get_attr` | Get an attribute from a resource | `{ get_attr: [my_server, first_address] }` |
| `get_param` | Get a parameter value | `{ get_param: instance_name }` |
| `str_replace` | String substitution | `{ str_replace: { template: "host=$HOST", params: { $HOST: { get_attr: [srv, first_address] } } } }` |
| `list_join` | Join list elements | `{ list_join: [",", [a, b, c]] }` |
| `if` | Conditional value | `{ if: [condition, value_true, value_false] }` |
| `repeat` | Iterate over a list | `{ repeat: { for_each: { "%item%": [a, b] }, template: { ... } } }` |

### Environment Files

Environment files override parameter defaults and map custom resource types:

```yaml
# env.yaml
parameters:
  image_id: cirros-0.5.2
  flavor: m1.tiny

resource_registry:
  "OS::Nova::Server::Custom": custom_server.yaml
```

### Nested Stacks

Templates can include other templates using `OS::Heat::Stack` or `type: file.yaml`:

```yaml
resources:
  web_tier:
    type: web-server.yaml
    properties:
      image: { get_param: image_id }
      count: 3
```

### Auto-Scaling Groups

```yaml
resources:
  asg:
    type: OS::Heat::AutoScalingGroup
    properties:
      min_size: 1
      max_size: 5
      desired_capacity: 2
      resource:
        type: OS::Nova::Server
        properties:
          image: { get_param: image_id }
          flavor: m1.small

  scale_up_policy:
    type: OS::Heat::ScalingPolicy
    properties:
      adjustment_type: change_in_capacity
      auto_scaling_group_id: { get_resource: asg }
      scaling_adjustment: 1
```

## Operate

### Stack CRUD

```bash
# Create a stack from a template
openstack stack create -t template.yaml -e env.yaml \
  --parameter "instance_name=prod-web" my-stack

# List all stacks
openstack stack list

# Show stack details
openstack stack show my-stack

# Show stack resources
openstack stack resource list my-stack

# Show specific resource details
openstack stack resource show my-stack my_server

# Show stack events (creation timeline)
openstack stack event list my-stack

# Show stack outputs
openstack stack output list my-stack
openstack stack output show my-stack server_ip
```

### Stack Update

```bash
# Update with modified template (in-place where possible)
openstack stack update -t updated-template.yaml my-stack

# Update parameters only
openstack stack update --parameter "flavor=m1.large" my-stack

# Preview update before applying (shows what will change)
openstack stack update --dry-run -t updated-template.yaml my-stack
```

Update semantics: Heat determines whether each resource can be updated in-place or requires replacement. Replacement creates a new resource before deleting the old one. Use `--dry-run` to preview which resources will be replaced.

### Template Validation

```bash
# Validate template syntax and resource types
openstack stack template validate -t template.yaml

# Validate with environment
openstack stack template validate -t template.yaml -e env.yaml
```

### Stack Lifecycle

```bash
# Suspend all resources in a stack
openstack stack suspend my-stack

# Resume suspended stack
openstack stack resume my-stack

# Create stack snapshot
openstack stack snapshot create my-stack snap-before-upgrade

# List snapshots
openstack stack snapshot list my-stack

# Restore from snapshot
openstack stack snapshot restore my-stack snap-before-upgrade

# Abandon stack (remove from Heat without deleting resources)
openstack stack abandon my-stack > abandoned-stack.json

# Adopt previously abandoned resources
openstack stack adopt -t template.yaml --adopt-file abandoned-stack.json adopted-stack

# Delete stack (deletes all resources)
openstack stack delete my-stack
```

## Troubleshoot

### Stack Create Fails

**Resource dependency cycle detected:**
The template has circular references where resource A depends on resource B which depends on resource A. Heat detects this at template validation time. Fix: restructure the template to break the cycle, often by using `depends_on` explicitly to clarify ordering, or by splitting into nested stacks.

**Invalid template syntax (ERROR_TEMPLATE_INVALID):**
Check `openstack stack event list my-stack` for the specific parsing error. Common causes: incorrect YAML indentation, invalid `heat_template_version`, referencing undefined parameters or resources, using functions in unsupported contexts.

**Resource type not found:**
The template references a resource type that is not registered. Check available types: `openstack orchestration resource type list`. If using custom types, verify the resource_registry in the environment file points to existing template files.

**Quota exceeded:**
Stack creation starts but resources fail with quota errors. Check: `openstack quota show` for the project. The template may request more instances, cores, RAM, or volumes than the project allows. Increase quotas or reduce template resource counts.

### Stack Stuck in IN_PROGRESS

**Dependent resource timeout:**
A resource is waiting for another resource that has not completed. Check `openstack stack resource list my-stack` to identify which resource is `CREATE_IN_PROGRESS`. Then check that resource's dependencies.

**Wait condition signal never received:**
If using `OS::Heat::WaitCondition`, the target instance must send a signal back to Heat. Verify the instance has network access to the Heat API, the signal URL is correctly passed via `get_attr`, and the software on the instance is actually sending the signal (check instance console log).

**Nested stack failure:**
A nested stack failed but the parent stack is still waiting. Check nested stack status: `openstack stack resource show parent-stack nested-resource`. Then inspect the nested stack directly: `openstack stack show <nested-stack-id>`.

### Stack Update Rollback

**Resource update not supported:**
Some resource properties cannot be updated in-place (e.g., changing an instance's image requires replacement). Heat will attempt rollback to the previous state. If rollback also fails, the stack enters UPDATE_FAILED state. Check `openstack stack event list my-stack` to identify which resource caused the failure.

**Replacement vs update semantics:**
Use `openstack stack update --dry-run` to preview which resources will be replaced before applying. Resources marked for replacement will be deleted and recreated, which means data loss for stateful resources (volumes, databases).

### Template Validation Passes but Create Fails

**Runtime constraints not caught at validation:**
Template validation checks syntax and resource type existence but cannot verify runtime conditions: image exists, flavor exists, network exists, security group allows required ports. These fail only at create time.

**Image not found at create time:**
Validation passes because `image` is a parameter, but the actual image ID or name does not exist in Glance. Verify: `openstack image list`.

### Nested Stack Failures

**Parameter passing errors:**
The parent template passes parameters to the nested template, but the names or types do not match. Check the nested template's `parameters` section against the parent's `properties` for the nested resource.

**Incorrect resource references:**
A nested template tries to reference resources from the parent template using `get_resource`. This does not work -- resources can only reference other resources within the same template. Use parameters to pass values between parent and nested templates.

## Integration Points

- **Keystone:** Heat authenticates all API requests through Keystone. Stack operations run with the token of the requesting user, meaning resource creation respects the user's project and RBAC policies. Heat uses trusts to allow the engine to perform deferred operations (like auto-scaling) on behalf of the user after the original token expires.
- **Nova:** `OS::Nova::Server` is the most commonly used resource type. Heat manages the full instance lifecycle including creation, update (resize), and deletion. Auto-scaling groups create and destroy Nova instances based on scaling policies.
- **Neutron:** Network resources (`OS::Neutron::Net`, `OS::Neutron::Subnet`, `OS::Neutron::Router`, `OS::Neutron::FloatingIP`) are orchestrated alongside compute resources to create complete network topologies in a single template.
- **Cinder:** Block storage volumes (`OS::Cinder::Volume`) and attachments (`OS::Cinder::VolumeAttachment`) are managed as stack resources. Volume lifecycle is tied to the stack -- deleting the stack deletes the volumes unless the `deletion_policy: retain` attribute is set.
- **Glance:** Heat references Glance images by name or ID in `OS::Nova::Server` definitions. Templates can also register new images using `OS::Glance::Image`.
- **Ceilometer:** Auto-scaling triggers connect Heat scaling policies to Ceilometer alarm thresholds. When a metric (CPU utilization, memory usage) crosses a threshold, Ceilometer fires an alarm that triggers Heat's scaling policy.
- **Software Deployment:** `OS::Heat::SoftwareConfig` and `OS::Heat::SoftwareDeployment` resources enable post-boot configuration of instances, executing scripts, Ansible playbooks, or Puppet manifests after the instance is running.

## NASA SE Cross-References

- **Phase C (Final Design and Fabrication):** Heat template development maps to the "fabrication" phase of the SE lifecycle. Templates are the design-to specifications (SP-6105 SS 5.1) -- they codify the infrastructure architecture into executable declarations. Template validation serves as the pre-build inspection step.
- **Phase D (Integration and Test):** Stack deployment is the integration step (SP-6105 SS 5.2-5.3). Creating a stack from a template and verifying all resources are healthy is the cloud equivalent of system integration testing. Stack outputs provide the verification data: IP addresses, resource IDs, and status confirming the integrated system matches the template specification.
- **Phase E (Operations and Sustainment):** Template management as operational infrastructure-as-code maps to the sustainment phase (SP-6105 SS 5.4-5.5). Stack updates represent controlled configuration changes with built-in rollback. Template version control in git provides the configuration management trail. Auto-scaling groups implement automated capacity management during operations.
