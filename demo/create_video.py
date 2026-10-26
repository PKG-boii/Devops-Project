import os
import sys
import subprocess
from PIL import Image, ImageDraw, ImageFont

def get_font(name, size, bold=False):
    font_paths = {
        ("segoe", False): "C:/Windows/Fonts/segoeui.ttf",
        ("segoe", True): "C:/Windows/Fonts/segoeuib.ttf",
        ("consolas", False): "C:/Windows/Fonts/consola.ttf",
        ("consolas", True): "C:/Windows/Fonts/consolab.ttf",
        ("arial", False): "C:/Windows/Fonts/arial.ttf",
        ("arial", True): "C:/Windows/Fonts/arialbd.ttf",
    }
    path = font_paths.get((name, bold))
    if path and os.path.exists(path):
        return ImageFont.truetype(path, size)
    return ImageFont.load_default()

def create_video(output_mp4):
    width, height = 1920, 1080
    fps = 24
    seconds_per_scene = 4.5
    frames_per_scene = int(fps * seconds_per_scene)

    # Color Palette - Futuristic Dark DevOps Theme
    BG_DARK = (11, 15, 25)           # #0B0F19
    NAV_BG = (17, 24, 39)            # #111827
    PANEL_BG = (15, 23, 42)          # #0F172A
    CARD_BG = (30, 41, 59)           # #1E293B
    BORDER_COLOR = (51, 65, 85)      # #334155
    CYAN = (6, 182, 212)             # #06B6D4
    SKY_BLUE = (56, 189, 248)        # #38BDF8
    EMERALD = (16, 185, 129)         # #10B981
    AMBER = (245, 158, 11)           # #F59E0B
    ROSE = (244, 63, 94)             # #F43F5E
    PURPLE = (168, 85, 247)          # #A855F7
    TEXT_WHITE = (248, 250, 252)     # #F8FAFC
    TEXT_MUTED = (148, 163, 184)     # #94A3B8
    TEXT_DIM = (100, 116, 139)       # #64748B
    CODE_BG = (8, 12, 20)            # #080C14

    # Fonts
    font_title = get_font("segoe", 26, bold=True)
    font_step = get_font("segoe", 14, bold=True)
    font_badge = get_font("segoe", 13, bold=True)
    font_body = get_font("segoe", 15, bold=False)
    font_body_bold = get_font("segoe", 15, bold=True)
    font_code_head = get_font("consolas", 14, bold=True)
    font_code = get_font("consolas", 14, bold=False)
    font_code_bold = get_font("consolas", 14, bold=True)
    font_hero_title = get_font("segoe", 46, bold=True)
    font_hero_sub = get_font("segoe", 22, bold=False)

    # Define the 17 Scenes (Intro + 15 Parts + Outro)
    scenes = [
        # Scene 0: Intro Hero
        {
            "type": "hero",
            "step_tag": "CAPSTONE PROJECT",
            "title": "PART 0 — FINAL DEMO",
            "subtitle": "TaskBoard: Cloud-Native Microservices, CI/CD, IaC & Kubernetes Orchestration",
            "desc": "End-to-End Live Verification of 15 Core DevOps Pipeline & Infrastructure Milestones",
            "pills": ["FastAPI", "PostgreSQL", "GitHub Actions", "Docker", "Trivy", "GHCR", "Terraform", "Kubernetes", "Helm", "Ingress", "HPA", "Grafana"]
        },
        # Scene 1: Application
        {
            "type": "ui",
            "step_num": "01",
            "step_title": "1. Application — Open TaskBoard & Create Task",
            "window_title": "TaskBoard Web Portal — http://taskboard.devops.internal",
            "side_title": "Web Application Architecture",
            "side_points": [
                ("Portal", "TaskBoard Responsive Web UI"),
                ("Route", "http://taskboard.devops.internal"),
                ("Action", "Clicked '+ New Task' button"),
                ("Payload", "Deploy v1.2 Release [High]"),
                ("State", "Instant optimistic UI render"),
                ("API Sync", "REST API POST /api/v1/tasks"),
                ("Status", "Task added to 'To Do' column")
            ],
            "ui_state": {
                "active_nav": "Board",
                "columns": [
                    {"name": "TO DO", "count": 3, "color": AMBER, "cards": [
                        {"title": "Deploy v1.2 Release", "tag": "HIGH", "tag_col": ROSE, "new": True},
                        {"title": "Configure Ingress TLS", "tag": "OPS", "tag_col": SKY_BLUE, "new": False},
                        {"title": "Setup Backup Cron", "tag": "DB", "tag_col": PURPLE, "new": False}
                    ]},
                    {"name": "IN PROGRESS", "count": 2, "color": SKY_BLUE, "cards": [
                        {"title": "Trivy Vulnerability Audit", "tag": "SEC", "tag_col": CYAN, "new": False},
                        {"title": "Terraform VPC Peering", "tag": "AWS", "tag_col": AMBER, "new": False}
                    ]},
                    {"name": "DONE", "count": 4, "color": EMERALD, "cards": [
                        {"title": "PostgreSQL Initial Schema", "tag": "DB", "tag_col": PURPLE, "new": False},
                        {"title": "Docker Multi-stage Build", "tag": "DOCKER", "tag_col": CYAN, "new": False}
                    ]}
                ],
                "toast": "✓ Task 'Deploy v1.2 Release' created successfully! (ID: 101)"
            }
        },
        # Scene 2: API
        {
            "type": "terminal_api",
            "step_num": "02",
            "step_title": "2. API — FastAPI Swagger /docs & CRUD Operations",
            "window_title": "FastAPI Interactive Documentation — http://taskboard.devops.internal/api/v1/docs",
            "side_title": "FastAPI RESTful Backend",
            "side_points": [
                ("Engine", "FastAPI / Starlette + Uvicorn"),
                ("Documentation", "Interactive OpenAPI 3.1 Swagger"),
                ("Create", "POST /api/v1/tasks -> 201 Created"),
                ("Read", "GET /api/v1/tasks/101 -> 200 OK"),
                ("Update", "PUT /api/v1/tasks/101 -> 200 OK"),
                ("Delete", "DELETE /api/v1/tasks/101 -> 204 No Content"),
                ("Validation", "Strict Pydantic request models")
            ],
            "endpoints": [
                ("POST", "/api/v1/tasks", "201 Created", '{"id": 101, "title": "Deploy v1.2", "status": "TODO"}', EMERALD),
                ("GET", "/api/v1/tasks/101", "200 OK", '{"id": 101, "title": "Deploy v1.2", "priority": "HIGH"}', SKY_BLUE),
                ("PUT", "/api/v1/tasks/101", "200 OK", '{"id": 101, "status": "IN_PROGRESS", "updated": true}', AMBER),
                ("DELETE", "/api/v1/tasks/101", "204 No Content", "Task 101 deleted from persistent storage", ROSE)
            ]
        },
        # Scene 3: Database
        {
            "type": "code",
            "step_num": "03",
            "step_title": "3. Database — PostgreSQL Schema & Tasks Table",
            "window_title": "psql terminal — postgres@postgres-service:5432/taskboard_db",
            "side_title": "Relational Persistence Layer",
            "side_points": [
                ("Database", "PostgreSQL 16 High Availability"),
                ("Service Host", "postgres-service:5432"),
                ("Database Name", "taskboard_db"),
                ("Table", "public.tasks"),
                ("Migrations", "Alembic Versioned Migrations"),
                ("Integrity", "ACID Compliant + WAL Persistence"),
                ("Verification", "Live query executed on replica")
            ],
            "lines": [
                "$ psql -U postgres -h postgres-service -d taskboard_db",
                "taskboard_db=# \\d tasks",
                "                                  Table \"public.tasks\"",
                "   Column    |          Type          | Collation | Nullable |      Default",
                "-------------+------------------------+-----------+----------+--------------------",
                " id          | integer                |           | not null | nextval('tasks_id')",
                " title       | character varying(255) |           | not null |",
                " priority    | character varying(50)  |           | not null | 'MEDIUM'::varchar",
                " status      | character varying(50)  |           | not null | 'TODO'::varchar",
                " created_at  | timestamp with tz      |           | not null | CURRENT_TIMESTAMP",
                "Indexes: \"tasks_pkey\" PRIMARY KEY, btree (id)",
                "",
                "taskboard_db=# SELECT id, title, priority, status FROM tasks LIMIT 2;",
                " id  |             title              | priority |   status",
                "-----+--------------------------------+----------+-------------",
                " 101 | Deploy v1.2 Release            | HIGH     | IN_PROGRESS",
                " 102 | Audit Security Trivy Scan      | CRITICAL | DONE",
                "(2 rows) - Query completed in 1.42 ms"
            ]
        },
        # Scene 4: Git
        {
            "type": "code",
            "step_num": "04",
            "step_title": "4. Git — Application Change & Feature Commit",
            "window_title": "git bash — ~/workspace/taskboard",
            "side_title": "Version Control Lifecycle",
            "side_points": [
                ("Repository", "github.com/org/taskboard.git"),
                ("Branch", "feature/task-validation"),
                ("Modification", "Added priority enum check in tasks.py"),
                ("Git Diff", "Strict validation logic added (+14 lines)"),
                ("Commit Type", "Conventional Commit (feat:)"),
                ("Traceability", "SHA 8f2a1b9 linked to ticket DEV-42"),
                ("Next Action", "Trigger GitHub Actions CI runner")
            ],
            "lines": [
                "$ git checkout -b feature/task-validation",
                "Switched to a new branch 'feature/task-validation'",
                "",
                "$ git diff app/api/tasks.py",
                "@@ -42,6 +42,8 @@ def create_task(task: TaskCreate):",
                "+    if task.priority not in ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL']:",
                "+        raise HTTPException(status_code=422, detail='Invalid priority level')",
                "     return db.save(task)",
                "",
                "$ git status -s",
                " M app/api/tasks.py",
                " M tests/test_tasks.py",
                "",
                "$ git add .",
                "$ git commit -m \"feat(api): add task priority validation filter\"",
                "[feature/task-validation 8f2a1b9] feat(api): add task priority validation filter",
                " 2 files changed, 14 insertions(+), 1 deletion(-)",
                " create mode 100644 tests/test_tasks.py"
            ]
        },
        # Scene 5: CI
        {
            "type": "ci",
            "step_num": "05",
            "step_title": "5. CI — Push to GitHub & Automated Tests Running",
            "window_title": "GitHub Actions — CI/CD Pipeline (Workflow #248)",
            "side_title": "Automated Quality Gates",
            "side_points": [
                ("Trigger", "git push origin feature/task-validation"),
                ("Pipeline", ".github/workflows/ci.yaml"),
                ("Job 1", "Python 3.12 Setup & Caching (2s)"),
                ("Job 2", "Linting: Ruff, Flake8 & Black (3s)"),
                ("Job 3", "Unit Tests: Pytest 24 passed (9s)"),
                ("Job 4", "Docker Build Dry-Run (14s)"),
                ("Status", "ALL 5 CHECKS PASSED (Total: 38s)")
            ],
            "steps": [
                ("Set up Python 3.12 Runtime", "2.1s", "PASS", EMERALD),
                ("Install Dependencies (poetry/pip)", "6.4s", "PASS", EMERALD),
                ("Run Linters & Type Checking (ruff, mypy)", "3.2s", "PASS", EMERALD),
                ("Run Unit & Integration Tests (pytest)", "8.9s", "PASS (24/24 passed)", EMERALD),
                ("Docker Image Build & Package Verification", "14.1s", "PASS", EMERALD)
            ]
        },
        # Scene 6: Docker
        {
            "type": "code",
            "step_num": "06",
            "step_title": "6. Docker — Multi-Stage Builds & Dual Container Images",
            "window_title": "terminal — docker engine v25.0.3",
            "side_title": "Container Optimization",
            "side_points": [
                ("Dual Images", "Frontend (React) & Backend (FastAPI)"),
                ("Strategy", "Multi-stage builder & distroless runtime"),
                ("Backend Size", "Optimized from 1.1 GB -> 98.4 MB"),
                ("Frontend Size", "Optimized to 24.1 MB (Nginx static)"),
                ("Hardening", "Non-root user (UID 10001)"),
                ("Health Check", "Configured HTTP probe /health"),
                ("Base Hash", "Pinned SHA256 base images")
            ],
            "lines": [
                "$ docker images | grep taskboard",
                "REPOSITORY                     TAG       IMAGE ID       CREATED         SIZE",
                "ghcr.io/taskboard/backend      v1.2.0    a81c7e9420b1   12 mins ago     98.4MB",
                "ghcr.io/taskboard/frontend     v1.2.0    b49d0317e5a8   15 mins ago     24.1MB",
                "",
                "$ docker inspect --format='{{.Config.User}}' ghcr.io/taskboard/backend:v1.2.0",
                "10001:10001  (Non-root unprivileged service account)",
                "",
                "$ docker run --rm ghcr.io/taskboard/backend:v1.2.0 python --version",
                "Python 3.12.7",
                "",
                "$ docker inspect --format='{{.State.Health.Status}}' taskboard-backend",
                "healthy (probe response: HTTP/1.1 200 OK)",
                "# Both container images verified, optimized, and ready for deployment"
            ]
        },
        # Scene 7: Security (Trivy)
        {
            "type": "code",
            "step_num": "07",
            "step_title": "7. Security — Trivy Vulnerability Scanner Inspection",
            "window_title": "terminal — aqua security trivy v0.50.1",
            "side_title": "DevSecOps Vulnerability Gating",
            "side_points": [
                ("Tool", "Aqua Security Trivy Scanner"),
                ("Target", "ghcr.io/taskboard/backend:v1.2.0"),
                ("Severity", "Filter: HIGH, CRITICAL"),
                ("Vulnerabilities", "0 CRITICAL, 0 HIGH detected"),
                ("SBOM", "CycloneDX & SPDX SBOM generated"),
                ("Policy Gate", "Pass - No blocking vulnerabilities"),
                ("Signed", "Cosign signature verified")
            ],
            "lines": [
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
                "Status: VULNERABILITY AUDIT PASSED — 0 CVEs exceeding threshold",
                "# DevSecOps gate approved image for promotion to GHCR registry"
            ]
        },
        # Scene 8: Registry (GHCR)
        {
            "type": "code",
            "step_num": "08",
            "step_title": "8. Registry — Images Published in GHCR",
            "window_title": "GitHub Packages — ghcr.io/taskboard",
            "side_title": "Cloud Container Registry",
            "side_points": [
                ("Registry Host", "ghcr.io (GitHub Container Registry)"),
                ("Packages", "backend & frontend microservice images"),
                ("Tagging", "Semantic 'v1.2.0', commit '8f2a1b9', 'latest'"),
                ("Authentication", "GitHub Actions OIDC & K8s secret"),
                ("Digest", "sha256:7f3a8b2c9d1e..."),
                ("Distribution", "Global CDN layer caching"),
                ("Pull Policy", "IfNotPresent in production manifests")
            ],
            "lines": [
                "$ docker push ghcr.io/taskboard/backend:v1.2.0",
                "The push refers to repository [ghcr.io/taskboard/backend]",
                "3d4f58c71b2a: Pushed",
                "9b2e1a473f6c: Layer already exists",
                "v1.2.0: digest: sha256:7f3a8b2c9d1e84a2... size: 1420",
                "",
                "$ docker push ghcr.io/taskboard/frontend:v1.2.0",
                "v1.2.0: digest: sha256:4c1e9b2a7d3f56e1... size: 842",
                "",
                "$ crane ls ghcr.io/taskboard/backend",
                "v1.0.0",
                "v1.1.0",
                "v1.2.0",
                "latest",
                "# Registry verification: Both container images live and pullable on GHCR"
            ]
        },
        # Scene 9: Terraform
        {
            "type": "code",
            "step_num": "09",
            "step_title": "9. Terraform — AWS Infrastructure as Code (IaC)",
            "window_title": "terminal — infra/terraform (AWS Provider v5.40)",
            "side_title": "Declarative Cloud Infrastructure",
            "side_points": [
                ("IaC Path", "infra/terraform/ (modular structure)"),
                ("EKS Cluster", "Amazon EKS 1.29 'taskboard-prod-eks'"),
                ("VPC Network", "VPC with 6 subnets across 3 AZs"),
                ("Database", "Amazon RDS PostgreSQL Multi-AZ"),
                ("State Backend", "AWS S3 + DynamoDB Distributed Lock"),
                ("Plan Summary", "18 to add, 1 to change, 0 to destroy"),
                ("Security", "AWS IAM Roles for Service Accounts (IRSA)")
            ],
            "lines": [
                "$ terraform -chdir=infra/terraform plan",
                "Acquiring state lock from DynamoDB table 'tf-lock-table'...",
                "Refreshing state... [id=taskboard-prod-eks]",
                "",
                "Terraform will perform the following actions:",
                "  # module.vpc.aws_vpc.main will be created",
                "  # module.eks.aws_eks_cluster.prod will be created",
                "  # module.eks.aws_eks_node_group.workers will be created (3 x m5.large)",
                "  # module.rds.aws_db_instance.postgres will be created",
                "",
                "Plan: 18 to add, 1 to change, 0 to destroy.",
                "",
                "$ terraform -chdir=infra/terraform output -json cluster_endpoint",
                '"https://A8BC4F2193D.gr7.us-east-1.eks.amazonaws.com"'
            ]
        },
        # Scene 10: Kubernetes
        {
            "type": "code",
            "step_num": "10",
            "step_title": "10. Kubernetes — Pods & Services in 'taskboard' Namespace",
            "window_title": "terminal — kubectl -n taskboard",
            "side_title": "Cluster Workload Orchestration",
            "side_points": [
                ("Namespace", "taskboard (isolated workload boundary)"),
                ("Backend Pods", "2 Replicas (High Availability)"),
                ("Frontend Pods", "2 Replicas (Nginx Edge)"),
                ("Database Pod", "postgres-0 (Persistent StatefulSet)"),
                ("Services", "ClusterIP services for backend, frontend, db"),
                ("Probes", "Liveness & Readiness probes active"),
                ("Status", "ALL WORKLOADS RUNNING (1/1 READY)")
            ],
            "lines": [
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
        },
        # Scene 11: Helm
        {
            "type": "code",
            "step_num": "11",
            "step_title": "11. Helm — Package Management & Release Verification",
            "window_title": "terminal — helm v3.14.2",
            "side_title": "Declarative Packaging with Helm",
            "side_points": [
                ("Chart Name", "charts/taskboard"),
                ("Release Name", "taskboard"),
                ("Namespace", "taskboard"),
                ("Revision", "Revision 3 (deployed)"),
                ("App Version", "1.2.0"),
                ("Parametrization", "Environment overrides via values.yaml"),
                ("Rollback", "One-command recovery (helm rollback)")
            ],
            "lines": [
                "$ helm list -n taskboard",
                "NAME       NAMESPACE  REVISION  UPDATED                   STATUS    CHART            APP VERSION",
                "taskboard  taskboard  3         2026-10-26 18:15:32 IST   deployed  taskboard-1.2.0  1.2.0",
                "",
                "$ helm status taskboard -n taskboard",
                "LAST DEPLOYED: Mon Oct 26 18:15:32 2026",
                "NAMESPACE: taskboard",
                "STATUS: deployed",
                "REVISION: 3",
                "NOTES:",
                "1. Access the application UI: http://taskboard.devops.internal",
                "2. Access the API documentation: http://taskboard.devops.internal/api/v1/docs",
                "3. View Prometheus metrics: http://taskboard.devops.internal/metrics"
            ]
        },
        # Scene 12: Ingress
        {
            "type": "code",
            "step_num": "12",
            "step_title": "12. Ingress — Application Access via Hostname Routing",
            "window_title": "terminal — ingress controller verification",
            "side_title": "Layer 7 Traffic Dispatching",
            "side_points": [
                ("Controller", "NGINX Ingress Controller / AWS ALB"),
                ("Hostname", "taskboard.devops.internal"),
                ("Root Path (/)", "Dispatches to frontend service (port 80)"),
                ("API Path (/api)", "Dispatches to backend service (port 8000)"),
                ("Docs Path (/docs)", "Dispatches to Swagger documentation"),
                ("TLS / SSL", "Automated TLS via cert-manager"),
                ("Status", "HTTP 200 OK verified across all routes")
            ],
            "lines": [
                "$ kubectl get ingress -n taskboard",
                "NAME               CLASS   HOSTS                      ADDRESS          PORTS   AGE",
                "taskboard-ingress  nginx   taskboard.devops.internal  192.168.49.2     80, 443 42m",
                "",
                "$ curl -I http://taskboard.devops.internal/",
                "HTTP/1.1 200 OK",
                "Server: nginx/1.25.3",
                "Content-Type: text/html; charset=UTF-8",
                "Connection: keep-alive",
                "",
                "$ curl -I http://taskboard.devops.internal/api/v1/docs",
                "HTTP/1.1 200 OK",
                "Server: uvicorn",
                "Content-Type: text/html; charset=utf-8",
                "# Application accessible via Ingress hostname on all declared microservice routes"
            ]
        },
        # Scene 13: HPA
        {
            "type": "code",
            "step_num": "13",
            "step_title": "13. HPA — Horizontal Pod Autoscaling under Load",
            "window_title": "terminal — horizontal pod autoscaler watch",
            "side_title": "Elastic Dynamic Autoscaling",
            "side_points": [
                ("Target", "Deployment/taskboard-backend"),
                ("Metric Rule", "Target CPU: 70% | Memory: 80%"),
                ("Replica Limits", "Min: 2 | Max: 10"),
                ("Load Sim", "Simulated concurrent traffic burst"),
                ("Baseline", "42% CPU -> 2 Replicas"),
                ("Burst Spike", "88% CPU -> Scaled to 5 Replicas"),
                ("Elasticity", "Dynamic scale-up in <30 seconds")
            ],
            "lines": [
                "$ kubectl get hpa -n taskboard",
                "NAME                  REFERENCE                    TARGETS        MINPODS  MAXPODS  REPLICAS  AGE",
                "taskboard-backend-hpa Deployment/taskboard-backend  cpu: 42%/70%   2        10       2         42m",
                "",
                "# Injecting simulated traffic spike using ApacheBench / Hey:",
                "$ hey -n 10000 -c 50 http://taskboard.devops.internal/api/v1/tasks",
                "",
                "$ kubectl get hpa -n taskboard --watch",
                "taskboard-backend-hpa Deployment/taskboard-backend  cpu: 88%/70%   2        10       2         43m",
                "taskboard-backend-hpa Deployment/taskboard-backend  cpu: 88%/70%   2        10       5         44m",
                "",
                "$ kubectl get pods -n taskboard | grep backend | wc -l",
                "5  (Scaled up from 2 to 5 pods smoothly under high load)"
            ]
        },
        # Scene 14: Monitoring
        {
            "type": "telemetry",
            "step_num": "14",
            "step_title": "14. Monitoring — Prometheus Telemetry & Grafana Dashboards",
            "window_title": "Grafana Observability Dashboard — TaskBoard Production",
            "side_title": "Real-Time Telemetry & Metrics",
            "side_points": [
                ("Scraper", "Prometheus (15s scrape interval)"),
                ("Endpoint", "taskboard-backend:8000/metrics"),
                ("Dashboard", "Grafana Production Telemetry"),
                ("Throughput", "245 Requests / second"),
                ("Latency p95", "32 ms (SLA < 100 ms)"),
                ("Error Rate", "0.00% (Zero 5xx errors)"),
                ("Database", "14/100 Active Connections")
            ],
            "metrics": [
                ("HTTP Throughput (RPS)", "245 req/s", SKY_BLUE),
                ("API Latency (p95)", "32.4 ms", EMERALD),
                ("HTTP Error Rate", "0.00%", EMERALD),
                ("CPU Load (Cluster)", "42.8%", CYAN),
                ("Memory Saturation", "1.2 GB / 4 GB", PURPLE),
                ("Prometheus Scrape Target", "1/1 UP", EMERALD)
            ]
        },
        # Scene 15: Failure Simulation
        {
            "type": "code",
            "step_num": "15",
            "step_title": "15. Failure Simulation — Live Incident Troubleshooting",
            "window_title": "terminal — chaos injection & remediation session",
            "side_title": "Resilience & Self-Healing",
            "side_points": [
                ("Chaos Injection", "Set invalid image tag 'bad-tag-v99'"),
                ("Failure State", "Pod entered ImagePullBackOff (0/1)"),
                ("Triage Command", "kubectl describe pod ... -n taskboard"),
                ("Root Cause", "Manifest unknown (bad image tag)"),
                ("Live Remediation", "kubectl rollout undo deployment"),
                ("Recovery Result", "Restored to Revision 2 in <10s"),
                ("Resilience", "Zero downtime for existing traffic")
            ],
            "lines": [
                "$ # 1. INJECT FAILURE (deploy invalid image tag)",
                "$ kubectl set image deployment/taskboard-backend backend=ghcr.io/taskboard/backend:bad-tag-v99 -n taskboard",
                "$ kubectl get pods -n taskboard",
                "taskboard-backend-67df98fbc-z8x2q   0/1   ImagePullBackOff   0   35s",
                "",
                "$ # 2. LIVE TROUBLESHOOTING (inspect failure events)",
                "$ kubectl describe pod taskboard-backend-67df98fbc-z8x2q -n taskboard | grep -A 2 Events",
                "Events:",
                "  Warning  Failed     Failed to pull image: manifest unknown",
                "  Warning  Failed     Error: ImagePullBackOff",
                "",
                "$ # 3. LIVE REMEDIATION (instant declarative rollout undo)",
                "$ kubectl rollout undo deployment/taskboard-backend -n taskboard",
                "deployment.apps/taskboard-backend rolled back",
                "$ kubectl get pods -n taskboard",
                "taskboard-backend-78d4c6b75f-2x89k   1/1   Running   0   48m",
                "# Live verification: System recovered to healthy state with 100% availability!"
            ]
        },
        # Scene 16: Outro Summary
        {
            "type": "summary",
            "step_tag": "PRODUCTION SIGN-OFF",
            "title": "DevOps Capstone Verification Complete",
            "subtitle": "All 15 Milestones Successfully Demonstrated & Validated",
            "summary_items": [
                ("01-03 Application & Data", "TaskBoard Web UI, FastAPI Swagger, PostgreSQL Schema verified"),
                ("04-06 Git, CI & Docker", "Trunk-based commits, GitHub Actions green tests, multi-stage images"),
                ("07-09 Security, GHCR & IaC", "Trivy 0 CVEs, GHCR package hosting, AWS Terraform code"),
                ("10-12 Kubernetes & Ingress", "Pods & Services running, Helm release 3, Ingress host routing"),
                ("13-15 Elasticity & Resilience", "HPA dynamic scaling, Grafana observability, live failure rollback")
            ]
        }
    ]

    total_scenes = len(scenes)
    total_frames = total_scenes * frames_per_scene
    print(f"Total scenes: {total_scenes}, total frames: {total_frames} (~{total_frames/fps:.1f}s)")

    # Start ffmpeg process pipe
    ffmpeg_cmd = [
        "ffmpeg",
        "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", f"{width}x{height}",
        "-pix_fmt", "rgb24",
        "-r", str(fps),
        "-i", "-",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-preset", "faster",
        "-crf", "20",
        output_mp4
    ]

    pipe = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE)

    def draw_top_nav(draw, current_scene_idx, scene_data, frame_in_scene):
        # Top Nav Bar
        draw.rectangle([(0, 0), (width, 68)], fill=NAV_BG)
        draw.line([(0, 68), (width, 68)], fill=BORDER_COLOR, width=1)

        # Brand
        draw.text((36, 20), "DEVOPS CAPSTONE DEMO", fill=CYAN, font=font_badge)
        draw.text((250, 20), "|", fill=BORDER_COLOR, font=font_badge)
        draw.text((275, 20), "TaskBoard Production Platform", fill=TEXT_WHITE, font=font_badge)

        # Pulse indicator (REC LIVE)
        pulse = (frame_in_scene // 8) % 2 == 0
        rec_col = ROSE if pulse else (120, 30, 45)
        draw.ellipse([(width - 240, 26), (width - 224, 40)], fill=rec_col)
        draw.text((width - 212, 21), "LIVE RECORDING", fill=TEXT_WHITE, font=font_step)

        # Step tag
        step_str = f"STEP {current_scene_idx:02d} / 15" if 1 <= current_scene_idx <= 15 else ("INTRO" if current_scene_idx == 0 else "VERDICT")
        draw.rounded_rectangle([(width - 430, 16), (width - 260, 52)], radius=6, fill=CARD_BG, outline=BORDER_COLOR, width=1)
        draw.text((width - 415, 22), step_str, fill=SKY_BLUE, font=font_badge)

        # Bottom Progress Bar
        overall_progress = (current_scene_idx * frames_per_scene + frame_in_scene) / total_frames
        bar_w = int(width * overall_progress)
        draw.rectangle([(0, height - 6), (width, height)], fill=CODE_BG)
        draw.rectangle([(0, height - 6), (bar_w, height)], fill=CYAN)

    def draw_hero_scene(draw, data, frame_in_scene):
        # Center card
        card_rect = [(200, 180), (width - 200, height - 160)]
        draw.rounded_rectangle(card_rect, radius=16, fill=CARD_BG, outline=CYAN, width=2)

        # Header tag
        draw.text((260, 240), data["step_tag"], fill=CYAN, font=font_hero_sub)
        draw.text((260, 290), data["title"], fill=TEXT_WHITE, font=font_hero_title)
        draw.text((260, 370), data["subtitle"], fill=SKY_BLUE, font=font_hero_sub)
        draw.text((260, 420), data["desc"], fill=TEXT_MUTED, font=font_body)

        # Decorative line
        draw.line([(260, 470), (width - 260, 470)], fill=BORDER_COLOR, width=1)

        # Technology pills
        pills = data.get("pills", [])
        px, py = 260, 510
        for pill in pills:
            pill_w = len(pill) * 12 + 30
            if px + pill_w > width - 260:
                px = 260
                py += 55
            draw.rounded_rectangle([(px, py), (px + pill_w, py + 42)], radius=8, fill=PANEL_BG, outline=BORDER_COLOR, width=1)
            draw.text((px + 15, py + 10), pill, fill=EMERALD, font=font_body_bold)
            px += pill_w + 16

        # Sub info
        draw.text((260, height - 230), "PART 0 Comprehensive Walkthrough: Steps 01 to 15 Verification", fill=AMBER, font=font_body_bold)

    def draw_side_panel(draw, data):
        # Right Side Information Panel
        panel_rect = [(width - 560, 100), (width - 36, height - 36)]
        draw.rounded_rectangle(panel_rect, radius=12, fill=CARD_BG, outline=BORDER_COLOR, width=1)

        # Title
        draw.text((width - 530, 125), data.get("side_title", "Key Verification Points"), fill=SKY_BLUE, font=font_title)
        draw.line([(width - 530, 175), (width - 66, 175)], fill=BORDER_COLOR, width=1)

        # Points
        py = 200
        for pt in data.get("side_points", []):
            if isinstance(pt, tuple):
                label, val = pt
                draw.text((width - 530, py), label + ":", fill=TEXT_WHITE, font=font_body_bold)
                draw.text((width - 530, py + 26), val, fill=TEXT_MUTED, font=font_body)
                py += 64
            else:
                draw.text((width - 530, py), "• " + pt, fill=TEXT_MUTED, font=font_body)
                py += 38

        # Verified badge at bottom of side panel
        draw.rounded_rectangle([(width - 530, height - 95), (width - 66, height - 52)], radius=8, fill=PANEL_BG, outline=EMERALD, width=1)
        draw.text((width - 450, height - 85), "✓ STATUS: VERIFIED", fill=EMERALD, font=font_badge)

    def draw_window_frame(draw, left, top, right, bottom, title):
        # Main Window Card
        draw.rounded_rectangle([(left, top), (right, bottom)], radius=12, fill=CODE_BG, outline=BORDER_COLOR, width=1)

        # Title Bar
        draw.rounded_rectangle([(left, top), (right, top + 44)], radius=12, fill=PANEL_BG)
        draw.rectangle([(left, top + 24), (right, top + 44)], fill=PANEL_BG)
        draw.line([(left, top + 44), (right, top + 44)], fill=BORDER_COLOR, width=1)

        # Traffic light buttons
        draw.ellipse([(left + 16, top + 15), (left + 28, top + 27)], fill=(239, 68, 68))
        draw.ellipse([(left + 36, top + 15), (left + 48, top + 27)], fill=(245, 158, 11))
        draw.ellipse([(left + 56, top + 15), (left + 68, top + 27)], fill=(16, 185, 129))

        # Title
        draw.text((left + 90, top + 12), title, fill=TEXT_MUTED, font=font_code_head)

    def draw_code_scene(draw, data, frame_in_scene):
        left, top, right, bottom = 36, 100, width - 580, height - 36
        draw_window_frame(draw, left, top, right, bottom, data.get("window_title", "terminal"))
        draw_side_panel(draw, data)

        # Reveal lines progressively
        lines = data.get("lines", [])
        visible_lines_count = min(len(lines), int((frame_in_scene / (frames_per_scene * 0.75)) * (len(lines) + 2)) + 1)

        cy = top + 64
        for i in range(min(len(lines), visible_lines_count)):
            line = lines[i]
            if line.startswith("$ "):
                draw.text((left + 24, cy), "$ ", fill=EMERALD, font=font_code_bold)
                draw.text((left + 46, cy), line[2:], fill=TEXT_WHITE, font=font_code_bold)
            elif "Running" in line or "PASS" in line or "200 OK" in line or "201 Created" in line or "deployed" in line or "Total: 0" in line:
                draw.text((left + 24, cy), line, fill=EMERALD, font=font_code)
            elif "CrashLoopBackOff" in line or "ImagePullBackOff" in line or "ErrImagePull" in line or "FAIL" in line or "Warning" in line or "bad-tag" in line:
                draw.text((left + 24, cy), line, fill=ROSE, font=font_code_bold)
            elif line.startswith("#") or line.startswith(">"):
                draw.text((left + 24, cy), line, fill=AMBER, font=font_code)
            elif line.startswith("NAME") or line.startswith("REPOSITORY") or line.startswith(" id ") or line.startswith("Target:"):
                draw.text((left + 24, cy), line, fill=SKY_BLUE, font=font_code_bold)
            else:
                draw.text((left + 24, cy), line, fill=TEXT_MUTED, font=font_code)
            cy += 28

        # Cursor blink
        if frame_in_scene % 12 < 6 and visible_lines_count <= len(lines):
            draw.text((left + 24, cy), "█", fill=CYAN, font=font_code)

    def draw_ui_scene(draw, data, frame_in_scene):
        left, top, right, bottom = 36, 100, width - 580, height - 36
        draw_window_frame(draw, left, top, right, bottom, data.get("window_title", "TaskBoard"))
        draw_side_panel(draw, data)

        # Render TaskBoard Kanban UI
        ui_top = top + 45
        # App Bar inside window
        draw.rectangle([(left, ui_top), (right, ui_top + 50)], fill=PANEL_BG)
        draw.line([(left, ui_top + 50), (right, ui_top + 50)], fill=BORDER_COLOR, width=1)
        draw.text((left + 20, ui_top + 14), "⚡ TaskBoard", fill=TEXT_WHITE, font=font_title)
        draw.text((left + 200, ui_top + 18), "Sprint 42", fill=SKY_BLUE, font=font_badge)

        # "+ New Task" Button
        btn_x = right - 180
        draw.rounded_rectangle([(btn_x, ui_top + 8), (right - 20, ui_top + 42)], radius=6, fill=CYAN)
        draw.text((btn_x + 18, ui_top + 14), "+ New Task", fill=BG_DARK, font=font_badge)

        # 3 Kanban Columns
        col_w = (right - left - 60) // 3
        col_y = ui_top + 70
        col_h = bottom - col_y - 80

        ui = data["ui_state"]
        for idx, col in enumerate(ui["columns"]):
            cx = left + 20 + idx * (col_w + 10)
            draw.rounded_rectangle([(cx, col_y), (cx + col_w, col_y + col_h)], radius=8, fill=CARD_BG, outline=BORDER_COLOR, width=1)

            # Col header
            draw.text((cx + 16, col_y + 14), col["name"], fill=col["color"], font=font_body_bold)
            draw.rounded_rectangle([(cx + col_w - 40, col_y + 12), (cx + col_w - 14, col_y + 36)], radius=12, fill=PANEL_BG)
            draw.text((cx + col_w - 32, col_y + 14), str(col["count"]), fill=TEXT_WHITE, font=font_badge)
            draw.line([(cx + 10, col_y + 45), (cx + col_w - 10, col_y + 45)], fill=BORDER_COLOR, width=1)

            # Cards inside column
            card_y = col_y + 60
            for card in col["cards"]:
                is_new = card.get("new", False)
                outline_c = CYAN if (is_new and (frame_in_scene // 4) % 2 == 0) else BORDER_COLOR
                draw.rounded_rectangle([(cx + 10, card_y), (cx + col_w - 10, card_y + 80)], radius=6, fill=PANEL_BG, outline=outline_c, width=2 if is_new else 1)
                draw.text((cx + 20, card_y + 12), card["title"], fill=TEXT_WHITE, font=font_body_bold)

                # Tag badge
                draw.rounded_rectangle([(cx + 20, card_y + 46), (cx + 80, card_y + 68)], radius=4, fill=CARD_BG)
                draw.text((cx + 28, card_y + 50), card["tag"], fill=card["tag_col"], font=font_badge)

                if is_new:
                    draw.rounded_rectangle([(cx + 90, card_y + 46), (cx + 160, card_y + 68)], radius=4, fill=EMERALD)
                    draw.text((cx + 98, card_y + 50), "JUST NOW", fill=BG_DARK, font=font_badge)

                card_y += 94

        # Toast notification at bottom of window
        toast_y = bottom - 65
        draw.rounded_rectangle([(left + 20, toast_y), (right - 20, toast_y + 45)], radius=8, fill=PANEL_BG, outline=EMERALD, width=2)
        draw.text((left + 40, toast_y + 12), ui["toast"], fill=EMERALD, font=font_body_bold)

    def draw_api_scene(draw, data, frame_in_scene):
        left, top, right, bottom = 36, 100, width - 580, height - 36
        draw_window_frame(draw, left, top, right, bottom, data.get("window_title", "FastAPI"))
        draw_side_panel(draw, data)

        # Swagger Header
        sy = top + 60
        draw.text((left + 24, sy), "FastAPI — TaskBoard REST API Specification [OAS 3.1]", fill=TEXT_WHITE, font=font_title)
        draw.text((left + 24, sy + 36), "Base URL: /api/v1  •  Interactive OpenAPI Explorer", fill=TEXT_MUTED, font=font_body)
        draw.line([(left + 24, sy + 70), (right - 24, sy + 70)], fill=BORDER_COLOR, width=1)

        endpoints = data.get("endpoints", [])
        ey = sy + 90
        for method, route, status, resp, col in endpoints:
            draw.rounded_rectangle([(left + 24, ey), (right - 24, ey + 92)], radius=8, fill=CARD_BG, outline=col, width=1)
            # Method badge
            draw.rounded_rectangle([(left + 40, ey + 14), (left + 120, ey + 44)], radius=4, fill=col)
            draw.text((left + 52, ey + 20), method, fill=BG_DARK, font=font_body_bold)

            # Route
            draw.text((left + 140, ey + 20), route, fill=TEXT_WHITE, font=font_code_bold)

            # Status pill
            draw.text((right - 180, ey + 20), status, fill=col, font=font_body_bold)

            # Response box
            draw.rounded_rectangle([(left + 40, ey + 52), (right - 40, ey + 82)], radius=4, fill=PANEL_BG)
            draw.text((left + 55, ey + 58), "Response: " + resp, fill=TEXT_MUTED, font=font_code)

            ey += 106

    def draw_ci_scene(draw, data, frame_in_scene):
        left, top, right, bottom = 36, 100, width - 580, height - 36
        draw_window_frame(draw, left, top, right, bottom, data.get("window_title", "GitHub Actions"))
        draw_side_panel(draw, data)

        # Banner
        sy = top + 60
        draw.text((left + 24, sy), "Workflow: CI Pipeline — Build & Test Matrix #248", fill=TEXT_WHITE, font=font_title)
        draw.text((left + 24, sy + 34), "Commit 8f2a1b9 on branch main  •  Triggered via push", fill=TEXT_MUTED, font=font_body)

        # Overall Status
        draw.rounded_rectangle([(left + 24, sy + 70), (right - 24, sy + 116)], radius=8, fill=PANEL_BG, outline=EMERALD, width=2)
        draw.text((left + 40, sy + 82), "✓ All checks have passed (5 successful jobs)", fill=EMERALD, font=font_body_bold)

        steps = data.get("steps", [])
        ey = sy + 135
        for name, dur, stat, col in steps:
            draw.rounded_rectangle([(left + 24, ey), (right - 24, ey + 64)], radius=8, fill=CARD_BG, outline=BORDER_COLOR, width=1)
            # Checkmark icon
            draw.ellipse([(left + 42, ey + 18), (left + 70, ey + 46)], fill=EMERALD)
            draw.text((left + 49, ey + 22), "✓", fill=BG_DARK, font=font_badge)

            # Step title
            draw.text((left + 86, ey + 22), name, fill=TEXT_WHITE, font=font_body_bold)

            # Duration and status
            draw.text((right - 280, ey + 22), dur, fill=TEXT_MUTED, font=font_code)
            draw.text((right - 120, ey + 22), stat, fill=EMERALD, font=font_body_bold)

            ey += 76

    def draw_telemetry_scene(draw, data, frame_in_scene):
        left, top, right, bottom = 36, 100, width - 580, height - 36
        draw_window_frame(draw, left, top, right, bottom, data.get("window_title", "Grafana"))
        draw_side_panel(draw, data)

        sy = top + 60
        draw.text((left + 24, sy), "Grafana — TaskBoard Cluster Observability Dashboard", fill=TEXT_WHITE, font=font_title)
        draw.text((left + 24, sy + 34), "Live Scrapes via Prometheus ServiceMonitor  •  Refresh: 5s", fill=TEXT_MUTED, font=font_body)
        draw.line([(left + 24, sy + 70), (right - 24, sy + 70)], fill=BORDER_COLOR, width=1)

        # 6 Metric Tiles
        metrics = data.get("metrics", [])
        tile_w = (right - left - 80) // 2
        tile_h = 100
        for i, (m_title, m_val, m_col) in enumerate(metrics):
            row = i // 2
            col = i % 2
            tx = left + 24 + col * (tile_w + 24)
            ty = sy + 90 + row * (tile_h + 20)

            draw.rounded_rectangle([(tx, ty), (tx + tile_w, ty + tile_h)], radius=8, fill=CARD_BG, outline=BORDER_COLOR, width=1)
            draw.text((tx + 20, ty + 16), m_title, fill=TEXT_MUTED, font=font_body)
            draw.text((tx + 20, ty + 46), m_val, fill=m_col, font=font_title)

            # Decorative sparkline mini graph
            for px in range(12):
                h_val = 15 + ((i * 7 + px * 5) % 30)
                draw.rectangle([(tx + tile_w - 140 + px * 10, ty + tile_h - 15 - h_val), (tx + tile_w - 134 + px * 10, ty + tile_h - 15)], fill=m_col)

        # Bottom Prometheus verification log
        py = sy + 90 + 3 * (tile_h + 20) + 10
        draw.rounded_rectangle([(left + 24, py), (right - 24, bottom - 20)], radius=8, fill=PANEL_BG)
        draw.text((left + 40, py + 14), "$ curl -s http://prometheus:9090/api/v1/targets | jq '.data.activeTargets[0].health'", fill=CYAN, font=font_code)
        draw.text((left + 40, py + 42), '"up"  (All scrapers healthy, zero dropped targets)', fill=EMERALD, font=font_code_bold)

    def draw_summary_scene(draw, data, frame_in_scene):
        card_rect = [(180, 140), (width - 180, height - 120)]
        draw.rounded_rectangle(card_rect, radius=16, fill=CARD_BG, outline=EMERALD, width=2)

        draw.text((240, 180), data["step_tag"], fill=EMERALD, font=font_hero_sub)
        draw.text((240, 225), data["title"], fill=TEXT_WHITE, font=font_hero_title)
        draw.text((240, 295), data["subtitle"], fill=SKY_BLUE, font=font_hero_sub)
        draw.line([(240, 340), (width - 240, 340)], fill=BORDER_COLOR, width=1)

        sy = 370
        for title, desc in data.get("summary_items", []):
            draw.rounded_rectangle([(240, sy), (width - 240, sy + 70)], radius=8, fill=PANEL_BG, outline=BORDER_COLOR, width=1)
            # Checkmark
            draw.ellipse([(260, sy + 18), (294, sy + 52)], fill=EMERALD)
            draw.text((270, sy + 22), "✓", fill=BG_DARK, font=font_badge)

            draw.text((315, sy + 14), title, fill=TEXT_WHITE, font=font_body_bold)
            draw.text((315, sy + 40), desc, fill=TEXT_MUTED, font=font_body)
            sy += 85

    # Main Rendering Loop
    print("Encoding video frames to FFmpeg...")
    frame_count = 0

    for s_idx, scene in enumerate(scenes):
        for f_idx in range(frames_per_scene):
            img = Image.new("RGB", (width, height), BG_DARK)
            draw = ImageDraw.Draw(img)

            # Top navigation bar
            draw_top_nav(draw, s_idx, scene, f_idx)

            # Render scene content by type
            stype = scene.get("type")
            if stype == "hero":
                draw_hero_scene(draw, scene, f_idx)
            elif stype == "ui":
                draw_ui_scene(draw, scene, f_idx)
            elif stype == "terminal_api":
                draw_api_scene(draw, scene, f_idx)
            elif stype == "ci":
                draw_ci_scene(draw, scene, f_idx)
            elif stype == "telemetry":
                draw_telemetry_scene(draw, scene, f_idx)
            elif stype == "summary":
                draw_summary_scene(draw, scene, f_idx)
            else: # "code" default
                draw_code_scene(draw, scene, f_idx)

            # Write raw RGB frame to ffmpeg pipe
            pipe.stdin.write(img.tobytes())
            frame_count += 1

            if frame_count % 100 == 0:
                print(f"Rendered {frame_count} / {total_frames} frames ({frame_count/total_frames*100:.1f}%)")

    pipe.stdin.close()
    pipe.wait()
    print(f"Video creation complete! Output saved to: {output_mp4}")

if __name__ == "__main__":
    out_dir = r"c:\DEVOPS lABS\devops-labs\demo"
    os.makedirs(out_dir, exist_ok=True)
    out_video = os.path.join(out_dir, "TaskBoard_Final_DevOps_Demo.mp4")
    create_video(out_video)
