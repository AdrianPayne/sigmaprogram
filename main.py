from enum import Enum
from datetime import date
from typing import List, Optional

from fastapi import FastAPI, Path, Query, Cookie, status
from pydantic import BaseModel, Field, EmailStr

app = FastAPI()


class Tags(Enum):
    courses = "courses"
    users = "users"


@app.get("/")
async def root():
    return "∑"

#
# Views
#


# Courses
@app.get("/courses", tags=[Tags.courses])
async def get_courses():
    """
    Get all courses available
    """
    return {"courses": "Courses"}


course_path = Path(..., title="The title of the course")


@app.get("/courses/{shortname}", tags=[Tags.courses])
async def get_course(shortname: str = course_path):
    return {"course": shortname}


class CourseItem(BaseModel):
    shortname: str = Field(..., max_length=20)
    title: str = Field(..., max_length=150)
    description: Optional[str]
    tags: Optional[List] = Field(None, title="Related tags")

    class Config:
        schema_extra = {
            "example": {
                "shortname": "my_course",
                "title": "A very nice course",
                "description": "This is not very useful course yet",
                "tags": ["easy", "unuseful"],
            }
        }


@app.post("/courses/{shortname}", tags=[Tags.courses], response_model=CourseItem, status_code=status.HTTP_201_CREATED)
async def post_course(
        *,
        shortname: str = course_path,
        body: CourseItem
):
    return {shortname: body}


# Users
class UserBasic(BaseModel):
    username: str = Field(..., max_length=20)
    email: EmailStr = Field(...)
    birth_date: date = Field(...)


class UserIn(UserBasic):
    password: str = Field(..., max_length=20)


@app.get("/users/{username}", tags=[Tags.users], response_model=UserBasic)
async def get_user(username: str):
    return username


@app.post("/users/{username}", tags=[Tags.users], response_model=UserBasic, status_code=status.HTTP_201_CREATED)
async def post_user(
        *,
        username: str,
        body: UserIn
):
    return body
