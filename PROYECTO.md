# Playlist según tu videojuego favorito

## Introducción

El proyecto consiste en unir dos mundos de nuestro interés: la música y los videojuegos. Se propone la creación de una aplicación en Python con la utilización de dos APIs: RAWG y Spotify.

El objetivo principal es que el usuario pueda ingresar el nombre de un videojuego y a partir de su género o ambientación, se le brindan una serie de playlists musicales relacionadas con el estilo del juego.

La idea busca ofrecer una experiencia inmersiva que se extienda más allá del universo del videojuego al plano musical, proponiendo listas que acompañen el estado de ánimo, ritmo o atmósfera del título seleccionado.



## Objetivos de aprendizaje

Con el proyecto buscamos poner en práctica y desarrollar el conocimiento en los siguientes conceptos:
Manejo de peticiones HTTP.
Manejo de datos en formato JSON.
Modularidad, claridad y reutilización de código.


## Bosquejo de Arquitectura
**Arquitectura basada en 3 capas:**

1. **Capa de Presentación**: HTML + CSS + Jinja2 + Flask templates.  
2. **Capa de Negocio**: lógica de interacción entre APIs, manejo de datos, filtros, control de flujo.  
3. **Capa de Datos**: consumo en tiempo real de datos desde RAWG y Spotify.
<img width="1024" height="1536" alt="imagen" src="https://github.com/user-attachments/assets/9c5398f2-7d52-49e8-b2b8-1fbbf9d2095a" />


## Requerimientos

### Requerimientos Funcionales

- **RF1**: El usuario podrá ingresar el nombre de un videojuego desde la página web.
- **RF2**: El sistema consultará la API de RAWG para obtener información del videojuego y procesará la respuesta para identificar género, etiquetas y ambientación.
- **RF3**: Se realizará una búsqueda en la API de Spotify utilizando las palabras clave extraídas.
- **RF4**: El sistema renderizará una página dinámica que mostrará los resultados musicales.
- **RF5**: Se presentarán las playlists con su nombre, descripción y enlace al perfil de Spotify.
- **RF6**: Si no se obtienen resultados, el sistema mostrará un mensaje informativo al usuario.

### Requerimientos No Funcionales

#### **Portability**
- El sistema debe funcionar correctamente en múltiples navegadores (Web).

#### **Security**
- Todos los Tokens / API Keys deben estar protegidos (por ejemplo, en variables de entorno o archivos `.env` no subidos a GIT).

#### **Maintainability**
- El sistema debe diseñarse con arquitectura en 3 capas.
- El sistema debe utilizar control de versiones mediante GIT.
- El sistema debe estar programado en Python 3.10 o superior.
- El código debe ser modular, documentado y seguir buenas prácticas de programación.

#### **Reliability**
- En caso de error en las APIs, se debe mostrar un mensaje adecuado al usuario sin que la aplicación se caiga.

#### **Scalability**
- El sistema debe funcionar correctamente en ventana normal y de incógnito (Web).
- No se deben guardar datos del usuario en variables locales: usar mecanismos como cookies, tokens o almacenamiento seguro si aplica.

#### **Performance**
- El tiempo total de respuesta no debe superar los 5 segundos en condiciones normales.
- El sistema debe funcionar en un equipo hogareño estándar.

#### **Reusability**
- El código debe estar separado en módulos para facilitar su reutilización en futuros proyectos.

#### **Flexibility**
- Por el momento no se utiliza base de datos, pero el sistema debe estar diseñado para permitir su incorporación futura sin afectar la estructura principal.



## Stack Tecnológico

### Capa de Datos

- **Base de datos**: no se utiliza base de datos actualmente.
- **ORM**: no aplica.
- **Motivo**: la aplicación trabaja en tiempo real con datos obtenidos directamente de las APIs externas, por lo que no es necesaria la persistencia local en esta versión.

### Capa de Negocio

- **Lenguaje principal**: Python 3.10+
- **Framework**: Flask
- **Librerías utilizadas**:
  - `requests` para consumo de APIs.
  - `dotenv` para manejo de variables de entorno.
  - `json` para procesamiento de respuestas.
- **APIs utilizadas**:
  - **RAWG**: provee datos sobre videojuegos.
  - **Spotify API**: provee playlists y contenido musical.
- **Motivo**: Flask permite un desarrollo rápido y flexible. La lógica de negocio queda clara y separada del resto.

### Capa de Presentación

- **Tecnologías utilizadas**:
  - HTML + CSS
  - Jinja2 (integrado con Flask)
- **Motivo**: suficiente para construir una interfaz web clara y funcional sin sobrecargar el stack. Ideal para prototipos funcionales y proyectos integradores.
