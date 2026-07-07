import os
import glob

def count_errors_in_logs():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    workspace_dir = os.path.dirname(script_dir)
    
    # 워크스페이스 폴더 전체에서 server*.log 재귀 탐색
    log_files = []
    pattern = os.path.join(workspace_dir, "**", "server*.log")
    found = glob.glob(pattern, recursive=True)
    
    for f in found:
        abs_f = os.path.abspath(f)
        if abs_f not in log_files and os.path.isfile(abs_f):
            log_files.append(abs_f)
            
    if not log_files:
        print("No server*.log files found in search directories.")
        return

    print(f"Analyzing {len(log_files)} log files with multi-line support...")
    
    results = {}
    for filepath in sorted(log_files):
        filename = os.path.basename(filepath)
        crc_count = 0
        link_down_count = 0
        
        try:
            entries = []
            current_entry = []
            
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    line_str = line.rstrip('\r\n')
                    if not line_str:
                        continue
                    
                    # 들여쓰기 공백으로 시작하는 줄은 이전 로그 엔트리에 속함
                    if line_str.startswith(' ') or line_str.startswith('\t'):
                        if current_entry:
                            current_entry.append(line_str)
                        else:
                            current_entry = [line_str]
                    else:
                        # 새로운 로그 엔트리 시작
                        if current_entry:
                            entries.append('\n'.join(current_entry))
                        current_entry = [line_str]
                        
                if current_entry:
                    entries.append('\n'.join(current_entry))
            
            # 로그 엔트리별로 검색
            for entry in entries:
                first_line = entry.split('\n')[0] if entry else ""
                
                # 첫 줄에 대문자 'ERROR' 레벨이 포함된 경우에만 집계
                if 'ERROR' in first_line:
                    lower_entry = entry.lower()
                    
                    # CRC error 체크 (대소문자 구분 없이 'crc' 포함 여부)
                    if 'crc' in lower_entry:
                        crc_count += 1
                        
                    # Link Down 체크 (대소문자 구분 없이 'link'와 'down'이 모두 포함된 여부)
                    if 'link' in lower_entry and 'down' in lower_entry:
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
    
    total_crc = 0
    total_link_down = 0
    for filename, counts in results.items():
        print(f"{filename:<20} | {counts['crc_error']:<15} | {counts['link_down']:<15}")
        total_crc += counts['crc_error']
        total_link_down += counts['link_down']
        
    print("-" * 56)
    print(f"{'Total':<20} | {total_crc:<15} | {total_link_down:<15}")

if __name__ == "__main__":
    count_errors_in_logs()
