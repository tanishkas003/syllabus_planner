from notion_client import Client

def push_to_notion(plan, notion_api_key):
    client = Client(auth=notion_api_key)
    page = client.pages.create(parent={"type":"page_id","page_id": "REPLACE_ME"},
                               properties={
                                   "title":[{"text":{"content": f"Study Plan: {plan.get('course_title')}"}}]
                               })
    return page
