# django-test-project

Тестовый проект на Django framework версии 2.2. Используется Python 3.7.3.

## Setup

#### Install requirements

```shell
$ pip install -r requirements.txt
```

## Using

#### Run server

```shell
$ python manage.py runserver
```

#### Admin account

> Login: `admin`

> Password: `admin`

## Troubleshooting

#### Site matching query does not exist.

1. Launch Django shell:
>```shell
>$ python manage.py shell
>```
2. Add new Site model:
>```python
>>>>from django.contrib.sites.models import Site
>>>>s = Site(domain='Your_IP_Address', name='Desired_Site_Name')
>>>>s.save()
>>>>exit()
>```
2. Run server:
>```shell
>$ python manage.py runserver
>```

## License

MIT License

Copyright (c) 2019 Shvetsov Dmitry

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.