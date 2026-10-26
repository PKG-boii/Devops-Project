import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_deck(output_path):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Color Palette - Modern Dark DevOps Theme
    BG_DARK = RGBColor(15, 23, 42)        # #0F172A - Slate 900
    CARD_BG = RGBColor(30, 41, 59)        # #1E293B - Slate 800
    CARD_BORDER = RGBColor(51, 65, 85)    # #334155 - Slate 700
    CYAN_ACCENT = RGBColor(6, 182, 212)   # #06B6D4 - Cyan 500
    SKY_BLUE = RGBColor(56, 189, 248)     # #38BDF8 - Sky 400
    EMERALD = RGBColor(16, 185, 129)      # #10B981 - Emerald 500
    AMBER = RGBColor(245, 158, 11)        # #F59E0B - Amber 500
    ROSE = RGBColor(244, 63, 94)          # #F43F5E - Rose 500
    TEXT_WHITE = RGBColor(248, 250, 252)  # #F8FAFC
    TEXT_MUTED = RGBColor(148, 163, 184)  # #94A3B8
    CODE_BG = RGBColor(10, 15, 26)        # #0A0F1A

    def set_slide_background(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_DARK
        bg.line.fill.background()
        return bg

    def add_header(slide, step_num, title, subtitle):
        # Header banner card
        header_card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.5), Inches(11.733), Inches(1.1))
        header_card.fill.solid()
        header_card.fill.fore_color.rgb = CARD_BG
        header_card.line.color.rgb = CARD_BORDER
        header_card.line.width = Pt(1)

        tf = header_card.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.3)
        tf.margin_top = Inches(0.12)
        tf.margin_bottom = Inches(0.1)

        p0 = tf.paragraphs[0]
        p0.text = f"PART 0 — FINAL DEMO  |  STEP {step_num}"
        p0.font.name = "Segoe UI"
        p0.font.size = Pt(11)
        p0.font.bold = True
        p0.font.color.rgb = CYAN_ACCENT

        p1 = tf.add_paragraph()
        p1.text = title
        p1.font.name = "Segoe UI"
        p1.font.size = Pt(20)
        p1.font.bold = True
        p1.font.color.rgb = TEXT_WHITE

        # Subtitle badge on right side
        badge = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(9.6), Inches(0.7), Inches(2.7), Inches(0.65))
        badge.fill.solid()
        badge.fill.fore_color.rgb = CODE_BG
        badge.line.color.rgb = CYAN_ACCENT
        badge.line.width = Pt(1)
        btf = badge.text_frame
        btf.margin_top = Inches(0.12)
        bp = btf.paragraphs[0]
        bp.alignment = PP_ALIGN.CENTER
        bp.text = subtitle
        bp.font.name = "Segoe UI"
        bp.font.size = Pt(11)
        bp.font.bold = True
        bp.font.color.rgb = SKY_BLUE

    def add_card(slide, left, top, width, height, title, items, border_color=CARD_BORDER, title_color=SKY_BLUE):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = border_color
        card.line.width = Pt(1.5)
        
        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.25)
        tf.margin_right = Inches(0.25)
        tf.margin_top = Inches(0.2)
        tf.margin_bottom = Inches(0.2)

        p = tf.paragraphs[0]
        p.text = title
        p.font.name = "Segoe UI"
        p.font.size = Pt(15)
        p.font.bold = True
        p.font.color.rgb = title_color

        for item in items:
            p2 = tf.add_paragraph()
            p2.space_before = Pt(8)
            p2.font.name = "Segoe UI"
            p2.font.size = Pt(12)
            if isinstance(item, tuple):
                bold_txt, reg_txt = item
                r1 = p2.add_run()
                r1.text = bold_txt + ": "
                r1.font.bold = True
                r1.font.color.rgb = TEXT_WHITE
                r2 = p2.add_run()
                r2.text = reg_txt
                r2.font.color.rgb = TEXT_MUTED
            else:
                r = p2.add_run()
                r.text = item
                r.font.color.rgb = TEXT_MUTED

    def add_terminal(slide, left, top, width, height, term_title, lines):
        term = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
        term.fill.solid()
        term.fill.fore_color.rgb = CODE_BG
        term.line.color.rgb = CARD_BORDER
        term.line.width = Pt(1)

        tf = term.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.25)
        tf.margin_right = Inches(0.25)
        tf.margin_top = Inches(0.18)
        tf.margin_bottom = Inches(0.18)

        # Terminal header bar
        p = tf.paragraphs[0]
        p.text = f"●  ●  ●   terminal  —  {term_title}"
        p.font.name = "Consolas"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = SKY_BLUE

        for line in lines:
            lp = tf.add_paragraph()
            lp.space_before = Pt(4)
            lp.font.name = "Consolas"
            lp.font.size = Pt(10.5)
            
            if line.startswith("$ "):
                r1 = lp.add_run()
                r1.text = "$ "
                r1.font.bold = True
                r1.font.color.rgb = EMERALD
                r2 = lp.add_run()
                r2.text = line[2:]
                r2.font.bold = True
                r2.font.color.rgb = TEXT_WHITE
            elif "Running" in line or "PASS" in line or "200 OK" in line or "201 Created" in line or "deployed" in line:
                r = lp.add_run()
                r.text = line
                r.font.color.rgb = EMERALD
            elif "CrashLoopBackOff" in line or "ImagePullBackOff" in line or "ErrImagePull" in line or "FAIL" in line:
                r = lp.add_run()
                r.text = line
                r.font.color.rgb = ROSE
            elif line.startswith(">") or line.startswith("#"):
                r = lp.add_run()
                r.text = line
                r.font.color.rgb = AMBER
            else:
                r = lp.add_run()
                r.text = line
                r.font.color.rgb = TEXT_MUTED

    # ==================== SLIDE 0: TITLE SLIDE ====================
    s0 = prs.slides.add_slide(blank_layout)
    set_slide_background(s0)

    # Accent decorative box
    acc = s0.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.5), Inches(1.2), Inches(10.333), Inches(5.1))
    acc.fill.solid()
    acc.fill.fore_color.rgb = CARD_BG
    acc.line.color.rgb = CYAN_ACCENT
    acc.line.width = Pt(2)

    atf = acc.text_frame
    atf.word_wrap = True
    atf.margin_left = Inches(0.8)
    atf.margin_right = Inches(0.8)
    atf.margin_top = Inches(0.7)

    p = atf.paragraphs[0]
    p.text = "DEVOPS CAPSTONE PROJECT"
    p.font.name = "Segoe UI"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = CYAN_ACCENT

    p = atf.add_paragraph()
    p.space_before = Pt(12)
    p.text = "PART 0 — FINAL DEMO"
    p.font.name = "Segoe UI"
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE

    p = atf.add_paragraph()
    p.space_before = Pt(8)
    p.text = "TaskBoard: Cloud-Native Microservices, CI/CD, IaC & Kubernetes Orchestration"
    p.font.name = "Segoe UI"
    p.font.size = Pt(18)
    p.font.color.rgb = SKY_BLUE

    p = atf.add_paragraph()
    p.space_before = Pt(28)
    p.text = "Comprehensive 15-Stage Live Verification & Resilience Walkthrough"
    p.font.name = "Segoe UI"
    p.font.size = Pt(13)
    p.font.color.rgb = TEXT_MUTED

    # Bottom badge line
    p = atf.add_paragraph()
    p.space_before = Pt(16)
    p.text = "FastAPI  •  PostgreSQL  •  GitHub Actions  •  Docker & Trivy  •  GHCR  •  Terraform  •  K8s & Helm  •  HPA  •  Grafana"
    p.font.name = "Consolas"
    p.font.size = Pt(11)
    p.font.color.rgb = EMERALD

    # ==================== SLIDE 1: AGENDA & WORKFLOW MAP ====================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1)
    add_header(s1, "OVERVIEW", "End-to-End Demonstration Workflow", "15 Verification Points")

    col1 = [
        ("01. Application", "Interactive TaskBoard UI & Live Task Creation"),
        ("02. API", "FastAPI Swagger Documentation & CRUD Tests"),
        ("03. Database", "PostgreSQL tasks Table & Schema Inspection"),
        ("04. Git Workflow", "Application Feature Change & Commit"),
        ("05. CI Pipeline", "GitHub Actions Automated Test & Lint Matrix"),
    ]
    col2 = [
        ("06. Docker Images", "Multi-stage Frontend & Backend Containerization"),
        ("07. Security Scan", "DevSecOps Trivy Vulnerability Assessment"),
        ("08. Image Registry", "GitHub Container Registry (GHCR) Publishing"),
        ("09. Terraform IaC", "AWS Infrastructure Code (EKS, VPC, RDS)"),
        ("10. Kubernetes", "Namespace Pods & Services Health Status"),
    ]
    col3 = [
        ("11. Helm Chart", "Declarative Release Lifecycle & Values"),
        ("12. Ingress Controller", "Host-based Application Traffic Routing"),
        ("13. HPA Autoscaling", "Dynamic Metric-based Pod Scaling"),
        ("14. Observability", "Prometheus Scraping & Grafana Dashboards"),
        ("15. Live Troubleshooting", "Pod Breakdown & Rollout Remediation"),
    ]
    add_card(s1, 0.8, 1.8, 3.7, 5.1, "Phase 1: App & CI/CD", col1, CYAN_ACCENT, CYAN_ACCENT)
    add_card(s1, 4.8, 1.8, 3.7, 5.1, "Phase 2: Cloud & Containers", col2, SKY_BLUE, SKY_BLUE)
    add_card(s1, 8.8, 1.8, 3.7, 5.1, "Phase 3: K8s & Resilience", col3, EMERALD, EMERALD)

    # ==================== SLIDE 2: 1. APPLICATION ====================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2)
    add_header(s2, "01", "Application — Open TaskBoard & Create Task", "Web Client UI")

    app_details = [
        ("Objective", "Verify user-facing portal & frontend-backend connectivity"),
        ("Portal URL", "http://taskboard.devops.internal (or localhost:3000)"),
        ("Workflow", "Access modern Kanban interface with To Do, In Progress, and Done"),
        ("Live Action", "Click '+ New Task' button to trigger creation modal"),
        ("Input Data", "Title: 'Deploy v1.2 Production Release' | Priority: High"),
        ("Reactivity", "Instant optimistic UI render and WebSocket/REST synchronization"),
        ("Persistence", "Task state automatically written to backend database via REST API"),
    ]
    add_card(s2, 0.8, 1.8, 5.5, 5.1, "Feature Capabilities", app_details, CYAN_ACCENT)

    app_term = [
        "$ curl -s http://taskboard.devops.internal/health",
        '{"status":"healthy","version":"1.2.0","service":"taskboard-ui"}',
        "",
        "# Task Created via UI Event Handler:",
        "> POST /api/v1/tasks HTTP/1.1",
        '> Host: taskboard.devops.internal',
        '> Content-Type: application/json',
        '> {',
        '>   "title": "Deploy v1.2 Production Release",',
        '>   "description": "Trigger EKS rollout with Helm chart",',
        '>   "priority": "HIGH",',
        '>   "status": "TODO"',
        '> }',
        "< HTTP/1.1 201 Created",
        '< Location: /api/v1/tasks/task-9842a',
        '{"id":"task-9842a","created_at":"2026-10-26T18:30:00Z","status":"TODO"}',
        "# UI rendered task-9842a into 'To Do' column successfully"
    ]
    add_terminal(s2, 6.6, 1.8, 5.9, 5.1, "http-traffic-inspector", app_term)

    # ==================== SLIDE 3: 2. API ====================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3)
    add_header(s3, "02", "API — FastAPI Swagger Documentation & CRUD", "RESTful Backend")

    api_details = [
        ("Swagger URL", "http://taskboard.devops.internal/api/v1/docs"),
        ("OpenAPI 3.1", "Auto-generated interactive Swagger schema & models"),
        ("Create (POST)", "POST /api/v1/tasks — validates request via Pydantic model"),
        ("Read (GET)", "GET /api/v1/tasks — supports pagination, filter by status"),
        ("Update (PUT)", "PUT /api/v1/tasks/{id} — transitions status to 'IN_PROGRESS'"),
        ("Delete (DELETE)", "DELETE /api/v1/tasks/{id} — safely removes record (204 No Content)"),
        ("Performance", "Asynchronous endpoints powered by Starlette & AsyncPG"),
    ]
    add_card(s3, 0.8, 1.8, 5.5, 5.1, "FastAPI Endpoints", api_details, SKY_BLUE)

    api_term = [
        "$ # 1. CREATE Task",
        '$ curl -X POST "http://localhost:8000/api/v1/tasks" -d \'{"title":"Test K8s"}\'',
        'HTTP/1.1 201 Created -> {"id": 101, "title": "Test K8s", "status": "TODO"}',
        "",
        "$ # 2. READ Task",
        '$ curl -X GET "http://localhost:8000/api/v1/tasks/101"',
        'HTTP/1.1 200 OK -> {"id": 101, "title": "Test K8s", "status": "TODO"}',
        "",
        "$ # 3. UPDATE Task",
        '$ curl -X PUT "http://localhost:8000/api/v1/tasks/101" -d \'{"status":"DONE"}\'',
        'HTTP/1.1 200 OK -> {"id": 101, "title": "Test K8s", "status": "DONE"}',
        "",
        "$ # 4. DELETE Task",
        '$ curl -X DELETE "http://localhost:8000/api/v1/tasks/101"',
        'HTTP/1.1 204 No Content -> Task deleted successfully'
    ]
    add_terminal(s3, 6.6, 1.8, 5.9, 5.1, "fastapi-crud-test", api_term)

    # ==================== SLIDE 4: 3. DATABASE ====================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4)
    add_header(s4, "03", "Database — PostgreSQL Schema & Tasks Table", "Persistent Storage")

    db_details = [
        ("Database Engine", "PostgreSQL 16 High Availability on Amazon RDS / K8s StatefulSet"),
        ("Connection URL", "postgresql://taskuser:***@postgres-service:5432/taskboard_db"),
        ("Table Name", "public.tasks"),
        ("Schema Constraints", "PRIMARY KEY (id), NOT NULL on title, created_at default NOW()"),
        ("ORM / Migrations", "SQLAlchemy 2.0 with Alembic versioned schema migrations"),
        ("Integrity", "ACID transactions with automated daily backup snapshots"),
    ]
    add_card(s4, 0.8, 1.8, 5.5, 5.1, "Database Architecture", db_details, EMERALD)

    db_term = [
        "$ psql -U postgres -h postgres-service -d taskboard_db",
        "taskboard_db=# \\d tasks",
        "                                  Table 'public.tasks'",
        "   Column    |          Type          | Collation | Nullable |      Default",
        "-------------+------------------------+-----------+----------+--------------------",
        " id          | integer                |           | not null | nextval('tasks_id')",
        " title       | character varying(255) |           | not null |",
        " priority    | character varying(50)  |           | not null | 'MEDIUM'",
        " status      | character varying(50)  |           | not null | 'TODO'",
        " created_at  | timestamp with tz      |           | not null | CURRENT_TIMESTAMP",
        "Indexes: 'tasks_pkey' PRIMARY KEY, btree (id)",
        "",
        "taskboard_db=# SELECT id, title, priority, status FROM tasks LIMIT 2;",
        " id  |             title              | priority | status",
        "-----+--------------------------------+----------+--------",
        " 101 | Deploy v1.2 Production Release | HIGH     | IN_PROGRESS",
        " 102 | Audit Security Trivy Scan      | CRITICAL | DONE",
        "(2 rows)"
    ]
    add_terminal(s4, 6.6, 1.8, 5.9, 5.1, "psql-client-session", db_term)

    # ==================== SLIDE 5: 4. GIT ====================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5)
    add_header(s5, "04", "Git — Application Code Modification & Commit", "Version Control")

    git_details = [
        ("Repository", "github.com/organization/taskboard.git"),
        ("Branching Model", "Trunk-Based Development with Short-Lived Feature Branches"),
        ("Live Change", "Modified 'app/api/tasks.py' to add strict task priority enum check"),
        ("Conventional Commit", "feat(api): add task priority validation filter & test"),
        ("Code Review", "Pull Request template enforces unit test pass & lint checks"),
        ("Traceability", "Commit hash links to GitHub Actions pipeline run automatically"),
    ]
    add_card(s5, 0.8, 1.8, 5.5, 5.1, "Developer Workflow", git_details, CYAN_ACCENT)

    git_term = [
        "$ git checkout -b feature/task-validation",
        "Switched to a new branch 'feature/task-validation'",
        "",
        "$ git status -s",
        " M app/api/tasks.py",
        " M tests/test_tasks.py",
        "",
        "$ git diff app/api/tasks.py",
        "@@ -42,6 +42,8 @@ def create_task(task: TaskCreate):",
        "+    if task.priority not in ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL']:",
        "+        raise HTTPException(status_code=422, detail='Invalid priority')",
        "     return db.save(task)",
        "",
        "$ git add .",
        '$ git commit -m "feat(api): add task priority validation filter"',
        "[feature/task-validation 8f2a1b9] feat(api): add task priority validation filter",
        " 2 files changed, 14 insertions(+), 1 deletion(-)"
    ]
    add_terminal(s5, 6.6, 1.8, 5.9, 5.1, "git-bash-session", git_term)

    # ==================== SLIDE 6: 5. CI ====================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6)
    add_header(s6, "05", "CI — GitHub Actions Automated Test & Build Matrix", "Continuous Integration")

    ci_details = [
        ("Workflow File", ".github/workflows/ci.yaml"),
        ("Trigger Event", "Push to main / Pull Request to feature branch"),
        ("Job 1: Linting", "Ruff & Flake8 for PEP8 formatting, MyPy static type check"),
        ("Job 2: Unit Tests", "Pytest suite running 24 unit & integration tests against DB"),
        ("Job 3: Security", "Bandit AST security checks & dependency vulnerability review"),
        ("Execution Time", "Total pipeline run completed in 38 seconds"),
        ("Gate Rule", "Branch protection rules block merges if any CI step fails"),
    ]
    add_card(s6, 0.8, 1.8, 5.5, 5.1, "Pipeline Specifications", ci_details, SKY_BLUE)

    ci_term = [
        "$ git push origin feature/task-validation",
        "Enumerating objects: 7, done.",
        "To github.com:organization/taskboard.git",
        " * [new branch]      feature/task-validation -> feature/task-validation",
        "",
        "# GitHub Actions Workflow Triggered: [Run #248]",
        "> [Step 1] Set up Python 3.12 ............................. [PASS 2.1s]",
        "> [Step 2] Install dependencies (poetry/pip) ............. [PASS 6.4s]",
        "> [Step 3] Run Linters (flake8, black, ruff) ............. [PASS 3.2s]",
        "> [Step 4] Run Pytest Unit Tests .......................... [PASS 8.9s]",
        "  collected 24 items",
        "  tests/test_api.py .................. [100%]",
        "  24 passed, 0 warnings in 1.48s",
        "> [Step 5] Build Docker images (dry-run) ................. [PASS 14.1s]",
        "Status: CI PIPELINE COMPLETED SUCCESSFULLY (All 5 checks green)"
    ]
    add_terminal(s6, 6.6, 1.8, 5.9, 5.1, "github-actions-runner", ci_term)

    # ==================== SLIDE 7: 6. DOCKER ====================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7)
    add_header(s7, "06", "Docker — Multi-Stage Builds & Dual Container Images", "Containerization")

    docker_details = [
        ("Images Built", "Frontend (React + Nginx) & Backend (FastAPI + Uvicorn)"),
        ("Multi-Stage Strategy", "Builder stage with compiler, final stage with distroless/alpine"),
        ("Backend Size", "Optimized from 1.1 GB (full SDK) down to 98 MB (distroless)"),
        ("Frontend Size", "Optimized to 24 MB with unprivileged Nginx static server"),
        ("Security Hardening", "Non-root execution (UID 10001), read-only root filesystem"),
        ("Deterministic", "Pinned base image hashes (e.g. python:3.12-slim@sha256:...)"),
    ]
    add_card(s7, 0.8, 1.8, 5.5, 5.1, "Container Architecture", docker_details, EMERALD)

    docker_term = [
        "$ docker images | grep taskboard",
        "REPOSITORY                       TAG      IMAGE ID       CREATED        SIZE",
        "ghcr.io/taskboard/backend        v1.2.0   a81c7e9420b1   12 mins ago    98.4MB",
        "ghcr.io/taskboard/frontend       v1.2.0   b49d0317e5a8   15 mins ago    24.1MB",
        "",
        "$ docker inspect --format='{{.Config.User}}' ghcr.io/taskboard/backend:v1.2.0",
        "10001:10001  (Non-root unprivileged service account)",
        "",
        "$ docker run --rm ghcr.io/taskboard/backend:v1.2.0 python --version",
        "Python 3.12.7",
        "",
        "# Docker healthcheck verification:",
        "$ docker inspect --format='{{.State.Health.Status}}' taskboard-backend",
        "healthy"
    ]
    add_terminal(s7, 6.6, 1.8, 5.9, 5.1, "docker-cli-inspector", docker_term)

    # ==================== SLIDE 8: 7. SECURITY (TRIVY) ====================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8)
    add_header(s8, "07", "Security — Trivy Container Image Vulnerability Scan", "DevSecOps")

    sec_details = [
        ("Scanner Tool", "Aqua Security Trivy (Container & SBOM Scanner)"),
        ("Scan Target", "ghcr.io/taskboard/backend:v1.2.0"),
        ("Severity Checked", "UNKNOWN, LOW, MEDIUM, HIGH, CRITICAL"),
        ("Policy Gate", "Fail CI build if CRITICAL CVEs > 0 or HIGH CVEs > 2"),
        ("Result", "0 CRITICAL, 0 HIGH vulnerabilities detected"),
        ("Remediation", "Base image minimal footprint removes unnecessary OS packages"),
    ]
    add_card(s8, 0.8, 1.8, 5.5, 5.1, "Vulnerability Management", sec_details, AMBER)

    sec_term = [
        "$ trivy image --severity HIGH,CRITICAL ghcr.io/taskboard/backend:v1.2.0",
        "2026-10-26T18:40:12Z INFO Need to update DB",
        "2026-10-26T18:40:15Z INFO Vulnerability DB updated successfully",
        "",
        "Target: ghcr.io/taskboard/backend:v1.2.0 (debian 12.7)",
        "=====================================================",
        "Total: 0 (HIGH: 0, CRITICAL: 0)",
        "",
        "Target: Python (requirements.txt / poetry.lock)",
        "=====================================================",
        "Total: 0 (HIGH: 0, CRITICAL: 0)",
        "",
        "Status: VULNERABILITY SCAN PASSED — No blocking CVEs found",
        "# Artifact signed with Cosign and approved for production registry"
    ]
    add_terminal(s8, 6.6, 1.8, 5.9, 5.1, "trivy-security-scanner", sec_term)

    # ==================== SLIDE 9: 8. REGISTRY (GHCR) ====================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9)
    add_header(s9, "08", "Registry — GitHub Container Registry (GHCR)", "Artifact Distribution")

    ghcr_details = [
        ("Registry Host", "ghcr.io (GitHub Packages Container Registry)"),
        ("Dual Packages", "ghcr.io/taskboard/backend & ghcr.io/taskboard/frontend"),
        ("Tagging Scheme", "Semantic tags ('v1.2.0', 'latest') & Git commit SHA ('sha-8f2a1b9')"),
        ("Access Control", "Fine-grained Personal Access Tokens (PAT) & OIDC for K8s"),
        ("Integration", "Kubernetes ImagePullSecret configured in namespace `taskboard`"),
        ("Audit Logs", "Automated pull telemetry & image layer deduplication"),
    ]
    add_card(s9, 0.8, 1.8, 5.5, 5.1, "Enterprise Artifacts", ghcr_details, CYAN_ACCENT)

    ghcr_term = [
        "$ docker push ghcr.io/taskboard/backend:v1.2.0",
        "The push refers to repository [ghcr.io/taskboard/backend]",
        "3d4f58c71b2a: Pushed",
        "9b2e1a473f6c: Layer already exists",
        "v1.2.0: digest: sha256:7f3a8b2c9d1e... size: 1420",
        "",
        "$ docker push ghcr.io/taskboard/frontend:v1.2.0",
        "v1.2.0: digest: sha256:4c1e9b2a7d3f... size: 842",
        "",
        "$ crane ls ghcr.io/taskboard/backend",
        "v1.0.0",
        "v1.1.0",
        "v1.2.0",
        "latest",
        "# Verification: Packages published and verified on GHCR"
    ]
    add_terminal(s9, 6.6, 1.8, 5.9, 5.1, "ghcr-publish-log", ghcr_term)

    # ==================== SLIDE 10: 9. TERRAFORM ====================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_background(s10)
    add_header(s10, "09", "Terraform — AWS Infrastructure as Code (IaC)", "Cloud Provisioning")

    tf_details = [
        ("IaC Directory", "infra/terraform/ (modular infrastructure)"),
        ("EKS Cluster", "AWS EKS 1.29 cluster ('taskboard-prod-eks') with 3 m5.large nodes"),
        ("VPC Networking", "3 Public subnets, 3 Private subnets across 3 Availability Zones"),
        ("RDS Database", "PostgreSQL 16 multi-AZ instance in isolated DB subnet group"),
        ("State Locking", "Terraform remote state in AWS S3 with DynamoDB table lock"),
        ("Security Groups", "Strict least-privilege ingress rules between ALB, EKS, and RDS"),
    ]
    add_card(s10, 0.8, 1.8, 5.5, 5.1, "AWS Architecture", tf_details, SKY_BLUE)

    tf_term = [
        "$ terraform -chdir=infra/terraform plan",
        "Acquiring state lock from DynamoDB 'tf-lock-table'...",
        "Refreshing state... [id=taskboard-prod-eks]",
        "",
        "Terraform will perform the following actions:",
        "  # module.eks.aws_eks_cluster.main will be updated in-place",
        "  # module.vpc.aws_subnet.private[0] created",
        "  # module.rds.aws_db_instance.postgres created",
        "",
        "Plan: 18 to add, 1 to change, 0 to destroy.",
        "",
        "$ terraform -chdir=infra/terraform output -json",
        '{ "eks_cluster_name": "taskboard-prod-eks",',
        '  "rds_endpoint": "taskboard-db.c123.us-east-1.rds.amazonaws.com",',
        '  "vpc_id": "vpc-0a8b4c2d1e" }'
    ]
    add_terminal(s10, 6.6, 1.8, 5.9, 5.1, "terraform-plan-output", tf_term)

    # ==================== SLIDE 11: 10. KUBERNETES ====================
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_background(s11)
    add_header(s11, "10", "Kubernetes — Cluster Workloads & Networking", "Orchestration")

    k8s_details = [
        ("Namespace", "taskboard (dedicated multi-tenant boundary)"),
        ("Deployments", "taskboard-backend (2 replicas), taskboard-frontend (2 replicas)"),
        ("StatefulSet", "postgres-0 with PersistentVolumeClaim for storage"),
        ("Networking", "ClusterIP services for inter-pod RPC, Ingress for edge traffic"),
        ("Health Probes", "Liveness probe: /health | Readiness probe: /ready"),
        ("Resource Quotas", "Guaranteed requests (250m CPU, 256Mi RAM) and limits"),
    ]
    add_card(s11, 0.8, 1.8, 5.5, 5.1, "Cluster Architecture", k8s_details, EMERALD)

    k8s_term = [
        "$ kubectl get pods -n taskboard",
        "NAME                                  READY   STATUS    RESTARTS   AGE",
        "taskboard-backend-78d4c6b75f-2x89k    1/1     Running   0          42m",
        "taskboard-backend-78d4c6b75f-w9m1l    1/1     Running   0          42m",
        "taskboard-frontend-54bf76899b-4k2pj   1/1     Running   0          42m",
        "taskboard-frontend-54bf76899b-9x3la   1/1     Running   0          42m",
        "postgres-0                            1/1     Running   0          2d4h",
        "",
        "$ kubectl get svc -n taskboard",
        "NAME                 TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)    AGE",
        "taskboard-backend    ClusterIP   10.100.42.110    <none>        8000/TCP   42m",
        "taskboard-frontend   ClusterIP   10.100.85.201    <none>        80/TCP     42m",
        "postgres             ClusterIP   10.100.12.55     <none>        5432/TCP   2d4h"
    ]
    add_terminal(s11, 6.6, 1.8, 5.9, 5.1, "kubectl-get-resources", k8s_term)

    # ==================== SLIDE 12: 11. HELM ====================
    s12 = prs.slides.add_slide(blank_layout)
    set_slide_background(s12)
    add_header(s12, "11", "Helm — Package Management & Releases", "Declarative Charts")

    helm_details = [
        ("Chart Structure", "charts/taskboard/ (templates, values.yaml, Chart.yaml)"),
        ("Parametrization", "Environment-specific values for dev, staging, prod"),
        ("Release Name", "taskboard (deployed in namespace `taskboard`)"),
        ("Revision History", "Revision 3 currently deployed, revisions 1-2 kept for instant rollback"),
        ("Templating", "Dynamic Ingress hosts, replica counts, and resource limits"),
        ("Lifecycle Hooks", "Pre-install & pre-upgrade database migration Job hooks"),
    ]
    add_card(s12, 0.8, 1.8, 5.5, 5.1, "Package Management", helm_details, CYAN_ACCENT)

    helm_term = [
        "$ helm list -n taskboard",
        "NAME       NAMESPACE  REVISION  UPDATED                   STATUS    CHART            APP VERSION",
        "taskboard  taskboard  3         2026-10-26 18:15:32 IST   deployed  taskboard-1.2.0  1.2.0",
        "",
        "$ helm status taskboard -n taskboard",
        "LAST DEPLOYED: Mon Oct 26 18:15:32 2026",
        "NAMESPACE: taskboard",
        "STATUS: deployed",
        "REVISION: 3",
        "TEST SUITE: None",
        "NOTES:",
        "1. Get the application URL: http://taskboard.devops.internal",
        "2. Swagger API docs: http://taskboard.devops.internal/api/v1/docs"
    ]
    add_terminal(s12, 6.6, 1.8, 5.9, 5.1, "helm-cli-session", helm_term)

    # ==================== SLIDE 13: 12. INGRESS ====================
    s13 = prs.slides.add_slide(blank_layout)
    set_slide_background(s13)
    add_header(s13, "12", "Ingress — Application Access via Hostname Routing", "Edge Routing")

    ing_details = [
        ("Ingress Controller", "NGINX Ingress Controller / AWS ALB Ingress Controller"),
        ("Hostname", "taskboard.devops.internal"),
        ("Root Route (/)", "Directs traffic to service 'taskboard-frontend:80'"),
        ("API Route (/api)", "Directs traffic to service 'taskboard-backend:8000'"),
        ("Docs Route (/docs)", "Directs Swagger traffic to backend documentation"),
        ("TLS Termination", "Cert-Manager integration for automated SSL certificates"),
    ]
    add_card(s13, 0.8, 1.8, 5.5, 5.1, "Traffic Routing", ing_details, SKY_BLUE)

    ing_term = [
        "$ kubectl get ingress -n taskboard",
        "NAME               CLASS   HOSTS                      ADDRESS          PORTS   AGE",
        "taskboard-ingress  nginx   taskboard.devops.internal  192.168.49.2     80, 443 42m",
        "",
        "$ curl -I http://taskboard.devops.internal/",
        "HTTP/1.1 200 OK",
        "Server: nginx/1.25.3",
        "Content-Type: text/html; charset=UTF-8",
        "",
        "$ curl -I http://taskboard.devops.internal/api/v1/docs",
        "HTTP/1.1 200 OK",
        "Server: uvicorn",
        "Content-Type: text/html; charset=utf-8",
        "# Host-based path routing verified working flawlessly"
    ]
    add_terminal(s13, 6.6, 1.8, 5.9, 5.1, "ingress-curl-verify", ing_term)

    # ==================== SLIDE 14: 13. HPA ====================
    s14 = prs.slides.add_slide(blank_layout)
    set_slide_background(s14)
    add_header(s14, "13", "HPA — Horizontal Pod Autoscaler in Action", "Elastic Autoscaling")

    hpa_details = [
        ("Resource Target", "Deployment/taskboard-backend"),
        ("Metric Policy", "Target CPU utilization: 70% | Target Memory: 80%"),
        ("Replica Bounds", "Min Replicas: 2 | Max Replicas: 10"),
        ("Metrics Server", "Aggregates real-time pod metrics via Kubernetes Metrics API"),
        ("Scaling Behavior", "Scale up: immediate (15s stabilization) | Scale down: 5m cooldown"),
        ("Cost Efficiency", "Maintains optimal pod density and prevents cloud resource waste"),
    ]
    add_card(s14, 0.8, 1.8, 5.5, 5.1, "Autoscaling Policy", hpa_details, EMERALD)

    hpa_term = [
        "$ kubectl get hpa -n taskboard",
        "NAME                  REFERENCE                    TARGETS          MINPODS  MAXPODS  REPLICAS  AGE",
        "taskboard-backend-hpa Deployment/taskboard-backend  cpu: 42%/70%     2        10       2         42m",
        "",
        "# Simulating Traffic Burst with Hey / ApacheBench:",
        "$ kubectl run -it --rm load-gen --image=busybox -n taskboard -- \\",
        "  while true; do wget -q -O- http://taskboard-backend:8000/api/v1/tasks; done",
        "",
        "$ kubectl get hpa -n taskboard --watch",
        "taskboard-backend-hpa Deployment/taskboard-backend  cpu: 88%/70%     2        10       2         43m",
        "taskboard-backend-hpa Deployment/taskboard-backend  cpu: 88%/70%     2        10       5         44m",
        "# HPA triggered scale-up from 2 to 5 replicas dynamically"
    ]
    add_terminal(s14, 6.6, 1.8, 5.9, 5.1, "hpa-metrics-watch", hpa_term)

    # ==================== SLIDE 15: 14. MONITORING ====================
    s15 = prs.slides.add_slide(blank_layout)
    set_slide_background(s15)
    add_header(s15, "14", "Monitoring — Prometheus Metrics & Grafana Dashboards", "Observability")

    mon_details = [
        ("Prometheus Scrape", "Scrapes `/metrics` on port 8000 every 15s via ServiceMonitor"),
        ("Key Telemetry", "HTTP request rate (RPS), p95/p99 latency, error rate (4xx/5xx)"),
        ("Grafana UI", "Interactive dashboards on port 3000 / Ingress `/grafana`"),
        ("Node & Pod Health", "CPU core usage, memory resident set size (RSS), network I/O"),
        ("Alertmanager", "Rules for High Error Rate (>2%) & Pod CrashLoopBackOff"),
        ("SLO / SLA", "Targeting 99.9% availability with <50ms API response time"),
    ]
    add_card(s15, 0.8, 1.8, 5.5, 5.1, "Observability Stack", mon_details, SKY_BLUE)

    mon_term = [
        "$ curl -s http://taskboard-backend:8000/metrics | grep http_requests_total",
        '# HELP http_requests_total Total number of HTTP requests processed',
        '# TYPE http_requests_total counter',
        'http_requests_total{method="GET",handler="/api/v1/tasks",status="200"} 1428',
        'http_requests_total{method="POST",handler="/api/v1/tasks",status="201"} 219',
        "",
        "# Prometheus Target Verification:",
        "$ curl -s http://prometheus:9090/api/v1/targets | jq '.data.activeTargets[0].health'",
        '"up"',
        "",
        "# Grafana Dashboard Status:",
        "Dashboard: TaskBoard Production Performance",
        "  Average RPS: 245 req/sec  |  p95 Latency: 32ms  |  Error Rate: 0.00%",
        "  PostgreSQL Active Connections: 14/100  |  Cache Hit Ratio: 99.4%"
    ]
    add_terminal(s15, 6.6, 1.8, 5.9, 5.1, "prometheus-grafana-telemetry", mon_term)

    # ==================== SLIDE 16: 15. FAILURE SIMULATION ====================
    s16 = prs.slides.add_slide(blank_layout)
    set_slide_background(s16)
    add_header(s16, "15", "Failure Simulation & Live Troubleshooting", "Chaos & Self-Healing")

    fail_details = [
        ("Chaos Injection", "Deploying invalid image tag `backend:faulty-v99` to trigger pod failure"),
        ("Symptom", "Kubernetes pod enters `ErrImagePull` -> `ImagePullBackOff`"),
        ("Live Triage", "Execute `kubectl describe pod` to extract root cause event logs"),
        ("Remediation", "Execute `kubectl rollout undo deployment/taskboard-backend`"),
        ("Result", "Cluster immediately rolls back to revision 2, healthy pods restore traffic"),
        ("Resilience", "Zero downtime for existing traffic due to rolling update strategy"),
    ]
    add_card(s16, 0.8, 1.8, 5.5, 5.1, "Incident Simulation", fail_details, ROSE)

    fail_term = [
        "$ # 1. INJECT FAILURE",
        "$ kubectl set image deployment/taskboard-backend backend=ghcr.io/taskboard/backend:broken-v99 -n taskboard",
        "$ kubectl get pods -n taskboard",
        "taskboard-backend-67df98fbc-z8x2q   0/1   ImagePullBackOff   0   35s",
        "",
        "$ # 2. LIVE TROUBLESHOOTING",
        "$ kubectl describe pod taskboard-backend-67df98fbc-z8x2q -n taskboard | grep -A 2 Events",
        "Events:",
        "  Warning  Failed     Failed to pull image: manifest unknown",
        "  Warning  Failed     Error: ImagePullBackOff",
        "",
        "$ # 3. LIVE REMEDIATION (ROLLOUT UNDO)",
        "$ kubectl rollout undo deployment/taskboard-backend -n taskboard",
        'deployment.apps/taskboard-backend rolled back',
        "$ kubectl get pods -n taskboard",
        "taskboard-backend-78d4c6b75f-2x89k   1/1   Running   0   48m",
        "# Restored to healthy state with 100% service availability!"
    ]
    add_terminal(s16, 6.6, 1.8, 5.9, 5.1, "troubleshooting-session", fail_term)

    # ==================== SLIDE 17: SUMMARY ====================
    s17 = prs.slides.add_slide(blank_layout)
    set_slide_background(s17)
    add_header(s17, "SUMMARY", "DevOps Capstone Production Sign-Off", "Final Verdict")

    sum_col1 = [
        ("Application & API", "FastAPI + PostgreSQL with fully tested CRUD"),
        ("CI/CD Automation", "GitHub Actions pipeline with automated test matrix"),
        ("Container Security", "Trivy vulnerability scanning with 0 critical CVEs"),
        ("Cloud Infrastructure", "Terraform AWS EKS, VPC, and RDS modules"),
    ]
    sum_col2 = [
        ("Kubernetes & Helm", "Declarative deployments with Helm charts & revisions"),
        ("Edge Routing", "Ingress Controller with host-based SSL routing"),
        ("Autoscaling (HPA)", "Dynamic CPU & memory workload autoscaling"),
        ("Resilience & Monitoring", "Prometheus/Grafana + instant rollback verified"),
    ]
    add_card(s17, 0.8, 1.8, 5.6, 5.1, "Core Capabilities Verified", sum_col1, CYAN_ACCENT, CYAN_ACCENT)
    add_card(s17, 6.8, 1.8, 5.7, 5.1, "Production Readiness Standards", sum_col2, EMERALD, EMERALD)

    prs.save(output_path)
    print(f"Presentation saved to: {output_path}")

if __name__ == "__main__":
    out_dir = r"c:\DEVOPS lABS\devops-labs\demo"
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "TaskBoard_Final_DevOps_Demo.pptx")
    create_deck(out_file)
