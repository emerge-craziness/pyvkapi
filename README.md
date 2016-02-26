Что это такое?
==============

Доступ ко всем существующим методам VK API из Python (3.x).  
Модуль авторизации взят из пакета pypi vk.  

Пример использования
====================
~~~python
>>> from vkapi import VkApi
>>> api = VkApi( login = None, password = None )
>>> api.users.get( user_id = 1 )
trying to get 'https://api.vk.com/method/users.get?user_id=1&lang=ru&v=5.45&access_token=&'
{'response': [{'last_name': 'Дуров', 'first_name': 'Павел', 'id': 1}]} 
>>> api.LOGIN, api.PASSWORD = "7999666666", "your_secret_phrase_of_the_life"
>>> api.audio.search( q = "Grave", performer_only = 1, count = 6, search_own = 1 )
trying to get 'https://api.vk.com/method/audio.search?q=Grave&v=5.45&search_own=1&access_token=c9c8ae2c24e810fecea53d3634ebdf7d4fa9f09e796dfc60d86f8869f686ff6dff6bcf719b1bc7712a51f&performer_only=1&count=6&lang=ru&'
{'response': {'items': [{'id': 436294577, 'owner_id': 215099131, 'date': 1454654606, 'url': 'https://psv4.vk.me/c6135/u60442456/audios/17fe2dde7b97.mp3?extra=nFP0UipnTNkPsO4iLC7AqKl_QhtsI0yU24aX6aLqAeP26vp3cnBEIltsrj15M4bQvvVJUhtmunQ3Eo0kLaLLJSSclRZ6oSadhy9tnHmrENUOmVbJlAmpGBcdPt1Pu7a5T6NeJqXFBbI', 'genre_id': 7, 'duration': 315, 'lyrics_id': 119427227, 'title': 'Severing Flesh', 'artist': 'Grave'}, {'id': 436295767, 'owner_id': 215099131, 'date': 1454655041, 'url': 'https://psv4.vk.me/c6109/u97168116/audios/66b89e7ed927.mp3?extra=bL6e6Ve7Ni4NQi6SRtoDnMrgPqX4T2pQznhFDKzfuPV5G-pM1uPmgdWkg5kLGyFHAvVD_pJfmEQN5piE2azOA8rVe9ayGCCNiZAAHcaH1HHwhrRgd_OfKSPyFJ2WlFd8G3A7cUz-Tuw', 'genre_id': 18, 'duration': 463, 'title': 'Epos', 'artist': 'Grave'}, {'id': 436296428, 'owner_id': 215099131, 'date': 1454655299, 'url': 'https://psv4.vk.me/c536413/u60442456/audios/e1790170022a.mp3?extra=UofTU8qObZEdirv4deC45AomT-4nhdv6fT2pq-bJvWGXw6YmfmwgQEZa6pIiqlyE3qP4tzKjOlO_-diZYyxOrm_GXWu-RCoJYF4xk4fDdjJrBZh4P-46GXb2T5d4o7_Ve9XeuRZUXhA', 'genre_id': 7, 'duration': 188, 'lyrics_id': 119660888, 'title': 'Soulless', 'artist': 'Grave'}, {'id': 436302033, 'owner_id': 215099131, 'date': 1454657267, 'url': 'https://psv4.vk.me/c536413/u60442456/audios/eef021856ead.mp3?extra=1w8CdWAOE1d0WEj7GR-fHJoHc6-rwa8T-MX3G_nsqPzvPL0Nu0qr0PJrd8xhEScgx6ITqLELySI2XrWKxBtLjUR1cgXInPOSCMKAAi2GgjbQD8-8ny4yCZoXNyD2_1OFskJd1hsL8kM', 'genre_id': 7, 'duration': 258, 'lyrics_id': 119660937, 'title': 'I Need You', 'artist': 'Grave'}, {'id': 436302920, 'owner_id': 215099131, 'date': 1454657542, 'url': 'https://psv4.vk.me/c6145/u60442456/audios/9d9379252b40.mp3?extra=wKy8HXcMqkr9vxlMiM2wFikDoWVJAtBlKbl27v4cZg9PowXCaqnWwRuTVyhPbhNSQv0trF6VPTPAnLECtPRd1bdEil_vNE-E6zVp2s--fdMwwYKq8Io3Ce9z0lASUldeQovcuwfxy5g', 'genre_id': 7, 'duration': 358, 'lyrics_id': 119647065, 'title': 'A World In Darkness', 'artist': 'Grave'}, {'id': 212034716, 'owner_id': 215099131, 'date': 1371734706, 'url': 'https://cs1-21v4.vk-cdn.net/p19/a984f991483c80.mp3?extra=kTgu-hqQqPhrL3RuqxoaSITogTB-tO2Op0jHLVdhrbGDllVg_nTg3vg2Ue8atYFUftz1wJufqP06-Y85Vh1FTbL8P_Ex27gEsGWJZLWHFCLaqtxvirUwiZKwpSGfAVsCK9DjjYz5juA', 'genre_id': 7, 'duration': 248, 'title': 'Into The Grave', 'artist': 'Grave'}], 'count': 51080}}
~~~
*And so on.*

Что осталось сделать
=================
- Хэндлинг исключений и ошибок API.
- __parse_response( response ):  
  o сделать класс под response (iterable, supscriptable, has `__str__` and `__repr__`).  
  о в случае ошибки - кидать исключение (относится к предыдущему пункту).  
- Красивый импорт (эстетика, все дела, да).
- Пакет для pypi (кто этим занимался?)
- Полностью осознать авторизацию.

Зачем?
======
Проще было переписать. (с)

License
=======
**lGPL**
