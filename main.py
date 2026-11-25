
import pygame
import os

pygame.init()
pygame.mixer.init()

from LOGICA.mazo import (
    crear_mazo,
    barajar,
    repartir_carta,
    calcular_puntos,
    pedir_carta,
    puede_dividir,
    turno_dealer
)


# ==================================
# CONFIGURACIÓN DE SONIDOS
# ==================================

pygame.mixer.music.load("FINALES/SONIDOS/fondo.mp3")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)

sonido_click = pygame.mixer.Sound("FINALES/SONIDOS/click.mp3")
sonido_victoria = pygame.mixer.Sound("FINALES/SONIDOS/victory.mp3")
sonido_perder = pygame.mixer.Sound("FINALES/SONIDOS/lost.mp3")

sonido_click.set_volume(0.6)
sonido_victoria.set_volume(0.8)
sonido_perder.set_volume(0.8)


# ==================================
# CONFIGURACIÓN DE PANTALLA
# ==================================

pantalla = pygame.display.set_mode((1000, 850))
pygame.display.set_caption("BLACKJACK")

VERDE_MESA = (0, 100, 0)
BLANCO = (255, 255, 255)

fuente = pygame.font.Font(None, 30)
fuente_resultado = pygame.font.Font(None, 30)


# ==================================
# CREAR Y BARAJAR EL MAZO
# ==================================

mazo = crear_mazo()
barajar(mazo)

mano_jugador = []
mano_dealer = []
mano_jugador_2 = []

jugando_mano_2 = False

# REPARTIR CARTAS INICIALES

mano_jugador.append(repartir_carta(mazo))
mano_dealer.append(repartir_carta(mazo))

mano_jugador.append(repartir_carta(mazo))
mano_dealer.append(repartir_carta(mazo))


# ==================================
# FUNCIÓN PARA CARGAR IMÁGENES
# ==================================

def cargar_imagen_carta(carta, oculta=False):

    valor, palo = carta

    if oculta:
        nombre = "card_back.png"
    else:
        nombre = f"card_{palo}_{valor}.png"

    ruta = os.path.join("GRAFICA", "CARTAS", nombre)

    imagen = pygame.image.load(ruta)
    imagen = pygame.transform.scale(imagen, (128, 128))

    return imagen


# ==================================
# VARIABLES DE ESTADO
# ==================================

jugador_plantado = False
jugador_perdio = False
dealer_juega = False
jugador_dividio = False

mano_1_terminada = False
mano_2_terminada = False

jugando_mano_2 = False

puntosmano1 = 0
puntosmano2 = 0
puntosdealer = 0

resultado_mano1 = ""
resultado_mano2 = ""

mensaje_estado = ""


# ==================================
# FUNCIÓN PARA NUEVA PARTIDA
# ==================================

def nueva_partida():

    global mazo
    global mano_jugador
    global mano_dealer
    global mano_jugador_2
    global jugando_mano_2

    global jugador_plantado
    global jugador_perdio
    global dealer_juega
    global jugador_dividio

    global mano_1_terminada
    global mano_2_terminada

    global puntosmano1
    global puntosmano2
    global puntosdealer

    global resultado_mano1
    global resultado_mano2
    global mensaje_estado

    mazo = crear_mazo()
    barajar(mazo)

    mano_jugador = []
    mano_dealer = []
    mano_jugador_2 = []

    mano_jugador.append(repartir_carta(mazo))
    mano_dealer.append(repartir_carta(mazo))

    mano_jugador.append(repartir_carta(mazo))
    mano_dealer.append(repartir_carta(mazo))

    jugando_mano_2 = False

    jugador_plantado = False
    jugador_perdio = False
    dealer_juega = False
    jugador_dividio = False

    mano_1_terminada = False
    mano_2_terminada = False

    puntosmano1 = 0
    puntosmano2 = 0
    puntosdealer = 0

    resultado_mano1 = ""
    resultado_mano2 = ""

    mensaje_estado = ""

    print("NUEVA PARTIDA")


# ==================================
# FUNCIÓN PARA COMPARAR RESULTADOS
# ==================================

