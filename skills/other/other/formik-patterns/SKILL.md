---
name: formik-patterns
description: 使用Formik进行表单处理和验证。在构建表单、实现验证或处理表单提交时使用。
---

# Formik 模式

## 基础表单设置

```tsx
import { useFormik } from "formik";
import * as yup from "yup";

const validationSchema = yup.object({
  email: yup.string().email("Invalid email").required("Email is required"),
  password: yup
    .string()
    .min(8, "Min 8 characters")
    .required("Password is required"),
});

const LoginForm = () => {
  const formik = useFormik({
    initialValues: {
      email: "",
      password: "",
    },
    validationSchema,
    onSubmit: async (values) => {
      await loginMutation({ variables: { input: values } });
    },
  });

  return (
    <VStack gap="$4">
      <Input
        label="Email"
        value={formik.values.email}
        onChangeText={formik.handleChange("email")}
        onBlur={formik.handleBlur("email")}
        error={formik.touched.email ? formik.errors.email : undefined}
        keyboardType="email-address"
        autoCapitalize="none"
      />

      <Input
        label="Password"
        value={formik.values.password}
        onChangeText={formik.handleChange("password")}
        onBlur={formik.handleBlur("password")}
        error={formik.touched.password ? formik.errors.password : undefined}
        secureTextEntry
      />

      <Button
        onPress={formik.handleSubmit}
        isDisabled={!formik.isValid || formik.isSubmitting}
        isLoading={formik.isSubmitting}
      >
        Login
      </Button>
    </VStack>
  );
};
```

## 验证模式

### 常见模式

```typescript
import * as yup from "yup";

// 邮箱
email: yup.string().email("邮箱格式无效").required("邮箱为必填项");

// 带要求的密码
password: yup
  .string()
  .min(8, "至少需要8个字符")
  .matches(/[a-z]/, "必须包含小写字母")
  .matches(/[A-Z]/, "必须包含大写字母")
  .matches(/[0-9]/, "必须包含数字")
  .required("密码为必填项");

// 确认密码
confirmPassword: yup
  .string()
  .oneOf([yup.ref("password")], "密码必须匹配")
  .required("请确认密码");

// 电话号码
phone: yup
  .string()
  .matches(/^\+?[1-9]\d{1,14}$/, "电话号码无效")
  .required("电话号码为必填项");

// 可选字段，当存在时需要验证
website: yup.string().url("必须是有效的URL").nullable();

// 带范围的数字
quantity: yup
  .number()
  .min(1, "最小值为1")
  .max(100, "最大值为100")
  .required("数量为必填项");

// 最少项数的数组
tags: yup.array().of(yup.string()).min(1, "至少选择一个标签");
```

### 条件验证

```typescript
const schema = yup.object({
  hasCompany: yup.boolean(),
  companyName: yup.string().when("hasCompany", {
    is: true,
    then: (schema) => schema.required("公司名称为必填项"),
    otherwise: (schema) => schema.nullable(),
  }),
});
```

## 表单字段助手

### 输入字段助手

```tsx
const getFieldProps = (name: keyof typeof formik.values) => ({
  value: formik.values[name],
  onChangeText: formik.handleChange(name),
  onBlur: formik.handleBlur(name),
  error: formik.touched[name] ? formik.errors[name] : undefined,
});

// Usage
<Input label="Email" {...getFieldProps("email")} />;
```

### 选择框/选择器助手

```tsx
<Select
  label="Country"
  value={formik.values.country}
  onValueChange={(value) => formik.setFieldValue("country", value)}
  error={formik.touched.country ? formik.errors.country : undefined}
  options={countryOptions}
/>
```

## 使用GraphQL的表单提交

```tsx
const CreateItemForm = () => {
  const [createItem] = useCreateItemMutation({
    onCompleted: () => {
      toast.success({ title: "项目已创建" });
      navigation.goBack();
    },
    onError: (error) => {
      console.error("createItem failed:", error);
      toast.error({ title: "创建项目失败" });
    },
  });

  const formik = useFormik({
    initialValues: { name: "", description: "" },
    validationSchema,
    onSubmit: async (values, { setSubmitting }) => {
      try {
        await createItem({ variables: { input: values } });
      } finally {
        setSubmitting(false);
      }
    },
  });

  return (
    <VStack gap="$4">
      {/* 表单字段 */}
      <Button
        onPress={formik.handleSubmit}
        isDisabled={!formik.isValid || formik.isSubmitting}
        isLoading={formik.isSubmitting}
      >
        创建
      </Button>
    </VStack>
  );
};
```

