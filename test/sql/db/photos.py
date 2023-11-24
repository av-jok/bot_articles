from typing import Optional

from sqlalchemy import String
from sqlalchemy import BIGINT
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from .base import Base


class Photo(Base):
    __tablename__ = "photo"

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    sid: Mapped[int] = mapped_column(BIGINT)
    nid: Mapped[int] = mapped_column(BIGINT, nullable=True)
    tid: Mapped[Optional[str]] = mapped_column(String(128))
    name: Mapped[Optional[str]] = mapped_column(String(128))
    file_id: Mapped[str] = mapped_column(String(255))

    def __repr__(self):
        return f"<Photo {self.id} {self.name} {self.sid}>"
