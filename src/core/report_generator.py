from jinja2 import Template
import pandas as pd
from datetime import datetime
from collections import defaultdict
import os
import tempfile
import webbrowser

class ReportGenerator:
    def __init__(self):
        pass

    def _summarize_work_content(self, commits):
        """根据提交记录生成工作内容总结"""
        work_summary = defaultdict(list)
        
        for commit in commits:
            commit_type = commit['message_analysis']['type']
            description = commit['message_analysis']['description']
            scope = commit['message_analysis']['scope']
            
            # 根据不同类型生成不同的描述
            if commit_type == '新功能':
                work_summary['功能开发'].append({
                    'description': description,
                    'scope': scope,
                    'changes': commit['code_changes']
                })
            elif commit_type == '修复':
                work_summary['问题修复'].append({
                    'description': description,
                    'scope': scope,
                    'changes': commit['code_changes']
                })
            elif commit_type == '重构':
                work_summary['代码优化'].append({
                    'description': description,
                    'scope': scope,
                    'changes': commit['code_changes']
                })
            elif commit_type == '文档':
                work_summary['文档完善'].append({
                    'description': description,
                    'scope': scope,
                    'changes': commit['code_changes']
                })
            else:
                work_summary['其他工作'].append({
                    'description': description,
                    'scope': scope,
                    'changes': commit['code_changes']
                })
        
        return work_summary

    def _save_and_open_report(self, html_content):
        """保存报告并自动打开"""
        with tempfile.NamedTemporaryFile(delete=False, suffix='.html', mode='w', encoding='utf-8') as f:
            f.write(html_content)
            temp_path = f.name
        
        webbrowser.open('file://' + temp_path)
        return temp_path

    def generate(self, commits_df, report_type, start_date, end_date, filters=None):
        """生成工作报告"""
        work_summary = self._summarize_work_content(commits_df.to_dict('records'))
        
        if report_type == "简单":
            html_content = self._generate_brief(work_summary, start_date, end_date)
        elif report_type == "中等":
            html_content = self._generate_detailed(work_summary, start_date, end_date)
        else:
            html_content = self._generate_very_detailed(work_summary, start_date, end_date)
        
        return self._save_and_open_report(html_content)

    def _generate_brief(self, work_summary, start_date, end_date):
        template = Template('''
        <html>
            <head>
                <title>工作总结报告</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 20px; line-height: 1.6; }
                    .summary { margin: 20px; padding: 20px; border: 1px solid #ddd; border-radius: 5px; }
                    h1, h2 { color: #333; }
                    .work-item { margin: 10px 0; }
                    .period { color: #666; }
                </style>
            </head>
            <body>
                <h1>工作总结报告</h1>
                <p class="period">总结期间：{{start_date}} 至 {{end_date}}</p>

                <div class="summary">
                    <h2>工作内容统计</h2>
                    <p>功能开发项目：{{work_summary['功能开发']|length}} 项</p>
                    <p>问题修复工作：{{work_summary['问题修复']|length}} 项</p>
                    <p>系统优化工作：{{work_summary['代码优化']|length}} 项</p>
                    <p>文档完善工作：{{work_summary['文档完善']|length}} 项</p>
                    <p>其他工作事项：{{work_summary['其他工作']|length}} 项</p>
                </div>
            </body>
        </html>
        ''')
        
        return template.render(
            work_summary=work_summary,
            start_date=start_date,
            end_date=end_date
        )

    def _generate_detailed(self, work_summary, start_date, end_date):
        template = Template('''
        <html>
            <head>
                <title>工作总结报告</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 20px; line-height: 1.6; }
                    .summary { margin: 20px; padding: 20px; border: 1px solid #ddd; border-radius: 5px; }
                    .work-section { margin: 15px 0; }
                    .work-item { 
                        margin: 10px 0; 
                        padding: 15px; 
                        background: #f8f9fa;
                        border-radius: 5px;
                        border-left: 4px solid #28a745;
                    }
                    .details { margin-left: 20px; font-size: 0.9em; color: #666; }
                    h1, h2, h3 { color: #333; }
                    .period { color: #666; }
                    .stats { 
                        margin: 20px 0; 
                        padding: 20px;
                        background: #f8f9fa;
                        border-radius: 5px;
                        border-left: 4px solid #17a2b8;
                    }
                </style>
            </head>
            <body>
                <h1>工作总结报告</h1>
                <p class="period">总结期间：{{start_date}} 至 {{end_date}}</p>

                <div class="stats">
                    <h2>工作量统计</h2>
                    <p>功能开发项目：{{work_summary['功能开发']|length}} 项</p>
                    <p>问题修复工作：{{work_summary['问题修复']|length}} 项</p>
                    <p>系统优化工作：{{work_summary['代码优化']|length}} 项</p>
                    <p>文档完善工作：{{work_summary['文档完善']|length}} 项</p>
                    <p>其他工作事项：{{work_summary['其他工作']|length}} 项</p>
                </div>

                <div class="summary">
                    <h2>工作内容详述</h2>
                    {% for category, items in work_summary.items() %}
                    {% if items %}
                    <div class="work-section">
                        <h3>{{category}}</h3>
                        {% for item in items %}
                        <div class="work-item">
                            <h4>{% if item.scope %}【{{item.scope}}】{% endif %}{{item.description}}</h4>
                        </div>
                        {% endfor %}
                    </div>
                    {% endif %}
                    {% endfor %}
                </div>
            </body>
        </html>
        ''')
        
        return template.render(
            work_summary=work_summary,
            start_date=start_date,
            end_date=end_date
        )

    def _generate_very_detailed(self, work_summary, start_date, end_date):
        template = Template('''
        <html>
            <head>
                <title>工作总结报告</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 20px; line-height: 1.6; }
                    .summary { margin: 20px; padding: 20px; border: 1px solid #ddd; border-radius: 5px; }
                    .work-section { margin: 15px 0; }
                    .work-item { 
                        margin: 10px 0; 
                        padding: 15px; 
                        background: #f8f9fa;
                        border-radius: 5px;
                        border-left: 4px solid #28a745;
                    }
                    .details { margin-left: 20px; font-size: 0.9em; color: #666; }
                    h1, h2, h3 { color: #333; }
                    .period { color: #666; }
                    .stats { 
                        margin: 20px 0; 
                        padding: 20px;
                        background: #f8f9fa;
                        border-radius: 5px;
                        border-left: 4px solid #17a2b8;
                    }
                    .impact { 
                        color: #444; 
                        font-style: italic; 
                        margin-top: 10px;
                        padding: 10px;
                        background: #e9ecef;
                        border-radius: 3px;
                    }
                </style>
            </head>
            <body>
                <h1>工作总结报告</h1>
                <p class="period">总结期间：{{start_date}} 至 {{end_date}}</p>

                <div class="stats">
                    <h2>工作量统计</h2>
                    <p>功能开发项目：{{work_summary['功能开发']|length}} 项</p>
                    <p>问题修复工作：{{work_summary['问题修复']|length}} 项</p>
                    <p>系统优化工作：{{work_summary['代码优化']|length}} 项</p>
                    <p>文档完善工作：{{work_summary['文档完善']|length}} 项</p>
                    <p>其他工作事项：{{work_summary['其他工作']|length}} 项</p>
                </div>

                <div class="summary">
                    <h2>工作内容详述</h2>
                    {% for category, items in work_summary.items() %}
                    {% if items %}
                    <div class="work-section">
                        <h3>{{category}}</h3>
                        {% for item in items %}
                        <div class="work-item">
                            <h4>{% if item.scope %}【{{item.scope}}】{% endif %}{{item.description}}</h4>
                            <div class="details">
                                <p>工作内容：</p>
                                <ul>
                                {% for change in item.changes %}
                                    <li>完成{{change.type}}的相关工作</li>
                                {% endfor %}
                                </ul>
                                <p class="impact">工作影响：该项工作的完成提升了系统的整体性能和用户体验，为后续功能开发奠定了基础。</p>
                            </div>
                        </div>
                        {% endfor %}
                    </div>
                    {% endif %}
                    {% endfor %}
                </div>
            </body>
        </html>
        ''')
        
        return template.render(
            work_summary=work_summary,
            start_date=start_date,
            end_date=end_date
        ) 