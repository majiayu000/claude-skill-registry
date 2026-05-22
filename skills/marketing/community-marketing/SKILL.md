---
name: community-marketing
description: Эксперт по community-маркетингу. Используй для построения сообществ, engagement стратегий, community-led growth и модерации.
---

# Community Marketing Expert

Стратегическая экспертиза в построении и развитии бренд-сообществ.

## Core Competencies

### Community Strategy
- Community purpose definition
- Platform selection
- Governance design
- Launch planning
- Growth strategy

### Community Management
- Content programming
- Engagement facilitation
- Moderation
- Member recognition
- Conflict resolution

### Community Growth
- Acquisition tactics
- Activation programs
- Retention strategies
- Ambassador programs
- Advocacy development

## Типы сообществ

### Customer Communities
- Support communities
- User groups
- Product feedback
- Best practice sharing

### Professional Communities
- Industry discussions
- Career development
- Networking
- Knowledge sharing

### Brand Communities
- Fan communities
- Lifestyle groups
- Interest-based
- Mission-driven

## Выбор платформы

| Платформа | Лучше для | Особенности |
|-----------|-----------|-------------|
| Slack | B2B, engaged | Real-time, может быть шумно |
| Discord | Tech, gaming | Много функций, нужно учиться |
| Circle | Курсы, membership | Платная, профессиональная |
| Discourse | Tech, open source | Асинхронная, поисковая |
| Facebook Groups | B2C, mainstream | Зависит от алгоритма |
| LinkedIn Groups | B2B professional | Ограниченные функции |
| Telegram | Быстрая коммуникация | Простота, но мало инструментов |

## Engagement Programming

### Контент-календарь

| День | Активность |
|------|------------|
| Пн | Еженедельный вопрос для обсуждения |
| Вт | Шеринг полезных ресурсов |
| Ср | Spotlight участника |
| Чт | AMA с экспертом |
| Пт | Wins of the week |

### Типы событий

- AMAs с экспертами
- Office hours
- Вебинары
- Challenges
- Митапы
- Годовая конференция

## Community Metrics

| Метрика | Что измеряет |
|---------|--------------|
| Active members | MAU — Monthly Active Users |
| Engagement rate | (Posts + Comments) / Members |
| Growth rate | New members / Period |
| Retention | Members still active |
| NPS | Member satisfaction |
| UGC volume | User-generated content |

### Health Score Formula

```javascript
const communityHealth = {
  engagement: activeMembers / totalMembers * 100,
  growth: (newMembers - churnedMembers) / totalMembers * 100,
  sentiment: positiveInteractions / totalInteractions * 100,

  calculateScore() {
    return (this.engagement * 0.4) +
           (this.growth * 0.3) +
           (this.sentiment * 0.3);
  }
};
```

## Ambassador Program

### Структура программы

```yaml
Уровни:
  1. Member:
    - Активное участие
    - Помощь новичкам

  2. Contributor:
    - Создание контента
    - Ответы на вопросы
    - 3+ месяца активности

  3. Ambassador:
    - Ведение событий
    - Менторство
    - Представление бренда

  4. Champion:
    - Стратегический input
    - Лидерство инициатив
    - Доступ к roadmap

Награды:
  - Эксклюзивный контент
  - Early access к продуктам
  - Swag и merchandise
  - Приглашения на события
  - Networking opportunities
  - LinkedIn recommendations
```

### Отбор амбассадоров

```markdown
**Критерии:**
- [ ] Минимум 6 месяцев активного участия
- [ ] 50+ качественных contributions
- [ ] Положительный фидбек от других участников
- [ ] Alignment с ценностями бренда
- [ ] Готовность к публичной активности

**Процесс:**
1. Self-nomination или номинация
2. Review engagement history
3. Interview call
4. Trial period (1 месяц)
5. Official onboarding
```

## Moderation Framework

### Правила сообщества

```markdown
# Community Guidelines

## Мы приветствуем:
- Конструктивные обсуждения
- Взаимопомощь и поддержку
- Sharing опыта и знаний
- Вежливое несогласие

## Недопустимо:
- Спам и самопиар
- Оскорбления и harassment
- Off-topic контент
- Нарушение конфиденциальности

## Последствия:
1. Предупреждение
2. Временный mute (24h)
3. Временный ban (7 дней)
4. Перманентный ban
```

### Escalation Matrix

| Нарушение | Действие | Ответственный |
|-----------|----------|---------------|
| Minor (off-topic) | Warning | Moderator |
| Moderate (spam) | Mute 24h | Moderator |
| Serious (harassment) | Ban 7d | Community Manager |
| Severe (threats) | Perm ban | Community Lead + Legal |

## Activation Campaigns

### Onboarding Flow

```yaml
День 1:
  - Welcome message
  - Intro prompt: "Расскажи о себе"
  - Guide по навигации

День 3:
  - Check-in: "Как дела?"
  - Приглашение в discussion thread

День 7:
  - Resource digest
  - Приглашение на event

День 14:
  - Feedback survey
  - Advanced tips

День 30:
  - Ambassador program info
  - Recognition for activity
```

### Re-engagement Campaign

```markdown
**Для неактивных 30+ дней:**

Subject: Мы скучаем по тебе, {name}! 👋

Привет {name}!

Заметили, что тебя давно не было в сообществе.
За это время произошло много интересного:

- 🎉 Запустили новую функцию X
- 📚 Опубликовали гайд по Y
- 🎙️ Провели AMA с экспертом Z

Возвращайся — у нас для тебя специальный бонус!

[Вернуться в сообщество]
```

## Community-Led Growth

### Flywheel Model

```
Content → Engagement → Trust → Advocacy → Growth → Content
```

### Referral Program

```javascript
const referralProgram = {
  rewards: {
    referrer: {
      1: "Exclusive badge",
      5: "1 month premium",
      10: "Lifetime premium",
      25: "Ambassador status"
    },
    referee: "7 days premium trial"
  },

  tracking: {
    uniqueLink: true,
    utmParameters: true,
    attribution: "first-touch"
  }
};
```

## Content Strategy

### User-Generated Content

```yaml
Форматы UGC:
  - Case studies от участников
  - Tutorial videos
  - Templates и resources
  - Q&A threads
  - Success stories

Incentives:
  - Featured placement
  - Social amplification
  - Rewards points
  - Expert badges
```

### Curation Framework

```markdown
**Weekly Digest структура:**

1. **Top Discussion** — самый engaging тред
2. **Member Spotlight** — интересный участник
3. **Resource Pick** — полезный материал
4. **Upcoming Events** — что планируется
5. **Quick Wins** — успехи участников
```

## Measurement Dashboard

```yaml
Metrics to track:
  Growth:
    - New members (daily/weekly/monthly)
    - Churn rate
    - Referral signups

  Engagement:
    - DAU/MAU ratio
    - Posts per member
    - Response rate
    - Time to first response

  Quality:
    - NPS score
    - Sentiment analysis
    - Support deflection rate

  Business Impact:
    - Community-influenced revenue
    - Product feedback implemented
    - Support cost savings
```

## Лучшие практики

1. **Start small** — лучше engaged 100, чем passive 1000
2. **Lead by example** — team должна быть активна
3. **Celebrate wins** — признавайте contributions
4. **Listen actively** — community = source of truth
5. **Iterate constantly** — тестируйте и адаптируйте
6. **Document everything** — playbooks для масштабирования
