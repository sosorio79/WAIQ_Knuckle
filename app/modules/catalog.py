# WAIQ Knuckle — Module Catalog
# Every module maps to questions from AppSec_Questions_Modules_Ideas (Q1–Q91)

MODULES = [
    # ─── Existing interactive demos ───
    {
        "slug": "xss-guestbook",
        "title": "XSS Guestbook (Reflected/Stored)",
        "description": "Unsanitized guestbook messages render as HTML/JS. Covers Reflected, Stored, DOM-based XSS and output encoding.",
        "questions": ["Q4", "Q8", "Q19", "Q41", "Q44", "Q65"],
        "type": "XSS",
    },
    {
        "slug": "sqli-login",
        "title": "SQLi Login",
        "description": "Unsafe string-built SQL query for authentication. Boolean, error-based, NoSQL concepts.",
        "questions": ["Q5", "Q28", "Q50", "Q64"],
        "type": "SQLi",
    },
    {
        "slug": "idor-profile",
        "title": "IDOR Profile Viewer",
        "description": "Direct object access by ID with no ownership check. Vertical/horizontal access control, 403 bypass.",
        "questions": ["Q10", "Q31", "Q42"],
        "type": "IDOR",
    },
    {
        "slug": "ssrf-proxy",
        "title": "SSRF Proxy (Go service)",
        "description": "Go sidecar fetches arbitrary URLs with no validation. Try http://localhost:5000 or http://169.254.169.254/.",
        "questions": ["Q37", "Q59"],
        "type": "SSRF",
    },
    {
        "slug": "csrf-no-token",
        "title": "CSRF No Token",
        "description": "State change endpoint without CSRF protection. SameSite, anti-CSRF tokens.",
        "questions": ["Q17", "Q27", "Q66"],
        "type": "CSRF",
    },
    {
        "slug": "upload-no-validation",
        "title": "File Upload (No Validation)",
        "description": "Accepts any file without type/path checks. LFI, RCE via upload.",
        "questions": ["Q22", "Q29", "Q60"],
        "type": "File Upload",
    },
    # ─── Web Cache ───
    {
        "slug": "web-cache",
        "title": "Web Cache Deception & Poisoning",
        "description": "Cache deception vs poisoning, unkeyed inputs, Param Miner.",
        "questions": ["Q1", "Q53"],
        "type": "Web Cache",
    },
    # ─── Session & Auth ───
    {
        "slug": "session-management",
        "title": "Session Management",
        "description": "Session fixation, session storage, session lifecycle.",
        "questions": ["Q2", "Q32", "Q71"],
        "type": "Session",
    },
    {
        "slug": "jwt-auth",
        "title": "JWT & Authentication",
        "description": "JWKs, JKUs, stateless auth, password reset, user enumeration, OAuth, 2FA, security tokens.",
        "questions": ["Q11", "Q16", "Q34", "Q47", "Q52", "Q56", "Q70", "Q78", "Q81"],
        "type": "Auth",
    },
    # ─── Encoding & Crypto ───
    {
        "slug": "encoding-crypto",
        "title": "Encoding & Cryptography",
        "description": "Base64/Base64URL, encoding vs encryption vs hashing, password hashing, salting.",
        "questions": ["Q3", "Q35", "Q72", "Q79", "Q80"],
        "type": "Crypto",
    },
    # ─── HTTP & Request Smuggling ───
    {
        "slug": "request-smuggling",
        "title": "HTTP Request Smuggling",
        "description": "TE.TE, CL.0, Transfer-Encoding manipulation, HTTP request syntax.",
        "questions": ["Q7", "Q36", "Q51", "Q57"],
        "type": "Request Smuggling",
    },
    {
        "slug": "hpp-waf",
        "title": "HTTP Parameter Pollution & WAF Bypass",
        "description": "HPP for WAF bypass, parameter concatenation.",
        "questions": ["Q9"],
        "type": "HPP",
    },
    # ─── Client-Side ───
    {
        "slug": "same-origin-cors",
        "title": "Same-Origin Policy & CORS",
        "description": "SOP, CORS preflight conditions, cross-origin attacks.",
        "questions": ["Q6", "Q20"],
        "type": "Client-Side",
    },
    {
        "slug": "websockets",
        "title": "WebSockets",
        "description": "Sec-WebSocket-Key, WebSocket handshake.",
        "questions": ["Q14"],
        "type": "Client-Side",
    },
    {
        "slug": "csp",
        "title": "Content Security Policy",
        "description": "unsafe-inline, script-src, CSP directives.",
        "questions": ["Q15"],
        "type": "Client-Side",
    },
    # ─── Server-Side Vulnerabilities ───
    {
        "slug": "business-logic",
        "title": "Business Logic & Race Conditions",
        "description": "Testing assumptions, limit overrun, state changes, resource access races.",
        "questions": ["Q12", "Q49"],
        "type": "Business Logic",
    },
    {
        "slug": "ssti",
        "title": "Server-Side Template Injection",
        "description": "SSTI detection payloads, polyglot, template engine identification, RCE.",
        "questions": ["Q13", "Q54"],
        "type": "SSTI",
    },
    {
        "slug": "deserialization",
        "title": "Insecure Deserialization",
        "description": "Object attribute modification, magic methods, RCE via deserialization.",
        "questions": ["Q21", "Q46"],
        "type": "Deserialization",
    },
    {
        "slug": "command-injection",
        "title": "Command Injection",
        "description": "Blind/inferential command injection, time delays, output redirection.",
        "questions": ["Q48"],
        "type": "RCE",
    },
    {
        "slug": "prototype-pollution",
        "title": "Prototype Pollution",
        "description": "Client/server-side prototype pollution, DOM XSS, access control bypass.",
        "questions": ["Q30"],
        "type": "Prototype Pollution",
    },
    # ─── API Security ───
    {
        "slug": "api-security",
        "title": "API Security",
        "description": "Mass assignment, GraphQL batching, type juggling, rate limit bypass.",
        "questions": ["Q23", "Q24", "Q25"],
        "type": "API",
    },
    # ─── XXE ───
    {
        "slug": "xxe",
        "title": "XXE Injection",
        "description": "XML parameter entities, SVG/Office docs, SOAP, out-of-band XXE.",
        "questions": ["Q18", "Q33"],
        "type": "XXE",
    },
    # ─── Information Disclosure & General ───
    {
        "slug": "information-disclosure",
        "title": "Information Disclosure",
        "description": "Finding sensitive data, source analysis, directory busting, error fuzzing.",
        "questions": ["Q26"],
        "type": "Info Disclosure",
    },
    {
        "slug": "sensitive-data-url",
        "title": "Sensitive Data in URL",
        "description": "Why URLs are insecure for secrets (logging, history, Referer).",
        "questions": ["Q39"],
        "type": "General",
    },
    {
        "slug": "open-redirect",
        "title": "Open Redirect",
        "description": "Redirect exploitation, OAuth token theft, SSRF chaining.",
        "questions": ["Q40"],
        "type": "Open Redirect",
    },
    {
        "slug": "captcha",
        "title": "CAPTCHA Weaknesses",
        "description": "Replay, validation bypass, leaked answers, low entropy.",
        "questions": ["Q43"],
        "type": "CAPTCHA",
    },
    {
        "slug": "formula-injection",
        "title": "Formula / CSV Injection",
        "description": "Excel formula injection, =cmd|, data exfiltration via CSV export.",
        "questions": ["Q55"],
        "type": "Formula Injection",
    },
    {
        "slug": "html-injection",
        "title": "HTML Injection",
        "description": "Beyond XSS: social engineering, DoS, SSRF/LFI via PDF, dangling markup.",
        "questions": ["Q58"],
        "type": "HTML Injection",
    },
    {
        "slug": "crlf-injection",
        "title": "CRLF Injection",
        "description": "Response splitting, Set-Cookie injection, session fixation via CRLF.",
        "questions": ["Q61"],
        "type": "CRLF",
    },
    # ─── Network & TLS ───
    {
        "slug": "network-tls",
        "title": "TLS/SSL & Network Security",
        "description": "TLS misconfiguration, HTTPS, SSL, SFTP, VPN.",
        "questions": ["Q38", "Q73", "Q74", "Q75", "Q76", "Q77"],
        "type": "Network",
    },
    # ─── Scoping & General ───
    {
        "slug": "scoping",
        "title": "Pentest Scoping",
        "description": "Questions to ask during web app pentest scoping.",
        "questions": ["Q45"],
        "type": "Scoping",
    },
    {
        "slug": "general-web-security",
        "title": "General Web Security",
        "description": "Web app security, common attacks, WAF, input validation, OWASP Top 10.",
        "questions": ["Q62", "Q63", "Q67", "Q68", "Q69"],
        "type": "General",
    },
    # ─── Behavioral ───
    {
        "slug": "behavioral",
        "title": "Behavioral Interview Questions",
        "description": "Why AppSec, stress, strengths/weaknesses, company fit, experience.",
        "questions": ["Q82", "Q83", "Q84", "Q85", "Q86", "Q87", "Q88", "Q89", "Q90", "Q91"],
        "type": "Behavioral",
    },
]

# Quick lookup: question_id -> list of module slugs
def questions_to_modules() -> dict[str, list[str]]:
    out: dict[str, list[str]] = {}
    for m in MODULES:
        for q in m["questions"]:
            out.setdefault(q, []).append(m["slug"])
    return out
