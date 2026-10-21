# coding: utf-8
"""stocking 库 RBAC 模型: 用户 / 角色 / 权限

对应 k-training 的 prisma/stocking.prisma
表: sys_user, sys_role, sys_user_role, sys_permission, sys_role_permission
"""
from sqlalchemy import (
    BigInteger,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class SysUser(Base):
    __tablename__ = "sys_user"

    id = Column(BigInteger, primary_key=True)
    username = Column(String(64), unique=True)
    password = Column(String(255))
    nickname = Column(String(64))
    email = Column(String(128))
    phone = Column(String(32))
    avatar = Column(String(512))
    status = Column(Integer, default=1)  # 1 启用 / 0 禁用
    last_login_at = Column(DateTime)
    create_time = Column(DateTime)
    update_time = Column(DateTime)

    user_roles = relationship("SysUserRole", back_populates="user")


class SysRole(Base):
    __tablename__ = "sys_role"

    id = Column(BigInteger, primary_key=True)
    role_code = Column(String(64), unique=True)
    role_name = Column(String(64))
    description = Column(String(255))
    status = Column(Integer, default=1)
    create_time = Column(DateTime)
    update_time = Column(DateTime)

    user_roles = relationship("SysUserRole", back_populates="role")
    role_permissions = relationship("SysRolePermission", back_populates="role")


class SysUserRole(Base):
    __tablename__ = "sys_user_role"
    __table_args__ = (
        UniqueConstraint("user_id", "role_id", name="unq_sys_user_role"),
    )

    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey("sys_user.id"))
    role_id = Column(BigInteger, ForeignKey("sys_role.id"))

    user = relationship("SysUser", back_populates="user_roles")
    role = relationship("SysRole", back_populates="user_roles")


class SysPermission(Base):
    __tablename__ = "sys_permission"

    id = Column(BigInteger, primary_key=True)
    perm_code = Column(String(160), unique=True)
    perm_name = Column(String(128))
    perm_type = Column(String(16))  # page | api
    parent_id = Column(BigInteger, default=0)
    path = Column(String(255))
    method = Column(String(16))
    sort = Column(Integer, default=0)
    status = Column(Integer, default=1)
    create_time = Column(DateTime)
    update_time = Column(DateTime)

    role_permissions = relationship("SysRolePermission", back_populates="perm")


class SysRolePermission(Base):
    __tablename__ = "sys_role_permission"
    __table_args__ = (
        UniqueConstraint("role_id", "perm_id", name="unq_sys_role_permission"),
    )

    id = Column(BigInteger, primary_key=True)
    role_id = Column(BigInteger, ForeignKey("sys_role.id"))
    perm_id = Column(BigInteger, ForeignKey("sys_permission.id"))

    role = relationship("SysRole", back_populates="role_permissions")
    perm = relationship("SysPermission", back_populates="role_permissions")


