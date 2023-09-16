from typing import List
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from uuid import UUID
from .. import models, schemas, database, utils, oauth2

router  = APIRouter(prefix='/posts', tags=['Posts'])

@router.get('/', response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(database.get_db), current_user: UUID = Depends(oauth2.get_current_user), query_params: schemas.QueryParams = Depends()):
    query = db.query(models.Post)

    if not query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No post found')

    query = utils.apply_query_params(query, query_params)

    return query.all()

@router.get('/likescount', response_model=List[schemas.PostLikeOut])
def get_post_likes_count(db: Session = Depends(database.get_db), current_user: UUID = Depends(oauth2.get_current_user), query_params: schemas.QueryParams = Depends()):
    query = db.query(models.Post, func.count(models.Like.post_id).label('like_count'))\
                    .join(models.Like, models.Like.post_id == models.Post.id, isouter=True)\
                    .group_by(models.Post.id)
    
    query = utils.apply_query_params(query, query_params)

    if not query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No post found')
    
    posts_out_list, likes_out_list = zip(*query.all())
    post_like_out_list = [schemas.PostLikeOut(post=post, likes=like) for post, like in zip(posts_out_list, likes_out_list)]
    
    return post_like_out_list

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.PostOut)
def create_post(post: schemas.PostCreateModel, db: Session = Depends(database.get_db), current_user: UUID = Depends(oauth2.get_current_user)):
    post = models.Post(**post.model_dump(), user_uuid=current_user.uuid)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

# @router.get('/latest', response_model=schemas.PostOut)
# def get_latest_post(db: Session = Depends(database.get_db), current_user: UUID = Depends(oauth2.get_current_user)):
#     post = db.query(models.Post).order_by(models.Post.created_at.desc()).first()
#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f'Post with id {id} not found')
#     return post

@router.get('/latest', response_model=schemas.PostLikeOut)
def get_latest_post(db: Session = Depends(database.get_db), current_user: UUID = Depends(oauth2.get_current_user)):
    query = db.query(models.Post, func.count(models.Like.post_id).label('like_count'))\
                    .join(models.Like, models.Like.post_id == models.Post.id, isouter=True)\
                    .group_by(models.Post.id)
    
    post = query.order_by(models.Post.created_at.desc()).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No post found')
    
    post_like_out = schemas.PostLikeOut(post=post[0], likes=post[1])
    return post_like_out

@router.get('/myposts', response_model=List[schemas.PostOut])
def get_owner_posts(db:Session = Depends(database.get_db), current_user: UUID = Depends(oauth2.get_current_user)):
    query = db.query(models.Post).filter(models.Post.user_uuid == current_user.uuid)
    if not query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post of user {current_user.email} not found')
    return query.all()

# @router.get('/{id}', response_model=schemas.PostOut)
# def get_post(id: int, db: Session = Depends(database.get_db), current_user: UUID = Depends(oauth2.get_current_user)):
#     post = db.query(models.Post).filter(models.Post.id == id).first()
#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f'Post with id {id} not found')
#     return post

@router.get('/{id}', response_model=schemas.PostLikeOut)
def get_post(id: int, db: Session = Depends(database.get_db), current_user: UUID = Depends(oauth2.get_current_user)):
    query = db.query(models.Post, func.count(models.Like.post_id).label('like_count'))\
                    .join(models.Like, models.Like.post_id == models.Post.id, isouter=True)\
                    .group_by(models.Post.id)
    
    post = query.filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id {id} not found')
    
    post_like_out = schemas.PostLikeOut(post=post[0], likes=post[1])
    return post_like_out

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(database.get_db), current_user: UUID = Depends(oauth2.get_current_user)):
    query = db.query(models.Post).filter(models.Post.id == id)

    if query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id {id} not found')
    
    if query.first().user_uuid != current_user.uuid:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'User {current_user.email} is not authorized to delete this post')
    
    query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put('/{id}', response_model=schemas.PostOut)
def update_post(id: int, post: schemas.PostUpdateModel, db: Session = Depends(database.get_db), current_user: UUID = Depends(oauth2.get_current_user)):
    query = db.query(models.Post).filter(models.Post.id == id)

    if query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id {id} not found')
    
    if query.first().user_uuid != current_user.uuid:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'User {current_user.email} is not authorized to update this post')
    
    query.update(post.model_dump(), synchronize_session=False)
    db.commit()
    return query.first()