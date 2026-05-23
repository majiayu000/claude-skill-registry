---
name: Customer Feedback Collection and Management
description: Gathering, analyzing, and acting on user input through surveys, feedback widgets, rating systems, sentiment analysis, and integration with product roadmap to improve products and services.
---

# Customer Feedback Collection and Management

> **Current Level:** Intermediate  
> **Domain:** Customer Support / Product

---

## Overview

Customer feedback collection enables businesses to gather, analyze, and act on user input to improve products and services. Effective feedback systems include multiple collection methods, sentiment analysis, categorization, routing, and integration with product development.

---

## Core Concepts

### Table of Contents

1. [Feedback Collection Methods](#feedback-collection-methods)
2. [Survey Design](#survey-design)
3. [Feedback Widgets](#feedback-widgets)
4. [Rating Systems](#rating-systems)
5. [Feedback Categorization](#feedback-categorization)
6. [Sentiment Analysis](#sentiment-analysis)
7. [Feedback Routing](#feedback-routing)
8. [Response Management](#response-management)
9. [Analytics and Reporting](#analytics-and-reporting)
10. [Integration with Product Roadmap](#integration-with-product-roadmap)
11. [Tools](#tools)
12. [Best Practices](#best-practices)

---

## Feedback Collection Methods

### In-App Surveys

```typescript
interface InAppSurvey {
  id: string;
  name: string;
  type: 'nps' | 'csat' | 'ces' | 'custom';
  trigger: SurveyTrigger;
  questions: SurveyQuestion[];
  targeting: SurveyTargeting;
  status: 'draft' | 'active' | 'paused' | 'archived';
}

interface SurveyTrigger {
  type: 'event' | 'time' | 'session_count' | 'feature_usage';
  config: Record<string, any>;
}

interface SurveyQuestion {
  id: string;
  type: 'rating' | 'text' | 'multiple_choice' | 'checkbox';
  question: string;
  options?: string[];
  required: boolean;
  min?: number;
  max?: number;
}

class InAppSurveyManager {
  constructor(private prisma: PrismaClient) {}

  /**
   * Create survey
   */
  async createSurvey(survey: Omit<InAppSurvey, 'id' | 'status'>): Promise<string> {
    const created = await this.prisma.inAppSurvey.create({
      data: {
        ...survey,
        status: 'draft',
      },
    });

    return created.id;
  }

  /**
   * Trigger survey
   */
  async triggerSurvey(
    surveyId: string,
    userId: string,
    context?: Record<string, any>
  ): Promise<void> {
    const survey = await this.prisma.inAppSurvey.findUnique({
      where: { id: surveyId },
      include: { questions: true },
    });

    if (!survey || survey.status !== 'active') {
      return;
    }

    // Check targeting
    const eligible = await this.checkEligibility(survey, userId, context);
    if (!eligible) return;

    // Create survey instance
    const instance = await this.prisma.surveyInstance.create({
      data: {
        surveyId,
        userId,
        context,
        status: 'pending',
        expiresAt: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000), // 7 days
      },
    });

    // Send notification
    await this.sendSurveyNotification(userId, instance.id, survey);
  }

  /**
   * Check survey eligibility
   */
  private async checkEligibility(
    survey: InAppSurvey,
    userId: string,
    context?: Record<string, any>
  ): Promise<boolean> {
    // Check user targeting
    if (survey.targeting.userSegments && survey.targeting.userSegments.length > 0) {
      const userSegments = await this.getUserSegments(userId);
      const hasRequiredSegment = survey.targeting.userSegments.some(segment =>
        userSegments.includes(segment)
      );

      if (!hasRequiredSegment) return false;
    }

    // Check trigger conditions
    if (survey.trigger.type === 'event') {
      const lastEvent = await this.getLastEvent(userId, survey.trigger.config.eventName);
      if (!lastEvent) return false;

      const eventAge = Date.now() - new Date(lastEvent.createdAt).getTime();
      const minDelay = survey.trigger.config.minDelay || 0;

      if (eventAge < minDelay) return false;
    }

    // Check if already responded
    const existingResponse = await this.prisma.surveyResponse.findFirst({
      where: {
        surveyId,
        userId,
      },
    });

    if (existingResponse) return false;

    return true;
  }

  /**
   * Submit survey response
   */
  async submitResponse(params: {
    instanceId: string;
    userId: string;
    answers: Record<string, any>;
  }): Promise<void> {
    const instance = await this.prisma.surveyInstance.findUnique({
      where: { id: params.instanceId },
      include: { survey: true },
    });

    if (!instance || instance.status !== 'pending') {
      throw new Error('Survey instance not found or already completed');
    }

    // Check expiry
    if (instance.expiresAt && instance.expiresAt < new Date()) {
      throw new Error('Survey has expired');
    }

    // Save response
    await this.prisma.surveyResponse.create({
      data: {
        instanceId: params.instanceId,
        userId: params.userId,
        answers: params.answers,
        submittedAt: new Date(),
      },
    });

    // Update instance
    await this.prisma.surveyInstance.update({
      where: { id: params.instanceId },
      data: { status: 'completed' },
    });

    // Trigger follow-up actions
    await this.handleSurveyResponse(instance.survey, params.answers);
  }

  /**
   * Handle survey response
   */
  private async handleSurveyResponse(
    survey: any,
    answers: Record<string, any>
  ): Promise<void> {
    switch (survey.type) {
      case 'nps':
        await this.handleNPSResponse(survey, answers);
        break;
      case 'csat':
        await this.handleCSATResponse(survey, answers);
        break;
      case 'ces':
        await this.handleCESResponse(survey, answers);
        break;
      default:
        await this.handleCustomResponse(survey, answers);
    }
  }

  private async handleNPSResponse(survey: any, answers: Record<string, any>): Promise<void> {
    const score = answers['score'];
    const category = this.getNPSCategory(score);

    await this.prisma.npsScore.create({
      data: {
        surveyId: survey.id,
        score,
        category,
        comment: answers['comment'],
      },
    });
  }

  private getNPSCategory(score: number): 'detractor' | 'passive' | 'promoter' {
    if (score >= 9) return 'promoter';
    if (score >= 7) return 'passive';
    return 'detractor';
  }

  private async sendSurveyNotification(
    userId: string,
    instanceId: string,
    survey: any
  ): Promise<void> {
    // Implement notification logic
    console.log(`Sending survey ${survey.id} to user ${userId}`);
  }

  private async getLastEvent(userId: string, eventName: string): Promise<any> {
    // Implement event tracking
    return null;
  }

  private async getUserSegments(userId: string): Promise<string[]> {
    // Implement user segmentation
    return [];
  }

  constructor(private prisma: PrismaClient) {}
}
```

### Email Surveys

```typescript
class EmailSurveyManager {
  constructor(private prisma: PrismaClient) {}

  /**
   * Create email campaign
   */
  async createCampaign(params: {
    name: string;
    subject: string;
    fromEmail: string;
    templateId: string;
    recipientIds: string[];
    sendAt?: Date;
  }): Promise<string> {
    const campaign = await this.prisma.emailSurveyCampaign.create({
      data: {
        ...params,
        status: 'scheduled',
      },
    });

    // Schedule send
    if (params.sendAt) {
      await this.scheduleCampaignSend(campaign.id, params.sendAt);
    } else {
      await this.sendCampaign(campaign.id);
    }

    return campaign.id;
  }

  /**
   * Send campaign
   */
  private async sendCampaign(campaignId: string): Promise<void> {
    const campaign = await this.prisma.emailSurveyCampaign.findUnique({
      where: { id: campaignId },
      include: { recipients: true },
    });

    if (!campaign) {
      throw new Error('Campaign not found');
    }

    // Get template
    const template = await this.prisma.surveyTemplate.findUnique({
      where: { id: campaign.templateId },
    });

    // Send emails
    for (const recipient of campaign.recipients) {
      const surveyUrl = this.generateSurveyUrl(campaign.id, recipient.id);

      await emailService.send({
        to: recipient.email,
        subject: campaign.subject,
        from: campaign.fromEmail,
        templateId: campaign.templateId,
        dynamicTemplateData: {
          surveyUrl,
          recipientName: recipient.name,
        },
      });
    }

    // Update campaign status
    await this.prisma.emailSurveyCampaign.update({
      where: { id: campaignId },
      data: {
        status: 'sent',
        sentAt: new Date(),
      },
    });
  }

  /**
   * Generate survey URL
   */
  private generateSurveyUrl(campaignId: string, recipientId: string): string {
    const token = this.generateSurveyToken(campaignId, recipientId);

    return `${process.env.APP_URL}/survey/email/${campaignId}/${recipientId}?token=${token}`;
  }

  /**
   * Generate survey token
   */
  private generateSurveyToken(campaignId: string, recipientId: string): string {
    const crypto = require('crypto');
    return crypto
      .createHmac('sha256', process.env.SURVEY_SECRET!)
      .update(`${campaignId}:${recipientId}`)
      .digest('hex');
  }

  /**
   * Schedule campaign send
   */
  private async scheduleCampaignSend(campaignId: string, sendAt: Date): Promise<void> {
    // Implement scheduling logic
    console.log(`Scheduling campaign ${campaignId} for ${sendAt}`);
  }
}
```

---

## Survey Design

### Survey Templates

```typescript
interface SurveyTemplate {
  id: string;
  name: string;
  type: 'nps' | 'csat' | 'ces' | 'custom';
  subject?: string;
  htmlContent: string;
  textContent?: string;
  variables: TemplateVariable[];
}

interface TemplateVariable {
  name: string;
  description: string;
  type: 'text' | 'link' | 'rating';
  required: boolean;
}

// NPS Template
const npsTemplate: SurveyTemplate = {
  name: 'NPS Survey',
  type: 'nps',
  subject: 'How likely are you to recommend us?',
  htmlContent: `
    <html>
      <body>
        <h1>How likely are you to recommend [Company Name] to a friend or colleague?</h1>
        <div class="nps-scale">
          <button onclick="submitNPS(0)">0</button>
          <button onclick="submitNPS(1)">1</button>
          <button onclick="submitNPS(2)">2</button>
          <button onclick="submitNPS(3)">3</button>
          <button onclick="submitNPS(4)">4</button>
          <button onclick="submitNPS(5)">5</button>
          <button onclick="submitNPS(6)">6</button>
          <button onclick="submitNPS(7)">7</button>
          <button onclick="submitNPS(8)">8</button>
          <button onclick="submitNPS(9)">9</button>
          <button onclick="submitNPS(10)">10</button>
        </div>
        <textarea id="comment" placeholder="Please tell us why you gave this score"></textarea>
        <button onclick="submitSurvey()">Submit</button>
      </body>
    </html>
  `,
  variables: [
    { name: 'surveyUrl', description: 'Survey submission URL', type: 'link', required: true },
  ],
};

// CSAT Template
const csatTemplate: SurveyTemplate = {
  name: 'CSAT Survey',
  type: 'csat',
  subject: 'How was your experience?',
  htmlContent: `
    <html>
      <body>
        <h1>How would you rate your recent experience with us?</h1>
        <div class="rating-scale">
          <button onclick="submitRating(1)">😠</button>
          <button onclick="submitRating(2)">😞</button>
          <button onclick="submitRating(3)">😐</button>
          <button onclick="submitRating(4)">🙂</button>
          <button onclick="submitRating(5)">😄</button>
        </div>
        <textarea id="comment" placeholder="Please share your feedback"></textarea>
        <button onclick="submitSurvey()">Submit</button>
      </body>
    </html>
  `,
  variables: [
    { name: 'surveyUrl', description: 'Survey submission URL', type: 'link', required: true },
  ],
};

// CES Template
const cesTemplate: SurveyTemplate = {
  name: 'CES Survey',
  type: 'ces',
  subject: 'Was it easy to accomplish your task?',
  htmlContent: `
    <html>
      <body>
        <h1>How easy was it to accomplish your task?</h1>
        <div class="ces-scale">
          <button onclick="submitCES(1)">Very Difficult</button>
          <button onclick="submitCES(2)">Difficult</button>
          <button onclick="submitCES(3)">Neutral</button>
          <button onclick="submitCES(4)">Easy</button>
          <button onclick="submitCES(5)">Very Easy</button>
        </div>
        <textarea id="comment" placeholder="Please share your feedback"></textarea>
        <button onclick="submitSurvey()">Submit</button>
      </body>
    </html>
  `,
  variables: [
    { name: 'surveyUrl', description: 'Survey submission URL', type: 'link', required: true },
  ],
};
```

---

## Feedback Widgets

### React Feedback Widget

```tsx
import React, { useState } from 'react';

interface FeedbackWidgetProps {
  type: 'rating' | 'emoji' | 'thumbs';
  position?: 'bottom-right' | 'bottom-left' | 'top-right' | 'top-left';
  showOnLoad?: boolean;
  delay?: number; // in seconds
  onFeedback: (feedback: any) => void;
}

const FeedbackWidget: React.FC<FeedbackWidgetProps> = ({
  type,
  position = 'bottom-right',
  showOnLoad = false,
  delay = 30,
  onFeedback,
}) => {
  const [visible, setVisible] = useState(showOnLoad);

  React.useEffect(() => {
    if (!showOnLoad && delay > 0) {
      const timer = setTimeout(() => setVisible(true), delay * 1000);
      return () => clearTimeout(timer);
    }
  }, [showOnLoad, delay]);

  const handleSubmit = (feedback: any) => {
    onFeedback(feedback);
    setVisible(false);
  };

  const positionClasses: Record<string, string> = {
    'bottom-right': 'bottom-4 right-4',
    'bottom-left': 'bottom-4 left-4',
    'top-right': 'top-4 right-4',
    'top-left': 'top-4 left-4',
  };

  return (
    <div className={`feedback-widget ${positionClasses[position]} ${visible ? 'visible' : 'hidden'}`}>
      <button className="close-button" onClick={() => setVisible(false)}>
        ✕
      </button>

      {type === 'rating' && (
        <div className="rating-widget">
          <p>Rate your experience:</p>
          {[1, 2, 3, 4, 5].map(star => (
            <button
              key={star}
              onClick={() => handleSubmit({ type: 'rating', value: star })}
              className="star-button"
            >
              ★
            </button>
          ))}
        </div>
      )}

      {type === 'emoji' && (
        <div className="emoji-widget">
          <p>How was your experience?</p>
          <button onClick={() => handleSubmit({ type: 'emoji', value: '😠' })}>😠</button>
          <button onClick={() => handleSubmit({ type: 'emoji', value: '😞' })}>😞</button>
          <button onClick={() => handleSubmit({ type: 'emoji', value: '😐' })}>😐</button>
          <button onClick={() => handleSubmit({ type: 'emoji', value: '🙂' })}>🙂</button>
          <button onClick={() => handleSubmit({ type: 'emoji', value: '😄' })}>😄</button>
        </div>
      )}

      {type === 'thumbs' && (
        <div className="thumbs-widget">
          <p>Was this helpful?</p>
          <button onClick={() => handleSubmit({ type: 'thumbs', value: 'up' })}>
            👍
          </button>
          <button onClick={() => handleSubmit({ type: 'thumbs', value: 'down' })}>
            👎
          </button>
        </div>
      )}

      <div className="comment-section">
        <textarea
          placeholder="Tell us more..."
          rows={3}
        />
        <button onClick={() => handleSubmit({ type: 'comment', value: document.querySelector('textarea')?.value })}>
          Submit
        </button>
      </div>
    </div>
  );
};

export default FeedbackWidget;
```

---

## Rating Systems

### NPS (Net Promoter Score)

```typescript
interface NPSMetrics {
  surveyId: string;
  totalResponses: number;
  promoters: number; // 9-10
  passives: number; // 7-8
  detractors: number; // 0-6
  npsScore: number; // -100 to 100
  npsCategory: string;
}

class NPSManager {
  constructor(private prisma: PrismaClient) {}

  /**
   * Calculate NPS metrics
   */
  async calculateMetrics(surveyId: string): Promise<NPSMetrics> {
    const responses = await this.prisma.npsScore.findMany({
      where: { surveyId },
    });

    const promoters = responses.filter(r => r.score >= 9).length;
    const passives = responses.filter(r => r.score >= 7 && r.score <= 8).length;
    const detractors = responses.filter(r => r.score <= 6).length;
    const total = responses.length;

    if (total === 0) {
      return {
        surveyId,
        totalResponses: 0,
        promoters: 0,
        passives: 0,
        detractors: 0,
        npsScore: 0,
        npsCategory: 'no_data',
      };
    }

    const npsScore = ((promoters - detractors) / total) * 100;
    const npsCategory = this.getNPSCategory(npsScore);

    return {
      surveyId,
      totalResponses: total,
      promoters,
      passives,
      detractors,
      npsScore,
      npsCategory,
    };
  }

  /**
   * Get NPS category
   */
  private getNPSCategory(score: number): string {
    if (score >= 70) return 'excellent';
    if (score >= 50) return 'good';
    if (score >= 0) return 'average';
    if (score >= -50) return 'poor';
    return 'terrible';
  }

  /**
   * Get NPS trend
   */
  async getTrend(surveyId: string, days: number = 30): Promise<Array<{
    date: Date;
    npsScore: number;
    responseCount: number;
  }>> {
    const startDate = new Date(Date.now() - days * 24 * 60 * 60 * 1000);

    const responses = await this.prisma.npsScore.findMany({
      where: {
        surveyId,
        createdAt: { gte: startDate },
      },
      orderBy: { createdAt: 'asc' },
    });

    // Group by day
    const grouped = new Map<string, { scores: number[]; count: number }>();

    for (const response of responses) {
      const dateKey = response.createdAt.toISOString().split('T')[0];
      const existing = grouped.get(dateKey) || { scores: [], count: 0 };
      existing.scores.push(response.score);
      existing.count++;
      grouped.set(dateKey, existing);
    }

    // Calculate daily NPS
    return Array.from(grouped.entries()).map(([date, data]) => {
      const scores = data.scores;
      const promoters = scores.filter(s => s >= 9).length;
      const detractors = scores.filter(s => s <= 6).length;
      const npsScore = (scores.length > 0)
        ? ((promoters - detractors) / scores.length) * 100
        : 0;

      return {
        date: new Date(date),
        npsScore,
        responseCount: data.count,
      };
    });
  }
}
```

---

## Feedback Categorization

### Feedback Categorizer

```typescript
interface FeedbackCategory {
  id: string;
  name: string;
  type: 'feature_request' | 'bug_report' | 'complaint' | 'compliment' | 'question' | 'other';
  keywords: string[];
  priority: 'low' | 'medium' | 'high' | 'critical';
}

class FeedbackCategorizer {
  private categories: FeedbackCategory[];

  constructor() {
    this.categories = [
      {
        id: 'feature_request',
        name: 'Feature Request',
        type: 'feature_request',
        keywords: ['feature', 'request', 'add', 'new', 'would like', 'wish', 'suggestion'],
        priority: 'medium',
      },
      {
        id: 'bug_report',
        name: 'Bug Report',
        type: 'bug_report',
        keywords: ['bug', 'error', 'issue', 'problem', 'broken', 'not working', 'crash', 'glitch'],
        priority: 'high',
      },
      {
        id: 'complaint',
        name: 'Complaint',
        type: 'complaint',
        keywords: ['complaint', 'unhappy', 'disappointed', 'frustrated', 'poor', 'slow'],
        priority: 'high',
      },
      {
        id: 'compliment',
        name: 'Compliment',
        type: 'compliment',
        keywords: ['great', 'awesome', 'love', 'excellent', 'amazing', 'thanks', 'helpful'],
        priority: 'low',
      },
      {
        id: 'question',
        name: 'Question',
        type: 'question',
        keywords: ['how', 'what', 'why', 'question', 'help', 'support'],
        priority: 'medium',
      },
      {
        id: 'other',
        name: 'Other',
        type: 'other',
        keywords: [],
        priority: 'low',
      },
    ];
  }

  /**
   * Categorize feedback
   */
  categorize(feedback: {
    text?: string;
    rating?: number;
    type?: string;
  }): FeedbackCategory {
    const text = (feedback.text || '').toLowerCase();

    // Check for keyword matches
    for (const category of this.categories) {
      for (const keyword of category.keywords) {
        if (text.includes(keyword)) {
          return category;
        }
      }
    }

    // Check rating-based categorization
    if (feedback.rating !== undefined) {
      if (feedback.rating <= 2) {
        return this.categories.find(c => c.id === 'complaint')!;
      }
      if (feedback.rating >= 4) {
        return this.categories.find(c => c.id === 'compliment')!;
      }
    }

    // Check type-based categorization
    if (feedback.type) {
      const category = this.categories.find(c => c.id === feedback.type);
      if (category) return category;
    }

    // Default to question
    return this.categories.find(c => c.id === 'question')!;
  }

  /**
   * Get category by ID
   */
  getCategory(id: string): FeedbackCategory | undefined {
    return this.categories.find(c => c.id === id);
  }

  /**
   * Get all categories
   */
  getAllCategories(): FeedbackCategory[] {
    return this.categories;
  }
}
```

---

## Sentiment Analysis

### Sentiment Analyzer

```typescript
// npm install @tensorflow/tfjs-node
import * as tf from '@tensorflow/tfjs-node';

class SentimentAnalyzer {
  private model: tf.LayersModel | null = null;

  constructor() {
    this.loadModel();
  }

  /**
   * Load sentiment model
   */
  private async loadModel(): Promise<void> {
    // Load pre-trained model or train your own
    // This is a simplified example
    // In production, you'd use a proper ML model
    console.log('Loading sentiment model...');
  }

  /**
   * Analyze sentiment
   */
  async analyze(text: string): Promise<{
    sentiment: 'positive' | 'negative' | 'neutral';
    score: number; // -1 to 1
    confidence: number; // 0 to 1
  }> {
    if (!this.model) {
      // Fallback to rule-based analysis
      return this.ruleBasedAnalysis(text);
    }

    // Use ML model
    const prediction = await this.model.predict(tf.tensor([text]));

    return {
      sentiment: this.getSentimentLabel(prediction),
      score: parseFloat(prediction.dataSync()[0]),
      confidence: 0.85,
    };
  }

  /**
   * Rule-based sentiment analysis
   */
  private ruleBasedAnalysis(text: string): {
    sentiment: 'positive' | 'negative' | 'neutral';
    score: number;
    confidence: number;
  } {
    const lowerText = text.toLowerCase();

    const positiveWords = ['great', 'awesome', 'love', 'excellent', 'amazing', 'thanks', 'helpful', 'good', 'happy', 'pleased'];
    const negativeWords = ['terrible', 'awful', 'hate', 'disappointed', 'frustrated', 'poor', 'slow', 'broken', 'bug', 'error'];

    let positiveCount = 0;
    let negativeCount = 0;

    for (const word of positiveWords) {
      if (lowerText.includes(word)) positiveCount++;
    }

    for (const word of negativeWords) {
      if (lowerText.includes(word)) negativeCount++;
    }

    if (positiveCount > negativeCount) {
      return {
        sentiment: 'positive',
        score: 0.5,
        confidence: Math.min(positiveCount / 5, 1),
      };
    }

    if (negativeCount > positiveCount) {
      return {
        sentiment: 'negative',
        score: -0.5,
        confidence: Math.min(negativeCount / 5, 1),
      };
    }

    return {
      sentiment: 'neutral',
      score: 0,
      confidence: 0.5,
    };
  }

  /**
   * Get sentiment label from prediction
   */
  private getSentimentLabel(prediction: any): 'positive' | 'negative' | 'neutral' {
    const score = prediction.dataSync()[0];

    if (score > 0.3) return 'positive';
    if (score < -0.3) return 'negative';
    return 'neutral';
  }

  /**
   * Analyze batch
   */
  async analyzeBatch(texts: string[]): Promise<Array<{
    text: string;
    sentiment: string;
    score: number;
    confidence: number;
  }>> {
    const results = [];

    for (const text of texts) {
      const analysis = await this.analyze(text);
      results.push({
        text,
        ...analysis,
      });
    }

    return results;
  }
}
```

---

## Feedback Routing

### Feedback Router

```typescript
interface FeedbackRoute {
  id: string;
  name: string;
  conditions: RouteCondition[];
  destination: {
    type: 'email' | 'slack' | 'jira' | 'zendesk' | 'custom';
    config: Record<string, any>;
  };
  priority: number;
}

interface RouteCondition {
  field: 'category' | 'sentiment' | 'rating' | 'priority';
  operator: 'equals' | 'not_equals' | 'greater_than' | 'less_than' | 'in' | 'not_in';
  value: any;
}

class FeedbackRouter {
  private routes: FeedbackRoute[] = [];

  constructor() {
    this.setupDefaultRoutes();
  }

  /**
   * Setup default routes
   */
  private setupDefaultRoutes(): void {
    this.routes = [
      {
        id: 'critical_bug',
        name: 'Critical Bug Reports',
        priority: 1,
        conditions: [
          { field: 'category', operator: 'equals', value: 'bug_report' },
          { field: 'priority', operator: 'equals', value: 'critical' },
        ],
        destination: {
          type: 'slack',
          config: { channel: '#critical-issues' },
        },
      },
      {
        id: 'feature_requests',
        name: 'Feature Requests',
        priority: 5,
        conditions: [
          { field: 'category', operator: 'equals', value: 'feature_request' },
        ],
        destination: {
          type: 'jira',
          config: { project: 'FEAT' },
        },
      },
      {
        id: 'negative_feedback',
        name: 'Negative Feedback',
        priority: 3,
        conditions: [
          { field: 'sentiment', operator: 'equals', value: 'negative' },
        ],
        destination: {
          type: 'email',
          config: { recipients: ['support@company.com'] },
        },
      },
      {
        id: 'compliments',
        name: 'Compliments',
        priority: 10,
        conditions: [
          { field: 'category', operator: 'equals', value: 'compliment' },
        ],
        destination: {
          type: 'slack',
          config: { channel: '#kudos' },
        },
      },
    ];
  }

  /**
   * Route feedback
   */
  async routeFeedback(feedback: {
    category: string;
    sentiment: string;
    rating?: number;
    priority?: string;
    text: string;
    userId: string;
  }): Promise<void> {
    // Find matching route
    const route = this.findMatchingRoute(feedback);

    if (!route) {
      console.log('No matching route found for feedback');
      return;
    }

    // Send to destination
    await this.sendToDestination(route.destination, feedback);
  }

  /**
   * Find matching route
   */
  private findMatchingRoute(feedback: any): FeedbackRoute | null {
    const sortedRoutes = [...this.routes].sort((a, b) => a.priority - b.priority);

    for (const route of sortedRoutes) {
      if (this.matchesConditions(route.conditions, feedback)) {
        return route;
      }
    }

    return null;
  }

  /**
   * Check if feedback matches conditions
   */
  private matchesConditions(conditions: RouteCondition[], feedback: any): boolean {
    for (const condition of conditions) {
      const value = feedback[condition.field];

      let matches = false;

      switch (condition.operator) {
        case 'equals':
          matches = value === condition.value;
          break;
        case 'not_equals':
          matches = value !== condition.value;
          break;
        case 'greater_than':
          matches = typeof value === 'number' && value > condition.value;
          break;
        case 'less_than':
          matches = typeof value === 'number' && value < condition.value;
          break;
        case 'in':
          matches = Array.isArray(condition.value) && condition.value.includes(value);
          break;
        case 'not_in':
          matches = !Array.isArray(condition.value) || !condition.value.includes(value);
          break;
      }

      if (!matches) return false;
    }

    return true;
  }

  /**
   * Send to destination
   */
  private async sendToDestination(
    destination: FeedbackRoute['destination'],
    feedback: any
  ): Promise<void> {
    switch (destination.type) {
      case 'slack':
        await this.sendToSlack(destination.config, feedback);
        break;
      case 'email':
        await this.sendToEmail(destination.config, feedback);
        break;
      case 'jira':
        await this.sendToJira(destination.config, feedback);
        break;
      case 'zendesk':
        await this.sendToZendesk(destination.config, feedback);
        break;
      case 'custom':
        await this.sendToCustom(destination.config, feedback);
        break;
    }
  }

  private async sendToSlack(config: any, feedback: any): Promise<void> {
    // Implement Slack integration
    console.log(`Sending to Slack channel: ${config.channel}`);
  }

  private async sendToEmail(config: any, feedback: any): Promise<void> {
    // Implement email sending
    console.log(`Sending to email: ${config.recipients}`);
  }

  private async sendToJira(config: any, feedback: any): Promise<void> {
    // Implement Jira integration
    console.log(`Creating Jira issue in project: ${config.project}`);
  }

  private async sendToZendesk(config: any, feedback: any): Promise<void> {
    // Implement Zendesk integration
    console.log('Creating Zendesk ticket');
  }

  private async sendToCustom(config: any, feedback: any): Promise<void> {
    // Implement custom destination
    console.log('Sending to custom destination');
  }
}
```

---

## Response Management

### Response Manager

```typescript
interface FeedbackResponse {
  id: string;
  feedbackId: string;
  responderId: string;
  response: string;
  status: 'draft' | 'sent' | 'acknowledged';
  sentAt?: Date;
  createdAt: Date;
}

class ResponseManager {
  constructor(private prisma: PrismaClient) {}

  /**
   * Create response
   */
  async createResponse(params: {
    feedbackId: string;
    responderId: string;
    response: string;
    status?: FeedbackResponse['status'];
  }): Promise<string> {
    const created = await this.prisma.feedbackResponse.create({
      data: {
        ...params,
        status: params.status || 'draft',
      },
    });

    return created.id;
  }

  /**
   * Send response
   */
  async sendResponse(responseId: string): Promise<void> {
    const response = await this.prisma.feedbackResponse.findUnique({
      where: { id: responseId },
      include: { feedback: true },
    });

    if (!response) {
      throw new Error('Response not found');
    }

    // Send response based on feedback type
    if (response.feedback.type === 'email') {
      await this.sendEmailResponse(response);
    } else if (response.feedback.type === 'in_app') {
      await this.sendInAppResponse(response);
    }

    // Update status
    await this.prisma.feedbackResponse.update({
      where: { id: responseId },
      data: {
        status: 'sent',
        sentAt: new Date(),
      },
    });
  }

  /**
   * Send email response
   */
  private async sendEmailResponse(response: any): Promise<void> {
    await emailService.send({
      to: response.feedback.email,
      subject: `Re: ${response.feedback.subject}`,
      templateId: 'feedback-response',
      dynamicTemplateData: {
        response: response.response,
        feedbackText: response.feedback.text,
      },
    });
  }

  /**
   * Send in-app response
   */
  private async sendInAppResponse(response: any): Promise<void> {
    // Implement in-app notification
    console.log(`Sending in-app response to user ${response.feedback.userId}`);
  }

  /**
   * Get canned responses
   */
  async getCannedResponses(category?: string): Promise<any[]> {
    const where: any = { isActive: true };

    if (category) {
      where.category = category;
    }

    return await this.prisma.cannedResponse.findMany({
      where,
      orderBy: { name: 'asc' },
    });
  }

  /**
   * Use canned response
   */
  async useCannedResponse(
    responseId: string,
    cannedResponseId: string
  ): Promise<void> {
    const canned = await this.prisma.cannedResponse.findUnique({
      where: { id: cannedResponseId },
    });

    if (!canned) {
      throw new Error('Canned response not found');
    }

    await this.prisma.feedbackResponse.update({
      where: { id: responseId },
      data: { response: canned.content },
    });
  }
}
```

---

## Analytics and Reporting

### Feedback Analytics

```typescript
interface FeedbackAnalytics {
  totalFeedback: number;
  byCategory: Record<string, number>;
  bySentiment: Record<string, number>;
  byRating: Record<number, number>;
  averageRating: number;
  npsScore: number;
  responseRate: number;
  averageResponseTime: number;
  topIssues: Array<{
    category: string;
    count: number;
    sentiment: string;
  }>;
}

class FeedbackAnalytics {
  constructor(private prisma: PrismaClient) {}

  /**
   * Get analytics
   */
  async getAnalytics(params: {
    startDate: Date;
    endDate: Date;
    category?: string;
  }): Promise<FeedbackAnalytics> {
    const where: any = {
      createdAt: {
        gte: params.startDate,
        lte: params.endDate,
      },
    };

    if (params.category) {
      where.category = params.category;
    }

    const [feedback, responses] = await Promise.all([
      this.prisma.feedback.findMany({ where }),
      this.prisma.feedbackResponse.findMany({
        where: {
          feedback: {
            createdAt: where.createdAt,
          },
        },
        include: { feedback: true },
      }),
    ]);

    // Calculate metrics
    const totalFeedback = feedback.length;
    const byCategory = this.groupBy(feedback, 'category');
    const bySentiment = this.groupBy(feedback, 'sentiment');
    const byRating = this.groupBy(feedback, 'rating');
    const averageRating = this.calculateAverageRating(feedback);
    const npsScore = this.calculateNPS(feedback);
    const responseRate = responses.length / totalFeedback;
    const averageResponseTime = this.calculateAverageResponseTime(responses);
    const topIssues = this.getTopIssues(feedback);

    return {
      totalFeedback,
      byCategory,
      bySentiment,
      byRating,
      averageRating,
      npsScore,
      responseRate,
      averageResponseTime,
      topIssues,
    };
  }

  /**
   * Group feedback by field
   */
  private groupBy(feedback: any[], field: string): Record<string, number> {
    return feedback.reduce((acc, f) => {
      const key = f[field] || 'unknown';
      acc[key] = (acc[key] || 0) + 1;
      return acc;
    }, {});
  }

  /**
   * Calculate average rating
   */
  private calculateAverageRating(feedback: any[]): number {
    const ratings = feedback.filter(f => f.rating !== null && f.rating !== undefined);
    if (ratings.length === 0) return 0;

    const sum = ratings.reduce((acc, f) => acc + f.rating, 0);
    return sum / ratings.length;
  }

  /**
   * Calculate NPS
   */
  private calculateNPS(feedback: any[]): number {
    const npsScores = feedback.filter(f => f.npsScore !== null);
    if (npsScores.length === 0) return 0;

    return npsScores.reduce((acc, f) => acc + f.npsScore, 0) / npsScores.length;
  }

  /**
   * Calculate average response time
   */
  private calculateAverageResponseTime(responses: any[]): number {
    const withTime = responses.filter(r => r.sentAt && r.createdAt);
    if (withTime.length === 0) return 0;

    const totalTime = withTime.reduce((acc, r) => {
      return acc + (r.sentAt!.getTime() - r.createdAt.getTime());
    }, 0);

    return totalTime / withTime.length;
  }

  /**
   * Get top issues
   */
  private getTopIssues(feedback: any[]): Array<{
    category: string;
    count: number;
    sentiment: string;
  }> {
    const grouped = this.groupBy(feedback, 'category');
    const issues = Object.entries(grouped).map(([category, count]) => {
      const categoryFeedback = feedback.filter(f => f.category === category);
      const sentiment = this.getCategorySentiment(categoryFeedback);

      return { category, count, sentiment };
    });

    return issues.sort((a, b) => b.count - a.count).slice(0, 10);
  }

  /**
   * Get category sentiment
   */
  private getCategorySentiment(feedback: any[]): string {
    const sentiments = feedback.map(f => f.sentiment);
    const positive = sentiments.filter(s => s === 'positive').length;
    const negative = sentiments.filter(s => s === 'negative').length;

    if (positive > negative) return 'positive';
    if (negative > positive) return 'negative';
    return 'neutral';
  }
}
```

---

## Integration with Product Roadmap

### Roadmap Integration

```typescript
class RoadmapIntegration {
  constructor(private prisma: PrismaClient) {}

  /**
   * Add feature request to roadmap
   */
  async addFeatureRequest(params: {
    feedbackId: string;
    title: string;
    description: string;
    userId: string;
    votes?: number;
  }): Promise<string> {
    // Create or update roadmap item
    const item = await this.prisma.roadmapItem.upsert({
      where: { feedbackId: params.feedbackId },
      create: {
        title: params.title,
        description: params.description,
        userId: params.userId,
        status: 'proposed',
        votes: 1,
        feedbackId: params.feedbackId,
      },
      update: {
        title: params.title,
        description: params.description,
      },
    });

    // Update feedback with roadmap item
    await this.prisma.feedback.update({
      where: { id: params.feedbackId },
      data: { roadmapItemId: item.id },
    });

    return item.id;
  }

  /**
   * Vote for feature
   */
  async voteForFeature(itemId: string, userId: string): Promise<void> {
    // Check if already voted
    const existingVote = await this.prisma.roadmapVote.findUnique({
      where: {
        itemId_userId: {
          itemId,
          userId,
        },
      },
    });

    if (existingVote) {
      throw new Error('Already voted');
    }

    // Add vote
    await this.prisma.roadmapVote.create({
      data: {
        itemId,
        userId,
      },
    });

    // Update vote count
    await this.prisma.roadmapItem.update({
      where: { id: itemId },
      data: { votes: { increment: 1 } },
    });
  }

  /**
   * Update roadmap item status
   */
  async updateStatus(itemId: string, status: string): Promise<void> {
    await this.prisma.roadmapItem.update({
      where: { id: itemId },
      data: { status },
    });
  }

  /**
   * Get roadmap items
   */
  async getRoadmap(params?: {
    status?: string;
    sortBy?: 'votes' | 'created_at';
    limit?: number;
  }): Promise<any[]> {
    const where: any = {};

    if (params?.status) {
      where.status = params.status;
    }

    const orderBy: any = {};
    if (params?.sortBy) {
      orderBy[params.sortBy] = params.sortBy === 'votes' ? 'desc' : 'desc';
    }

    return await this.prisma.roadmapItem.findMany({
      where,
      orderBy,
      take: params?.limit || 20,
      include: {
        votes: true,
        user: true,
      },
    });
  }
}
```

---

## Tools

### Typeform Integration

```typescript
// npm install @typeform/node
import { createClient } from '@typeform/node';

const typeform = createClient({
  apiKey: process.env.TYPEFORM_API_KEY!,
});

class TypeformIntegration {
  /**
   * Create form
   */
  async createForm(form: {
    title: string;
    description?: string;
    fields: any[];
  }): Promise<string> {
    const response = await typeform.forms.create({
      data: form,
    });

    return response.id;
  }

  /**
   * Get responses
   */
  async getResponses(formId: string): Promise<any[]> {
    const responses = await typeform.responses.list({
      uid: formId,
    page_size: 100,
    completed: true,
    sort: 'desc',
    order_by: ['submitted_at'],
    });

    return responses.items;
  }

  /**
   * Create NPS form
   */
  async createNPSForm(): Promise<string> {
    return await this.createForm({
      title: 'NPS Survey',
      description: 'Net Promoter Score survey',
      fields: [
        {
          type: 'rating',
          ref: 'nps_score',
          title: 'How likely are you to recommend us to a friend or colleague?',
          description: '0 = Not at all likely, 10 = Extremely likely',
          required: true,
          shape: 'emoji',
          steps: 10,
        },
        {
          type: 'long_text',
          ref: 'comment',
          title: 'Please tell us why you gave this score',
          description: 'Your feedback helps us improve',
        },
      ],
    });
  }

  /**
   * Create CSAT form
   */
  async createCSATForm(): Promise<string> {
    return await this.createForm({
      title: 'CSAT Survey',
      description: 'Customer Satisfaction survey',
      fields: [
        {
          type: 'rating',
          ref: 'csat_score',
          title: 'How would you rate your experience?',
          description: '1 = Very dissatisfied, 5 = Very satisfied',
          required: true,
          shape: 'star',
          steps: 5,
        },
        {
          type: 'long_text',
          ref: 'comment',
          title: 'Please share your feedback',
          description: 'Your feedback helps us improve',
        },
      ],
    });
  }
}
```

### SurveyMonkey Integration

```typescript
// npm install survey-monkey
import SurveyMonkey from 'survey-monkey';

const surveyMonkey = new SurveyMonkey({
  apiKey: process.env.SURVEYMONKEY_API_KEY!,
});

class SurveyMonkeyIntegration {
  /**
   * Create survey
   */
  async createSurvey(survey: {
    title: string;
    description?: string;
    questions: any[];
  }): Promise<string> {
    const response = await surveyMonkey.createSurvey(survey);

    return response.id;
  }

  /**
   * Get responses
   */
  async getResponses(surveyId: string): Promise<any> {
    const response = await surveyMonkey.getResponses(surveyId);
    return response.data;
  }

  /**
   * Send survey
   */
  async sendSurvey(surveyId: string, recipients: string[]): Promise<void> {
    await surveyMonkey.createCollector({
      surveyId,
      type: 'email',
      recipients,
    });
  }
}
```

---

## Best Practices

### Feedback Best Practices

```typescript
// 1. Keep surveys short
function validateSurveyLength(questions: SurveyQuestion[]): {
  valid: boolean;
  warnings: string[];
} {
  const warnings: string[] = [];

  if (questions.length > 10) {
    warnings.push('Survey has too many questions (recommended: 5-10)');
  }

  if (questions.length < 3) {
    warnings.push('Survey has too few questions (recommended: 5-10)');
  }

  return {
    valid: warnings.length === 0,
    warnings,
  };
}

// 2. Use clear, unbiased questions
function validateQuestions(questions: SurveyQuestion[]): {
  valid: boolean;
  warnings: string[];
} {
  const warnings: string[] = [];

  for (const question of questions) {
    // Check for leading questions
    if (question.question.toLowerCase().startsWith('don\'t you')) {
      warnings.push(`Question "${question.question}" may be leading`);
    }

    // Check for double-barreled questions
    if (question.question.includes('?') && question.question.includes('?')) {
      warnings.push(`Question "${question.question}" is double-barreled`);
    }

    // Check for jargon
    const jargonWords = ['synergize', 'leverage', 'disrupt', 'paradigm', 'ecosystem'];
    if (jargonWords.some(word => question.question.toLowerCase().includes(word))) {
      warnings.push(`Question "${question.question}" contains jargon`);
    }
  }

  return {
    valid: warnings.length === 0,
    warnings,
  };
}

// 3. Always follow up on feedback
async function scheduleFollowup(feedbackId: string, delayDays: number = 3): Promise<void> {
  const followupDate = new Date(Date.now() + delayDays * 24 * 60 * 60 * 1000);

  await prisma.feedbackFollowup.create({
    data: {
      feedbackId,
      scheduledFor: followupDate,
      status: 'pending',
    },
  });
}

// 4. Close the feedback loop
async function closeFeedbackLoop(feedbackId: string, resolution: string): Promise<void> {
  await prisma.feedback.update({
    where: { id: feedbackId },
    data: {
      status: 'resolved',
      resolution,
      resolvedAt: new Date(),
    },
  });

  // Notify user
  await notifyUserOfResolution(feedbackId, resolution);
}

// 5. Analyze feedback regularly
async function generateWeeklyReport(): Promise<void> {
  const weekAgo = new Date(Date.now() - 7 * 24 * 60 * 60 * 1000);

  const feedback = await prisma.feedback.findMany({
    where: {
      createdAt: { gte: weekAgo },
    },
  });

  const analytics = new FeedbackAnalytics(prisma);
  const report = await analytics.getAnalytics({
    startDate: weekAgo,
      endDate: new Date(),
    });

  // Send report to team
  await sendWeeklyReport(report);
}

async function sendWeeklyReport(report: FeedbackAnalytics): Promise<void> {
  // Implement report sending
  console.log('Weekly feedback report:', report);
}
```

---

---

## Quick Start

### Feedback Widget

```typescript
interface Feedback {
  id: string
  userId?: string
  type: 'bug' | 'feature' | 'complaint' | 'praise'
  message: string
  rating?: number
  metadata?: Record<string, any>
}

async function submitFeedback(feedback: Feedback) {
  return await db.feedback.create({
    data: {
      ...feedback,
      sentiment: await analyzeSentiment(feedback.message),
      category: await categorizeFeedback(feedback)
    }
  })
}
```

### Sentiment Analysis

```typescript
async function analyzeSentiment(text: string): Promise<'positive' | 'negative' | 'neutral'> {
  // Use NLP library or API
  const sentiment = await sentimentAPI.analyze(text)
  return sentiment.label
}
```

---

## Production Checklist

- [ ] **Collection Methods**: Multiple feedback collection methods
- [ ] **Survey Design**: Well-designed surveys
- [ ] **Feedback Widgets**: In-app feedback widgets
- [ ] **Rating Systems**: Rating and review systems
- [ ] **Categorization**: Automatic feedback categorization
- [ ] **Sentiment Analysis**: Sentiment analysis
- [ ] **Routing**: Route feedback to appropriate teams
- [ ] **Response**: Response management
- [ ] **Analytics**: Feedback analytics
- [ ] **Integration**: Integrate with product roadmap
- [ ] **Documentation**: Document feedback process
- [ ] **Action**: Act on feedback

---

## Anti-patterns

### ❌ Don't: Collect but Don't Act

```markdown
# ❌ Bad - Collect but ignore
Feedback collected: 1000
Actions taken: 0
# Users lose trust!
```

```markdown
# ✅ Good - Act on feedback
Feedback collected: 1000
Actions taken: 50
Public updates: 20
# Users see value
```

### ❌ Don't: No Follow-up

```typescript
// ❌ Bad - No follow-up
await submitFeedback(feedback)
// User never hears back!
```

```typescript
// ✅ Good - Follow-up
await submitFeedback(feedback)
await sendAcknowledgment(feedback.userId)
// Update user when action taken
await notifyUserWhenResolved(feedback.userId, feedback.id)
```

---

## Integration Points

- **Ticketing System** (`29-customer-support/ticketing-system/`) - Convert to tickets
- **Knowledge Base** (`29-customer-support/knowledge-base/`) - Self-service
- **Product Analytics** (`23-business-analytics/`) - Product insights

---

## Further Reading

- [Customer Feedback Best Practices](https://www.zendesk.com/blog/customer-feedback/)
- [Sentiment Analysis](https://monkeylearn.com/sentiment-analysis/)

## Resources

- [Typeform API](https://developer.typeform.com/)
- [SurveyMonkey API](https://developer.surveymonkey.com/)
- [Google Forms API](https://developers.google.com/forms/api/)
- [NPS Calculation](https://www.qualtrics.com/nps/)
- [CSAT Best Practices](https://www.qualtrics.com/blog/csat/)
