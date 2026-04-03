import logging
import time

from slowapi import Limiter
from slowapi.util import get_remote_address
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

# Configuration du logger d'audit — sortie structurée vers stdout (capturé par Docker)
logging.basicConfig(
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
    level=logging.INFO,
)
audit_logger = logging.getLogger("vtek.audit")

# Rate limiter keyed par IP client
limiter = Limiter(key_func=get_remote_address)


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Injecte les en-têtes HTTP de sécurité sur toutes les réponses (OWASP A05)."""

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        # X-XSS-Protection désactivé : la protection est assurée par CSP (recommandation OWASP)
        response.headers["X-XSS-Protection"] = "0"
        response.headers["Referrer-Policy"] = "no-referrer"
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
        response.headers["Strict-Transport-Security"] = "max-age=63072000; includeSubDomains"
        return response


class AuditLoggingMiddleware(BaseHTTPMiddleware):
    """Journalise toutes les requêtes HTTP avec leurs métadonnées de sécurité (OWASP A09)."""

    async def dispatch(self, request: Request, call_next):
        start = time.perf_counter()
        response = await call_next(request)
        duration_ms = round((time.perf_counter() - start) * 1000, 2)

        # Erreurs 4xx/5xx en WARNING pour faciliter la détection d'anomalies
        level = logging.WARNING if response.status_code >= 400 else logging.INFO
        audit_logger.log(
            level,
            "%s %s → %d (%.1fms) | client=%s",
            request.method,
            request.url.path,
            response.status_code,
            duration_ms,
            request.client.host if request.client else "unknown",
        )
        return response
