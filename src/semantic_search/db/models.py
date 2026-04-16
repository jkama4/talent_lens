from sqlalchemy import (
    Boolean,
    Column,
    Date,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


class Candidate(Base):
    __tablename__ = "candidate"

    external_id = Column(String, primary_key=True)
    user_id = Column(String)
    last_name = Column(String)
    first_name = Column(String)
    gender = Column(String)
    date_of_birth = Column(Date)
    ethnicity = Column(String)
    address_line1 = Column(String)
    address_line2 = Column(String)
    address_city = Column(String)
    address_zip = Column(String)
    address_state = Column(String)
    address_country_id = Column(String)
    work_phone = Column(String)
    mobile = Column(String)
    email = Column(String)
    email2 = Column(String)
    source = Column(String)
    date_available = Column(Date)
    bsn = Column(String)
    business_sector_id = Column(String)
    category = Column(String)
    specialty_category_id = Column(String)
    skill_id = Column(String)
    status = Column(String)

    attachments = relationship("CandidateAttachment", back_populates="candidate")
    education = relationship("CandidateEducation", back_populates="candidate")
    gdpr = relationship("CandidateGDPR", back_populates="candidate")
    work_experience = relationship("CandidateWorkExperience", back_populates="candidate")


class CandidateAttachment(Base):
    __tablename__ = "candidate_attachment"

    id = Column(Integer, primary_key=True, autoincrement=True)
    external_id = Column(String, unique=True)
    candidate_external_id = Column(String, ForeignKey("candidate.external_id"), nullable=False)
    filename = Column(String)
    relative_file_path = Column(String)
    is_resume = Column(Boolean)

    candidate = relationship("Candidate", back_populates="attachments")


class CandidateEducation(Base):
    __tablename__ = "candidate_education"

    id = Column(Integer, primary_key=True, autoincrement=True)
    external_id = Column(String, unique=True)
    candidate_external_id = Column(String, ForeignKey("candidate.external_id"), nullable=False)
    start_date = Column(Date)
    end_date = Column(Date)
    school = Column(String)
    city = Column(String)
    degree = Column(String)
    comments = Column(Text)

    candidate = relationship("Candidate", back_populates="education")


class CandidateGDPR(Base):
    __tablename__ = "candidate_gdpr"

    id = Column(Integer, primary_key=True, autoincrement=True)
    candidate_external_id = Column(String, ForeignKey("candidate.external_id"), nullable=False)
    consent_purpose = Column(String)
    legal_basis = Column(String)
    date_last_sent = Column(Date)
    date_last_received = Column(Date)
    consent_source = Column(String)

    candidate = relationship("Candidate", back_populates="gdpr")


class CandidateWorkExperience(Base):
    __tablename__ = "candidate_work_experience"

    id = Column(Integer, primary_key=True, autoincrement=True)
    external_id = Column(String, unique=True)
    candidate_external_id = Column(String, ForeignKey("candidate.external_id"), nullable=False)
    start_date = Column(Date)
    end_date = Column(Date)
    comments = Column(Text)
    company_name = Column(String)
    termination_reason = Column(String)
    title = Column(String)

    candidate = relationship("Candidate", back_populates="work_experience")


class ClientCorporation(Base):
    __tablename__ = "client_corporation"

    external_id = Column(String, primary_key=True)
    name = Column(String)
    user_id = Column(String)
    main_phone = Column(String)
    company_url = Column(String)
    address_line1 = Column(String)
    address_line2 = Column(String)
    address_zip = Column(String)
    address_city = Column(String)
    address_state = Column(String)
    address_country_id = Column(String)
    billing_address_line1 = Column(String)
    billing_address_line2 = Column(String)
    billing_address_zip = Column(String)
    billing_address_city = Column(String)
    billing_address_state = Column(String)
    billing_address_country_id = Column(String)
    billing_contact = Column(String)
    billing_phone = Column(String)
    business_sector_list = Column(String)
    company_description = Column(Text)
    status = Column(String)
    notes = Column(Text)

    contacts = relationship("ClientContact", back_populates="corporation")


class ClientContact(Base):
    __tablename__ = "client_contact"

    external_id = Column(String, primary_key=True)
    client_corporation_external_id = Column(String, ForeignKey("client_corporation.external_id"))
    user_id = Column(String)
    last_name = Column(String)
    first_name = Column(String)
    phone = Column(String)
    phone2 = Column(String)
    email1 = Column(String)
    email2 = Column(String)
    title = Column(String)
    address_line1 = Column(String)
    address_line2 = Column(String)
    address_zip = Column(String)
    address_city = Column(String)
    address_state = Column(String)
    address_country_id = Column(String)
    source = Column(String)
    status = Column(String)
    division = Column(String)
    comments = Column(Text)

    corporation = relationship("ClientCorporation", back_populates="contacts")
