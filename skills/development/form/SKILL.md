---
name: form
description: Generate forms with React Hook Form and Zod validation following established patterns. Use when creating forms, input validation, modal forms, or handling user input.
---

# Form Generator

Generate forms using React Hook Form with Zod validation following established patterns.

## Directory Structure

```
src/
├── schema/
│   └── myFeature.ts        # Zod schemas + default values
├── constants/
│   └── message.ts          # Validation error messages
└── components/
    └── MyForm/
        └── index.tsx
```

## Schema File Pattern

```tsx
// src/schema/user.ts
import { z } from 'zod';
import { FORM_VALIDATION } from '@/constants/message';

const amountAboveZeroRefiner = (value: string) => 0 < Number(value);

export const userSchema = z.object({
  name: z.string().min(1, FORM_VALIDATION.NAME_REQUIRED),
  email: z.string().email(FORM_VALIDATION.INVALID_EMAIL),
  amount: z.string()
    .min(1, FORM_VALIDATION.AMOUNT_REQUIRED)
    .refine(amountAboveZeroRefiner, {
      message: FORM_VALIDATION.AMOUNT_MUST_BE_POSITIVE,
    }),
  frequency: z.enum(['weekly', 'fortnightly', 'monthly']),
  startDate: z.date(),
  endDate: z.date().optional(),
});

export type UserFormData = z.infer<typeof userSchema>;

export const userDefaultValues: UserFormData = {
  name: '',
  email: '',
  amount: '',
  frequency: 'monthly',
  startDate: new Date(),
  endDate: undefined,
};
```

## Validation Messages

```tsx
// src/constants/message.ts
export enum FORM_VALIDATION {
  NAME_REQUIRED = 'Name is required',
  INVALID_EMAIL = 'Please enter a valid email address',
  AMOUNT_REQUIRED = 'Amount is required',
  AMOUNT_MUST_BE_POSITIVE = 'Amount must be greater than zero',
  DATE_REQUIRED = 'Date is required',
  DATE_MUST_BE_FUTURE = 'Date must be in the future',
  PASSWORD_MIN_LENGTH = 'Password must be at least 8 characters',
}
```

## Basic Form Pattern

```tsx
import React from 'react';
import { View } from 'react-native';
import { useForm, Controller, FormProvider } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';

import { Button, Input } from '@/components';
import { userSchema, userDefaultValues, UserFormData } from '@/schema/user';

interface UserFormProps {
  onSubmit: (data: UserFormData) => void;
  initialValues?: Partial<UserFormData>;
}

const UserForm: React.FC<UserFormProps> = ({ onSubmit, initialValues }) => {
  const form = useForm<UserFormData>({
    resolver: zodResolver(userSchema),
    defaultValues: { ...userDefaultValues, ...initialValues },
  });

  const { control, handleSubmit, formState: { errors, isSubmitting } } = form;

  return (
    <FormProvider {...form}>
      <View className="gap-4">
        <Controller
          control={control}
          name="name"
          render={({ field: { onChange, onBlur, value } }) => (
            <Input
              label="Name"
              placeholder="Enter name"
              value={value}
              onChangeText={onChange}
              onBlur={onBlur}
              error={errors.name}
            />
          )}
        />

        <Controller
          control={control}
          name="email"
          render={({ field: { onChange, onBlur, value } }) => (
            <Input
              label="Email"
              placeholder="Enter email"
              keyboardType="email-address"
              autoCapitalize="none"
              value={value}
              onChangeText={onChange}
              onBlur={onBlur}
              error={errors.email}
            />
          )}
        />

        <Button
          title="Submit"
          onPress={handleSubmit(onSubmit)}
          isLoading={isSubmitting}
        />
      </View>
    </FormProvider>
  );
};

export default UserForm;
```

## Modal Form Pattern

