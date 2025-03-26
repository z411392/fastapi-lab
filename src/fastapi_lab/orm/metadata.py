from fastapi_lab.orm.models.general.log import Log  # noqa: F401
from fastapi_lab.orm.models.general.user import User  # noqa: F401
from fastapi_lab.orm.models.general.product import Product  # noqa: F401
from fastapi_lab.orm.models.general.order import Order  # noqa: F401
from fastapi_lab.orm.models.general.base import Base

metadata = Base.metadata
__all__ = ["metadata"]
