FROM python:3.12-bookworm AS backupsheep-base

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
	&& apt-get -y upgrade \
	&& apt-get -y install zsh htop libpq-dev gcc gnupg2 python3-dev musl-dev git g++-11 ruby ruby-full postgresql-server-dev-all \
	&& apt-get -y install curl dirmngr \
	&& curl -LsS https://r.mariadb.com/downloads/mariadb_repo_setup | bash \
	&& apt-get update \
	&& apt-get -y install mariadb-server mariadb-client \
	&& apt-get -y install tree build-essential vim supervisor openssh-server libffi-dev git libpq-dev python3-dev libffi-dev libjpeg-dev git zip unzip nano libmysqlclient-dev gunicorn g++ libzmq3-dev gcc \
	&& apt-get -y install libssl-dev libxml2-dev libxslt1-dev python3-dev libcurl4-openssl-dev libffi-dev unixodbc unixodbc-dev libsqlite3-dev ncurses-dev libexpat1-dev \
	&& apt-get -y install pkg-config ncurses-dev libreadline6-dev zlib1g-dev libssl-dev autoconf automake libtool pkg-config autoconf \
	&& apt-get -y install libncurses-dev libgnutls28-dev libexpat1-dev pkg-config libreadline-dev zlib1g-dev libssl-dev \
	&& apt-get -y install tree libfreetype6-dev \
	&& apt-get -y install lftp nginx tzdata wget \
	&& pip install psycopg2

RUN wget https://github.com/robbyrussell/oh-my-zsh/raw/master/tools/install.sh -O - | zsh || true

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

FROM backupsheep-base

RUN mkdir /code
WORKDIR /code

# copy project
COPY . /code/

COPY _nginx/default_80.conf /etc/nginx/sites-available/default

EXPOSE 80

COPY init.sh /usr/local/bin/
RUN chmod u+x /usr/local/bin/init.sh

#COPY init.sh init.sh

ENTRYPOINT ["/usr/local/bin/init.sh"]
