# Sapid

## Setup Project using Docker

First make sure you have installed `docker` and `docker-compose` on your machine.
https://docs.docker.com/get-docker/

1. Clone the project from git repository and move into the project directory.

```sh
git clone https://github.com/kaushik-tagline/sapid.git
cd sapid/
```

2. Create environment variable file to example file and add your own credentials for third party services.

```sh
cp .env.example .env
```

3. Then run the following command to setup project using docker:

```sh
docker-compose up -d --build
```

4. Migrate the database

```sh
docker-compose exec web python manage.py migrate
```

5. Create a super user with following command; So you can login into the admin site:

```sh
docker-compose exec web python manage.py createsuperuser
```

You can go to the http:///127.0.0.1:8020 to view the application running.

## Docker Development

### Build the docker containers

```sh
docker-compose up -d --build
```

### Stop the containers

```
docker-compose stop
```

### Check the docker containers status

```sh
docker-compose ps -a
```

### Check the logs of the docker containers

The below command displays logs of both containers together.

```sh
docker-compose logs -f --tail 20
```

Check the logs for only the database container.

```sh
docker-compose logs -f --tail 20 postgres
```

Check the logs for only the django container.

```sh
docker-compose logs -f --tail 20 web
```

### To remove the docker containers

```sh
docker-compose down
```

To remove the docker containers with all the data. `Do not use this command. This will removes all the data of database.`

```sh
docker-compose down -v
```
