create database testdb;

use testdb;

create table testtable(id int not null AUTO_INCREMENT, column1 varchar(50), column2 varchar(50), PRIMARY KEY (id));
                                          

docker network create app-network -d bridge

docker run -d --name mysql --network app-network -e MYSQL_ROOT_PASSWORD=password mysql

docker exec -it mysql mysql -u root -p

docker run -d --name backend --network app-network -e MYSQL_HOST=mysql -e MYSQL_USER=root -e MYSQL_PASSWORD=password -e MYSQL_DATABASE=testdb -e MYSQL_TABLE=testtable backend:v0

docker run -d --name frontend --network app-network -p 80:80 frontend:v1


