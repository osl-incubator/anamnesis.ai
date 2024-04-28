from anamnesisai import orm


def test_organization():

    data = {
        "id": "f001",
        "active": True,
        "name": "Acme Corporation",
        "address": [{"country": "Switzerland"}],
    }
    breakpoint()
    org = orm.OrganizationModel(**data)
    org.resource_type == "Organization"
    # True

    isinstance(org.address[0], orm.AddressModel)
    # True

    org.address[0].country == "Switzerland"
    # True

    org.dict()["active"] is True
    # True
