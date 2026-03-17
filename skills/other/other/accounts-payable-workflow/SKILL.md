---
name: accounts-payable-workflow
description: Эксперт AP workflow. Используй для процессов кредиторской задолженности, invoice processing, three-way matching и payment automation.
---

# Accounts Payable Workflow Expert

Эксперт по рабочим процессам кредиторской задолженности.

## Основные принципы

### Трехстороннее сопоставление
- **Заказ на покупку (PO)**: Авторизация на покупку
- **Получение товара**: Доказательство поставки
- **Счет поставщика**: Запрос на оплату
- Все три документа должны совпадать перед утверждением

### Разделение обязанностей
- Ввод и утверждение счетов — разные люди
- Авторизация платежей отдельно от исполнения
- Изменения поставщика требуют двойного утверждения

## Автоматизированный рабочий процесс

```python
class APWorkflowEngine:
    def __init__(self):
        self.tolerance_price = 0.05  # 5%
        self.tolerance_qty = 0.02    # 2%

    def process_invoice(self, invoice):
        # 1. Захват данных и валидация
        extracted_data = self.ocr_extract(invoice)
        validation = self.validate_invoice_data(extracted_data)

        if not validation.is_valid:
            return self.route_to_exception_queue(invoice)

        # 2. Трехстороннее сопоставление
        matching = self.perform_three_way_match(extracted_data)

        if matching.has_exceptions:
            if matching.within_tolerance(self.tolerance_price, self.tolerance_qty):
                return self.route_for_payment(extracted_data)
            else:
                return self.route_for_approval(extracted_data, matching)

        # 3. Маршрутизация по матрице утверждений
        return self.route_based_on_amount(extracted_data)
```

## Матрица утверждений

```yaml
approval_matrix:
  department_managers:
    amount_limit: 10000
    auto_approve_tolerance: 0.02

  finance_director:
    amount_limit: 50000
    requires_backup_documentation: true

  cfo_approval:
    amount_limit: 250000
    requires_board_notification: true
```

## Обнаружение дубликатов

```python
def detect_duplicates(new_invoice):
    # Точные совпадения
    exact = db.query(
        "SELECT * FROM invoices WHERE vendor_id = ? AND invoice_number = ?",
        new_invoice.vendor_id, new_invoice.invoice_number
    )

    # Нечеткое сопоставление
    potential = db.query(
        """SELECT * FROM invoices
           WHERE vendor_id = ?
           AND invoice_date BETWEEN ? AND ?
           AND ABS(amount - ?) < ?""",
        new_invoice.vendor_id,
        new_invoice.invoice_date - timedelta(days=30),
        new_invoice.invoice_date + timedelta(days=30),
        new_invoice.amount,
        new_invoice.amount * 0.05
    )

    return {'exact': exact, 'potential': potential}
```

## Оптимизация платежей

```python
class PaymentScheduler:
    def optimize_payment_schedule(self, approved_invoices):
        for invoice in approved_invoices:
            # Скидка за досрочную оплату
            discount_deadline = invoice.due_date - timedelta(days=invoice.early_pay_days)
            discount_value = invoice.amount * (invoice.early_pay_rate / 100)

            if discount_deadline >= date.today() and discount_value > 100:
                payment_date = discount_deadline
                payment_amount = invoice.amount - discount_value
            else:
                payment_date = invoice.due_date - timedelta(days=2)
                payment_amount = invoice.amount

            yield {
                'invoice_id': invoice.id,
                'payment_date': payment_date,
                'payment_amount': payment_amount,
                'discount_captured': discount_value
            }
```

## KPI мониторинг

```python
def generate_ap_metrics(start_date, end_date):
    return {
        'processing_efficiency': {
            'average_processing_time': calc_avg_time(start_date, end_date),
            'straight_through_rate': calc_stp_rate(start_date, end_date),
            'exception_rate': calc_exception_rate(start_date, end_date)
        },
        'cost_savings': {
            'early_payment_discounts': sum_discounts(start_date, end_date),
            'duplicates_prevented': count_duplicates(start_date, end_date)
        },
        'compliance': {
            'three_way_match_rate': calc_3way_compliance(start_date, end_date),
            'sod_violations': count_sod_violations(start_date, end_date)
        }
    }
```

## Лучшие практики

- Используйте OCR и ML для автоматизации ввода данных
- Внедрите портал самообслуживания для поставщиков
- Шифруйте банковскую информацию
- Поддерживайте полный аудиторский след
- Тестируйте соответствие SOX регулярно
