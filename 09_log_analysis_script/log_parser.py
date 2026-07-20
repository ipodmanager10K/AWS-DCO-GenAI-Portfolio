import os
from datetime import datetime

def analyze_logs(input_path, output_path):
    print(f"[*] '{input_path}' 로그 파일 분석을 시작합니다...")
    
    # 07_log_analysis_script/ 폴더가 없으면 자동으로 만듭니다.
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"[*] 출력 폴더 생성 완료: {output_dir}/")

    total_lines = 0
    severity_counts = {}
    event_counts = {}
    warning_or_critical = []
    major_events = [] # CRC_ERROR, LINK_DOWN, TICKET_ESCALATED 감지용

    # 파일을 안전하게 열고 한 줄씩 읽습니다 (UTF-8 인코딩 지정)
    with open(input_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue  # 빈 줄은 건너뜁니다.
            
            total_lines += 1
            
            # 로그의 구분자인 세로바(|)를 기준으로 데이터를 쪼갭니다.
            parts = [part.strip() for part in line.split('|')]
            if len(parts) < 5:
                continue  # 형식이 올바르지 않은 로그는 분석에서 제외합니다.
                
            timestamp, device, severity, event, message = parts[0], parts[1], parts[2], parts[3], parts[4]
            
            # 1. 심각도별(SEVERITY) 로그 개수 카운팅
            severity_counts[severity] = severity_counts.get(severity, 0) + 1
            
            # 2. 이벤트별(EVENT) 로그 개수 카운팅
            event_counts[event] = event_counts.get(event, 0) + 1
            
            # 3. WARNING 또는 CRITICAL 등급의 로그만 별도로 모으기
            if severity in ['WARNING', 'CRITICAL']:
                warning_or_critical.append({
                    'timestamp': timestamp,
                    'device': device,
                    'severity': severity,
                    'event': event,
                    'message': message
                })
                
            # 4. CRC_ERROR, LINK_DOWN, TICKET_ESCALATED 주요 장애 키워드 요약
            # 이벤트 종류나 상세 메시지에 해당 키워드가 포함되어 있다면 주요 이벤트로 감지합니다.
            for keyword in ['CRC_ERROR', 'LINK_DOWN', 'TICKET_ESCALATED']:
                if keyword in event or keyword in message:
                    major_events.append({
                        'keyword': keyword,
                        'timestamp': timestamp,
                        'device': device,
                        'severity': severity,
                        'event': event,
                        'message': message
                    })
                    break  # 하나의 로그가 여러 키워드에 매칭될 경우 한 번만 저장하고 종료

    # 5. 결과를 Markdown 보고서로 구성하기
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    markdown_content = f"""# 📊 DCO 로그 분석 보고서 (DCO Log Analysis Report)

이 보고서는 교육용 샘플 DCO 로그 파일(`{input_path}`)을 분석하여 파이썬 스크립트로 자동 생성된 결과입니다.

## 📈 1. 전체 통계
* **분석된 총 로그 라인 수:** {total_lines}개

---

## ⚠️ 2. 심각도별 로그 분포 (Severity Distribution)
시스템의 긴급 수준과 안정성을 판단하기 위한 심각도 분포 통계입니다.

| 심각도 (Severity) | 로그 수 (Count) | 진단 상태 및 비고 |
| :--- | :---: | :--- |
"""
    # 심각도를 보기 좋게 정렬하여 표에 채웁니다.
    for sev in sorted(severity_counts.keys()):
        count = severity_counts[sev]
        note = "정상 동작 상태 로그"
        if sev == 'CRITICAL':
            note = "🚨 즉각적인 확인 및 해결 필요 (인시던트)"
        elif sev == 'WARNING':
            note = "⚠️ 이상 징후 감지 (사전 예방 조치 필요)"
        markdown_content += f"| {sev} | {count} | {note} |\n"

    markdown_content += f"""
---

## 🔍 3. 이벤트별 발생 빈도 (Event Frequency)
네트워크 장비 및 호스트에서 감지된 이벤트 종류별 빈도 통계입니다.

| 이벤트명 (Event Name) | 발생 횟수 (Count) |
| :--- | :---: |
"""
    # 발생 빈도가 높은 순서대로 이벤트를 정렬합니다.
    for evt, count in sorted(event_counts.items(), key=lambda x: x[1], reverse=True):
        markdown_content += f"| {evt} | {count} |\n"

    markdown_content += f"""
---

## 🚨 4. 경고 및 심각 로그 목록 (WARNING & CRITICAL Logs)
장애 파악을 위해 즉각 조치가 요구되는 경보 수준의 원본 로그 상세 내역입니다.

| 발생 일시 (Timestamp) | 장비명 (Device) | 심각도 | 이벤트명 | 상세 메시지 (Message) |
| :--- | :--- | :---: | :--- | :--- |
"""
    if warning_or_critical:
        for log in warning_or_critical:
            markdown_content += f"| {log['timestamp']} | {log['device']} | `{log['severity']}` | {log['event']} | {log['message']} |\n"
    else:
        markdown_content += "| - | - | - | - | 감지된 WARNING 또는 CRITICAL 등급의 로그가 없습니다. |\n"

    markdown_content += f"""
---

## 🎯 5. 장애 핵심 감지 요약 (CRC_ERROR, LINK_DOWN, TICKET_ESCALATED)
물리적인 에러(`CRC_ERROR`), 링크 단절(`LINK_DOWN`), 상위 에스컬레이션(`TICKET_ESCALATED`) 등 DCO에서 매우 중요하게 모니터링하는 핵심 이벤트 요약입니다.

| 감지 유형 | 발생 일시 (Timestamp) | 장비명 (Device) | 심각도 | 이벤트명 | 탐지 메시지 |
| :---: | :--- | :--- | :---: | :--- | :--- |
"""
    if major_events:
        for log in major_events:
            markdown_content += f"| `{log['keyword']}` | {log['timestamp']} | {log['device']} | `{log['severity']}` | {log['event']} | {log['message']} |\n"
    else:
        markdown_content += "| - | - | - | - | - | 핵심 감지 키워드가 포함된 이벤트가 발견되지 않았습니다. |\n"

    markdown_content += f"""
---
* **보고서 생성 시각:** {now_str} (KST)
* *본 보고서는 인턴십 직무 이해를 돕기 위한 교육용 시뮬레이션 결과로 실제 인프라의 실제 동작 데이터가 아닙니다.*
"""

    # 지정된 경로에 결과를 저장합니다 (UTF-8 인코딩)
    with open(output_path, 'w', encoding='utf-8') as out_file:
        out_file.write(markdown_content)
        
    print(f"[성공] 분석 결과가 성공적으로 저장되었습니다 -> {output_path}")

# 스크립트를 직접 실행했을 때만 분석을 구동합니다.
if __name__ == "__main__":
    INPUT_FILE = "sample_dco_log.txt"
    OUTPUT_FILE = "07_log_analysis_script/incident_summary.md"
    
    analyze_logs(INPUT_FILE, OUTPUT_FILE)
