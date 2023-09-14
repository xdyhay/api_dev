from passlib.context import CryptContext
from . import models, schemas

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)



def apply_query_params(query, query_params: schemas.QueryParams):
    # Used for path operations to filter, sort, paginate, etc.
    if query_params.search is not None:
        query = query.filter(models.Post.title.contains(query_params.search))

    if query_params.limit is not None:
        query = query.limit(query_params.limit)

    if query_params.skip is not None:
        query = query.offset(query_params.skip)
        
    return query