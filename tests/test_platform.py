import pytest

import dominus.platform


@pytest.mark.usefixtures('db')
def test_get_kingdom():
    user1 = dominus.platform.create_user('user1', 'secret')
    user2 = dominus.platform.create_user('user2', 'secret')
    kingdom_uuid = dominus.platform.create_kingdom(user1, {
        'cards'         : [],
        'has_colony'    : False,
        'has_platinum'  : False,
        'has_shelters'  : False,
        'name'          : 'test-kingdom',
    })
    dominus.platform.create_kingdom_rating(user1, kingdom_uuid, 2)
    dominus.platform.create_kingdom_rating(user2, kingdom_uuid, 3)
    kingdoms = dominus.platform.get_kingdoms(user1, [kingdom_uuid])
    kingdom = kingdoms[0]
    assert kingdom.rating_mine == 2
    assert kingdom.rating_average == 2.5
