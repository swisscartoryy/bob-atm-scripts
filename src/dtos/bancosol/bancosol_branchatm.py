import re

from pydantic import BaseModel, Field, computed_field
from .const import BancoSolOfficeName, BancoSolOfficeTypeName

transvowels = str.maketrans(
    "áéíóúÁÉÍÓÚ",
    "aeiouAEIOU",
)


class OpeningHours(BaseModel):
    hour: str


class BoliviaLocality(BaseModel):
    name: str = Field(validation_alias="localityName")


class BoliviaDepartment(BaseModel):
    name: str = Field(validation_alias="departmentName")
    holidays: str


class OfficeType(BaseModel):
    name: BancoSolOfficeName = Field(validation_alias="officeName")
    type_name: BancoSolOfficeTypeName = Field(validation_alias="officeTypeName")


class BancoSolBranchATM(BaseModel):
    id: str
    name: str

    phone: str
    address_name: str = Field(validation_alias="addressName")

    latitude: float
    longitude: float

    opening_hours: OpeningHours = Field(validation_alias="openingHours", exclude=True)

    @computed_field(alias="fopeningHours")
    def fopening_hours(self) -> str:
        return self.opening_hours.hour

    locality: BoliviaLocality = Field(exclude=True)

    @computed_field
    def flocality(self) -> str:
        locname = self.locality.name.translate(transvowels)
        return re.sub(r"\s+", "_", locname).upper()

    department: BoliviaDepartment = Field(exclude=True)

    @computed_field
    def fdepartment(self) -> str:
        depname = self.department.name.translate(transvowels)
        return re.sub(r"\s+", "_", depname).upper()

    office_type: OfficeType = Field(validation_alias="officeType", exclude=True)

    @computed_field(alias="fofficeName")
    def foffice_name(self) -> str:
        return re.sub(r"\s+", "_", self.office_type.name).upper()

    @computed_field(alias="fofficeTypeName")
    def foffice_typename(self) -> str:
        typename = self.office_type.type_name.replace("-", " ")
        return re.sub(r"\s+", "_", typename.translate(transvowels)).upper()
