# Instalación

1. Instala las dependencias necesarias
    ```
    pip install -r requirements.txt
    ```
2. Crea el fichero config.ini

    * Usar el fichero **config_Users.ini** como referencia
    * Obten tu apiKey de coinmarketcap [aquí](https://coinmarketcap.com/api/)

3. Ejecuta la aplicación desde **-main.py**


# Simulador de cryptos

Simulador de inversiones en cryptos, que consulta el valor real en euros, de las diez cryptomonedas con mayor volumen de negocios actualmente (2021):

* Las cryptos utilizadas por esta aplicación son:

    | Cryptos               |                   |                         |                   |                   
    |-----------------------|:----------------- |:------------------------|:------------------| 
    | ADA - Cardano         |   ETH - Ethereum  |   BSV - Bitcoin SV      |   USDT - Tether   |
    | BCH - Bitcoin Cash    |   LTC - Litecoin  |   BTC - Bitcoin         |   XLM - Stellar   |                     
    | BNB - Binance Coin    |   TRX - TRON      |   EOS - EOS             |   XRP - XRP       |           

* La aplicación nos permitirá realizar las siguientes conversiones:
    * **De euros a caulquier crypto**: Se considerará inversión, el total de euros invertidos se mostrará en € invertidos
    * **De crypto a otra crypto**: Estos movimientos los haremos en función de su valor relativo de manera que logremos incrementar el número de bitcoins que tenemos.
    * **De cualquier crypto a euros**: Se considerará retorno de la inversión y se descontará del total invertido cuando queramos hacer balance

* Cada una de estas conversiones o movimientos se grabarán en la base de datos registrando la fecha y hora.
* La aplicación se conectará a la api de coinmarketcap, para indicarnos el valor real de nuestras transacciones registradas en la base de datos.
    * Cuantos euros se invirtieron
    * El valor actual en euros de nuestras cryptos

# Estructura del proyecto

Consta de diferentes ficheros:
* api_acces.py: gestiona llamadas y posibles errores a la api de coinmarketcap
* movementsDB. py: gestiona llamadas a la base de datos **movements.db**
* config.ini: contiene endpoints y api_key
* requierements.txt: librerías necesarias para la ejecución de la aplicación
* main.py: archivo principal que lanza la aplicación

Los archivos disponen de comentarios explicando la función de cada uno de ellos.

El formato de la salida de las cryptos de from_Q, to_Q y precio unitario, es de 5 decimales, debido a que en algunos casos, el valor es muy bajo.




   
    
    
    
    

