import pytz
from datetime import datetime, timedelta
from sqlalchemy import func


class NutriCommands:
    def create(self, session, target):
        try:
            session.add(target)
            session.commit()
        except Exception as e:
            return str(e)

    def read(self, tmpSession, where, user_id: str, generated_time=None):
        if generated_time == None:
            return tmpSession.query(where).filter_by(user_id=user_id).all()
        else:
            kst = pytz.timezone('Asia/Seoul')
            current_time = datetime.now(kst)
            seven_days_ago = current_time - timedelta(days=generated_time)

            query = (tmpSession.query(
                func.date(where.generated_time).label('date'),
                func.sum(where.kcal).label('total_kcal'),
                func.sum(where.carbohydrate).label('total_carbs'),
                func.sum(where.protein).label('total_protein'),
                func.sum(where.fat).label('total_fat'))
                .filter(where.user_id == user_id)
                .filter(where.generated_time >= seven_days_ago)
                .group_by(func.date(where.generated_time))
                .all())
            return query

    def delete(self, tmpSession, where, user_id: str, generated_time=None):
        try:
            if generated_time == None:
                tmpSession.query(where).filter_by(user_id=user_id).delete()
            else:
                kst = pytz.timezone('Asia/Seoul')
                current_time = datetime.now(kst)
                seven_days_ago = current_time - timedelta(days=generated_time)
                tmpSession.query(where).filter_by(user_id=user_id).filter(
                    where.generated_time >= seven_days_ago).delete()

            tmpSession.commit()
        except Exception as e:
            return str(e)
