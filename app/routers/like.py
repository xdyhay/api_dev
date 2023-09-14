from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from uuid import UUID
from .. import models, schemas, database, oauth2

router = APIRouter (prefix='/likes', tags=['Likes'])

@router.post('/', status_code=status.HTTP_201_CREATED)
def like(like: schemas.LikeCreateModel, db: Session = Depends(database.get_db), current_user: UUID = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == like.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id {like.post_id} not found')
    
    query = db.query(models.Like).filter(
        models.Like.post_id == like.post_id, models.Like.user_uuid == current_user.uuid)
    found_like = query.first()

    if like.dir == 1:
        # Found a like: user already liked the post
        if found_like:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f'User {current_user.email} already liked the post {like.post_id}')

        new_like = models.Like(post_id=like.post_id, user_uuid=current_user.uuid)
        db.add(new_like)
        db.commit()
        db.refresh(new_like)
        return {'message': 'Like successful'}
    else:
        if not found_like:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'Like does not exist')
        # If the like is found, unlike/delete it
        query.delete(synchronize_session=False)
        db.commit()
        return {'message': 'Unlike post'}