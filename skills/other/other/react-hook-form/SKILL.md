---
name: "react-hook-form"
description: "Performant React forms with minimal re-renders and built-in validation"
when_to_use: "Building forms in React with validation, dynamic fields, or complex form state"
---

# React Hook Form

## Quick Start

### Basic Form

```jsx
import { useForm } from "react-hook-form";

function BasicForm() {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm();

  const onSubmit = (data) => console.log(data);

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register("firstName")} />
      <input {...register("lastName", { required: "Last name is required" })} />
      {errors.lastName && <p>{errors.lastName.message}</p>}
      <input {...register("age", { pattern: /\d+/ })} />
      {errors.age && <p>Please enter number for age.</p>}
      <input type="submit" />
    </form>
  );
}
```

### Form with Default Values

```jsx
import { useForm } from "react-hook-form";

function FormWithDefaults() {
  const { register, handleSubmit } = useForm({
    defaultValues: {
      firstName: "John",
      lastName: "Doe",
      email: "john@example.com",
    },
  });

  const onSubmit = (data) => console.log(data);

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register("firstName")} />
      <input {...register("lastName")} />
      <input {...register("email")} />
      <button type="submit">Submit</button>
    </form>
  );
}
```

## Common Patterns

### Form Validation

```jsx
import { useForm } from "react-hook-form";

function ValidationExample() {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm();

  const onSubmit = (data) => console.log(data);

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input
        {...register("username", {
          required: "Username is required",
          minLength: {
            value: 3,
            message: "Username must be at least 3 characters",
          },
          maxLength: {
            value: 20,
            message: "Username must be less than 20 characters",
          },
        })}
      />
      {errors.username && <span>{errors.username.message}</span>}

      <input
        {...register("email", {
          required: "Email is required",
          pattern: {
            value: /^\S+@\S+$/i,
            message: "Invalid email format",
          },
        })}
      />
      {errors.email && <span>{errors.email.message}</span>}

      <button type="submit">Submit</button>
    </form>
  );
}
```

### Password Confirmation

```jsx
import { useForm } from "react-hook-form";

function PasswordForm() {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm();

  const onSubmit = (data) => console.log(data);

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input
        type="password"
        {...register("password", {
          required: "Password is required",
          minLength: {
            value: 8,
            message: "Password must be at least 8 characters",
          },
        })}
      />
      {errors.password && <span>{errors.password.message}</span>}

      <input
        type="password"
        {...register("confirmPassword", {
          required: "Please confirm your password",
          validate: (value, formValues) =>
            value === formValues.password || "Passwords do not match",
        })}
      />
      {errors.confirmPassword && <span>{errors.confirmPassword.message}</span>}

      <button type="submit">Submit</button>
    </form>
  );
}
```

### Using Controller for Custom Components

```jsx
import { useForm, Controller } from "react-hook-form";
import Select from "react-select";

function CustomInputForm() {
  const { handleSubmit, control } = useForm();

  const options = [
    { value: "chocolate", label: "Chocolate" },
    { value: "strawberry", label: "Strawberry" },
    { value: "vanilla", label: "Vanilla" },
  ];

  const onSubmit = (data) => console.log(data);

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <Controller
        name="flavor"
        control={control}
        rules={{ required: "Please select a flavor" }}
        render={({ field, fieldState: { error } }) => (
          <div>
            <Select {...field} options={options} />
            {error && <span>{error.message}</span>}
          </div>
        )}
      />

      <button type="submit">Submit</button>
    </form>
  );
}
```

### Dynamic Fields with useFieldArray

