# grow-infra
grow-infra

sudo apt install apache2-utils
htpasswd -c docker/nginx/.htpasswd user

cp docker/.env.tmpl docker/.env 
docker-compose --env-file .env up -d

cp grafana/grafana.ini.tmpl grafana/grafana.ini