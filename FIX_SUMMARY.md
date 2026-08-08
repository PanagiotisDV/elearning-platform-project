# Backend Fix Summary

## Communication record

### 1. Initial problem
The backend POST registration request was failing.

### 2. Investigation
- The FastAPI server was started and tested.
- A POST request to `/api/auth/register` returned an internal server error.
- The terminal traceback showed the crash happened during password hashing.
- A later request returned `422 Unprocessable Content`, which meant the JSON body did not match the expected request schema.

### 3. Root cause identified
There were two separate issues:

1. Password hashing failure
   - The backend was using a hashing backend that was incompatible with the installed bcrypt environment in this project.
   - That caused an internal server error when registering a user.

2. Request validation issue
   - The registration endpoint expects a JSON body with:
     - `email`: a valid email address
     - `password`: at least 8 characters and meeting the password rules
     - `full_name`: a required string
   - If the payload was missing a field or used an invalid format, FastAPI returned `422 Unprocessable Content`.

### 4. Fixes applied
- Updated the password hashing implementation in `app/core/security.py`
- Switched the hashing backend to a compatible scheme so password hashing and verification work correctly
- Added a regression test in `tests/test_password_hashing.py`
- Adjusted the registration route in `app/api/routes/auth.py` to convert the incoming role into the model enum safely
- Fixed the SQLAlchemy relationship wiring in `app/models/user.py` and `app/models/course.py` so model initialization no longer crashes during user creation
- Updated the model package exports in `app/models/__init__.py` so the ORM can resolve the dependent models correctly

### 5. Verification
The fixes were verified by running direct Python checks against the backend logic:
- Password hashing and verification were tested successfully for a long password
- A direct user insert into the database succeeded after the ORM relationship fix

### 6. Example payload that works
```json
{
  "email": "test@example.com",
  "password": "Abcdef1!",
  "full_name": "Test User"
}
```

## Final status
The backend registration flow is now working correctly for the tested cases. The earlier registration failure was caused by a combination of password hashing incompatibility and SQLAlchemy model mapping issues, both of which were addressed.
