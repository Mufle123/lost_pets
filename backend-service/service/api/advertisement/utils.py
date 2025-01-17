from typing import List
from fastapi import HTTPException

from service.api.advertisement.models import AdvertisementOutputShort, AdvertisementOutputFull, AdvertisementInput
from service.repository.mappers import Advertisement, UserCustom, Pet, Picture


def map_to_output_advert_short(db_advert: Advertisement):
    user: UserCustom = db_advert.user_posted
    pet: Pet = db_advert.pet_posted
    pictures: List[Picture] = db_advert.picture_posted

    return AdvertisementOutputShort(
        advert_id=db_advert.id,
        advert_category=db_advert.category,
        username=user.username,
        pet_name=pet.name if pet.name else '?',
        picture_link=pictures[0].link if len(pictures) > 0 else None
    )


def map_to_output_advert_full(db_advert: Advertisement):
    user: UserCustom = db_advert.user_posted
    pet: Pet = db_advert.pet_posted
    pictures: List[Picture] = db_advert.picture_posted
    shelter: UserCustom = db_advert.shelter

    return AdvertisementOutputFull(
        advert_id=db_advert.id,
        advert_category=db_advert.category,
        pet_name=pet.name if pet.name else '?',
        pet_species=pet.species if pet.species else None,
        pet_color=pet.color,
        pet_age=pet.age,
        date_time_lost=pet.date_time_lost,
        location_lost=pet.location_lost,
        description=pet.description,
        is_in_shelter=db_advert.is_in_shelter,
        username=user.username,
        user_email=user.email,
        user_phone_number=user.phone_number,
        picture_links=[picture.link for picture in pictures],
        shelter_name=shelter.shelter_name if shelter else None,
        shelter_username=shelter.username if shelter else None,
        shelter_email=shelter.email if shelter else None,
        shelter_phone_number=shelter.phone_number if shelter else None
    )


def validate_advert_input(advert_input: AdvertisementInput):
    if not (
            advert_input.pet_name or
            advert_input.pet_species or
            advert_input.description or
            advert_input.picture_links
    ):
        raise HTTPException(status_code=400, detail='Please provide additional information')

    return advert_input
