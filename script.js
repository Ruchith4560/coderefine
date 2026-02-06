function analyzeCode() {
    const code = document.getElementById("codeInput").value;
    const language = document.getElementById("language").value;

    document.getElementById("loader").classList.remove("hidden");

    fetch("http://127.0.0.1:8000/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ code, language })
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById("bugs").innerText = data.bugs || "No issues";
        document.getElementById("performance").innerText = data.performance || "N/A";
        document.getElementById("explanation").innerText =
            (data.explanation || []).join("\n");
        document.getElementById("commentedCode").innerText =
            data.optimized_code || "";

        document.getElementById("loader").classList.add("hidden");
    })
    .catch(err => {
        alert("Backend connection failed");
        document.getElementById("loader").classList.add("hidden");
    });
}