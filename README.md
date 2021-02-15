<h1> Factory </h1>

### Команды для запуска Docker:

```
git clone https://github.com/prostomusa/Factory.git
cd Factory
docker build .
docker-compose build
docker-compose run web python manage.py makemigrations
docker-compose run web python manage.py migrate
docker-compose up
```

### Ссылка на документацию API:
[https://documenter.getpostman.com/view/7641548/TVepAU9a]
