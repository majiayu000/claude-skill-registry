---
name: education-expert
version: 1.0.0
description: Expert-level education technology, learning management systems, and ed-tech platforms
category: domains
tags: [education, edtech, lms, e-learning, assessment]
allowed-tools:
  - Read
  - Write
  - Edit
---

# Education Expert

Expert guidance for education technology, learning management systems, online learning platforms, and educational software development.

## Core Concepts

### Educational Technology
- Learning Management Systems (LMS)
- Student Information Systems (SIS)
- Assessment and evaluation tools
- Adaptive learning platforms
- Virtual classrooms
- Content management

### Standards
- SCORM (Sharable Content Object Reference Model)
- xAPI (Experience API / Tin Can API)
- LTI (Learning Tools Interoperability)
- QTI (Question and Test Interoperability)
- Accessibility (WCAG, Section 508)

### Key Features
- Course management
- Grade tracking
- Student analytics
- Content delivery
- Collaborative tools
- Assessment engines

## LMS Core Implementation

```python
from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime
from enum import Enum

class EnrollmentStatus(Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    DROPPED = "dropped"
    PENDING = "pending"

@dataclass
class Course:
    course_id: str
    title: str
    description: str
    instructor_id: str
    start_date: datetime
    end_date: datetime
    credits: int
    capacity: int
    syllabus_url: str
    prerequisites: List[str]

@dataclass
class Student:
    student_id: str
    first_name: str
    last_name: str
    email: str
    enrolled_date: datetime
    grade_level: str
    gpa: float

@dataclass
class Enrollment:
    enrollment_id: str
    student_id: str
    course_id: str
    enrollment_date: datetime
    status: EnrollmentStatus
    final_grade: Optional[float]

class LMSPlatform:
    """Learning Management System core functionality"""

    def __init__(self, db):
        self.db = db

    def enroll_student(self, student_id, course_id):
        """Enroll student in course"""
        course = self.db.get_course(course_id)
        current_enrollment = self.db.count_enrollments(course_id)

        # Check capacity
        if current_enrollment >= course.capacity:
            raise Exception("Course is full")

        # Check prerequisites
        if course.prerequisites:
            completed = self.get_completed_courses(student_id)
            if not all(prereq in completed for prereq in course.prerequisites):
                raise Exception("Prerequisites not met")

        enrollment = Enrollment(
            enrollment_id=generate_id(),
            student_id=student_id,
            course_id=course_id,
            enrollment_date=datetime.now(),
            status=EnrollmentStatus.ACTIVE,
            final_grade=None
        )

        return self.db.save_enrollment(enrollment)

    def get_student_transcript(self, student_id):
        """Generate student transcript"""
        enrollments = self.db.get_student_enrollments(student_id)
        transcript = []

        for enrollment in enrollments:
            if enrollment.status == EnrollmentStatus.COMPLETED:
                course = self.db.get_course(enrollment.course_id)
                transcript.append({
                    'course_code': course.course_id,
                    'course_name': course.title,
                    'credits': course.credits,
                    'grade': enrollment.final_grade,
                    'term': self.get_term(enrollment.enrollment_date)
                })

        return transcript

    def calculate_gpa(self, student_id):
        """Calculate student GPA"""
        transcript = self.get_student_transcript(student_id)
        total_points = 0
        total_credits = 0

        for record in transcript:
            if record['grade'] is not None:
                total_points += record['grade'] * record['credits']
                total_credits += record['credits']

        return total_points / total_credits if total_credits > 0 else 0.0
```

## Assessment Engine

```python
from abc import ABC, abstractmethod

class Question(ABC):
    """Base question class"""

    def __init__(self, question_id, text, points):
        self.question_id = question_id
        self.text = text
        self.points = points

    @abstractmethod
    def check_answer(self, student_answer):
        pass

class MultipleChoiceQuestion(Question):
    """Multiple choice question"""

    def __init__(self, question_id, text, points, choices, correct_answer):
        super().__init__(question_id, text, points)
        self.choices = choices
        self.correct_answer = correct_answer

    def check_answer(self, student_answer):
        return student_answer == self.correct_answer

class Essay Question(Question):
    """Essay question requiring manual grading"""

    def __init__(self, question_id, text, points, rubric):
        super().__init__(question_id, text, points)
        self.rubric = rubric

    def check_answer(self, student_answer):
        # Requires manual grading
        return None

class AssessmentEngine:
    """Assessment and grading system"""

    def grade_assessment(self, assessment, student_answers):
        """Grade student assessment"""
        total_points = 0
        earned_points = 0
        results = []

        for question in assessment.questions:
            total_points += question.points
            student_answer = student_answers.get(question.question_id)

            if isinstance(question, MultipleChoiceQuestion):
                is_correct = question.check_answer(student_answer)
                points_earned = question.points if is_correct else 0
                earned_points += points_earned

                results.append({
                    'question_id': question.question_id,
                    'correct': is_correct,
                    'points': points_earned,
                    'feedback': 'Correct!' if is_correct else f'Incorrect. Correct answer: {question.correct_answer}'
                })
            else:
                # Essay questions need manual grading
                results.append({
                    'question_id': question.question_id,
                    'status': 'pending_review',
                    'answer': student_answer
                })

        score_percentage = (earned_points / total_points) * 100 if total_points > 0 else 0

        return {
            'total_points': total_points,
            'earned_points': earned_points,
            'percentage': score_percentage,
            'results': results
        }

    def analyze_assessment_statistics(self, assessment_id, all_submissions):
        """Analyze assessment performance"""
        scores = [s['percentage'] for s in all_submissions]

        return {
            'mean': sum(scores) / len(scores),
            'median': sorted(scores)[len(scores) // 2],
            'min': min(scores),
            'max': max(scores),
            'std_dev': self.calculate_std_dev(scores)
        }
```