```jsx
import { useForm, useFieldArray } from "react-hook-form";

function DynamicFieldsForm() {
  const { register, handleSubmit, control } = useForm({
    defaultValues: {
      users: [{ name: "", email: "" }],
    },
  });

  const { fields, append, remove } = useFieldArray({
    control,
    name: "users",
  });

  const onSubmit = (data) => console.log(data);

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      {fields.map((field, index) => (
        <div key={field.id}>
          <input
            {...register(`users.${index}.name`, {
              required: "Name is required",
            })}
            placeholder="Name"
          />
          <input
            {...register(`users.${index}.email`, {
              required: "Email is required",
            })}
            placeholder="Email"
          />
          <button type="button" onClick={() => remove(index)}>
            Remove
          </button>
        </div>
      ))}

      <button type="button" onClick={() => append({ name: "", email: "" })}>
        Add User
      </button>

      <button type="submit">Submit</button>
    </form>
  );
}
```

### Async Form Submission

```jsx
import { useForm } from "react-hook-form";

function AsyncSubmitForm() {
  const {
    register,
    handleSubmit,
    formState: { isSubmitting },
  } = useForm();

  const onSubmit = async (data) => {
    try {
      // Simulate API call
      await new Promise((resolve) => setTimeout(resolve, 2000));
      console.log("Form submitted:", data);
    } catch (error) {
      console.error("Submission failed:", error);
    }
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register("name", { required: true })} />
      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? "Submitting..." : "Submit"}
      </button>
    </form>
  );
}
```

### Form with Context (FormProvider)

```jsx
import { useForm, FormProvider, useFormContext } from "react-hook-form";

function NestedInput({ name, label }) {
  const {
    register,
    formState: { errors },
  } = useFormContext();

  return (
    <div>
      <label>{label}</label>
      <input {...register(name)} />
      {errors[name] && <span>{errors[name].message}</span>}
    </div>
  );
}

function ContextForm() {
  const methods = useForm();
  const onSubmit = (data) => console.log(data);

  return (
    <FormProvider {...methods}>
      <form onSubmit={methods.handleSubmit(onSubmit)}>
        <NestedInput name="firstName" label="First Name" />
        <NestedInput name="lastName" label="Last Name" />
        <button type="submit">Submit</button>
      </form>
    </FormProvider>
  );
}
```

### Async Field Validation

```jsx
import { useForm } from "react-hook-form";

function AsyncValidationForm() {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm();

  const checkUsernameAvailability = async (username) => {
    // Simulate API call to check username
    await new Promise((resolve) => setTimeout(resolve, 500));

    const takenUsernames = ["admin", "user", "test"];
    if (takenUsernames.includes(username.toLowerCase())) {
      return "Username is already taken";
    }
    return true;
  };

  const onSubmit = (data) => console.log(data);

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input
        {...register("username", {
          required: "Username is required",
          validate: checkUsernameAvailability,
        })}
      />
      {errors.username && <span>{errors.username.message}</span>}

      <button type="submit">Submit</button>
    </form>
  );
}
```

## Key Methods

### useForm() Hook

```jsx
const {
  register, // Register input fields
  handleSubmit, // Form submission handler
  formState, // Form state (errors, dirty, isValid, etc.)
  setValue, // Set field value programmatically
  getValues, // Get form values
  reset, // Reset form to default values
  trigger, // Trigger validation
  clearErrors, // Clear specific or all errors
  setError, // Set custom errors
  control, // Control object for Controller
} = useForm();
```

### Form State

```jsx
const {
  errors, // Validation errors
  dirty, // Form is dirty (has unsaved changes)
  dirtyFields, // Array of dirty field names
  isDirty, // Boolean indicating if form is dirty
  touched, // Array of touched field names
  touchedFields, // Object of touched field states
  isSubmitted, // Form has been submitted
  isSubmitting, // Form is currently submitting
  isValid, // Form passes all validations
  isValidating, // Form is currently validating
} = formState;
```

### Common Validation Rules

```jsx
register("fieldName", {
  required: "Field is required",
  minLength: { value: 3, message: "Minimum 3 characters" },
  maxLength: { value: 50, message: "Maximum 50 characters" },
  min: { value: 18, message: "Must be at least 18" },
  max: { value: 100, message: "Must be less than 100" },
  pattern: { value: /^\d+$/, message: "Numbers only" },
  validate: (value) => value === "expected" || "Custom validation failed",
});
```
