# Librarian

Librarian es un sistema de reserva en línea de libros para bibliotecas. Permite a estudiantes
y demás usuarios de la biblioteca reservar en línea los libros que necesitan para luego
retirarlos.

## Características principales

- Biblioteca en línea que permite agregar los libros a mi "canasta" de préstamo y finalmente confirmar el pedido.
- Historial de préstamos realizados y préstamos vigentes.
- Programar la fecha y hora de retiro de un préstamo.
- Recordatorios de fecha devolución.
- Cálculo de multas por devolución tardía.

## Modelos

### User
Modelo provisto por el sistema de autenticación de Django para representar a un usuario del sistema.

### Book
Representa a un libro registrado en el sistema.

### Stock
Relacionado con un libro donde se registra la cantidad disponible de libros.

### Loan
Cabecera del pedido de préstamo donde se registra el estado del préstamo y la fecha de
devolución.
Un `User` puede tener uno o varios pedidos. Asociada a esta cabecera está un listado de
items `LoanLineItem` donde se detallan todos los libros que se solicitan.

### LoanLineItem
Referencia al libro (`Book`) solicitado.


**Estados**

Un préstamo transiciona de estado en estado para indicar en que paso del proceso se encuentra.
El escenario común para reserva y retiro sería el siguiente:

**basket** → **placed** → **ready** → **lent** → **returned**


| Estado        | Descripción                                                          |
| ------------- | -------------------------------------------------------------------- |
| basket        | Estado inicial del pedido mientras se agregan libros al pedido       |
| placed        | El pedido de préstamo fue confirmado por el usuario                  |
| ready         | El pedido de préstamo está listo para ser retirado                   |
| lent          | Pedido entregado al usuario                                          |
| returned      | Libros devueltos                                                     |

## Proceso de despacho

Usuario confirma el préstamo -> Administrador de la biblioteca revisa los libros que han sido prestados -> Administrador pre-procesa el pedido -> Administrador alista el pedido para entregar -> Usuario recibe una notificación para retirar el pedido

## Datos de prueba

Carga la información de prueba

    $ python manage.py loaddata users authors books stock


Para iniciar sesión como administrador utiliza el usuario "superduper" y para iniciar sesión como usuario que reserva libros "juanita". La contraseña para ambos es "12345678"
