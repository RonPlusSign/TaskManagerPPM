> **B028451 (B047) - PROGETTAZIONE E PRODUZIONE MULTIMEDIALE**
>
> **Delli Andrea (7052940)**
>
> University of Florence
>
> Academic Year 2022-2023
>
> Bachelor's Degree in Computer Engineering

## Task Management System

Develop a **task management system** where users can create, assign, and track tasks.

Implement features like user registration, task creation, task assignment, and task status tracking.

The model complexity can involve defining relationships between users, tasks, and task statuses.

The templates can focus on displaying tasks and their details in a clear and organized manner.

### Requirements

- The application must be implemented using the **Django** framework.
- The application must be implemented using the **Model-View-Template** architectural pattern.
- The application has to be hosted on a web server like **Railway** or **Heroku**.

### Implementation Details

The implementation follows a similar structure and functionalities offered by the **Asana** application.

When a user is registered, he can create a list of tasks. He now is the owner of the list and can decide who can join
the list.
Only the owner of the list can edit the list, add or remove users from the list.

The users that join the list can create tasks and assign them to other users.
Everyone in the list can see the tasks and their status, can edit the tasks and change their status.
They also can add comments to the tasks, and see the comments of other users.

Only the task assignee can mark the task as completed.

Every user can see the list of tasks he has to do, the lists he is part of, the lists he created, and the tasks he
completed.