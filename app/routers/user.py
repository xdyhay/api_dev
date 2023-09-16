from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from uuid import UUID
from .. import models, schemas, database, utils

router  = APIRouter(prefix='/users', tags=['Users'])

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreateModel, db: Session = Depends(database.get_db)):
    query = db.query(models.User).filter(models.User.email == user.email)
    if query.first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f'User with email {user.email} already exists')
    
    hashed_password = utils.hash_password(user.password)
    user.password = hashed_password
    user = models.User(**user.model_dump())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.get('/{uuid}', response_model=schemas.UserOut)
def get_user(uuid: UUID, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.uuid == uuid).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with id {uuid} not found')
    return user