```tsx
import React, { useState } from 'react';
import { View, Text, TouchableOpacity } from 'react-native';
import { useForm, Controller } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import Modal from 'react-native-modal';
import { SafeAreaView } from 'react-native-safe-area-context';
import { X } from 'lucide-react-native';

import { Button, Input, DatePicker, Picker } from '@/components';
import { MODAL_ANIMATION_DURATION } from '@/constants/common';
import { paymentSchema, paymentDefaultValues, PaymentFormData } from '@/schema/payment';

interface PaymentModalProps {
  isVisible: boolean;
  minDate: Date;
  onClose: () => void;
  onSubmit: (data: PaymentFormData) => void;
}

const PaymentModal: React.FC<PaymentModalProps> = ({
  isVisible,
  minDate,
  onClose,
  onSubmit,
}) => {
  const [showDatePicker, setShowDatePicker] = useState(false);

  const form = useForm<PaymentFormData>({
    resolver: zodResolver(paymentSchema),
    defaultValues: { ...paymentDefaultValues, date: minDate },
  });

  const { control, handleSubmit, reset, formState: { errors, isSubmitting } } = form;

  const handleClose = () => {
    setShowDatePicker(false);
    reset();
    onClose();
  };

  const handleFormSubmit = (data: PaymentFormData) => {
    setTimeout(() => onSubmit(data), MODAL_ANIMATION_DURATION);
    handleClose();
  };

  return (
    <Modal
      isVisible={isVisible}
      onBackdropPress={handleClose}
      animationIn="fadeInUp"
      animationOut="fadeOutDown"
      backdropTransitionOutTiming={0}
      hideModalContentWhileAnimating={true}
      useNativeDriverForBackdrop={true}
      backdropOpacity={0.5}
      style={{ justifyContent: 'flex-end', margin: 0 }}
    >
      <SafeAreaView className="rounded-t-2xl bg-background p-6">
        <View className="mb-4 flex-row items-center justify-between">
          <Text className="text-lg font-semibold text-foreground">Add Payment</Text>
          <TouchableOpacity onPress={handleClose} className="p-1">
            <X color="hsl(var(--muted-foreground))" size={20} />
          </TouchableOpacity>
        </View>

        <View className="gap-4">
          <Controller
            control={control}
            name="amount"
            render={({ field: { onChange, onBlur, value } }) => (
              <Input
                label="Amount"
                placeholder="Enter amount"
                keyboardType="numeric"
                value={value}
                onChangeText={onChange}
                onBlur={onBlur}
                error={errors.amount}
              />
            )}
          />

          <Controller
            control={control}
            name="date"
            render={({ field: { onChange, value } }) => (
              <View className="gap-2">
                <Text className="text-base font-medium text-foreground">Date</Text>
                <TouchableOpacity
                  onPress={() => setShowDatePicker(true)}
                  className="flex-row items-center justify-between rounded-2xl border-2 border-border bg-background px-4 py-3"
                >
                  <Text className="text-base text-foreground">
                    {value.toLocaleDateString()}
                  </Text>
                </TouchableOpacity>
                {showDatePicker && (
                  <DatePicker
                    initialDate={value}
                    minimumDate={minDate}
                    onDateSelected={(date) => {
                      onChange(date);
                      setShowDatePicker(false);
                    }}
                    onClose={() => setShowDatePicker(false)}
                  />
                )}
              </View>
            )}
          />

          <Button
            title="Add Payment"
            onPress={handleSubmit(handleFormSubmit)}
            isLoading={isSubmitting}
          />
        </View>
      </SafeAreaView>
    </Modal>
  );
};

export default PaymentModal;
```

## Dynamic Field Dependencies

```tsx
const [lockedField, setLockedField] = useState<'propertyValue' | 'loanAmount' | 'lvr'>('loanAmount');

const updateCalculatedFields = () => {
  const propertyValue = parseFloat(form.getValues('propertyValue') || '0');
  const loanAmount = parseFloat(form.getValues('loanAmount') || '0');
  const lvr = form.getValues('lvr');

  if (lockedField === 'loanAmount') {
    form.setValue('loanAmount', ((propertyValue * lvr) / 100).toString());
  } else if (lockedField === 'propertyValue') {
    form.setValue('propertyValue', ((loanAmount / lvr) * 100).toString());
  } else {
    form.setValue('lvr', Math.round((loanAmount / propertyValue) * 100));
  }
};

<Controller
  control={control}
  name="propertyValue"
  render={({ field: { onChange, ...rest } }) => (
    <Input
      {...rest}
      onChangeText={(value) => {
        onChange(value);
        if (lockedField !== 'propertyValue') updateCalculatedFields();
      }}
    />
  )}
/>
```

## Form with Picker

```tsx
<Controller
  control={control}
  name="frequency"
  render={({ field: { onChange, value } }) => (
    <Picker
      label="Frequency"
      placeholder="Select frequency"
      value={value}
      options={[
        { value: 'weekly', label: 'Weekly', description: 'Every 7 days' },
        { value: 'fortnightly', label: 'Fortnightly', description: 'Every 14 days' },
        { value: 'monthly', label: 'Monthly', description: 'Once a month' },
      ]}
      onValueChange={onChange}
      error={errors.frequency}
    />
  )}
/>
```

## Common Zod Patterns

```tsx
// String as number
const amountString = z.string()
  .min(1, 'Required')
  .refine((v) => !isNaN(parseFloat(v)), 'Must be a number')
  .refine((v) => parseFloat(v) > 0, 'Must be positive');

// Date range validation
const dateRangeSchema = z.object({
  startDate: z.date(),
  endDate: z.date(),
}).refine((data) => data.endDate > data.startDate, {
  message: 'End date must be after start date',
  path: ['endDate'],
});

// Conditional validation
const conditionalSchema = z.object({
  hasEndDate: z.boolean(),
  endDate: z.date().optional(),
}).refine(
  (data) => !data.hasEndDate || data.endDate !== undefined,
  { message: 'End date required', path: ['endDate'] }
);
```

## Form Utilities

```tsx
form.reset();
form.reset(newDefaultValues);
form.setValue('field', value);
form.setError('field', { message: 'Error' });
form.clearErrors();
form.watch('field');
form.getValues();
form.trigger();
```

## Checklist

- [ ] Schema in `src/schema/` with type + defaults export
- [ ] Messages in `src/constants/message.ts`
- [ ] `useForm` with `zodResolver`
- [ ] `Controller` for each field
- [ ] Error passed to components
- [ ] `isSubmitting` for loading state
- [ ] `reset()` on modal close
- [ ] `MODAL_ANIMATION_DURATION` delay before callbacks
