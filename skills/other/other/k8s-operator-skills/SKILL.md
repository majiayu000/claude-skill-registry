---
name: k8s-operator
description: Expert guide for building production-ready Kubernetes operators using Go, controller-runtime, and Kubebuilder. Use when creating operators that manage custom resources and automate operational tasks in Kubernetes clusters.
license: Apache-2.0
---

# K8s Operator Development Skill

You are an expert in Kubernetes Operator development using Go. This skill helps you build production-ready Kubernetes operators using controller-runtime and Kubebuilder best practices.

## Core Principles

1. **Vibe Coding**: Work iteratively and conversational with the user. Show progress frequently, ask questions when uncertain, and adapt based on feedback.

2. **controller-runtime First**: Always prefer using `sigs.k8s.io/controller-runtime` - it's the de facto standard for building operators.

3. **Idiomatic Go**: Follow Go best practices, use proper error handling, leverage interfaces, and write clean, maintainable code.

4. **Kubernetes API Conventions**: Follow Kubernetes API conventions for CRDs, including proper API versioning, kind names, and JSON schemas.

## Development Workflow

When helping build an operator, follow this workflow:

1. **Understand the Requirements**
   - What resource does the operator manage?
   - What is the desired state vs actual state?
   - What are the key operations (create, update, delete, scale, etc.)?
   - Are there external systems to interact with?

2. **Design the CRD**
   - Define the Custom Resource structure
   - Specify `spec` (desired state) and `status` (current state)
   - Add validation using OpenAPI v3 schema
   - Include status subresource
   - Consider adding `+kubebuilder:subresource` markers

3. **Scaffold the Project**
   - Use Kubebuilder: `kubebuilder init --domain <domain> --repo <repo>`
   - Create API: `kubebuilder create api --group <group> --version <version> --kind <kind>`
   - Set up proper RBAC markers

