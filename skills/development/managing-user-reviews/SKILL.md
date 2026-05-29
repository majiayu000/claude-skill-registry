---
name: managing-user-reviews
description: Logic for handling user reviews, ratings, and admin moderation. Use to build the community feedback section.
---

# User Reviews and Moderation

## When to use this skill
- Implementing the "Reviews" collection logic.
- Building the admin approval dashboard.

## Workflow
- [ ] Users post a review (Doc created in `reviews` collection).
- [ ] Status set to `pending` by default.
- [ ] Admin changes status to `approved`.
- [ ] Tour details page only shows reviews where `status === 'approved'`.

## Calculations (Aggregation)
- **Problem**: Calculating average rating every time is slow.
- **Solution**: Use an Appwrite Function to update the `averageRating` and `reviewCount` on the `Tour` document whenever a review is approved.

## Instructions
- **Abuse**: Limit users to 1 review per tour.
- **Content**: Ensure Zod sanitization (see `sanitizing-inputs-zod`) to prevent profanity or spam.
