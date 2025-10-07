# TPI-Soporte-Grupo10

## Introducción

El proyecto consiste en unir dos mundos de nuestro interés: la música y los videojuegos. Se propone la creación de una aplicación en Python con la utilización de dos APIs: RAWG y Spotify.

El objetivo principal es que el usuario pueda ingresar el nombre de un videojuego y a partir de su género o ambientación, se le brindan una serie de playlists musicales relacionadas con el estilo del juego.

La idea busca ofrecer una experiencia inmersiva que se extienda más allá del universo del videojuego al plano musical, proponiendo listas que acompañen el estado de ánimo, ritmo o atmósfera del título seleccionado.



## Objetivos de aprendizaje

Con el proyecto buscamos poner en práctica y desarrollar el conocimiento en los siguientes conceptos:
Manejo de peticiones HTTP.
Manejo de datos en formato JSON.
Modularidad, claridad y reutilización de código.

## Stack tecnológico

En el Backend el lenguaje sera Python y nuestro framework será Flask.

El Frontend será relativamente simple. Utilizaremos HTML, CSS, y Jinja2 para insertar variables dinámicas.

## Requerimientos Funcionales

- **RF1:** El usuario podrá ingresar el nombre de un videojuego desde la página web.  
- **RF2:** El sistema consultará la API para obtener información del videojuego y procesará la respuesta para identificar género, etiquetas y ambientación.  
- **RF3:** Se realizará una búsqueda en la API de Spotify utilizando las palabras clave extraídas.  
- **RF4:** El sistema renderizará una página dinámica que mostrará los resultados musicales.  
- **RF5:** Se presentarán las playlists con su nombre, descripción y enlace al perfil de Spotify.  
- **RF6:** Si no se obtienen resultados, el sistema mostrará un mensaje informativo al usuario.  

## Requerimientos No Funcionales

- **RNF1 – Usabilidad:** La interfaz debe ser simple, intuitiva y con navegación clara.  
- **RNF2 – Rendimiento:** El tiempo total de respuesta no debe superar los 5 segundos en condiciones normales.  
- **RNF3 – Portabilidad:** La aplicación debe poder ejecutarse en cualquier entorno que soporte Python 3.10+ y Flask.  
- **RNF4 – Mantenibilidad:** El código debe ser modular, documentado y seguir buenas prácticas de programación.  
- **RNF5 – Escalabilidad:** El diseño del sistema debe permitir futuras ampliaciones sin afectar la estructura principal.  
