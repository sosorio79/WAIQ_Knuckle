/**
 * WAIQ Knuckle - TypeScript frontend (compiled)
 * Client-side logic for the training app.
 */
const API_BASE = "/api";
async function fetchViaProxy(url) {
    const res = await fetch(`${API_BASE}/proxy?url=${encodeURIComponent(url)}`);
    const body = await res.text();
    return { status: res.status, body };
}
function showStatus(message, type) {
    const el = document.getElementById("ts-status");
    if (!el)
        return;
    el.textContent = message;
    el.className = `status status-${type}`;
    el.hidden = false;
    setTimeout(() => {
        el.hidden = true;
    }, 5000);
}
function initSsrfForm() {
    const form = document.getElementById("ssrf-proxy-form");
    const urlInput = document.getElementById("ssrf-url");
    const resultEl = document.getElementById("ssrf-result");
    if (!form || !urlInput || !resultEl)
        return;
    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        const targetUrl = urlInput.value.trim();
        if (!targetUrl) {
            showStatus("Enter a URL to fetch", "error");
            return;
        }
        resultEl.textContent = "Fetching...";
        resultEl.className = "ssrf-result loading";
        try {
            const { status, body } = await fetchViaProxy(targetUrl);
            resultEl.textContent = `Status: ${status}\n\n${body.slice(0, 2000)}`;
            resultEl.className = "ssrf-result";
        }
        catch (err) {
            resultEl.textContent = `Error: ${err instanceof Error ? err.message : String(err)}`;
            resultEl.className = "ssrf-result error";
        }
    });
}
function init() {
    if (document.getElementById("ssrf-proxy-form")) {
        initSsrfForm();
    }
}
if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
} else {
    init();
}
