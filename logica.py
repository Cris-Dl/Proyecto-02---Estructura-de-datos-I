import flet as ft
import flet.canvas as cv

class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izquierdo = None
        self.derecho = None
        self.x = 0
        self.y = 0
        self.altura = 1

class ArbolBinario:
    def __init__(self):
        self.raiz = None

    def insertar(self, valor):
        if self.raiz is None:
            self.raiz = Nodo(valor)
            return
        cola = [self.raiz]
        while cola:
            nodo = cola.pop(0)
            if nodo.izquierdo is None:
                nodo.izquierdo = Nodo(valor)
                break
            else:
                cola.append(nodo.izquierdo)

            if nodo.derecho is None:
                nodo.derecho = Nodo(valor)
                break
            else:
                cola.append(nodo.derecho)

    def calcular_posiciones(self, ancho_lienzo):
        if self.raiz is not None:
            self._calcular_coordenadas(self.raiz, 0, ancho_lienzo / 2, 50, ancho_lienzo / 4, 80)

    def _calcular_coordenadas(self, nodo, nivel, x, y, desplazamiento, espaciado_y):
        if nodo is not None:
            nodo.x = x
            nodo.y = y
            self._calcular_coordenadas(nodo.izquierdo, nivel + 1, x - desplazamiento, y + espaciado_y, desplazamiento / 2, espaciado_y)
            self._calcular_coordenadas(nodo.derecho, nivel + 1, x + desplazamiento, y + espaciado_y, desplazamiento / 2, espaciado_y)

class ArbolBST(ArbolBinario):
    def insertar(self, valor):
        if self.raiz is None:
            self.raiz = Nodo(valor)
        else:
            self._insertar_recursivo(self.raiz, valor)

    def _insertar_recursivo(self, nodo, valor):
        if valor < nodo.valor:
            if nodo.izquierdo is None:
                nodo.izquierdo = Nodo(valor)
            else:
                self._insertar_recursivo(nodo.izquierdo, valor)
        elif valor > nodo.valor:
            if nodo.derecho is None:
                nodo.derecho = Nodo(valor)
            else:
                self._insertar_recursivo(nodo.derecho, valor)

class ArbolAVL(ArbolBST):
    def insertar(self, valor):
        super().insertar(valor)

def main(page: ft.Page):
    page.title = "Visualizador de Árboles - Proyecto 2"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20
    mi_arbol = ArbolBST()
    lienzo = cv.Canvas(width=800, height=600, expand=True)

    def dibujar_arbol_en_lienzo(nodo):
        if nodo is not None:
            if nodo.izquierdo:
                lienzo.shapes.append(cv.Line(nodo.x, nodo.y, nodo.izquierdo.x, nodo.izquierdo.y, paint=ft.Paint(stroke_width=2, color=ft.Colors.WHITE54)))
                dibujar_arbol_en_lienzo(nodo.izquierdo)
            if nodo.derecho:
                lienzo.shapes.append(cv.Line(nodo.x, nodo.y, nodo.derecho.x, nodo.derecho.y, paint=ft.Paint(stroke_width=2, color=ft.Colors.WHITE54)))
                dibujar_arbol_en_lienzo(nodo.derecho)
            lienzo.shapes.append(cv.Circle(nodo.x, nodo.y, 20, paint=ft.Paint(color=ft.Colors.BLUE_700)))
            lienzo.shapes.append(cv.Text(nodo.x - 10, nodo.y - 10, str(nodo.valor), style=ft.TextStyle(size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)))

    def cambiar_tipo_arbol(e):
        nonlocal mi_arbol
        tipo = selector_arbol.value
        if tipo == "Binario":
            mi_arbol = ArbolBinario()
        elif tipo == "BST":
            mi_arbol = ArbolBST()
        elif tipo == "AVL":
            mi_arbol = ArbolAVL()
        lienzo.shapes.clear()
        page.update()

    async def btn_insertar_click(e):
        try:
            valor = int(txt_valor.value)
            mi_arbol.insertar(valor)
            txt_valor.value = ""
            await txt_valor.focus()
            mi_arbol.calcular_posiciones(lienzo.width)
            lienzo.shapes.clear()
            dibujar_arbol_en_lienzo(mi_arbol.raiz)
            page.update()
        except ValueError:
            pass
    selector_arbol = ft.Dropdown(
        label="Tipo de Árbol",
        options=[ft.dropdown.Option("Binario"), ft.dropdown.Option("BST"), ft.dropdown.Option("AVL"),],
        value="BST",
        width=180,
        on_select=cambiar_tipo_arbol)
    txt_valor = ft.TextField(label="Valor del Nodo", width=180)
    btn_insertar = ft.Button("Insertar", on_click=btn_insertar_click, width=180)
    panel_control = ft.Column([ft.Text("Controles", size=20, weight=ft.FontWeight.BOLD), selector_arbol, txt_valor, btn_insertar], width=200)
    page.add(ft.Row([panel_control,ft.Container(content=lienzo, bgcolor=ft.Colors.BLACK87, border_radius=10, expand=True)], expand=True))

ft.run(main)