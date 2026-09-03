#!/usr/bin/env python3
"""Generate the SentinelOne Windows Server host-performance test plan PDF."""

from __future__ import annotations

from datetime import date
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    CondPageBreak,
    KeepTogether,
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

OUT = Path(__file__).with_name(
    "SentinelOne_Windows_Server_Host_Performance_Test_Plan.pdf"
)
DOC_ID = "S1-WIN-HOST-PERF-TP-1.0"
DOC_DATE = date(2026, 9, 3)
NAVY = colors.HexColor("#0B1F3A")
TEAL = colors.HexColor("#0E7490")
GOLD = colors.HexColor("#C4A35A")
LT = colors.HexColor("#F4F7FB")
ROW = colors.HexColor("#E8EEF6")
RED = colors.HexColor("#7F1D1D")


def styles():
    s = getSampleStyleSheet()
    s.add(
        ParagraphStyle(
            "CoverKicker",
            fontName="Times-Bold",
            fontSize=10,
            textColor=GOLD,
            alignment=TA_CENTER,
            tracking=1.2,
            spaceAfter=8,
        )
    )
    s.add(
        ParagraphStyle(
            "CoverTitle",
            fontName="Times-Bold",
            fontSize=22,
            leading=26,
            textColor=colors.white,
            alignment=TA_CENTER,
            spaceAfter=10,
        )
    )
    s.add(
        ParagraphStyle(
            "CoverSub",
            fontName="Times-Italic",
            fontSize=12,
            leading=16,
            textColor=colors.HexColor("#D6DEEA"),
            alignment=TA_CENTER,
            spaceAfter=6,
        )
    )
    s.add(
        ParagraphStyle(
            "CoverMeta",
            fontName="Times-Roman",
            fontSize=10,
            leading=14,
            textColor=colors.HexColor("#E8EEF6"),
            alignment=TA_CENTER,
        )
    )
    s.add(
        ParagraphStyle(
            "H1",
            fontName="Times-Bold",
            fontSize=14,
            leading=18,
            textColor=NAVY,
            spaceBefore=14,
            spaceAfter=8,
            borderPadding=3,
        )
    )
    s.add(
        ParagraphStyle(
            "H2",
            fontName="Times-Bold",
            fontSize=12,
            leading=15,
            textColor=TEAL,
            spaceBefore=11,
            spaceAfter=6,
        )
    )
    s.add(
        ParagraphStyle(
            "H3",
            fontName="Times-Bold",
            fontSize=11,
            leading=14,
            textColor=NAVY,
            spaceBefore=8,
            spaceAfter=4,
        )
    )
    s.add(
        ParagraphStyle(
            "Body",
            fontName="Times-Roman",
            fontSize=10,
            leading=13.5,
            alignment=TA_JUSTIFY,
            spaceAfter=6,
        )
    )
    s.add(
        ParagraphStyle(
            "BodyLeft",
            fontName="Times-Roman",
            fontSize=10,
            leading=13.5,
            alignment=TA_LEFT,
            spaceAfter=6,
        )
    )
    s.add(
        ParagraphStyle(
            "Note",
            fontName="Times-Italic",
            fontSize=9.5,
            leading=12.5,
            textColor=colors.HexColor("#334155"),
            alignment=TA_JUSTIFY,
            leftIndent=8,
            rightIndent=8,
            spaceBefore=4,
            spaceAfter=8,
        )
    )
    s.add(
        ParagraphStyle(
            "Caption",
            fontName="Times-Italic",
            fontSize=8.5,
            leading=11,
            textColor=colors.HexColor("#475569"),
            alignment=TA_CENTER,
            spaceBefore=2,
            spaceAfter=10,
        )
    )
    s.add(
        ParagraphStyle(
            "TOC",
            fontName="Times-Roman",
            fontSize=10.5,
            leading=16,
            textColor=NAVY,
        )
    )
    s.add(
        ParagraphStyle(
            "CodeBlock",
            fontName="Courier",
            fontSize=7.6,
            leading=10.2,
            textColor=NAVY,
            backColor=LT,
            leftIndent=4,
            rightIndent=4,
            spaceBefore=4,
            spaceAfter=8,
        )
    )
    s.add(
        ParagraphStyle(
            "Cell",
            fontName="Times-Roman",
            fontSize=8,
            leading=10.5,
            textColor=NAVY,
        )
    )
    s.add(
        ParagraphStyle(
            "CellH",
            fontName="Times-Bold",
            fontSize=8,
            leading=10.5,
            textColor=colors.white,
        )
    )
    s.add(
        ParagraphStyle(
            "Footer",
            fontName="Times-Roman",
            fontSize=8,
            textColor=colors.HexColor("#64748B"),
        )
    )
    s.add(
        ParagraphStyle(
            "BulletBody",
            fontName="Times-Roman",
            fontSize=10,
            leading=13.2,
            alignment=TA_LEFT,
        )
    )
    return s


S = styles()


def p(text, style="Body"):
    return Paragraph(text, S[style])


def h1(text):
    return Paragraph(text, S["H1"])


def h2(text):
    return Paragraph(text, S["H2"])


def h3(text):
    return Paragraph(text, S["H3"])


def bullets(items):
    flow = []
    for it in items:
        flow.append(
            ListItem(Paragraph(it, S["BulletBody"]), leftIndent=12, bulletColor=TEAL)
        )
    return ListFlowable(
        flow,
        bulletType="bullet",
        start="•",
        leftIndent=18,
        bulletFontName="Times-Roman",
        bulletFontSize=10,
        spaceAfter=8,
    )


def numbered(items):
    flow = []
    for it in items:
        flow.append(
            ListItem(Paragraph(it, S["BulletBody"]), leftIndent=14, bulletColor=NAVY)
        )
    return ListFlowable(
        flow,
        bulletType="1",
        leftIndent=22,
        bulletFontName="Times-Bold",
        bulletFontSize=10,
        spaceAfter=8,
    )


def tbl(headers, rows, col_widths=None):
    head = [Paragraph(h, S["CellH"]) for h in headers]
    data = [head]
    for r in rows:
        data.append([Paragraph(str(c), S["Cell"]) for c in r])
    t = Table(data, colWidths=col_widths, repeatRows=1)
    cmd = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 3.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3.5),
        ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#94A3B8")),
        ("FONTNAME", (0, 0), (-1, 0), "Times-Bold"),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            cmd.append(("BACKGROUND", (0, i), (-1, i), ROW))
        else:
            cmd.append(("BACKGROUND", (0, i), (-1, i), colors.white))
    t.setStyle(TableStyle(cmd))
    return t


def code(text):
    return Preformatted(text.strip("\n"), S["CodeBlock"])


def header_footer(canvas, doc):
    canvas.saveState()
    w, h = A4
    if doc.page == 1:
        canvas.restoreState()
        return
    canvas.setFillColor(NAVY)
    canvas.rect(0, h - 14 * mm, w, 14 * mm, fill=1, stroke=0)
    canvas.setFillColor(GOLD)
    canvas.rect(0, h - 14.8 * mm, w, 1.2 * mm, fill=1, stroke=0)
    canvas.setFillColor(colors.white)
    canvas.setFont("Times-Bold", 8)
    canvas.drawString(
        16 * mm,
        h - 9 * mm,
        "SentinelOne Host-Level Performance Test Plan — Windows Server 2016–2025",
    )
    canvas.setFont("Times-Roman", 8)
    canvas.drawRightString(w - 16 * mm, h - 9 * mm, DOC_ID)
    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, w, 12 * mm, fill=1, stroke=0)
    canvas.setFillColor(GOLD)
    canvas.rect(0, 12 * mm, w, 0.8 * mm, fill=1, stroke=0)
    canvas.setFillColor(colors.white)
    canvas.setFont("Times-Roman", 8)
    canvas.drawString(16 * mm, 5 * mm, "INTERNAL USE  |  Performance Engineering & Cybersecurity Architecture")
    canvas.drawRightString(w - 16 * mm, 5 * mm, f"Page {doc.page}")
    canvas.restoreState()


def cover_page(canvas, doc):
    canvas.saveState()
    w, h = A4
    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, w, h, fill=1, stroke=0)
    canvas.setFillColor(TEAL)
    canvas.rect(0, 0, 8 * mm, h, fill=1, stroke=0)
    canvas.setFillColor(GOLD)
    canvas.rect(8 * mm, 0, 1.4 * mm, h, fill=1, stroke=0)
    canvas.setFillColor(GOLD)
    canvas.rect(24 * mm, h - 42 * mm, w - 48 * mm, 0.6 * mm, fill=1, stroke=0)
    canvas.restoreState()
    header_footer(canvas, doc)


