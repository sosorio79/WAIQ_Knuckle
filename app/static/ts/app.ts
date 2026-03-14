/**
 * WAIQ Knuckle - TypeScript frontend
 * Client-side logic for the training app.
 */

// API base URL (same origin in dev; configurable for proxied Go service)
const API_BASE = "/api";

/** Fetch URL via the Go SSRF proxy (intentionally vulnerable endpoint) */
export async function fetchViaProxy(url: string): Promise<{ status: number; body: string }> {
  const res = await fetch(`${API_BASE}/proxy?url=${encodeURIComponent(url)}`);
  const body = await res.text();
  return { status: res.status, body };
}

/** Show a toast/status message in the UI */
export function showStatus(message: string, type: "info" | "success" | "error"): void {
  const el = document.getElementById("ts-status");
  if (!el) return;
  el.textContent = message;
  el.className = `status status-${type}`;
  el.hidden = false;
  setTimeout(() => {
    el.hidden = true;
  }, 5000);
}

/** Wire up SSRF proxy form (called when on ssrf-proxy module page) */
export function initSsrfForm(): void {
  const form = document.getElementById("ssrf-proxy-form") as HTMLFormElement | null;
  const urlInput = document.getElementById("ssrf-url") as HTMLInputElement | null;
  const resultEl = document.getElementById("ssrf-result") as HTMLElement | null;

  if (!form || !urlInput || !resultEl) return;

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
    } catch (err) {
      resultEl.textContent = `Error: ${err instanceof Error ? err.message : String(err)}`;
      resultEl.className = "ssrf-result error";
    }
  });
}

/** Initialize all TypeScript-driven behavior */
function init(): void {
  if (document.getElementById("ssrf-proxy-form")) {
    initSsrfForm();
  }
}
if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", init);
} else {
  init();
}
