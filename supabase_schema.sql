-- Supabase SQL Editor 에서 실행하세요.
create table if not exists public.attendance (
  log_id      text primary key,          -- ATT-LOG-20260901-1001
  emp_id      text not null,             -- GBSA2018012
  emp_name    text not null,
  dept_name   text not null,
  tag_date    date not null,
  tag_time    time not null,
  event_type  text not null check (event_type in ('CHECK_IN','CHECK_OUT')),
  gate_name   text,
  device_id   text,
  auth_method text,
  raw_status  text,
  ip_address  text
);
create index if not exists attendance_emp_date_idx on public.attendance (emp_id, tag_date);

-- 프론트엔드(anon 키)가 읽을 수 있도록 읽기 전용 정책 추가
alter table public.attendance enable row level security;
create policy "anon can read attendance" on public.attendance for select to anon using (true);
