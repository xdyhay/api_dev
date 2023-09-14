from fastapi import status, HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import models, database, utils, oauth2

router = APIRouter(tags=['Authentication'])

@router.post('/login')
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'Invalid Credentials provided')
    
    if not utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'Invalid Credentials provided')
    
    access_token = oauth2.create_access_token(data={'user_id': str(user.uuid)})
    
    # return {'message': 'Login Successful'}
    return {'access_token': access_token, 'token_type': 'bearer'}