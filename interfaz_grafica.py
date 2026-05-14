import flet as ft
import math
from logica import ArbolBinario


def main(page: ft.Page):
    page.title = "Visualizador de Árboles - Proyecto 2"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20
    mi_arbol = ArbolBinario()
    lienzo = ft.canvas.Canvas(width=800,height=600,expand=True)

    def dibujar_arbol_en_lienzo(nodo):
        if nodo is not None:
            if nodo.izquierdo:
                lienzo.shapes.append(ft.canvas.Line(nodo.x, nodo.y, nodo.izquierdo.x, nodo.izquierdo.y, paint=ft.Paint(stroke_width=2, color=ft.colors.WHITE54)))
                dibujar_arbol_en_lienzo(nodo.izquierdo)
            if nodo.derecho:
                lienzo.shapes.append(ft.canvas.Line(nodo.x, nodo.y, nodo.derecho.x, nodo.derecho.y, paint=ft.Paint(stroke_width=2, color=ft.colors.WHITE54)))
                dibujar_arbol_en_lienzo(nodo.derecho)
            lienzo.shapes.append(ft.canvas.Circle(nodo.x, nodo.y, 20, paint=ft.Paint(color=ft.colors.BLUE_700)))
            lienzo.shapes.append(ft.canvas.Text(nodo.x - 10, nodo.y - 10, text=str(nodo.valor), style=ft.TextStyle(size=16, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE)))

    def btn_insertar_click(e):
        try:
            valor = int(txt_valor.value)
            mi_arbol.insertar(valor)
            txt_valor.value = ""
            mi_arbol.calcular_posiciones(lienzo.width)
            lienzo.shapes.clear()
            dibujar_arbol_en_lienzo(mi_arbol.raiz)
            page.update()

        except ValueError:
            pass

    txt_valor = ft.TextField(label="Valor del Nodo", width=150)
    btn_insertar = ft.ElevatedButton("Insertar", on_click=btn_insertar_click)
    panel_control = ft.Column([txt_valor, btn_insertar], width=200)
    page.add(ft.Row([panel_control, ft.Container(content=lienzo, bgcolor=ft.colors.BLACK87, border_radius=10, expand=True)], expand=True))

ft.app(target=main)