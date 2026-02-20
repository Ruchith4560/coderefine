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
def optimization_suggestions(code: str):
    suggestions = []

    if "for" in code and "range" in code:
        suggestions.append(
            "Consider using Python built-in functions like min(), max(), or sum() for better performance."
        )

    if "for" in code:
        suggestions.append(
            "Time complexity appears to be O(n). Ensure this is acceptable for large inputs."
        )

    return suggestions
def explain_code(code: str):
    explanations = []
    lines = code.split("\n")

    for idx, line in enumerate(lines, start=1):
        stripped = line.strip()

        if stripped.startswith("for "):
            explanations.append(f"Line {idx}: Starts a loop.")
        elif stripped.startswith("if "):
            explanations.append(f"Line {idx}: Checks a condition.")
        elif "=" in stripped and not stripped.startswith("if"):
            explanations.append(f"Line {idx}: Assigns a value to a variable.")
        elif stripped.startswith("print"):
            explanations.append(f"Line {idx}: Outputs a value.")
        elif stripped == "":
            continue
        else:
            explanations.append(f"Line {idx}: Executes a statement.")

    return explanations
def explain_code(code: str):
    explanations = []
    lines = code.split("\n")

    for idx, line in enumerate(lines, start=1):
        stripped = line.strip()

        if stripped.startswith("for "):
            explanations.append(f"Line {idx}: Starts a loop.")
        elif stripped.startswith("if "):
            explanations.append(f"Line {idx}: Checks a condition.")
        elif "=" in stripped and not stripped.startswith("if"):
            explanations.append(f"Line {idx}: Assigns a value to a variable.")
        elif stripped.startswith("print"):
            explanations.append(f"Line {idx}: Outputs a value.")
        elif stripped == "":
            continue
        else:
            explanations.append(f"Line {idx}: Executes a statement.")

    return explanations
import ast

@app.post("/analyze")
def analyze_code(request: CodeRequest):
    syntax_errors = []
    logic_issues = []
    optimizations = []

    # 1️⃣ Syntax check
    if request.language.lower() == "python":
        try:
            ast.parse(request.code)
        except SyntaxError as e:
            syntax_errors.append(
                f"Syntax Error: {e.msg} (line {e.lineno})"
            )
            return {
                "language": request.language,
                "syntax_errors": syntax_errors,
                "logic_issues": [],
                "optimization_suggestions": [],
                "explanation": [],
                "commented_code": ""
            }

    # 2️⃣ Logic issues
    logic_issues = detect_logic_issues(request.code)

    # 3️⃣ Optimization suggestions
    optimizations = optimization_suggestions(request.code)

    # 4️⃣ Code explanation
    explanation = explain_code(request.code)

    # 5️⃣ Comment generation
    commented_code = generate_comments(request.code)

    return {
        "language": request.language,
        "syntax_errors": syntax_errors,
        "logic_issues": logic_issues,
        "optimization_suggestions": optimizations,
        "explanation": explanation,
        "commented_code": commented_code
    }