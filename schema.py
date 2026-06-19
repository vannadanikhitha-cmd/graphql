import strawberry
from models import User
from database import SessionLocal

@strawberry.type
class UserType:
    id: int
    name: str
    email: str
@strawberry.type
class Query:

    @strawberry.field
    def users(self) -> list[UserType]:

        db = SessionLocal()

        users = db.query(User).all()

        return [
            UserType(
                id=u.id,
                name=u.name,
                email=u.email
            )
            for u in users
        ]
@strawberry.type
class Mutation:

    @strawberry.mutation
    def create_user(
        self,
        name: str,
        email: str
    ) -> UserType:

        db = SessionLocal()

        user = User(
            name=name,
            email=email
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return UserType(
            id=user.id,
            name=user.name,
            email=user.email
        )


    @strawberry.mutation
    def update_user(
        self,
        id: int,
        name: str
    ) -> UserType:

        db = SessionLocal()

        user = db.query(User).filter(
            User.id == id
        ).first()

        user.name = name

        db.commit()
        db.refresh(user)

        return UserType(
            id=user.id,
            name=user.name,
            email=user.email
        )


    @strawberry.mutation
    def delete_user(
        self,
        id: int
    ) -> str:

        db = SessionLocal()

        user = db.query(User).filter(
            User.id == id
        ).first()

        db.delete(user)

        db.commit()

        return "Deleted Successfully"
schema = strawberry.Schema(
    query=Query,
    mutation=Mutation
)