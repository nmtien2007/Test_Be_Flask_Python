from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Float, UniqueConstraint, ARRAY
from app.database import db
from sqlalchemy_utils import JSONType, ScalarListType
from sqlalchemy.orm import relationship


class Test(db.Model):
    __tablename__ = 'test'
    id = Column(Integer, primary_key=True)


class Users(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(120), nullable=False, unique=True)
    user_type = Column(Integer, nullable=False)
    user_id = Column(String(64), nullable=False)

    score = relationship("UserScore", back_populates="user", uselist=False)
    jobs = relationship("VolunteerJobs", back_populates="user", uselist=False)
    __table_args__ = (UniqueConstraint('email', name='unique_email_constraint'),)


class UserScore(db.Model):
    __tablename__ = 'user_score'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    scores = Column(JSONType, nullable=False, default={})
    good_subjects = Column(String(256), nullable=False)
    avg_score = Column(Float, nullable=False, default=0.0)

    user = relationship("Users", back_populates="score", uselist=False, lazy=True)


class VolunteerJobs(db.Model):
    __tablename__ = 'volunteer_jobs'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    jobs = Column(ARRAY(String), nullable=False, default=[])

    user = relationship("Users", back_populates="jobs", uselist=False, lazy=True)