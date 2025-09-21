def build_events_from_plan(plan):
    events = []
    for i, week in enumerate(plan.get("weeks", []), start=1):
        for t in week.get("topics", []):
            events.append({
                "summary": f"Study: {t['title']}",
                "description": f"{t.get('objective','')}\nResources: {', '.join([r.get('title','') for r in t.get('resources',[])])}",
                "start": {"date": week.get("start_date") or "2025-01-01"},
                "end": {"date": week.get("end_date") or "2025-01-02"},
            })
    return events

def push_events(events, google_credentials):
    print("Would push these events to Google Calendar:")
    for e in events[:5]:
        print(e)
    return []
