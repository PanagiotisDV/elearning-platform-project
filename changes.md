# Changes Export

## Problem
- The `create_course`, `update_course`, and `delete_course` endpoints in `backend/app/api/routes/courses.py` used `Depends(require_role("instructor"))`.
- This dependency blocked admin users and could fail for valid instructor users if the role check did not match exactly.
- There was also a stray `instructor` line in `courses.py` causing a syntax / stray token issue.

## Fix applied
- Removed the stray `instructor` line from `backend/app/api/routes/courses.py`.
- Replaced `Depends(require_role("instructor"))` with `Depends(get_current_active_user)` for:
  - `create_course`
  - `update_course`
  - `delete_course`
- Added explicit role validation within those endpoints:
  - `create_course`: allow only users with role `instructor` or `admin`
  - `update_course`: allow `instructor` or `admin`, with ownership restriction for instructors
  - `delete_course`: allow `instructor` or `admin`, with ownership restriction for instructors

## Summary of conversation
- User reported inability to create a course despite having a registered instructor role.
- Investigation showed the issue came from an overly strict dependency check in FastAPI route definitions.
- The fix was to use the standard authenticated user dependency and validate roles in route logic.
- Updated `fix_summary.md` / `FIX_SUMMARY.md` with the change details and date.

## Final result
- Registered instructors can now create courses.
- Admins can create, update, and delete courses.
- Instructors can update/delete only their own courses.
- Course endpoints now use proper authentication and authorization checks.

```# filepath: e:\AUEB\PYTHON\FINAL EXAM\E-LEARNING-PLATFORM\changes.md
# Changes Export

## Problem
- The `create_course`, `update_course`, and `delete_course` endpoints in `backend/app/api/routes/courses.py` used `Depends(require_role("instructor"))`.
- This dependency blocked admin users and could fail for valid instructor users if the role check did not match exactly.
- There was also a stray `instructor` line in `courses.py` causing a syntax / stray token issue.

## Fix applied
- Removed the stray `instructor` line from `backend/app/api/routes/courses.py`.
- Replaced `Depends(require_role("instructor"))` with `Depends(get_current_active_user)` for:
  - `create_course`
  - `update_course`
  - `delete_course`
- Added explicit role validation within those endpoints:
  - `create_course`: allow only users with role `instructor` or `admin`
  - `update_course`: allow `instructor` or `admin`, with ownership restriction for instructors
  - `delete_course`: allow `instructor` or `admin`, with ownership restriction for instructors

## Summary of conversation
- User reported inability to create a course despite having a registered instructor role.
- Investigation showed the issue came from an overly strict dependency check in FastAPI route definitions.
- The fix was to use the standard authenticated user dependency and validate roles in route logic.
- Updated `fix_summary.md` / `FIX_SUMMARY.md` with the change details and date.

## Final result
- Registered instructors can now create courses.
- Admins can create, update, and delete courses.
- Instructors can update/delete only their own courses.
- Course endpoints now use proper authentication and authorization checks.
