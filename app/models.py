from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from .database import Base


class User(Base):
    __tablename__ = 'users'

    uuid = Column(UUID(as_uuid=True), primary_key=True, index=True, nullable=False, 
                  server_default=text('gen_random_uuid()'), unique=True)
    email = Column(String, index=True, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), 
                        nullable=False, server_default=text('current_timestamp'))
    
class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    title = Column(String, index=True, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, nullable=False, server_default='True')
    created_at = Column(TIMESTAMP(timezone=True), 
                        nullable=False, server_default=text('current_timestamp'))
    
    user_uuid = Column(UUID(as_uuid=True), 
                       ForeignKey('users.uuid', ondelete='CASCADE'), nullable=False)
    user = relationship('User')

class Like(Base):
    __tablename__ = 'likes'

    post_id = Column(Integer, ForeignKey('posts.id', ondelete='CASCADE'), 
                     primary_key=True)
    user_uuid = Column(UUID(as_uuid=True), ForeignKey('users.uuid', ondelete='CASCADE'), 
                       primary_key=True)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('current_timestamp'))
    
    post = relationship('Post')
    user = relationship('User')