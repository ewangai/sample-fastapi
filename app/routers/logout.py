
from fastapi import APIRouter, Depends, status, HTTPException, responses
from sqlalchemy.orm import Session
from .. import database, models, oauth2


router = APIRouter(
    prefix="/logout",
    tags=['logout']
) 


@router.delete("/")  # Use DELETE for logout
async def logout(current_user: int = Depends(oauth2.get_current_user), db: Session = Depends(database.get_db)):
#def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)): # define the function

    """
    Logs out the current user by revoking their access token and deleting it.

    Returns a success message upon successful logout.
    """

    jti = current_user.get("jti")  # Extract the JWT ID (jti) from the token
    if jti:
        try:
            # Revoke the token using a suitable mechanism
            await oauth2.revoke_token(jti)

            # Delete the token from the database (assuming a token storage mechanism)
            db.query(models.RevokedToken).filter_by(jti=jti).delete()
            db.commit()

            # Optionally, log the logout event or perform additional actions
            db_user = db.query(models.User).filter_by(id=current_user.get("user_id")).first()
            # ... (e.g., update user's last_logout_time, invalidate session)

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to log out",
            ) from e

    return responses.JSONResponse(content={"message": "Logged out successfully"}, status_code=status.HTTP_204_NO_CONTENT)