## 编辑表单（带初始值）

```tsx
const EditItemForm = ({ item }: { item: Item }) => {
  const [updateItem] = useUpdateItemMutation({
    onCompleted: () => toast.success({ title: "已保存" }),
    onError: (error) => {
      console.error("updateItem failed:", error);
      toast.error({ title: "保存失败" });
    },
  });

  const formik = useFormik({
    initialValues: {
      name: item.name,
      description: item.description ?? "",
    },
    enableReinitialize: true, // 当item属性改变时更新
    validationSchema,
    onSubmit: async (values) => {
      await updateItem({
        variables: { id: item.id, input: values },
      });
    },
  });

  // 追踪表单是否有更改
  const hasChanges = formik.dirty;

  return (
    <VStack gap="$4">
      {/* 表单字段 */}
      <Button
        onPress={formik.handleSubmit}
        isDisabled={!hasChanges || !formik.isValid || formik.isSubmitting}
        isLoading={formik.isSubmitting}
      >
        保存更改
      </Button>
    </VStack>
  );
};
```

## 表单状态助手

```tsx
const {
  values, // 当前表单值
  errors, // 验证错误
  touched, // 已被触碰的字段
  isValid, // 表单是否通过验证
  isSubmitting, // 是否正在提交
  dirty, // 值是否与初始值不同
  handleSubmit, // 提交处理器
  handleChange, // 改变处理器
  handleBlur, // 模糊处理器
  setFieldValue, // 设置单个字段
  setFieldTouched, // 标记字段已触碰
  resetForm, // 重置为初始值
  setSubmitting, // 控制提交状态
} = formik;
```

## 多步骤表单

```tsx
const MultiStepForm = () => {
  const [step, setStep] = useState(0);

  const formik = useFormik({
    initialValues: {
      // Step 1
      name: "",
      email: "",
      // Step 2
      address: "",
      city: "",
      // Step 3
      cardNumber: "",
    },
    validationSchema: stepSchemas[step],
    onSubmit: async (values) => {
      if (step < steps.length - 1) {
        setStep(step + 1);
      } else {
        await submitOrder(values);
      }
    },
  });

  return (
    <VStack>
      {step === 0 && <PersonalInfoStep formik={formik} />}
      {step === 1 && <AddressStep formik={formik} />}
      {step === 2 && <PaymentStep formik={formik} />}

      <HStack gap="$4">
        {step > 0 && (
          <Button variant="outline" onPress={() => setStep(step - 1)}>
            上一步
          </Button>
        )}
        <Button
          onPress={formik.handleSubmit}
          isDisabled={!formik.isValid}
          isLoading={formik.isSubmitting}
        >
          {step < steps.length - 1 ? "下一步" : "提交"}
        </Button>
      </HStack>
    </VStack>
  );
};
```

## 反面模式

```tsx
// 错误 - 未显示验证错误
<Input
  value={formik.values.email}
  onChangeText={formik.handleChange('email')}
/>

// 正确 - 触碰时显示错误
<Input
  value={formik.values.email}
  onChangeText={formik.handleChange('email')}
  onBlur={formik.handleBlur('email')}
  error={formik.touched.email ? formik.errors.email : undefined}
/>


// 错误 - 提交按钮始终启用
<Button onPress={formik.handleSubmit}>提交</Button>

// 正确 - 在无效或提交时禁用
<Button
  onPress={formik.handleSubmit}
  isDisabled={!formik.isValid || formik.isSubmitting}
  isLoading={formik.isSubmitting}
>
  提交
</Button>


// 错误 - mutation上没有错误处理
onSubmit: async (values) => {
  await createItem({ variables: { input: values } });
}

// 正确 - 处理错误
onSubmit: async (values, { setSubmitting }) => {
  try {
    await createItem({ variables: { input: values } });
  } catch (error) {
    toast.error({ title: '保存失败' });
  } finally {
    setSubmitting(false);
  }
}
```

## 与其他技能的集成

- **graphql-schema**: Mutation提交模式
- **react-ui-patterns**: 加载/错误状态
- **testing-patterns**: 测试表单验证和提交
