from jinja2 import Template
from weasyprint import HTML
from datetime import datetime

PDF_TEMPLATE = """
<html>
  <head>
    <style>
      body { font-family: Arial, sans-serif; padding: 20px; }
      .week { border: 1px solid #ddd; padding: 10px; margin-bottom: 12px; border-radius: 8px; }
      .topic { margin-left: 8px; }
      header { text-align: center; margin-bottom: 16px; }
    </style>
  </head>
  <body>
    <header>
      <h1>{{course_title}}</h1>
      <p>Generated: {{generated_at}}</p>
    </header>
    {% for idx, week in enumerate(weeks, start=1) %}
      <div class="week">
        <h3>Week {{idx}} - {{week.date_range if week.date_range else ""}}</h3>
        <p>Estimated hours left: {{week.remaining}}</p>
        <ul>
        {% for t in week.topics %}
          <li class="topic">
            <strong>{{t.title}}</strong> — {{t.est_hours}} hrs
            <div>{{t.objective}}</div>
          </li>
        {% endfor %}
        </ul>
      </div>
    {% endfor %}
  </body>
</html>
"""

def generate_pdf(plan: dict, filename="study_plan.pdf"):
    tpl = Template(PDF_TEMPLATE)
    html = tpl.render(course_title=plan.get("course_title","Study Plan"),
                      weeks=plan.get("weeks",[]),
                      generated_at=datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"))
    HTML(string=html).write_pdf(filename)
    return filename
