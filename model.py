from database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship


class User(Base):
    """
    Represents all users in the system, both patients and doctors.
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    id_number = Column(String(255), unique=True, index=True, nullable=False)
    name = Column(String(100), nullable=False)
    surname = Column(String(100), nullable=False)


class DoctorEducation(Base):

    __tablename__ = 'doctor_education'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(11), ForeignKey('users.id'))
    title = Column(String(100), nullable=False)
    description = Column(String(255), nullable=False)
    medicines = Column(String(255), nullable=False)
    advice = Column(String(255), nullable=False)
    possibility = Column(String(255), nullable=False)
    level = Column(String(100), nullable=False)
    area = Column(String(100), nullable=False)


