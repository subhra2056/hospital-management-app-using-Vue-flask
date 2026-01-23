from datetime import datetime, timedelta
from Backend.controllers.database import db
from Backend.controllers.models import TokenBlocklist
from Backend.controllers.config import config

def delete_expired_tokens():
    expiry_time = datetime.utcnow() - timedelta(
        seconds=config.JWT_ACCESS_TOKEN_EXPIRES
    )

    TokenBlocklist.query.filter(TokenBlocklist.created_at < expiry_time).delete()

    db.session.commit()
