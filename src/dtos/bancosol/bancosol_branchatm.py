import re

from pydantic import BaseModel, Field, computed_field, field_validator

from .const import BancoSolOfficeName, BancoSolOfficeTypeName

transvowels = str.maketrans(
    "áéíóúÁÉÍÓÚ",
    "aeiouAEIOU",
)


class OpeningHours(BaseModel):
    hour: str

    @field_validator("hour", mode="before")
    def strip_props(cls, propvalue):
        return (
            propvalue
            if not isinstance(propvalue, str)
            else re.sub(r"\s+", " ", propvalue).strip()
        )


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
    address_name: str = Field(validation_alias="addressName", exclude=True)

    latitude: float
    longitude: float

    opening_hours: OpeningHours = Field(validation_alias="openingHours", exclude=True)

    @computed_field
    def working_hours(self) -> str:
        return self.opening_hours.hour

    locality: BoliviaLocality = Field(exclude=True)

    @computed_field
    def city(self) -> str:
        locname = self.locality.name.translate(transvowels)
        return re.sub(r"\s+", "_", locname).upper()

    bodepartament: BoliviaDepartment = Field(
        exclude=True,
        validation_alias="department",
    )

    @computed_field
    def department(self) -> str:
        depname = self.bodepartament.name.translate(transvowels)
        return re.sub(r"\s+", "_", depname).upper()

    office_type: OfficeType = Field(validation_alias="officeType", exclude=True)

    @computed_field
    def type(self) -> str:
        return (
            re.sub(r"\s+", "_", self.office_type.name)
            .upper()
            .replace("CAJEROS", "ATM")
            .replace("AGENCIAS", "AGENCIA")
        )

    @computed_field
    def subtype(self) -> str:
        typename = self.office_type.type_name.replace("-", " ")
        return (
            re.sub(r"\s+", "_", typename.translate(transvowels))
            .upper()
            .replace("CAJERO_AUTOMATICO", "ATM")
        )

    @field_validator("*", mode="before")
    def strip_props(cls, prop_value):
        return (
            prop_value
            if not isinstance(prop_value, str)
            else re.sub(r"\s+", " ", prop_value).strip()
        )
