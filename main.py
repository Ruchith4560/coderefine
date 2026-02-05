
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class CodeRequest(BaseModel):
    code: str
    language: str

@app.get("/")
def home():
    return {"message": "Backend running successfully 🚀"}
def detect_logic_issues(code: str):
    issues = []

    # Shadowing built-in functions
    builtins = ["min", "max", "sum", "list", "dict"]
    for name in builtins:
        if f"{name} =" in code:
            issues.append(
                f"Variable '{name}' shadows Python built-in function '{name}()'"
            )

    # Manual min/max implementation
    if "for" in code and "<" in code and "min(" not in code:
        issues.append(
            "Manual loop used to find minimum. Built-in min() is more efficient."
        )

    return issues

import ast

@app.post("/analyze")
def analyze_code(request: CodeRequest):
    bugs = "No critical bugs found"

    # 🔍 Syntax check (Python only for now)
    if request.language.lower() == "python":
        try:
            ast.parse(request.code)
        except SyntaxError as e:
            bugs = f"Syntax Error: {e.msg} (line {e.lineno})"

    return {
        "language": request.language,
        "bugs": bugs,
        "performance": "Code can be optimized",
        "security": "No security issues detected",
        "optimized_code": request.code
    }