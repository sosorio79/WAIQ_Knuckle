// SSRF-vulnerable proxy service for WAIQ Knuckle training
// Intentionally fetches arbitrary URLs without validation (for AppSec demos)
package main

import (
	"fmt"
	"io"
	"net/http"
	"os"
)

func main() {
	port := os.Getenv("GO_PROXY_PORT")
	if port == "" {
		port = "9000"
	}

	http.HandleFunc("/fetch", fetchHandler)
	http.HandleFunc("/health", healthHandler)

	addr := ":" + port
	fmt.Printf("[Go] SSRF proxy listening on %s\n", addr)
	if err := http.ListenAndServe(addr, nil); err != nil {
		fmt.Fprintf(os.Stderr, "listen error: %v\n", err)
		os.Exit(1)
	}
}

func healthHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	w.Write([]byte(`{"status":"ok","service":"ssrf-proxy"}`))
}

func fetchHandler(w http.ResponseWriter, r *http.Request) {
	url := r.URL.Query().Get("url")
	if url == "" {
		http.Error(w, "missing url parameter", 400)
		return
	}

	// Intentionally vulnerable: fetches arbitrary URL (SSRF)
	resp, err := http.Get(url)
	if err != nil {
		http.Error(w, fmt.Sprintf("fetch failed: %v", err), 502)
		return
	}
	defer resp.Body.Close()

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		http.Error(w, "read body failed", 502)
		return
	}

	w.Header().Set("Content-Type", "text/plain; charset=utf-8")
	w.WriteHeader(resp.StatusCode)
	w.Write(body)
}
