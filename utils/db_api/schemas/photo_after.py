from sqlalchemy import Column, String, sql, DateTime, ForeignKey

from utils.db_api.db_gino import BaseModel, db


class PhotoAfter(BaseModel):
    __tablename__ = 'photos_after'
    query: sql.Select

    file_id = Column(String(256), primary_key=True)
    user_id = Column(ForeignKey('users.user_id', ondelete='CASCADE'))
    date = Column(DateTime(True), server_default=db.func.now())
    tech_type = Column(String(32))
    tech_number = Column(String(32))
    remont_type = Column(String(32))

    @staticmethod
    async def create_photo(user_id: int, tech_type: str, tech_number: str, remont_type: str, photo_after: list):
        for file in photo_after:
            await PhotoAfter.create(
                file_id=str(file),
                tech_type=tech_type,
                tech_number=tech_number,
                remont_type=remont_type,
                user_id=user_id
            )
