from typing import Optional
from pydantic import BaseModel
from utils.security.generics import hash_str, check_hash


class UserModel(BaseModel):
    id: int
    username: str
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: str
    password: str
    is_active: int
    is_admin: int
    created_on: str
    
    model_config = {
        "from_attributes": True
    }
    
    # class Config:
    #     from_attributes = True  # Convert dict to Pydantic models
    
    @property
    def pk(self):
        return self.id
    
    @property
    def _is_active(self):
        return bool(self.is_active)
    
    @property
    def _is_admin(self):
        return bool(self.is_admin)
    
    @property
    def is_superuser(self):
        return self._is_admin
    
    def as_public_dict(self):
        return self.model_dump(exclude={"password"})





class ProductModel(BaseModel):
    id: int
    name: str
    code: str
    price: float
    details: Optional[str] = None
    created_by: Optional[str] = None
    created_on: str
    is_active: int
    stock: int
    image_url: Optional[str] = None
    
    model_config = {
        "from_attributes": True
    }
    
    @property
    def _is_active(self):
        return bool(self.is_active)
