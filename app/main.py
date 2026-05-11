from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
import markdown
import os
import sqlite3
from pathlib import Path

# ── 路径解析 ──
HERE = Path(__file__).resolve().parent          # app/
PROJECT_ROOT = HERE.parent                      # mysite（项目根目录）

# 内容目录：环境变量优先，未设则默认 <项目根>/个人知识网站
KNOWLEDGE_BASE_DIR = Path(
    os.getenv("KNOWLEDGE_BASE_DIR", PROJECT_ROOT / "个人知识网站")
)

# 模板目录：始终相对于项目根
TEMPLATES_DIR = PROJECT_ROOT / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

# 数据库路径：环境变量可覆盖
DB_PATH = os.getenv("COMMENTS_DB_PATH", str(PROJECT_ROOT / "comments.db"))

app = FastAPI()


# ── 留言板数据库 ──

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            page_path TEXT,
            username TEXT,
            content TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

init_db()


# ── 目录树（支持嵌套子目录）──

def slug_display(slug: str) -> str:
    """将文件 slug 转为显示名"""
    # 去掉数字前缀（01-xx → xx）
    if len(slug) > 2 and slug[:2].isdigit() and slug[2:3] in ('', '-'):
        return slug[3:] if slug[2:3] == '-' else slug
    return slug


def get_directory_tree(base_dir):
    """递归构建导航树，支持多级子目录"""
    tree = []
    for item in sorted(os.listdir(base_dir)):
        item_path = base_dir / item
        if not item_path.is_dir():
            continue

        # 本级 .md 文件
        raw_files = sorted([
            f.name.replace('.md', '')
            for f in item_path.glob("*.md")
        ])
        files = [{"slug": f, "display": slug_display(f)} for f in raw_files]

        # 子目录（嵌套层级）
        children = []
        for sub in sorted(os.listdir(item_path)):
            sub_path = item_path / sub
            if sub_path.is_dir():
                raw_nested = sorted([
                    f.name.replace('.md', '')
                    for f in sub_path.glob("*.md")
                ])
                if raw_nested:
                    children.append({
                        "name": sub,
                        "files": [{"slug": f, "display": slug_display(f)} for f in raw_nested]
                    })

        entry = {"name": item, "files": files}
        if children:
            entry["children"] = children
        tree.append(entry)

    return tree


# ── JSON 导航 API（供前端动态渲染）──

@app.get("/api/nav", response_class=JSONResponse)
async def nav_api():
    return get_directory_tree(KNOWLEDGE_BASE_DIR)


# ── JSON 内容 API（供前端 SPA 过渡导航）──

@app.get("/api/content/{path:path}")
async def api_content(path: str):
    target_md = path if path.endswith(".md") else path + ".md"
    target_file = KNOWLEDGE_BASE_DIR / target_md

    if not target_file.exists() or not target_file.is_file():
        return JSONResponse({"error": "not found"}, status_code=404)

    md_text = target_file.read_text(encoding="utf-8")
    title = extract_title(md_text, target_md)
    html = render_markdown(md_text)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT username, content, timestamp FROM comments WHERE page_path=? ORDER BY timestamp DESC",
        (target_md,),
    )
    comments = [
        {"username": r[0], "content": r[1], "timestamp": r[2]}
        for r in cursor.fetchall()
    ]
    conn.close()

    section_index = -1
    dirs = sorted(d for d in KNOWLEDGE_BASE_DIR.iterdir() if d.is_dir())
    for i, child in enumerate(dirs):
        if str(target_file).startswith(str(child)):
            section_index = i
            break

    return {"title": title, "html": html, "comments": comments, "section_index": section_index}


# ── 从 Markdown 提取标题 ──

def extract_title(md_text: str, fallback: str) -> str:
    for line in md_text.strip().split("\n"):
        line = line.strip()
        if line.startswith("# "):
            return line[2:].strip()
    stem = Path(fallback).stem
    if "-" in stem:
        return stem.split("-", 1)[1]
    return stem


# ── Markdown → HTML ──

def render_markdown(md_text: str) -> str:
    return markdown.markdown(
        md_text,
        extensions=[
            "extra",           # 表格、脚注、定义列表
            "codehilite",      # 代码高亮
            "toc",             # 目录
            "md_in_html",      # HTML 内部解析 Markdown
        ],
    )


# ── 核心路由 ──

@app.get("/", response_class=HTMLResponse)
@app.get("/{file_path:path}", response_class=HTMLResponse)
async def read_page(request: Request, file_path: str = ""):
    nav_tree = get_directory_tree(KNOWLEDGE_BASE_DIR)

    if not file_path:
        # 首页 → 显示 Landing Page
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "content": "",
                "nav_tree": nav_tree,
                "current_path": "",
                "comments": [],
                "page_title": "鸿勋",
            },
        )

    # 内容页
    target_md = file_path
    if not target_md.endswith(".md"):
        target_md += ".md"

    target_file = KNOWLEDGE_BASE_DIR / target_md
    page_exists = target_file.exists() and target_file.is_file()

    if page_exists:
        md_text = target_file.read_text(encoding="utf-8")
        page_title = extract_title(md_text, target_md)
        content_html = render_markdown(md_text)
    else:
        content_html = '<div class="not-found"><h1>404</h1><p>页面未找到</p></div>'
        page_title = "404"

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT username, content, timestamp FROM comments WHERE page_path=? ORDER BY timestamp DESC",
        (target_md,),
    )
    comments = cursor.fetchall()
    conn.close()

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "content": content_html,
            "nav_tree": nav_tree,
            "current_path": target_md,
            "comments": comments,
            "page_title": page_title,
        },
    )


# ── 提交留言 ──

@app.post("/submit_comment")
async def submit_comment(
    page_path: str = Form(...),
    username: str = Form(...),
    content: str = Form(...),
):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO comments (page_path, username, content) VALUES (?, ?, ?)",
        (page_path, username, content),
    )
    conn.commit()
    conn.close()
    return HTMLResponse(f"<script>location.href='/{page_path}'</script>")
