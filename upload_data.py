"""data_raw/data_attendance.csv 를 Supabase `attendance` 테이블에 업로드합니다. (외부 패키지 불필요)

사용법 (PowerShell):
  $env:SUPABASE_URL = "https://xxxx.supabase.co"
  $env:SUPABASE_SERVICE_KEY = "service_role 키"   # 업로드 전용. index.html/깃허브에 절대 넣지 마세요
  python upload_data.py
"""
import csv, json, os, sys, urllib.request, urllib.error

URL = os.environ.get("SUPABASE_URL", "").rstrip("/")
KEY = os.environ.get("SUPABASE_SERVICE_KEY", "")
CSV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data_raw", "data_attendance.csv")

if not URL or not KEY:
    sys.exit("SUPABASE_URL 과 SUPABASE_SERVICE_KEY 환경변수를 먼저 설정하세요.")

def pad(t):  # 8:53:37 -> 08:53:37
    h, m, s = t.split(":")
    return f"{int(h):02d}:{m}:{s}"

with open(CSV_PATH, encoding="utf-8-sig", newline="") as f:
    rows = list(csv.DictReader(f))
for r in rows:
    r["tag_time"] = pad(r["tag_time"])

req = urllib.request.Request(
    f"{URL}/rest/v1/attendance?on_conflict=log_id",
    data=json.dumps(rows).encode("utf-8"),
    method="POST",
    headers={
        "apikey": KEY, "Authorization": f"Bearer {KEY}",
        "Content-Type": "application/json",
        "Prefer": "resolution=merge-duplicates,return=minimal",  # 재실행해도 중복 없이 갱신
    },
)
try:
    urllib.request.urlopen(req)
    print(f"완료: {len(rows)}건 업로드")
except urllib.error.HTTPError as e:
    sys.exit(f"실패 {e.code}: {e.read().decode('utf-8', 'replace')}")
