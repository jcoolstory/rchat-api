from pydantic import BaseConfig, BaseModel, Field



class TokenSchema(BaseModel):
    username: str = Field(title="사용자 이메일")
    password: str = Field(title="사용자 비밀번호")
    class Config(BaseConfig):
        schema_extra = {
            "example":{
                "id": "admin@admin.com",
                "password": "1234",
            }
        }


class UserLoginSchema(BaseModel):
    id: str = Field(title="사용자 이메일")
    password: str = Field(title="사용자 비밀번호")
    class Config(BaseConfig):
        schema_extra = {
            "example":{
                "id": "admin@admin.com",
                "password": "1234",
            }
        }

class UserSchema(BaseModel):
    id: str = Field(title="id")
    name: str = Field(title="이름")

class UserUpdateSchema(BaseModel):
    name: str = Field(title="이름")

class UserCreateSchema(UserSchema):
    password: str = Field(title="사용자 비밀번호")

class UserJoinSchema(UserCreateSchema):
    password_repeat: str = Field(title="사용자 비밀번호")
    