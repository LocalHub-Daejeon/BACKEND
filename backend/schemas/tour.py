from pydantic import BaseModel


class TourListItem(BaseModel):
    contentid: str
    contenttypeid: str
    contentType: str
    title: str
    addr1: str
    addr2: str
    firstimage: str
    mapx: str
    mapy: str
    eventstartdate: str = ""
    eventenddate: str = ""


class TourDetail(BaseModel):
    contentid: str
    contenttypeid: str
    contentType: str
    title: str
    addr1: str
    addr2: str
    zipcode: str
    tel: str
    mapx: str
    mapy: str
    firstimage: str
    firstimage2: str
    createdtime: str
    modifiedtime: str
    eventstartdate: str = ""
    eventenddate: str = ""


class TourListResponse(BaseModel):
    items: list[TourListItem]
    page: int
    size: int
    total: int
