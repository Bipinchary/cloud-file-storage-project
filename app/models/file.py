import uuid , enum 
from datetime import datetime
from sqlalchemy import Enum , Column 

from sqlalchemy import (
    Column,
    String,
    BigInteger,
    DateTime,
    Boolean,
    ForeignKey,
    Index,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.db import Base


class FileStatus(str, enum.Enum):
    PENDING = "PENDING"
    ACTIVE = "ACTIVE"
    FAILED = "FAILED"


class File(Base):
    __tablename__ = "files"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    owner_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    s3_key = Column(String, nullable=False, unique=True)
    original_filename = Column(String, nullable=False)
    content_type = Column(String, nullable=False)
    size = Column(BigInteger, nullable=False)

    is_deleted = Column(Boolean, default=False, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    owner = relationship("User", backref="files")

    status = Column(
        Enum(FileStatus, name="file_status"),
        nullable=False,
        default=FileStatus.PENDING,
    )  

     # -------------------------
    # Relationships
    # -------------------------

    owner = relationship("User", back_populates="files")

    # -------------------------
    # Indexes
    # -------------------------

    __table_args__ = (
        Index("ix_files_owner_id", "owner_id"),
    )

   