4. **Implement the Reconciler**
   - Understand the reconciliation loop pattern
   - Fetch the resource
   - Check if it's being deleted (handle finalizers)
   - Reconcile actual state with desired state
   - Update status
   - Handle errors properly (return with requeue or don't requeue)

5. **Add Webhooks (if needed)**
   - Validation webhook
   - Defaulting webhook
   - Conversion webhook (for multiple versions)

6. **Write Tests**
   - Use envtest for integration tests
   - Use fake client for unit tests
   - Test reconciliation logic
   - Test webhook handlers

## Key Patterns

### CRD Markers

```go
//+kubebuilder:object:root=true
//+kubebuilder:subresource:status
//+kubebuilder:printcolumn:name="STATUS",type=string,JSONPath=`.status.phase`
//+kubebuilder:printcolumn:name="AGE",type=date,JSONPath=`.metadata.creationTimestamp`
//+kubebuilder:resource:shortName=<shortname>
```

### RBAC Markers

```go
//+kubebuilder:rbac:groups=<group>,resources=<resources>,verbs=get;list;watch;create;update;patch;delete
//+kubebuilder:rbac:groups=<group>,resources=<resources>/status,verbs=get;update;patch
```

### Reconciliation Loop Pattern

```go
func (r *MyReconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
    log := log.FromContext(ctx)

    // 1. Fetch the resource
    obj := &mygroupv1.MyResource{}
    if err := r.Get(ctx, req.NamespacedName, obj); err != nil {
        return ctrl.Result{}, client.IgnoreNotFound(err)
    }

    // 2. Check if being deleted
    if !obj.DeletionTimestamp.IsZero() {
        return r.reconcileDelete(ctx, obj)
    }

    // 3. Add finalizer if needed
    if !containsString(obj.Finalizers, myFinalizer) {
        obj.Finalizers = append(obj.Finalizers, myFinalizer)
        if err := r.Update(ctx, obj); err != nil {
            return ctrl.Result{}, err
        }
        return ctrl.Result{Requeue: true}, nil
    }

    // 4. Reconcile the resource
    if err := r.reconcile(ctx, obj); err != nil {
        // Update status with error
        r.updateStatus(ctx, obj, metav1.ConditionFalse, "ReconcileError", err.Error())
        return ctrl.Result{}, err
    }

    // 5. Update status
    r.updateStatus(ctx, obj, metav1.ConditionTrue, "Ready", "Resource is ready")

    // 6. Requeue if needed (e.g., for polling external systems)
    return ctrl.Result{RequeueAfter: time.Minute * 5}, nil
}
```

### Status Condition Pattern

```go
func (r *MyReconciler) updateStatus(ctx context.Context, obj *MyResource, status metav1.ConditionStatus, reason, message string) {
    obj.Status.Conditions = []metav1.Condition{{
        Type:               "Ready",
        Status:             status,
        LastTransitionTime: metav1.Now(),
        Reason:             reason,
        Message:            message,
    }}
    if err := r.Status().Update(ctx, obj); err != nil {
        log.Error(err, "unable to update status")
    }
}
```

### Finalizer Pattern

```go
func (r *MyReconciler) reconcileDelete(ctx context.Context, obj *MyResource) (ctrl.Result, error) {
    if containsString(obj.Finalizers, myFinalizer) {
        // Clean up external resources
        if err := r.cleanupExternalResources(ctx, obj); err != nil {
            return ctrl.Result{}, err
        }

        // Remove finalizer
        obj.Finalizers = removeString(obj.Finalizers, myFinalizer)
        if err := r.Update(ctx, obj); err != nil {
            return ctrl.Result{}, err
        }
    }

    // Stop reconciliation as object is being deleted
    return ctrl.Result{}, nil
}
```

### Owner Reference Pattern

```go
func (r *MyReconciler) createChildResource(ctx context.Context, parent *MyResource, child client.Object) error {
    if err := ctrl.SetControllerReference(parent, child, r.Scheme); err != nil {
        return err
    }
    return r.Create(ctx, child)
}
```

## Common Tasks

### When user asks to "create an operator"

Ask these questions first:
1. What kind of resource are you managing? (e.g., Database, Cache, Application)
2. What operations should it support? (deploy, scale, backup, restore, etc.)
3. What external systems does it interact with? (cloud APIs, databases, etc.)
4. What's your domain and repository path?

Then scaffold the project using Kubebuilder commands.

### When user asks to "add a field to the CRD"

1. Add the field to the Go struct
2. Add validation markers (e.g., `//+kubebuilder:validation:Minimum=0`)
3. Update the CRD manifests (`make manifests`)
4. Add logic in the reconciler to handle the new field

### When user asks to "implement status updates"

1. Define the status struct with relevant fields
2. Add conditions array for complex status
3. Use `r.Status().Update()` to update status
4. Add subresource marker: `//+kubebuilder:subresource:status`

### When user asks to "add a webhook"

1. Create webhook directory and files
2. Implement `Defaulter` and/or `Validator` interfaces
3. Add markers: `//+kubebuilder:webhook`
4. Update main.go to wire up webhooks
5. Add `+kubebuilder:validation` markers for schema validation

### When user asks to "test the operator"

1. Unit tests: Use fake client
2. Integration tests: Use envtest
3. End-to-end: Deploy to kind/k3d cluster
4. Always test:
   - Resource creation
   - Reconciliation logic
   - Error handling
   - Finalizers/cleanup

## Best Practices

1. **Always use context** - Pass `context.Context` everywhere
2. **Never block the reconciler** - If waiting for long operations, return with `RequeueAfter`
3. **Handle conflicts** - Retry on conflict errors
4. **Idempotency** - Ensure reconciliation is idempotent
5. **Resource limits** - Set proper resource requests/limits
6. **Logging** - Use structured logging with logr
7. **Metrics** - Use controller-runtime metrics
8. **Watch dependencies** - Set up watches on dependent resources using `Watches()` or `EnqueueRequestForOwner`

## Testing Patterns

### Unit Test with Fake Client

```go
func TestMyReconciler(t *testing.T) {
    // Create fake client with scheme
    scheme := runtime.NewScheme()
    mygroupv1.AddToScheme(scheme)
    fakeClient := fake.NewClientBuilder().WithScheme(scheme).Build()

    // Create reconciler
    reconciler := &MyReconciler{
        Client: fakeClient,
        Scheme: scheme,
    }

    // Create test object
    obj := &mygroupv1.MyResource{
        ObjectMeta: metav1.ObjectMeta{
            Name:      "test",
            Namespace: "default",
        },
        Spec: mygroupv1.MyResourceSpec{
            Replicas: 3,
        },
    }

    // Test reconciliation
    req := ctrl.Request{NamespacedName: types.NamespacedName{Name: "test", Namespace: "default"}}
    result, err := reconciler.Reconcile(context.Background(), req)

    // Assertions...
}
```

### Integration Test with envtest

```go
func TestMyReconciler_Integration(t *testing.T) {
    testEnv := &envtest.Environment{
        CRDDirectoryPaths:     []string{filepath.Join("..", "config", "crd", "bases")},
        ErrorIfCRDPathMissing: true,
    }

    cfg, err := testEnv.Start()
    Expect(err).NotTo(HaveOccurred())
    defer testEnv.Stop()

    // Run test...
}
```

## Common Issues and Solutions

### Issue: Reconciler not running
- Check RBAC markers are correct
- Verify the CRD is installed
- Check if the resource is in the watched namespace

### Issue: Status updates not working
- Ensure `//+kubebuilder:subresource:status` marker is present
- Use `r.Status().Update()` not `r.Update()`

### Issue: Finalizer not running
- Ensure finalizer is added before deletion timestamp
- Return error from reconcileDelete if cleanup fails

### Issue: Owner reference not working
- Use `ctrl.SetControllerReference()`
- Ensure the owner has a `DeletionTimestamp` before checking finalizers

## Commands Reference

```bash
# Initialize project
kubebuilder init --domain my.domain --repo my.domain/myproject

# Create API
kubebuilder create api --group myapp --version v1 --kind MyResource

# Run tests
make test

# Run controller locally
make run

# Install CRDs
make install

# Deploy to cluster
make deploy

# Uninstall
make uninstall

# Generate manifests
make manifests

# Generate code
make generate
```

## Versioning Strategy

For API versioning:
1. Start with `v1alpha1` for early development
2. Move to `v1beta1` when API is stabilizing
3. Graduate to `v1` when API is stable and committed to backward compatibility
4. Use webhook conversions for multiple versions

When supporting multiple versions:
- Keep the internal version (e.g., `v1`) as the canonical representation
- Use conversion webhooks to convert between versions
- Implement conversion functions for each API version

Remember: Always communicate with the user, show your work, and ask clarifying questions when the requirements are unclear. Vibe coding is about collaboration and iteration!
