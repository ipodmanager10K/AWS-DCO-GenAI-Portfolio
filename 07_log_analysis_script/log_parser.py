import os
import glob

def count_errors_in_logs():
    # 현재 스크립트 위치 및 워크스페이스 상위 디렉토리 등을 기준으로 server*.log 탐색
    script_dir = os.path.dirname(os.path.abspath(__file__))
    workspace_dir = os.path.dirname(script_dir)
    
    # 탐색할 디렉토리 목록
    search_dirs = [
        script_dir,
        os.path.join(workspace_dir, "07_log_analysis_script - 복사본"),
        workspace_dir
    ]
    
    log_files = []
    for d in search_dirs:
        if os.path.exists(d):
            found = glob.glob(os.path.join(d, "server*.log"))
            for f in found:
                abs_f = os.path.abspath(f)
                if abs_f not in log_files:
                    log_files.append(abs_f)
                    
    if not log_files:
        print("No server*.log files found in search directories.")
        return

    print(f"Analyzing {len(log_files)} log files...")
    
    results = {}
    for filepath in sorted(log_files):
        filename = os.path.basename(filepath)
        crc_count = 0
        link_down_count = 0
        
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    lower_line = line.lower()
                    if "crc error" in lower_line:
                        crc_count += 1
                    if "link down" in lower_line:
                        link_down_count += 1
                        
            results[filename] = {
                "crc_error": crc_count,
                "link_down": link_down_count
            }
        except Exception as e:
            print(f"Error reading {filename}: {e}")
            
    # 결과 출력
    print("\n[Log Analysis Results]")
    print(f"{'Server Log File':<20} | {'CRC Error Count':<15} | {'Link Down Count':<15}")
    print("-" * 56)
    for filename, counts in results.items():
        print(f"{filename:<20} | {counts['crc_error']:<15} | {counts['link_down']:<15}")

if __name__ == "__main__":
    count_errors_in_logs()
