from git import Repo
from datetime import datetime
import pandas as pd
import os

class GitAnalyzer:
    def __init__(self, repo_path):
        self.repo = Repo(repo_path)
        
    def analyze_commits(self, start_date, end_date, filters=None):
        commits_data = []
        
        for commit in self.repo.iter_commits():
            commit_date = datetime.fromtimestamp(commit.committed_date)
            
            if start_date <= commit_date.date() <= end_date:
                # 作者筛选
                if filters and filters['author'] and \
                   filters['author'].lower() not in commit.author.name.lower():
                    continue
                    
                # 获取提交的文件变更
                stats = commit.stats.files
                
                # 文件类型筛选
                if filters and filters['file_types']:
                    stats = {
                        f: s for f, s in stats.items()
                        if any(f.endswith(ft) for ft in filters['file_types'])
                    }
                    if not stats:  # 如果没有匹配的文件，跳过这个提交
                        continue
                
                # 忽略文件筛选
                if filters and filters['ignore_files']:
                    stats = {
                        f: s for f, s in stats.items()
                        if not any(
                            ignore in f 
                            for ignore in filters['ignore_files']
                        )
                    }
                
                total_changes = sum(
                    d['lines'] for d in stats.values()
                )
                
                commits_data.append({
                    'hash': commit.hexsha,
                    'author': commit.author.name,
                    'date': commit_date,
                    'message': commit.message,
                    'files_changed': len(stats),
                    'total_changes': total_changes,
                    'stats': stats
                })
                
        return pd.DataFrame(commits_data) 