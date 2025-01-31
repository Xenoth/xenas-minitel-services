# XeNAS Minitel Services
Docker and scripts requirements to run the server:
*minitel.xenoth.fr:3615*

Basic description of the infrastructure:
* cache-service: redis database allowing to share data between services;
* xenas-service: main server handling Minitels clients;
* helldivers-service: Pulling data regularly from https://github.com/helldivers-2/api;
* iss-service: Pulling data regularly from http://api.open-notify.org.
* haikus-service: Pulling data daily from https://calendhaiiku.com/.

# Requirements 
* docker;
* docker-compose.

# Authors
* Xenoth (xenothvalack@gmail.com).