def build():
    story = []
    story += [
        Spacer(1, 52 * mm),
        p("FORMAL TEST PLAN  ·  REVISION 1.0", "CoverKicker"),
        p(
            "Host-Level Performance Impact Assessment of the<br/>SentinelOne Singularity Windows Agent",
            "CoverTitle",
        ),
        p(
            "Windows Server 2016, 2019, 2022, and 2025<br/>A–B–A Isolated Methodology · Kernel, Minifilter, and User-Mode Telemetry",
            "CoverSub",
        ),
        Spacer(1, 10 * mm),
        p(f"Document ID: {DOC_ID}", "CoverMeta"),
        p("Classification: Internal — Performance Engineering / Security Architecture", "CoverMeta"),
        p(f"Effective Date: {DOC_DATE.isoformat()}  ·  Status: Approved for Lab Execution (Draft for Stakeholder Review)", "CoverMeta"),
        p("Prepared for: Infrastructure Performance Engineering, Endpoint Security Architecture, and Platform Operations", "CoverMeta"),
        p("Product under test: SentinelOne Singularity Endpoint (Windows Server agent, 64-bit Group 1 installer)", "CoverMeta"),
        PageBreak(),
    ]

    story += [
        h1("Contents"),
        p(
            "0. Document Control, Scope Boundaries, and Explicit Assumptions<br/>"
            "1. Executive Summary and Objectives<br/>"
            "2. Environment and Architecture<br/>"
            "3. Instrumentation: Metrics, Counters, and Kernel Traces<br/>"
            "4. Methodology: Isolated A–B–A Procedure<br/>"
            "5. Engineering SLOs, Gates, and Severity<br/>"
            "6. Test Case Catalog — Core (TC-01 to TC-04)<br/>"
            "7. Extended Test Cases (TC-05 to TC-24)<br/>"
            "8. Experiment Matrix and Execution Calendar Logic<br/>"
            "9. Automation and Telemetry Pipeline<br/>"
            "10. Data Analysis, Attribution, and Reporting<br/>"
            "11. Risks, Ethics, and Interference Management<br/>"
            "12. Roles and RACI<br/>"
            "13. Entry, Exit, and Deliverables<br/>"
            "14. Regression Pack (every SentinelOne GA)<br/>"
            "15. Open Questions Requiring Stakeholder Clarification<br/>"
            "16–20. Appendices A–E (sentinelctl, WPR, Prometheus, change log, glossary)",
            "TOC",
        ),
        PageBreak(),
    ]

    # 0 Document control
    story += [
        h1("0. Document Control, Scope Boundaries, and Explicit Assumptions"),
        h2("0.1 Document control"),
    ]
    story.append(
        tbl(
            ["Field", "Value"],
            [
                ["Document ID", DOC_ID],
                ["Title", "Host-Level Performance Impact Assessment of SentinelOne on Windows Server 2016–2025"],
                ["Revision", "1.0"],
                ["Date", DOC_DATE.isoformat()],
                ["Authors / roles", "Senior Performance Engineer; Cybersecurity Architect; Windows Platform Engineer (lab)"],
                ["Primary audience", "CISO architecture board, server platform owners, capacity planners, SOC engineering"],
                ["Related artifacts", "Lab runbook (PowerShell), Perfmon XML templates, Grafana dashboards, results workbook"],
                ["Retention", "Retain raw ETL/BLG/CSV for ≥ 24 months or per corporate evidence policy"],
            ],
            [45 * mm, 132 * mm],
        )
    )
    story.append(p("Table 0-1. Document control block.", "Caption"))

    story += [
        h2("0.2 What this plan measures — and what it does not"),
        p(
            "This plan quantifies <b>host-level resource overhead and kernel-path latency</b> attributable to the SentinelOne (S1) Windows agent while the operating system executes sustained, heavy, and adversarial-shaped workloads. "
            "Primary dependent variables are CPU (user + privileged + DPC/ISR), RAM (working set, private bytes, commit, pool), Disk I/O (IOPS, throughput, latency, minifilter completion delay), and network stack cost (WFP/NDIS, TCP, SMB). "
            "The independent variable is agent presence and policy configuration on otherwise identical VM templates."
        ),
        p(
            "This plan is <b>not</b> a detection-efficacy, MITRE ATT&amp;CK coverage, or red-team bypass study. Synthetic generators must not drop real malware, exploit kits, or weaponized payloads. "
            "Where Static AI / Behavioral AI engines must be exercised, use vendor-permitted benign PE mutation, EICAR-class markers (if policy allows), unsigned test binaries built in-lab, and high-churn file/process patterns. "
            "Mitigation actions (kill, quarantine, rollback) are measured only as <i>performance side-effects</i> of false-positive or intentional test detections, not as security quality scores."
        ),
        h2("0.3 Assumptions applied because certain facts were not specified"),
        p(
            "The request did not pin several laboratory parameters. The following assumptions are <b>explicitly adopted</b> so the plan is executable. Any assumption that is wrong for the intended environment must be corrected before first execution; they are restated as open questions in Section 15."
        ),
        bullets(
            [
                "<b>Product SKU:</b> SentinelOne Singularity Complete (or equivalent Server SKU) with Windows 64-bit Group 1 installer. Cloud Workload Security / CWPP container sensors are <i>out of scope</i> unless stakeholders expand TC-19.",
                "<b>Agent version:</b> One GA build pinned for the campaign (example placeholder: 25.x Windows Server). Record exact file version, build, and console package ID. Do not mix N and N-1 on the same OS cell of the matrix.",
                "<b>Policy:</b> Production-representative <b>Protect</b> for Malicious + configured handling for Suspicious; <b>Deep Visibility (EDR) ON</b>; Anti-Tamper ON; Storyline / forensic snapshot features at site default. Detect-only and Deep Visibility OFF are additional factors (TC-12, TC-13), not the primary production proxy.",
                "<b>Competing AV:</b> Microsoft Defender Antivirus remains installed (Windows Server default) but is placed in a documented state: either passive/EDR-only per Microsoft + S1 interoperability guidance, or fully disabled via Group Policy in the isolated lab. Coexistence is a separate factor (TC-20).",
                "<b>Hypervisor:</b> VMware vSphere 8+ or Microsoft Hyper-V on Windows Server 2022/2025. CPU and memory <b>reserved at 100%</b> of VM size; no overcommit; independent datastores or equivalent IOPS isolation; paravirtual SCSI (PVSCSI / VMware PVSCSI or Hyper-V SCSI).",
                "<b>VM size (reference):</b> 8 vCPU, 32 GiB RAM, 200 GiB OS VMDK/VHDX on NVMe-backed storage, plus a 200 GiB data volume for DiskSpd. Scale-up (16 vCPU / 64 GiB) is a sensitivity cell, not the default.",
                "<b>Network:</b> 10/25 GbE virtual NIC, VMXNET3 or Synthetic NIC, no NSX/microsegmentation in the data path of the test vSwitch except as TC-04b. Console connectivity via a dedicated management VLAN with measured RTT.",
                "<b>Identity:</b> Domain-joined to an isolated lab AD; time sync via NTP/PTP; no production GPOs.",
                "<b>Windows Server 2025:</b> Treated as in-scope. Before kickoff, confirm the pinned S1 agent is on the vendor OS support matrix for Server 2025 (Desktop Experience and Server Core as required).",
                "<b>Success thresholds:</b> No contractual S1 SLA was provided. This plan therefore defines <b>engineering SLOs</b> (Section 5) that stakeholders may tighten. They are gates for “acceptable overhead,” not vendor marketing claims.",
                "<b>Isolation:</b> A–B–A is performed on the <i>same VM</i> (snapshot revert) rather than parallel twins, to eliminate host-level noisy-neighbor variance. Parallel twins are permitted only if the hypervisor can guarantee identical pCPU mapping and storage QoS.",
            ]
        ),
        h2("0.4 Safety, change control, and anti-tamper"),
        p(
            "Anti-Tamper prevents local service stop, driver unload, and unauthorized uninstall. All agent state transitions (install, upgrade, policy, uninstall) require a console-generated passphrase and a change ticket. "
            "Do not use Driver Verifier against SentinelMonitor.sys on any host that must remain stable; if used at all, confine it to a disposable clone tagged TC-21-DV and accept bugcheck risk. "
            "Full Disk Scan, rollback (VSS), and network quarantine have blast radius: execute only in the isolated lab site."
        ),
    ]

    story += [
        h1("1. Executive Summary and Objectives"),
        h2("1.1 Executive summary"),
        p(
            "Endpoint detection and response agents that operate through file-system minifilters, process-notify callbacks, object callbacks, registry callbacks, and Windows Filtering Platform (WFP) callouts impose a <b>tax on every I/O, create, and connect</b> that the kernel would otherwise complete with a shorter code path. "
            "On Windows Server, that tax is paid during the exact conditions operators care about: boot storms, patch nights, backup windows, SQL checkpoints, IIS/TLS termination, file-server metadata storms, and CI/CD process-create bursts. "
            "Idle CPU of a few percent is not a sufficient acceptance test. This campaign forces the SentinelOne Windows agent through idle, volatility, interrupt, and network extremes, then isolates the delta with a statistically controlled A–B–A design."
        ),
        p(
            "The agent under evaluation is a multi-process Windows service plus kernel driver. Typical user-mode processes include <b>SentinelAgent.exe</b> (policy, behavioral engines, console transport), <b>SentinelServiceHost.exe</b> (worker host), and <b>SentinelStaticEngine.exe</b> (on-write / pre-execution Static AI). "
            "Kernel instrumentation is centered on <b>SentinelMonitor.sys</b> (minifilter and related callbacks). Deep Visibility, if enabled, adds user-mode serialization and network upload of Storyline telemetry, which can shift the bottleneck from CPU to disk (local database under ProgramData\\Sentinel) and egress bandwidth."
        ),
        p(
            "Outcomes of this plan are: (1) per-OS, per-policy overhead tables with confidence intervals; (2) kernel latency distributions (minifilter microseconds per MB, DPC/ISR, context switches); (3) identification of pathological interactions (Defender coexistence, exclusions, Full Disk Scan, database growth); (4) a go/no-go recommendation against the SLOs in Section 5; (5) a reusable automation pack for regression on each agent upgrade."
        ),
        h2("1.2 Quantified objectives"),
        p("For each OS (2016, 2019, 2022, 2025) × each policy cell, compute the following after A–B–A (see Section 4). All deltas are B − mean(A1, A2) unless A2 fails the stability gate."),
    ]
    story.append(
        tbl(
            ["ID", "Objective", "Primary metrics", "Reporting form"],
            [
                [
                    "O-CPU",
                    "Quantify CPU overhead under idle and under each stressor",
                    "\\Processor(_Total)\\% Processor Time; % Privileged Time; % User Time; % DPC Time; % Interrupt Time; per-process % Processor Time for S1 PIDs; Processor Queue Length",
                    "Mean, p95, p99, max; delta pp (percentage points) and relative %",
                ],
                [
                    "O-RAM",
                    "Quantify RAM and commit overhead, including leaks over soak",
                    "Working Set, Private Bytes, Virtual Bytes for S1 processes; \\Memory\\Available MBytes; Committed Bytes; Pool Nonpaged/Paged; Cache Bytes; Pages/sec",
                    "MiB delta at T+15m and T+24h; slope (MiB/h) for leak detection",
                ],
                [
                    "O-DISK",
                    "Quantify disk I/O tax on OS and data volumes",
                    "Disk Transfers/sec, Bytes/sec, Avg. Disk sec/Read|Write, Avg. Disk Queue Length, Split IO/sec; DiskSpd IOPS/latency; minifilter completion delay",
                    "IOPS and MB/s delta; added µs/IO; µs per MB of minifilter delay",
                ],
                [
                    "O-KLAT",
                    "Quantify kernel-level latency beyond disk",
                    "Minifilter ETW (WPR); context switches/sec; system calls/sec; DPC/ISR µs; process create/exit latency; registry set-value latency",
                    "p50/p95/p99 of completion time; µs/MB; CreateProcess wall time",
                ],
                [
                    "O-NET",
                    "Quantify network inspection and throughput degradation",
                    "TCP throughput (NTttcp/iPerf3), retransmits, TCP RSC, WFP drops; SMB copy time; TLS handshake rate if applicable",
                    "Gb/s delta; added RTT; CPU per Gb/s",
                ],
                [
                    "O-APP",
                    "Quantify application-visible SLO impact",
                    "SQL TPC-C-like or HammerDB NOPM; IIS requests/sec; robocopy metadata ops; AD bind latency (if DC cell used)",
                    "Relative % change vs A-phase; p95 latency",
                ],
                [
                    "O-STA",
                    "Quantify agent self-stability",
                    "Handle count, thread count, ProgramData\\Sentinel size, log volume, console online time, unexpected mitigations",
                    "Pass/fail vs leak and disk-growth gates",
                ],
            ],
            [18 * mm, 38 * mm, 72 * mm, 49 * mm],
        )
    )
    story.append(p("Table 1-1. Quantified campaign objectives.", "Caption"))

    story += [
        h2("1.3 Hypotheses (pre-registered)"),
        numbered(
            [
                "H1 — Idle overhead is dominated by user-mode polling, Deep Visibility timers, and small minifilter metadata I/O, not by DiskSpd-class data path cost.",
                "H2 — Extreme file create/close/rename churn produces the largest minifilter delay per MB because IRP_MJ_CREATE / CLEANUP / SET_INFORMATION dominate over IRP_MJ_READ/WRITE of large sequential files.",
                "H3 — Process-create storms increase privileged CPU and context switches disproportionately versus CPU of SentinelAgent.exe alone, because kernel callbacks and Static AI on new images are serialized through the driver and static engine.",
                "H4 — Large sequential network transfers show modest throughput loss unless WFP inspection or Deep Visibility connection events are on the hot path; CPU per Gb/s will rise even if throughput is similar.",
                "H5 — Deep Visibility ON increases disk writes to the local agent database and RAM of SentinelAgent.exe versus Deep Visibility OFF, especially under process and network storms.",
                "H6 — A second A-phase (agent removed or snapshot-reverted) returns metrics to within the stability band of A1; residual elevation indicates incomplete uninstall, Defender state drift, or hypervisor cache effects.",
            ]
        ),
        h2("1.4 Decision use"),
        p(
            "Results feed: (a) hypervisor oversubscription policy for S1-protected clusters; (b) exclusion design for SQL, backup, and hypervisor data paths; (c) whether Deep Visibility can remain ON for file servers and domain controllers; "
            "(d) agent upgrade acceptance (repeat the abbreviated suite on each GA); (e) capacity model: additional vCPU/RAM required per 100 protected guests."
        ),
    ]

    story += [
        h1("2. Environment and Architecture"),
        h2("2.1 Design principle: identical templates, isolated cells"),
        p(
            "Four gold templates are built — one per OS version — from the same hardware class, firmware, virtual hardware version, vCPU topology, memory reservation, disk controller, and NIC type. "
            "Templates are generalized (Sysprep) then cloned. Each clone is a <b>cell</b> in the experiment matrix. Cells never share a datastore with production, never share a pCPU oversubscribed host, and never receive opportunistic live migration during a run."
        ),
        h2("2.2 Logical architecture"),
        p(
            "The laboratory is partitioned into: (1) <b>System Under Test (SUT)</b> VMs — one active SUT per run; (2) <b>Load Generator (LG)</b> VMs — Windows Server 2022, no S1 agent, used for NTttcp/iPerf3/SMB clients so the SUT is not generating its own client CPU; "
            "(3) <b>Telemetry plane</b> — Windows Admin Center / local Perfmon, windows_exporter, optional Splunk Universal Forwarder, and a Linux collector (Prometheus + Grafana) on a dedicated VLAN; "
            "(4) <b>SentinelOne Management Console</b> — a dedicated test site/account, not production, with a unique site token; (5) <b>Time and identity</b> — lab AD + NTP; (6) <b>Jump / automation controller</b> — Ansible/WinRM or PowerShell Remoting over the management VLAN."
        ),
        p(
            "Traffic policy: SUT may reach the S1 console (required for policy and Deep Visibility upload), Windows Update (pinned or WSUS in lab), and LG. All other egress is denied. Record console RTT and whether the agent is operating with full cloud intelligence versus deferred upload; both states must be labeled on the run."
        ),
        h2("2.3 Gold image specification (all OS versions)"),
    ]
    story.append(
        tbl(
            ["Layer", "Specification (lock before imaging)"],
            [
                ["Compute", "8 vCPU, 1 socket, 8 cores (or 2×4 if NUMA testing is in-scope). CPU Hot-Add OFF. HV exposed: ON (Windows). CPU reservation = 8 × host GHz equivalent; shares Normal."],
                ["Memory", "32 GiB RAM, 100% reserved, ballooning disabled (VMware: disable balloon where policy allows; Hyper-V: Dynamic Memory OFF)."],
                ["Firmware", "UEFI, Secure Boot ON (if S1 and OS support in this lab), TPM 2.0 virtual if BitLocker is a factor; default cell: BitLocker OFF to reduce cryptographic I/O confounders."],
                ["OS disk", "200 GiB, PVSCSI/SCSI, lazy-zeroed thick or Hyper-V fixed VHDX, NTFS 4K or 64K as per role (see 2.6). Pagefile system-managed on OS volume unless SQL cell."],
                ["Data disk", "200 GiB dedicated to DiskSpd and file-churn trees. Separate VMDK/VHDX. No S1 ProgramData on this volume."],
                ["Network", "VMXNET3 / Synthetic, 1× data, 1× mgmt. RSS enabled. VMQ/SR-IOV: document ON/OFF; keep constant across A–B–A."],
                ["Storage path", "Physical NVMe or all-flash array LUN with QoS floor ≥ 50k IOPS / 2 GB/s so the array is not the bottleneck. Disable storage DRS / SIOC interference during runs."],
                ["Windows", "Latest CU at template freeze. .NET 4.8 / 4.8.1 as shipped. OpenSSH optional. WinRM HTTPS. PowerShell 5.1 (7.x optional). Windows Performance Toolkit from matching ADK."],
                ["Roles (base cell)", "No extra roles. Role-specific cells (IIS, SQL, File Services, AD DS) are clones with roles added via unattended scripts after sysprep specialize."],
                ["Time", "w32tm / NTP. Max allowed offset 50 ms before abort."],
                ["Defender", "State captured with Get-MpComputerStatus. Lab default: real-time protection OFF if S1 is the AV engine, per interoperability note; Attack Surface Reduction rules documented."],
                ["S1 folders", "Do not pre-create exclusions in the gold image. Exclusions are applied only in TC-14 via console policy."],
            ],
            [38 * mm, 139 * mm],
        )
    )
    story.append(p("Table 2-1. Gold template lock-list.", "Caption"))

    story += [
        h2("2.4 OS version matrix"),
    ]
    story.append(
        tbl(
            ["OS", "Edition (lab default)", "Notes that affect performance testing"],
            [
                ["Windows Server 2016", "Datacenter, Desktop Experience", "Older kernel/minifilter manager; confirm KB4093119 (S1 log-retention behavior). Older TCP stack vs 2022/2025. PowerShell/WinRM quirks. May need older ADK WPT."],
                ["Windows Server 2019", "Datacenter, Desktop Experience", "Confirm KB5005625 as applicable. Defender ATP features differ. SMB 3.1.1 baseline."],
                ["Windows Server 2022", "Datacenter, Desktop Experience", "Confirm KB5005619. Secured-core optional — if enabled, treat as a factor (HVCI/Memory Integrity increases kernel cost independently of S1)."],
                ["Windows Server 2025", "Datacenter, Desktop Experience", "Confirm S1 GA support on freeze date. New scheduler/storage/SMB behaviors; do not assume 2022 deltas transfer. Repeat minifilter altitude checks."],
            ],
            [38 * mm, 42 * mm, 97 * mm],
        )
    )
    story.append(p("Table 2-2. OS cells. Server Core is an optional parallel matrix (TC-22) because GUI idle cost and Defender/UI components differ.", "Caption"))

    story += [
        h2("2.5 SentinelOne component map (Windows)"),
        p(
            "Record exact image names and driver altitudes on each OS after install. Names can vary slightly by agent train; the table is the expected production map."
        ),
    ]
    story.append(
        tbl(
            ["Component", "Type", "Performance relevance"],
            [
                ["SentinelAgent.exe", "User-mode service", "Primary RAM/CPU; policy; Behavioral AI; console comms; local DB"],
                ["SentinelServiceHost.exe", "User-mode", "Ancillary workers; watch for extra instances under load"],
                ["SentinelStaticEngine.exe", "User-mode", "On-write / on-execute Static AI — hot during PE create and file write storms"],
                ["SentinelHelperService / related", "User-mode (if present)", "Install/upgrade helpers; should be quiet at steady state"],
                ["SentinelUI.exe", "User session", "Usually negligible on Server; still capture if session 1 is logged on"],
                ["SentinelRemediation.exe", "Ephemeral", "Appears during kill/quarantine/rollback — spikes I/O and VSS"],
                ["SentinelMonitor.sys", "Kernel minifilter + callbacks", "IRP completion delay; CREATE storms; FS volatility"],
                ["InProcessClient64.dll", "Injected / in-process client (as deployed)", "Potential per-process tax; measure via Agent Activity Analyzer if CPU concentrates in apps"],
                ["C:\\ProgramData\\Sentinel", "On-disk state", "Database and logs; RAM inflation has been correlated in the field with disk pressure and large internal DB"],
                ["C:\\Program Files\\SentinelOne\\...", "Install tree", "Driver and binaries; Authenticode-signed"],
            ],
            [48 * mm, 38 * mm, 91 * mm],
        )
    )
    story.append(p("Table 2-3. S1 component map for telemetry attribution.", "Caption"))

    story += [
        h2("2.6 Role-specific overlay cells (optional but recommended)"),
        p(
            "The base cell is a clean OS. Production servers are not clean. After the base matrix, clone templates and add one role per overlay so interactions are attributable:"
        ),
        bullets(
            [
                "<b>File server:</b> File Services + SMB share on data volume, 4K NTFS. Metadata-heavy.",
                "<b>IIS/TLS:</b> IIS + a static+dynamic app pool, TLS 1.2/1.3, 10k concurrent connections from LG.",
                "<b>SQL:</b> SQL Server Developer/Eval, separate data/log VMDKs, 64K NTFS on data, Instant File Initialization ON, pagefile sized, Lock Pages in Memory as per DBA standard. S1 on-write of MDF/LDF is a classic minifilter hazard.",
                "<b>AD DS:</b> Single-lab DC (never a production DC). LSASS and NTDS.dit I/O.",
                "<b>Hyper-V nested (caution):</b> Only if the business runs S1 on Hyper-V hosts. Nested virt plus S1 on vmwp.exe/VHDX is a known conflict class; requires vendor exclusion guidance.",
            ]
        ),
        h2("2.7 Snapshot and revert architecture for A–B–A"),
        numbered(
            [
                "Freeze gold image. Take hypervisor snapshot S0 (post-sysprep specialize, domain join, tools installed, no S1).",
                "A1: boot from S0, soak, run suite, export telemetry. Do not patch mid-run.",
                "B: install S1 from console/site token, reboot if required, wait until console shows Healthy/Online and policy applied (document the wait, default 15 minutes). Snapshot S1-B after healthy.",
                "B-run: execute identical suite. Optionally snapshot S1-B-end for forensics.",
                "A2: revert to S0 (not uninstall, unless uninstall-path is itself a test). Confirm S1 processes/drivers absent. Repeat suite.",
                "Never revert to a dirty snapshot. If Windows Update sneaks in, invalidate the cell.",
            ]
        ),
        h2("2.8 Hypervisor host requirements"),
        p(
            "Place all SUTs for a given OS version on the same physical host for a campaign week, or pin via DRS rules. Disable power-management C-states in BIOS if latency tests show jitter. "
            "Collect host-level CPU ready time (%RDY / Hyper-V CPU wait). If CPU ready &gt; 5% during a run, the run is invalid — the delta would be contaminated by scheduling delay not caused by S1."
        ),
    ]

    story += [
        h1("3. Instrumentation: Metrics, Counters, and Kernel Traces"),
        h2("3.1 Principle of dual instrumentation"),
        p(
            "Coarse telemetry (Perfmon / windows_exporter, 1-second or 5-second grain) answers capacity questions. Fine telemetry (WPR/ETW, xperf, Windows Performance Analyzer) answers <b>why</b> and produces minifilter microseconds. "
            "Never run heavy ETW during the official DiskSpd throughput number except in a dedicated trace replicate: ETW itself is a probe effect. Official numbers come from Perfmon + application timers; ETW is a paired replicate at the same load."
        ),
        h2("3.2 Perfmon / PDH counter catalog (mandatory)"),
        p("Logman binary circular logs, 1-second sample for 15-minute tests; 5-second for 24-hour soak. Relog to CSV/BLG. Align clocks."),
    ]
    story.append(
        tbl(
            ["Object", "Counters (non-exhaustive; instantiate all)"],
            [
                ["Processor", "% Processor Time, % Privileged Time, % User Time, % DPC Time, % Interrupt Time, Interrupts/sec, DPCs Queued/sec (and Processor Information per CPU)"],
                ["System", "Processor Queue Length, Context Switches/sec, System Calls/sec, File Read/Write/Control Ops/sec, Processes, Threads"],
                ["Memory", "Available MBytes, Committed Bytes, Commit Limit, Pool Paged/Nonpaged Bytes, Cache Bytes, Pages/sec, Page Faults/sec, Transition Faults/sec, Page Reads/sec"],
                ["Process", "ID Process, % Processor Time, Working Set, Working Set - Private, Private Bytes, Virtual Bytes, Thread Count, Handle Count, IO Data/Read/Write Bytes/sec, IO Data Operations/sec — instances: SentinelAgent, SentinelStaticEngine, SentinelServiceHost, DiskSpd, sqlservr, etc., and _Total"],
                ["Process", "Also capture lsass, MsMpEng (if Defender live), System (PID 4) — kernel I/O often lands in System"],
                ["PhysicalDisk / LogicalDisk", "Disk Transfers/sec, Disk Reads/sec, Disk Writes/sec, Disk Bytes/sec, Avg. Disk sec/Read, Avg. Disk sec/Write, Avg. Disk Queue Length, Current Disk Queue Length, Split IO/sec, % Idle Time — _Total, OS, Data"],
                ["Paging File", "% Usage"],
                ["TCPv4 / TCPv6", "Connections Established, Segments/sec, Segments Retransmitted/sec, Connection Failures"],
                ["Network Interface", "Bytes Total/sec, Packets/sec, Packets Received/Outbound Discarded, Output Queue Length — per NIC"],
                ["SMB Server Shares (role cells)", "Read/Write Bytes/sec, Requests/sec, Average sec/Request"],
                ["HTTP Service (IIS cell)", "Request Execution Time, Current Connections, URI Requests/sec"],
                ["Filter Manager (if available)", "Any published minifilter counters on that OS build — confirm with typeperf -q"],
                ["Search / Defender", "If Defender remains active: Microsoft Defender Antivirus counters to avoid mis-attributing CPU"],
            ],
            [42 * mm, 135 * mm],
        )
    )
    story.append(p("Table 3-1. Mandatory Perfmon catalog.", "Caption"))

    story += [
        h2("3.3 Logman example"),
        code(
            r"""logman create counter S1Perf -f bincirc -max 2048 -si 00:00:01 ^
  -c "\Processor(*)\*" "\Processor Information(*)\*" "\Memory\*" ^
     "\System\*" "\Process(*)\*" "\PhysicalDisk(*)\*" "\LogicalDisk(*)\*" ^
     "\Network Interface(*)\*" "\TCPv4\*" "\TCPv6\*" ^
     "\Paging File(*)\*" ^
  -o C:\PerfLogs\S1Perf.blg
logman start S1Perf
REM ... workload ...
logman stop S1Perf"""
        ),
        h2("3.4 Kernel and minifilter traces (WPR / Windows Performance Toolkit)"),
        p(
            "Install Windows ADK Performance Toolkit matching the OS generation as closely as practical. Use WPR (UI or wpr.exe) with: First-level triage; CPU; Disk I/O; File I/O; Registry; Networking (for TC-04); <b>Minifilter I/O activity</b>. "
            "For boot measurements (TC-08), WPR Boot scenario, Light, File mode, 2–3 iterations, Autologon with a lab admin. Compare Total IO Bytes versus minifilter delay in microseconds; report <b>µs of minifilter delay per MB of I/O</b> for A vs B."
        ),
        p(
            "In Windows Performance Analyzer: Graph Explorer → File I/O → Minifilter delays; attribute to SentinelMonitor (or the altitude string recorded via fltmc). "
            "Also capture CPU Usage (Precise) for DPC/ISR stacks. If minifilter graphs are empty, the WPR profile lacked the minifilter provider — treat as a failed trace, not zero delay."
        ),
        h2("3.5 fltmc, driver, and callback inventory"),
        code(
            r"""fltmc
fltmc instances
driverquery /v
Get-AuthenticodeSignature "C:\Program Files\SentinelOne\*\SentinelMonitor.sys"
sc.exe qc SentinelAgent
Get-CimInstance Win32_SystemDriver | Where-Object { $_.PathName -match 'Sentinel' }"""
        ),
        p(
            "Record minifilter altitude. Altitude determines stack position relative to Defender, backup, encryption, and Dedup filters. A change in altitude across OS versions is a finding.",
            "Note",
        ),
        h2("3.6 SentinelOne-native telemetry"),
        bullets(
            [
                "<b>sentinelctl status / version</b> (install directory) — protection state, console URL, pending reboot.",
                "<b>Agent Activity Analyzer</b> (console / Windows exclusion troubleshooting) — fraction of agent time spent per process; 5-minute agent CPU avg/max. Use when user-mode CPU is high but kernel traces are quiet.",
                "<b>Console device timeline</b> — Full Disk Scan, updates, mitigations, connectivity gaps. Align to Perfmon with UTC.",
                "<b>Deep Visibility event rate</b> — if the console or API exposes ingest volume per endpoint, record it; it explains disk/network tax.",
            ]
        ),
        h2("3.7 windows_exporter + Prometheus + Grafana"),
        p(
            "Deploy windows_exporter on SUT and LG with collectors: cpu, cpu_info, cs, logical_disk, net, os, process (include Sentinel*), system, tcp, memory, cache, logon, service. "
            "Scrape interval 5s (1s only for 15-minute tests if cardinality is acceptable). Prometheus recording rules: rate of context switches, disk latency histograms if using extra exporters, process RSS. "
            "Grafana dashboards: one per TC, with A1/B/A2 overlays using a run_id label injected via a textfile collector (run_id, phase, os, agent_version, policy_hash)."
        ),
        h2("3.8 Splunk (or equivalent SIEM) pipeline"),
        p(
            "Optional but recommended for enterprise evidence: Splunk Universal Forwarder ingesting (1) Windows Security + System + Application; (2) Microsoft-Windows-Winlogon, Kernel-File, Kernel-Process if subscribed (volume warning); "
            "(3) S1 agent logs under ProgramData\\Sentinel\\logs (size-cap them); (4) exported Perfmon CSV via a monitored spool. Index with run_id. Do not enable verbose kernel ETW into Splunk during official timed tests."
        ),
        h2("3.9 Time alignment and run_id"),
        p(
            "Every artifact (BLG, ETL, DiskSpd XML, Grafana, console screenshot metadata) carries run_id = {os}-{yyyyMMddTHHmmssZ}-{phase}-{tc}-{rep}. NTP offset is logged at start/stop. Discard runs with clock step."
        ),
    ]

    story += [
        h1("4. Methodology: Isolated A–B–A Procedure"),
        h2("4.1 Why A–B–A, not A–B"),
        p(
            "A–B (baseline then agent) cannot distinguish agent overhead from time drift: Windows Update, Defender definition load, NTFS fragmentation, hypervisor cache warming, or a noisy neighbor that appears at 14:00. "
            "A–B–A applies the agent in the middle phase and <b>returns to the unmanaged snapshot</b>. If A2 matches A1 within the stability gate, the B delta is causal. If A2 does not match A1, the cell is contaminated; investigate before quoting numbers."
        ),
        h2("4.2 Phase definitions"),
    ]
    story.append(
        tbl(
            ["Phase", "Agent state", "Purpose", "Duration (typical)"],
            [
                ["A1 — Unmanaged baseline", "No S1 binaries/drivers; Defender state = lab default", "Establish idle and loaded baselines", "Idle 30m + each TC 15–30m + cooldown 10m"],
                ["B — Agentized", "S1 installed, Anti-Tamper ON, policy applied, Healthy", "Measure overhead", "Identical scripts and durations as A1"],
                ["A2 — Unmanaged re-baseline", "Revert to S0 (preferred) or authorized uninstall + reboot", "Prove reversibility and absence of hysteresis", "Identical to A1"],
                ["B′ — optional policy variants", "Same install, different policy (Detect, DV off, exclusions)", "Attribute overhead to features, not merely 'agent present'", "Subset of TCs"],
            ],
            [38 * mm, 48 * mm, 48 * mm, 43 * mm],
        )
    )
    story.append(p("Table 4-1. A–B–A phases.", "Caption"))

    story += [
        h2("4.3 Experimental controls (mandatory)"),
        numbered(
            [
                "Identical PowerShell runbook hash; no manual clicking during timed sections.",
                "Disable Windows Update, defrag, scheduled optimize, Defender scheduled scans, S1 Full Disk Scan, and backup agents during timed windows (except tests that target those scans).",
                "No RDP during timed tests (RDP interrupts and bitmap traffic). Use WinRM. If console access is required, use hypervisor console without GUI login.",
                "Fix power plan: High Performance. Disable Core Parking (or document if OS ignores).",
                "Pin DiskSpd working set files; pre-create and pre-warm in an untimed setup step so first-run NTFS allocation is not billed to the test.",
                "Drop file-system cache between replicates with a documented method (e.g., large file flush + restart of test process; full reboot if cache is a listed factor). State whether cache-hot or cache-cold.",
                "Replicates: n ≥ 5 independent 15-minute runs per TC per phase for inferential stats; plus one 24-hour soak per OS in B only (and A1 once per OS).",
                "Randomize TC order within a phase using a seeded shuffle recorded in run_id metadata, except TC-01 always first after boot soak.",
                "Warm-up: 10 minutes after login/boot discarded; S1 additional 15 minutes after 'Healthy' discarded (policy pull, module load).",
            ]
        ),
        h2("4.4 Statistical treatment"),
        p(
            "For each metric M, compute M_A = mean of A1 and A2 replicate means if |A1 − A2| / A1 ≤ 5% (stability gate) or within 1.5× IQR; else fail the cell. "
            "Delta_abs = M_B − M_A. Delta_rel = Delta_abs / M_A for non-zero baselines. For latency, use geometric mean and percentile deltas, not only arithmetic mean. "
            "Report 95% bootstrap confidence intervals on Delta_abs. Do not quote a single-run max as the official number; max is a tail-risk indicator."
        ),
        p(
            "CPU percent is not additive across machines with different idle baselines in an interesting way — always report both percentage points and the absolute run-queue. "
            "Disk latency is highly heteroscedastic; prefer DiskSpd’s own percentile output plus Perfmon averages."
        ),
        h2("4.5 Probe-effect budget"),
        p(
            "windows_exporter + 1 Hz Perfmon should add well under 1% CPU on 8 vCPU; verify in a probe-only A-phase. If probe CPU &gt; 1.5%, increase scrape interval. WPR file-mode traces are separate billed runs. Never combine circular ETW + DiskSpd official number."
        ),
        h2("4.6 Failure and abort criteria (invalidate run)"),
        bullets(
            [
                "Hypervisor CPU ready &gt; 5% or memory ballooning / swapping on host.",
                "S1 console Offline &gt; 2 minutes during B (unless testing offline mode as a factor).",
                "Unexpected mitigation/quarantine that kills the load generator or DiskSpd.",
                "Bugcheck, unexpected reboot, disk full, ProgramData volume &lt; 10% free.",
                "NTP step, or lost Perfmon samples &gt; 1% of intervals.",
            ]
        ),
        h2("4.7 Formulae"),
        code(
            """delta_pp(CPU)     = CPU_B - CPU_A          # percentage points
delta_rel(IOPS)    = (IOPS_B - IOPS_A) / IOPS_A
minifilter_us_per_MB = minifilter_delay_us / (total_io_bytes / 1e6)
cpu_per_gbps       = CPU_privileged_percent / throughput_Gbps
soak_slope_MiB_h   = OLS_slope(Private_Bytes of SentinelAgent vs hours)"""
        ),
    ]

    story += [
        h1("5. Engineering SLOs, Gates, and Severity"),
        p(
            "These gates are <b>engineering defaults</b> for a general-purpose 8 vCPU / 32 GiB VM. Tighten for SQL/HPC; loosen only with a signed exception from the platform owner. "
            "They apply to the B vs A delta on the base cell unless noted."
        ),
    ]
    story.append(
        tbl(
            ["Gate", "Idle (TC-01)", "Loaded (TC-02–04 and extensions)", "Severity if missed"],
            [
                ["CPU _Total mean", "≤ 3 pp privileged+user combined attributable to S1", "≤ 8 pp at specified load; p99 ≤ 15 pp", "Sev-2 if loaded mean missed; Sev-1 if p99 &gt; 25 pp or persistent 100% core"],
                ["S1 process RSS sum", "≤ 1.5 GiB after 30m healthy (adjust if vendor published guidance differs for that build)", "≤ 2.5 GiB at 15m; soak slope ≤ 50 MiB/h after first 2h", "Sev-2; Sev-1 if RSS approaches 50% of VM RAM or host paging"],
                ["Available RAM", "Not reduced &gt; 2 GiB vs A", "No paging storm (Pages/sec p95 &lt; 100 on this size unless A also pages)", "Sev-1 if thrash"],
                ["DiskSpd p95 latency", "n/a", "≤ +15% vs A on the same profile; IOPS ≥ 90% of A", "Sev-2; Sev-1 if IOPS &lt; 75% or latency ×2"],
                ["Minifilter µs/MB", "Informational baseline", "Report; investigate if B/A &gt; 3× on sequential, or &gt; 5× on create-churn", "Sev-2 investigation"],
                ["NTttcp throughput", "n/a", "≥ 95% of A on 10 GbE class; CPU/Gbps documented", "Sev-2 if 90–95%; Sev-1 if &lt; 90%"],
                ["Context switches", "Informational", "Flag if B/A &gt; 2× at same offered load", "Sev-3 unless app latency also moved"],
                ["Unexpected mitigations", "0", "0 during official generators", "Sev-1 (test invalid + possible FP risk)"],
                ["Bugcheck / hang", "0", "0", "Sev-1"],
            ],
            [32 * mm, 48 * mm, 55 * mm, 42 * mm],
        )
    )
    story.append(p("Table 5-1. Default SLO gates. Recalibrate after the first OS cell if storage is faster/slower than assumed.", "Caption"))

    story += [
        h1("6. Test Case Catalog — Core (TC-01 to TC-04)"),
        p(
            "Each test case below includes: intent, S1 subsystem hypothesized to be on the hot path, exact load recipe, metrics, pass/fail mapping to Section 5, and probe-effect notes. "
            "Unless stated, run cache-cold and cache-hot as two labeled variants."
        ),
        h2("TC-01 — Baseline Idle Performance Delta"),
        h3("Intent"),
        p(
            "Measure the standing tax of a Healthy agent: timers, telemetry heartbeat, minifilter attachment, Defender interaction, and Deep Visibility idle flush. This is the number capacity planners put on every VM, including those that are not busy."
        ),
        h3("Hot path (hypothesized)"),
        p("SentinelAgent.exe user-mode; small IRPs through SentinelMonitor.sys; network to console; possible MsMpEng if Defender live."),
        h3("Procedure"),
        numbered(
            [
                "Reboot. Discard 10 minutes (A phases) or 15 minutes after Healthy (B).",
                "No user processes beyond instrumentation. Disconnect RDP.",
                "Collect 30 minutes at 1-second PDH. One 60-second WPR Light (CPU+Disk+Minifilter) in a separate replicate.",
                "Record console Online, last seen, policy ID, DV status, pending reboot = false.",
                "Capture fltmc, handle/thread counts, ProgramData\\Sentinel size.",
            ]
        ),
        h3("Metrics"),
        p(
            "CPU mean/p95; privileged vs user; S1 RSS; Available MBytes; Disk Transfers/sec (should be near A); network bytes to console; DPC %; context switches. "
            "Idle is the only TC where a 1 pp CPU delta can be meaningful — use longer windows."
        ),
        h3("Pass"),
        p("Idle CPU gate and RSS gate in Table 5-1. No scan in progress (console)."),
        h2("TC-02 — Extreme File System Volatility (DiskSpd + rapid file churn)"),
        h3("Intent"),
        p(
            "Stress the minifilter on both (a) high-throughput I/O and (b) metadata-heavy create/close/rename/delete. These are different IRP mixes. Combining them in one TC is intentional: production file servers do both; split scoring into TC-02a and TC-02b so results remain interpretable."
        ),
        h3("Hot path"),
        p("SentinelMonitor.sys IRP_MJ_CREATE/CLEANUP/READ/WRITE/SET_INFORMATION; Static AI on newly written PE-like files (02b); ProgramData DB writes."),
        h3("TC-02a DiskSpd throughput/latency (data path)"),
        p(
            "Pre-create a 32 GiB test file on the data volume during untimed setup. Run four official profiles, 15 minutes each, 5 replicates. Use Microsoft DiskSpd (inbox alternative: winsat disk, not sufficient)."
        ),
        code(
            r"""REM 4K random 70/30 R/W, QD32, 8 threads — OLTP-like
diskspd -c32G -d900 -Sh -r -w30 -b4K -o32 -t8 -L -D -Rxml E:\io\testfile.dat
REM 64K sequential read, QD8 — backup-like
diskspd -c32G -d900 -Sh -si -b64K -o8 -t4 -L -Rxml E:\io\testfile.dat
REM 1M sequential write, QD8 — ingest-like
diskspd -c32G -d900 -Sh -w100 -si -b1M -o8 -t4 -L -Rxml E:\io\testfile.dat
REM 4K random 100% write, QD16 — log-like small writes
diskspd -c32G -d900 -Sh -w100 -r -b4K -o16 -t8 -L -Rxml E:\io\testfile.dat"""
        ),
        p(
            "Flags: -Sh disables software/hardware cache as documented by DiskSpd for that version — confirm against the DiskSpd wiki for the binary used; if -Sh is too harsh for a role cell (SQL), add a cache-on variant labeled TC-02a-cache. "
            "-L latency histogram is mandatory. Compare p50/p95/p99 and IOPS, not only MB/s.",
            "Note",
        ),
        h3("TC-02b Rapid file churn (metadata / minifilter create path)"),
        p(
            "On a dedicated directory tree (millions of files will wreck NTFS — cap the working set): 50 000 files per cycle, 1–64 KiB random content, mix of .bin, .tmp, .dll, .exe (benign, lab-signed or unsigned as a factor), 20 cycles. "
            "Operations: create, write, flush, rename, set attributes, delete. Parallelism: 16 PowerShell runspaces or a compiled C# churner (preferred for less PS overhead). "
            "Include a PE-write submix (copy a 5 MiB benign EXE 2 000 times under new hashes/names) to force Static AI on-write without malware."
        ),
        h3("Metrics"),
        p(
            "DiskSpd XML; PDH disk latency and queue; CPU privileged; System process I/O; minifilter µs/MB (paired ETL); time-to-complete churn cycles; SentinelStaticEngine CPU; ProgramData growth during churn."
        ),
        h3("Pass"),
        p("DiskSpd gates; no unexpected quarantine of the churner; NTFS remains mountable; no disk full."),
        h2("TC-03 — Process Churn Interrupt Stress"),
        h3("Intent"),
        p(
            "PsSetCreateProcessNotifyRoutine / image-load notify / Static AI on execute are expensive. Short-lived processes (cmd, PowerShell -NoProfile -Command exit, whoami, hostname) generate interrupts, object manager traffic, and ETW-like telemetry internally in S1 Storyline."
        ),
        h3("Procedure"),
        numbered(
            [
                "Use a compiled launcher (C/C#) that CreateProcess/WaitForSingleObject in a tight loop to avoid PowerShell host cost dominating. Keep a PowerShell variant only as a sensitivity test (real admins use PS).",
                "Burst profile: 2 000 process creates/second target for 60 seconds, then 10 s idle, repeat for 15 minutes. If the OS cannot sustain 2k/s, record achieved rate and keep offered load identical across A/B/A2 (fixed concurrency, not fixed rate, if rate cannot be met).",
                "Image mix: 70% tiny native EXE, 20% cmd.exe, 10% powershell.exe -NoProfile -Command 'exit 0'.",
                "Do not disable Windows Defender AMSI in A if it is on in B’s coexistence cell; keep OS controls identical.",
                "Paired WPR: CPU Precise + Process create + Minifilter, 30-second slice.",
            ]
        ),
        h3("Metrics"),
        p(
            "Achieved creates/sec; mean CreateProcess wall time; CPU privileged; context switches; S1 CPU; handle count leaks; DV event volume; unexpected kills of the launcher (fail)."
        ),
        h3("Pass"),
        p("Loaded CPU gate; create rate ≥ 90% of A; no leak of handles in launcher or S1 beyond soak slope."),
        h2("TC-04 — Network Inspection and Throughput Degradation"),
        h3("Intent"),
        p(
            "S1 is not a full TLS-intercepting secure web gateway. Overhead comes from WFP/callout classification, connection Storyline events, DNS/process-network correlation, and CPU stolen from the TCP stack. Measure bulk throughput and connection-setup storms separately (04a/04b/04c)."
        ),
        h3("TC-04a Bulk TCP (NTttcp / iPerf3)"),
        p(
            "LG ↔ SUT, same VLAN, 10/25 GbE class. NTttcp preferred on Windows (ctsTraffic or Microsoft ntttcp). Example: ntttcp -s/-r, 8 threads, 30–60 s warmup, 5 × 60 s. iPerf3 as cross-check. Disable Windows Firewall only if it is disabled in production; otherwise keep firewall ON in all phases (it is a confounder if toggled)."
        ),
        h3("TC-04b Connection storm"),
        p(
            "Short TCP connects to an IIS or custom socket on SUT, 10k concurrent attempts, HTTP GET of 1 KB. Measures per-connection inspection better than elephant flows."
        ),
        h3("TC-04c SMB data + metadata"),
        p(
            "From LG: robocopy /NFL /NDL /NJH /NJS a 20 GiB tree and a 100k-small-file tree to an SMB share on SUT (file-server overlay or a simple share on base cell). Report tree-copy minutes and files/sec."
        ),
        h3("Metrics"),
        p("Gb/s, retransmits, NIC PPS, CPU/Gbps, WFP drops if logged, S1 network bytes, firewall drops. ETL networking + CPU in paired run."),
        h3("Pass"),
        p("Throughput gate in Table 5-1; connection storm p95 latency ≤ +20% vs A."),
    ]

    story += [
        h1("7. Extended Test Cases (TC-05 to TC-24)"),
        p(
            "The following cases are in scope for an exhaustive campaign. If calendar or hardware forces a cut, execute P0 (TC-01–04, 07, 08, 11, 16) on all OS versions; P1 on 2022 and 2025 first."
        ),
        h2("TC-05 — Registry volatility"),
        p(
            "Hot path: CmRegisterCallbackEx-style registry callbacks. Recipe: 100k RegSetValue/RegDeleteValue cycles across HKLM\\SOFTWARE\\LabChurn (pre-created). Metric: ops/sec, privileged CPU, S1 CPU. Pass: ops/sec ≥ 90% of A."
        ),
        h2("TC-06 — Memory pressure and large working sets"),
        p(
            "Allocate 20 GiB user-mode array, touch pages, then sequential DiskSpd. Detect whether S1 RSS + Defender + working set induces paging that A does not. Metric: Pages/sec, Available MBytes, SQL-like latency if overlay. Pass: no paging storm unique to B."
        ),
        h2("TC-07 — Full Disk Scan / On-demand Static AI storm"),
        p(
            "From console, initiate Full Disk Scan during idle and during DiskSpd 4K random. This is the classic “backup window plus AV scan” failure mode. Metric: scan duration, CPU, disk queue, DiskSpd IOPS collapse, user-visible app latency. "
            "Pass: document scan duration; DiskSpd IOPS during scan is informational but if IOPS &lt; 50% of A-without-scan, flag Sev-2 for scheduling guidance (do not scan during business I/O)."
        ),
        h2("TC-08 — Boot, login, and service-start path (WPR Boot)"),
        p(
            "WPR Boot + Autologon, 3 iterations, minifilter + CPU + disk. Compare boot-to-desktop and boot-to-WinRM ready. S1 driver load at boot can delay other SERVICE_AUTO_START. Metric: WPA gold bars, µs/MB, time to HEALTHY. Pass: WinRM ready ≤ +20% vs A unless justified by driver load."
        ),
        h2("TC-09 — PowerShell, WMI, and AMSI-shaped scripting"),
        p(
            "Run a signed lab script that enumerates WMI (Win32_Process, Win32_Service) in a loop and a constrained language test. Behavioral AI and AMSI (if Defender) interact. Metric: loop time, CPU. Do not use attack-tool semantics; keep administrative WMI only."
        ),
        h2("TC-10 — Certificate / Authenticode storm"),
        p(
            "Copy 5 000 signed and 5 000 unsigned benign EXEs and execute hash-only (Get-FileHash) versus execute. Distinguishes catalog/signature checks from execute callbacks."
        ),
        h2("TC-11 — Deep Visibility telemetry storm"),
        p(
            "Policy B-DV-ON vs B-DV-OFF (A–B–A still uses unmanaged A). Under TC-03 and TC-04b load, measure ProgramData growth, SentinelAgent RSS, egress Mbps to console, and CPU. Hypothesis H5. Pass: DV-ON RSS and disk growth documented; if RSS gate missed only with DV-ON, recommend DV sampling policy rather than removing the agent."
        ),
        h2("TC-12 — Policy mode matrix: Detect vs Protect vs engines off"),
        p(
            "Cells: Protect+all engines; Detect-only; Static AI suspicious off; Behavioral off (if license/policy allows). Same TC-02b/TC-03. Attributes overhead to engines. Never leave engines off outside lab."
        ),
        h2("TC-13 — Offline / deferred cloud intelligence"),
        p(
            "Block console after Healthy (ACL) for 4 hours under TC-02a. Measures local DB buffering and RAM when upload fails. Aligns with field reports of RAM growth under disk pressure. Pass: no crash; RSS slope documented; agent remains protective offline."
        ),
        h2("TC-14 — Interoperability exclusions effectiveness"),
        p(
            "Apply vendor-recommended path exclusions for the SQL overlay (MDF/LDF/backup) and DiskSpd directory. Re-run TC-02a/SQL. Measure recovered IOPS vs security coverage loss (qualitative, signed by security architect). Pass: IOPS returns to ≥ 97% of A on excluded paths; confirm via Analyzer that those paths are no longer in agent time."
        ),
        h2("TC-15 — Agent install, upgrade, and uninstall hysteresis"),
        p(
            "Timed install from MSI/EXE silent; reboot; Healthy TTR (time-to-ready). Upgrade N-1 → N during DiskSpd (should be a maintenance window). Uninstall with passphrase; verify driver gone (fltmc). A2 must match A1. Pass: uninstall completeness; no leftover filters."
        ),
        h2("TC-16 — 24-hour soak (stability, leak, DB growth)"),
        p(
            "B phase only plus one A1 control. Light background: 1% DiskSpd + 10 proc/s. Metric: RSS slope, handle count, ProgramData GiB, log rotation (2016 KB4093119 relevance), console flaps. Pass: slope and disk-growth gates; free disk &gt; 20%."
        ),
        h2("TC-17 — VSS / snapshot / rollback feature tax"),
        p(
            "Enable VSS; hourly shadow copy during TC-02a. Optional: console-initiated rollback on a disposable clone (not the official cell). Metric: disk latency spikes aligned to VSS. Pass: no VSS hangs; document spike magnitude."
        ),
        h2("TC-18 — Application overlays (SQL, IIS, file server, AD)"),
        p(
            "HammerDB or ostress against SQL; IIS httperf/wrk-equivalent (Windows: bombardier/NTttcp HTTP); SMB as TC-04c; AD: many LDAP binds from LG. Report application SLOs, not only OS counters. Pass: app p95 ≤ +10% vs A unless exclusion cell recovers it."
        ),
        h2("TC-19 — Containers / Hyper-V host (conditional)"),
        p(
            "If production places S1 on Hyper-V hosts or Windows containers: vmwp.exe, VHDX churn, live storage migration. Follow SentinelOne Hyper-V exclusion publications. Nested virt optional. Out of scope if the estate only agents guests, not hosts — state the estate fact in the report."
        ),
        h2("TC-20 — Microsoft Defender coexistence"),
        p(
            "Three subcells: Defender RTP OFF; Defender RTP ON + S1; Defender passive. Dual minifilters can double CREATE tax. Metric: TC-02b create rate. Pass: choose a production state; do not ship dual RTP without numbers."
        ),
        h2("TC-21 — DPC/ISR and kernel latency deep dive"),
        p(
            "xperf -on PROCESSOR+DPC+INTERRUPT+DISK_IO_INIT or WPR CPU Precise. 30 s under TC-02a and TC-03. Attribute DPC stacks. Driver Verifier: disposable clone only. Pass: no DPC &gt; 1 ms persistent; document ISR/DPC % delta."
        ),
        h2("TC-22 — Server Core vs Desktop Experience"),
        p(
            "Repeat TC-01, 02a, 03, 04a on Server Core 2022/2025. Idle CPU should drop; agent UI absent. Pass: Core is not worse than GUI for loaded gates."
        ),
        h2("TC-23 — High-entropy and compressed write mix (Static AI cost)"),
        p(
            "Write 20 GiB of /dev/urandom-equivalent vs zeros vs ZIP archives vs PE. Static AI cost should spike on PE, not on zeros. Metric: write MB/s and StaticEngine CPU by file class."
        ),
        h2("TC-24 — Patch storm / installer burst"),
        p(
            "Install a stack of lab MSIs (7-Zip, C++ redistributables, a signed in-house MSI) in sequence. Real servers see this on patch Tuesdays. Metric: total wall time vs A; CPU; unexpected mitigations on installers."
        ),
    ]

    story += [
        h1("8. Experiment Matrix and Execution Calendar Logic"),
        p(
            "Full factorial: 4 OS × 3 phases × (core TCs + extensions) × 5 replicates is large. Execute as a blocked design:"
        ),
        bullets(
            [
                "<b>Block 1 — Core:</b> All OS × A1/B/A2 × TC-01, 02a, 02b, 03, 04a, 04c. Mandatory.",
                "<b>Block 2 — Kernel:</b> 2022 + 2025 × paired WPR for 02b, 03, 08, 21.",
                "<b>Block 3 — Policy:</b> 2022 only × TC-11, 12, 14, 20.",
                "<b>Block 4 — Overlays:</b> 2022 + 2019 × SQL and File Server × TC-18.",
                "<b>Block 5 — Soak:</b> All OS × TC-16 (B) + A1 once.",
                "<b>Block 6 — Legacy risk:</b> 2016 gets Block 1 + soak + TC-08; skip overlays if hardware-limited.",
            ]
        ),
        p(
            "Do not parallelize two SUTs on one host unless CPU ready remains &lt; 2%. Prefer sequential SUT, parallel LG."
        ),
    ]

    story += [
        h1("9. Automation and Telemetry Pipeline"),
        h2("9.1 Built-in and first-party Windows load generators"),
    ]
    story.append(
        tbl(
            ["Tool", "Role in this plan", "Notes"],
            [
                ["DiskSpd", "TC-02a official storage"],
                ["NTttcp / ctsTraffic", "TC-04a TCP"],
                ["iPerf3 (Win64)", "TC-04a cross-check"],
                ["robocopy", "TC-04c SMB / tree copy"],
                ["winsat", "Sanity only, not official"],
                ["WPR / WPA / xperf", "Minifilter, DPC, boot"],
                ["logman / relog / typeperf", "PDH collection"],
                ["fltmc", "Filter inventory"],
                ["Performance Monitor MMC", "Ad-hoc; templates exported to XML"],
                ["Windows Admin Center", "Optional live view, not source of truth"],
                ["PowerShell 5.1/7", "Orchestration, churner host (not hot loop)"],
                ["WinRM / OpenSSH", "Remote execution"],
                ["wevtutil", "Export System/Application around failures"],
                ["ProcMon", "Last resort; high probe effect — 10 s slices only"],
                ["Resource Monitor", "Human debug, not evidence"],
            ],
            [50 * mm, 127 * mm],
        )
    )
    story.append(p("Table 9-1. Load and OS tools.", "Caption"))

    story += [
        h2("9.2 Orchestration architecture"),
        p(
            "A controller VM (no S1) holds the runbook repository. Execution is idempotent: invoke-test.ps1 -RunId -Os -Phase -TestCase -Rep. "
            "The script: (1) asserts NTP, power plan, S1 presence matches phase; (2) starts logman and windows_exporter textfile labels; (3) starts workload; (4) stops collectors; (5) hashes artifacts; (6) pushes to a CIFS/S3-compatible evidence store; (7) writes a JSON summary (IOPS, CPU mean, RSS)."
        ),
        h2("9.3 Prometheus / Grafana"),
        bullets(
            [
                "windows_exporter listen on mgmt NIC only.",
                "Labels: os, phase, tc, run_id, agent_version, policy_id, host.",
                "Dashboards: Idle standing tax; DiskSpd overlay; Process storm; Network; Soak slope.",
                "Alerting is optional in lab; use recording rules for p95 CPU over 5m.",
            ]
        ),
        h2("9.4 Splunk"),
        p(
            "Index=winperf_lab sourcetype=perfmon:csv and sourcetype=s1:agentlog. SPL example: timechart avg(Processor_Percent) by phase. "
            "Correlate EventCode 7036 (service) and S1 operational events with CPU spikes. Keep license volume in mind — drop Process Creation (4688) at full rate unless a dedicated TC requires it."
        ),
        h2("9.5 Evidence pack schema"),
        code(
            r"""evidence/{run_id}/
  meta.json          # os, phase, hashes, ntp, fltmc, sentinelctl status
  perf/S1Perf.blg
  perf/S1Perf.csv
  diskspd/*.xml
  ntttcp/*.log
  wpr/*.etl          # only trace replicates
  grafana/screenshot_refs.txt
  console/device_export.json
  programdata_size.txt
  summary.json"""
        ),
        h2("9.6 Sample meta.json fields"),
        code(
            """{
  "run_id": "2022-20260903T180000Z-B-TC02a-r3",
  "os": "Windows Server 2022 Datacenter 21H2 CU",
  "agent_file_version": "25.x.x.x",
  "policy_hash": "sha256:...",
  "deep_visibility": true,
  "protect_mode": true,
  "defender_rtp": false,
  "hypervisor_cpu_ready_pct_max": 1.2,
  "diskspd_version": "2.2",
  "wpt_version": "ADK 10.1.x"
}"""
        ),
    ]

    story += [
        h1("10. Data Analysis, Attribution, and Reporting"),
        h2("10.1 Attribution tree"),
        numbered(
            [
                "If DiskSpd IOPS dropped but CPU is idle: storage or minifilter blocking (look at Avg Disk sec and WPA minifilter).",
                "If CPU privileged high and S1 user-mode low: kernel callbacks / System PID 4 / DPC.",
                "If SentinelStaticEngine CPU high: on-write/on-execute PE path (TC-02b, TC-10, TC-23).",
                "If SentinelAgent RSS high and disk free low: local DB / flush issue (TC-13, TC-16) — capture ProgramData size.",
                "If only DV-ON shows egress and disk writes: telemetry path (TC-11).",
                "If A2 ≠ A1: fragmentation, Defender defs, leftover driver, or host noise — do not publish B delta.",
            ]
        ),
        h2("10.2 Required result tables (per OS)"),
        p(
            "Publish: idle CPU/RAM; DiskSpd four profiles (IOPS, p95 latency); churn files/sec; process creates/sec; NTttcp Gb/s; minifilter µs/MB; soak slope. Each with A1, B, A2, delta, CI, n."
        ),
        h2("10.3 Narrative report sections"),
        p(
            "Executive scorecard (pass/fail SLOs); methodology deviations; findings ranked by Sev; exclusion recommendations; capacity model (extra vCPU per guest); upgrade regression plan; open questions from Section 15."
        ),
    ]

    story += [
        h1("11. Risks, Ethics, and Interference Management"),
        bullets(
            [
                "No malware, exploits, credential dumps, or weaponized macros. Benign PE only.",
                "Anti-Tamper passphrase stored in an HSM/secret manager, not in git.",
                "Lab site token ≠ production token.",
                "Process storms can trip SOC detections — notify SOC that the lab site is noisy.",
                "Full Disk Scan and rollback can resemble destructive activity — disposable data only.",
                "Driver Verifier and experimental filters can bugcheck — isolated cluster.",
                "GDPR/PII: do not copy production user data into churn trees.",
            ]
        ),
    ]

    story += [
        h1("12. Roles and RACI (abbreviated)"),
    ]
    story.append(
        tbl(
            ["Activity", "Perf Eng", "Sec Arch", "Windows Plat", "SOC", "Hypervisor"],
            [
                ["Template freeze", "C", "I", "A/R", "I", "C"],
                ["S1 policy design", "C", "A/R", "C", "C", "I"],
                ["Run execution", "A/R", "I", "C", "I", "C"],
                ["WPA minifilter analysis", "A/R", "C", "C", "I", "I"],
                ["Exclusion approval", "C", "A", "C", "R", "I"],
                ["Go/no-go", "R", "A", "C", "C", "I"],
            ],
            [42 * mm, 27 * mm, 27 * mm, 28 * mm, 22 * mm, 31 * mm],
        )
    )
    story.append(p("Table 12-1. R = Responsible, A = Accountable, C = Consulted, I = Informed.", "Caption"))

    story += [
        h1("13. Entry, Exit, and Deliverables"),
        h2("13.1 Entry criteria"),
        bullets(
            [
                "Gold images hashed; CU level frozen; ADK/WPT installed; DiskSpd/NTttcp staged.",
                "S1 test site created; agent package pinned; passphrase escrowed.",
                "Hypervisor reservations verified; storage QoS floor measured with DiskSpd from a non-S1 VM.",
                "NTP, WinRM, exporter scrape verified.",
                "Section 15 questions either answered or accepted as assumptions in 0.3.",
            ]
        ),
        h2("13.2 Exit criteria"),
        bullets(
            [
                "Block 1 complete on all four OS versions with A2 stability gate passed.",
                "Scorecard vs Table 5-1 published.",
                "Raw evidence pack archived.",
                "Known issues filed (agent bugs vs config).",
            ]
        ),
        h2("13.3 Deliverables"),
        bullets(
            [
                "This test plan (PDF).",
                "Results workbook + Grafana snapshot.",
                "WPA analysis notes for minifilter.",
                "Capacity recommendation (vCPU/RAM adder).",
                "Policy/exclusion recommendations signed by Security Architecture.",
            ]
        ),
    ]

    story += [
        h1("14. Regression Pack (every SentinelOne GA)"),
        p(
            "On each agent GA: 2022 + 2025 only; A1 snapshot reuse if OS unchanged; B new agent; TC-01, 02a (4K mixed), 02b (one cycle), 03 (5 min), 04a, 16 (8 h abbreviated). Fail upgrade if loaded CPU or DiskSpd gates regress &gt; 5% relative to previous GA on the same template."
        ),
    ]

    story += [
        h1("15. Open Questions and Items Requiring Stakeholder Clarification"),
        p(
            "The following were not specified in the originating request. The plan is executable under Section 0.3 assumptions; confirmation will change policy cells, SLOs, or scope."
        ),
    ]
    story.append(
        tbl(
            ["ID", "Question", "Impact if unanswered", "Assumption in this revision"],
            [
                ["Q1", "Exact Singularity SKU and whether Deep Visibility / EDR is licensed on servers?", "DV-ON may be invalid; overhead attribution wrong", "DV ON, Protect, Complete-class"],
                ["Q2", "Pinned Windows agent version and whether Server Core is in estate?", "Support matrix / TC-22", "Latest GA Group 1; Core optional"],
                ["Q3", "Production policy JSON (engines, suspicious handling, network, USB, etc.)?", "Lab B phase may be lighter/heavier than prod", "Protect + default engines + Anti-Tamper"],
                ["Q4", "Is S1 the sole AV, or must Defender RTP remain on?", "TC-20 becomes the production proxy", "Defender RTP off in lab default"],
                ["Q5", "Hypervisor (vSphere vs Hyper-V), NIC speed, and storage class?", "Throughput ceilings and CPU ready", "Reserved 8 vCPU / NVMe / 10 GbE+"],
                ["Q6", "Are Hyper-V hosts themselves agented?", "TC-19 in or out", "Guests only unless told otherwise"],
                ["Q7", "Application overlays in scope (SQL/IIS/AD/file)?", "TC-18 effort", "Recommended P1 on 2019/2022"],
                ["Q8", "Numeric SLOs or vendor contractual overhead limits?", "Table 5-1 may be too strict/loose", "Engineering defaults in §5"],
                ["Q9", "Telemetry standard: Splunk vs Prometheus vs both? Retention?", "Pipeline build", "windows_exporter+Prometheus+Grafana required; Splunk recommended"],
                ["Q10", "May lab use unsigned benign EXEs, or must all images be Authenticode-signed?", "TC-02b/10/23 Static AI mix", "Mix signed+unsigned, documented"],
                ["Q11", "Console region, air-gapped, or proxy MITM?", "TC-04/11/13 network path", "Direct HTTPS to S1 cloud with measured RTT"],
                ["Q12", "Windows Server 2025 build (GA channel) and HVCI/VBS required?", "Kernel tax confounder", "VBS off unless production requires on — then add factor"],
                ["Q13", "Acceptable probe: may we install windows_exporter, or must we use only in-box logman?", "Cardinality / change control", "Both: logman source of truth; exporter for viz"],
                ["Q14", "Who owns exclusion approval if SQL IOPS recover only with path exclusions?", "RACI", "Security Architecture accountable (Table 12-1)"],
                ["Q15", "Is a dedicated S1 test tenant available, and can Full Disk Scan / rollback be used?", "TC-07/17", "Yes, isolated site"],
            ],
            [14 * mm, 55 * mm, 52 * mm, 56 * mm],
        )
    )
    story.append(p("Table 15-1. Clarifications. Resolve Q1–Q6 and Q8 before Block 1.", "Caption"))

    story += [
        h1("16. Appendix A — Sentinelctl and Health Preflight"),
        code(
            r"""cd "C:\Program Files\SentinelOne\Sentinel Agent *"
.\sentinelctl.exe status
.\sentinelctl.exe version
# Record: protection, pending reboot, management URL
Get-Process SentinelAgent, SentinelStaticEngine, SentinelServiceHost -ErrorAction SilentlyContinue |
  Select-Object Name, Id, CPU, WorkingSet64, PrivateMemorySize64, HandleCount
fltmc
# ProgramData footprint
Get-ChildItem C:\ProgramData\Sentinel -Recurse -ErrorAction SilentlyContinue |
  Measure-Object -Property Length -Sum"""
        ),
        h1("17. Appendix B — WPR Minifilter Boot Profile (operator notes)"),
        p(
            "WPRUI as Administrator → Performance scenario = Boot → Detail = Light → Logging = File → Iterations = 2 or 3. "
            "Enable First Level Triage; Resource Analysis: CPU, Disk I/O; Scenario Analysis: Minifilter I/O activity. "
            "Configure Autologon for a lab admin (Sysinternals Autologon) so logon is deterministic. Zip WPA Files from the autologon profile. "
            "In WPA, compute minifilter delay µs / MB for the Sentinel filter versus total. Compare A vs B on the same gold image."
        ),
        h1("18. Appendix C — Example Grafana / Prometheus Metric Names"),
        p(
            "windows_cpu_time_total (rate, idle vs privileged); windows_memory_available_bytes; windows_logical_disk_read_latency_seconds_total; "
            "windows_net_bytes_total; windows_system_context_switches_total; windows_process_working_set_bytes{process=~\"Sentinel.*\"}; "
            "windows_process_cpu_time_total{process=~\"Sentinel.*\"}; windows_process_handles{process=~\"Sentinel.*\"}."
        ),
        h1("19. Appendix D — Change Log"),
    ]
    story.append(
        tbl(
            ["Rev", "Date", "Notes"],
            [
                ["1.0", DOC_DATE.isoformat(), "Initial exhaustive plan: A–B–A, TC-01–24, S1-specific component map, SLO gates, open questions Q1–Q15."],
            ],
            [22 * mm, 32 * mm, 123 * mm],
        )
    )
    story.append(p("Table 19-1. Revision history.", "Caption"))

    story += [
        h1("20. Appendix E — Glossary"),
        bullets(
            [
                "<b>A–B–A:</b> Unmanaged / agentized / unmanaged-revert experimental design.",
                "<b>Deep Visibility (DV):</b> S1 EDR telemetry of process/file/network storylines uploaded to console.",
                "<b>Minifilter:</b> File-system filter driver hosted by Filter Manager (fltmgr.sys), stacked by altitude.",
                "<b>Static AI:</b> Pre-execution / on-write ML inspection of files (SentinelStaticEngine).",
                "<b>WFP:</b> Windows Filtering Platform — kernel network inspection points.",
                "<b>Probe effect:</b> Measurement tools changing the metric being measured.",
                "<b>CPU ready:</b> Hypervisor time a vCPU wanted to run but waited for a pCPU.",
                "<b>SLO gate:</b> Engineering pass/fail threshold, not a legal warranty.",
            ]
        ),
        Spacer(1, 8 * mm),
        p(
            "End of document. This test plan is intended for isolated laboratory execution against SentinelOne management sites designated for testing. "
            "It does not authorize production Full Disk Scan, rollback, policy weakening, or Anti-Tamper bypass outside change control.",
            "Note",
        ),
    ]

    doc = SimpleDocTemplate(
        str(OUT),
        pagesize=A4,
        leftMargin=16 * mm,
        rightMargin=16 * mm,
        topMargin=20 * mm,
        bottomMargin=16 * mm,
        title="SentinelOne Windows Server Host-Level Performance Test Plan",
        author="Performance Engineering & Cybersecurity Architecture",
        subject=DOC_ID,
    )
    doc.build(story, onFirstPage=cover_page, onLaterPages=header_footer)
    print(f"Wrote {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    build()
