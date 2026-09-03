# SentinelOne Windows Server host-performance test plan

Formal laboratory test plan for quantifying **CPU, RAM, Disk I/O, and kernel-level latency** overhead of the **SentinelOne Singularity Windows agent** on **Windows Server 2016, 2019, 2022, and 2025**.

## Artifact

- **PDF:** [SentinelOne_Windows_Server_Host_Performance_Test_Plan.pdf](./SentinelOne_Windows_Server_Host_Performance_Test_Plan.pdf)
- **Document ID:** `S1-WIN-HOST-PERF-TP-1.0`
- **Generator:** `generate_testplan_pdf.py` (ReportLab)

Regenerate:

```bash
python3 -m pip install reportlab
python3 docs/sentinelone-host-performance/generate_testplan_pdf.py
```

## Scope (short)

- Isolated **A–B–A** design (unmanaged → agentized → snapshot revert).
- Core cases: idle, DiskSpd + file churn, process-create storms, network/SMB throughput.
- Extended cases TC-05–TC-24 (registry, soak, Deep Visibility, Defender coexistence, SQL/IIS overlays, boot/minifilter WPR, and more).
- Telemetry: `logman`/Perfmon, WPR/WPA minifilter traces, `windows_exporter` + Prometheus + Grafana; Splunk optional.

Assumptions and open questions (SKU, policy, Defender RTP, hypervisor, SLOs) are listed in the PDF, Section 0.3 and Section 15.
