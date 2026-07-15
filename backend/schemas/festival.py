from pydantic import BaseModel


class FestivalExtendedProps(BaseModel):
    addr1: str
    firstimage: str
    tel: str


class FestivalEvent(BaseModel):
    id: str
    title: str
    start: str
    end: str
    extendedProps: FestivalExtendedProps
