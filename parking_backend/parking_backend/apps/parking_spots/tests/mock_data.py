MOCK_NAMES = ['Adam', 'Max', 'Stephanie']


MOCK_RESERVATIONS = [
    {
        'username': MOCK_NAMES[0],
        'reservations': [
            {
                'parking_spot_id': 1,
                'parking_spot_reservation_date': '2020-11-09',
                'start_reservation_time': '17:00',
                'end_reservation_time': '17:10',
            },
            {
                'parking_spot_id': 1,
                'parking_spot_reservation_date': '2020-11-10',
                'start_reservation_time': '18:00',
                'end_reservation_time': '19:00',
            },
            {
                'parking_spot_id': 1,
                'parking_spot_reservation_date': '2020-11-13',
                'start_reservation_time': '20:00',
                'end_reservation_time': '22:00',
            },
        ]
    },
    {
        'username': MOCK_NAMES[1],
        'reservations': [
            {
                'parking_spot_id': 3,
                'parking_spot_reservation_date': '2020-11-09',
                'start_reservation_time': '07:00',
                'end_reservation_time': '10:00',
            },
            {
                'parking_spot_id': 2,
                'parking_spot_reservation_date': '2020-11-10',
                'start_reservation_time': '05:00',
                'end_reservation_time': '06:00',
            },
        ]
    },
    {
        'username': MOCK_NAMES[2],
        'reservations': [
            {
                'parking_spot_id': 4,
                'parking_spot_reservation_date': '2020-11-09',
                'start_reservation_time': '22:00',
                'end_reservation_time': '23:00',
            }
        ]
    },
]
