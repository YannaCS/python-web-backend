from fastapi import APIRouter, status, Depends
from sqlmodel import Session
from app.schemas import NoteCreate, NoteResponse
from app.models import Note
from app.database import get_session

from app.dependency import DBSession

router = APIRouter(prefix='/notes')

@router.post('/', response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
# dependency injection
def create_note(
    note: NoteCreate,
    # db: Session = Depends(get_session)
    # db: Annotated[Session, Depends(get_session)]
    # or put the above in dependency.py (can add more others)
    # then just import and call it
    db: DBSession
):
    user_id = 1
    
    db_note = Note(
        title=note.title,
        content=note.content,
        user_id=user_id
    )
    
    db.add(db_note)
    db.commit()
    return db_note

"""
When a request comes in:

1. FastAPI sees db: DBSession parameter
2. Recognizes it needs to call get_session()
3. Calls get_session() → gets a Session
4. Passes that Session to your function as db
5. The function runs
6. FastAPI completes the yield in get_session() (cleanup happens)

This all happens automatically! 🎉
"""