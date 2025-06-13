from fastapi import Header, HTTPException, status
from helpers.jwt import verify_token

def authorise_user(authorisation: str = Header(...)):
    if not authorisation.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorisation header"
        )
    token = authorisation.split(" ")[1]
    payload = verify_token(token)
    return payload