def comparar_resultado(puntos_jugador, puntos_dealer, numero_mano):

    if puntos_jugador > 21:
        return f"DEALER GANA MANO {numero_mano}"

    elif puntos_dealer > 21:
        return f"GANASTE LA MANO {numero_mano}"

    elif puntos_jugador > puntos_dealer:
        return f"GANASTE LA MANO {numero_mano}"

    elif puntos_jugador < puntos_dealer:
        return f"DEALER GANA MANO {numero_mano}"

    else:
        return f"EMPATE {numero_mano}"


# ==================================
# FUNCIÓN PARA FINALIZAR LA PARTIDA
# ==================================

def finalizar_partida(jugar_dealer):

    global puntosmano1
    global puntosmano2
    global puntosdealer

    global resultado_mano1
    global resultado_mano2

    global jugador_plantado
    global dealer_juega

    # EVITAR FINALIZAR DOS VECES

    if jugador_plantado:
        return

    # TURNO DEL DEALER

    if jugar_dealer:
        turno_dealer(mazo, mano_dealer)

    # CALCULAR PUNTAJES

    puntosmano1 = calcular_puntos(mano_jugador)
    puntosdealer = calcular_puntos(mano_dealer)

    resultado_mano1 = comparar_resultado(
        puntosmano1,
        puntosdealer,
        1
    )

    # SI EL JUGADOR DIVIDIÓ

    if jugador_dividio:

        puntosmano2 = calcular_puntos(mano_jugador_2)

        resultado_mano2 = comparar_resultado(
            puntosmano2,
            puntosdealer,
            2
        )

    # ==================================
    # SONIDOS DEL RESULTADO
    # ==================================

    if jugador_dividio:

        if (
            "GANASTE" in resultado_mano1
            or "GANASTE" in resultado_mano2
        ):

            sonido_victoria.play()

        elif (
            "DEALER GANA" in resultado_mano1
            and "DEALER GANA" in resultado_mano2
        ):

            sonido_perder.play()

    else:

        if "GANASTE" in resultado_mano1:

            sonido_victoria.play()

        elif "DEALER GANA" in resultado_mano1:

            sonido_perder.play()

    # MARCAR PARTIDA TERMINADA

    jugador_plantado = True
    dealer_juega = True

    print("PARTIDA FINALIZADA")
    print("Resultado mano 1:", resultado_mano1)

    if jugador_dividio:
        print("Resultado mano 2:", resultado_mano2)

    print("Puntos dealer:", puntosdealer)


# ==================================
# CREAR BOTONES
# ==================================

boton_pedir = pygame.Rect(60, 275, 120, 70)
boton_dividir = pygame.Rect(60, 475, 120, 70)
boton_plantarse = pygame.Rect(60, 375, 120, 70)
boton_volver = pygame.Rect(700, 710, 230, 70)

esp_vaso = pygame.Rect(70, 680, 60, 60)

imagen_vaso = pygame.image.load(
    os.path.join("FINALES", "vaso.png")
)

imagen_vaso = pygame.transform.scale(
    imagen_vaso, (130, 130)
)

esp_dolar = pygame.Rect(170, 620, 200, 200)

imagen_dolar = pygame.image.load(
    os.path.join("FINALES", "dolar.png")
)

imagen_dolar = pygame.transform.scale(
    imagen_dolar, (270, 270)
)


# ==================================
# CARGAR IMÁGENES DE BOTONES
# ==================================

imagen_volver = pygame.image.load(
    os.path.join("GRAFICA", "BOTONES", "JUGAR.png")
)

imagen_volver = pygame.transform.scale(
    imagen_volver, (230, 70)
)

imagen_pedir = pygame.image.load(
    os.path.join("GRAFICA", "BOTONES", "pedir.png")
)

imagen_pedir = pygame.transform.scale(
    imagen_pedir, (120, 80)
)

imagen_plantarse = pygame.image.load(
    os.path.join("GRAFICA", "BOTONES", "plantarse.png")
)

imagen_plantarse = pygame.transform.scale(
    imagen_plantarse, (120, 90)
)

imagen_dividir = pygame.image.load(
    os.path.join("GRAFICA", "BOTONES", "dividir.png")
)

imagen_dividir = pygame.transform.scale(
    imagen_dividir, (120, 80)
)


# ==================================
# FONDO DE LA MESA
# ==================================

