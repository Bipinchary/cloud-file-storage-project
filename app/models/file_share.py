import uuid
from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Boolean,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.db import Base


class FileShare(Base):
    __tablename__ = "file_shares"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    file_id = Column(
        UUID(as_uuid=True),
        ForeignKey("files.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    token = Column(
        UUID(as_uuid=True),
        unique=True,
        nullable=False,
        default=uuid.uuid4,
        index=True,
    )

    expires_at = Column(DateTime, nullable=True)

    is_active = Column(Boolean, default=True, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    file = relationship("File", backref="shares")
