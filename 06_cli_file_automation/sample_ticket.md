# [교육용 샘플 데이터] SAMPLE-TOR-SW-01 장애 티켓

> [!NOTE]
> **교육용 샘플 데이터 사용 안내**
> 이 문서는 AWS DCO 인턴십 직무 이해를 위한 생성형 AI 활용 및 포트폴리오 제작 과정의 실습 자료입니다. 
> 본 문서에 기재된 모든 정보는 가상의 교육용 샘플 데이터이며, 실제 AWS 내부 정보, 실제 장비명, 실제 IP, 실제 시리얼 번호 및 실제 고객 정보와는 전혀 무관합니다.

---

## 1. 티켓 기본 정보 (Ticket Information)

- **티켓 ID:** EDU-TICKET-2026-1007
- **발생 시간:** 2026-07-07 15:10:00 KST
- **샘플 장비명:** SAMPLE-TOR-SW-01
- **이벤트 종류:** CRC Error Increase & Link Down (CRC 에러 증가 및 링크 다운)
- **심각도:** Medium (교육용 가상 등급)
- **Escalation 필요 여부:** 필요 (상위 지원 부서 및 하드웨어 점검 부서 전달 대상)

---

## 2. 관찰 내용 및 가상 현상 기록 (Observations)

- **상황 설명:** 
  가상의 모니터링 시스템 로그 분석 중 `SAMPLE-TOR-SW-01` 스위치 장비에서 다음 현상이 차례로 관찰되었습니다.
  1. 특정 포트(가상 포트: `eth-1/1`)에서 CRC(Cyclic Redundancy Check) 에러 카운트가 급격히 증가함.
  2. 에러 누적 이후 해당 인터페이스의 상태가 `Link Down`으로 전환됨.
- **상세 관찰 로그 패턴 (예시):**
  - `2026-07-07 15:05:22 KST [SAMPLE-TOR-SW-01] WARNING: CRC error threshold exceeded on interface eth-1/1 (errors: 1240)`
  - `2026-07-07 15:10:00 KST [SAMPLE-TOR-SW-01] CRITICAL: Interface eth-1/1 status changed to Link Down`

---

## 3. 조치 및 Escalation 가이드

- **원인 단정 금지:** 현 단계에서 케이블 불량, 모듈 고정 상태 불량, 혹은 포트 고장 등으로 원인을 단정 짓지 않습니다. 로그에 표현된 CRC 에러 누적과 링크 다운 현상만 객관적으로 보고서에 기재합니다.
- **Escalation 절차:** 추가적인 정밀 물리 점검을 위해 가상의 하드웨어 운영팀(DCO-HW-Team)으로 티켓 이관을 검토합니다.

---

## 4. 보안 주의사항 (Security Guidelines)

- 실제 AWS 내부망 정보, 실제 장비 IP 주소, 시리얼 번호, 개인정보 및 고객 데이터를 본 티켓 및 관련 실습 파일에 절대 포함하지 마십시오.
- 모든 식별자에는 `SAMPLE-`, `EDU-` 등의 접두어를 사용하여 실제 데이터와 혼동을 피합니다.