fondo_mesa = pygame.image.load(
    os.path.join("GRAFICA", "MESA", "MESA1.jpg")
).convert()

fondo_mesa = pygame.transform.scale(
    fondo_mesa, (1000, 850)
)


# ==================================
# RELOJ PARA LIMITAR A 60 FPS
# ==================================

reloj = pygame.time.Clock()


# ==================================
# INICIAR JUEGO
# ==================================

corriendo = True

while corriendo:

    # ==================================
    # PROCESAR EVENTOS
    # ==================================

    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:

            corriendo = False

        if evento.type == pygame.MOUSEBUTTONDOWN:

            # ==================================
            # BOTÓN VOLVER / NUEVA PARTIDA
            # ==================================

            if jugador_plantado and dealer_juega:

                if boton_volver.collidepoint(evento.pos):

                    sonido_click.play()
                    nueva_partida()

            # ==================================
            # BOTONES DURANTE LA PARTIDA
            # ==================================

            elif not jugador_plantado and not dealer_juega:

                # ==================================
                # BOTÓN PEDIR CARTA
                # ==================================

                if boton_pedir.collidepoint(evento.pos):

                    sonido_click.play()

                    if jugando_mano_2:
                        mano_activa = mano_jugador_2
                    else:
                        mano_activa = mano_jugador

                    puntosjugador = pedir_carta(
                        mazo,
                        mano_activa
                    )

                    print("Mano 1:", mano_jugador)
                    print("Mano 2:", mano_jugador_2)
                    print("Puntos mano activa:", puntosjugador)

                    # SI EL JUGADOR SE PASA DE 21

                    if puntosjugador > 21:

                        print("PERDISTE ESTA MANO")

                        if jugador_dividio:

                            if not jugando_mano_2:

                                mano_1_terminada = True
                                jugando_mano_2 = True

                                mensaje_estado = "PERDISTE MANO 1"

                                print("AHORA JUEGAS CON LA MANO 2")

                            else:

                                mano_2_terminada = True

                                mensaje_estado = "MANO 2 PERDIDA"

                                # COMPROBAR SI AMBAS MANOS TERMINARON

                                if (
                                    mano_1_terminada
                                    and mano_2_terminada
                                ):

                                    finalizar_partida(True)

                        else:

                            jugador_perdio = True
                            mano_1_terminada = True

                            mensaje_estado = "TE PASASTE, DEALER GANA"

                            # EL DEALER NO NECESITA ROBAR

                            finalizar_partida(False)


                # ==================================
                # BOTÓN DIVIDIR
                # ==================================

                if (
                    boton_dividir.collidepoint(evento.pos)
                    and puede_dividir(mano_jugador)
                    and not jugador_dividio
                    and not jugador_plantado
                ):

                    sonido_click.play()

                    mano_jugador_2.append(mano_jugador[1])
                    mano_jugador.pop()

                    mano_jugador.append(repartir_carta(mazo))
                    mano_jugador_2.append(repartir_carta(mazo))

                    jugando_mano_2 = False
                    jugador_dividio = True

                    mensaje_estado = "MANOS DIVIDIDAS"

                    print("EL JUGADOR DIVIDIÓ")
                    print("Mano 1:", mano_jugador)
                    print("Mano 2:", mano_jugador_2)


                # ==================================
                # BOTÓN PLANTARSE
                # ==================================

                if boton_plantarse.collidepoint(evento.pos):

                    sonido_click.play()

                    if jugador_dividio and not jugando_mano_2:

                        mano_1_terminada = True
                        jugando_mano_2 = True

                        mensaje_estado = "MANO 1 TERMINADA"

                        print("MANO 1 TERMINADA")
                        print("AHORA JUEGAS CON LA MANO 2")

                    else:

                        if jugador_dividio:

                            mano_2_terminada = True

                        else:

                            mano_1_terminada = True

                        mensaje_estado = "TERMINASTE TURNO"

                        print("JUGADOR TERMINÓ SU TURNO")

                    # COMPROBAR SI TODAS LAS MANOS TERMINARON

                    if (
                        mano_1_terminada
                        and (
                            mano_2_terminada
                            or not jugador_dividio
                        )
                    ):

                        print("EL JUGADOR TERMINÓ TODAS SUS MANOS")

                        mensaje_estado = "PARTIDA TERMINADA"

                        finalizar_partida(True)


    # ==================================
    # DIBUJAR INTERFAZ
    # ==================================

    pantalla.blit(fondo_mesa, (0, 0))


    # ==================================
    # ELEMENTOS DECORATIVOS
    # ==================================

    pantalla.blit(imagen_vaso, esp_vaso)
    pantalla.blit(imagen_dolar, esp_dolar)


    # ==================================
    # DIBUJAR BOTONES
    # ==================================

    if not jugador_plantado:

        pantalla.blit(imagen_pedir, boton_pedir)

        pantalla.blit(imagen_plantarse, boton_plantarse)

    if (
        puede_dividir(mano_jugador)
        and not jugador_plantado
        and not jugador_dividio
    ):

        pantalla.blit(imagen_dividir, boton_dividir)

    if jugador_plantado and dealer_juega:

        pantalla.blit(imagen_volver, boton_volver)


    # ==================================
    # DIBUJAR CARTAS DEL JUGADOR
    # ==================================

    if not jugador_dividio:

        posicion_x = 310

        for carta in mano_jugador:

            imagen = cargar_imagen_carta(carta)

            pantalla.blit(
                imagen,
                (posicion_x, 410)
            )

            posicion_x += 90

    else:

        # MANO 1

        posicion_x1 = 310
        posicion_y1 = 410

        for carta in mano_jugador:

            imagen = cargar_imagen_carta(carta)

            pantalla.blit(
                imagen,
                (posicion_x1, posicion_y1)
            )

            posicion_y1 += 60

        # MANO 2

        posicion_x2 = 580
        posicion_y2 = 410

        for carta in mano_jugador_2:

            imagen = cargar_imagen_carta(carta)

            pantalla.blit(
                imagen,
                (posicion_x2, posicion_y2)
            )

            posicion_y2 += 60


    # ==================================
    # DIBUJAR CARTAS DEL DEALER
    # ==================================

    posicion_x1 = 570

    for i, carta in enumerate(mano_dealer):

        if i == 0 and not jugador_plantado:

            imagen = cargar_imagen_carta(
                carta,
                True
            )

        else:

            imagen = cargar_imagen_carta(carta)

        pantalla.blit(
            imagen,
            (posicion_x1, 250)
        )

        posicion_x1 -= 90


    # ==================================
    # DIBUJAR PUNTAJES
    # ==================================

    puntos_actuales1 = calcular_puntos(mano_jugador)

    texto_puntos1 = fuente.render(
        f"TUS PUNTOS: {puntos_actuales1}",
        True,
        BLANCO
    )

    pantalla.blit(texto_puntos1, (70, 70))


    if jugador_dividio:

        puntos_actuales2 = calcular_puntos(
            mano_jugador_2
        )

        texto_puntos2 = fuente.render(
            f"PUNTOS EN MANO 2: {puntos_actuales2}",
            True,
            BLANCO
        )

        pantalla.blit(texto_puntos2, (70, 100))


    # ==================================
    # PUNTAJE DEL DEALER
    # ==================================

    if jugador_plantado:

        texto_dealer = fuente.render(
            f"PUNTOS DEALER: {puntosdealer}",
            True,
            BLANCO
        )

    else:

        texto_dealer = fuente.render(
            "PUNTOS DEALER: --",
            True,
            BLANCO
        )

    pantalla.blit(texto_dealer, (725, 70))


    # ==================================
    # RESULTADOS FINALES
    # ==================================

    if jugador_plantado:

        texto_resultado1 = fuente_resultado.render(
            resultado_mano1,
            True,
            BLANCO
        )

        pantalla.blit(
            texto_resultado1,
            (400, 70)
        )

        if jugador_dividio:

            texto_resultado2 = fuente_resultado.render(
                resultado_mano2,
                True,
                BLANCO
            )

            pantalla.blit(
                texto_resultado2,
                (400, 100)
            )


    # ==================================
    # ACTUALIZAR PANTALLA
    # ==================================

    pygame.display.flip()

    reloj.tick(60)


# ==================================
# CERRAR JUEGO
# ==================================

pygame.quit()


