MODULES = [
    {
        "slug": "xss-guestbook",
        "title": "XSS Guestbook (Reflected/Stored)",
        "description": "Unsanitized guestbook messages render as HTML/JS.",
        "questions": ["Q4", "Q8", "Q19", "Q41", "Q44", "Q65"],
        "type": "XSS",
    },
    {
        "slug": "sqli-login",
        "title": "SQLi Login",
        "description": "Unsafe string-built SQL query for authentication.",
        "questions": ["Q5", "Q28", "Q50", "Q64"],
        "type": "SQLi",
    },
    {
        "slug": "idor-profile",
        "title": "IDOR Profile Viewer",
        "description": "Direct object access by ID with no ownership check.",
        "questions": ["Q10", "Q31"],
        "type": "IDOR",
    },
    {
        "slug": "upload-no-validation",
        "title": "File Upload (No Validation)",
        "description": "Accepts any file without type/path checks.",
        "questions": ["Q22", "Q29"],
        "type": "File Upload",
    },
    {
        "slug": "csrf-no-token",
        "title": "CSRF No Token",
        "description": "State change endpoint without CSRF protection.",
        "questions": ["Q17", "Q27", "Q66"],
        "type": "CSRF",
    },
]

