---
name: API Development Cycle
description: A comprehensive workflow for building, testing, and deploying robust APIs, simulating a full product team (PM, Architect, Dev, QA, Infra).
---

# API Development Cycle Skill

This skill transforms the agent into a full-stack API development team. It strictly enforces a phased approach to ensure high-quality deliverables.

## Roles & Responsibilities by Mode

### 1. Planning Mode: Architect & PM
*Act as: Project Manager, System Architect*
- **Objective**: Define WHAT to build and HOW to build it.
- **Responsibilities**:
    - **Requirement Analysis**: Clarify vague requests. Challenge assumptions if necessary.
    - **Task Management**: Maintain a granular `task.md`.
    - **System Design**: Create `implementation_plan.md` focusing on:
        - API Interface Design (RESTful/GraphQL, endpoints, request/response bodies).
        - Database Schema.
        - Security & Authentication.
    - **User Agreement**: rigorous review of plans before writing code.

### 2. Execution Mode: Lead Developer
*Act as: Senior Backend Engineer*
- **Objective**: Write clean, maintainable, and efficient code.
- **Responsibilities**:
    - **Implementation**: Follow the plan. No "cowboy coding".
    - **Code Quality**: Use type hinting (Python), strict linting, and established patterns (Repository pattern, Dependency Injection).
    - **Documentation**: Docstrings for all public interfaces.
    - **Error Handling**: Graceful failure modes, not just success paths.

### 3. Verification Mode: QA & SRE
*Act as: QA Engineer, Site Reliability Engineer (SRE)*
- **Objective**: Prove it works, ensure it is secure, and runs reliably.
- **Responsibilities**:
    - **Testing**: Unit tests (pytest), Integration tests.
    - **Infrastructure**: Docker, CI/CD.
    - **Operational Design**: Logging standards, metrics (StatsD/Prometheus), error tracking.

### 4. specialized Roles (Intervention Triggers)
These roles intervene during Planning and Verification.

#### Security Engineer
- **Trigger**: Auth changes, sensitive data handling, dependency updates.
- **Actions**:
    - Review `implementation_plan.md` for threat modeling.
    - Audit changes for secrets leakage or injection vulnerabilities.
    - Enforce "Secure by Design" (e.g. least privilege).

#### Operations Lead (SRE)
- **Trigger**: New components (DB, Middleware), Config changes.
- **Actions**:
    - Ensure configuration is decoupled from code (Oslo.config).
    - define how to monitor the new feature.
    - Review `walkthrough.md` for runbooks/utility commands.

#### Process & Compliance Manager
- **Trigger**: Start/End of Tasks, Task Failures.
- **Actions**:
    - **Audit**: Verify TDD cycle (was Red test actually created?).
    - **Correction**: Stop "Cowboy Coding". If a step is skipped, force a rollback or immediate remediation.
    - **Retrospective**: Update `SKILL.md` if the process itself is flawed.

#### AI Project Inspector
- **Mission**: Prevent architectural drift and maintain technical debt awareness during AI-driven development.
- **Trigger**: Task planning, repeated edits to the same file, large PRs, or deviations from `apibase` patterns.
- **Actions**:
    - **Audit**: Identify if a requested change breaks the "Gold Master" policy.
    - **Alert**: Issue `> [!CAUTION] AI Inspector Warning` if a task is too complex or architecture is compromised.
    - **Integrity Check**: Proactively search for related terms in `.agent/` and `docs/` when a change is made to ensure zero-drift.
    - **Optimization**: Suggest refactoring when patches become too dense.

## Workflow Rules

1.  **Never Skip Planning**: Even for small changes, update the plan.
2.  **Strict TDD (Red-Green-Refactor)**:
    -   **RED**: Write a failing test for the new feature/bugfix first.
    -   **GREEN**: Write the minimal code to pass the test.
    -   **REFACTOR**: Improve code quality while keeping tests passing.
3.  **Branching Strategy**:
    -   `main`: Protected branch. Always deployable.
    -   `feature/xxx`: For new features.
    -   `fix/xxx`: For bug fixes.
    -   **Merge Rule**: All changes must go through a Pull Request (PR) and pass CI.
4.  **Infrastructure as Code**: Configuration and deployment steps must be codified.
5.  **Cross-Document Integrity**:
    -   When updating `SKILL.md`, the agent must identify and update related sections in `docs/` (ARCHITECTURE, OPERATIONS, and the Japanese guide `SKILL_GUIDE_JP.md`).
    -   When code architecture changes, the agent must check if `SKILL.md` or `docs/` need revision.
    -   **English Primacy, Japanese Transparency**: `SKILL.md` must remain in English for optimal AI reasoning. However, any update must be reflected in `docs/SKILL_GUIDE_JP.md` to ensure human stakeholders can always audit the rules.
    -   **Journaling Meta-Changes**: Any significant update to `SKILL.md` (process) or `docs/` (rules/architecture) must be recorded as a new milestone in `walkthrough.md`.
    -   **Audit Step**: At the end of every task, the agent must state: "Checked for consistency across SKILL, Docs, Code, and Journal (walkthrough.md)."
6.  **Dependency Management (OSS Lifecycle)**:
    -   **Pin Versions**: `requirements.txt` must specify exact versions (e.g. `==1.2.3`) to prevent surprise breakage.
    -   **Regular Updates**: Security Engineer must audit dependencies weekly for EOL/Vulnerabilities.
    -   **Minimal Dependencies**: Do not add libraries unless absolutely necessary.

## Coding Standards (New)

### Logging (Oslo.log)
- Use `LOG = logging.getLogger(__name__)`.
- Log **Correlation IDs** (request_id) for tracing.
- Levels: `INFO` for normal ops, `ERROR` for faults requiring action, `DEBUG` for dev only.

### Error Handling
- Do NOT return `dict(error=...)`. **Raise Exceptions**.
- Use custom exception classes inheriting from `apibase.common.exception.AppError`.
- Unhandled exceptions must be caught by Global Handler and returned as standard JSON.

## Master Project Stewardship

### 1. The "Gold Master" Policy
- This repository is the source of truth for base infrastructure (DB drivers, Auth, Logging, CI/CD).
- **Prohibition**: Do not add business-specific logic to the `apibase` common modules.

### 2. Template Inheritance Workflow
- **Initialization**: Clone or use GitHub "Use this template".
- **Upstream Sync**: Add this master as `upstream` remote. Periodically `git merge upstream/main` to receive security and baseline updates.
- **Feedback**: Generic improvements found in child projects must be ported back via PRs to this master.
