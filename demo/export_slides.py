import os
import subprocess

def extract_slide_images(mp4_path, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    # 17 scenes at 4.5s intervals (sample at 3.5s into each scene for complete display)
    scene_names = [
        "00_intro_architecture",
        "01_application_taskboard",
        "02_api_fastapi_swagger",
        "03_database_postgresql",
        "04_git_workflow_commit",
        "05_ci_github_actions",
        "06_docker_dual_images",
        "07_security_trivy_scan",
        "08_registry_ghcr",
        "09_terraform_aws_iac",
        "10_kubernetes_workloads",
        "11_helm_declarative_releases",
        "12_ingress_host_routing",
        "13_hpa_autoscaling",
        "14_monitoring_prometheus_grafana",
        "15_failure_simulation_troubleshooting",
        "16_production_signoff"
    ]

    print("Extracting high-resolution slide images from video...")
    for idx, name in enumerate(scene_names):
        timestamp = idx * 4.5 + 3.6
        out_file = os.path.join(out_dir, f"slide_{idx:02d}_{name}.png")
        cmd = [
            "ffmpeg", "-y",
            "-ss", f"{timestamp:.2f}",
            "-i", mp4_path,
            "-frames:v", "1",
            "-q:v", "2",
            out_file
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"Extracted: slide_{idx:02d}_{name}.png (time: {timestamp:.1f}s)")

    print(f"All {len(scene_names)} slide images exported to: {out_dir}")

if __name__ == "__main__":
    mp4 = r"c:\DEVOPS lABS\devops-labs\demo\TaskBoard_Final_DevOps_Demo.mp4"
    slides_folder = r"c:\DEVOPS lABS\devops-labs\demo\slides"
    extract_slide_images(mp4, slides_folder)
