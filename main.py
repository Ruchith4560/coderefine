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

def analyze_by_language(code: str, language: str):
    language = language.lower()

    if language == "python":
        return analyze_python(code)
    elif language == "c":
        return analyze_c(code)
    elif language == "cpp" or language == "c++":
        return analyze_cpp(code)
    elif language == "java":
        return analyze_java(code)
    else:
        return {"error": "Language not supported"}

def analyze_by_language(code: str, language: str):
    language = language.lower()

    if language == "python":
        return analyze_python(code)
    elif language == "c":
        return analyze_c(code)
    elif language == "cpp" or language == "c++":
        return analyze_cpp(code)
    elif language == "java":
        return analyze_java(code)
    else:
        return {"error": "Language not supported"}

def analyze_cpp(code: str):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".cpp") as f:
        f.write(code.encode())
        filename = f.name

    result = subprocess.run(
        ["g++", "-fsyntax-only", filename],
        capture_output=True,
        text=True
    )

    os.remove(filename)

    if result.stderr:
        return {"syntax": result.stderr}
    return {"syntax": "Valid C++ syntax"}

def analyze_java(code: str):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".java") as f:
        f.write(code.encode())
        filename = f.name

    result = subprocess.run(
        ["javac", filename],
        capture_output=True,
        text=True
    )

    os.remove(filename)

    if result.stderr:
        return {"syntax": result.stderr}
    return {"syntax": "Valid Java syntax"}


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
    logic_issues = detect_logic_issues(request.code)
    optimization_suggestions = []
    explanation = []

    # Syntax check (Python example)
    if request.language.lower() == "python":
        try:
            ast.parse(request.code)
        except SyntaxError as e:
            syntax_errors.append(
                f"Line {e.lineno}: {e.msg}"
            )

    # Optimization suggestions
    if "for" in request.code and "min(" not in request.code:
        optimization_suggestions.append(
            "Use built-in functions like min(), max(), sum() for better performance"
        )

    # Simple explanation (line-by-line)
    lines = request.code.split("\n")
    for i, line in enumerate(lines, start=1):
        explanation.append(f"Line {i}: {line.strip()}")

    return {
        "syntax_errors": syntax_errors,
        "logic_issues": logic_issues,
        "optimization_suggestions": optimization_suggestions,
        "explanation": explanation,
        "commented_code": request.code
    }
