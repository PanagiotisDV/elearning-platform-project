"""
API MODULE - ΕΞΑΓΩΓΗ ROUTERS ΚΑΙ DEPENDENCIES
"""

from app.api.routes import auth, courses, lessons, enrollments, progress, quizzes
from app.api.deps import (
    get_current_user,
    get_current_active_user,
    require_role,
    oauth2_scheme,
)

__all__ = [
    # Routers
    "auth",
    "courses",
    "lessons",
    "enrollments",
    "progress",
    "quizzes",
    # Dependencies
    "get_current_user",
    "get_current_active_user",
    "require_role",
    "oauth2_scheme",
]

