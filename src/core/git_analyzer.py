from git import Repo
from datetime import datetime
import pandas as pd
import os
from collections import defaultdict
import re
import json
from translate import Translator
import time

class GitAnalyzer:
    def __init__(self, repo_path):
        self.repo = Repo(repo_path)
        # 初始化翻译器
        self.translator = Translator(to_lang="zh", from_lang="en")
        # 扩展英文词汇翻译对照表
        self.translation_dict = {
            # 动词
            'add': '添加',
            'update': '更新',
            'fix': '修复',
            'remove': '移除',
            'delete': '删除',
            'change': '修改',
            'improve': '改进',
            'implement': '实现',
            'refactor': '重构',
            'optimize': '优化',
            'clean': '清理',
            'rename': '重命名',
            'replace': '替换',
            'support': '支持',
            'upgrade': '升级',
            'modify': '修改',
            'enhance': '增强',
            'revise': '修订',
            'create': '创建',
            
            # 名词
            'bug': '缺陷',
            'feature': '功能',
            'code': '代码',
            'test': '测试',
            'docs': '文档',
            'documentation': '文档',
            'config': '配置',
            'style': '样式',
            'format': '格式',
            'performance': '性能',
            'security': '安全性',
            'error': '错误',
            'warning': '警告',
            'issue': '问题',
            'dependency': '依赖',
            'interface': '接口',
            'function': '函数',
            'module': '模块',
            'component': '组件',
            'package': '包',
            'library': '库',
            'service': '服务',
            'api': 'API',
            'database': '数据库',
            'data': '数据',
            'file': '文件',
            'directory': '目录',
            'path': '路径',
            'version': '版本',
            'release': '发布',
            'build': '构建',
            'deploy': '部署',
            
            # 形容词
            'new': '新的',
            'old': '旧的',
            'better': '更好的',
            'faster': '更快的',
            'smaller': '更小的',
            'larger': '更大的',
            'unused': '未使用的',
            'deprecated': '已废弃的',
            'invalid': '无效的',
            'missing': '缺失的',
            'broken': '损坏的',
            'unnecessary': '不必要的',
            'redundant': '冗余的',
            
            # 常见短语
            'initial commit': '初始提交',
            'first commit': '首次提交',
            'minor changes': '小改动',
            'minor fixes': '小修复',
            'code review': '代码审查',
            'pull request': '拉取请求',
            'merge conflict': '合并冲突',
            'unit test': '单元测试',
            'integration test': '集成测试',
            'bug fix': '缺陷修复',
            'hot fix': '紧急修复',
            'quick fix': '快速修复',
            'temp fix': '临时修复',
            'workaround': '临时解决方案',
            'code cleanup': '代码清理',
            'code optimization': '代码优化',
            'performance improvement': '性能改进',
            'security patch': '安全补丁',
            'version bump': '版本升级',
            'dependency update': '依赖更新',
            
            # 补充更多常见的开发术语
            'init': '初始化',
            'initialize': '初始化',
            'setup': '设置',
            'configure': '配置',
            'integration': '集成',
            'integrate': '集成',
            'merge': '合并',
            'branch': '分支',
            'commit': '提交',
            'push': '推送',
            'pull': '拉取',
            'sync': '同步',
            'synchronize': '同步',
            'upload': '上传',
            'download': '下载',
            'install': '安装',
            'uninstall': '卸载',
            'export': '导出',
            'import': '导入',
            'generate': '生成',
            'parse': '解析',
            'process': '处理',
            'validate': '验证',
            'verify': '验证',
            'check': '检查',
            'review': '审查',
            'test': '测试',
            'debug': '调试',
            'log': '日志',
            'cache': '缓存',
            'backup': '备份',
            'restore': '恢复',
            'save': '保存',
            'load': '加载',
            'start': '启动',
            'stop': '停止',
            'restart': '重启',
            'pause': '暂停',
            'resume': '恢复',
            'cancel': '取消',
            'abort': '中止',
            'complete': '完成',
            'finish': '完成',
            'success': '成功',
            'fail': '失败',
            'error': '错误',
            'warning': '警告',
            'info': '信息',
            'debug': '调试',
            'trace': '追踪',
            
            # 补充项目相关术语
            'project': '项目',
            'repository': '仓库',
            'workspace': '工作区',
            'development': '开发',
            'production': '生产',
            'staging': '预发布',
            'testing': '测试',
            'alpha': '内测版',
            'beta': '公测版',
            'release': '发布版',
            'stable': '稳定版',
            'unstable': '不稳定版',
            'experimental': '实验性',
            
            # 补充常见动作
            'move': '移动',
            'copy': '复制',
            'paste': '粘贴',
            'cut': '剪切',
            'edit': '编辑',
            'modify': '修改',
            'delete': '删除',
            'insert': '插入',
            'append': '追加',
            'prepend': '前置',
            'sort': '排序',
            'filter': '过滤',
            'search': '搜索',
            'find': '查找',
            'replace': '替换',
            
            # 补充常见状态
            'enabled': '已启用',
            'disabled': '已禁用',
            'active': '活动的',
            'inactive': '非活动的',
            'available': '可用的',
            'unavailable': '不可用的',
            'valid': '有效的',
            'invalid': '无效的',
            'deprecated': '已废弃的',
            'obsolete': '已过时的',
            
            # 补充常见描述词
            'successfully': '成功地',
            'failed': '失败的',
            'completed': '已完成',
            'pending': '待处理',
            'processing': '处理中',
            'updating': '更新中',
            'creating': '创建中',
            'deleting': '删除中',
            'loading': '加载中',
            'saving': '保存中',
        }
    
    def _translate_text(self, text):
        """将英文文本翻译成中文"""
        if not text:
            return text
            
        # 先使用本地词典进行翻译
        result = text
        text_lower = text.lower()
        
        # 处理本地词典中的短语和单词
        # ... 保持原有的本地词典翻译逻辑 ...
        
        # 对剩余的英文内容使用翻译API
        # 分割文本为句子，避免过长
        sentences = result.split('. ')
        translated_sentences = []
        
        for sentence in sentences:
            # 检查是否还有未翻译的英文内容
            if any(c.isascii() and c.isalpha() for c in sentence):
                try:
                    # 添加延时避免请求过快
                    time.sleep(0.5)
                    translated = self.translator.translate(sentence)
                    translated_sentences.append(translated)
                except Exception as e:
                    # 如果翻译失败，保留原文
                    translated_sentences.append(sentence)
            else:
                translated_sentences.append(sentence)
        
        return '. '.join(translated_sentences)
    
    def get_all_authors(self):
        """获取仓库中的所有作者"""
        authors = set()
        for commit in self.repo.iter_commits():
            authors.add(commit.author.name)
        return sorted(list(authors))
    
    def analyze_code_changes(self, commit):
        """分析代码变更的具体内容"""
        code_changes = []
        try:
            # 处理第一次提交的情况
            parent = commit.parents[0] if commit.parents else None
            
            # 获取差异
            for diff in commit.diff(parent):
                try:
                    # 分析变更类型
                    if diff.new_file:
                        change_type = "新增文件"
                        old_content = ""
                        try:
                            new_content = diff.b_blob.data_stream.read().decode('utf-8', errors='ignore')
                        except:
                            new_content = ""
                    elif diff.deleted_file:
                        change_type = "删除文件"
                        try:
                            old_content = diff.a_blob.data_stream.read().decode('utf-8', errors='ignore')
                        except:
                            old_content = ""
                        new_content = ""
                    else:
                        change_type = "修改文件"
                        try:
                            old_content = diff.a_blob.data_stream.read().decode('utf-8', errors='ignore') if diff.a_blob else ""
                            new_content = diff.b_blob.data_stream.read().decode('utf-8', errors='ignore') if diff.b_blob else ""
                        except:
                            old_content = ""
                            new_content = ""
                    
                    # 计算变更行数
                    try:
                        diff_text = diff.diff.decode('utf-8', errors='ignore')
                        insertions = diff_text.count('\n+') - 1 if diff_text.startswith('+++') else diff_text.count('\n+')
                        deletions = diff_text.count('\n-') - 1 if diff_text.startswith('---') else diff_text.count('\n-')
                    except:
                        insertions = 0
                        deletions = 0
                    
                    # 记录变更信息
                    code_changes.append({
                        'file': diff.a_path or diff.b_path,
                        'type': change_type,
                        'old_content': old_content,
                        'new_content': new_content,
                        'insertions': insertions,
                        'deletions': deletions
                    })
                except Exception as e:
                    # 如果处理某个文件时出错，记录错误信息
                    code_changes.append({
                        'file': diff.a_path or diff.b_path,
                        'type': '处理出错',
                        'old_content': '',
                        'new_content': '',
                        'insertions': 0,
                        'deletions': 0,
                        'error': str(e)
                    })
        except Exception as e:
            # 如果整个提交处理出错，返回空的变更列表
            code_changes.append({
                'file': 'ERROR',
                'type': '处理出错',
                'old_content': '',
                'new_content': '',
                'insertions': 0,
                'deletions': 0,
                'error': str(e)
            })
        
        return code_changes
    
    def analyze_commit_message(self, message):
        """分析提交信息，提取关键信息并翻译"""
        # 先检查是否有feat标识
        if message.lower().startswith('feat') or 'feat:' in message.lower() or 'feat(' in message.lower():
            commit_type = '新功能'
        else:
            # 先进行完整的翻译
            translated_message = self._translate_text(message)
            
            # 根据关键词判断提交类型
            message_lower = translated_message.lower()
            
            # 新功能相关关键词（更精确的匹配）
            if any(keyword in message_lower for keyword in [
                '新增功能', '添加功能', '新功能', '实现功能', 
                '新增特性', '添加特性', '新特性',
                '功能开发', '新增模块', '添加模块',
                'new feature', 'add feature', 'implement feature'
            ]) or (
                # 以这些词开头的很可能是功能开发
                any(message_lower.startswith(keyword) for keyword in [
                    '新增', '添加', '实现', '开发', '创建'
                ]) and
                # 但要避免一些非功能开发的情况
                not any(keyword in message_lower for keyword in [
                    '修复', '优化', '重构', '文档', '注释', '配置',
                    '删除', '移除', '更新', '调整', '变更'
                ])
            ):
                commit_type = '新功能'
            
            # 修复相关关键词
            elif any(keyword in message_lower for keyword in [
                '修复', '解决', '修正', '处理', '问题', '错误', '缺陷',
                'fix', 'bug', 'issue', 'problem', 'error'
            ]):
                commit_type = '修复'
            
            # 重构相关关键词
            elif any(keyword in message_lower for keyword in [
                '重构', '优化', '改进', '提升', '重写', '调整',
                'refactor', 'optimize', 'improve', 'enhancement'
            ]):
                commit_type = '重构'
            
            # 文档相关关键词
            elif any(keyword in message_lower for keyword in [
                '文档', '注释', 'doc', 'docs', 'document', 'comment'
            ]):
                commit_type = '文档'
            
            # 默认为其他类型
            else:
                commit_type = '其他'
        
        # 翻译消息内容（如果还没翻译）
        if not locals().get('translated_message'):
            translated_message = self._translate_text(message)
        
        # 尝试提取范围信息
        scope = ''
        scope_match = re.search(r'\[(.*?)\]|\((.*?)\)', translated_message)
        if scope_match:
            scope = scope_match.group(1) or scope_match.group(2)
        
        # 清理描述文本，移除范围标记
        description = re.sub(r'\[(.*?)\]|\((.*?)\)', '', translated_message).strip()
        
        return {
            'type': commit_type,
            'scope': scope,
            'description': description
        }
    
    def analyze_commits(self, start_date, end_date, filters=None, progress_callback=None):
        """
        分析提交记录
        progress_callback: 进度回调函数，接收一个0-100的整数表示进度
        """
        commits_data = []
        summary_by_type = defaultdict(int)
        summary_by_author = defaultdict(lambda: defaultdict(int))
        
        # 定义要过滤的分支操作关键词
        branch_operations = {
            'merge', 'revert', 'branch', 'cherry-pick', 'rebase',
            'pull request', 'pr:', 'pr(', 'pr [', 
            'cherry pick', 'cherrypick',
            'rollback', 'roll back',
            'reset', 'restore'
        }
        
        # 先获取所有符合日期范围的提交数量
        total_commits = len(list(self.repo.iter_commits(
            since=start_date.strftime('%Y-%m-%d'),
            until=end_date.strftime('%Y-%m-%d')
        )))
        
        if progress_callback:
            progress_callback(5)
        
        processed_commits = 0
        
        for commit in self.repo.iter_commits():
            # 忽略分支操作相关的提交
            commit_msg_lower = commit.message.strip().lower()
            
            # 跳过以下情况：
            # 1. 合并提交（多个父提交）
            # 2. 包含分支操作关键词的提交
            # 3. 自动生成的合并提交信息
            if (len(commit.parents) > 1 or  # 合并提交
                any(op in commit_msg_lower for op in branch_operations) or  # 包含分支操作关键词
                commit_msg_lower.startswith(tuple(branch_operations)) or  # 以分支操作关键词开头
                'merged' in commit_msg_lower or  # 合并相关
                'reverted' in commit_msg_lower or  # 还原相关
                'pulled from' in commit_msg_lower or  # 拉取相关
                'rebased' in commit_msg_lower or  # 变基相关
                'cherry picked' in commit_msg_lower):  # Cherry-pick相关
                continue
            
            commit_date = datetime.fromtimestamp(commit.committed_date)
            
            if start_date <= commit_date.date() <= end_date:
                # 作者筛选
                if filters and filters['authors'] and \
                   commit.author.name not in filters['authors']:
                    continue
                
                # 分析代码变更
                code_changes = self.analyze_code_changes(commit)
                
                # 分析提交信息
                commit_analysis = self.analyze_commit_message(commit.message)
                
                # 如果提交信息以 'Merge' 开头，也跳过
                if commit.message.strip().lower().startswith('merge'):
                    continue
                
                # 统计信息
                summary_by_type[commit_analysis['type']] += 1
                summary_by_author[commit.author.name]['commits'] += 1
                
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
                
                total_changes = sum(d['lines'] for d in stats.values())
                summary_by_author[commit.author.name]['changes'] += total_changes
                
                commits_data.append({
                    'hash': commit.hexsha,
                    'author': commit.author.name,
                    'date': commit_date,
                    'message': commit.message,
                    'message_analysis': commit_analysis,
                    'files_changed': len(stats),
                    'total_changes': total_changes,
                    'stats': stats,
                    'code_changes': code_changes
                })
                
                processed_commits += 1
                if progress_callback:
                    # 计算进度（5-90%的范围）
                    progress = 5 + min(int((processed_commits / total_commits) * 85), 85)
                    progress_callback(progress)
        
        if progress_callback:
            progress_callback(90)  # 分析完成
        
        df = pd.DataFrame(commits_data)
        df.attrs['summary_by_type'] = dict(summary_by_type)
        df.attrs['summary_by_author'] = dict(summary_by_author)
        
        if progress_callback:
            progress_callback(95)  # 数据处理完成
        
        return df 