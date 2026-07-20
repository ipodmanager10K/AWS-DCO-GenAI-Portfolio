# 📊 DCO 로그 분석 보고서 (DCO Log Analysis Report)

이 보고서는 교육용 샘플 DCO 로그 파일(`sample_dco_log.txt`)을 분석하여 파이썬 스크립트로 자동 생성된 결과입니다.

## 📈 1. 전체 통계
* **분석된 총 로그 라인 수:** 140개

---

## ⚠️ 2. 심각도별 로그 분포 (Severity Distribution)
시스템의 긴급 수준과 안정성을 판단하기 위한 심각도 분포 통계입니다.

| 심각도 (Severity) | 로그 수 (Count) | 진단 상태 및 비고 |
| :--- | :---: | :--- |
| ERROR | 2 | 정상 동작 상태 로그 |
| INFO | 135 | 정상 동작 상태 로그 |
| WARNING | 3 | ⚠️ 이상 징후 감지 (사전 예방 조치 필요) |

---

## 🔍 3. 이벤트별 발생 빈도 (Event Frequency)
네트워크 장비 및 호스트에서 감지된 이벤트 종류별 빈도 통계입니다.

| 이벤트명 (Event Name) | 발생 횟수 (Count) |
| :--- | :---: |
| Normal heartbeat | 125 |
| Ticket opened | 3 |
| Ticket escalated | 3 |
| Maintenance completed | 3 |
| Fan Alert | 1 |
| Temperature warning | 1 |
| SSD failure warning | 1 |
| CRC error 증가 | 1 |
| Link Down | 1 |
| Link Up | 1 |

---

## 🚨 4. 경고 및 심각 로그 목록 (WARNING & CRITICAL Logs)
장애 파악을 위해 즉각 조치가 요구되는 경보 수준의 원본 로그 상세 내역입니다.

| 발생 일시 (Timestamp) | 장비명 (Device) | 심각도 | 이벤트명 | 상세 메시지 (Message) |
| :--- | :--- | :---: | :--- | :--- |
| 2026-07-03 01:05:00 | DEMO_CORE_SW_02 | `WARNING` | Fan Alert | Fan module 2 RPM dropped to 15% (Below threshold 20%). IP: 198.51.100.2 |
| 2026-07-03 02:05:00 | EDU_SRV_R04_N12 | `WARNING` | Temperature warning | Chassis temperature reached 42C (Threshold: 40C). IP: 192.0.2.12 |
| 2026-07-03 03:05:00 | SAMPLE_TOR_SW_01 | `WARNING` | CRC error 증가 | Interface Gi0/1 CRC error counter increased to 154 within 5 minutes. IP: 192.0.2.1 |

---

## 🎯 5. 장애 핵심 감지 요약 (CRC_ERROR, LINK_DOWN, TICKET_ESCALATED)
물리적인 에러(`CRC_ERROR`), 링크 단절(`LINK_DOWN`), 상위 에스컬레이션(`TICKET_ESCALATED`) 등 DCO에서 매우 중요하게 모니터링하는 핵심 이벤트 요약입니다.

| 감지 유형 | 발생 일시 (Timestamp) | 장비명 (Device) | 심각도 | 이벤트명 | 탐지 메시지 |
| :---: | :--- | :--- | :---: | :--- | :--- |
| - | - | - | - | - | 핵심 감지 키워드가 포함된 이벤트가 발견되지 않았습니다. |

---
* **보고서 생성 시각:** 2026-07-20 11:26:41 (KST)
* *본 보고서는 인턴십 직무 이해를 돕기 위한 교육용 시뮬레이션 결과로 실제 인프라의 실제 동작 데이터가 아닙니다.*
