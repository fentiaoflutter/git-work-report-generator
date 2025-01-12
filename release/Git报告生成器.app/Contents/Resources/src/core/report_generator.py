from jinja2 import Template
import pandas as pd

class ReportGenerator:
    def generate(self, commits_df, report_type, start_date, end_date):
        if report_type == "简介":
            return self._generate_brief(commits_df, start_date, end_date)
        elif report_type == "详细":
            return self._generate_detailed(commits_df, start_date, end_date)
        else:
            return self._generate_very_detailed(commits_df, start_date, end_date)
    
    def _generate_brief(self, commits_df, start_date, end_date):
        summary = {
            'total_commits': len(commits_df),
            'total_changes': commits_df['total_changes'].sum(),
            'active_days': len(commits_df['date'].dt.date.unique()),
            'authors': commits_df['author'].unique().tolist()
        }
        
        template = Template('''
        <html>
            <head>
                <title>Git提交记录简报</title>
                <style>
                    body { font-family: Arial, sans-serif; }
                    .summary { margin: 20px; }
                </style>
            </head>
            <body>
                <h1>Git提交记录简报</h1>
                <div class="summary">
                    <p>报告期间: {{start_date}} 至 {{end_date}}</p>
                    <p>总提交次数: {{summary.total_commits}}</p>
                    <p>代码变更行数: {{summary.total_changes}}</p>
                    <p>活跃工作天数: {{summary.active_days}}</p>
                    <p>参与开发人员: {{summary.authors|join(', ')}}</p>
                </div>
            </body>
        </html>
        ''')
        
        return template.render(
            summary=summary,
            start_date=start_date,
            end_date=end_date
        ) 