## Learning Analytics

```python
class LearningAnalytics:
    """Student learning analytics"""

    def get_student_engagement(self, student_id, course_id):
        """Calculate student engagement metrics"""
        activities = self.db.get_student_activities(student_id, course_id)

        metrics = {
            'login_frequency': self.calculate_login_frequency(activities),
            'content_completion_rate': self.calculate_completion_rate(activities),
            'assessment_participation': self.calculate_participation(activities),
            'forum_posts': len([a for a in activities if a['type'] == 'forum_post']),
            'time_on_platform': sum(a['duration'] for a in activities)
        }

        return metrics

    def predict_student_risk(self, student_id, course_id):
        """Predict at-risk students"""
        engagement = self.get_student_engagement(student_id, course_id)
        grades = self.get_recent_grades(student_id, course_id)

        risk_score = 0

        # Low engagement indicators
        if engagement['login_frequency'] < 2:  # Less than 2x per week
            risk_score += 25
        if engagement['content_completion_rate'] < 0.5:
            risk_score += 25
        if engagement['assessment_participation'] < 0.7:
            risk_score += 25

        # Grade indicators
        if grades and sum(grades) / len(grades) < 60:
            risk_score += 25

        risk_level = 'high' if risk_score >= 75 else 'medium' if risk_score >= 50 else 'low'

        return {
            'student_id': student_id,
            'risk_score': risk_score,
            'risk_level': risk_level,
            'recommendations': self.generate_interventions(risk_score, engagement)
        }

    def generate_learning_path(self, student_id, learning_goals):
        """Generate personalized learning path"""
        # Analyze student's current knowledge
        current_skills = self.assess_skills(student_id)
        gap_analysis = self.identify_skill_gaps(current_skills, learning_goals)

        # Recommend courses and resources
        recommended_courses = self.match_courses_to_goals(gap_analysis)

        return {
            'student_id': student_id,
            'current_level': current_skills,
            'target_level': learning_goals,
            'skill_gaps': gap_analysis,
            'recommended_path': recommended_courses,
            'estimated_duration': self.estimate_completion_time(recommended_courses)
        }
```

## xAPI (Tin Can API) Integration

```python
import json
from datetime import datetime

class xAPIStatement:
    """xAPI statement builder"""

    @staticmethod
    def create_statement(actor, verb, object_data, result=None):
        """Create xAPI statement"""
        statement = {
            'actor': {
                'objectType': 'Agent',
                'name': actor['name'],
                'mbox': f"mailto:{actor['email']}"
            },
            'verb': {
                'id': verb['id'],
                'display': {'en-US': verb['display']}
            },
            'object': {
                'id': object_data['id'],
                'definition': {
                    'name': {'en-US': object_data['name']},
                    'description': {'en-US': object_data.get('description', '')}
                }
            },
            'timestamp': datetime.utcnow().isoformat()
        }

        if result:
            statement['result'] = result

        return statement

    @staticmethod
    def completed_course(student, course, score):
        """Create course completion statement"""
        return xAPIStatement.create_statement(
            actor={'name': student['name'], 'email': student['email']},
            verb={
                'id': 'http://adlnet.gov/expapi/verbs/completed',
                'display': 'completed'
            },
            object_data={
                'id': f"http://lms.example.com/course/{course['id']}",
                'name': course['title']
            },
            result={
                'score': {
                    'scaled': score / 100,
                    'raw': score,
                    'min': 0,
                    'max': 100
                },
                'completion': True,
                'success': score >= 70
            }
        )
```

## Best Practices

- Implement accessibility standards (WCAG)
- Support mobile learning
- Enable offline access
- Provide real-time feedback
- Use adaptive learning algorithms
- Protect student data privacy (FERPA)
- Enable collaborative learning
- Provide detailed analytics
- Support multiple content formats
- Implement plagiarism detection
- Enable parent/guardian access
- Support multilingual content

## Anti-Patterns

❌ Poor mobile experience
❌ No accessibility features
❌ Ignoring data privacy
❌ No analytics or reporting
❌ Inflexible assessment tools
❌ No offline capabilities
❌ Poor user experience

## Resources

- SCORM: https://scorm.com/
- xAPI: https://xapi.com/
- LTI: https://www.imsglobal.org/activity/learning-tools-interoperability
- Moodle: https://moodle.org/
- Canvas LMS: https://www.instructure.com/canvas
- FERPA: https://www2.ed.gov/policy/gen/guid/fpco/ferpa/
