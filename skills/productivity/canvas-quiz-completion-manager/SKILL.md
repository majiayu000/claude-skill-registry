---
name: canvas-quiz-completion-manager
description: When the user needs to manage and complete multiple quizzes on Canvas LMS, this skill provides automated quiz discovery, question retrieval, answer analysis, and batch submission capabilities. It handles the complete workflow from listing enrolled courses, identifying available quizzes, starting quiz attempts, retrieving questions, analyzing correct answers based on subject matter expertise, and submitting all responses. Key triggers include 'unfinished quizzes', 'complete all quizzes', 'Canvas assignments', 'course assessments', 'submit quizzes', and 'quiz deadlines'. The skill is particularly useful when users have multiple pending quizzes across different courses and need systematic completion with accurate answers.
---
# Instructions

## Primary Objective
Systematically discover, answer, and submit all available/unfinished quizzes for the user across all their enrolled Canvas courses. Ensure all answers are correct and all submissions are successfully completed.

## Core Workflow

### Phase 1: Discovery & Initialization
1.  **List Enrolled Courses:** Use `canvas-canvas_list_courses` to get all courses where the user has a student enrollment (`"type": "student"`). Store the list of course IDs.
2.  **List Available Quizzes:** For each enrolled course, use `canvas-canvas_list_quizzes` to find all published quizzes. Filter for quizzes where `"submit": true` in the permissions. Compile a master list of `(course_id, quiz_id)` pairs.

### Phase 2: Quiz Attempt Initialization
3.  **Start All Quiz Attempts:** For each `(course_id, quiz_id)` pair, call `canvas-canvas_start_quiz_attempt`. This is a parallelizable operation. Capture the returned `quiz_submission_id` and `validation_token` for each quiz. Handle any errors gracefully (e.g., quiz already started, access denied) but log them.

### Phase 3: Question Retrieval & Analysis
4.  **Retrieve All Questions:** For each active quiz attempt, use `canvas-canvas_list_quiz_questions` with the `quiz_submission_id` and `use_submission_endpoint: true` to get the specific questions and answer choices for that attempt.
5.  **Analyze and Determine Correct Answers:** For each retrieved question, use your general knowledge and reasoning to identify the single correct answer. **Crucially, you must provide the correct `answer_id` from the provided answer choices.** Do not guess. If a question's subject matter is outside your reliable knowledge, note it but proceed with your best logical deduction based on the question text and answer choices. The goal is 100% accuracy.
    *   **Pattern from Trajectory:** Questions are typically multiple-choice (`"question_type": "multiple_choice_question"`). The correct `answer_id` is a numeric ID within the `answers` array.

### Phase 4: Batch Submission & Verification
6.  **Prepare Submission Payloads:** For each quiz, construct a submission payload for `canvas-canvas_submit_quiz_answers`. The payload must include:
    *   `course_id`, `quiz_id`, `submission_id` (the `quiz_submission_id`), `validation_token`
    *   `answers`: An array of objects, each with `question_id` and the correct `answer_id`.
7.  **Submit All Quizzes:** Submit the payloads for all quizzes. This can be done in parallel.
8.  **Verify Success:** Check the response for each submission. Confirm `"workflow_state": "complete"` and that the `"score"` equals `"quiz_points_possible"` (indicating a perfect score). If any submission fails, retry or investigate.

### Phase 5: Reporting & Completion
9.  **Generate Summary Report:** Create a clear summary table listing: Course Name, Quiz Title, Score/Max Points, and Status.
10. **Claim Completion:** Once all quizzes are submitted and verified, use `local-claim_done` to signal task completion. Provide the final summary to the user.

## Key Considerations & Error Handling
*   **Memory Access:** The trajectory shows an attempt to read memory (`memory-read_graph`) that failed. Proceed with Canvas API calls if memory is unavailable. If personal info (like specific course preferences) is needed and memory fails, state the limitation and work with the available Canvas data.
*   **Canvas Errors:** The user mentioned "there might be some error with the canvas." Be resilient. If a single API call fails (e.g., listing quizzes for one course), skip that course and continue with others. Log the error for the user.
*   **Parallel Execution:** The trajectory shows batched calls for listing quizzes and starting attempts. You should emulate this efficient pattern where safe and logical (e.g., starting attempts, submitting answers). Do not batch calls that have dependencies.
*   **Answer Accuracy:** The user's tip emphasizes you "must make sure all quizzes are submitted and answered correctly." Your analysis in Phase 3 is the critical step. Double-check your reasoning for each answer.
*   **State Management:** Keep track of the state (course list, quiz list, submission IDs, tokens, answers) throughout the process. The provided trajectory is a successful execution; follow its logical flow.

## Triggers
Activate this skill when the user request involves: completing unfinished quizzes, submitting all Canvas quizzes, managing course assessments, or meeting quiz deadlines across multiple courses.
