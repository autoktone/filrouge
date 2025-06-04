# SOA
Example of SOA, Service Oriented Architecture with independant and stateless micro services through an API gateway and a reverse proxy (Caddy).

# Student project
This is a student project but it can be useful for other people who may need to connect a front with a back end using API Rest HTTPS requests.
Docker is helpful here to deploy this basic python/FastApi/Flask/joblib project (useful for ML tasks for example). Those services can be then deployed in Cloud Infrastructure as scalable containers with different public IP Addresses and Ports (example AWS, Azure, Google Cloud...).

# Security
The communications between internet and the gateway are cyphered (HTTPS/TLS), no need for internal Docker network exchanges.
A token is necessary for calling services (JWT), as private services should implement it in our case (it is not open DATA API).
Many actions may harden the security concerns as showed in Caddyfile for more secured HTTP requests.

# Repository
This repository can be cloned via Azure CLI or other ways, in order to deploy the project files into an os or a virtual machine (Linux Ubuntu for example).

# Application
Here is the example of a Sport App, providing User Centric high valued informations about events and dedicated sites. The recommandations depend on the user preferences, the user context and other trends amongst other members based on the digital ecosystem (informations sources) :
An intelligent User Interface for composing various services dedidated to sport preferences. The app must be user centric and provides sports events as spectator or participant from the digital ecosystem. Firstly, the user should connect from GOOGLE SSO for example, and while creating his account, the user should answer various questions about his sport preferences (sports, when, how, his biological caracteristics and social data). After user account creation, the app will provide events following his preferences and the real time contextual data (agenda, climate and localization). Clicking on the sections will call API external services which will respond though JSON data as usually on web oriented architecture. The home page displays the trends as sections (best events from similar users, best sports complex).
