# Rutificador Automatizado de datos a Excel
Esta software esta pensando para las personas que necesitan datos especificos y desean hacerlo de manera automatizada.

# IMPORTANTE

- El presente proyecto no tiene relación alguna con el sitio:
  
          https://rutificador.net/
- Ni tampoco con su base de datos, mucho menos con sus creadores/administradores.
- El autor se desliga de cualquier responsabilidad derivada del uso del presente código.

# Lógica a utilizar.
- Por lo mismo he desarrollado este codigo con pensando en los siguientes criterios:

- 1.- Utilizaremos la pagina web "https://rutificador.net/rut/" para acceder a estos datos
- 2.- Bloquearemos los anuncios propios de la pagina para evitar problemas y fallos de ello
- 3.- Almacenaremos los datos en especifico que necesitamos
- 4.- Tendremos la opción de almacenar en formato .xlsl (Excel) todos los datos obtenidos.

# Metodo de uso e Instalación de dependencias
- Para poder usar el programa debemos:

- 1.- Descargar el codigo de "Busqueda Automatizada.py" 
- 2.- Instalar las siguientes dependencias en la terminal
  - Se utilizarán: Playwright - Beautifulsoup4 - Pandas - Openpyxl
    
        pip install playwright beautifulsoup4 pandas openpyxl
  - Luego necesitamos instalar en la misma terminal:
        
        playwright install
