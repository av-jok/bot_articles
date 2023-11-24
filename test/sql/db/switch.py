from typing import Optional
from sqlalchemy import String
from sqlalchemy import text, BIGINT, Boolean, true
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from .base import Base


class Switch(Base):
    __tablename__ = "switch"

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    nid: Mapped[int] = mapped_column(BIGINT, nullable=True)
    asset_tag: Mapped[int] = mapped_column(BIGINT)
    sn: Mapped[Optional[str]] = mapped_column(String(250))
    model: Mapped[Optional[str]] = mapped_column(String(250))
    name: Mapped[Optional[str]] = mapped_column(String(250))
    ipaddres: Mapped[Optional[str]] = mapped_column(String(250))
    vlan: Mapped[Optional[str]] = mapped_column(String(250))
    upswitch: Mapped[Optional[str]] = mapped_column(String(250))
    upport: Mapped[Optional[str]] = mapped_column(String(250))
    arenda: Mapped[Optional[str]] = mapped_column(String(250))
    type_bc: Mapped[Optional[str]] = mapped_column(String(250))
    contact: Mapped[Optional[str]] = mapped_column(String(250))
    comment: Mapped[Optional[str]] = mapped_column(String(250))
    username: Mapped[Optional[str]] = mapped_column(String(128))
    staus: Mapped[str] = mapped_column(String(128))
    active: Mapped[bool] = mapped_column(Boolean, server_default=true())

    def __repr__(self):
        return f"<Switch {self.id} {self.name}>"
