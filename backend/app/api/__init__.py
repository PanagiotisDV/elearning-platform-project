"""
ROUTES - ΕΞΑΓΩΓΗ ΟΛΩΝ ΤΩΝ ENDPOINTS
"""

from app.api.routes import auth
from app.api.routes import courses
from app.api.routes import lessons
from app.api.routes import enrollments
from app.api.routes import progress
from app.api.routes import quizzes

__all__ = [
    "auth",
    "courses",
    "lessons",
    "enrollments",
    "progress",
    "quizzes",
]

